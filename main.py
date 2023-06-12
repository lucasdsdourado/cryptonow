import sqlite3
import json
import zipfile
import os
import querys as q
import selects as sl
from pybit.unified_trading import HTTP
from flask_apscheduler import APScheduler
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, flash, url_for, send_file

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Lucas","ldsd","1234")
usuarios = {usuario1.nickname : usuario1}

def criarbd():
    conexao = sqlite3.connect('Banco_de_dados')
    cursor = conexao.cursor()
    cursor.execute(q.sql[0][0])
    cursor.execute(q.sql[2][0])
    cursor.execute(q.sql[4][0])
    cursor.execute(q.sql[8][0])
    conexao.commit()
    cursor.close()

def selectprecos():
    conexao = sqlite3.connect('Banco_de_dados')
    cursor = conexao.cursor()
    cursor.execute(sl.variacao)
    selecao = cursor.fetchall()
    cursor.close()   
    return selecao

def selectprecosfav():
    conexao = sqlite3.connect('Banco_de_dados')
    cursor = conexao.cursor()
    cursor.execute(sl.favoritas)
    selecao = cursor.fetchall()
    cursor.close()   
    return selecao

def selectulatulz():
    conexao = sqlite3.connect('Banco_de_dados')
    cursor = conexao.cursor()
    cursor.execute(sl.utlimaatualiz)
    selecao = cursor.fetchone()
    cursor.close()   
    return selecao[0]

def baixarprecos():
    dtxt = datetime.now().strftime('%d/%m/%Y %H:%M')
    tmdata = int(datetime.strptime(dtxt, '%d/%m/%Y %H:%M').timestamp()*1000)
    conexao = sqlite3.connect('Banco_de_dados')
    cursor = conexao.cursor()
    cursor.execute(q.sql[7][0])
    cursor.execute(q.sql[5][0])
    session = HTTP(testnet=False)
    dados = session.get_instruments_info(
        category="spot"
    )
    print('baixando precos')
    for i in dados['result']['list']:
        session = HTTP(testnet=False)
        try:
            if((i['symbol'][-4:]) == 'USDT'):
                dkline = session.get_index_price_kline(
                category="linear",
                symbol=i['symbol'],
                interval=3,
                start=tmdata-600000,
                end=tmdata,
                )
                moeda = i['symbol'][:-4] + '/USDT'
                vlatual = float(dkline['result']['list'][0][1])
                vlanter = float(dkline['result']['list'][1][1])
                percent = f'{(1 - (vlanter/vlatual))*100:.8f}'
                insert = q.sql[1][0].format(tmdata,moeda,vlatual,vlanter,percent)
                cursor.execute(insert)
                conexao.commit()
        except:
            insert = q.sql[6][0].format(f"'{i['symbol']}'")
            cursor.execute(insert)
            conexao.commit()

    cursor.execute(q.sql[3][0])
    cursor.execute(q.sql[4][0])
    cursor.close()
    print('fim')
    return 0
criarbd()

app = Flask(__name__)
app.secret_key = 'cryptonowkey'
app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}

# Configuração do APScheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route('/')
def index():
    lista = selectprecos()
    ultalz = selectulatulz()
    return render_template('lista.html', titulo='CryptoNow', valores = lista, ultatualiz = ultalz)

@app.route('/favoritas')
def favoritas():
    lista = selectprecosfav()
    return render_template('favoritas.html', titulo='CryptoNow', valores = lista)

@app.route('/dados')
def dados():
    return render_template('export.html', titulo='CryptoNow')

@app.route('/export', methods=['GET'])
def export():
    # Nome do arquivo do banco de dados SQLite
    database_file = 'Banco_de_dados'
    # Lista de tabelas a serem exportadas
    tables = ['FAVORITAS', 'LOGERROS', 'MARKETANTIG', 'MARKETATUAL']
    # Nome do arquivo ZIP resultante
    zip_file_name = 'export.zip'

    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Crie um dicionário para armazenar os dados de todas as tabelas
    data = {}

    # Itere sobre as tabelas e obtenha os dados
    for table_name in tables:
        # Consultar todas as linhas da tabela
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Lista para armazenar as linhas da tabela
        table_data = []

        # Percorra as linhas e adicione ao dicionário da tabela
        for row in rows:
            # Crie um dicionário com os dados da linha
            row_data = {}
            for i, column_name in enumerate(cursor.description):
                row_data[column_name[0]] = row[i]
            
            # Adicione a linha à lista de dados da tabela
            table_data.append(row_data)

        # Adicione os dados da tabela ao dicionário principal
        data[table_name] = table_data

    # Feche a conexão com o banco de dados SQLite
    cursor.close()
    conn.close()

    # Salve os dados em arquivos JSON
    for table_name, table_data in data.items():
        # Crie o nome do arquivo com base no nome da tabela
        filename = f"{table_name}.json"

        # Escreva os dados da tabela no arquivo JSON
        with open(filename, 'w') as json_file:
            json.dump(table_data, json_file)

    # Crie um arquivo ZIP e adicione todos os arquivos JSON a ele
    with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
        for table_name in tables:
            filename = f"{table_name}.json"
            zip_file.write(filename)

            # Remova o arquivo JSON após adicioná-lo ao arquivo ZIP
            os.remove(filename)

    # Envie o arquivo ZIP como resposta para o cliente
    return send_file('export.zip', as_attachment=True)


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname+ ' logado com sucesso!','success')
            proxima_pagina = request.form['proxima']
            if proxima_pagina == "":
                return redirect(proxima_pagina)
            else:
                return redirect(url_for('index'))
    else:
        flash('Usuário ' + request.form['usuario'] + ' não cadastrado.', 'error')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/bybit')
def bybit():
    return render_template('bybit.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/atualizar_tabela', methods=['POST'])
def atualizar_tabela():
    data = request.get_json()
    moeda = data.get('moeda')
    conexao = sqlite3.connect('Banco_de_dados')
    cursor = conexao.cursor()
    cont = cursor.execute(sl.checkmoeda.format(moeda)).fetchone()
    if(cont[0] == 0):
        cursor.execute(q.sql[9][0].format(moeda))
    else:
        cursor.execute(q.sql[10][0].format(moeda))

    conexao.commit()
    cursor.close()

    # Retorne uma resposta adequada
    return 'Tabela atualizada com sucesso'


# Tarefa agendada para executar
@scheduler.task('interval', id='update_number', seconds=360, misfire_grace_time=1)
def update_number():
    number = baixarprecos()
    # Envie o número para todos os clientes conectados
    scheduler.app.number = number

if __name__ == '__main__':
    app.run(debug=True)

