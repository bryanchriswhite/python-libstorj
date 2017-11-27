#include "storj.h"
#include "uv.h"
#include "Python.h"


void get_info(storj_env_t *env, PyObject *handle);
void get_info_cb(uv_work_t *work_req, int status);
void create_bucket(storj_env_t *env, PyObject *name, PyObject *handle);
void create_bucket_cb(uv_work_t *work_req, int status);
void delete_bucket(storj_env_t *env, PyObject *id, PyObject *handle);
void delete_bucket_cb(uv_work_t *work_req, int status);
void list_buckets(storj_env_t *env, PyObject *handle);
void list_buckets_cb(uv_work_t *work_req, int status);
void list_files(storj_env_t *env, PyObject *py_bucket_id, PyObject *callback);
void list_files_cb(uv_work_t *work_req, int status);
uv_loop_t *set_loop(storj_env_t *env);
void run(uv_loop_t *loop);
