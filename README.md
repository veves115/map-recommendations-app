# ExploreNow

Aplicación web fullstack de recomendaciones de lugares basada en un mapa interactivo, con sistema de amigos, chat en tiempo real y compartición de ubicación GPS.

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | FastAPI + Python 3.11 |
| ORM | SQLAlchemy 2.x + Alembic |
| Base de datos | PostgreSQL 16 |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Tiempo real | WebSockets nativos de FastAPI |
| Mapas (backend) | Google Maps Python SDK |
| Frontend | Vue 3.5 + TypeScript + Vite |
| Estado global | Pinia |
| Estilos | Tailwind CSS v4 |
| HTTP | Axios con interceptores JWT |
| Mapas (frontend) | Google Maps JS API (AdvancedMarkerElement) |
| APIs externas | Google Maps Platform + OpenWeatherMap |
| Contenedores | Docker + Docker Compose |

---

## Funcionalidades

- Autenticación con JWT (registro, login, cambio de contraseña, eliminación de cuenta)
- Mapa interactivo centrado en la ubicación GPS del usuario
- Recomendaciones personalizadas de lugares según preferencias del usuario
- Filtros por categoría (restaurantes, cafés, museos, parques, etc.)
- Detalles de lugares: rating, horarios, reseñas, teléfono, web, ruta
- Widget del tiempo en tiempo real (OpenWeatherMap)
- Selector de tipo de mapa (Auto / Calles / Satélite) con previews reales
- Sistema de amigos por código de invitación único
- Compartición de ubicación en tiempo real entre amigos
- Envío de emojis en tiempo real entre amigos
- Chat persistente con historial en base de datos
- Gestión de preferencias de lugares en el perfil

---

## Estructura del proyecto

```
map-recommendations-app/
├── backend/
│   ├── alembic/              # Migraciones de base de datos
│   ├── app/
│   │   ├── api/              # Routers FastAPI (auth, users, maps, preferences,
│   │   │                     #   locations, recommendations, messages, friendships)
│   │   ├── core/             # Config, database, security, deps
│   │   ├── models/           # Modelos SQLAlchemy
│   │   ├── schemas/          # Schemas Pydantic
│   │   ├── services/         # Lógica de negocio
│   │   └── websocket/        # Chat y presencia en tiempo real
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/              # Wrappers Axios por recurso
│   │   ├── components/       # ui/, map/, layout/, profile/
│   │   ├── composables/      # useChat, usePresence, useWeather, useUserSocket
│   │   ├── router/           # Vue Router con guard requiresAuth
│   │   ├── stores/           # Pinia (auth)
│   │   ├── types/            # Tipos TypeScript de la API
│   │   ├── utils/            # placeCategories, time, api-errors
│   │   └── views/            # HomeView, ProfileView, ChatView, FriendsView, ...
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
└── .env                      # Variables de entorno (no en git)
```

---

## Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Google Maps
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Base de datos
DATABASE_URL=postgresql://postgres:postgres@db:5432/mapapp

# JWT
SECRET_KEY=your_secret_key_here   # genera con: openssl rand -hex 32

# CORS (orígenes permitidos separados por coma)
CORS_ORIGINS=http://localhost:5173,http://localhost:5174

# Email (Resend)
RESEND_API_KEY=your_resend_api_key
FRONTEND_URL=http://localhost:5173
```

Crea también `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_MAPS_KEY=your_google_maps_api_key
VITE_OPENWEATHER_KEY=your_openweathermap_api_key
```

### Cómo obtener las API keys

- **Google Maps**: [console.cloud.google.com](https://console.cloud.google.com) — activa Maps JavaScript API y Places API
- **OpenWeatherMap**: [openweathermap.org/api](https://openweathermap.org/api) — plan gratuito suficiente
- **Resend**: [resend.com](https://resend.com) — para emails de recuperación de contraseña (plan gratuito)

---

## Despliegue con Docker (recomendado)

### Requisitos
- Docker Desktop instalado y en ejecución
- Archivo `.env` en la raíz con las variables descritas arriba

### Levantar el proyecto

```bash
git clone https://github.com/veves115/map-recommendations-app.git
cd map-recommendations-app

