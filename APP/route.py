from flask import Blueprint, request, redirect, url_for, g, render_template, flash
from werkzeug.exceptions import abort
from .auth_bp import login_required
from .db.connection import get_db

bp = Blueprint('route', __name__)

@bp.route('/')
@login_required
def index():
    query = request.args.get('q')
    db, c = get_db()
    Equipos = []

    try:
        if query and query.strip():
            c.execute("""
                SELECT * FROM equipos 
                WHERE usuario ILIKE %s OR marca ILIKE %s OR modelo ILIKE %s
            """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        else:
            c.execute('SELECT * FROM equipos')
        Equipos = c.fetchall()
    except Exception as e:
        flash(f'Error al obtener los datos: {e}')
    finally:
        db.close()
    flash(f'Se encontraron {len(Equipos)} equipos')
    return render_template('datos/datos.html', Equipos=Equipos, query=query)


#Ingreso de nuevo elemento en la base de datos
@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
       
        usuario = request.form['usuario']
        marca = request.form['marca']
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        numero_parte = request.form['numero_parte']
        estado = request.form['estado']
        sistema_operativo = request.form['sistema_operativo']
        version_bios = request.form['version_bios']
        created_by = g.user['id'] #ID del usuario Autenticado
        error = None
        
        if usuario is None:
            error = 'El usuario es requerido'
        elif marca is None:
            error = 'La marca del equipo es requerido'
        elif modelo is None:
            error = 'El modelo del equipo es requerido'
        elif numero_serie is None:
            error = 'El numero de serie es requerido'
        elif numero_parte is None:
            error = 'El Numero de Parte es requerido'
        elif estado is None:
            error = 'El estado del equipo es requerido'
        elif sistema_operativo is None:
            error = 'El Sistema Operativo es requerido'
        elif version_bios is None:
            error = 'La version de Bios es requerido'
        
        if error is not None:
            flash(error)

        else:
            db, c = get_db()
            c.execute(
            '''INSERT INTO equipos 
            (usuario, marca, modelo, numero_serie, numero_parte, estado, sistema_operativo, version_bios, created_by) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (usuario, marca, modelo, numero_serie, numero_parte, estado, sistema_operativo, version_bios, created_by))
      
            db.commit()
            flash('Equipo registrado exitosamente', 'success')
            return redirect(url_for('route.create'))
    return render_template('datos/create.html')

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    equipo = get_up(id)

    if request.method == 'POST':
        usuario = request.form['usuario']
        marca = request.form['marca']
        modelo = request.form['modelo']
        numero_serie = request.form['numero_serie']
        numero_parte = request.form['numero_parte']
        estado = request.form['estado']
        sistema_operativo = request.form['sistema_operativo']
        version_bios = request.form['version_bios']

        db, c = get_db()
        c.execute('''
            update equipos set usuario = %s, marca = %s, modelo = %s, numero_serie = %s, numero_parte = %s, estado = %s, sistema_operativo = %s, version_bios = %s where id = %s 
''', (usuario, marca, modelo, numero_serie, numero_parte, estado, sistema_operativo, version_bios, id))
        db.commit()
        flash('Equipo actualizado correctamente', 'success')
        return redirect(url_for('route.index'))
    return render_template('datos/update.html', equipo = equipo)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    equipo = get_up(id)
    db, c = get_db()
    c.execute('DELETE FROM equipos WHERE id = %s', (id,))
    db.commit()
    flash('Equipo eliminado correctamente', 'success')
    return redirect(url_for('route.index'))

def get_up(id):
    db, c = get_db()
    c.execute (
        'SELECT e.id, e.usuario, e.modelo, e.marca, e.numero_serie, e.numero_parte, e.estado, e.sistema_operativo, e.version_bios, e.created_by, u.username '
        ' FROM equipos e JOIN users u ON e.created_by = u.id WHERE e.id = %s',
        (id,)
    )
    equipo = c.fetchone()

    if equipo is None:
        abort(404, "El equipo de id {0} no existe".format(id))
    
    return equipo