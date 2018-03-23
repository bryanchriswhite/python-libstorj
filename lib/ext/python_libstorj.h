#include "storj.h"
#include "uv.h"
#include "Python.h"


void get_info(storj_env_t *env, PyObject *handle);
void get_info_cb(uv_work_t *work_req, int status);
// Buckets
void create_bucket(storj_env_t *env, PyObject *name, PyObject *handle);
void create_bucket_cb(uv_work_t *work_req, int status);
void delete_bucket(storj_env_t *env, PyObject *id, PyObject *handle);
void delete_bucket_cb(uv_work_t *work_req, int status);
void get_bucket_id(storj_env_t *env, PyObject *name, PyObject *handle);
void get_bucket_id_cb(uv_work_t *work_req, int status);
void list_buckets(storj_env_t *env, PyObject *handle);
void list_buckets_cb(uv_work_t *work_req, int status);
// Files
void delete_file(storj_env_t *env, PyObject *bucket_id, PyObject *file_id, PyObject *handle);
void delete_file_cb(uv_work_t *work_req, int status);
void list_files(storj_env_t *env, PyObject *py_bucket_id, PyObject *callback);
void list_files_cb(uv_work_t *work_req, int status);
//void store_file_progress_callback_cb(double progress, uint64_t bytes, uint64_t total_bytes, void *handle);
//void store_file_finished_callback_cb(int error_status, char *file_id, void *handle);
//
storj_upload_state_t* store_file(storj_env_t *env, storj_upload_opts_t *upload_options, PyObject *progress_callback, PyObject *finished_callback);
uv_loop_t *set_loop(storj_env_t *env);
void run(uv_loop_t *loop);
