..
      Copyright 2014-2019 OpenStack Foundation
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.


==============================
Prometheus Plugin Installation
==============================

This document describes the way to install Prometheus Plugin via Devstack and
how to set default exporters such as 'kube-state-metrics', 'node exporters',
and etc.

# Install Prometheus
echo "> Prometheus Installation Start"
cd $HOME
echo "> Install Nginx"
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx

echo "> Create User for Prometheus"
sudo useradd --no-create-home --shell /bin/false prometheus
sudo mkdir -p /etc/prometheus
sudo mkdir -p /var/lib/prometheus
sudo chown prometheus:prometheus /etc/prometheus
sudo chown prometheus:prometheus /var/lib/prometheus

echo "> Download Prometheus and setting ownership"
wget https://github.com/prometheus/prometheus/releases/download/v2.0.0/prometheus-2.0.0.linux-amd64.tar.gz
tar -xvf prometheus-2.0.0.linux-amd64.tar.gz
sudo cp prometheus-2.0.0.linux-amd64/prometheus /usr/local/bin/
sudo cp prometheus-2.0.0.linux-amd64/promtool /usr/local/bin/
sudo chown prometheus:prometheus /usr/local/bin/prometheus
sudo chown prometheus:prometheus /usr/local/bin/promtool

sudo cp -r prometheus-2.0.0.linux-amd64/consoles /etc/prometheus
sudo cp -r prometheus-2.0.0.linux-amd64/console_libraries /etc/prometheus
sudo chown -R prometheus:prometheus /etc/prometheus/consoles
sudo chown -R prometheus:prometheus /etc/prometheus/console_libraries

echo "> Install Node Exporter"
# Install Node Exporter for local node
wget https://github.com/prometheus/node_exporter/releases/download/v0.15.2/node_exporter-0.15.2.linux-amd64.tar.gz
tar -xf node_exporter-0.15.2.linux-amd64.tar.gz
sudo mv node_exporter-0.15.2.linux-amd64/node_exporter /usr/local/bin
sudo useradd -rs /bin/false node_exporter
sudo echo -e "[Unit]\nDescription=Node Exporter\nAfter=network.target\n\n[Service]\nUser=node_exporter\nGroup=node_exporter\nType=simple\nExecStart=/usr/local/bin/node_exporter\n\n[Install]\nWantedBy=multi-user.target" > /etc/systemd/system/node_exporter.service
sudo systemctl daemon-reload
sudo systemctl enable node_exporter
sudo systemctl start node_exporter

echo "> Create Prom Yaml File"
# Create prometheus.yaml file
sudo echo -e "global:\n  scrape_interval: 15s\n  evaluation_interval: 15s\nrule_files: []\nscrape_configs:\n  # Scrape Prometheus itself\n  - job_name: 'prometheus'\n    static_configs:\n      - targets: ['localhost:9090']\n  # Scrape Node Exporters\n  - job_name: 'nodes'\n    file_sd_configs:\n    - files:\n      - 'tacker_targets.yaml'" > /etc/prometheus/prometheus.yaml

echo "> Create Tacker Target File"
# Create tacker_targets.yaml file
sudo echo -e "---\n- targets:\n  - localhost:9100\n  labels:\n    job: node" > /etc/prometheus/tacker_targets.yaml

echo "> Create Prometheus System Daemon File"
# Create Prometheus as System Daemon
sudo echo -e "[Unit]\nDescription=Prometheus\nWants=network-online.target\nAfter=network-online.target\n\n[Service]\nUser=prometheus\nGroup=prometheus\nType=simple\nExecStart=/usr/local/bin/prometheus --config.file /etc/prometheus/prometheus.yaml --storage.tsdb.path /var/lib/prometheus/ --web.console.templates=/etc/prometheus/consoles --web.console.libraries=/etc/prometheus/console_libraries\n\n[Install]\nWantedBy=multi-user.target" > /etc/systemd/system/prometheus.service
sudo systemctl daemon-reload
sudo systemctl enable prometheus
sudo systemctl start prometheus

echo "> Install Prometheus Finished"