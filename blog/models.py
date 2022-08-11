from django.db import models
import os
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}'
    def get_absoulte_url(self):
        return f'/blog/{self.pk}/'

    def get_file_exit(self):
        return os.path.basename(self.file_upload.name)

    def get_file_exit(self):
        return self.get_file_name().split('.')[-1]

# Create your models here.

