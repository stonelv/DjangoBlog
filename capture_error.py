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
from django.http import HttpRequest

# 创建一个模拟请求
request = HttpRequest()
request.method = 'GET'
request.path = '/'
request.META['HTTP_HOST'] = '127.0.0.1:8000'

# 尝试渲染IndexView
view = IndexView.as_view()
try:
    response = view(request)
    print("Success! Response status:", response.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
    print("\nError type:", type(e))
    print("Error message:", e)
