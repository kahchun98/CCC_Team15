#!/bin/bash



. ./unimelb-comp90024-2021-grp-15-openrc.sh; ansible-playbook --ask-become-pass -i hosts -u ubuntu --key-file=~/.ssh/ansible.pem set_environments.yaml