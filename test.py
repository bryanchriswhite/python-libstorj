import python_libstorj
# import pyuv
# import ipdb
# ipdb.set_trace()

print python_libstorj.storj_mnemonic_check('this is not a valid mnemonic')
print python_libstorj.storj_mnemonic_check('zebra dilemma mirror dignity forum style lyrics tape guitar inject leisure finish')
status, mnemonic = python_libstorj.storj_mnemonic_generate(128)
print mnemonic
