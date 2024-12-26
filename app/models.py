
# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError



class HashTag(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

def validate_image_or_video(value):

    valid_mime_types = [
        'image/jpeg', 'image/png', 'image/gif',  
        'video/mp4', 'video/mpeg', 'video/quicktime'  
    ]
    if value.file.content_type not in valid_mime_types:
        raise ValidationError('Only image or video files are allowed.')

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="tweets")
    content = models.TextField(max_length=280)  # Limiting tweet length to 280 characters
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(HashTag,related_name="tweet")
    media = models.FileField(
        upload_to='tweets/media/',
        blank=True,
        null=True,
        validators=[validate_image_or_video] 
    )

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"  
    def is_image(self):
        return self.media.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

    def is_video(self):
        return self.media.name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
    def like_count(self):

        return self.likes.count()
    def total_comments(self):
        return self.comments.count()

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_comments(self):
        return self.comments.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    post = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post.title}"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Preventing duplicate follows

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"



class Trending(models.Model):
    tag =  models.CharField(max_length=20)
    post = models.ForeignKey(Tweet,on_delete=models.CASCADE)
    date_created =  models.DateTimeField(auto_created=True)
    
class Bookmark(models.Model):
    post = models.ForeignKey(Tweet,on_delete=models.CASCADE,related_name="bookmarks")
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} bookmarked {self.post}"
    

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic = models.ImageField(upload_to="users/",null=True)
    banner_pic = models.ImageField(upload_to="banner/",null=True)

    

    
