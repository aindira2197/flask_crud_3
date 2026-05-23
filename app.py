from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'

db = SQLAlchemy(app)


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)


@app.route('/')
def index():

    contacts = Contact.query.all()

    return render_template(
        'index.html',
        contacts=contacts
    )


@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':

        fullname = request.form.get('fullname')
        phone = request.form.get('phone')
        email = request.form.get('email')

        contact = Contact(
            fullname=fullname,
            phone=phone,
            email=email
        )

        db.session.add(contact)
        db.session.commit()

        return redirect('/')

    return render_template('create.html')


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
