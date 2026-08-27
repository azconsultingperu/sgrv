"""Tests de usuarios: unicidad de DNI y soft-delete."""
from app import db
from app.models.usuario import Usuario


def test_crear_usuario_dni_duplicado_rechazado(auth_client, app):
    with app.app_context():
        u = Usuario(dni='71444100', nombres='EXISTENTE', apellidos='USER',
                    username='71444100', email='existe@iestp.edu.pe', rol_id=3)
        u.set_password('Clave1234')
        db.session.add(u)
        db.session.commit()

    r = auth_client.post('/usuarios/crear', data={
        'dni': '71444100', 'nombres': 'DUP', 'apellidos': 'USER',
        'password': 'Clave1234', 'email': 'dup@iestp.edu.pe', 'rol_id': '3',
    }, follow_redirects=True)
    assert 'ya está registrado' in r.get_data(as_text=True)


def test_lista_usuarios_no_muestra_eliminados(auth_client, app):
    with app.app_context():
        u = Usuario(dni='71444123', nombres='ELIM', apellidos='PROBADO',
                    username='71444123', email='elim@iestp.edu.pe', rol_id=3)
        u.set_password('Clave1234')
        db.session.add(u)
        db.session.commit()
        uid = u.id

    html_antes = auth_client.get('/usuarios/').get_data(as_text=True)
    assert '71444123' in html_antes

    with app.app_context():
        u = db.session.get(Usuario, uid)
        u.eliminado = True
        db.session.commit()

    html_despues = auth_client.get('/usuarios/').get_data(as_text=True)
    assert '71444123' not in html_despues
