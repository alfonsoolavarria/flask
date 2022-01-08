NOTA: antes de lanzar las migraciones se debe descomentar la linea #13 del app.py que me esta dando
un errro de redundancia circular y no lo he logrado resolver

Pero se comenta la linea #13 se lanzan los siguientes comandos:

1 ) flask db init
2 ) flask db migrate
3 ) flask db upgrade

Luego se comenta de nuevo la linea #13 del app.py y se ejecuta el programa con:

1) python app.py


INFORMACION DEL CRUD PARA SU USO

###############USER###############

POST: http://127.0.0.1:5000/user

{
    "name":"Alfonso",
    "password":"1q2w3e4r",
    "email":"alfonsojn152@gmail.com"    
}

PUT: http://127.0.0.1:5000/user

{
    "name":"AlfonsoEditados",
    "email":"alfonsojn152@gmail.com"    
}

DELETE: http://127.0.0.1:5000/user

{
    "email":"alfonsojn152@gmail.com"    
}

GET: http://127.0.0.1:5000/user

no tiene parámetros a enviar


###############PUBLICATION###############
GET:http://127.0.0.1:5000/publicacion
no tiene parámetros a enviar, devuelve todas las publicaciones


POST:http://127.0.0.1:5000/publicacion
{
    "title":"Publicacion dos",
    "description":"Prieba de descripcion",
    "prioridad":"ALta",
    "user_id":1
}



NOTA:
El swagger me dio guerra con un error

Traceback (most recent call last):
  File "app.py", line 6, in <module>
    from flask_restplus import Api
  File "/Users/aolavarria/Proyects/flaskTest/lib/python3.8/site-packages/flask_restplus/__init__.py", line 4, in <module>
    from . import fields, reqparse, apidoc, inputs, cors
  File "/Users/aolavarria/Proyects/flaskTest/lib/python3.8/site-packages/flask_restplus/fields.py", line 17, in <module>
    from werkzeug import cached_property
ImportError: cannot import name 'cached_property' from 'werkzeug' (/Users/aolavarria/Proyects/flaskTest/lib/python3.8/site-packages/werkzeug/__init__.py)
