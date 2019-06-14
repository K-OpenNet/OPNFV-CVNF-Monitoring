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


import ruamel.yaml as yaml

import copy
from oslo_log import log as logging
from tacker.vnfm.monitor_drivers import abstract_driver
from tacker.vnfm.monitor_drivers.prometheus import prometheus_api as papi


LOG = logging.getLogger(__name__)


# TODO(jaewook.oh) Prometheus Plugin should generate a new configuration
# file which defines the generated VDU as monitoring host.
# That conf file also includes an action trigger value and app information
# to perform monitoring for each VDU.
class VNFMonitorPrometheus(abstract_driver.VNFMonitorAbstractDriver):
    def __init__(self):
        self.kwargs = None
        self.vnf = None
        self.vdu_name = []
        self.host_info = {}

    def get_type(self):
        return 'prometheus'

    def get_name(self):
        return 'prometheus'

    def get_description(self):
        return 'Tacker VNFMonitor Prometheus Driver'

    def monitor_url(self, plugin, context, vnf):
        LOG.debug('monitor_url %s', vnf)
        return vnf.get('monitor_url', '')

    def monitor_call(self, vnf, kwargs):
        if not kwargs['mgmt_ip']:
            return

    def add_to_prom_monitor(self, vnf, kwargs):
        self.__init__()
        self.kwargs = kwargs
        self.vnf = vnf
        # TODO(jaewook.oh) Setting some vdu info is needed
        self.set_vdu_info()
        self.add_host_to_prometheus()

    def add_host_to_prometheus(self):
        self.register_host()

    # TODO(jaewook.oh) Trigger Creation Function is needed
    def create_trigger(self, trigger_params, vdu_name):
        pass

    def register_host(self):
        """Register new host or new trigger to Prometheus
        by modifying file_sd (tacker_targets.yaml) file
        Append a new host or trigger to the yaml file.
        """

        # TODO(jaewook.oh) Instead kwargs, using host_info is better.
        # Then I should use node parameter, but it needs
        tacker_targets_path = \
            self.kwargs['vdus']['prom_info']['prometheus_server_targets_path']
            #self.host_info[node]['prom_info']['prometheus_server_targets_path']

        with open(tacker_targets_path, 'r') as fp:
            try:
                tacker_targets = yaml.safe_load(fp)
            except yaml.YAMLError as err:
                tacker_targets = None # TODO(jaewook.oh) If tt is none, return error.
                print(err)
                LOG.error('Loading tacker_targets.yaml failed : %s', err)
            LOG.debug('Loaded tacker_targets.yaml : %s', tacker_targets)

        tmp_vdu_name = self.kwargs['vdus'].keys()
        for node in tmp_vdu_name:
            for i, tt in enumerate(tacker_targets):
                if tt['labels']['job'] == self.host_info[node]['labels_job']:
                    LOG.debug('target label job is %s', \
                              self.host_info[node]['labels_job'])
                    tacker_targets[i]['targets'].append(self.host_info[node]['mgmt_ip'] + \
                                                        ':' + self.host_info[node]['target_exporter_port'])

        with open(tacker_targets_path, 'w') as fp:
            try:
                yaml.dump(tacker_targets, fp, Dumper=yaml.RoundTripDumper)
            except yaml.YAMLError as err:
                print(err)
                LOG.error('Dumping tacker_targets.yaml failed : %s', err)
            LOG.debug('Dumped tacker_targets.yaml : %s', tacker_targets)

    def set_prom_info(self, node):
        self.host_info[node]['prom_info'] = \
            copy.deepcopy(papi.dPROM_INFO)
        self.host_info[node]['prom_info']['prometheus_server_ip'] = \
            self.kwargs['vdus'][node]['prometheus_server_ip']
        self.host_info[node]['prom_info']['prometheus_server_port'] = \
            self.kwargs['vdus']['prom_info']['prometheus_server_port']
        self.host_info[node]['prom_info']['prometheus_server_targets_path'] = \
            self.kwargs['vdus']['prom_info']['prometheus_server_targets_path']

    def set_vdu_info(self):
        tmp_vdu_name = self.kwargs['vdus'].keys()
        for node in tmp_vdu_name:
            if 'alert' in \
                    self.kwargs['vdus'][node]['parameters'].keys():
                self.vdu_name.append(node)
                self.host_info[node] = copy.deepcopy(papi.dVDU_INFO)
                self.set_prom_info(node)
                self.host_info[node]['labels_job'] = \
                    self.kwargs['vdus'][node]['labels_job']
                self.host_info[node]['mgmt_ip'] = \
                    self.kwargs['vdus'][node]['mgmt_ip']
                self.host_info[node]['target_exporter_port'] = \
                    self.kwargs['vdus'][node]['target_exporter_port']
                self.host_info[node]['parameters'] = \
                    self.kwargs['vdus'][node]['parameters']
                self.host_info[node]['vdu_id'] = self.vnf['id']