# Crear el .env con tus variables (ver sección anterior)

docker compose up --build
```

Servicios disponibles tras el arranque:

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Docs Swagger | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 (usuario: `postgres`, contraseña: `postgres`, db: `mapapp`) |

### Parar el proyecto

```bash
docker compose down
```

### Parar y eliminar datos (reset completo)

```bash
docker compose down -v
```

---

## Migraciones de base de datos

Las migraciones se aplican automáticamente al arrancar con Docker. Para ejecutarlas manualmente:

```bash
# Dentro del contenedor
docker compose exec backend alembic upgrade head

# Crear una nueva migración
docker compose exec backend alembic revision --autogenerate -m "descripción"

# Revertir última migración
docker compose exec backend alembic downgrade -1
```

---

## Desarrollo sin Docker

### Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

> En PowerShell puede ser necesario ejecutar primero:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

### Comandos útiles del frontend

```bash
npm run type-check   # Verificar tipos TypeScript
npm run lint         # Linter
npm run build        # Build de producción
```

---

## API Endpoints

### Autenticación `/api/v1/auth`

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| POST | `/register` | No | Crear cuenta |
| POST | `/login` | No | Obtener token JWT |
| GET | `/me` | Sí | Datos del usuario actual |
| POST | `/change-password` | Sí | Cambiar contraseña |
| POST | `/forgot-password` | No | Solicitar reset por email |
| POST | `/reset-password` | No | Resetear contraseña con token |

### Usuarios `/api/v1/users`

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| GET | `/` | Sí | Listar usuarios |
| GET | `/{id}` | Sí | Obtener usuario por ID |
| PATCH | `/me` | Sí | Editar perfil |
| DELETE | `/me` | Sí | Eliminar cuenta (soft delete) |

### Mapas `/api/v1/maps`

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| GET | `/nearby` | Sí | Lugares cercanos |
| GET | `/place/{place_id}` | Sí | Detalles de un lugar |
| GET | `/geocode` | Sí | Geocodificación de dirección |

### Preferencias `/api/v1/preferences`

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| GET | `/` | Sí | Listar preferencias del usuario |
| POST | `/` | Sí | Añadir preferencia |
| DELETE | `/{id}` | Sí | Eliminar preferencia |

### Recomendaciones `/api/v1/recommendations`

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| GET | `/` | Sí | Lugares recomendados según preferencias y ubicación |

### Mensajes `/api/v1/messages`

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| GET | `/{user_id}` | Sí | Historial de conversación |
| POST | `/` | Sí | Enviar mensaje |
| PATCH | `/{id}/read` | Sí | Marcar como leído |
| DELETE | `/{user_id}` | Sí | Borrar conversación completa |

### Amistades `/api/v1/friendships`

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| GET | `/` | Sí | Listar amigos |
| POST | `/invites` | Sí | Crear invitación |
| GET | `/invites` | Sí | Listar invitaciones propias |
| GET | `/invites/received` | Sí | Invitaciones recibidas |
| POST | `/invites/accept` | Sí | Aceptar invitación por código |
| DELETE | `/invites/{id}` | Sí | Eliminar invitación |
| DELETE | `/{friend_id}` | Sí | Eliminar amigo |

### WebSockets

| Protocolo | Endpoint | Descripción |
|-----------|----------|-------------|
| WS | `/ws/chat/{room_id}?token=...` | Chat en tiempo real |
| WS | `/ws/presence?token=...` | Ubicación en tiempo real |
| WS | `/ws/user?token=...` | Eventos de usuario (emojis) |

---

## Autor

Proyecto desarrollado por [Pablo Ares](https://github.com/veves115) como Proyecto Intermodular de 2º DAW.
