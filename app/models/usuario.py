# shim: re-export desde el módulo identidad + user_loader
from app.modules.identidad.domain.usuario import Usuario  # noqa: F401
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    u = Usuario.query.get(int(user_id))
    if u and u.estado and not u.is_bloqueado() and not u.eliminado:
        return u
    return None
