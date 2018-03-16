#!/usr/bin/expect

set email "$env(STORJ_EMAIL)\n"
set pass "$env(STORJ_PASS)\n"
set keypass "$env(STORJ_KEYPASS)\n"
set strength "128\n"
set timeout 3

spawn storj register

expect {
    Bridge username {send_user $email}
    Bridge password: {send_user $pass}
    Strength: {send_user $strength}
    Unlock passphrase {send_user $keypass}
    Again to verify {send_user $keypass}
}

spawn echo "sleeping 3..."
spawn sleep 3
