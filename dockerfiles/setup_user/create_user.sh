#!/usr/bin/expect

set email "$env(STORJ_EMAIL)\n"
set pass "$env(STORJ_PASS)\n"
set keypass "$env(STORJ_KEYPASS)\n"
set strength "128\n"
set timeout 3

spawn storj register

expect {
    Bridge username {send $email}
    Bridge password: {send $pass}
    Strength: {send $strength}
    Unlock passphrase {send $keypass}
    Again to verify {send $keypass}
}
close
