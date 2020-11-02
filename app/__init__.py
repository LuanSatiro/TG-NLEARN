from flask import Flask
from flask_wtf.file import FileField, FileAllowed
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from flask_wtf  import  FlaskForm 
from  wtforms  import  StringField, PasswordField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, AnyOf, DataRequired
from flask_login import LoginManager

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(message='deu ruim')])
    password = PasswordField("password", validators=[DataRequired(message='deu ruim')])
    submit= SubmitField('Realizar login')

class CreateLanguageForm(FlaskForm):
    title = StringField('Titulo', validators=[InputRequired(message='Um titulo é exigido'), Length(min=1, max=20, message= 'Máximo de 20 caracteres.')])
    description = TextAreaField('Descrição', validators=[InputRequired('Um subtitulo é exigido')])
    picture = FileField('Upload da imagem', validators=[FileAllowed(['jpg', 'png'])])
    image= StringField('Imagem', validators=[InputRequired('A key is required'), Length(min=1, max=40, message= 'Máximo de 40 caracteres.')])
    key = StringField('key (Este é um valor único, não é possivel ter uma key repetida)', validators=[InputRequired('Uma key é exigida'), Length(min=1, max=20, message= 'Máximo de 20 caracteres.')])
    submit= SubmitField('Finalizar')

class CreatePostForm(FlaskForm):
    title = StringField('Titulo', validators=[InputRequired(message='Um titulo é exigido'), Length(min=1, max=20, message= 'Máximo de 20 caracteres.')])
    subtitle = StringField('Subtitulo', validators=[InputRequired('Um subtitulo é exigido')])
    text= TextAreaField('Texto', validators=[InputRequired('Um texto é exigido')])
    exercise = TextAreaField('Exercicio', validators=[InputRequired('A exercise is required')])
    key = StringField('key (Será atribuido ao guia de tópicos da linguagem)', validators=[InputRequired('Uma key é exigida'), Length(min=1, max=20, message= 'Máximo de 20 caracteres')])
    languageKey = StringField('Key da linguagem (Para criação desse campo é importante se atentar a KEY da linguagem no qual ele é atribuido, caso a KEY utilizada não estiver atribuido a nenhuma linguagem, não sera possivel criar um novo conteudo)', validators=[InputRequired('Um ID de linguagem é exigido')])
    submit= SubmitField('Finalizar')

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

lm = LoginManager(app)
lm.init_app(app)



from .models import tables
# from app import admin
# admin.init_app(app)
from app.controllers import index
