#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoblog.settings')
sys.path.insert(0, '/Users/lvzhe/github/DjangoBlog')
django.setup()

from django.core.cache import cache

# 检查缓存
keys = cache.keys('*')
print('Cache keys:', keys)

for key in keys:
    value = cache.get(key)
    print(f'Key: {key}, Type: {type(value)}')
    if hasattr(value, '__iter__'):
        try:
            print(f'  Length: {len(value)}')
            if len(value) > 0:
                print(f'  First item type: {type(value[0])}')
        except:
            print(f'  Cannot iterate')
