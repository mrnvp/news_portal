from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    rating = models.FloatField()
    
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    def update_rating(self):
        posts_rating = sum(post.rating*3 for post in Post.objects.filter(author = self))
        comments_rating = sum(comment.rating for comment in Comment.objects.filter(user = self.user))
        comments_posts_rate = sum(comment.rating for post in Post.objects.filter(author=self) for comment in post.comment_set.all())
        
        self.rating = posts_rating + comments_posts_rate + comments_rating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    

class Post(models.Model):
    new = 'NW'
    paper = 'PR'
    
    TYPES = [
        (new, 'новость'),
        (paper, 'статья')
    ]
    
    name = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.FloatField()
    datetime_in = models.DateTimeField(auto_now_add = True)
    type = models.CharField(max_length=2, choices=TYPES, default=paper)
    
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    category = models.ManyToManyField(Category, through= 'PostCategory')
    
    def like(self):
        self.rating += 1
        self.save()
        
    def dislike(self):
        if self.rating:
            self.rating -= 1
        
        self.save()
    
    def preview(self):
        return f"{self.text[:124]}..."
    
class PostCategory(models.Model):

    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    

class Comment(models.Model):
    
    rating = models.FloatField()
    datetime_in = models.DateTimeField(auto_now_add = True)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
