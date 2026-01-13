
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoblog.settings")
django.setup()

from accounts.models import BlogUser
from blog.models import Article, Category, Tag

def seed():
    # Create User
    if not BlogUser.objects.filter(username="admin").exists():
        user = BlogUser.objects.create_superuser("admin", "admin@example.com", "password")
        print("Superuser created.")
    else:
        user = BlogUser.objects.get(username="admin")

    # Create Category
    category, created = Category.objects.get_or_create(
        name="Tech",
        defaults={'slug': 'tech', 'parent_category': None}
    )
    if created:
        print("Category created.")

    # Create Tag
    tag, created = Tag.objects.get_or_create(
        name="Django",
        defaults={'slug': 'django'}
    )
    if created:
        print("Tag created.")

    # Create Article
    if not Article.objects.filter(title="Test Article").exists():
        article = Article.objects.create(
            title="Test Article",
            body="This is a test article body.",
            status='p', # Published
            type='a', # Article
            author=user,
            category=category
        )
        article.tags.add(tag)
        article.save()
        print(f"Article created with ID: {article.id}")
    else:
        print("Article already exists.")

if __name__ == "__main__":
    seed()
