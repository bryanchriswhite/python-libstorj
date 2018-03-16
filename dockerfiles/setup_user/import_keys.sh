#!/usr/bin/expect

set email "$env(STORJ_EMAIL)\n"
set pass "$env(STORJ_PASS)\n"
set keypass "$env(STORJ_KEYPASS)\n"
set mnemonic "$env(STORJ_MNEMONIC)\n"
set timeout 3

spawn storj import-keys

expect "Would you like to overwrite"
send "y\n"

expect "Bridge username"
send $email

expect "Bridge password:"
send $pass

expect "Encryption key:"
send $mnemonic

expect "Unlock passphrase:"
send $keypass

expect "Again to verify:"
send $keypass

expect "EOF"

exit
