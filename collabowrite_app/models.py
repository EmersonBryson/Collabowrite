from django.db import models
import re, bcrypt, datetime
from PIL import Image

# REGEX and Validators

class UserManager(models.Manager):

    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be at least two characters long!'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least two characters long!'
        if len(postData['user_name']) < 3:
            errors['user_name'] = 'Last name should be at least three characters long!'
        else:
            userName = User.objects.filter(user_name = postData['user_name'])
            if len(userName) > 0:
                errors['username'] = 'Username already exists. Please register with a different username or log in.'
        if len(postData['email']) < 3:
            errors['email'] = 'Valid email address is required.'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        else:
            userEmail = User.objects.filter(email = postData['email'])
            if len(userEmail) > 0:
                errors['unavailable'] = 'Email already exists. Please register with a different email or log in.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long.'
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = 'Passwords do not match.'
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['user_name']) < 1:
            errors['user_name'] = 'Please enter a username.'
        else:
            user = User.objects.filter(user_name = postData['user_name'])
            if len(user) == 0:
                errors['none'] = ' not registered.'
            else:
                logged_user = user[0]
                if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                    errors['password'] = 'Password is incorrect.'
        return errors

class BoardManager(models.Manager):

    def board_validator(self, postData):
        errors = {}
        if len(postData['board_title']) < 3:
            errors['board_title'] = 'Board title must be at least three characters long!'
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length = 30)
    email = models.CharField(max_length = 255)
    user_name = models.CharField(max_length = 25)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()

class Board(models.Model):
    user = models.ForeignKey(User, related_name= "boards", on_delete = models.CASCADE, null=True)
    board_title = models.CharField(max_length = 50)
    board_topic = models.CharField(max_length = 30)
    board_tags = models.CharField(max_length = 100)
    board_image = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BoardManager()

class Section(models.Model):
    user = models.ForeignKey(User, related_name= "sections", on_delete = models.CASCADE, null=True)
    section_title = models.CharField(max_length = 100)
    section_summary = models.CharField(max_length = 255)
    board = models.ForeignKey(Board, related_name= "sections", on_delete = models.CASCADE, null= True)

class Post(models.Model):
    user = models.ForeignKey(User, related_name = "posts", on_delete = models.CASCADE, null=True)
    post_title = models.CharField(max_length = 100)
    post_content = models.CharField(max_length = 1500)
    section = models.ForeignKey(Section, related_name='posts', on_delete = models.CASCADE, null=True)
