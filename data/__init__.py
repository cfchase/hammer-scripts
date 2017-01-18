import os
import datetime
from config import rhv
from utils.hammer import *

from Crypto.PublicKey import RSA


def create_rhv_deployment_data():
    with open(os.path.dirname(__file__) + "/rhv_deployment_defaults.json") as data_file:
        deployment = json.load(data_file)

    hosts = get_discovered_hosts()

    for host in hosts:
        if host["Memory"] > rhv.MIN_RHV_HYPERVISOR_MEMORY:
            deployment["rhv"]["hypervisor_discovered_host_names"].append(host["Name"])
        else:
            deployment["rhv"]["engine_discovered_host_name"] = host["Name"]

    write_rhv_deployment_data(deployment)
    update_keys(deployment)

    return deployment


def read_rhv_deployment_data():
    with open(os.path.dirname(__file__) + "/tmp/rhv_deployment.json") as data_file:
        deployment = json.load(data_file)
    return deployment


def write_rhv_deployment_data(deployment):
    with open(os.path.dirname(__file__) + "/tmp/rhv_deployment.json", "w") as outfile:
        json.dump(deployment, outfile)


def backup_rhv_deployment_data(deployment):
    date_str = "{:%Y-%m-%d-%H:%M:%S:%f}".format(datetime.datetime.now())
    with open(os.path.dirname(__file__) + "/tmp/rhv_deployment_%s.json" % date_str, "w") as outfile:
        json.dump(deployment, outfile)


def update_keys(deployment):
    key = RSA.generate(2048)
    deployment["private_key"] = key.exportKey('PEM')
    deployment["public_key"] = key.publickey().exportKey('OpenSSH')


def write_ssh_keys(deployment):
    private_key_path = get_private_key_path()
    public_key_path = get_public_key_path()

    with open(private_key_path, 'w') as key_file:
        key_file.write(deployment["private_key"])
        os.chmod(private_key_path, 0600)

    with open(public_key_path, 'w') as key_file:
        key_file.write(deployment["public_key"])


def create_ssh_key():
    key = RSA.generate(2048)

    private_key_path = get_private_key_path()
    public_key_path = get_public_key_path()

    with open(private_key_path, 'w') as key_file:
        os.chmod(private_key_path, 0600)
        key_file.write(key.exportKey('PEM'))

    pubkey = key.publickey()
    with open(public_key_path, 'w') as key_file:
        key_file.write(pubkey.exportKey('OpenSSH'))


def get_private_key_path():
    return os.path.dirname(__file__) + "/tmp/id_rsa"


def get_public_key_path():
    return get_private_key_path() + ".pub"
