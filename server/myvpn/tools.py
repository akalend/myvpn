import os
import paramiko
import socket



def write_file( filename, data):
    if os.path.exists(filename):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    fd = open(filename, append_write)
    fd.write(data)
    fd.close()


def check_access(host, secret):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(hostname=host, username='user', password=secret, port=22,  timeout=1)
        except (paramiko.ssh_exception.BadHostKeyException, paramiko.ssh_exception.AuthenticationException, 
                paramiko.ssh_exception.SSHException, socket.error) as e:

            return 1


        transport = client.get_transport()
        if transport is None:
            return 1
        # data = stdout.read() + stderr.read()
        client.close()
        return 0



# def create_key(filename, template):
#     print('Ok')


# pki = '/home/akalend/myvpn/pki/'

# filename = pki + '205527/private/ca.key'
# template = 
# create_key(filename, )