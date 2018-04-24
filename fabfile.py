#!/usr/bin/env python
# _*_ encoding: utf-8 _*_

from datetime import datetime
from fabric3.api import *


def prepare_deploy():
    local("./manage.py test my_app")