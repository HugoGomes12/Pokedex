from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import  StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from comunidade_impressionadora.models import Usuario 
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('nome do usuario', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(),Email()])
    senha = PasswordField('senha', validators=[DataRequired(), length(6, 15)])
    confirmacao = PasswordField('confirmação da senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_CriarConta = SubmitField('Criar Conta')
    
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado !, por favor cadastre-se com outro email ou faça login')
    
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('senha', validators=[DataRequired(), length(6, 15)])
    botao_lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')
    
    
class FormEditarPerfil(FlaskForm):
     username = StringField('nome do usuario', validators=[DataRequired()])
     email = StringField('E-mail', validators=[DataRequired(), Email()])
     foto_perfil = FileField('Atualizar a foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
     
     curso_excel = BooleanField('Curso Excel')
     curso_CSharp = BooleanField('Curso C#')
     curso_python = BooleanField('Curso Python')
     curso_JavaScript = BooleanField('Curso JavaScript')
     curso_HTML_CSS = BooleanField('Curso HTML E CSS')
     curso_SQL = BooleanField('Curso SQL')
     botao_submit_perfil = SubmitField('Confirmar alteração') 

     def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuario com esse e-mail, por favor cadastre-se com outro e-mail' )
    
class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do post',validators=[DataRequired(), length(5,150)])
    corpo = TextAreaField('Escreva seu post', validators=[DataRequired()])
    botao_submit = SubmitField('Criar post') 