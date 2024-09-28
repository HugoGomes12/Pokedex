from flask import render_template, redirect,url_for,flash,request, abort
from comunidade_impressionadora import app, database, bcrypt
from comunidade_impressionadora.form import FormLogin,FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidade_impressionadora.models import Usuario, Post
from flask_login import login_user,logout_user, current_user, login_required
import secrets
import os
from PIL import Image

@app.route("/")
def Home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template("home.html", posts=posts)

@app.route("/contatos")
def contatos():
    return render_template("contatos.html")

@app.route('/lista_Usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET','POST'])
def login(): 
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form: 
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha , form_login.senha.data):
            login_user(usuario, remember=form_login.botao_lembrar_dados.data)
            flash(f'login feito com sucesso ! no email : {form_login.email.data} ','alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect('par_next')
            else:
                return redirect(url_for('Home'))
        else:
            flash(f'falha no login email ou senhas incorretos !', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_CriarConta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data,email=form_criarconta.email.data,senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso ! para o email : {form_criarconta.email.data}','alert-success')
        return redirect(url_for('Home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso !','alert-success')
    return redirect(url_for('Home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET','POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criando com sucesso !', 'alert-success')
        return redirect(url_for('Home'))
    return render_template('criar-post.html', form=form)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)    
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)   
    return nome_arquivo
    
def atualizar_cursos(form):
    lista_cursos = []
    for campo in form :
        if 'curso_' in campo.name:
            if campo.data:
            #Adicionaro o campo do curso_exel.label na lista de cursos
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)
    
    
@app.route('/perfil/editar', methods=['GET','POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)          
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('perfil atulizado com sucesso !', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)



@app.route('/post/<post_id>', methods=['GET','POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso !', 'alert-success')
            return redirect(url_for('Home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form) 
    

@app.route('/post/<post_id>/excluir', methods=['GET','POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluido com sucesso !', 'alert-success')
        return redirect(url_for('Home'))
    else:
        abort(404)