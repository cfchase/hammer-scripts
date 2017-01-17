from config import satellite
from config import rhv

from utils.hammer import *


def configure_host_groups(deployment):
    print("****************** Configuring Host Groups ******************")
    proxy_id = str(get_proxy(satellite.SERVER_FQDN)["Id"])
    medium_id = str(get_os(rhv.OS_TITLE)["Installation media"][0]["id"])

    create_hostgroup("Fusor Base", domain=satellite.DOMAIN_NAME, subnet=satellite.SUBNET_NAME)
    set_hostgroup_param("Fusor Base", "ntp_server", SERVER_FQDN)

    # deployment hostgroup
    create_hostgroup(deployment["label"],
                     parent="Fusor Base",
                     lifecycle_environment=rhv.LIFECYCLE,
                     content_view=rhv.CONTENT_VIEW,
                     content_source_id=proxy_id,
                     puppet_ca_proxy_id=proxy_id,
                     puppet_proxy_id=proxy_id)

    # hostgroups belonging to deployment hostgroup
    hg_name = "RHV-Engine"
    create_hostgroup(hg_name,
                     parent=deployment["label"],
                     lifecycle_environment=rhv.LIFECYCLE,
                     content_view=rhv.CONTENT_VIEW,
                     architecture=rhv.ARCHITECTURE_NAME,
                     operatingsystem=rhv.OS_TITLE,
                     medium_id=medium_id,
                     partition_table=rhv.PARTITION_TABLE_NAME,
                     root_pass=rhv.ROOT_PASS,
                     locations=satellite.DEFAULT_LOCATION_NAME)

    key_name = "RHV_Engine-" + deployment["label"] + "-RHV_Engine"
    create_activation_key(key_name,
                          lifecycle_environment=rhv.LIFECYCLE,
                          content_view=rhv.CONTENT_VIEW)
    set_hostgroup_param("RHV-Engine", "kt_activation_keys", key_name)

    hg_name = "RHV-Hypervisor"
    create_hostgroup(hg_name,
                     parent=deployment["label"],
                     lifecycle_environment=rhv.LIFECYCLE,
                     content_view=rhv.CONTENT_VIEW,
                     architecture=rhv.ARCHITECTURE_NAME,
                     operatingsystem=rhv.OS_TITLE,
                     medium_id=medium_id,
                     partition_table=rhv.PARTITION_TABLE_NAME,
                     root_pass=rhv.ROOT_PASS,
                     locations=satellite.DEFAULT_LOCATION_NAME)

    key_name = "RHV_Hypervisor-" + deployment["label"] + "-RHV_Hypervisor"
    create_activation_key(key_name,
                          lifecycle_environment=rhv.LIFECYCLE,
                          content_view=rhv.CONTENT_VIEW)
    set_hostgroup_param(hg_name, "kt_activation_keys", key_name)

    print("****************** Completed Configuring Host Groups ******************")

