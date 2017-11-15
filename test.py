import python_libstorj as pystorj

class StorjEnv():
    def __init__(self,
                 bridge_options,
                 encrypt_options,
                 http_options,
                 log_options):

        options_list = (
            (bridge_options, pystorj.BridgeOptions()),
            (encrypt_options, pystorj.EncryptOptions()),
            (http_options, pystorj.HttpOptions()),
            (log_options, pystorj.LogOptions())
        )

        for option_pair in options_list:
            (options, option_struct) = option_pair
            for key, value in options.viewitems():
                if key == 'pass':
                    key = '_pass'
                setattr(option_struct, key, value)

        options = zip(*options_list)[1]
        self.env = pystorj.init_env(*options)
        self.env.loop = pystorj.set_loop(self.env)

    def get_info(self, handle):
        pystorj.get_info(self.env, handle)
        pystorj.run(self.env.loop)

    def list_buckets(self, handle):
        pystorj.list_buckets(self.env, handle)
        pystorj.run(self.env.loop)


env = StorjEnv(
    bridge_options={
        'proto': 'http',
        'host': 'localhost',
        'port': 8080,
        'user': 'user@example.com',
        'password': 'examplepassword'

    },
    encrypt_options={
        'mnemonic': 'crash venture snow hungry script arch ankle luxury borrow airport voyage man'
    },
    http_options={
        'user_agent': 'curl/7.52.1',
        'low_speed_limit': 30720,
        'low_speed_time': 20,
        'timeout': 60
    },
    log_options={
        'level': 4
    }
)


def handle(result, error):
    if (error is not None):
        print('error: %s' % error)
        return

    print('result: %s' % result)


# env.get_info(handle)
env.list_buckets(handle)
