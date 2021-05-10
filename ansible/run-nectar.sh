#!/bin/bash

. ./unimelb-comp90024-2021-grp-15-openrc.sh; ansible-playbook -i hosts.ini -u ubuntu --key-file=~/.ssh/ansible.pem --ask-become-pass mrc.yaml