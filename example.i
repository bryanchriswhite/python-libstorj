/* File: example.i */
%module example

%{
#define SWIG_FILE_WITH_INIT
#include "example.h"
#include "storj.h"
%}

int fact(int n);
bool storj_mnemonic_check(const char *mnemonic);
