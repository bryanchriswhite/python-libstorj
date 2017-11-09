%module python_libstorj

%{
#define SWIG_FILE_WITH_INIT
#include "python_libstorj.h"
#include "storj.h"
%}

%include <stdint.i>
%include <cstring.i>
%cstring_output_allocate(char **buffer, free(*$1));
int storj_mnemonic_generate(int strength, char **buffer);

%include "ext/libstorj/src/storj.h"