from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.TextField()
    cat_image = models.ImageField(upload_to='images/categories')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.id)])
    
    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    post_image = models.ImageField(upload_to='images/posts', blank=True, default='images/posts/default.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    votes = models.ManyToManyField(User, related_name='votes', blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(timezone.timedelta(days=1), default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Posts'
    def total_votes(self):
        upvotes = self.vote_set.filter(vote_type=1).count()
        downvotes = self.vote_set.filter(vote_type=-1).count()
        return upvotes - downvotes
    
    def num_comments(self):
        return Comment.objects.filter(post=self).count()
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    def drafts(self):
        return Post.objects.filter(is_published=False, User=self.author).order_by('created_at')
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Comments'

class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.IntegerField(choices=((1, 'Upvote'), (-1, 'Downvote')), default=1)

    def __str__(self):
        return self.vote

    class Meta:
        verbose_name_plural = 'Votes'

class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title

    class Meta:
        verbose_name_plural = 'Bookmarks'