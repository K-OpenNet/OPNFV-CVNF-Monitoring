# OPNFV-Container-Multi-Interface
---
# Problem Description
Currently, Tacker provides container-based VNF [1],[#third]_. Current Kuryr-Kubernetes support multiple interfaces. However, when creating a C-VNF using a VNFD template in the tacker, it provides only a single interface. Therefore, it has a limitation to use C-VNF as a Network Function. this proposal suggests providing the multi network interfaces on a container using Kuryr-Kubernetes based ‘npwg_multiple_interfaces’
