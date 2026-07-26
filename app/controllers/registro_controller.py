from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.alumno import Alumno
from app.models.visita import Visita
from app.models.institucion_educativa import InstitucionEducativa
from app.models.promotor import Promotor
from app.models.carrera import Carrera
from app.services.auditoria_service import registrar_auditoria
from app import db
from datetime import datetime, date
import re

registro_bp = Blueprint('registro', __name__, url_prefix='/registro')

def calcular_edad(fecha_nac):
    hoy = date.today()
    return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

def validar_dni(dni):
    return re.match(r'^\d{8}$', dni)

def validar_celular(celular):
    return re.match(r'^\d{9}$', celular)

def validar_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) if email else True

@registro_bp.route('/', methods=['GET', 'POST'])
@login_required
def registrar():
    colegios = InstitucionEducativa.query.filter_by(activo=True).all()
    promotores = Promotor.query.filter_by(activo=True).all()
    carreras = Carrera.query.filter_by(activo=True).all()

    if request.method == 'POST':
        apellidos = request.form.get('apellidos', '').strip().upper()
        nombres = request.form.get('nombres', '').strip().upper()
        dni = request.form.get('dni', '').strip()
        fecha_nac = request.form.get('fecha_nacimiento', '')
        sexo = request.form.get('sexo', '').upper()
        celular = request.form.get('celular', '').strip()
        email = request.form.get('email', '').strip()
        direccion = request.form.get('direccion', '').strip()
        institucion_id = request.form.get('institucion_id', type=int)
        carrera_id = request.form.get('carrera_id', type=int)
        area_interes = request.form.get('area_interes', '')
        desea_estudiar = request.form.get('desea_estudiar') == 'on'
        solicita_info = request.form.get('solicita_info') == 'on'
        modalidad_contacto = request.form.get('modalidad_contacto', '')
        fecha_visita = request.form.get('fecha_visita', '')
        hora_visita = request.form.get('hora_visita', '')
        promotor_id = request.form.get('promotor_id', type=int)
        observaciones = request.form.get('observaciones', '')

        errores = []
        if not validar_dni(dni):
            errores.append('El DNI debe tener 8 dígitos.')
        if Alumno.query.filter_by(dni=dni).first():
            errores.append('El DNI ya está registrado.')
        if not validar_celular(celular):
            errores.append('El celular debe tener 9 dígitos.')
        if email and not validar_email(email):
            errores.append('El correo electrónico no es válido.')
        if not apellidos or not nombres:
            errores.append('Nombres y apellidos son obligatorios.')

        if errores:
            for e in errores:
                flash(e, 'danger')
            return render_template('registro/index.html', colegios=colegios, promotores=promotores, carreras=carreras,
                form=request.form)

        try:
            fecha_nac_date = datetime.strptime(fecha_nac, '%Y-%m-%d').date()
            edad = calcular_edad(fecha_nac_date)

            alumno = Alumno(
                apellidos=apellidos,
                nombres=nombres,
                dni=dni,
                fecha_nacimiento=fecha_nac_date,
                edad=edad,
                sexo=sexo,
                celular=celular,
                email=email,
                direccion=direccion,
                institucion_id=institucion_id,
                carrera_id=carrera_id,
                area_interes=area_interes,
                desea_estudiar=desea_estudiar,
                solicita_info=solicita_info,
                modalidad_contacto=modalidad_contacto
            )
            db.session.add(alumno)
            db.session.flush()

            fv = datetime.strptime(fecha_visita, '%Y-%m-%d').date() if fecha_visita else date.today()
            hv = datetime.strptime(hora_visita, '%H:%M').time() if hora_visita else datetime.now().time()

            visita = Visita(
                alumno_id=alumno.id,
                promotor_id=promotor_id,
                usuario_id=current_user.id,
                fecha_visita=fv,
                hora_visita=hv,
                observaciones=observaciones
            )
            db.session.add(visita)
            db.session.commit()

            registrar_auditoria(current_user.id, 'Creación de registro', 'Registro',
                f'Registro creado: Alumno {dni} - {nombres} {apellidos}')
            flash('Registro creado exitosamente.', 'success')
            return redirect(url_for('consulta.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}', 'danger')

    return render_template('registro/index.html', colegios=colegios, promotores=promotores, carreras=carreras,
        form=request.form)

@registro_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    alumno = Alumno.query.get_or_404(id)
    visita = Visita.query.filter_by(alumno_id=alumno.id).first()
    colegios = InstitucionEducativa.query.filter_by(activo=True).all()
    promotores = Promotor.query.filter_by(activo=True).all()
    carreras = Carrera.query.filter_by(activo=True).all()

    if request.method == 'POST':
        alumno.apellidos = request.form.get('apellidos', '').strip().upper()
        alumno.nombres = request.form.get('nombres', '').strip().upper()
        alumno.celular = request.form.get('celular', '').strip()
        alumno.email = request.form.get('email', '').strip()
        alumno.direccion = request.form.get('direccion', '').strip()
        alumno.institucion_id = request.form.get('institucion_id', type=int)
        alumno.carrera_id = request.form.get('carrera_id', type=int)
        alumno.area_interes = request.form.get('area_interes', '')
        alumno.desea_estudiar = request.form.get('desea_estudiar') == 'on'
        alumno.solicita_info = request.form.get('solicita_info') == 'on'
        alumno.modalidad_contacto = request.form.get('modalidad_contacto', '')

        if visita:
            visita.promotor_id = request.form.get('promotor_id', type=int)
            visita.observaciones = request.form.get('observaciones', '')

        db.session.commit()
        registrar_auditoria(current_user.id, 'Edición de registro', 'Registro',
            f'Registro editado: Alumno {alumno.dni}')
        flash('Registro actualizado exitosamente.', 'success')
        return redirect(url_for('consulta.index'))

    form = {
        'apellidos': alumno.apellidos,
        'nombres': alumno.nombres,
        'dni': alumno.dni,
        'fecha_nacimiento': alumno.fecha_nacimiento.strftime('%Y-%m-%d') if alumno.fecha_nacimiento else '',
        'sexo': alumno.sexo,
        'celular': alumno.celular,
        'email': alumno.email or '',
        'direccion': alumno.direccion or '',
        'institucion_id': alumno.institucion_id,
        'carrera_id': alumno.carrera_id,
        'area_interes': alumno.area_interes or '',
        'desea_estudiar': alumno.desea_estudiar,
        'solicita_info': alumno.solicita_info,
        'modalidad_contacto': alumno.modalidad_contacto or '',
        'fecha_visita': visita.fecha_visita.strftime('%Y-%m-%d') if visita else '',
        'hora_visita': visita.hora_visita.strftime('%H:%M') if visita else '',
        'promotor_id': visita.promotor_id if visita else '',
        'observaciones': visita.observaciones if visita else ''
    }

    return render_template('registro/editar.html',
        alumno=alumno, visita=visita, colegios=colegios,
        promotores=promotores, carreras=carreras, form=form)

@registro_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    alumno = Alumno.query.get_or_404(id)
    Visita.query.filter_by(alumno_id=alumno.id).delete()
    dni = alumno.dni
    db.session.delete(alumno)
    db.session.commit()
    registrar_auditoria(current_user.id, 'Eliminación de registro', 'Registro',
        f'Registro eliminado: Alumno {dni}')
    flash('Registro eliminado permanentemente.', 'success')
    return redirect(url_for('consulta.index'))

@registro_bp.route('/calcular-edad', methods=['GET'])
def calcular_edad_route():
    fecha = request.args.get('fecha_nacimiento', '')
    if fecha:
        try:
            fn = datetime.strptime(fecha, '%Y-%m-%d').date()
            return jsonify({'edad': calcular_edad(fn)})
        except:
            return jsonify({'edad': 0})
    return jsonify({'edad': 0})
