# SISTEMA DE GESTIÓN DE REGISTRO DE VISITAS (SGRV)

## IESTP "Paiján"

Sistema web para registrar y gestionar las visitas realizadas por promotores institucionales a colegios de 5to de secundaria, con el objetivo de generar una base de datos para analizar, segmentar y predecir potenciales estudiantes interesados en estudiar en el Instituto de Educación Superior Tecnológico Público "Paiján".

---

## Características

- **Dashboard interactivo** con gráficos estadísticos y métricas en tiempo real
- **Registro de visitas** con formulario inteligente y validaciones
- **Búsqueda avanzada** con filtros múltiples
- **Gestión de usuarios** con 3 roles (Administrador, Supervisor, Operador)
- **Auditoría completa** de todas las acciones del sistema
- **Reportes exportables** en CSV y Excel
- **Modo oscuro/claro** con persistencia de preferencia
- **Diseño responsive** adaptado a dispositivos móviles
- **Seguridad**: contraseñas hasheadas, sesiones protegidas, CSRF, validación de intentos fallidos

---

## Tecnologías

### Backend
- Python 3.10+
- Flask 3.0
- SQLAlchemy 2.0
- Flask-Login
- Flask-WTF (CSRF)
- Flask-Migrate

### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5.3
- Chart.js 4.4
- Bootstrap Icons

### Base de Datos
- SQLite (desarrollo)
- PostgreSQL (producción)

### Control de Versiones
- Git
- GitHub

---

## Estructura del Proyecto

```
gestion_registro_visitas/
├── app/
│   ├── controllers/     # Controladores (blueprints)
│   ├── models/          # Modelos SQLAlchemy
│   ├── views/           # Vistas (reservado)
│   ├── templates/       # Plantillas HTML
│   │   ├── auth/        # Login, recuperar contraseña
│   │   ├── dashboard/   # Dashboard principal
│   │   ├── registro/    # Registro y edición de visitas
│   │   ├── consulta/    # Búsqueda y detalle
│   │   ├── usuarios/    # Gestión de usuarios
│   │   ├── auditoria/   # Registro de auditoría
│   │   ├── reportes/    # Generación de reportes
│   │   ├── errors/      # Páginas de error
│   │   └── partials/    # Componentes reutilizables
│   ├── static/
│   │   ├── css/         # Estilos personalizados
│   │   ├── js/          # Scripts del frontend
│   │   └── img/         # Imágenes
│   ├── services/        # Lógica de negocio
│   ├── utils/           # Utilidades y seed data
│   └── config.py        # Configuración de la aplicación
├── database/            # Archivos de base de datos
├── migrations/          # Migraciones de base de datos
├── requirements.txt     # Dependencias del proyecto
├── run.py               # Punto de entrada
├── .gitignore           # Archivos ignorados por Git
└── README.md            # Este archivo
```

---

## Instalación

### 1. Requisitos previos

- Python 3.10 o superior
- Git
- Navegador web moderno

### 2. Clonar el repositorio

```bash
git clone https://github.com/azconsultingperu/gestion-registro-visitas.git
cd gestion-registro-visitas
```

### 3. Crear entorno virtual

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación

```bash
python run.py
```

La aplicación se iniciará en: `http://localhost:5000`

---

## Usuarios por defecto

| Usuario    | Contraseña | Rol            |
|------------|-----------|----------------|
| admin      | admin123  | Administrador  |
| supervisor | super123  | Supervisor     |
| operador   | opera123  | Operador       |

> **Nota**: Cambie estas credenciales inmediatamente después del primer inicio de sesión.

---

## Roles y Permisos

### Administrador
- Acceso total al sistema
- Gestión de usuarios
- Gestión de auditoría
- Gestión del sistema

### Supervisor
- Registrar visitas
- Consultar registros
- Editar registros
- Generar reportes

### Operador
- Registrar visitas
- Consultar registros

---

## Módulos del Sistema

### 1. Login
- Autenticación por DNI y contraseña
- Mostrar/ocultar contraseña
- Recordar sesión
- Recuperación de contraseña
- Bloqueo por intentos fallidos

### 2. Dashboard
- Métricas principales (totales)
- Gráficos interactivos (Chart.js)
- Alumnos por colegio, distrito, sexo
- Edad promedio
- Registros del día, semana, mes
- Ranking de colegios visitados
- Proyección de postulantes

### 3. Registrar
- Formulario completo de registro
- Validación de DNI único
- Cálculo automático de edad
- Fecha y hora automática
- Verificación de duplicados

### 4. Consultar
- Búsqueda por múltiples criterios
- Filtros combinados
- Paginación de resultados
- Ver detalle, editar, eliminar

### 5. Usuarios
- CRUD completo de usuarios
- Asignación de roles
- Control de estado (activo/inactivo)

### 6. Auditoría
- Registro automático de acciones
- Filtros por usuario, acción, módulo, fecha
- Seguimiento de IP y user-agent

### 7. Reportes
- Exportación a CSV
- Exportación a Excel
- Reportes de alumnos, visitas, colegios, carreras

---

## Base de Datos

### Tablas principales

- `usuarios` - Usuarios del sistema
- `roles` - Roles y permisos
- `alumnos` - Alumnos registrados
- `instituciones_educativas` - Colegios
- `visitas` - Registro de visitas
- `promotores` - Promotores institucionales
- `auditorias` - Registro de auditoría
- `sesiones` - Sesiones de usuario
- `carreras` - Carreras profesionales
- `reportes` - Reportes generados
- `dashboard_estadisticas` - Estadísticas del dashboard

---

## Preparado para Machine Learning

El sistema incluye tablas y estructura de datos preparada para implementar modelos predictivos:

- Regresión Logística
- Random Forest
- Decision Tree
- KNN
- XGBoost

### Indicadores predictivos disponibles:
- Probabilidad de postulación
- Probabilidad de matrícula
- Segmentación de alumnos
- Ranking de captación

---

## Despliegue en Producción

### Configuración para PostgreSQL

1. Instalar PostgreSQL
2. Crear base de datos:
```sql
CREATE DATABASE gestion_visitas;
```
3. Configurar variables de entorno:
```bash
set DATABASE_URL=postgresql://usuario:password@localhost:5432/gestion_visitas
```

### Servidor de producción

```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

---

## Licencia

Este proyecto es propiedad del Instituto de Educación Superior Tecnológico Público "Paiján".

---

## Contacto

**Desarrollado por:** azconsultingperu
**GitHub:** [https://github.com/azconsultingperu](https://github.com/azconsultingperu)
**Repositorio:** [https://github.com/azconsultingperu/gestion-registro-visitas](https://github.com/azconsultingperu/gestion-registro-visitas)
