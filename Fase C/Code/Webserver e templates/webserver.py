from flask import Flask, request, jsonify, redirect, url_for, render_template_string,render_template, session, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector

app = Flask(__name__)
app.secret_key = 'ok'  
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redireciona utilizadores para a pagina login se não tiveram logados

# Configuração da Base de Dados MySQL
DB_CONFIG = {
    "host": "localhost",
    "auth_plugin": "mysql_native_password",
    #User e pass depende da pessoa que têm acesso á base de dados (localhost)
    "user": "root",
    "passwd": "idkwhattodo",
    "database": "teste"
}
# User model para o Flask-Login
class User(UserMixin):
    def __init__(self, id, username, type):
        self.id = id
        self.username = username
        self.type = type

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT user_id, username, user_type FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    connection.close()
    if user:
        return User(user['user_id'], user['username'], user['user_type'])
    return None

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, username, password_hash FROM users WHERE username = %s AND password_hash = %s", (username,password,))
        user = cursor.fetchone()
        #connection.close()

        if user: #and bcrypt.check_password_hash(user['password_hash'], password):
            cursor.execute("SELECT user_type FROM users WHERE username = %s AND password_hash = %s", (username,password,))
            admin = cursor.fetchone()
            connection.close()
            if admin['user_type'] == "admin":
                login_user(User(user['user_id'], user['username'],admin['user_type']))
                return redirect(url_for('admin'))
            else:
                login_user(User(user['user_id'], user['username'],admin['user_type']))
                return redirect(url_for('dashboard'))
        else:
            message = 'Username ou palavra-passe incorreta.'

    return render_template('login.html', message=message)

# Parque de Estacionamento
@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch parking spots from the database
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT spot_id, status, last_update FROM parking_spots")
    parking_spots = cursor.fetchall()
    connection.close()
    return render_template('parkinglot.html', user=current_user, spots=parking_spots)

#Admin
@app.route('/admin')
@login_required
def admin():
    message = ''
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT username , user_type FROM users")
    listusers = cursor.fetchall()
    connection.close()
    return render_template('admin.html',message=message, user=current_user, spots=listusers)

#Promover
@app.route('/upgrade_user/<username>')
@login_required
def upgrade_user(username):
    message = "O utilizador "+ username + " foi promovido."
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("UPDATE users SET user_type = 'admin' WHERE username = %s", (username,))
    connection.commit()
    cursor.execute("SELECT username , user_type FROM users")
    listusers = cursor.fetchall()
    connection.close()
    return render_template('admin.html',message=message, user=current_user, spots=listusers)
    #return redirect(url_for('admin'))

#Despromover
@app.route('/downgrade_user/<username>')
@login_required
def downgrade_user(username):
    message = "O utilizador "+ username + " foi despromovido."
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("UPDATE users SET user_type = 'normal' WHERE username = %s", (username,))
    connection.commit()
    cursor.execute("SELECT username , user_type FROM users")
    listusers = cursor.fetchall()
    connection.close()
    return render_template('admin.html',message=message, user=current_user, spots=listusers)
    #return redirect(url_for('admin'))

#Remover
@app.route('/remove_user/<username>')
@login_required
def remove_user(username):
    message = "O utilizador "+ username + " foi removido."
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("DELETE FROM users WHERE username = %s", (username,))
    connection.commit()
    cursor.execute("SELECT username , user_type FROM users")
    listusers = cursor.fetchall()
    connection.close()
    return render_template('admin.html',message=message, user=current_user, spots=listusers)
    #return redirect(url_for('admin'))

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Criar Conta
@app.route('/createacc', methods=['GET', 'POST'])
def createacc():
    message= ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar se já existe uma conta com esse username.
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            message = 'Username já existe. Por favor escolhe outro.'
        else:
            # Colocar esse user na base de dados
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password))
            connection.commit()
            message = 'Conta criada com sucesso! Já podes fazer login.'

        connection.close()
    return render_template('createaccount.html',message=message)

# Run the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')