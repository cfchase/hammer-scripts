#!/usr/bin/env bash

source config.sh

###################################
# Repositories
###################################

check_repo ()
{
    local cmd_result=$(hammer --server $SERVER \
                              --username $USERNAME \
                              --password $PASSWORD \
                              repository info \
                              --organization-label $ORG_LABEL \
                              --product "$1" \
                              --name "$2" 2>&1)

    if [[ $cmd_result == *"not found"* ]]; then
        echo false
    else
        echo true
    fi
}

create_repo ()
{
#hammer repository create --name "repo_name" \
#  --organization-label org_label --product "product_name" \
#  --content-type cont_type --publish-via-http true \
#  --url "repo_url"

    local repo_enabled=$(check_repo "$1" "$2")

    if [[ $repo_enabled == false ]]; then
        echo "Creating repository $1 $2"
        local cmd_result=$(hammer --server $SERVER \
                                  --username $USERNAME \
                                  --password $PASSWORD \
                                  repository create \
                                  --organization-label $ORG_LABEL \
                                  --product "$1" \
                                  --name "$2"\
                                  --label "$3" \
                                  --content-type "$4" \
                                  $([[ !  -z  "$5"  ]] && echo "--publish-via-http true --url ""$5") \
                                  $([[ !  -z  "$6"  ]] && echo "--docker-upstream-name ""$6"))
        echo $cmd_result
    else
        echo "Skipping creation of repository $1 $2.  Repository already created"
    fi
}

disable_repo ()
{
    local cmd_result=$(hammer --server $SERVER \
                              --username $USERNAME \
                              --password $PASSWORD \
                              repository-set disable \
                              --organization-label $ORG_LABEL \
                              --product "$1" \
                              $([[ !  -z  "$2"  ]] && echo "--releasever " "$2") \
                              --basearch "$3" \
                              --name "$4")
    echo $cmd_result
}

enable_repo ()
{
    local repo_enabled=$(check_repo "$1" "$5")

    if [[ $repo_enabled == false ]]; then
        echo "Enabling $5"
        local cmd_result=$(hammer --server $SERVER \
                                  --username $USERNAME \
                                  --password $PASSWORD \
                                  repository-set enable \
                                  --organization-label $ORG_LABEL \
                                  --product "$1" \
                                  $([[ !  -z  "$2"  ]] && echo "--releasever " "$2") \
                                  --basearch "$3" \
                                  --name "$4")
        echo $cmd_result
    else
        echo "Skipping enabling repository $5.  Repository already enabled"
    fi
}

list_repos ()
{
    hammer --server $SERVER --username $USERNAME --password $PASSWORD repository list --organization-label $ORG_LABEL
}

sync_repo_sync ()
{
    local cmd_result=$(hammer --server $SERVER \
                              --username $USERNAME \
                              --password $PASSWORD \
                              repository synchronize \
                              --organization-label $ORG_LABEL \
                              --product "$1" \
                              --name "$2")

    echo $cmd_result
}

sync_repo_async ()
{
    local cmd_result=$(hammer --server $SERVER \
                              --username $USERNAME \
                              --password $PASSWORD \
                              repository synchronize \
                              --organization-label $ORG_LABEL \
                              --product "$1" \
                              --name "$2" \
                              --async)


    local task_id=$(echo $cmd_result | sed -nr 's/Repository is being synchronized in task ([a-f|0-9|-]+)/\1/p')
    echo $task_id
}

sync_repo ()
{
    echo $(sync_repo_async "$1" "$2")
}


###################################
# Products
###################################

check_product ()
{
    local cmd_result=$(hammer --server $SERVER \
                              --username $USERNAME \
                              --password $PASSWORD \
                              product info \
                              --organization-label $ORG_LABEL \
                              --name "$1" 2>&1)

    if [[ $cmd_result == *"not found"* ]]; then
        echo false
    else
        echo true
    fi
}

create_product ()
{
    local product_exists=$(check_product "$1")

    if [[ $product_exists == false ]]; then
        echo "Creating product $1"
        local cmd_result=$(hammer --server $SERVER \
                                  --username $USERNAME \
                                  --password $PASSWORD \
                                  product create \
                                  --organization-label $ORG_LABEL \
                                  --name "$1")
        echo $cmd_result
    else
        echo "Skipping creation of product $1.  Product already exists"
    fi
}

###################################
# Content
###################################

check_content_view ()
{
    local cmd_result=$(hammer --server $SERVER \
                              --username $USERNAME \
                              --password $PASSWORD \
                              content-view info \
                              --organization-label $ORG_LABEL \
                              --name "$1" 2>&1)

    if [[ $cmd_result == *"not found"* ]]; then
        echo false
    else
        echo true
    fi
}

create_content_view ()
{
    local content_view_exists=$(check_content_view "$1")

    if [[ $content_view_exists == false ]]; then
        echo "Creating content view $1"
        local cmd_result=$(hammer --server $SERVER \
                                  --username $USERNAME \
                                  --password $PASSWORD \
                                  content-view create \
                                  --organization-label $ORG_LABEL \
                                  --name "$1")
        echo $cmd_result
    else
        echo "Skipping creation of content view $1. Content view already exists"
    fi
}

publish_content_view ()
{
    local content_view_exists=$(check_content_view "$1")

    if [[ $content_view_exists == true ]]; then
        echo "Publishing content view $1"
        local cmd_result=$(hammer --server $SERVER \
                                  --username $USERNAME \
                                  --password $PASSWORD \
                                  content-view publish \
                                  --organization-label $ORG_LABEL \
                                  --name "$1")
        echo $cmd_result
    else
        echo "Unable to publish content view $1. Content view doesn't exist"
    fi
}

create_and_publish_content_view ()
{
    local content_view_exists=$(check_content_view "$1")

    if [[ $content_view_exists == false ]]; then
        echo "Creating content view $1"
        local cmd_result=$(hammer --server $SERVER \
                                  --username $USERNAME \
                                  --password $PASSWORD \
                                  content-view create \
                                  --organization-label $ORG_LABEL \
                                  --name "$1")
        echo $cmd_result

        echo "Creating content view $1"
        cmd_result=$(hammer --server $SERVER \
                            --username $USERNAME \
                            --password $PASSWORD \
                            content-view create \
                            --organization-label $ORG_LABEL \
                            --name "$1")
        echo $cmd_result
    else
        echo "Skipping creation and publish of content view $1. Content view already exists"
    fi
}




