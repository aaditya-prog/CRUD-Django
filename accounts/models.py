from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from PIL import Image


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(max_length=30, blank=True)
    full_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="last login")
    USERNAME_FIELD = "email"

    # def save(self, *args, **kwargs):
    #     if self.admin != "True" and self.update_password:
    #         self.set_password(self.password)
    #     super(CustomUser, self).save(*args, **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def __str__(self):
        return self.email

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def is_superuser(self):
        return self.admin


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png", upload_to="profile_pics/")

    def __str__(self):
        return f"{self.user.full_name} Profile"

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)
