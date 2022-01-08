from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#import yaml
from settings import URI_DB
from flask_restplus import Api
#from models import User
app = Flask(__name__)
#db_config = yaml.load(open('database.yaml'))
app.config['SQLALCHEMY_DATABASE_URI'] = URI_DB
db = SQLAlchemy(app)
#CORS(app)
from datetime import datetime
#from models import User
from flask_login import LoginManager, current_user, login_user
import json
from flask_migrate import Migrate


migrate = Migrate(app, db)
db.init_app(app)
migrate.init_app(app, db)


app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'

login_manager = LoginManager()
login_manager.init_app(app)

app = Api(app)

name_space = app.namespace('main', description='Main APIs')


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.filter_by(id=user_id).first()


@app.route('/login', methods=['POST'])
def login():
    from models import User
    from werkzeug.security import check_password_hash
    info = json.loads(request.data)
    username = info.get('email', 'guest')
    password = info.get('password', '')
    user = User.query.filter_by(email=username).first()

    if user and check_password_hash(user.password,password):
        login_user(user)
        return jsonify({"status": 200,"email":user.email,
                        "message": "Sesion Exitosa"})
    else:
        return jsonify({"status": 401,
                        "error": "Username or Password Error"})


@app.route('/user', methods=['POST', 'GET', 'PUT', 'DELETE'])
def users():

    # Registro de Usuario
    if request.method == 'POST':
        from models import User
        body = request.json

        name = body['name']
        password = body['password']
        email = body['email']
        status = body['status'] if 'status' in body else True
        picture = "--"
        try:
            data = User(name=name,password=password,email=email,picture=picture,status=status)
            db.session.add(data)
            db.session.commit()

            return jsonify({
                'status': 'Usuario registrad en PostgreSQL!',
                'email': email
            })
        except Exception as e:
            return jsonify({
                'status': 'Intente más tarde!',
                'error': str(e)
            })

    # Edicion de Usuario
    if request.method == 'PUT':
        try:
            from models import User
            body = request.json
            email = body['email']
            user_edit = User.query.filter_by(email=email).first()
            user_edit.name = body['name']
            user_edit.status = True
            db.session.merge(user_edit)
            db.session.commit()
            return jsonify({
                'status': 'Usuario Editado en PostgreSQL!',
                'email': email
            })
        except Exception as e:
            return jsonify({
                'status': 'Intente más tarde!',
                'error': str(e)
            })

    #Borrado (desactivado) del usuario
    if request.method == 'DELETE':
        try:
            from models import User
            body = request.json
            email = body['email']
            user_edit = User.query.filter_by(email=email).first()
            user_edit.status = False
            db.session.merge(user_edit)
            db.session.commit()
            return jsonify({
                'status': 'Usuario Eliminado en PostgreSQL!',
                'email': email
            })
        except Exception as e:
            return jsonify({
                'status': 'Intente más tarde!',
                'error': str(e)
            })

    # Obtener los usuarios del sistema
    if request.method == 'GET':
        from models import User
        data = User.query.all()
        dataJson = []
        for value in data:
            dataDict = {
                'id': value.id,
                'name': value.name,
                'email': value.email
            }
            dataJson.append(dataDict)
        return jsonify(dataJson)

@app.route('/publicacion', methods=['GET', 'POST' ,'DELETE', 'PUT'])
def publicacion_crud():

    # Obtiene una publicacion
    if request.method == 'GET':
        from models import Publication
        data_ = Publication.query.filter_by(status=True)
        dataJson = []
        for value in data_:
            dataDict = {
                'id': value.id,
                'title': value.title,
                'description':value.description,
                'creacion':value.created
            }
            dataJson.append(dataDict)
        return jsonify(dataJson)

    # Registra una publicacion
    if request.method == 'POST':
        from models import Publication
        body = request.json

        title = body['title'] if 'title' in body else ""
        description = body['description'] if 'description' in body else ""
        prioridad = body['prioridad'] if 'prioridad' in body else "Alta"
        status = body['status'] if 'status' in body else True
        created = datetime.now()
        user_id = body['user_id']

        try:
            data_pub = Publication(title,description,prioridad,status,created,user_id)
            db.session.add(data_pub)
            db.session.commit()

            return jsonify({
                'status': 'Publicacion registrada en PostgreSQL!',
                'title': title
            })
        except Exception as e:
            return jsonify({
                'status': 'Intente más tarde!',
                'error': str(e)
            })

    # DELETE la publicacion
    if request.method == 'DELETE':
        from models import Publication
        try:
            body = request.json
            id_post = body['id_post']
            post_del = Publication.query.filter_by(id=id_post).first()
            post_del.status = False
            db.session.merge(post_del)
            db.session.commit()
            return jsonify({
                'status': 'Publicación Eliminada en PostgreSQL!',
                'id_post': id_post
            })
        except Exception as e:
            return jsonify({
                'status': 'Intente más tarde!',
                'error': str(e)
            })

    # Actualizacion de Publicacion
    if request.method == 'PUT':
        from models import Publication
        try:
            body = request.json
            id_post = body['id_post']
            title = body['title'] if 'title' in body else None
            description = body['description'] if 'description' in body else None
            prioridad = body['prioridad'] if 'prioridad' in body else None
            status = body['status'] if 'status' in body else True
            post_edit = Publication.query.filter_by(id=id_post).first()
            if title:post_edit.title = title
            if description:post_edit.description = description
            if prioridad:post_edit.prioridad = prioridad
            if status :post_edit.status = status
            db.session.merge(post_edit)
            db.session.commit()
            return jsonify({
                'status': 'Publicación Editada en PostgreSQL!',
                'title': title
            })
        except Exception as e:
            return jsonify({
                'status': 'Intente más tarde!',
                'error': str(e)
            })




if __name__ == '__main__':
    app.debug = True

    app.run()
