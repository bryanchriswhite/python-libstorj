#!/usr/bin/expect

set email "$env(STORJ_EMAIL)\n"
set pass "$env(STORJ_PASS)\n"
set keypass "$env(STORJ_KEYPASS)\n"
set mnemonic "$env(STORJ_MNEMONIC)\n"
set timeout 3

spawn storj import-keys

expect {
    Bridge username {send $email}
    Bridge password: {send $pass}
    Encryption key: {send $mnemonic}
    Unlock passphrase {send $keypass}
    Again to verify {send $keypass}
}
close
