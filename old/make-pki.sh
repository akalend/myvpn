#!/bin/bash

# PWD=`pwd`

# echo "pwd $PWD"

PKI="/home/akalend/projects/myvpn/pki"


if [ -z "$NUMBER" ] 
then
	echo the ID enviromenst variable absent
	exit 1
fi

LOG="$PKI/$NUMBER/pki.log"
echo "log: $LOG"
if  mkdir "$PKI/$NUMBER"
then
	echo "mkdir $PKI/$NUMBER ok $?"
else
	echo "mkdir error $PKI/$NUMBER $?"
	exit 1
fi

if touch $LOG
then
	echo "create log $LOG" 
else		
	echo "code $?"
	echo "can't create log $LOG"

	exit 1
fi

exec 3<> "$LOG"
1>&3
2>&3
# echo "test\n" > "$LOG"
echo -n "start init $PKI/$NUMBER"  >&3

exec 3>&-
exec 3<> "$LOG"
# exit 0


# exit 0

# mkdir $PKI

cd "$PKI/$NUMBER"


# echo "log $LOG"


EASY_RSA=/home/akalend/src/easy-rsa/easyrsa3/easyrsa

$EASY_RSA init-pki >&3 2>&3

$EASY_RSA build-ca nopass >&3 2>&3
$EASY_RSA build-server-full server nopass >&3 2>&3
$EASY_RSA build-client-full client nopass >&3 2>&3
$EASY_RSA gen-dh 1>&3 2>&3
openvpn --genkey --secret "$PKI/$NUMBER/ta.key" >&3 2>&3
# tree "$PKI/$NUMBER" >&3 2>&3

exec 3>&-
echo 'finish pki'
# rm -fr $PKI/$NUMBER