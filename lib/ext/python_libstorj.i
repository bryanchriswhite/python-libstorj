%module python_libstorj

%{
#define SWIG_FILE_WITH_INIT
#include "python_libstorj.h"
#include "storj.h"
#include "uv.h"
#include "Python.h"
#include "stdio.h"
%}

%include <stdint.i>
%include <cstring.i>

%cstring_output_allocate(char **buffer, free(*$1));
int storj_mnemonic_generate(int strength, char **buffer);

%rename(HttpOptions) storj_http_options;
%rename(EncryptOptions) storj_encrypt_options;
%rename(LogOptions) storj_log_options;
%rename(BridgeOptions) storj_bridge_options_t;
%rename(UploadState) storj_upload_state_t;
%rename(init_env) storj_init_env;
%rename(destroy_env) storj_destroy_env;
%rename(strerror) storj_strerror;

%include "storj.h"
%include "python_libstorj.h"

FILE *fopen(const char *pathname, const char *mode);
%constant FILE *fopen(const char *pathname, const char *mode);

void get_info(storj_env_t *env, PyObject *callback);
%constant void get_info(storj_env_t *env, PyObject *callback);

void create_bucket(storj_env_t *env, PyObject *name, PyObject *callback);
%constant void create_bucket(storj_env_t *env, PyObject *name, PyObject *callback);

void delete_bucket(storj_env_t *env, PyObject *id, PyObject *handle);
%constant void delete_bucket(storj_env_t *env, PyObject *id, PyObject *callback);

void list_buckets(storj_env_t *env, PyObject *callback);
%constant void list_buckets(storj_env_t *env, PyObject *callback);

void list_files(storj_env_t *env, PyObject *py_bucket_id, PyObject *callback);
%constant void list_files(storj_env_t *env, PyObject *py_bucket_id, PyObject *callback);

//void store_file_progress_callback_cb(double progress, uint64_t bytes, uint64_t total_bytes, void *handle);
//%constant void store_file_progress_callback_cb(double progress, uint64_t bytes, uint64_t total_bytes, void *handle);
//
//void store_file_finished_callback_cb(int error_status, char *file_id, void *handle);
//%constant void store_file_finished_callback_cb(int error_status, char *file_id, void *handle);

storj_upload_state_t* store_file(storj_env_t *env, storj_upload_opts_t *upload_options, PyObject *progress_callback, PyObject *finished_callback);
%constant storj_upload_state_t* store_file(storj_env_t *env, storj_upload_opts_t *upload_options, PyObject *progress_callback, PyObject *finished_callback);

void run(uv_loop_t *loop);
