import os
import sys

import dttlz

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'dttlz'
]

requires = []

setup(
    name='dttlz',
    version=dttlz.__version__,
    description='Python data tools.',
    long_description=open('README.markdown').read(),
    author='Adam Tauber',
    author_email='asciimoo@gmail.com',
    url='http://github.com/asciimoo/dttlz',
    packages=packages,
    package_dir={'dttlz': 'dttlz'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Affero General Public License v3'
    ),
)
