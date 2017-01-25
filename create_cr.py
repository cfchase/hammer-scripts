from config import satellite
from config import rhv

from utils.hammer import *


def create_cr(deployment):
    print("****************** Creating Compute Resource ******************")

    cr_name = deployment["label"] + "-RHV"
    print(cr_name)
    create_compute_resource(cr_name,
                            locations="Default Location",
                            url="https://%s/ovirt-engine/api/v3" % deployment["rhv"]["engine_managed_host_name"],
                            provider="Ovirt",
                            user="admin@internal",
                            password=deployment["rhv"]["root_password"])

    print("****************** Completed Creating Compute Resource ******************")
