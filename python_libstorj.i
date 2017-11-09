%module python_libstorj

%{
#define SWIG_FILE_WITH_INIT
#include "python_libstorj.h"
#include "storj.h"
%}

%include <cstring.i>
%cstring_output_allocate(char **buffer, free(*$1));

bool storj_mnemonic_check(const char *mnemonic);
int storj_mnemonic_generate(int strength, char **buffer);
