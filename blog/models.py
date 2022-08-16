from django.db import models
import os
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=50)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # 작성자 탈퇴 시 작성한 글 모두 자동 삭제

    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author}'
    def get_absoulte_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_exit(self):
        return self.get_file_name().split('.')[-1]

# Create your models here.

