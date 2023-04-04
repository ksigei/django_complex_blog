from django.contrib import admin

from .models import Category, Post, Comment, Vote, Bookmark
regs = [Category, Post, Comment, Vote, Bookmark]
admin.site.register(regs)
