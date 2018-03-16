#!/usr/bin/expect

set email "$env(STORJ_EMAIL)\n"
set pass "$env(STORJ_PASS)\n"
set keypass "$env(STORJ_KEYPASS)\n"
set strength "128\n"
set timeout 3

spawn storj register

expect 'Bridge username'
send $email

expect 'Bridge password:'
send $pass

expect 'Strength:'
send $strength

# expect 'overwrite'
# send 'y'

expect 'Unlock passphrase:'
send $keypass

expect 'Again to verify:'
send $keypass

close

spawn echo "sleeping for 3..."
close

spawn sleep 3
close
