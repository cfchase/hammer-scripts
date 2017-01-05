###################################
# Host Groups
###################################

import json
import subprocess
from config.satellite import *


def execute_cmd(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    proc.wait()
    return {
        "returncode": proc.returncode,
        "stdout": out,
        "stderr": err,
    }


def construct_hammer_cmd(hammer_cmd_arr, **kwargs):
    cmd = [
        "hammer",
        "--server", SERVER,
        "--username", USERNAME,
        "--password", PASSWORD,
        "--output", "json",
    ]

    cmd = cmd + hammer_cmd_arr

    for key, value in kwargs.iteritems():
        param_name = key.replace("_", "-")
        cmd.append("--%s" % param_name)
        cmd.append(value)

    return cmd


def execute_hammer_cmd(hammer_cmd_arr, **kwargs):
    cmd = construct_hammer_cmd(hammer_cmd_arr, **kwargs)
    cmd_result = execute_cmd(cmd)
    if cmd_result["returncode"] == 0:
        return json.loads(cmd_result["stdout"])
    else:
        raise Exception("Error executing hammer command", cmd_result["returncode"], cmd_result["stderr"])


def get_content_view(name):
    return execute_hammer_cmd(["content-view", "info"], name=name, organization=DEFAULT_ORG_NAME)


def get_subnet(name):
    return execute_hammer_cmd(["subnet", "info"], name=name)


def get_proxy(name):
    return execute_hammer_cmd(["proxy", "info"], name=name)


def get_os(title):
    return execute_hammer_cmd(["os", "info"], title=title)


def get_hostgroup(name):
    return execute_hammer_cmd(["hostgroup", "info"], name=name)


def get_discovered_hosts():
    return execute_hammer_cmd(["discovery", "list"])


def check_exists(hammer_type, name, uses_org=True):
    try:
        if uses_org:
            execute_hammer_cmd([hammer_type, "info"], name=name, organization=DEFAULT_ORG_NAME)
        else:
            execute_hammer_cmd([hammer_type, "info"], name=name)
    except Exception as e:
        message, returncode, stderr = e.args
        if returncode == 70 and stderr.find("not found") >= 0:
            return False
        else:
            raise e

    return True


def create_hostgroup(name, **kwargs):
    print("Creating host group " + name)
    if check_exists("hostgroup", name, uses_org=False):
        print("Skipping creation of host group %s.  Host group already created" % name)
        return

    result = execute_hammer_cmd(["hostgroup", "create"], name=name, organization=DEFAULT_ORG_NAME, **kwargs)
    print("Completed creating host group " + name)
    return result


def set_hostgroup_param(hostgroup_name, param_name, param_value):
    print("Setting host group %s parameter %s: %s" % (hostgroup_name, param_name, param_value))
    result = execute_hammer_cmd(["hostgroup", "set-parameter"],
                                hostgroup=hostgroup_name,
                                name=param_name,
                                value=param_value)
    print("Successfully set host group %s parameter %s: %s" % (hostgroup_name, param_name, param_value))
    return result


def create_activation_key(name, **kwargs):
    print("Creating activation key " + name)
    if check_exists("activation-key", name):
        print("Skipping creation of activation key %s. Activation key already created" % name)
        return

    result = execute_hammer_cmd(["activation-key", "create"], name=name, organization=DEFAULT_ORG_NAME, **kwargs)
    print("Completed creating activation key " + name)
    return result


def provision_host(discovered_hostname, new_hostname, hostgroup, **kwargs):
    print("Attempting to provisioning discovered host %s to become %s in hostgroup %s" % (discovered_hostname, new_hostname, hostgroup))
    result = execute_hammer_cmd(["discovery", "provision"],
                                name=discovered_hostname,
                                new_name=new_hostname,
                                hostgroup=hostgroup,
                                build="true",
                                enabled="true",
                                managed="true",
                                **kwargs)
    print("Triggered provisioning of host %s in hostgroup %s from discovered host %s" % (new_hostname, hostgroup, discovered_hostname))
    return result
