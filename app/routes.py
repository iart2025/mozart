from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Usuario, Sessao, Mensagem
from .forms import LoginForm, CadastroForm, AgendamentoForm, MensagemForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.senha_hash, form.senha.data):
            session['usuario_id'] = usuario.id
            session['tipo'] = usuario.tipo
            return redirect(url_for('main.dashboard'))
        else:
            flash('Credenciais inválidas.')
    return render_template('login.html', form=form)

@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        senha_hash = generate_password_hash(form.senha.data)
        novo = Usuario(nome=form.nome.data, email=form.email.data, telefone=form.telefone.data,
                       senha_hash=senha_hash, tipo=form.tipo.data)
        db.session.add(novo)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça o login.')
        return redirect(url_for('main.login'))
    return render_template('cadastro.html', form=form)

@main.route('/dashboard')
def dashboard():
    tipo = session.get('tipo')
    usuario_id = session.get('usuario_id')
    usuario = Usuario.query.get(usuario_id)
    qr = None
    if tipo == 'Profissional':
        qr = f"https://wa.me/55{usuario.telefone}"
    return render_template('dashboard.html', usuario=usuario, qr=qr)

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@main.route("/agendar", methods=["GET", "POST"])
def agendar():
    if session.get('tipo') != 'Paciente':
        flash("Apenas pacientes podem agendar sessões.")
        return redirect(url_for('main.dashboard'))

    profissionais = Usuario.query.filter_by(tipo='Profissional').all()
    form = AgendamentoForm()
    form.profissional_id.choices = [(p.id, p.nome) for p in profissionais]

    if form.validate_on_submit():
        sessao = Sessao(
            paciente_id=session.get('usuario_id'),
            profissional_id=form.profissional_id.data,
            data=form.data.data
        )
        db.session.add(sessao)
        db.session.commit()
        flash("Sessão agendada com sucesso!")
        return redirect(url_for('main.dashboard'))
    return render_template("agendar.html", form=form)

@main.route("/sessoes")
def sessoes():
    usuario_id = session.get('usuario_id')
    tipo = session.get('tipo')
    if tipo == 'Paciente':
        sessoes = Sessao.query.filter_by(paciente_id=usuario_id).all()
    else:
        sessoes = Sessao.query.filter_by(profissional_id=usuario_id).all()
    return render_template("sessoes.html", sessoes=sessoes)

@main.route("/chat/<int:user_id>", methods=["GET", "POST"])
def chat(user_id):
    atual_id = session.get('usuario_id')
    outro = Usuario.query.get_or_404(user_id)
    form = MensagemForm()
    if form.validate_on_submit():
        msg = Mensagem(
            remetente_id=atual_id,
            destinatario_id=outro.id,
            texto=form.texto.data
        )
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('main.chat', user_id=user_id))

    mensagens = Mensagem.query.filter(
        ((Mensagem.remetente_id == atual_id) & (Mensagem.destinatario_id == outro.id)) |
        ((Mensagem.remetente_id == outro.id) & (Mensagem.destinatario_id == atual_id))
    ).order_by(Mensagem.timestamp).all()
    return render_template("chat.html", mensagens=mensagens, outro=outro, form=form)
