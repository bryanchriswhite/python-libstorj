#!/usr/bin/expect

set email "$env(STORJ_EMAIL)\n"
set pass "$env(STORJ_PASS)\n"
set keypass "$env(STORJ_KEYPASS)\n"
set mnemonic "$env(STORJ_MNEMONIC)\n"
set timeout 3

spawn storj import-keys

expect {
    Bridge username {send_user "$email"}
    Bridge password: {send_user "$pass"}
    Encryption key: {send_user $mnemonic}
    Unlock passphrase {send_user $keypass}
    Again to verify {send_user "$keypass"}
}

spawn echo "sleeping 3..."
spawn sleep 3