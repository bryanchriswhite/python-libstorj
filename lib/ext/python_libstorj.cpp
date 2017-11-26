#include "python_libstorj.h"
#include "storj.h"
#include "uv.h"
#include "Python.h"
#include "typeinfo"

template <typename ReqType>
bool error_and_status_check(ReqType *req, char **error) {
    char *_error = NULL;
    if (req->error_code) {
        *error = (char *)curl_easy_strerror((CURLcode)req->error_code);
    } else if (req->status_code > 399) {
        *error = storj_strerror(req->status_code);
    } else {
        return true;
    }

    return false;
}

void get_info_cb(uv_work_t *work_req, int status) {
    char *error = NULL;
    char *result = NULL;
    json_request_t *req = (json_request_t *)work_req->data;
    PyObject *_handle = (PyObject *)req->handle;

    if (error_and_status_check<json_request_t>(req, &error)) {
        result = (char *)json_object_to_json_string(req->response);
    }

    PyObject_CallFunction(_handle, "ss", error, result);
}

void list_buckets_cb(uv_work_t *work_req, int status) {
    char *error_str = NULL;
    PyObject *error = Py_None;
    PyObject *bucket_list = Py_None;
    get_buckets_request_t *req = (get_buckets_request_t *)work_req->data;
    PyObject *_handle = (PyObject *)req->handle;

    if (error_and_status_check<get_buckets_request_t>(req, &error_str)) {
        bucket_list = PyList_New(req->total_buckets);
        for (uint8_t i=0; i<req->total_buckets; i++) {
            PyObject *bucket_dict = PyDict_New();
            PyDict_SetItemString(bucket_dict,"name", PyString_FromString(req->buckets[i].name));
            PyDict_SetItemString(bucket_dict,"id", PyString_FromString(req->buckets[i].id));
            PyDict_SetItemString(bucket_dict,"decrypted", PyBool_FromLong((long)req->buckets[i].decrypted));
            PyDict_SetItemString(bucket_dict,"created", PyString_FromString(req->buckets[i].created));
            PyList_SetItem(bucket_list, i, bucket_dict);
        }
    } else {
        bucket_list = PyList_New(0);
        error = PyString_FromString(error_str);
    }

    PyObject *args_tuple = PyTuple_New(2);
    PyTuple_SetItem(args_tuple, 0, error);
    PyTuple_SetItem(args_tuple, 1, bucket_list);
    PyObject_CallObject(_handle, args_tuple);
}

void create_bucket_cb(uv_work_t *work_req, int status) {
    char *error_str = NULL;
    PyObject *error = Py_None;
    PyObject *bucket = Py_None;
    create_bucket_request_t *req = (create_bucket_request_t *)work_req->data;
    PyObject *_handle = (PyObject *)req->handle;

    if (error_and_status_check<create_bucket_request_t>(req, &error_str)) {
        bucket = PyDict_New();
        PyDict_SetItemString(bucket, "name", PyString_FromString(req->bucket->name));
        PyDict_SetItemString(bucket, "id", PyString_FromString(req->bucket->id));
        PyDict_SetItemString(bucket, "decrypted", PyBool_FromLong((long)req->bucket->decrypted));
    } else {
        error =  PyString_FromString(error_str);
    }

    PyObject *args_tuple = PyTuple_New(2);
    PyTuple_SetItem(args_tuple, 0, error);
    PyTuple_SetItem(args_tuple, 1, bucket);
    PyObject_CallObject(_handle, args_tuple);
}

void get_info(storj_env_t *env, PyObject *callback) {
    void *void_callback = (void *)callback;
    storj_bridge_get_info(env, void_callback, get_info_cb);
}

void list_buckets(storj_env_t *env, PyObject *callback) {
    void *void_callback = (void *)callback;
    storj_bridge_get_buckets(env, void_callback, list_buckets_cb);
}

void create_bucket(storj_env_t *env, PyObject *py_name, PyObject *callback) {
    void *void_callback = (void *)callback;
    char *name = PyString_AsString(py_name);
    storj_bridge_create_bucket(env, name, void_callback, create_bucket_cb);
}

void run(uv_loop_t *loop) {
    uv_run(loop, UV_RUN_DEFAULT);
}

uv_loop_t *set_loop(storj_env_t *env) {
    uv_loop_t *loop = (uv_loop_t *)malloc(sizeof(uv_loop_t));
    uv_loop_init(loop);
    env->loop = loop;
    return loop;
}
