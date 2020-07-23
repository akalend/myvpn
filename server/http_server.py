#!/usr/bin/python2


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer # python2
# from http.server import BaseHTTPRequestHandler, HTTPServer # python3
import urlparse, os
  
from myvpn.tools import write_file, check_access
# from myvpn.tools import write_file
from myvpn.init import run
import subprocess

class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # def do_GET(self):
    #     self._set_headers()
    #     self.wfile.write("received get request")

    def do_POST(self):
        '''Reads post request body'''
        # print self.path
        split_list=self.path.split('/')
        # print split_list
        if len(split_list) != 2 or split_list[1] != 'start'  :
            # self.code = 403
            self._set_headers(400)
            # self.wfile.write("error request".encode())
            return

        self._set_headers()

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        params = urlparse.parse_qs(post_body)
        id = params['id'][0]
        host = params['ip'][0]
        psw = params['psw'][0]
        print(host)
        print(psw)

        filename = '/home/akalend/projects/myvpn/status/' + id
        log = '/home/akalend/projects/myvpn/log/txt_' + id + '.log'
        # --------------------------------------------------------
        # rc = check_access(host, psw)
        rc = 0
        # --------------------------------------------------------
        if rc:
            print('abort connections')
            write_file(log, 'ssh comnnection is abort')
            write_file(filename, '1')
            self.wfile.write('error ssh' )
            return


        # stdin, stdout, stderr = client.exec_command('ls -l')


        #  create PKI
        my_env = os.environ
        my_env["NUMBER"] = id
        # my_env["PKI"] = "'/home/akalend/projects/myvpn/pki/%s" % id
        
        cmd = ['/usr/bin/python2','/home/akalend/projects/myvpn/server/make-pki.py', id, host]
    

        write_file(filename, '0')

        print('cmd:' , ' '.join(cmd) )

        subprocess.Popen(cmd, env=my_env, stdin=None, stdout=None, stderr=None)

        # it is Work!!!
        # subprocess.Popen(['/usr/bin/python2', '/home/akalend/projects/myvpn/master.py', id], stdin=None, stdout=None, stderr=None)

        self.wfile.write('id=' + id  )

    def do_PUT(self):
        self.do_POST()

host = ''
port = 8000
HTTPServer((host, port), HandleRequests).serve_forever()


