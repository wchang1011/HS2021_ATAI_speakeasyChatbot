# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 12:01:58 2021

@author: Wenqing
"""
import re

qTemp1 = "([\w\s]+) the name of (the)?(.+) in ([\w\s]+)?" #What is the name of director in movie Batman?
print(re.match(qTemp1,'What is the name of director in movie Batman?').groups()())