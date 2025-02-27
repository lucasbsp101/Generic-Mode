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
    AQ1 = db.Column(db.String(500), nullable=True)
    AQ2 = db.Column(db.String(500), nullable=True)
    AQ3 = db.Column(db.String(500), nullable=True)
    AQ4 = db.Column(db.String(500), nullable=True)

# Page - Personal data
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

# Page - test_1
@app.route('/test_1', methods=['GET', 'POST'])
def test_1():
    # Check if personal data was entered
    if 'person_id' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'AQ1' in request.form and 'AQ2' in request.form:
            AQ1 = request.form['AQ1']
            AQ2 = request.form['AQ2']

            # Update test responses in the database
            person = Person.query.get(session['person_id'])
            person.AQ1 = AQ1
            person.AQ2 = AQ2
            db.session.commit()

            return redirect(url_for('course', AQ1=AQ1, AQ2=AQ2))
        else:
            return "Form data is missing", 400

    return render_template('test_1.html')

# Page -course
@app.route('/course')
def course():
    AQ1 = request.args.get('AQ1')
    AQ2 = request.args.get('AQ2')
    return render_template('course.html', AQ1=AQ1, AQ2=AQ2)

# Page - test_2
@app.route('/test_2', methods=['GET', 'POST'])
def test_2():
    # Check if personal data was entered
    if 'person_id' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'AQ3' in request.form and 'AQ4' in request.form:
            AQ1 = request.form['AQ1']
            AQ2 = request.form['AQ2']
            AQ3 = request.form['AQ3']
            AQ4 = request.form['AQ4']

            # Update test responses in the database
            person = Person.query.get(session['person_id'])
            person.AQ3 = AQ3
            person.AQ4 = AQ4
            db.session.commit()

            return redirect(url_for('comparison', AQ1=AQ1, AQ2=AQ2, AQ3=AQ3, AQ4=AQ4))
        else:
            return "Form data is missing", 400

    return render_template('test_2.html')



# Page - comparison (developing...)
@app.route('/comparison')
def comparison():
    AQ1 = request.args.get('AQ1')
    AQ2 = request.args.get('AQ2')
    AQ3 = request.args.get('AQ3')
    AQ4 = request.args.get('AQ4')
    return render_template('comparison.html', AQ1=AQ1, AQ2=AQ2, AQ3=AQ3, AQ4=AQ4)

if __name__ == '__main__':
    app.run(debug=True)