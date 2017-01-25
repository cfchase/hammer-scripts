import time
from config import satellite
from utils.hammer import *


def provision_hosts(deployment):
    print("****************** Provisioning Hosts ******************")

    engine_dh_name = deployment["rhv"]["engine_discovered_host_name"]
    hypervisor_dh_names = deployment["rhv"]["hypervisor_discovered_host_names"]

    if not engine_dh_name:
        raise Exception('RHV Engine not found')

    if not hypervisor_dh_names:
        raise Exception('RHV Hypervisors not found')

    engine_new_name = (deployment["label"] + "-engine-" + engine_dh_name).replace("_", "-")
    provision_host(engine_dh_name, engine_new_name, "RHV-Engine")
    engine_fqdn = "%s.%s" % (engine_new_name, satellite.DOMAIN_NAME)
    deployment["rhv"]["engine_managed_host_name"] = engine_fqdn

    i = 0
    deployment["rhv"]["hypervisor_managed_host_names"] = []
    for dh_name in hypervisor_dh_names:
        i += 1
        hypervisor_new_name = (deployment["label"] + "-hypervisor-" + dh_name).replace("_", "-")
        provision_host(dh_name, hypervisor_new_name, "RHV-Hypervisor")
        hypervisor_fqdn = "%s.%s" % (hypervisor_new_name, satellite.DOMAIN_NAME)
        deployment["rhv"]["hypervisor_managed_host_names"].append(hypervisor_fqdn)

    in_progress = True
    while in_progress:
        get_rhv_hosts(deployment)
        in_progress = not fully_provisioned(deployment)
        time.sleep(30)

    time.sleep(60)
    get_rhv_hosts(deployment)

    print("****************** Completed Provisioning of Hosts ******************")


def get_rhv_hosts(deployment):
    deployment["rhv"]["engine"] = get_host(deployment["rhv"]["engine_managed_host_name"])
    hypervisors = []
    for host_name in deployment["rhv"]["hypervisor_managed_host_names"]:
        hypervisors.append(get_host(host_name))
    deployment["rhv"]["hypervisors"] = hypervisors


def fully_provisioned(deployment):
    if not is_provisioned(deployment["rhv"]["engine"]):
        return False
    for host in deployment["rhv"]["hypervisors"]:
        if not is_provisioned(host):
            return False
    return True


def is_provisioned(host):
    return host and host.get("Managed") and host.get("Installed at") and host["Additional info"]["Model"]["errata_status"] == 0
