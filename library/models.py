from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,password=None):
        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_reader = True
        user.is_active=True
        user.save(using=self._db)
        return user
    
    def create_admin(self, first_name, last_name, email, password=None):
        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_admin=True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,email,password=None):
        user=self.model(
            email=self.normalize_email(email), 
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superadmin(self,first_name,last_name,email,password=None):
        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        # user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.set_password(password)
        user.save(using=self._db)
        return user
    


class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    # push_token=models.CharField(max_length=100,null=True,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)

    is_admin=models.BooleanField(default=False)
    is_reader = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    #is_masteradmin=models.BooleanField(default=False)
    #is_project_director=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name']

    

    objects=MyAccountManager()

    def has_perm(self, perm, obj=None):
        if self.is_superadmin  or self.is_admin:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_superadmin or self.is_admin:
            return True
        return False
    
    def _str_(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def role(self):
        if self.is_superadmin:
            return "Super Admin"
        elif self.is_admin:
            return "Admin"
        else:
            return "Reader"
    
    def can_upload_books(self):
        return self.is_superadmin or self.is_admin
    
    def can_manage_admins(self):
        return self.is_superadmin

class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biographie'),
        ('history', 'History'),
        ]
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True, null = True)
    category = models.CharField(max_length=30, choices=catchoice, default = 'education')
    isbn = models.PositiveIntegerField(unique=True, help_text="13 Character ISBN number")
    description = models.TextField(blank=True, null=True, help_text="Book description or summary")
    cover_image = models.ImageField(upload_to='books/covers/', blank=True, null=True)
    language = models.CharField(max_length=50, default='English')

    def __str__(self):
        return self.name
    
class BookRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned')
    ] 
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.full_name} - {self.book.name}"