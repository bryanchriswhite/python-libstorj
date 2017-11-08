`python_libstorj`
===

Dependencies
---
+ python 2.7
+ [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)


Environment Setup
---
1. Setup a virtualenv
    ```
    virtualenv env
    ```
1. Activate your virtualenv
    ```
    source ./env/bin/activate
    ```
1. Installing project dependencies
    ```
    pip install -r
    ```

Build
---
1. Run swig to generate c++/python
    ```
    swig -c++ -python ./python_libstorj.i
    ```
1. Run setup.py to build shared object
    ```
    python ./setup.py build_ext --inplace
    ```
