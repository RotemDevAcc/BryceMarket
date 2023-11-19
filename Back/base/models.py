from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission

class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)

class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    # Add this line for the manager
    objects = UserProfileManager()

    # Define custom through model for groups and user_permissions
    groups = models.ManyToManyField(
        Group, related_name="user_profiles", through="UserProfileGroup"
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="user_profiles", through="UserProfilePermission"
    )

    def __str__(self):
        return self.username

class UserProfileGroup(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class UserProfilePermission(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

class Receipt(models.Model):
    id = models.AutoField(primary_key=True)
    products = models.TextField()
    price = models.FloatField(null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)  # Foreign key to User

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=80,null=True)
    def __str__(self):
           return self.desc
    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,null=True)
    desc = models.CharField(max_length=80,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    img = models.ImageField(null=True,blank=True,default='/placeholder.png')
    createdTime=models.DateTimeField(auto_now_add=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)  # Foreign key to Category
 
    def __str__(self):
           return self.desc