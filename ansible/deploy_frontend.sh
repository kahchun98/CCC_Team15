#!/bin/bash

. ./unimelb-comp90024-2021-grp-15-openrc.sh; ansible-playbook -vvvv -i inventory/hosts.ini -u ubuntu --key-file=~/.ssh/ansible.pem deploy_frontend.yaml

#chmod +x ./set_docker.sh