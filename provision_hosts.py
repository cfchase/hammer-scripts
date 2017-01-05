from hammer_helpers import *


def provision_hosts(deployment):
    print("****************** Provisioning Hosts ******************")

    engine_dh_name = deployment["rhv"]["engine_discovered_host_name"]
    hypervisor_dh_names = deployment["rhv"]["hypervisor_discovered_host_names"]

    if not engine_dh_name:
        raise Exception('RHV Engine not found')

    if not hypervisor_dh_names:
        raise Exception('RHV Hypervisors not found')

    engine_new_name = (deployment["label"] + "-engine").replace("_", "-")
    provision_host(engine_dh_name, engine_new_name, "RHV-Engine")

    i = 0
    for dh_name in hypervisor_dh_names:
        i += 1
        hypervisor_new_name = (deployment["label"] + "-hypervisor" + str(i)).replace("_", "-")
        provision_host(dh_name, hypervisor_new_name, "RHV-Hypervisor")

    # Poll and wait until complete
    print("****************** Completed Provisioning of Hosts ******************")
