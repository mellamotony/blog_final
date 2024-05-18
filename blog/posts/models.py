from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(models.Model):
    nombre = models.CharField(max_length=150)
    apellidop = models.CharField(max_length=150)
    apellidom = models.CharField(max_length=150)
    telefono = models.CharField(max_length=10)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    username = models.CharField(max_length=100, unique=True)

class Publicar(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='imagenes/')
    fecha_publi = models.DateTimeField(auto_now_add= True)
    autor = models.ForeignKey(Usuario, on_delete = models.CASCADE )
    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    contenido = models.TextField()
    fecha_comentario = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicar, on_delete=models.CASCADE, related_name='comentarios')

    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.publicacion.titulo}"