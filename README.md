# OPNFV-Container-Multi-Interface
---
## Problem Description
Currently, Tacker provides container-based VNF [1],[#third]_. Current Kuryr-Kubernetes support multiple interfaces. However, when creating a C-VNF using a VNFD template in the tacker, it provides only a single interface. Therefore, it has a limitation to use C-VNF as a Network Function. this proposal suggests providing the multi network interfaces on a container using Kuryr-Kubernetes based ‘npwg_multiple_interfaces’

## Propose Change
Therefore, in this specification, we want to add functionality to the translator so that we can use multi-interface feature mentioned above when deploying C-VNF.

Definition of ToscaKubeObject:
ToscaKubeObject holds the basic struct of a VDU. That is used for translating TOSCA to Kubernetes templates such as Service, Deployment, Horizon Pod Autoscaling, ConfigMap. In this specification, we use VL section for multi interface. When user defines VL more than one, it makes to provide multiple interface for C-VNF.

Basically, this specification follows previous containerized VNF specification [3]. To support multi-interface, we use VL section and network name.

network_name: network of VDU, for pure Kubernetes, it is used when enable
neutron network with Kuryr-Kubernetes. When user define virtual link more than one, user can use multi-interface network in the C-VNF.
When user define virtual link more than one, kubernetes translator get the network information from network_name. These information is used to make a kubernetes template which used to create POD with multi interface.

To support this function, kubernetes translator of Tacker should be changed to create multiple-interface using VL information.
