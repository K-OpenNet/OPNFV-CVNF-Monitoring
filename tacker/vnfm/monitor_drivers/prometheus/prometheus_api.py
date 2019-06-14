#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
dTRIGGER_LIST = {
    'node_memory': [{''}],
    'os_agent_info': [{'description': 'Zabbix agent on '
                                       '{HOST.NAME} is '
                                       'unreachable '
                                       'for 15 seconds',
                        'expression': '{', 'priority': 3}],
    'app_status': [{'description': 'Service is down '
                                   'on {HOST.NAME}',
                    'expression': '{', 'priority': 3}],
    'app_memory': [{'description': 'Process Memory '
                                   'is lacking '
                                   'on {HOST.NAME}',
                    'expression': '{', 'priority': 3}],
    'os_cpu_usage': [{'description': 'Disk I/O is '
                                     'overloaded '
                                     'on {HOST.NAME}',
                      'expression': '{', 'priority': 3}],
    'os_cpu_load': [{'description': 'Processor load '
                                    'is too high '
                                    'on {HOST.NAME}',
                     'expression': '{', 'priority': 3}],
    'os_proc_value': [{'description': 'Too many '
                                      'processes running '
                                      'on {HOST.NAME}',
                       'expression': '{', 'priority': 3}]
}

dPROM_INFO = {
    'prometheus_server_ip': None,
    'prometheus_server_port': None,
    'prometheus_server_targets_path': None
}

dVDU_INFO = {
    'template_id': None,
    'template_name': None,
    'hostid': None,
    'group_id': None,
    'mgmt_ip': None,
    'target_exporter_port': None,
    'labels_job': None,
    'target_ip': None,
    'vdu_id': None,
    'parameters': None,
    'actioninfo': [],
    'appinfo': None,
    'zbx_info': None
}
