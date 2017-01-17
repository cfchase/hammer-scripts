from config import satellite
from config import rhv

from utils.hammer import *

def create_compute_resource(deployment):
    print("****************** Creating Compute Resource ******************")

    # ::Fusor.log.debug '====== RHV Compute Resource run method ======'
    # deployment = ::Fusor::Deployment.find(input[:deployment_id])
    # rhevm  = ::Host.find(deployment.rhev_engine_host_id).name
    # api_url = "https://#{rhevm}/ovirt-engine/api/v3"
    # ca_url = "http://#{rhevm}/ovirt-engine/services/pki-resource?resource=ca-certificate&format=X509-PEM-CA"
    # ca_cert = "#{Net::HTTP.get(URI.parse(ca_url))}"
    # rhev = { "name" => "#{deployment.label}-RHEV",
    #          "location_ids" => ["", Location.where(:name => "Default Location").first.id],
    #          "url" => api_url,
    #          "provider" => "Foreman::Model::Ovirt", "user" => 'admin@internal',
    #          "password" => deployment.rhev_root_password,
    #          "organization_ids" => [deployment.organization_id],
    #          "public_key" => ca_cert }
    # cr = ::Foreman::Model::Ovirt.create(rhev)
    # cr.uuid = cr.datacenters.find { |dc| dc[0] == deployment.rhev_data_center_name }[1]
    # cr.save
    # ::Fusor.log.debug '=== Leaving RHV Compute Resource run method ==='

    print("****************** Completed Creating Compute Resource ******************")
