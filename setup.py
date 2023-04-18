from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


def version():
    about_file = "natt/about.py"
    with open(about_file) as f:
        exec(compile(f.read(), about_file, "exec"))
    return locals()["__version__"]


setup(
    name='natt',
    version=version(),
    description='natt is Not Another Time Tracker',
    long_description=readme(),
    author='Jean-Christophe Fabre',
    author_email='jean-christophe.fabre@inrae.fr',
    url='https://github.com/jctophefabre/natt',
    license='GPLv3',
    packages=['natt'],
    package_data={
        'natt': []
    },
    entry_points={
        'console_scripts': [
            'natt=natt.__main__:main'
        ]
    },
    install_requires=[
        'argparse',
        'pyexcel-ods'
    ],
    python_requires='~=3.9',
)
