#!/bin/bash

. ./unimelb-comp90024-2021-grp-15-openrc.sh; ansible-playbook -vvvv -i inventory/hosts.ini -u ubuntu --key-file=~/.ssh/ansible.pem deploy_backend.yaml

#chmod +x ./set_docker.sh