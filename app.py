#GERENCIADOR DE LINKS

import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
db = SQLAlchemy(app)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)


@app.route('/')
def pagina_inicial():
    
    links_do_db = Link.query.all()
    # Envia os links para o 'index.html'
    return render_template('index.html', links_para_mostrar=links_do_db)

# ROTA 2: ADICIONAR LINK (Recebe os dados do formulário)
@app.route('/adicionar', methods=['POST'])
def adicionar_link():
    # Pega os dados que vieram do formulário HTML
    titulo_novo = request.form['titulo_html']
    url_nova = request.form['url_html']
    
    # Cria um novo "Link" com esses dados
    novo_link = Link(titulo=titulo_novo, url=url_nova)
    
    # Adiciona e Salva o novo link no banco de dados
    db.session.add(novo_link)
    db.session.commit()
    
    # Manda o usuário de volta para a página inicial
    return redirect(url_for('pagina_inicial'))

# ROTA 3: EXCLUIR LINK
@app.route('/excluir/<int:id_do_link>', methods=['POST'])
def excluir_link(id_do_link):
    
    # 1. Encontra o link no banco de dados usando o ID que recebemos
    link_para_excluir = Link.query.get(id_do_link)
    
    # 2. Se o link for encontrado, exclui ele
    if link_para_excluir:
        db.session.delete(link_para_excluir)
        db.session.commit()
    
    # 3. Manda o usuário de volta para a página inicial
    return redirect(url_for('pagina_inicial'))


# --- CÓDIGO ADICIONADO (ROTA 4) ---
# ROTA 4: EDITAR LINK (Lida com GET e POST)
@app.route('/editar/<int:id_do_link>', methods=['GET', 'POST'])
def editar_link(id_do_link):
    
    # 1. Encontra o link no banco de dados que queremos editar
    #    (Usamos .get() que é a forma mais simples de buscar por ID)
    link_para_editar = Link.query.get(id_do_link)

    # Se o link não for encontrado, apenas redireciona para a home
    if not link_para_editar:
        return redirect(url_for('pagina_inicial'))

    # 2. SE O USUÁRIO SALVOU O FORMULÁRIO (Método POST)
    if request.method == 'POST':
        # Pega os novos dados que vieram do formulário de 'editar.html'
        link_para_editar.titulo = request.form['titulo_html']
        link_para_editar.url = request.form['url_html']
        
        # Salva (commita) as mudanças no banco
        db.session.commit()
        
        # Redireciona de volta para a página inicial
        return redirect(url_for('pagina_inicial'))
    
    # 3. SE O USUÁRIO ACABOU DE CLICAR EM "EDITAR" (Método GET)
    else:
        # Mostra a página 'editar.html' e envia os dados do link atual
        # para preencher os campos do formulário (value="{{ link.titulo }}")
        return render_template('editar.html', link=link_para_editar)
# --- FIM DO CÓDIGO ADICIONADO (ROTA 4) ---


# --- EXECUÇÃO ---

if __name__ == '__main__':
    
    with app.app_context():
        instance_path = os.path.join(basedir, 'instance')
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
            
        db.create_all() 
        
    app.run(debug=True)

