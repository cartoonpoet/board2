from django.db import models


# Create your models here.
class Board(models.Model):
    user = models.ForeignKey('api_user.User', on_delete=models.CASCADE, null=False, default='')
    title = models.CharField(max_length=50, null=False)
    contents = models.TextField(null=False)
    write_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'board'


class BoardFile(models.Model):
    num = models.ForeignKey('Board', on_delete=models.CASCADE, null=False, default='')
    file = models.FileField(null=False, upload_to='files/', blank=True)

    class Meta:
        db_table = 'board_file'
