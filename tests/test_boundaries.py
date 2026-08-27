import os
import pytest

def test_import_linter_contracts_exist():
    """Verifica que setup.cfg define los contratos de fronteras."""
    cfg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "setup.cfg")
    assert os.path.exists(cfg_path), "setup.cfg no existe"
    with open(cfg_path) as f:
        content = f.read()
    assert "layers-boundaries" in content
    assert "forbid-domain-imports-app" in content
    assert "forbid-cross-consulta-registro" in content
    assert "forbid-registro-auditoria" in content
    assert "root_package = app" in content

def test_import_linter_passes():
    import subprocess, sys
    result = subprocess.run([sys.executable, "-m", "importlinter.cli", "lint-imports"] if False else ["venv/bin/lint-imports"], capture_output=True, text=True)
    # fallback to lint-imports binary
    if result.returncode != 0:
        # try venv path
        import subprocess as sp
        result = sp.run(["venv/bin/lint-imports"], capture_output=True, text=True)
    assert result.returncode == 0, f"lint-imports falló:\n{result.stdout}\n{result.stderr}"

def test_publish_without_subscriber_no_falla():
    from app.shared.events import bus, AlumnoRegistrado
    bus.clear()
    # no suscriptor
    evt = AlumnoRegistrado(alumno_id=1, dni="71234001", nombres="A", apellidos="B", actor_id=1)
    bus.publish(evt)  # no debe lanzar
    bus.clear()

def test_publish_entrega_en_orden_y_aisla_errores():
    from app.shared.events import bus, AlumnoRegistrado
    bus.clear()
    order = []
    def h1(e): order.append("h1")
    def h_err(e): raise RuntimeError("fail")
    def h2(e): order.append("h2")
    bus.subscribe(AlumnoRegistrado, h1)
    bus.subscribe(AlumnoRegistrado, h_err)
    bus.subscribe(AlumnoRegistrado, h2)
    evt = AlumnoRegistrado(alumno_id=1, dni="71234001", nombres="A", apellidos="B", actor_id=1)
    bus.publish(evt)
    assert order == ["h1", "h2"], f"orden incorrecto: {order}"
    bus.clear()

def test_uow_rollback_descarta_eventos():
    os.environ["FLASK_ENV"] = "testing"
    from app import create_app
    from app.shared.db import db
    from app.shared.unit_of_work import UnitOfWork
    from app.shared.events import bus, AlumnoRegistrado
    app = create_app()
    with app.app_context():
        db.create_all()
        bus.clear()
        captured = []
        def cap(e): captured.append(e)
        bus.subscribe(AlumnoRegistrado, cap)
        try:
            with UnitOfWork() as uow:
                uow.publish(AlumnoRegistrado(alumno_id=99, dni="00000001", nombres="X", apellidos="Y", actor_id=1))
                raise ValueError("boom")
        except ValueError:
            pass
        assert len(captured) == 0, "rollback debe descartar eventos"
        bus.clear()

def test_uow_commit_despacha_eventos():
    os.environ["FLASK_ENV"] = "testing"
    from app import create_app
    from app.shared.db import db
    from app.shared.unit_of_work import UnitOfWork
    from app.shared.events import bus, AlumnoRegistrado
    app = create_app()
    with app.app_context():
        db.create_all()
        bus.clear()
        captured = []
        def cap(e): captured.append(e)
        bus.subscribe(AlumnoRegistrado, cap)
        with UnitOfWork() as uow:
            uow.publish(AlumnoRegistrado(alumno_id=100, dni="00000002", nombres="X", apellidos="Y", actor_id=1))
        assert len(captured) == 1, "commit debe despachar"
        assert captured[0].dni == "00000002"
        bus.clear()

def test_eventos_tienen_occurred_at_y_serializable():
    from app.shared.events import AlumnoRegistrado
    evt = AlumnoRegistrado(alumno_id=1, dni="71234001", nombres="A", apellidos="B", actor_id=1)
    assert evt.occurred_at is not None
    d = evt.to_dict()
    assert d["event_type"] == "AlumnoRegistrado"
    assert d["dni"] == "71234001"

def test_evento_falla_sin_campo_requerido():
    from app.shared.events import AlumnoRegistrado
    with pytest.raises(TypeError):
        AlumnoRegistrado(alumno_id=1, nombres="A", apellidos="B")  # falta dni
