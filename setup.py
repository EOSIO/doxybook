from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='doxybook',
    version='2.1.6',
    description='Convert Doxygen XML to GitBook or Vuepress or Gatsby markdown files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/matusnovak/doxybook',
    author='Matus Novak',
    author_email='matusnov@gmail.com',
    license='MIT',
    keywords='doxygen gitbook vuepress markdown generator',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'doxybook=doxybook:main',
        ],
    },
)
