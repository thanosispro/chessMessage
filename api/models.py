from django.db import models



# Create your models here.
class Message(models.Model):
    message = models.TextField()
    username = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + self.message[:20]
    