from django.db import models

# Create your models here.
class Client(models.Model):
    contract_number = models.CharField(max_length=9, unique=True)
    contact_phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.contract_number}"


class Intent(models.Model):
    name = models.CharField(max_length=50)
    keywords = models.TextField()
    response_text = models.TextField()
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.name}"