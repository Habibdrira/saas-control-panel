from flask import render_template, flash, redirect, url_for, current_app
from flask_login import current_user, login_user, logout_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from app.services.provision_service import provision_user_container


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('main.dashboard'))

    return render_template('auth/login.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        # 🔥 PROVISION AUTOMATIQUE
        provision = provision_user_container(user.username)

        user.container_name = provision["container_name"]
        user.container_port = provision["port"]
        db.session.commit()

        current_app.logger.info(
            f"Container {user.container_name} created on port {user.container_port}"
        )

        flash('Account created successfully!')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)
