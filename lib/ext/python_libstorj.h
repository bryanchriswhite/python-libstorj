#include "storj.h"
#include "uv.h"
#include "Python.h"

void get_info(storj_env_t *env, PyObject *handle);

// Buckets
void create_bucket(storj_env_t *env, PyObject *name, PyObject *handle);
void delete_bucket(storj_env_t *env, PyObject *id, PyObject *handle);
void get_bucket_id(storj_env_t *env, PyObject *name, PyObject *handle);
void list_buckets(storj_env_t *env, PyObject *handle);

// Files
void delete_file(storj_env_t *env, PyObject *bucket_id, PyObject *file_id, PyObject *handle);
void list_files(storj_env_t *env, PyObject *py_bucket_id, PyObject *callback);
storj_upload_state_t* store_file(storj_env_t *env, storj_upload_opts_t *upload_options, PyObject *progress_callback, PyObject *finished_callback);
storj_download_state_t* resolve_file(storj_env_t *env, PyObject *bucket_id, PyObject *file_id, PyObject *destination, PyObject *progress_callback, PyObject *finished_callback);

// Libuv
uv_loop_t *set_loop(storj_env_t *env);
void run(uv_loop_t *loop);
