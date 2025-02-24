from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Importante para segurança entre as trocas de páginas

# CÓDIGO ANTERIOR #
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db = SQLAlchemy(app)
# Inicializa o Flask-Migrate
migrate = Migrate(app, db)

# Modelo para a tabela de pessoas
class Person(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        phone_number = db.Column(db.String(50), nullable=False, default='default_value')

# Rota para a página inicial
@app.route('/', methods=['GET', 'POST'])
def index():
        if request.method == 'POST':
            # Coleta o nome e o número de telefone do formulário
            name = request.form['Name']
            phone_number = request.form['Phone Number']

            # Cria um novo registro no banco de dados
            new_person = Person(name=name, phone_number=phone_number)
            db.session.add(new_person)
            db.session.commit()

            # Redireciona para a página inicial
            return redirect(url_for('index'))

        # Renderiza a página inicial sem passar os registros
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

# CÓDIGO ATUALIZADO #


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']

        # Armazena os dados na sessão
        session['nome'] = nome
        session['telefone'] = telefone

        # Ou armazena no banco de dados
        # conn = sqlite3.connect('seu_banco.db')
        # cursor = conn.cursor()
        # cursor.execute('INSERT INTO alunos (nome, telefone) VALUES (?, ?)', (nome, telefone))
        # conn.commit()
        # conn.close()

        return redirect(url_for('teste'))

    return render_template('index.html')

@app.route('/teste', methods=['GET', 'POST'])
def teste():
    # Verifica se os dados pessoais foram inseridos
    if 'nome' not in session:
        return redirect(url_for('index'))

    # ... (seu código existente para o teste) ...