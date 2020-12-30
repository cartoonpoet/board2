import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group


class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, id, name, password):
        user = self.model(
            id=id,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, name, password):
        u = self.create_user(id=id, name=name, password=password)
        u.is_admin = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):

    id = models.TextField(unique=True, verbose_name='아이디', primary_key=True)
    password = models.TextField(verbose_name='비번', max_length=40)
    name = models.CharField(verbose_name='이름', max_length=20)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')
    is_admin = models.BooleanField(default=False, verbose_name='관리자 여부')

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def __str__(self):
        return self.id

    @property
    def is_staff(self):
        return self.is_admin


class Group(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, null=False)

    class Meta:
        db_table = 'group'


class User_Group(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=False, default='')
    group_id = models.ForeignKey('Group', on_delete=models.CASCADE, null=False, default='')

    class Meta:
        db_table = 'user_group'