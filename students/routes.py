from flask import render_template, flash, redirect, url_for, request
from .forms import LoginForm, AddStudentForm, UpdateAccountForm, UpdateStudentForm
from . import app, db 
from .models import User, Student 
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['GET'])
def home(): 
    students = Student.query.all()     
    return render_template('index.html', students=students)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and (user.password == form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin'))

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/admin')
@login_required
def admin():
    students = Student.query.all()
    return render_template('index.html', students=students, title='Admin Area')

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.password = form.password.data 
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('admin'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.password.data = current_user.password

    return render_template('update_account.html', form=form, title='Account')

@app.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            attended_class=form.attended_class.data
        )
        db.session.add(student)
        db.session.commit()
        flash(f'Student created for {form.name.data}', 'success')
        return redirect(url_for('admin'))
    return render_template('add_student.html', form=form, legend='Add Form', title='Add Student')


@app.route('/student/<int:student_id>')
@login_required
def student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student.html', student=student, title='Student')

@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
@login_required
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    form = UpdateStudentForm()
    if form.validate_on_submit():
        student.name = form.name.data
        student.email = form.email.data
        student.phone = form.phone.data
        student.attended_class = form.attended_class.data
        db.session.commit()
        flash(f'Student data ({student.name}) has been updated!', 'success')
        return redirect(url_for('admin'))

    elif request.method == 'GET':
        form.name.data = student.name
        form.email.data = student.email
        form.phone.data = student.phone
        form.attended_class.data = student.attended_class

    return render_template('add_student.html', form=form, legend='Update Form', title='Update Student')


@app.route('/student/<int:student_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Successfully deleted!', 'success')
    return redirect(url_for('admin'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
