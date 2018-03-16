#!/usr/bin/expect

set email "$env(STORJ_EMAIL)\n"
set pass "$env(STORJ_PASS)\n"
set keypass "$env(STORJ_KEYPASS)\n"
set mnemonic "$env(STORJ_MNEMONIC)\n"
set timeout 3

spawn storj register

expect 'Bridge username:'
send $email

expect 'Bridge password:'
send $pass

expect 'Strength:'
send 128

# expect 'overwrite'
# send 'y'

expect 'Unlock passphrase:'
send $keypass

expect 'Again to verify:'
send $keypass
