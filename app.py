from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db = SQLAlchemy(app)


# Modelo para a tabela de pessoas
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preferencia = db.Column(db.String(50), nullable=False)  # Nova coluna


# Recria o banco de dados (execute apenas uma vez)
with app.app_context():
    db.drop_all()  # Exclui todas as tabelas existentes
    db.create_all()  # Cria as tabelas com a nova estrutura


# Rota para a página inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Coleta o nome e a preferência do formulário
        nome = request.form['nome']
        preferencia = request.form['preferencia']

        # Cria um novo registro no banco de dados
        nova_pessoa = Pessoa(nome=nome, preferencia=preferencia)
        db.session.add(nova_pessoa)
        db.session.commit()

        # Redireciona para a página inicial
        return redirect(url_for('index'))

    # Recupera todas as pessoas do banco de dados
    pessoas = Pessoa.query.all()
    return render_template('index.html', pessoas=pessoas)


if __name__ == '__main__':
    app.run(debug=True)

