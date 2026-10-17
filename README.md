# API de Tareas con FastAPI

API REST desarrollada con Python y FastAPI para gestionar tareas mediante operaciones CRUD.

## Tecnologías utilizadas

- Python
- FastAPI
- Pydantic
- Postman
- Git y GitHub

## Funcionalidades

- **GET** `/tareas` — Obtener todas las tareas.
- **POST** `/tareas` — Crear una tarea.
- **PUT** `/tareas/{tarea_id}` — Actualizar una tarea completa.
- **PATCH** `/tareas/{tarea_id}` — Actualizar campos específicos.
- **DELETE** `/tareas/{tarea_id}` — Eliminar una tarea.

## Validaciones

- Validación de datos mediante Pydantic.
- Prevención de IDs duplicados.
- Manejo de errores HTTP.
- Validación de prioridades: alta, media y baja.

## Ejecución local

Instala las dependencias:

```bash
pip install fastapi uvicorn
```

Inicia el servidor:

```bash
uvicorn main:app --reload
```

Consulta la documentación interactiva en:

http://127.0.0.1:8000/docs

## Almacenamiento

Actualmente, las tareas se almacenan en una lista en memoria. Los datos se pierden al reiniciar el servidor.

## Próximas mejoras

- Integración con PostgreSQL.
- Persistencia mediante SQLAlchemy.
- Generación automática de identificadores.
