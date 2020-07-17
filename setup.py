#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/27 14:13
# @Author  : Xingqi Tang
# @Contact : xingqitangatgmaildotcom
# @File    : setup.py
# @Software: PyCharm
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xq-fund",
    version="0.0.1",
    author="xingqi",
    author_email="xingqitang@gmail.com",
    description="A small package for check fund status",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers={
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    },
    python_requires='>=3.6',
)
