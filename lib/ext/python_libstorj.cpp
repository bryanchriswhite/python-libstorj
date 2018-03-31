#include "storj.h"
#include "uv.h"
#include "Python.h"
#include "typeinfo"

bool status_check(int status_code, char **error) {
    if (status_code > 0) {
        char *storj_error = storj_strerror(status_code);
        // TODO: should this be 254 or is 255 okay?
        snprintf(*error, 254, "%s: status code %i", storj_error, status_code);
        return false;
    }

    return true;
}

template <typename ReqType>
bool error_and_status_check(ReqType *req, char **error) {
    if (req->error_code) {
        *error = (char *)curl_easy_strerror((CURLcode)req->error_code);
    } else if (req->status_code > 399) {
        return status_check(req->status_code, error);
    } else {
        *error = NULL;
        return true;
    }

    return false;
}

void get_info_cb(uv_work_t *work_req, int status) {
    char *error = (char *)calloc(255, sizeof(char));
    char *result = NULL;
    json_request_t *req = (json_request_t *)work_req->data;
    PyObject *_handle = (PyObject *)req->handle;

    if (error_and_status_check<json_request_t>(req, &error)) {
        result = (char *)json_object_to_json_string(req->response);
    }

    PyObject_CallFunction(_handle, "ss", error, result);
}

