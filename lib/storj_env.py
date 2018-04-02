import json, os
from datetime import datetime
from .ext import python_libstorj as ext
from .ext.upload_options import UploadOptions
from .ext import load_yaml_options


class StorjEnv:
    def __init__(self,
                 path=None,
                 **options_dict):
        option_names = ('bridge_options',
                        'encrypt_options',
                        'http_options',
                        'log_options')

        options_dict = options_dict or dict(zip(option_names, [None]*4))
        option_types = (ext.BridgeOptions,
                        ext.EncryptOptions,
                        ext.HttpOptions,
                        ext.LogOptions)

        options_zip = zip(option_names, option_types)

        if path is not None and os.path.exists(path):
            options_dict.update(load_yaml_options(path))

        options_list = [(options_dict[name], type_()) for name, type_ in options_zip]

        for o_dict, o_struct in options_list:
            for key, value in o_dict.iteritems():
                if key == 'pass':
                    # NB: `pass` is a reserved attribute name; swig
                    #     knows this and has changed `pass` to `_pass`
                    key = '_pass'
                setattr(o_struct, key, value)

        options = zip(*options_list)[1]

        self.env = ext.init_env(*options)
        self.env.loop = ext.set_loop(self.env)

    @staticmethod
    def _error_check(results):
        error, data = None, None

        try:
            if type(results) is list:
                data = results[0]
            elif type(results) is dict:
                try:
                    error = results['error']
                    if error is not None:
                        data = error
                except KeyError:
                    data = results['data']
            else:
                raise Exception('Unknown results structure')

            if type(data) is Exception:
                raise data
            return data
        except(IndexError, KeyError):
            return None

    def destroy(self):
        ext.destroy_env(self.env)

    def get_info(self, callback=None):
        results = []

        def handle(error, result):
            # NB: method executes in a separate C thread!
            info = None
            try:
                info = json.loads(result)
                results.append(info)
            finally:
                if error is not None:
                    error = Exception(error)
                    results.append(error)

                if callback is not None:
                    callback(error, info)

        ext.get_info(self.env, handle)
        ext.run(self.env.loop)
        return self._error_check(results)

    def create_bucket(self, name, callback=None):
        results = []

        def handle(error, bucket):
            if bucket is not None:
                results.append(bucket)

            if error is not None:
                error = Exception(error)
                results.append(error)

            if callback is not None:
                callback(error, bucket)

        ext.create_bucket(self.env, name, handle)
        ext.run(self.env.loop)
        return self._error_check(results)

    def delete_bucket(self, bucket_id, callback=None):
        results = []

        def handle(error):
            if error is not None:
                error = Exception(error)
                results.append(error)

            if callback is not None:
                callback(error)

        ext.delete_bucket(self.env, bucket_id, handle)
        ext.run(self.env.loop)
        return self._error_check(results)

    def get_bucket_id(self, bucket_name, callback=None):
        results = {}

        def handle(error, bucket):
            if bucket is not None:
                results['data'] = bucket

            if error is not None:
                error = Exception(error)
                results['error'] = error

            if callback is not None:
                callback(error, bucket)

        ext.get_bucket_id(self.env, bucket_name, handle)
        ext.run(self.env.loop)
        return self._error_check(results)

    def list_buckets(self, callback=None):
        results = {}

        def handle(error, buckets):
            if buckets is not None:
                for i, bucket in enumerate(buckets):
                    iso8601_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                    created_date = datetime.strptime(bucket['created'], iso8601_format)
                    buckets[i]['created'] = created_date
                results['data'] = buckets

            if error is not None:
                error = Exception(error)
                results['error'] = error

            if callback is not None:
                callback(error, buckets)

        ext.list_buckets(self.env, handle)
        ext.run(self.env.loop)
        return self._error_check(results)

    def delete_file(self, bucket_id, file_id, callback=None):
        results = []

        def handle(error):
            if error is not None:
                error = Exception(error)
                results.append(error)

            if callback is not None:
                callback(error)

        ext.delete_file(self.env, bucket_id, file_id, handle)
        ext.run(self.env.loop)
        return self._error_check(results)

    def list_files(self, bucket_id, callback=None):
        results = {}

        def handle(error, files):
            if files is not None:
                for i, file_ in enumerate(files):
                    iso8601_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                    created_date = datetime.strptime(file_['created'], iso8601_format)
                    files[i]['created'] = created_date
                results['data'] = files

            if error is not None:
                error = Exception(error)
                results['error'] = error

            if callback is not None:
                callback(error, files)

        ext.list_files(self.env, bucket_id, handle)
        ext.run(self.env.loop)
        return self._error_check(results)

    def store_file(self,
                   bucket_id,
                   file_path,
                   options=None,
                   progress_callback=None,
                   finished_callback=None):
        results = {}

        def handle_progress(progress, bytes, total_bytes):
            if progress_callback is not None:
                progress_callback(progress, bytes, total_bytes)

        def handle_finished(error, file_):
            # TODO: error handling based on `status`
            results['data'] = file_

            if error is not None:
                error = Exception(error)
                results['error'] = error

            if finished_callback is not None:
                finished_callback(error, file_)

        upload_options = UploadOptions(bucket_id, file_path, options)
        ext.store_file(self.env,
                       upload_options,
                       handle_progress,
                       handle_finished)
        ext.run(self.env.loop)
        return self._error_check(results)
