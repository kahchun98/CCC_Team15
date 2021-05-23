#!/bin/bash

. ./unimelb-comp90024-2021-grp-15-openrc.sh; ansible-playbook -i inventory/hosts.ini -u ubuntu --key-file=~/.ssh/ansible.pem deploy_frontend_and_backend.yaml

#chmod +x ./set_docker.sh