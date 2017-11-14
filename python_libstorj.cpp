#include "python_libstorj.h"
#include "storj.h"
#include "uv.h"
#include "Python.h"

template <typename ReqType>
bool error_and_status_check(ReqType *req, char **error) {
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

    PyObject_CallFunction(_handle, "ss", result, error);
}

void get_info(storj_env_t *env, PyObject *handle) {
    void *cb = (void *)handle;
    storj_bridge_get_info(env, cb, get_info_cb);
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
