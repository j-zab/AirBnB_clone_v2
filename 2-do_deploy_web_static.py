#!/usr/bin/python3
"""script that distributes archive to webservers"""
from fabric.api import local, hosts
from datetime import datetime
from fabric.contrib.files import exists
hosts_list = ['ubuntu@34.207.190.235', 'ubuntu@100.24.255.166']


@hosts(hosts_list)
def do_deploy(archive_path):
