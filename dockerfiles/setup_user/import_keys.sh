#!/usr/bin/expect

set email "$env(STORJ_EMAIL)\n"
set pass "$env(STORJ_PASS)\n"
set keypass "$env(STORJ_KEYPASS)\n"
set mnemonic "$env(STORJ_MNEMONIC)\n"
set timeout 1

spawn storj import-keys

# expect 'overwrite'
# send 'y'

expect 'username'
send $email

expect 'password'
send $pass

expect 'key'
send $mnemonic

expect 'passphrase'
send $keypass

expect 'verify'
send $keypass
