from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
# local
from post.models import Post


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.datetime.now)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return str(self.user.username) + " " + str(self.post.title)  + " " + str(self.content)

    def parent_comments(self):
        return Comment.objects.filter(parent=None, )

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent == None:
            return True
        else:
            return False
