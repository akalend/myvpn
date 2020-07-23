import os
import sys
import json
import shutil
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
import ansible.constants as C



class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        print 'callback **'
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


def run():

    results_callback = ResultCallback()
    loader = DataLoader()

    context.CLIARGS = ImmutableDict( forks=10, become=None, syntax=None, start_at_task=None, stdout_callback=results_callback,
                            connection='ssh', private_key_file='pk.pem', become_method='sudo', become_user='root', check=False, diff=False)


    inventory = InventoryManager(loader=loader) # , sources='/home/akalend/myvpn/host.2.yml'
    inventory.add_group('all')

    inventory.add_host(host='88.99.241.225  ', group='all', port=40000)

    print inventory.list_hosts()
    # print inventory.list_groups()

    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # variable_manager.extra_vars = {'customer': 'test', 'disabled': 'yes'}

    #  set_host_variable(, host, varname, value):

    playbook_path = '/home/akalend/projects/myvpn/install.yml'

    if not os.path.exists(playbook_path):
        print ( '[INFO] The playbook file %s does not exist' % playbook_path )
        sys.exit()


    passwords = {}

                           # playbooks, inventory, variable_manager, loader, passwords
    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,loader=loader, passwords=passwords)

    pbex.run()

    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)


def main(body):
    return body