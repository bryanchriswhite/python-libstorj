import python_libstorj as pystorj
# import pyuv
# import ipdb

print pystorj.storj_mnemonic_check('this is not a valid mnemonic')
print pystorj.storj_mnemonic_check('zebra dilemma mirror dignity forum style lyrics tape guitar inject leisure finish')
status, mnemonic = pystorj.storj_mnemonic_generate(128)
print mnemonic

bridge_options = pystorj.storj_bridge_options_t()
bridge_options.proto = 'https'
bridge_options.host = 'app.storj.io'
bridge_options.port = 443
bridge_options.user = 'bryan@liminal.ly'

encrypt_options = pystorj.storj_encrypt_options_t()
encrypt_options.mnemonic = 'crash venture snow hungry script arch ankle luxury borrow airport voyage man'

http_options = pystorj.storj_http_options_t()
http_options.user_agent = 'curl/7.52.1'
http_options.low_speed_limit = 30720
http_options.low_speed_time = 20
http_options.timeout = 60

log_options = pystorj.storj_log_options_t()
log_options.level = 4

env = pystorj.storj_init_env(bridge_options,
                       encrypt_options,
                       http_options,
                       log_options)

# ipdb.set_trace()
