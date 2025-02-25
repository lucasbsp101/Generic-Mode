from flask import Flask, render_template, request, redirect, url_for, session
from forms import PersonalDataForm
import sqlite3

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'  # Important for using sessions

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Model for the people table
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    resposta_pergunta_1 = db.Column(db.String(500), nullable=True)
    resposta_pergunta_2 = db.Column(db.String(500), nullable=True)

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = PersonalDataForm()
    if form.validate_on_submit():
        name = form.name.data
        phone_number = form.phone_number.data

        # Save data to the database
        person = Person(name=name, phone_number=phone_number)
        db.session.add(person)
        db.session.commit()

        # Store data in session
        session['person_id'] = person.id

        return redirect(url_for('test_1'))

    return render_template('personal_data.html', form=form)

@app.route('/test_1', methods=['GET', 'POST'])
def test_1():
    # Check if personal data was entered
    if 'person_id' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'resposta_pergunta_1' in request.form and 'resposta_pergunta_2' in request.form:
            resposta_pergunta_1 = request.form['resposta_pergunta_1']
            resposta_pergunta_2 = request.form['resposta_pergunta_2']

            # Update test responses in the database
            person = Person.query.get(session['person_id'])
            person.resposta_pergunta_1 = resposta_pergunta_1
            person.resposta_pergunta_2 = resposta_pergunta_2
            db.session.commit()

            #Anterior, voltar se erro
            #return redirect(url_for('resultado'))
            return redirect(url_for('resultado', resposta_pergunta_1=resposta_pergunta_1, resposta_pergunta_2=resposta_pergunta_2))
        else:
            return "Form data is missing", 400

    return render_template('test_1.html')

@app.route('/resultado')
def resultado():
    resposta_pergunta_1 = request.args.get('resposta_pergunta_1')
    resposta_subgrupos = request.args.get('resposta_pergunta_2')


    #return render_template('resultado.html', resposta_pergunta_1=resposta_pergunta_1, resposta_pergunta_2=resposta_pergunta_2)

    #Voltar, se erro
    return ("Course in development..."
            "Test 2 will be available soon..."
            "Comparison too")

if __name__ == '__main__':
    app.run(debug=True)