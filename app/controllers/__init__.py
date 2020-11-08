from flask import render_template, flash, request, redirect, url_for, send_from_directory
from app import app, db, CreateLanguageForm, CreatePostForm, LoginForm, lm
from app.models.tables import Languages, Posts, UserAdm
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
import secrets
import os


@lm.user_loader
def load_user(id):
    return UserAdm.query.filter_by(id=id).first()


@app.route("/index")
def index():

    languagess = Languages.query.all()
    
    return render_template('index.html', languagess=languagess)

@app.route("/index/<key>")
def language(key):
    
    languages = Languages.query.filter_by(key=key).first()
    
    if languages == None:
        return "<h1> Não existe está linguagem cadastrada <h1>"
    languagess = Languages.query.all()
    
    posts = Posts.query.filter_by(languageKey = languages.key).all()
    post= Posts.query.all()
    
    return render_template('language.html',languages=languages, posts=posts,post=post, languagess=languagess)

@app.route("/aboutus")
def aboutus():
    languagess = Languages.query.all()
    return render_template('aboutus.html', languagess=languagess)




# rotas de login
@app.route("/index/login", methods=["GET","POST"])
def login():
    languagess = Languages.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('adm'))
    form = LoginForm()
  
    if form.validate_on_submit():
      
        
        user = UserAdm.query.filter_by(username=form.username.data).first()
        
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("adm"))
        else:
            flash("login invalido")
   
    return render_template('login.html', form=form, languagess=languagess)

@app.route("/logout")
def logout():
    languagess = Languages.query.all()
    logout_user()
    return redirect(url_for("index", languagess=languagess))

@app.route("/index/login/adm")
def adm():
    languagess = Languages.query.all()
    return render_template('selecaoadm.html', languagess=languagess)



# rotas para criação de languages
@app.route("/adm/list/languages/")
@login_required
def lists():
    languagess = Languages.query.all()
    post = Languages.query.all()
    return render_template('listlanguages.html', post=post, languagess=languagess)


@app.route("/adm/list/languages/<int:post_id>")
@login_required
def listlanguages(post_id):
    languagess = Languages.query.all()
    post = Languages.query.get_or_404(post_id)
    print(post.id)
    return render_template('post.html', title=post.title, post=post, languagess=languagess)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/storage', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
   
@app.route("/adm/list/languages/post/new", methods=['GET','POST'])
@login_required
def post():
    languagess = Languages.query.all()
    form = CreateLanguageForm()
    if form.validate_on_submit():
        for o in languagess:
            if o.key == form.key.data:
                flash('Já existe uma linguagem com esta Key tente um valor diferente')
                return  render_template('create_language.html', title='Nova linguagem',
                           form=form, legend='Nova linguagem', languagess=languagess)
        picture_file = ''
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            
        i = Languages(title=form.title.data, description=form.description.data, image=picture_file, key=form.key.data)
        db.session.add(i)
        db.session.commit()
        db.session.commit()
        flash('Uma nova linguagem foi adicionada', 'success')
        return redirect(url_for('lists'))
    return render_template('create_language.html', title='Nova linguagem',
                           form=form, legend='Nova linguagem', languagess=languagess)
    


@app.route("/adm/list/languages/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    languages = Languages.query.all()
    post = Languages.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('A linguagem escolhida foi deletada', 'success')
    return redirect(url_for('lists', languages=languages))

@app.route("/adm/list/languages/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    languagess = Languages.query.all()
    post = Languages.query.get_or_404(post_id)
    form = CreateLanguageForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.description=form.description.data
        post.image=form.image.data
        post.key=form.key.data
        
        db.session.commit()
        flash('A linguagem escolhida foi atualizada', 'success')
        return redirect(url_for('listlanguages', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.image.data = post.image
        form.key.data = post.key
    return render_template('create_language.html', title='Atualizar linguagem',
                           form=form, legend='Atualizar linguagem', languagess=languagess)



# rotas para criação de posts


@app.route("/adm/list/posts")
@login_required
def listposts():
    languagess = Languages.query.all()
    posts = Posts.query.all()
    return render_template('listposts.html', posts=posts, languagess=languagess)

@app.route("/adm/list/posts/<int:post_id>")
def postView(post_id):
    languagess = Languages.query.all()
    post = Posts.query.get_or_404(post_id)
    return render_template('postpost.html', title=post.title, post=post, languagess=languagess)


@app.route("/adm/list/posts/post/new", methods=['GET','POST'])
def postpost():
    languagess = Languages.query.all()
    form = CreatePostForm()
    form.languageKey.choices = [(l.key, l.title) for l in Languages.query.all()]
    if form.validate_on_submit():
        i = Posts(title=form.title.data, subtitle=form.subtitle.data, text=form.text.data, key=form.key.data, exercise=form.exercise.data, languageKey=form.languageKey.data)
        db.session.add(i)
        db.session.commit()
        flash('Seu conteudo foi criado', 'success')
        return redirect(url_for('listposts'))
    return render_template('create_post.html', title='Novo conteudo',
                           form=form, legend='Novo conteudo', languagess=languagess)



@app.route("/adm/list/posts/<int:post_id>/delete", methods=['POST'])
def delete_postpost(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Seu conteudo escolhido foi deletado', 'success')
    return redirect(url_for('listposts'))
                    
@app.route("/adm/list/posts/<int:post_id>/update", methods=['GET', 'POST'])
def update_postpost(post_id):
    languagess = Languages.query.all()
    post = Posts.query.get_or_404(post_id)
    form = CreatePostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.subtitle=form.subtitle.data
        post.text=form.text.data
        post.exercise=form.exercise.data
        post.key=form.key.data
        post.languageKey=form.languageKey.data
        db.session.commit()
        flash('Seu conteudo escolhido foi atualizado', 'success')
        return redirect(url_for('postView', post_id=post.id, languagess=languagess))
    elif request.method == 'GET':
        form.title.data=post.title
        form.subtitle.data=post.subtitle
        form.text.data=post.text
        form.exercise.data=post.exercise
        form.key.data=post.key
        form.languageKey.data=post.languageKey
    return render_template('create_post.html', title='Atualizar conteudo',
                           form=form, legend='Atualizar conteudo')