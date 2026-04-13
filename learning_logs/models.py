from django.db import models
from django.contrib.auth.models import User
class Topic(models.Model):
    """Um assunto sobre qual o usuário está aprendendo"""
    text = models.CharField(max_length=200)
    date_Added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        """Devolve uma documentação em string do modelo"""
        return self.text 
class Entry(models.Model):
    """Algo Especifico aprendido sobre um Assunto"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    date_Added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Devolve uma documentação em string do modelo"""
        return self.text[:50] + '...'
    
