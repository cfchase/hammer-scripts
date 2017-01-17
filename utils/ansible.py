###################################
# Ansible
###################################

import utils.shell


def run_ansible(playbook, inv_file_path, vars_file_path, environment):
    print("ansible-playbook %s -i %s -e @%s" % (playbook, inv_file_path, vars_file_path))
    utils.shell.execute_cmd_out([
        "ansible-playbook",
        playbook,
        "-i", inv_file_path,
        "-e", "@" + vars_file_path,
        "-vvvv"
    ], env=environment)

