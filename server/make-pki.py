#!/usr/bin/python2

import os
import sys
import json
import shutil
import logging
import  daemon
from collections import namedtuple

from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible import context
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.plugins.callback.log_plays import CallbackModule
from ansible.utils.display import Display
import ansible.constants as C
from myvpn.tools import write_file
# from ansible import constants as C


class ResultCallback(CallbackBase):

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        path = getattr(C, 'DEFAULT_LOG_PATH')
        self.fd = open(path, 'a')
        host = result._host
        print('log file:', path)
        if self.fd is None:
            print('error open log')
            return

        self.fd.write( '<br>=============  %s  =================\n<br>' % result._task )
        if result._task.name == 'Gathering Facts':
            return
        out = {}
        for item in result._result:
            if item[0] == '_':
                continue
            out[item] = result._result[item]

        txt = json.dumps({host.name: out}, indent=2).split("\n")


        self.fd.write(  "<br>".join(txt) )
        # self.fd.write("\n")
        self.fd.close()


def start(id):
# logger = 

    home_path =  '/home/akalend/projects/myvpn/'
    
    os.chdir(home_path)
    path = home_path + '/log/txt_'+ id +'.log'
    # self.fd = open(path, 'a')
    # print path
    setattr(C, 'DEFAULT_LOG_PATH', path)
    # logger = logging.getLogger('ansible')
    # logging.basicConfig(filename=path)
    results_callback = ResultCallback()
    loader = DataLoader()



    context.CLIARGS = ImmutableDict( forks=10, become=None, syntax=None, start_at_task=None, 
                            stdout_callback=results_callback, module_path=[home_path],
                            connection='ssh', private_key_file='pk.pem', become_method='sudo',
                            become_user='root', check=False, diff=False)


    inventory = InventoryManager(loader=loader) 

    inventory.add_group('local')
    inventory.add_host(host='127.0.0.1', group='local', port=40000)

    # print inventory.list_hosts()
    # print inventory.list_groups()

    variable_manager = VariableManager(loader=loader, inventory=inventory)


    #  set_host_variable(, host, varname, value):

    playbook_path = home_path + '/playbook/pki.yml'

    if not os.path.exists(playbook_path):
        print ( '[INFO] The playbook file %s does not exist' % playbook_path )
        sys.exit()


    passwords = {}

                           # playbooks, inventory, variable_manager, loader, passwords
    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,loader=loader, passwords=passwords)

    pbex._tqm._stdout_callback = results_callback
    result = pbex.run()
    # print 'result code',result

    playbook_path = home_path + '/playbook/create_conf.yml'
    if not os.path.exists(playbook_path):
        print ( '[INFO] The playbook file %s does not exist' % playbook_path )
        sys.exit()

    # variable_manager.extra_vars = {'ca': 'test', 'pkey': 'yes', 'cert': '****'}
    variable_manager.set_host_variable('127.0.0.1', 'ca', 'valuevalue')
    variable_manager.set_host_variable('127.0.0.1', 'cert', 'valuevalue 11')
    variable_manager.set_host_variable('127.0.0.1', 'pk', 'valuevalue 333')
    variable_manager.set_host_variable('127.0.0.1', 'number', id)
    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,loader=loader, passwords=passwords)

    # pbex._tqm._stdout_callback = results_callback
    result = pbex.run()

    filename = '/home/akalend/projects/myvpn/status/' + id
    if  os.path.exists(filename):
        fd = open(filename, 'w')

        if fd is None:
            print('error open file')
            return
        fd.write('1')
        fd.close()


    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    return

    inventory.add_group('remote')
    inventory.add_host(host='78.47.159.230', group='remote', port=40000)
    
    # inventory.subset('94.130.91.89')
    variable_manager.set_inventory(inventory) 

    playbook_path = home_path + 'pki-test.yml'


    if not os.path.exists(playbook_path):
        print ( '[INFO] The playbook file %s does not exist' % playbook_path )
        sys.exit()


    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,loader=loader, passwords=passwords)

    # pbex._tqm._stdout_callback = results_callback
    result = pbex.run()

    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)



    filename = '/home/akalend/projects/myvpn/status/' + id
    write_file(filename, '1')


# n = 123 
# print(sys.argv)
if len(sys.argv) < 2:
    print('error args')
    exit()

n = sys.argv[1]

start(n)
print('finish')


