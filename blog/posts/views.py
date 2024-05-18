import json
from django.http import JsonResponse
from .models import Comentario, Usuario, Publicar
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.serializers import serialize


@csrf_exempt
def crear_usuario(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            nombre = data.get('nombre')
            apellidop = data.get('apellidop')
            apellidom = data.get('apellidom')
            telefono = data.get('telefono')
            email = data.get('email')
            password = data.get('password')
            password2 = data.get('password2')
            username= data.get('username')

            if password == password2:
                contraseña_encriptada = make_password(password)
                nuevo_usuario = Usuario(
                    nombre=nombre,
                    apellidop=apellidop,
                    apellidom=apellidom,
                    telefono=telefono,
                    email=email,
                    password=contraseña_encriptada,
                    username= username,
                )
                nuevo_usuario.save()
                return JsonResponse({'mensaje': 'Usuario creado con éxito'})
            else:
                return JsonResponse({'mensaje': 'Las contraseñas no coinciden'}, status=400)
        except IntegrityError:
            return JsonResponse({'mensaje': 'El usuario ya existe'}, status=409)
        except Exception as e:
            return JsonResponse({'mensaje': f'Error al crear usuario: {str(e)}'}, status=500)
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)


# @csrf_exempt
# def cerrar_sesion( request):
#     logout(request)
#     return JsonResponse({'mensaje': 'cerraste sesion'}, status=405)

@csrf_exempt
def crear_publicar(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        titulo = data.get('titulo')
        contenido = data.get('contenido') 
        imagen  = request.FILES.get('imagen')
        fecha_publi = data.get('fecha_publi')
        autor_id = data.get('autor') 
        
        
        
        try:
            autor = Usuario.objects.get(pk=autor_id)
        except Usuario.DoesNotExist:
            return JsonResponse({'mensaje': 'El autor especificado no existe'}, status=400)
        
        nuevo_post = Publicar(
            titulo = titulo,
            contenido = contenido,
            imagen = imagen,
            fecha_publi = fecha_publi,
            autor = autor,
           
        )
        
        
        nuevo_post.save()

        return JsonResponse({'mensaje': 'Post creado correctamente'})

    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        # Verifica si el cuerpo de la solicitud contiene datos JSON
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON no válido'}, status=400)

        # Verifica si las claves 'email' y 'password' están presentes en los datos JSON
        if 'email' in data and 'password' in data:
            email = data['email']
            password = data['password']

            try:
                user = Usuario.objects.get(email=email)
            except Usuario.DoesNotExist:
                return JsonResponse({'error': 'Usuario no encontrado'}, status=401)

            if check_password(password, user.password):
                # Generar el token de acceso JWT
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'userid' : user.id
                })
            else:
                return JsonResponse({'error': 'Usuario o contraseña incorrecta'}, status=401)
        else:
            return JsonResponse({'error': 'Datos de inicio de sesión incompletos'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
def Blogs(request):
    blogs = Publicar.objects.all()
    # Serializar los productos a JSON
    blogs_json = serialize('json', blogs)
    # Devolver la respuesta como JSON
    return JsonResponse({'blogs': blogs_json}, safe=False)

@csrf_exempt
def Comentarios(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            contenido = data.get('contenido')
            fecha_comentario = data.get('fecha_comentario')
            autor_id = data.get('autor')
            publicacion_id = data.get('publicacion')

            # Obtener el autor y la publicación por sus IDs
            autor = Usuario.objects.get(id=autor_id)
            publicacion = Publicar.objects.get(id=publicacion_id)

            # Crear el comentario con la fecha actual
            nuevo_comentario = Comentario(
                contenido=contenido,
                fecha_comentario= fecha_comentario,
                autor=autor,
                publicacion=publicacion,
             
            )

            nuevo_comentario.save()
            return JsonResponse({'mensaje': 'Comentario creado con éxito'})
        except Usuario.DoesNotExist:
            return JsonResponse({'mensaje': 'Usuario no encontrado'}, status=404)
        except Publicar.DoesNotExist:
            return JsonResponse({'mensaje': 'Publicación no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'mensaje': f'Error al hacer el comentario: {str(e)}'}, status=500)
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

def Mostrar_comentarios(request):
    comentarios = Comentario.objects.all()
    # Serializar los productos a JSON
    comentarios_json = serialize('json', comentarios)
    # Devolver la respuesta como JSON
    return JsonResponse({'comentarios': comentarios_json}, safe=False)




