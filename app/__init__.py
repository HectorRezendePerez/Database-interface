from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import os
from app.consulta import *
import math
import fnmatch

app = Flask(__name__)
app.secret_key = os.urandom(24)


admin_user = 'admin'
admin_pswd = 'manager'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        

        if username == admin_user and password == admin_pswd:
            session['username'] = username
            return redirect(url_for('search'))
        else:
            error = 'Credenciais incorretas. Tente novamente.'
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect('login')

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        session['modelo'] = str(request.form['modelo']).lower()
        session['marca'] = str(request.form['marca']).lower()
        session['ano_ini'] = str(request.form['ano-inicial']).lower()
        session['ano_fin'] = str(request.form['ano-final']).lower()
        return redirect(url_for('result'))
    return render_template('search.html')

@app.route('/result', methods=['GET', 'POST'])
@login_required
def result():
    ID = ''
    cor = '' # A FAZER PESQUISA DE COR NO FRONT
    chassi = '' # A FAZER PESQUISA DE COR NO FRONT
    placa = ''# A FAZER PESQUISA DE COR NO FRONT
    fk_Produto_Id_produto = '' # VER NECESSIDADE DESSA PESQUISA
    Id_produto = '' # VER NECESSIDADE DESSA PESQUISA
    modelo = session['modelo']
    print(modelo)
    marca = session['marca']
    print(marca)
    # preco = str().lower()
    # preco = str().lower()
    preco = '' # A FAZER COMPARAÇÂO IGUAL A ANO
    ano_ini = session['ano_ini']
    ano_fin = session['ano_fin']
    # request.form["marca"]
    # request.form['modelo']
    # request.form['ano-inicial']
    # 
    # request.form['quilometragem-inicial']
    # request.form['quilometragem-final']
    results = db.query(ID, ano_ini, ano_fin, cor, chassi, placa, fk_Produto_Id_produto, Id_produto, modelo, marca, preco)
    
    current_page = int(request.args.get('page', 1))
    results_per_page = 10
    start_index = (current_page - 1) * results_per_page
    end_index = start_index + results_per_page
    paginated_results = results[start_index:end_index]
    total_pages = math.ceil(len(results) / results_per_page)
        


    return render_template('results.html', results=paginated_results, current_page=current_page, total_pages=total_pages, paginated_results=paginated_results)
