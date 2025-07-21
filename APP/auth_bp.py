import functools
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, flash, redirect, url_for, render_template, g, session, request
from .db.connection import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def log(user_id, accion):
    db, c = get_db()
    c.execute('insert into logs_actividad (user_id, accion) values (%s, %s)', (user_id, accion))
    db.commit()

def permisos_requeridos(modulo, permiso):
    def decorador(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            db, c = get_db()
            c.execute(
                'select * from permisos where user_id = %s and modulo = %s and permiso = %s', (g.user['id'], modulo, permiso))
            
            if c.fetchone() is None:
                flash('Permiso denegado', 'error')
                return redirect(url_for('auth.login'))
            return view(**kwargs)
        return wrapped_view
    return decorador
            

#Registro de usuario
@bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None

        #Verificacion si el usuario existe en la base de datos
        c.execute('select id from users where username = %s', (username, ))
        existing_user = c.fetchone()

        #Usuarios Registrados
        c.execute('select count(*) as count from users')
        user_count = c.fetchone()['count']
        role = 'admin' if user_count == 0 else 'lector'

        if not username:
            error = 'Usuario es requerido'
        if not password:
            error = 'Contraseña es requerida'
        elif existing_user is not None:
            error = 'El usuario {} ya se encuentra registrado'.format(username)
        
        if error is None:
            c.execute (
                'INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, generate_password_hash(password), role)
            )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


def roles_required(*roles):
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None or g.user['role'] not in roles:
                flash('Acceso denegado: permisos insuficientes', 'error')
                return redirect(url_for('auth.login'))
            return view(**kwargs)
        return wrapped_view
    return decorator

@bp.route('/manage_roles', methods=['GET', 'POST'])
@roles_required('admin')
def manage_roles():
    db, c = get_db()

    if request.method == 'POST':
        user_id = request.form['user_id']
        new_role = request.form['new_role']

        c.execute('update users set role = %s where id = %s', (new_role, user_id))
        db.commit()
        log(g.user['id'], f'cambio de rol para usuario ID {user_id} a {new_role}')
        flash('Rol asignado correctamente', 'success')
    
    c.execute('select id, username, role from users')
    users = c.fetchall()
    return render_template('auth/manage_roles.html', users = users)

#Inicio de sesion
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute('SELECT * FROM users WHERE username = %s', (username, ))
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o Contraseña Incorrectos'

        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o Contraseña incorrectos'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            log(user['id'], 'Inicio de Sesion')
            return redirect(url_for('mikoshi.index'))
        flash(error)
    return render_template('auth/login.html')


# Carga de usuarios antes de cada solicitud
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute('SELECT * FROM users WHERE id = %s', (user_id, ))
        g.user = c.fetchone()

# Decorar para proteccion de rutas
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        db, c = get_db()
        error = None

        #Verificacion de contraseña
        c.execute('select * from users where id = %s', (g.user['id'], ))
        user = c.fetchone()

        if not check_password_hash(user['password'], current_password):
            error = 'La contraseña actual es incorrecta '
        
        elif new_password != confirm_password:
            error = 'Las nuevas contraseñas no coinciden'
        
        elif not new_password:
            error = 'La nueva contraseña no puede estar vacia'
        
        if error is None:
            c.execute(
                'update users set password = %s where id = %s',
                (generate_password_hash(new_password), g.user['id'])
            )
            db.commit()
            log(g.user['id'], 'Cambio de contraseña')
            flash('Contraseña actualizada exitosamente')
            return redirect(url_for('auth.update_password'))
        flash(error)
    return render_template('auth/update_password.html')

# Cierre de Sesion
@bp.route('/logout')
def logout():
    
    if g.user:
        log(g.user['id'], 'Cierre de sesion')
    session.clear()
    return redirect(url_for('auth.login'))

