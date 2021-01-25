from flask import render_template, flash, request, redirect, url_for, send_from_directory, abort
from app import app, db, CreateLanguageForm, CreatePostForm, LoginForm, lm, UpdateAccount, UpdateAccount1, Coment, Response1
from app.models.tables import Languages, Posts, Users, Comments, Response
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
import secrets
import os


@lm.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/index")
def index():

    languagess = Languages.query.all()
    
    return render_template('index.html', languagess=languagess)




@app.route("/index/<key>", methods=["GET","POST"])
def language(key):
    
    languages = Languages.query.filter_by(key=key).first()
    comment = Coment()
    response2 = Response1()
    languagess = Languages.query.all()
    # comments= Comments.query.all()
    posts = Posts.query.filter_by(languageKey = languages.key).all()
    post= Posts.query.all()
    comments = Comments.query.all()
    response = Response.query.all()
    if languages == None:
        return "<h1> Não existe está linguagem cadastrada <h1>"
    return render_template('language.html', response2=response2, response=response, comments=comments, comment=comment, languages=languages, posts=posts,post=post, languagess=languagess)

@app.route("/index/posts/<key>/<int:post_id>/new", methods=["POST"])
def comment(key, post_id):
    comment = Coment()
    comments = Comments.query.all()
    if comment.validate_on_submit():
        for o in comments:
            if o.name == comment.name.data:
                flash('Já existe um comentário com este nome')
                return redirect(url_for('language',key=key))
    i = Comments(name=comment.name.data, content=comment.text.data, post_id=post_id)
    db.session.add(i)
    db.session.commit()
    flash('Comentário criado', 'success')
    return redirect(url_for('language',key=key))

@app.route("/index/posts/<key>/<int:post_id>/<int:comments_id>/new", methods=["POST"])
def response(key, post_id, comments_id):
    response2 = Response1()
    i = Response(name=response2.name.data, content=response2.text.data, comments_id=comments_id)
    db.session.add(i)
    db.session.commit()
    flash('comentário respondido', 'success')
    return redirect(url_for('language',key=key))

@app.route("/index/posts/<key>/<int:post_id>/<int:comments_id>/delete", methods=["POST"])
def responsedel(key, post_id, comments_id):
    post = Response.query.get_or_404(comments_id)
    db.session.delete(post)
    db.session.commit()
    flash('Comentário excluido', 'success')
    return redirect(url_for('language',key=key))

@app.route("/index/posts/<key>/<int:post_id>/delete", methods=["POST"])
def commentdel(key, post_id):
    comment = Coment()
    post = Comments.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Comentário excluido', 'success')
    return redirect(url_for('language',key=key))
    
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
        user = Users.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("adm"))
        else:
            flash("login invalido")
   
    return render_template('login.html', form=form, languagess=languagess)

@app.route("/adm/accounts", methods=['GET','POST'])
@login_required
def account():
    languagess = Languages.query.all()
    form = UpdateAccount1()
    print('entrou1')
    if form.validate_on_submit():
        print(form.errors)
        current_user.username=form.username.data
        current_user.password=form.password.data
        current_user.contato=form.contato.data
        db.session.commit()
        flash('Os dados de sua conta foram atualizados', 'success')
        return redirect(url_for("adm", form=form))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.password.data = current_user.password
        form.contato.data = current_user.contato
    return render_template("conta.html", form=form, languagess=languagess)



# rotas manager
@app.route("/adm/managermonitor", methods=['GET','POST'])
@login_required
def manager():
    languagess = Languages.query.all()
    flag = 'mestre'
    flagMaster='king'
    users = Users.query.all()
    if flagMaster == current_user.flag:
        return render_template("manager.html", users=users, flagMaster=flagMaster, languagess=languagess)
    elif flag == current_user.flag:
        return render_template("manager.html", users=users, flagMaster=flagMaster, languagess=languagess)
    else:
         flash('Você não tem permissão para acesso', 'success')
    return render_template("selecaoadm.html", languagess=languagess)

