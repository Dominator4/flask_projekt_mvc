from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, Offers
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from app.forms import EditProfileForm
from app.forms import Resetpasswordform
from datetime import datetime
from app.forms import Addoffersform

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Strona główna')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by( email = form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Podałeś nieprawidłowe dane!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Logowanie', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User( firstname = form.firstname.data, lastname = form.lastname.data , email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        if user.id ==1 :
            user.status ='Admin'
        else:
            user.status='User'
        db.session.add(user)
        db.session.commit()
        flash('Gratulujemy rejestracji!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Rejestracja', form=form)

@app.route('/user/<int:id>')
@login_required
def user( id):
    user = User.query.get(id)
    return render_template('user.html', user=user)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile/<int:id>',  methods=['GET', 'POST'])
@login_required
def edit_profile( id ):
    form = EditProfileForm()
    user = User.query.get(id)
    if form.validate_on_submit():
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.about_me = form.about_me.data
        user.contact = form.contact.data
        db.session.add(user)
        db.session.commit()
        flash('Twoje zmiany zostały zapisane.')
        return redirect(url_for('edit_profile', id=user.id ))
    elif request.method == 'GET':
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.about_me.data = user.about_me
        form.contact.data = user.contact
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)



@app.route('/add_offers', methods=['GET', 'POST'])
@login_required
def add_offers():
    form = Addoffersform()
    if form.validate_on_submit():
        offers = Offers( about_this = form.about_this.data , name = form.name.data, user_id =current_user.id )
        db.session.add(offers)
        db.session.commit()
        flash('Twoja zmiana zostala zapisana')
        return redirect(url_for('add_offers'))
    return render_template('add_offers.html', title='Wystaw oferte',
                           form=form)


@app.route('/lists_offers')
@login_required
def lists_offers():
    offers = Offers.query.all()
    return render_template('lists_offers.html', title='Lista ofert:', offers= offers)

@app.route('/your_lists_offers/<email>')
@login_required
def your_lists_offers(email):
    user = User.query.filter_by( email = email ).first()
    offers = Offers.query.all()
    return render_template('your_lists_offers.html', title='Twoje oferty:', offers= offers, user=user)

@app.route('/lists_users')
@login_required
def lists_users():
    users = User.query.all()
    return render_template('lists_users.html', title='Lista kont:', users = users)

@app.route('/detailsoffers/<int:id>')
@login_required
def details_offers(id):
    offers = Offers.query.get(id)
    user = User.query.get(offers.user_id)
    return render_template('details_offers.html', title='Oferta:', offers= offers, user=user)



@app.route('/del_offers/<int:id>')
def del_offers(id):
    offers = Offers.query.get(id)
    if offers is None:
        abort(404)
    db.session.delete(offers)
    db.session.commit()
    return redirect(url_for('lists_offers'))

@app.route('/del_user/<int:id>')
def del_user(id):
    user = User.query.get(id)
    offers = Offers.query.all()
    for offer in offers:
        if user.id ==offer.user_id:
            db.session.delete(offer)
            db.session.commit()
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('lists_users'))

@app.route('/reset_password/<int:id>', methods=['GET', 'POST'])
def reset_password(id):
    form = Resetpasswordform()
    user = User.query.get(id)
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Twoja zmiana została zatwierdzona')
        return redirect(url_for('user', id =id))
    return render_template('reset_password.html', title='Resetowanie hasła', form=form)

