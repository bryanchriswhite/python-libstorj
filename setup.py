#!/usr/bin/env python

from distutils.core import setup, Extension

python_libstorj_module = Extension('_python_libstorj',
                                   sources=['python_libstorj_wrap.cxx', 'python_libstorj.cpp'],
                                   )

setup(name='python_libstorj',
      version='0.0',
      author="Bryan White <bryanchriswhite@gmail.com>",
      description="""Python bindings for [libstorj](https://github.com/storj/libstorj)""",
      ext_modules=[python_libstorj_module],
      py_modules=["python_libstorj"],
      )