@app.route("/adm/managermonitor/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_monitor(post_id):
    flag = 'mestre'
    flagMaster='king'
    if flagMaster != current_user.flag:
        post = Users.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('O monitor escolhido foi deletado', 'success')
        return redirect(url_for('manager'))
    elif flag != current_user.flag:
        post = Users.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('O monitor escolhido foi deletado', 'success')
        return redirect(url_for('manager'))
    else:
        abort(403)

@app.route("/adm/managermonitor/newmonitor", methods=['GET','POST'])
@login_required
def new_monitor():
    languagess = Languages.query.all()
    flag = 'mestre'
    flagMaster='king'
    if flagMaster == current_user.flag:
            users = Users.query.all()
            form =UpdateAccount()
            if form.validate_on_submit():
                for o in users:
                    if o.username == form.username.data:
                        flash('Já existe um usuário com este nome tente um valor diferente')
                        return  render_template('create_monitor.html', title='Nova linguagem',
                                form=form, legend='Nova linguagem', )
                i = Users(username=form.username.data, password=form.password.data, contato=form.contato.data, flag=form.flag.data)
                db.session.add(i)
                db.session.commit()
                flash('Um novo monitor foi adicionada', 'success')
                return redirect(url_for('manager'))
    elif flag == current_user.flag:
            users = Users.query.all()
            form =UpdateAccount()
            if form.validate_on_submit():
                for o in users:
                    if o.username == form.username.data:
                        flash('Já existe um usuário com este nome tente um valor diferente')
                        return  render_template('create_monitor.html', title='Nova linguagem',
                                form=form, legend='Nova linguagem', )
                i = Users(username=form.username.data, password=form.password.data, contato=form.contato.data, flag=form.flag.data)
                db.session.add(i)
                db.session.commit()
                db.session.commit()
                flash('Um novo monitor foi adicionada', 'success')
                return redirect(url_for('manager'))
    else:
        abort(403)
    return render_template('create_monitor.html', form=form, legend='Novo monitor', languagess=languagess)
    

@app.route("/logout")
@login_required
def logout():
    languagess = Languages.query.all()
    logout_user()
    return redirect(url_for("index", languagess=languagess))

@app.route("/index/login/adm")
@login_required
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
            
        i = Languages(title=form.title.data, description=form.description.data, image=picture_file, key=form.key.data, author=current_user)
        db.session.add(i)
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
    flag = 'mestre'
    flagMaster='king'
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash('A linguagem escolhida foi deletada', 'success')
    elif flag or flagMaster != current_user.flag:
        db.session.delete(post)
        db.session.commit()
        flash('A linguagem escolhida foi deletada', 'success')
    else:
        abort(403)
    return redirect(url_for('lists', languages=languages))

@app.route("/adm/list/languages/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    languagess = Languages.query.all()
    post = Languages.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)
    form = CreateLanguageForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.description=form.description.data
        post.key=form.key.data
       
        db.session.commit()
        flash('A linguagem escolhida foi atualizada', 'success')
        return redirect(url_for('listlanguages', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        
        form.key.data=post.key
    
    return render_template('updatelanguage.html', title='Atualizar linguagem',
                           form=form, legend='Atualizar linguagem', languagess=languagess)



# rotas para criação de posts
@app.route("/adm/list/posts")
@login_required
def listposts():
    languagess = Languages.query.all()
    posts = Posts.query.all()
    return render_template('listposts.html', posts=posts, languagess=languagess)

@app.route("/adm/list/posts/<int:post_id>")
@login_required
def postView(post_id):
    languagess = Languages.query.all()
    post = Posts.query.get_or_404(post_id)
    return render_template('postpost.html', title=post.title, post=post, languagess=languagess)


@app.route("/adm/list/posts/post/new", methods=['GET','POST'])
@login_required
def postpost():
    languagess = Languages.query.all()
    form = CreatePostForm()
    form.languageKey.choices = [(l.key, l.title) for l in Languages.query.all()]
    if form.validate_on_submit():
        i = Posts(title=form.title.data, subtitle=form.subtitle.data, text=form.text.data, key=form.key.data, exercise=form.exercise.data, languageKey=form.languageKey.data, author=current_user)
        db.session.add(i)
        db.session.commit()
        flash('Seu conteudo foi criado', 'success')
        return redirect(url_for('listposts'))
    return render_template('create_post.html', title='Novo conteudo',
                           form=form, legend='Novo conteudo', languagess=languagess)



@app.route("/adm/list/posts/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_postpost(post_id):
    post = Posts.query.get_or_404(post_id)
    flag = 'mestre'
    flagMaster='king'
    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash('O conteudo escolhido foi deletado', 'success')
    elif flag or flagMaster != current_user.flag:
        db.session.delete(post)
        db.session.commit()
        flash('O conteudo escolhido foi deletado', 'success')
    else:
        abort(403)
    return redirect(url_for('listposts'))
                    
@app.route("/adm/list/posts/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_postpost(post_id):
    languagess = Languages.query.all()
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = CreatePostForm()
    form.languageKey.choices = [(l.key, l.title) for l in Languages.query.all()]
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