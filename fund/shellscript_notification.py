#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/26 16:00
# @Author  : Xingqi Tang
# @Contact : xingqitangatgmaildotcom
# @File    : shellscript_notification.py
# @Software: PyCharm
from subprocess import call

from fund import fund_utils

msg = fund_utils.daily_notification()

cmd = 'display notification \"' + \
      "%s" % msg + '\" with title \"Daily Notes\"'
call(["osascript", "-e", cmd])
