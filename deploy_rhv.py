#!/usr/bin/env python

from config import satellite
from config import rhv

from hammer_helpers import *

print("****************** Deploying RHV ******************")


# hosts_with_hostgroups(deployment).each do |host, hostgroup|
#     plan_action(::Actions::Fusor::Host::TriggerProvisioning,
#                                         deployment,
#                                         hostgroup,
#                                         host)
# end
#
# concurrence do
#     hosts_with_hostgroups(deployment).each do |host, hostgroup|
#         plan_action(::Actions::Fusor::Host::WaitUntilProvisioned,
#                                             host.id)
#         end
# end
#
# plan_action(::Actions::Fusor::Deployment::Rhev::TriggerAnsibleRun, deployment)
# plan_action(::Actions::Fusor::Deployment::Rhev::WaitForDataCenter,
#                                                 deployment)
# plan_action(::Actions::Fusor::Deployment::Rhev::CreateCr, deployment)

print("****************** Completed Deploying RHV ******************")

