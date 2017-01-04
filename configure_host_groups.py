#!/usr/bin/env python

from config import satellite
from config import rhv_deployment

from hammer_helpers import *

print("****************** Configuring Host Groups ******************")
proxy_id = str(get_proxy(satellite.SERVER_FQDN)["Id"])
medium_id = str(get_os(rhv_deployment.OS_TITLE)["Installation media"][0]["id"])

create_hostgroup("Fusor Base", domain=satellite.DOMAIN_NAME, subnet=satellite.SUBNET_NAME)
set_hostgroup_param("Fusor Base", "ntp_server", SERVER_FQDN)

# deployment hostgroup
create_hostgroup(rhv_deployment.LABEL,
                 parent="Fusor Base",
                 lifecycle_environment=rhv_deployment.LIFECYCLE,
                 content_view=rhv_deployment.CONTENT_VIEW,
                 content_source_id=proxy_id,
                 puppet_ca_proxy_id=proxy_id,
                 puppet_proxy_id=proxy_id)

# hostgroups belonging to deployment hostgroup
hg_name = "RHV-Engine"
create_hostgroup(hg_name,
                 parent=rhv_deployment.LABEL,
                 lifecycle_environment=rhv_deployment.LIFECYCLE,
                 content_view=rhv_deployment.CONTENT_VIEW,
                 architecture=rhv_deployment.ARCHITECTURE_NAME,
                 operatingsystem=rhv_deployment.OS_TITLE,
                 medium_id=medium_id,
                 partition_table=rhv_deployment.PARTITION_TABLE_NAME,
                 root_pass=rhv_deployment.ROOT_PASS)

key_name = "RHV_Engine-" + rhv_deployment.LABEL + "-RHV_Engine"
create_activation_key(key_name,
                      lifecycle_environment=rhv_deployment.LIFECYCLE,
                      content_view=rhv_deployment.CONTENT_VIEW)
set_hostgroup_param("RHV-Engine", "kt_activation_keys", key_name)


hg_name = "RHV-Hypervisor"
create_hostgroup(hg_name,
                 parent=rhv_deployment.LABEL,
                 lifecycle_environment=rhv_deployment.LIFECYCLE,
                 content_view=rhv_deployment.CONTENT_VIEW,
                 architecture=rhv_deployment.ARCHITECTURE_NAME,
                 operatingsystem=rhv_deployment.OS_TITLE,
                 medium_id=medium_id,
                 partition_table=rhv_deployment.PARTITION_TABLE_NAME,
                 root_pass=rhv_deployment.ROOT_PASS)

key_name = "RHV_Hypervisor-" + rhv_deployment.LABEL + "-RHV_Hypervisor"
create_activation_key(key_name,
                      lifecycle_environment=rhv_deployment.LIFECYCLE,
                      content_view=rhv_deployment.CONTENT_VIEW)
set_hostgroup_param(hg_name, "kt_activation_keys", key_name)

print("****************** Completed Configuring Host Groups ******************")
