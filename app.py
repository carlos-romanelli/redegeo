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
    return render_template('atendimento.html', titulo='Consulta atendimentos do Redegeo')

@app.route('/consulta_atendimento', methods=['POST',])
def consulta_atendimento():
    # Comando SQL a executar
    cursor.execute("SELECT top(1000) id_Atend as Atendimento, dcr_serv as Serviço, mat_atend as Matrícula, nm_atend as Cliente, tel_cntto_atend as Contato, dt_hr_inic_atend as [Início do atendimento], u.nome_User as Atendente, obs_atend as Observação FROM tblAtendimentos a inner join tblUsuarios u on a.cod_func_atend = u.cod_User inner join tblServicos s on a.cod_serv_sol_atend = s.cod_serv where mat_atend = '" + request.form['matricula'] + "' order by dt_hr_inic_atend desc")

    # cursor.execute("SELECT top(1000) * FROM tblAtendimentos where mat_atend = '" + request.form[
    #    'matricula'] + "' order by id_Atend desc")
    return render_template('atendimento.html', titulo='Consulta atendimentos do Redegeo', atendimentos=cursor)







# from views import *

if __name__ == '__main__':
    app.run(debug=True)

conn.close()
