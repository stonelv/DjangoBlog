#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoblog.settings')
sys.path.insert(0, '/Users/lvzhe/github/DjangoBlog')
django.setup()

from blog.models import Article
from django.core.paginator import Paginator

# 测试QuerySet切片
article_list = Article.objects.filter(type='a', status='p')
print(f"Article count: {article_list.count()}")

# 尝试不同的切片方式
try:
    # 测试整数索引
    article = article_list[0]
    print(f"First article: {article.title}")
except Exception as e:
    print(f"Error with integer index: {e}")
    import traceback
    traceback.print_exc()

try:
    # 测试切片
    articles = article_list[:10]
    print(f"First 10 articles: {len(articles)}")
except Exception as e:
    print(f"Error with slice: {e}")
    import traceback
    traceback.print_exc()

# 测试Paginator
print("\nTesting Paginator:")
try:
    paginator = Paginator(article_list, 10)
    page1 = paginator.page(1)
    print(f"Page 1 has {page1.object_list.count()} articles")
except Exception as e:
    print(f"Error with Paginator: {e}")
    import traceback
    traceback.print_exc()
