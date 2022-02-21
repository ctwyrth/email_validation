from email_valid_app import app
from flask import render_template, redirect, request, session
from email_valid_app.models.email_valid import Email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    if not Email.validate_email(request.form):
        return redirect('/')
    else:
        data = {
            'email': request.form['email']
        }
    id = Email.save(data)
    return redirect(f'/show/{ id }')

@app.route('/show/<int:id>')
def show_all(id):
    return render_template('/results.html', emails = Email.show_all(), new = Email.show(id))

@app.route('/delete/<int:id>') 
def delete(id):
    data = {
        'id': id,
    }
    Email.delete(data)
    return redirect('/show')
