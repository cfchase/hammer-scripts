from config import rhv
from hammer_helpers import *


def create_rhv_deployment_data():
    with open(rhv.DEFAULTS_FILE_LOCATION) as data_file:
        deployment = json.load(data_file)

    hosts = get_discovered_hosts()

    for host in hosts:
        if host["Memory"] > rhv.MIN_RHV_HYPEVISOR_MEMORY:
            deployment["rhv"]["hypervisor_discovered_host_names"].append(host["Name"])
        else:
            deployment["rhv"]["engine_discovered_host_name"] = host["Name"]

    return deployment
