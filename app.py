from flask import Flask,render_template,request,session,redirect,url_for,flash
import psycopg2

conexao = psycopg2.connect(database = "trabalho",
                           host = "localhost",
                           user = "postgres",
                           password = "12345",
                           port = "5432")

#print(conexao.info)
app = Flask(__name__)
app.secret_key = 'tanto_faz'

@app.route('/')
def home_page():

    if 'loggedin' in session:
        return render_template('home_page.html')
    return redirect(url_for('login'))

@app.route('/cadastra_usuario', methods=['POST', 'GET'])
def cadastra_usuario():
    message = None
    nome_usuario = request.form.get('nome_usuario')
    senha_usuario = request.form.get('senha_usuario')

    if request.method == 'POST' and len(nome_usuario) > 0 and len(senha_usuario) > 0:
        try:
            
            cur = conexao.cursor()

            sql = 'SELECT * FROM usuario WHERE nome_usuario = %s'
            cur.execute(sql, (nome_usuario,))

            account = cur.fetchone()
            print(account)

            if account:
                message = 'Essa conta já existe'
            else:
                sql = "INSERT INTO usuario (nome_usuario, senha_usuario) VALUES (%s, %s)"
                cur.execute(sql, (nome_usuario, senha_usuario))
                print("Voce foi registrado")
                conexao.commit()
                
                return redirect(url_for('login'))
        
        except Exception as e:
            return f"Ocorreu um erro ao cadastrar o usuario: {str(e)}"
        
    print(f'Mensagem a ser exibida: {message}')
    return render_template('cadastra_usuario.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    nome_usuario = request.form.get('login_usuario')
    senha_usuario = request.form.get('login_senha')

    if request.method == 'POST' and len(nome_usuario) > 0 and len(senha_usuario) > 0:

        try:
            cur = conexao.cursor()

            sql = 'SELECT * FROM usuario WHERE nome_usuario = %s '
            cur.execute(sql, (nome_usuario,))

            account = cur.fetchone()

            if account:
                stored_password = account[2]
                if senha_usuario == stored_password:
                    session['loggedin'] = True
                    session['nome_usuario'] = nome_usuario
                    return redirect(url_for('home_page'))
                else:
                    message = 'Senha Incorreta!'
            else:
                message = 'Nome de usuário não encontrado'
        
        except Exception as e:
            return f"Ocorreu um erro: {str(e)}"
                
    return render_template('login.html', message=message)

@app.route('/cadastra_livro', methods=['POST', 'GET'])
def cadastra_livro():
    titulo = request.form.get('titulo')
    ano = request.form.get('ano')
    genero = request.form.get('genero')
    id_autor = request.form.get('id_autor')

    if request.method == 'POST' and titulo in request.form and ano in request.form and genero in request.form and id_autor in request.form:
        
        try:
            cur = conexao.cursor()

            sql = """
            INSERT INTO livro (titulo, ano, genero, autor_id)
            VALUES (%s, %s, %s, %s)
            """

            cur.execute(sql, (titulo, ano, genero, id_autor))

            conexao.commit()

            cur.close()

            return redirect(url_for('home_page'))
        
        except Exception as e:
            return f"Ocorreu um erro ao cadastrar o livro: {str(e)}"
    else:
        print('Os campos são obrigatórios')

    return render_template('cadastra_livro.html')

@app.route('/cadastra_autor', methods=['POST', 'GET'])
def cadastra_autor():
    nome = request.form.get('nome_autor')
    nacionalidade = request.form.get('nacionalidade')
    data_nascimento = request.form.get('data_nascimento')
    
    if request.method == 'POST' and nome in request.form and nacionalidade in request.form and data_nascimento in request.form:
        
        try:
            cur = conexao.cursor()

            sql = """
            INSERT INTO autor (nome, nacionalidade, data_nascimento)
            VALUES (%s, %s, %s)
            """

            cur.execute(sql, (nome, nacionalidade, data_nascimento))

            conexao.commit()

            cur.close()

            return redirect(url_for('home_page'))

        except Exception as e:
            return f"Ocorreu um erro ao cadastrar o autor: {str(e)}"
    else:
        print('Os campos são obrigatórios')
    return render_template('cadastrar_autor.html')