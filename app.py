from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, session, flash, url_for
import datetime

# from models import Atendimento

import pyodbc


# String de conexão com o banco de dados
conn = pyodbc.connect('Driver={SQL Server};'
'Server=ATI06\CESADW;'
'Database=Redegeo-ant;'
'UID=redegeo.cons;'
'PWD=redegeo')

# Criar um objeto cursor

cursor = conn.cursor()



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', titulo='Consulta do Redegeo')

@app.route('/atendimento')
def atendimento():
    # Comando SQL a executar
    cursor.execute('SELECT top(1000) * FROM tblAtendimentos order by id_Atend desc')
    return render_template('atendimento.html', titulo='Consulta do Redegeo', atendimentos=cursor)


# from views import *

if __name__ == '__main__':
    app.run(debug=True)

conn.close()