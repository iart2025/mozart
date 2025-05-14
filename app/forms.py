from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class CadastroForm(FlaskForm):
    nome = StringField('Nome completo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=8)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    tipo = SelectField('Tipo de usuário', choices=[('Paciente', 'Paciente'), ('Profissional', 'Profissional')])
    submit = SubmitField('Cadastrar')

class AgendamentoForm(FlaskForm):
    profissional_id = SelectField('Profissional', coerce=int, validators=[DataRequired()])
    data = StringField('Data e Hora', validators=[DataRequired()])
    submit = SubmitField('Agendar')

class MensagemForm(FlaskForm):
    texto = StringField('Mensagem', validators=[DataRequired()])
    submit = SubmitField('Enviar')
