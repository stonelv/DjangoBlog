#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoblog.settings')
sys.path.insert(0, '/Users/lvzhe/github/DjangoBlog')
django.setup()

from blog.views import IndexView
from django.test import RequestFactory

# 创建一个模拟请求
factory = RequestFactory()
request = factory.get('/')

# 尝试渲染IndexView
view = IndexView.as_view()
try:
    response = view(request)
    print("Success! Response status:", response.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