void create_bucket_cb(uv_work_t *work_req, int status) {
    char *error_str = (char *)calloc(255, sizeof(char));
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

void delete_bucket_cb(uv_work_t *work_req, int status) {
    char *error_str = (char *)calloc(255, sizeof(char));
    json_request_t *req = (json_request_t *)work_req->data;
    PyObject *_handle = (PyObject *)req->handle;

    error_and_status_check<json_request_t>(req, &error_str);
    PyObject_CallFunction(_handle, "s", error_str);
}

void get_bucket_id_cb(uv_work_t *work_req, int status) {
    char *error_str = (char *)calloc(255, sizeof(char));
    PyObject *error = Py_None;
    get_bucket_id_request_t *req = (get_bucket_id_request_t *)work_req->data;
    PyObject *_handle = (PyObject *)req->handle;

    PyObject *bucket_dict = PyDict_New();
    if (error_and_status_check<get_bucket_id_request_t>(req, &error_str)) {
        PyDict_SetItemString(bucket_dict, "name", PyString_FromString(req->bucket_name));
        PyDict_SetItemString(bucket_dict, "id", PyString_FromString(req->bucket_id));
        // TODO: manage encrypted bucket name
    } else {
        error = PyString_FromString(error_str);
    }

    PyObject *args_tuple = PyTuple_New(2);
    PyTuple_SetItem(args_tuple, 0, error);
    PyTuple_SetItem(args_tuple, 1, bucket_dict);
    PyObject_CallObject(_handle, args_tuple);
}

void list_buckets_cb(uv_work_t *work_req, int status) {
    char *error_str = (char *)calloc(255, sizeof(char));
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

void delete_file_cb(uv_work_t *work_req, int status) {
    char *error_str = (char *)calloc(255, sizeof(char));
    json_request_t *req = (json_request_t *)work_req->data;
    PyObject *_handle = (PyObject *)req->handle;

    error_and_status_check<json_request_t>(req, &error_str);
    PyObject_CallFunction(_handle, "s", error_str);
}

void list_files_cb(uv_work_t *work_req, int status) {
    char *error_str = (char *)calloc(255, sizeof(char));
    PyObject *error = Py_None;
    PyObject *file_list = Py_None;
    list_files_request_t *req = (list_files_request_t *)work_req->data;
    PyObject *_handle = (PyObject *)req->handle;

    if (error_and_status_check<list_files_request_t>(req, &error_str)) {
        file_list = PyList_New(req->total_files);
        for (uint8_t i=0; i<req->total_files; i++) {
            PyObject *file_dict = PyDict_New();
            PyDict_SetItemString(file_dict,"filename", PyString_FromString(req->files[i].filename));
            PyDict_SetItemString(file_dict,"id", PyString_FromString(req->files[i].id));
            PyDict_SetItemString(file_dict,"decrypted", PyBool_FromLong((long)req->files[i].decrypted));
            PyDict_SetItemString(file_dict,"created", PyString_FromString(req->files[i].created));
            PyDict_SetItemString(file_dict,"size", Py_BuildValue("k", req->files[i].size));
            PyDict_SetItemString(file_dict,"mimetype", PyString_FromString(req->files[i].mimetype));
            PyList_SetItem(file_list, i, file_dict);
        }
    } else {
        file_list = PyList_New(0);
        error = PyString_FromString(error_str);
    }

    PyObject *args_tuple = PyTuple_New(2);
    PyTuple_SetItem(args_tuple, 0, error);
    PyTuple_SetItem(args_tuple, 1, file_list);
    PyObject_CallObject(_handle, args_tuple);
}

void store_file_progress_callback_cb(double progress,
                                     uint64_t bytes,
                                     uint64_t total_bytes,
                                     void *handle) {
    PyObject *py_handle = (PyObject *)handle;
    PyObject *py_progress_callback = Py_None;
    PyObject *py_finished_callback = Py_None;
    int parse_status = PyArg_ParseTuple(py_handle, "OO", &py_progress_callback, &py_finished_callback);

    PyObject_CallFunction(py_progress_callback, "dII", progress, bytes, total_bytes);
}

void store_file_finished_callback_cb(int error_status,
                                     storj_file_meta_t *file,
                                     void *handle) {
    char *error_str = (char *)calloc(255, sizeof(char));
    PyObject *py_handle = (PyObject *)handle;
    PyObject *py_progress_callback = Py_None;
    PyObject *py_finished_callback = Py_None;
    PyObject *file_dict = Py_None;
    PyObject *error = Py_None;
    PyArg_ParseTuple(py_handle, "OO", &py_progress_callback, &py_finished_callback);

    if (status_check(error_status, &error_str)) {
        file_dict = PyDict_New();
        PyDict_SetItemString(file_dict,"filename", PyString_FromString(file->filename));
        PyDict_SetItemString(file_dict,"id", PyString_FromString(file->id));
        PyDict_SetItemString(file_dict,"decrypted", PyBool_FromLong((long)file->decrypted));
        PyDict_SetItemString(file_dict,"created", PyString_FromString(file->created));
        PyDict_SetItemString(file_dict,"size", Py_BuildValue("k", file->size));
        PyDict_SetItemString(file_dict,"mimetype", PyString_FromString(file->mimetype));
    } else {
        error = PyString_FromString(error_str);
    }

    PyObject_CallFunction(py_finished_callback, "OO", error, file_dict);
    Py_DECREF(py_progress_callback);
    Py_DECREF(py_finished_callback);
}

void get_info(storj_env_t *env, PyObject *callback) {
    void *void_callback = (void *)callback;
    storj_bridge_get_info(env, void_callback, get_info_cb);
}

void create_bucket(storj_env_t *env, PyObject *py_name, PyObject *callback) {
    void *void_callback = (void *)callback;
    char *name = PyString_AsString(py_name);
    storj_bridge_create_bucket(env, name, void_callback, create_bucket_cb);
}

void delete_bucket(storj_env_t *env, PyObject *py_id, PyObject *callback) {
    void *void_callback = (void *)callback;
    char *id = PyString_AsString(py_id);
    storj_bridge_delete_bucket(env, id, void_callback, delete_bucket_cb);
}

void get_bucket_id(storj_env_t *env, PyObject *name, PyObject *callback) {
    void *void_callback = (void *)callback;
    char *bucket_name = PyString_AsString(name);
    storj_bridge_get_bucket_id(env, bucket_name, void_callback, get_bucket_id_cb);
}

void list_buckets(storj_env_t *env, PyObject *callback) {
    void *void_callback = (void *)callback;
    storj_bridge_get_buckets(env, void_callback, list_buckets_cb);
}

void delete_file(storj_env_t *env, PyObject *bucket_id, PyObject *file_id, PyObject *callback) {
    void *void_callback = (void *)callback;
    char *idbucket = PyString_AsString(bucket_id);
    char *idfile = PyString_AsString(file_id);
    storj_bridge_delete_file(env, idbucket, idfile, void_callback, delete_bucket_cb);
}

void list_files(storj_env_t *env, PyObject *py_bucket_id, PyObject *callback) {
    char *bucket_id = PyString_AsString(py_bucket_id);
    void *void_callback = (void *)callback;
    storj_bridge_list_files(env, bucket_id, void_callback, list_files_cb);
}

storj_upload_state_t* store_file(storj_env_t *env,
                storj_upload_opts_t *upload_options,
                PyObject *py_progress_callback,
                PyObject *py_finished_callback) {
    Py_INCREF(py_progress_callback);
    Py_INCREF(py_finished_callback);
    PyObject *py_handle = Py_BuildValue("(OO)", py_progress_callback, py_finished_callback);
    void *handle = (void *)py_handle;
    storj_upload_state_t *upload_state;
    upload_state = storj_bridge_store_file(env,
                                             upload_options,
                                             handle,
                                             store_file_progress_callback_cb,
                                             store_file_finished_callback_cb);
    return upload_state;
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
