#!/usr/bin/env bash

source hammer-helpers.sh
#set -x

echo '****************** Preparing Org  ******************'
create_product Fusor

create_repo Fusor Puppet Puppet1 puppet

create_repo Fusor ose-docker-registry ose-docker-registry docker \
            'https://registry.access.redhat.com/' 'openshift3/ose-docker-registry'

create_repo Fusor ose-haproxy-router ose-haproxy-router docker \
            'https://registry.access.redhat.com/' 'openshift3/ose-docker-registry'

create_repo Fusor ose-deployer ose-deployer docker \
            'https://registry.access.redhat.com/' 'openshift3/ose-docker-registry'

create_repo Fusor ose-sti-builder ose-sti-builder docker \
            'https://registry.access.redhat.com/' 'openshift3/ose-docker-registry'

create_repo Fusor ose-pod ose-pod docker \
            'https://registry.access.redhat.com/' 'openshift3/ose-docker-registry'

create_repo Fusor ose-docker-builder ose-docker-builder docker \
            'https://registry.access.redhat.com/' 'openshift3/ose-docker-registry'

create_repo Fusor ose-keepalived-ipfailover ose-keepalived-ipfailover docker \
            'https://registry.access.redhat.com/' 'openshift3/ose-docker-registry'

create_content_view 'Fusor Puppet Content'

# TODO import Access Insights Puppet classes
#importer = PuppetClassImporter.new({ :url => SmartProxy.first.url })
#changes = importer.changes
#unless changes.empty? || changes.nil?
#  ['new', 'updated', 'obsolete'].each do |kind|
#    changes[kind].each_key do |key|
#      changes[kind.to_s][key] = changes[kind.to_s][key].to_json
#    end
#  end
#  PuppetClassImporter.new.obsolete_and_new(changes)
#end


# TODO check version of last published version and only publish if necessary
#cv_version=$(check_content_view_version 'Fusor Puppet Content')
#if [[ -z $cv_version || $(cmp.awk $cv_version 1.0) -lt 0 ]]; then
  publish_content_view 'Fusor Puppet Content'
#fi

echo '****************** Completed Preparing Org  ******************'
