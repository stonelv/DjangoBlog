# Create your views here.
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView

from accounts.models import BlogUser
from blog.models import Article
from .forms import CommentForm
from .models import Comment


class CommentPostView(FormView):
    form_class = CommentForm
    template_name = 'blog/article_detail.html'

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(CommentPostView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        article_id = self.kwargs['article_id']
        article = get_object_or_404(Article, pk=article_id)
        url = article.get_absolute_url()
        return HttpResponseRedirect(url + "#comments")

    def form_invalid(self, form):
        article_id = self.kwargs['article_id']
        article = get_object_or_404(Article, pk=article_id)

        return self.render_to_response({
            'form': form,
            'article': article
        })

    def form_valid(self, form):
        """提交的数据验证合法后的逻辑"""
        user = self.request.user
        author = BlogUser.objects.get(pk=user.pk)
        article_id = self.kwargs['article_id']
        article = get_object_or_404(Article, pk=article_id)

        if article.comment_status == 'c' or article.status == 'c':
            raise ValidationError("该文章评论已关闭.")
        comment = form.save(False)
        comment.article = article
        from djangoblog.utils import get_blog_setting
        settings = get_blog_setting()
        if not settings.comment_need_review:
            comment.is_enable = True
        comment.author = author

        if form.cleaned_data['parent_comment_id']:
            parent_comment = Comment.objects.get(
                pk=form.cleaned_data['parent_comment_id'])
            comment.parent_comment = parent_comment

            # 发送评论回复通知
            if parent_comment.author != author:
                from accounts.models import Notification
                title = _('Your comment has been replied')
                content = _('%(username)s replied your comment: %(content)s') % {
                    'username': author.username,
                    'content': comment.body[:50] + '...' if len(comment.body) > 50 else comment.body
                }
                target_url = f"{article.get_absolute_url()}#div-comment-{comment.pk}"
                Notification.objects.create(
                    recipient=parent_comment.author,
                    sender=author,
                    title=title,
                    content=content,
                    notification_type=Notification.NotificationType.COMMENT_REPLY,
                    target_url=target_url
                )

        comment.save(True)
        return HttpResponseRedirect(
            "%s#div-comment-%d" %
            (article.get_absolute_url(), comment.pk))
