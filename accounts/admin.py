from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import BlogUser, Notification


class BlogUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Enter password again'), widget=forms.PasswordInput)

    class Meta:
        model = BlogUser
        fields = ('email', 'username', 'nickname')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("passwords do not match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.source = 'adminsite'
            user.save()
        return user


class BlogUserChangeForm(UserChangeForm):
    class Meta:
        model = BlogUser
        fields = '__all__'
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BlogUserAdmin(UserAdmin):
    form = BlogUserChangeForm
    add_form = BlogUserCreationForm
    list_display = ['email', 'username', 'nickname', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('nickname',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'nickname', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'username', 'nickname')
    ordering = ('-id',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'sender', 'notification_type', 'is_read', 'create_time']
    list_filter = ['notification_type', 'is_read', 'create_time']
    search_fields = ['title', 'content', 'recipient__username', 'recipient__email']
    fieldsets = (
        (None, {'fields': ('recipient', 'sender', 'title', 'content', 'target_url')}),
        (_('Type & Status'), {'fields': ('notification_type', 'is_read')}),
    )
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = _('Mark selected notifications as read')

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = _('Mark selected notifications as unread')


admin.site.register(BlogUser, BlogUserAdmin)
admin.site.register(Notification, NotificationAdmin)
