#!/usr/bin/env bash

source hammer-helpers.sh
#set -x

echo "****************** Enabling Repos ******************"

enable_repo 'Red Hat Enterprise Linux Server' \
            '7Server' \
            'x86_64' \
            'Red Hat Enterprise Linux 7 Server (RPMs)' \
            'Red Hat Enterprise Linux 7 Server RPMs x86_64 7Server'

enable_repo 'Red Hat Enterprise Linux Server' \
            '7.3' \
            'x86_64' \
            'Red Hat Enterprise Linux 7 Server (Kickstart)' \
            'Red Hat Enterprise Linux 7 Server Kickstart x86_64 7.3'

enable_repo 'Red Hat Enterprise Linux Server' \
            '' \
            'x86_64' \
            'Red Hat Satellite Tools 6.2 (for RHEL 7 Server) (RPMs)' \
            'Red Hat Satellite Tools 6.2 for RHEL 7 Server RPMs x86_64'

enable_repo 'Red Hat Enterprise Linux Server' \
            '7Server' \
            'x86_64' \
            'Red Hat Enterprise Linux 7 Server - Supplementary (RPMs)' \
            'Red Hat Enterprise Linux 7 Server - Supplementary RPMs x86_64 7Server'

enable_repo 'Red Hat Enterprise Linux Server' \
            '7Server' \
            'x86_64' \
            'Red Hat Enterprise Linux 7 Server - Optional (RPMs)' \
            'Red Hat Enterprise Linux 7 Server - Optional RPMs x86_64 7Server'

enable_repo 'JBoss Enterprise Application Platform' \
            '7Server' \
            'x86_64' \
            'JBoss Enterprise Application Platform 7 (RHEL 7 Server) (RPMs)' \
            'JBoss Enterprise Application Platform 7 RHEL 7 Server RPMs x86_64 7Server'

enable_repo 'Red Hat Virtualization' \
            '' \
            'x86_64' \
            'Red Hat Virtualization Manager 4.0 (RHEL 7 Server) (RPMs)' \
            'Red Hat Virtualization Manager 4.0 RHEL 7 Server RPMs x86_64'

enable_repo 'Red Hat Virtualization' \
            '7Server' \
            'x86_64' \
            'Red Hat Virtualization 4 Management Agents for RHEL 7 (RPMs)' \
            'Red Hat Virtualization 4 Management Agents for RHEL 7 RPMs x86_64 7Server'

list_repos

echo "****************** Completed Enabling Repos ******************"

echo '****************** Syncing Repos ******************'
task_ids=()

task_ids+=($(sync_repo 'Red Hat Enterprise Linux Server' 'Red Hat Enterprise Linux 7 Server RPMs x86_64 7Server'))
task_ids+=($(sync_repo 'Red Hat Enterprise Linux Server' 'Red Hat Enterprise Linux 7 Server Kickstart x86_64 7.3'))
task_ids+=($(sync_repo 'Red Hat Enterprise Linux Server' 'Red Hat Satellite Tools 6.2 for RHEL 7 Server RPMs x86_64'))
task_ids+=($(sync_repo 'Red Hat Enterprise Linux Server' 'Red Hat Enterprise Linux 7 Server - Supplementary RPMs x86_64 7Server'))
task_ids+=($(sync_repo 'Red Hat Enterprise Linux Server' 'Red Hat Enterprise Linux 7 Server - Optional RPMs x86_64 7Server'))
task_ids+=($(sync_repo 'JBoss Enterprise Application Platform' 'JBoss Enterprise Application Platform 7 RHEL 7 Server RPMs x86_64 7Server'))
task_ids+=($(sync_repo 'Red Hat Virtualization' 'Red Hat Virtualization Manager 4.0 RHEL 7 Server RPMs x86_64'))
task_ids+=($(sync_repo 'Red Hat Virtualization' 'Red Hat Virtualization 4 Management Agents for RHEL 7 RPMs x86_64 7Server'))

echo ${task_ids[@]}
echo '****************** Completed Syncing Repos ******************'
