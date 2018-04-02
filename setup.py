#!/usr/bin/env python

from setuptools import setup, Extension

python_libstorj_module = Extension('_python_libstorj',
                                   sources=[
                                       'lib/ext/python_libstorj_wrap.cxx',
                                       'lib/ext/python_libstorj.cpp'
                                   ],
                                   libraries=['storj']
                                   )

setup(name='python_libstorj',
      version='1.0a2',
      author="Bryan White",
      author_email="bryanchriswhite@gmail.com",
      url="https://github.com/storj/python-libstorj",
      description="""Python bindings for [libstorj](https://github.com/storj/libstorj)""",
      long_description="""See https://github.com/storj/python-libstorj""",
      ext_modules=[python_libstorj_module],
      packages=['python_libstorj', 'python_libstorj.ext'],
      package_dir={'python_libstorj': 'lib'},
      install_requires=['pyyaml'],
      )
