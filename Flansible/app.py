import platform

#Visual studio remote debugger
if platform.node() == 'ansible':
    try:
        import ptvsd
        ptvsd.enable_attach(secret='my_secret', address = ('0.0.0.0', 3000))
    except:
        pass

import os
import time
import sys
import json
from threading import Thread
from subprocess import Popen, PIPE
import subprocess
from Queue import Queue, Empty
from datetime import datetime
from ConfigParser import SafeConfigParser
from flask import render_template
from flask import Flask, request, render_template, session, flash, redirect, url_for, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, Api, reqparse, fields
from flask_restful_swagger import swagger
import celery.events.state
from celery import Celery

from ModelClasses import AnsibleCommandModel, AnsiblePlaybookModel, AnsibleRequestResultModel, AnsibleExtraArgsModel



#Setup queue for celery
io_q = Queue()

app = Flask(__name__)
auth = HTTPBasicAuth()

this_path = sys.path[0]

config = SafeConfigParser()
config.read('config.ini')

ansible_config = SafeConfigParser()
try:
    ansible_config.read('/etc/ansible/ansible.cfg')
    ansible_default_inventory = config.get("Defaults", "inventory")
except:
    ansible_default_inventory = '/etc/ansible/hosts'

app.config['CELERY_BROKER_URL'] = config.get("Default", "CELERY_BROKER_URL")
app.config['CELERY_RESULT_BACKEND'] = config.get("Default", "CELERY_RESULT_BACKEND")
str_task_timeout = config.get("Default", "CELERY_TASK_TIMEOUT")
playbook_root = config.get("Default", "playbook_root")
playbook_filter = config.get("Default", "playbook_filter")
task_timeout = int(str_task_timeout)

api = swagger.docs(Api(app), apiVersion='0.1')

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], )
celery.control.time_limit('do_long_running_task', soft=900, hard=900, reply=True)
celery.conf.update(app.config)

inventory_access = []


  
    


            

if __name__ == '__main__':
    app.run(debug=True, host=config.get("Default", "Flask_tcp_ip"), use_reloader=False, port=int(config.get("Default", "Flask_tcp_port")))