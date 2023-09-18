from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, mobile_number, age, course, occupation, location, tc, password=None, password2=None, otp=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          mobile_number = mobile_number,
          age = age,
          course = course,
          occupation = occupation,
          location = location,
          otp=otp,
          tc=tc,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, mobile_number, age, course, occupation, location, tc, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          name = name,
          mobile_number=mobile_number,
          age= age,
          course=course,
          occupation=occupation,
          location=location,
          password=password,
          tc=tc,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  name = models.CharField(max_length=200,unique=True)
  email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
  mobile_number = models.CharField(max_length=17, default=None, unique=True)
  age = models.IntegerField(default=None)
  course = models.CharField(max_length=200, default=None)
  occupation = models.CharField(max_length=200, default=None )
  location = models.CharField(max_length=200, default=None)
  otp = models.CharField(max_length=4, null=True, blank=True)
  tc = models.BooleanField()
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name','mobile_number', 'age', 'course', 'occupation', 'location', 'tc']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin



