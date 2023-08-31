from flask import Flask
from flask import render_template, request, redirect, flash, url_for

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
app.config.from_pyfile('config.py')


@app.route('/')
def index():
    return render_template('index.html', titulo='Consulta do Redegeo')


@app.route('/atendimento')
def atendimento():
    return render_template('atendimento.html', titulo='Consulta atendimentos do Redegeo')


@app.route('/consulta_atendimento', methods=['POST', ])
def consulta_atendimento():
    # Comando SQL a executar
    cursor.execute("SELECT id_Atend as Atendimento,"
                   "dcr_serv as Serviço, "
                   "mat_atend as Matrícula, "
                   "nm_atend as Cliente, "
                   "tel_cntto_atend as Contato, "
                   "dt_hr_inic_atend as [Início do atendimento], "
                   "u.nome_User as Atendente, "
                   "obs_atend as Observação FROM tblAtendimentos a "
                   "left join tblUsuarios u on a.cod_func_atend = u.cod_User "
                   "left join tblServicos s on a.cod_serv_sol_atend = s.cod_serv "
                   "where mat_atend = '" + request.form['matricula'] + "' order by dt_hr_inic_atend desc")
    return render_template('atendimento.html', titulo='Consulta atendimentos do Redegeo', atendimentos=cursor)


@app.route('/servico')
def servico():
    return render_template('servico.html', titulo='Consulta SSs do Redegeo')


@app.route('/consulta_servico', methods=['POST', ])
def consulta_servico():
    # Comando SQL a executar
    if request.form['servico']:
        cursor.execute("SELECT id_ss, "
                       "format(dt_hr_ss, 'dd/MM/yyyy','en-US'), "
                       "dcr_serv, "
                       "matricula_ss, "
                       "nome_solic_ss, "
                       "logradouro_ss, "
                       "nmr_imov_ss, "
                       "compl_end_ss, "
                       "tel_solic_ss, "
                       "cod_ss_origem, "
                       "o.nome_user, "
                       "u.nm_undd, "
                       "obs_sol_ss "
                       "FROM[Redegeo-ant].[dbo].[tblSS] as s "
                       "left join tblServicos as v on s.cod_ser = v.cod_serv "
                       "left join tblEquipes e on s.cod_eqp_ss = e.cod_eqp "
                       "left join tblUnidades u on s.cod_und_sol = u.cod_undd "
                       "left join tblUsuarios o on s.cod_user_ss = o.cod_user "
                       "where id_ss = " + request.form['servico'])

        return render_template('servico.html', titulo='Consulta SSs do Redegeo', servicos=cursor)
    else:
        flash('Digite o número da SS')
        return redirect(url_for('servico'))


@app.route('/ss')
def ss():
    return render_template('ss.html', titulo='Consulta SSs do Redegeo')


@app.route('/consulta_ss', methods=['POST', ])
def consulta_ss():
    # Comando SQL a executar
    if request.form['matricula']:
        cursor.execute("SELECT id_ss, "
                       "format(dt_hr_ss, 'dd/MM/yyyy','en-US'), "
                       "dcr_serv, "
                       "matricula_ss, "
                       "nome_solic_ss, "
                       "logradouro_ss, "
                       "nmr_imov_ss, "
                       "compl_end_ss, "
                       "tel_solic_ss, "
                       "cod_ss_origem, "
                       "o.nome_user, "
                       "u.nm_undd, "
                       "obs_sol_ss "
                       "FROM[Redegeo-ant].[dbo].[tblSS] as s "
                       "left join tblServicos as v on s.cod_ser = v.cod_serv "
                       "left join tblEquipes e on s.cod_eqp_ss = e.cod_eqp "
                       "left join tblUnidades u on s.cod_und_sol = u.cod_undd "
                       "left join tblUsuarios o on s.cod_user_ss = o.cod_user "
                       "where matricula_ss = '" + request.form['matricula'] + "'")

        return render_template('ss.html', titulo=f"SSs da matrícula {request.form['matricula']}", sss=cursor)
    else:
        flash('Digite o número da matrícula')
        return redirect(url_for('ss'))


@app.route('/consulta_tramite, <int:id_ss>')
def consulta_tramite(id_ss):
    # Comando SQL a executar
    cursor.execute("SELECT id_tram, "
                   "cod_ss_tram, "
                   "format(dt_tram, 'dd/MM/yyyy', 'en-US'), "
                   "d.nm_undd, "
                   "u.nome_User, "
                   "d2.nm_undd, "
                   "u2.nome_User, "
                   "texto_despacho_tram "
                   "FROM[Redegeo-ant].dbo.tblTramiteSS t "
                   "left join tblUsuarios u on t.cod_func_origem_tram = u.cod_User "
                   "left join tblUsuarios u2 on t.cod_user_tram = u2.cod_User "
                   "left join tblUnidades d on t.cod_undd_origem_tram = d.cod_undd "
                   "left join tblUnidades d2 on t.cod_undd_destino_tram = d2.cod_undd "
                   "where cod_ss_tram = " + str(id_ss))

    return render_template('tramite.html', titulo=f'Lista de Trâmites da SS {str(id_ss)}', tramites=cursor)

# from views import *


if __name__ == '__main__':
    app.run(debug=True)

conn.close()
