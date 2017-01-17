import os
import yaml
from pprint import pprint

import data

from config import satellite
from config import rhv

from utils.hammer import *
from utils.ansible import *


def install_rhv(deployment):
    print("****************** Deploying RHV ******************")

    playbook = rhv.ANSIBLE_PLAYBOOK_LOCATION
    config_dir = os.path.dirname(__file__) + "/tmp/ansible"

    inventory = generate_inventory(deployment)
    print(inventory)
    inv_file_path = "%s/%s_inventory" % (config_dir, deployment["label"])
    with open(inv_file_path, "w") as outfile:
        outfile.write(inventory)

    ansible_vars = generate_vars(deployment)
    pprint(ansible_vars)
    vars_file_path = "%s/%s_vars.yaml" % (config_dir, deployment["label"])
    with open(vars_file_path, "w") as outfile:
        yaml.safe_dump(dict(ansible_vars), outfile, default_flow_style=False)
    print(inventory)

    environment = generate_environment(deployment, config_dir)
    pprint(environment)

    distribute_public_key(deployment)

    run_ansible(playbook, inv_file_path, vars_file_path, environment)

    # TODO: Poll and wait until complete
    print("****************** Completed Deployment of RHV ******************")


def generate_inventory(deployment):
    engine = deployment["rhv"]["engine"]
    hypervisors = deployment["rhv"]["hypervisors"]
    engine_repositories = repositories_for("rhevm")
    hypervisor_repositories = repositories_for("rhevh")
    return "\n".join([
        "[engine]",
        "%s mac_address=%s" % (engine["fqdn"], engine["mac"]),
        "[engine:vars]",
        "repositories=" + engine_repositories,
        "[hypervisors]",
        "\n".join(list(map(lambda h: h["fqdn"], hypervisors))),
        "[hypervisors:vars]",
        "repositories=" + hypervisor_repositories
    ])


def generate_vars(deployment):
    engine_activation_key = get_engine_activation_key()
    gateway = get_default_gateway()
    mac_address_range = get_mac_address_range(deployment)
    satellite_fqdn = satellite.SERVER_FQDN
    engine_repositories = repositories_for("rhevm")

    return {
        "admin_password": deployment["rhv"]["engine_admin_password"],
        "cluster_name": deployment["rhv"]["cluster_name"],
        "dc_name": deployment["rhv"]["data_center_name"],
        "cpu_model": deployment["rhv"]["cpu_model"],
        "cpu_type": deployment["rhv"]["cpu_type"],
        "data_storage_address": deployment["rhv"]["storage_address"],
        "data_storage_name": deployment["rhv"]["storage_name"],
        "data_storage_path": deployment["rhv"]["share_path"],
        "create_export_domain": deployment["rhv"]["create_export_domain"],
        "export_storage_address": deployment["rhv"]["export_domain_address"],
        "export_storage_name": deployment["rhv"]["export_domain_name"],
        "export_storage_path": deployment["rhv"]["export_domain_path"],
        "engine_activation_key": engine_activation_key,
        "engine_db_password": deployment["rhv"]["engine_admin_password"],
        "engine_fqdn": deployment["rhv"]["engine"]["fqdn"],
        "engine_mac_address": deployment["rhv"]["engine"]["mac"],
        "gateway": gateway,
        "mac_address_range": mac_address_range,
        "mac_pool_name": "qci",
        "root_password": deployment["rhv"]["root_password"],
        "satellite_fqdn": satellite_fqdn,
        "config_dir": "/etc/qci/",
        "storageDatacenterName": "hosted_storage",
        "storage_type": deployment["rhv"]["storage_type"],
        "engine_repositories": engine_repositories
    }


def get_engine_activation_key():
    key = None
    hostgroup = get_hostgroup('RHV-Engine')
    for param in hostgroup["Parameters"]:
        if param["name"] == "kt_activation_keys":
            key = param["value"]
    return key


def get_default_gateway():
    return get_subnet('default')['Gateway']


def get_mac_address_range(deployment):
    identifier = deployment.get("id") or 0
    str_id = format(identifier, 'x')
    if len(str_id) == 1:
        str_id = '0' + str_id
    return "00:1A:%s:00:00:00,00:1A:%s:FF:FF:FF" % (str_id, str_id)


def repositories_for(product):
    # TODO: Use Fusor.yaml
    repos = []
    if product == 'rhevh':
        repos = [
            "rhel-7-server-rpms",
            "rhel-7-server-satellite-tools-6.2-rpms",
            "rhel-7-server-rhv-4-mgmt-agent-rpms",
            "rhel-7-server-supplementary-rpms",
            "rhel-7-server-optional-rpms"
        ]
    elif product == 'rhevm':
        repos = [
            "rhel-7-server-rpms",
            "rhel-7-server-satellite-tools-6.2-rpms",
            "rhel-7-server-supplementary-rpms",
            "rhel-7-server-rhv-4.0-rpms",
            "jb-eap-7-for-rhel-7-server-rpms",
            "rhel-7-server-optional-rpms"
        ]

    return "[" + ", ".join(list(map(lambda x: '"' + x + '"', repos))) + "]"


def generate_environment(deployment, config_dir):
    return {
        'ANSIBLE_HOST_KEY_CHECKING': 'False',
        'ANSIBLE_LOG_PATH': config_dir + "/%s.log" % (deployment["label"]),
        'ANSIBLE_RETRY_FILES_ENABLED': "False",
        'ANSIBLE_SSH_CONTROL_PATH': "/tmp/%%h-%%r",
        'ANSIBLE_ASK_SUDO_PASS': "False",
        'ANSIBLE_PRIVATE_KEY_FILE': data.get_private_key_path(),
        'ANSIBLE_CONFIG': config_dir,
        'HOME': config_dir
    }


def distribute_public_key(deployment):
    data.write_ssh_keys(deployment)
    copy_keys_to_root(deployment["rhv"]["engine"]["fqdn"], deployment["rhv"]["root_password"])
    for host in deployment["rhv"]["hypervisors"]:
        copy_keys_to_root(host["fqdn"], deployment["rhv"]["root_password"])


def copy_keys_to_root(hostname, password):
    utils.shell.execute_cmd(["sshpass", "-p", password,
                             "scp",
                             "-o", "StrictHostKeyChecking=no",
                             "-o", "UserKnownHostsFile=/dev/null",
                             data.get_private_key_path(), "root@%s:/root/.ssh/" % hostname
                             ])

    utils.shell.execute_cmd(["sshpass", "-p", password,
                             "scp",
                             "-o", "StrictHostKeyChecking=no",
                             "-o", "UserKnownHostsFile=/dev/null",
                             data.get_public_key_path(), "root@%s:/root/.ssh/" % hostname
                             ])

    utils.shell.execute_cmd(["sshpass", "-p", password,
                             "ssh",
                             "-o", "StrictHostKeyChecking=no",
                             "-o", "UserKnownHostsFile=/dev/null",
                             "root@%s" % hostname,
                             "cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys"
                             ])
