__license__ = "MIT"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inrae.fr>"

import argparse
import datetime
import pyexcel_ods

from . import config
from .about import __version__


def load_data(filename, begin_date=None, end_date=None):
    data = pyexcel_ods.get_data(filename)
    filtered_data = list()
    for record in data['Activity'][1:]:
        is_accepted_record = (len(record) > 0
                              and (begin_date is None or (begin_date is not None and record[0] >= begin_date))
                              and (end_date is None or (end_date is not None and record[0] <= end_date)))
        if is_accepted_record:
            filtered_data.append(record)

    return filtered_data


def get_week_range(ref_date):

    year, week, dow = ref_date.isocalendar()

    if dow == 7:
        start_date = ref_date
    else:
        start_date = ref_date - datetime.timedelta(dow)
    end_date = start_date + datetime.timedelta(6)

    return (start_date.date(), end_date.date())


def week_board(filename, date_str):
    ref_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    begin_date, end_date = get_week_range(ref_date)

    data = load_data(filename, begin_date, end_date)
    stats = dict()

    # sorted list of week dates
    date_list = sorted([end_date - datetime.timedelta(days=x) for x in range(0, 7)])

    # initialize stats
    for d in date_list:
        stats[d] = 0

    # dispatch stats by date
    for record in data:
        stats[record[0]] += record[1]

    # initialize balance and board
    balance = 0
    total = 0
    other_days = 0
    board = dict()

    # dispatch stats in work days and other days
    for k, v in stats.items():
        day_name = k.strftime('%A')
        if day_name in ['Saturday', 'Sunday']:
            other_days += v
        else:
            if day_name not in board:
                board[day_name] = 0
            board[day_name] += v

    # work days : print and compute balance
    print('=== Week from {} to {} ==='.format(begin_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    for k, v in board.items():
        if v > 0:
            day_balance = (v-config.HOURS_BY_DAY)
            balance += day_balance
            total += v
            print('{:>12s} : {:>1.2f} ({:+1.2f})'.format(k, v, day_balance))
        else:
            print('{:>12s} : no data'.format(k))

    # other days : compute balance
    if other_days > 0:
        balance += other_days
        total += other_days
        print('{:>12s} : {:>1.2f} ({:+1.2f})'.format('Other days', other_days, other_days))
    else:
        print('{:>12s} : no data'.format('Other days'))

    # other days : print
    print('------------------------------------')
    # print('  Week total : {:>1.2f} ({:+1.2f})'.format(Total,Balance))
    print('  Week total : {:>1.2f}'.format(total))
    print('Week balance : {:+1.2f}'.format(total-config.HOURS_BY_WEEK))
    print('Week achievement : {:1.0f}%'.format((total/config.HOURS_BY_WEEK)*100))


def year_board(filename, date_str):
    ref_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    year = ref_date.year
    begin_date = datetime.datetime(int(year), 1, 1).date()
    end_date = datetime.datetime(int(year), 12, 31).date()

    data = load_data(filename, begin_date, end_date)
    balance_by_week = dict()

    week_nbr = 0

    for record in data:
        week_nbr = record[0].isocalendar().week
        if week_nbr == 52 and record[0].month == 1:
            pass  # ignore week 52 when it is the end of year n-1 during first week of january of year n
        else:
            if week_nbr not in balance_by_week:
                balance_by_week[week_nbr] = -config.HOURS_BY_WEEK
            balance_by_week[week_nbr] += record[1]

    balance_full = 0.0

    for k, v in balance_by_week.items():
        print('week {:>2d} : {:>+1.2f}'.format(k, v))
        balance_full += v

    print()
    print('year balance : {:>+1.2f}'.format(balance_full))


def run(cmd_args):

    if cmd_args['board'] == "week":
        week_board(cmd_args['path'], cmd_args['date'])
        return 0
    elif cmd_args['board'] == "year":
        year_board(cmd_args['path'], cmd_args['date'])
        return 0
    else:
        print("unknown board type, aborting.")
    return 127


def main():

    parser = argparse.ArgumentParser(description="natt is not a time tracker")

    parser.add_argument("path", type=str)
    parser.add_argument("--board", "-b", type=str, default="week")
    parser.add_argument("--date", "-d", type=str, default=datetime.datetime.today().strftime('%Y-%m-%d'))
    parser.add_argument("--version", action="version", version=__version__)

    return run(vars(parser.parse_args()))


if __name__ == '__main__':
    main()
