import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# --- CONFIGURAÇÕES ---
app.config['SECRET_KEY'] = 'chave-secreta-do-yago-tokito-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configura onde salvar as fotos
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- MODELOS ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # Nova coluna: Nome do arquivo da foto (pode ser vazio)
    foto_perfil = db.Column(db.String(150), nullable=True)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    categoria = db.Column(db.String(50), nullable=False, default='Outros')
    publico = db.Column(db.Boolean, default=False)
    clicks = db.Column(db.Integer, default=0)


# --- CRIAÇÃO DO BANCO DE DADOS (Preparado para o Render) ---
with app.app_context():
    # Cria a pasta de uploads se ela não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # Cria as tabelas do banco de dados
    db.create_all()
    # Cria o usuário padrão se não existir
    if not User.query.filter_by(username='yago.costa').first():
        senha_hash = generate_password_hash('12345')
        admin = User(username='yago.costa', password=senha_hash)
        db.session.add(admin)
        db.session.commit()


# --- ROTAS ---

# ROTA DE UPLOAD DE FOTO
@app.route('/upload_foto', methods=['POST'])
@login_required
def upload_foto():
    if 'foto' not in request.files:
        flash('Nenhuma imagem enviada.')
        return redirect(url_for('pagina_inicial'))
    
    arquivo = request.files['foto']
    
    if arquivo.filename == '':
        flash('Nenhuma imagem selecionada.')
        return redirect(url_for('pagina_inicial'))

    if arquivo and allowed_file(arquivo.filename):
        filename = secure_filename(arquivo.filename)
        # Salva na pasta static/uploads
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Salva o nome no banco de dados do usuário atual
        current_user.foto_perfil = filename
        db.session.commit()
        
    return redirect(url_for('pagina_inicial'))

@app.route('/ir/<int:id_do_link>')
def ir_para_link(id_do_link):
    link = Link.query.get_or_404(id_do_link)
    link.clicks += 1
    db.session.commit()
    url_destino = link.url
    if not url_destino.startswith('http'):
        url_destino = 'https://' + url_destino
    return redirect(url_destino)

@app.route('/')
def pagina_inicial():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))     
    links_do_db = Link.query.all()
    return render_template('index.html', links_para_mostrar=links_do_db)

@app.route('/u/yago')
def perfil_publico():
    # Pega o usuário Yago para mostrar a foto dele
    dono = User.query.filter_by(username='yago.costa').first()
    links_publicos = Link.query.filter_by(publico=True).all()
    return render_template('publico.html', links=links_publicos, dono=dono)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']
        user = User.query.filter_by(username=usuario).first()
        if user and check_password_hash(user.password, senha):
            login_user(user)
            return redirect(url_for('pagina_inicial'))
        flash('Login inválido.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('pagina_inicial'))

@app.route('/adicionar', methods=['POST'])
@login_required
def adicionar_link():
    titulo = request.form.get('titulo_html')
    url = request.form.get('url_html')
    categoria = request.form.get('categoria_html', 'Outros')
    is_public = True if request.form.get('publico_html') else False
    novo_link = Link(titulo=titulo, url=url, categoria=categoria, publico=is_public)
    db.session.add(novo_link)
    db.session.commit()
    return redirect(url_for('pagina_inicial'))

@app.route('/excluir/<int:id_do_link>', methods=['POST'])
@login_required
def excluir_link(id_do_link):
    link = Link.query.get(id_do_link)
    if link:
        db.session.delete(link)
        db.session.commit()
    return redirect(url_for('pagina_inicial'))

@app.route('/editar/<int:id_do_link>', methods=['GET', 'POST'])
@login_required
def editar_link(id_do_link):
    link = Link.query.get(id_do_link)
    if not link: return redirect(url_for('pagina_inicial'))

    if request.method == 'POST':
        link.titulo = request.form.get('titulo_html')
        link.url = request.form.get('url_html')
        link.categoria = request.form.get('categoria_html', 'Outros')
        link.publico = True if request.form.get('publico_html') else False
        db.session.commit()
        return redirect(url_for('pagina_inicial'))
    else:
        return render_template('editar.html', link=link)

if __name__ == '__main__':
    # Agora aqui fica apenas o comando para rodar localmente na sua máquina
    app.run(debug=True)
