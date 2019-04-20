# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='python-hearthis',
    version='1.0.0',
    url='https://github.com/jinchuuriki91/python-hearthis',
    license='MIT',
    platforms=['OS Independent'],
    description="Unofficial Python library for hearthis.io API https://hearthis.at/api-v2/",
    install_requires=[
        'requests>=2.21.0'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Gandhar Pednekar',
    author_email='gandhar.pednekar15@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='python library requests hearthis API',
)