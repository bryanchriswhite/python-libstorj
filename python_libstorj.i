%module python_libstorj

%{
#define SWIG_FILE_WITH_INIT
#include "python_libstorj.h"
#include "storj.h"
#include "uv.h"
#include "Python.h"
%}

%include <stdint.i>
%include <cstring.i>

%cstring_output_allocate(char **buffer, free(*$1));
int storj_mnemonic_generate(int strength, char **buffer);

%rename(HttpOptions) storj_http_options;
%rename(EncryptOptions) storj_encrypt_options;
%rename(LogOptions) storj_log_options;
%rename(BridgeOptions) storj_bridge_options_t;
%rename(init_env) storj_init_env;

%include "ext/libstorj/src/storj.h"
%include "python_libstorj.h"

void get_info(storj_env_t *env, PyObject *handle);
%constant void get_info(storj_env_t *env, PyObject *handle);
void run(uv_loop_t *loop);
