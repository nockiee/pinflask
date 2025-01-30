from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Post
from app.forms import RegistrationForm, LoginForm, PostForm
from app.forms import UpdateProfileForm
import os

main = Blueprint('main', __name__)

def save_image(image_file):
    if image_file:
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(
            current_app.config['UPLOADED_PHOTOS_DEST'],
            filename
        )
        image_file.save(filepath)
        return filename
    return None

@main.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=9)
    return render_template('home.html', posts=posts)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Проверка существующего email
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Этот email уже зарегистрирован', 'danger')
            return redirect(url_for('main.register'))
        
        # Создание пользователя
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data  # Убедитесь, что пароль хешируется
        )
        
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)  # <-- Используйте form.remember.data
            return redirect(url_for('main.home'))
        flash('Неверный email или пароль', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = UpdateProfileForm()
    
    if form.validate_on_submit():
        if form.avatar.data:
            filename = secure_filename(form.avatar.data.filename)
            filepath = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
            form.avatar.data.save(filepath)
            user.image_file = filename
        
        user.username = form.username.data
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('main.profile', username=user.username))
    
    elif request.method == 'GET':
        form.username.data = user.username
    
    posts = Post.query.filter_by(author=user).all()
    return render_template('profile.html', user=user, posts=posts, form=form)

@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Сохранение изображения
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
            form.image.data.save(filepath)
        else:
            filename = 'default.jpg'
        
        # Создание поста
        post = Post(
            title=form.title.data,
            content=form.content.data,
            image_file=filename,
            author=current_user  # Используйте связь через backref
        )
        db.session.add(post)
        db.session.commit()
        flash('Пост успешно создан!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', form=form)

@main.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@main.route('/change-password')
@login_required
def change_password():
    # Логика смены пароля
    return render_template('change_password.html')