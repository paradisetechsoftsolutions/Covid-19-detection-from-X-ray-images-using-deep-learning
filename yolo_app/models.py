from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# user model is created which contains name of the user who have uploaded the file,
# uploaded file path with its name, result whether corona positive or negative and created at
class UserHistory(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
	uploaded_img_path = models.ImageField()
	result = models.CharField(blank=True, null=True, max_length=255)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)




