from app import create_app
from dotenv import load_dotenv
import os
import stat
import threading
from pathlib import Path

load_dotenv()

app = create_app()


def _fix_cloudflared_permissions():
    """
    En Linux/macOS, pycloudflared descarga el binario de cloudflared sin
    permiso de ejecución. Esta función lo detecta y lo corrige automáticamente
    para evitar el error [Errno 13] Permission denied.
    """
    try:
        import pycloudflared
        pkg_dir = Path(pycloudflared.__file__).parent
        for binary in pkg_dir.glob('cloudflared-*'):
            if binary.is_file():
                current = binary.stat().st_mode
                # Añade bit de ejecución para owner, group y others si falta
                if not (current & stat.S_IXUSR):
                    binary.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    except Exception:
        pass  # Si falla silenciosamente, el error real aparecerá en iniciar_tunel


def iniciar_tunel(port):
    try:
        _fix_cloudflared_permissions()
        import pycloudflared
        urls = pycloudflared.try_cloudflare(port=port, verbose=False)
        Path('logs').mkdir(exist_ok=True)
        with open('logs/tunel.txt', 'w') as f:
            f.write(urls.tunnel)
        print('=' * 60)
        print('TUNEL CLOUDFLARE ACTIVO (URL TEMPORAL)')
        print('  URL publica: ' + urls.tunnel)
        print('  Estadisticas: ' + urls.metrics)
        print('  Guardada en: logs/tunel.txt')
        print('  La URL expira al cerrar el servidor')
        print('=' * 60)
    except Exception as e:
        print('No se pudo iniciar el túnel de Cloudflare:', e)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    usar_tunel = os.environ.get('CLOUDFLARE_TUNNEL', '1') == '1'
    reloader = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    if usar_tunel and reloader:
        t = threading.Thread(target=iniciar_tunel, args=(port,), daemon=True)
        t.start()
    app.run(host='0.0.0.0', port=port, debug=True)
