# Plan de Desarrollo — Map Recommendations App

Aplicación fullstack de recomendaciones de lugares en tiempo real con mapa interactivo, chat entre usuarios y motor de recomendaciones personalizadas.

---

## Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| **Backend** | FastAPI + Python 3.10+ |
| **Frontend** | Vue 3 + TypeScript + Vite |
| **Base de datos** | PostgreSQL (dev y prod) |
| **ORM** | SQLAlchemy + Alembic |
| **Mapas** | Google Maps JS API (frontend) + Google Maps Python API (backend) |
| **Tiempo real** | WebSockets |
| **Contenedores** | Docker + Docker Compose |
| **Estilos** | Tailwind CSS |
| **Estado global** | Pinia |
| **HTTP Client** | Axios |

---

## Estructura del Monorepo

```
map-recommendations-app/
├── backend/                    # FastAPI (código actual en raíz → mover aquí)
│   ├── app/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── frontend/                   # Vue 3 + TypeScript (por crear)
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── .env
├── docker-compose.yml          # Orquestación local
├── docker-compose.prod.yml     # Orquestación producción
└── PLAN.md
```

---

## Fase 1 — Backend: Completar API REST

### 1.1 Endpoints ya implementados
- [x] `POST /api/v1/auth/register` — Registro de usuario
- [x] `POST /api/v1/auth/login` — Login con JWT
- [x] `GET /api/v1/auth/me` — Usuario autenticado
- [x] `GET /api/v1/users/` — Listar usuarios (paginado)
- [x] `GET /api/v1/users/{user_id}` — Obtener usuario por ID

### 1.2 Maps endpoints (pendiente)
- [ ] `GET /api/v1/maps/nearby` — Lugares cercanos (lat, lng, radius, type)
- [ ] `GET /api/v1/maps/place/{place_id}` — Detalle de un lugar
- [ ] `GET /api/v1/maps/geocode` — Dirección → coordenadas

### 1.3 Preferences endpoints (pendiente)
- [ ] `GET /api/v1/preferences/` — Listar preferencias del usuario
- [ ] `POST /api/v1/preferences/` — Añadir preferencia
- [ ] `PUT /api/v1/preferences/{id}` — Actualizar preferencia
- [ ] `DELETE /api/v1/preferences/{id}` — Eliminar preferencia

### 1.4 Locations endpoints (pendiente)
- [ ] `POST /api/v1/locations/` — Registrar ubicación del usuario
- [ ] `GET /api/v1/locations/me` — Historial de ubicaciones propias
- [ ] `GET /api/v1/locations/latest` — Última ubicación del usuario

### 1.5 Recommendations engine (pendiente)
- [ ] `GET /api/v1/recommendations/` — Recomendaciones personalizadas
  - Lógica: cruzar preferencias del usuario con lugares cercanos (Google Maps)
  - Ordenar por rating, distancia y match con categorías preferidas
  - Filtros opcionales: radio, categoría, precio

### 1.6 Messages / Chat REST (pendiente)
- [ ] `GET /api/v1/messages/{user_id}` — Historial de mensajes con un usuario
- [ ] `POST /api/v1/messages/` — Enviar mensaje (fallback REST)
- [ ] `PATCH /api/v1/messages/{id}/read` — Marcar como leído

### 1.7 WebSocket Chat (pendiente)
- [ ] `WS /ws/chat/{room_id}` — Conexión WebSocket autenticada
  - Autenticación por query param `?token=<jwt>`
  - Broadcast a sala o usuario específico
  - Persistencia de mensajes en BD

### 1.8 Mejoras de infraestructura backend (pendiente)
- [ ] Migrar de SQLite a PostgreSQL (apuntando al contenedor Docker local)
- [ ] Añadir Alembic para control de migraciones de BD
- [ ] Paginación consistente en todos los endpoints de lista
- [ ] Rate limiting básico
- [ ] Logging estructurado

---

## Fase 2 — Frontend: Vue 3 + TypeScript

### 2.1 Setup inicial
- [ ] Crear proyecto con Vite: `npm create vue@latest frontend`
  - TypeScript: sí
  - Vue Router: sí
  - Pinia: sí
  - ESLint + Prettier: sí
- [ ] Instalar dependencias:
  - `axios` — HTTP client
  - `@googlemaps/js-api-loader` — Google Maps JS
  - `tailwindcss` + `@headlessui/vue` — UI
  - `@vueuse/core` — Composables de utilidad
  - WebSocket nativo — Chat en tiempo real

### 2.2 Estructura del frontend

```
frontend/src/
├── api/                    # Llamadas HTTP a la API
│   ├── auth.ts
│   ├── maps.ts
│   ├── preferences.ts
│   ├── recommendations.ts
│   └── messages.ts
├── components/
│   ├── map/
│   │   ├── MapContainer.vue       # Google Maps canvas
│   │   ├── PlaceMarker.vue        # Marcador de lugar
│   │   └── PlaceInfoCard.vue      # Card de detalle al click
│   ├── auth/
│   │   ├── LoginForm.vue
│   │   └── RegisterForm.vue
│   ├── recommendations/
│   │   ├── RecommendationList.vue
│   │   └── RecommendationCard.vue
│   ├── preferences/
│   │   └── PreferencesManager.vue
│   ├── chat/
│   │   ├── ChatWindow.vue
│   │   ├── MessageBubble.vue
│   │   └── UserList.vue
│   └── ui/                        # Componentes genéricos (Button, Input, etc.)
├── composables/
│   ├── useAuth.ts
│   ├── useMap.ts
│   ├── useGeolocation.ts
│   ├── useRecommendations.ts
│   └── useChat.ts
├── stores/
│   ├── auth.ts           # Usuario autenticado, token
│   ├── map.ts            # Estado del mapa, lugares
│   ├── recommendations.ts
│   └── chat.ts
├── views/
│   ├── HomeView.vue       # Mapa principal + recomendaciones
│   ├── LoginView.vue
│   ├── RegisterView.vue
│   ├── ProfileView.vue    # Preferencias del usuario
│   └── ChatView.vue
├── router/
│   └── index.ts
└── types/
    ├── api.ts             # Tipos de respuestas de la API
    └── maps.ts            # Tipos de Google Maps
```

### 2.3 Vistas y funcionalidades

#### HomeView (Vista principal)
- Mapa de Google Maps a pantalla completa
- Botón "Usar mi ubicación" → geolocalización del navegador
- Panel lateral con lista de recomendaciones
- Marcadores en el mapa por cada lugar recomendado
- Click en marcador → PlaceInfoCard con detalle
- Filtros: categoría, radio, precio

#### Auth (Login / Register)
- Formularios de login y registro
- Guardar JWT en localStorage via Pinia
- Guards de rutas (solo acceso autenticado al mapa)
- Redirect tras login → HomeView

#### ProfileView
- Ver y editar preferencias (categorías de interés)
- Historial de ubicaciones visitadas
- Configuración de cuenta básica

#### ChatView
- Lista de usuarios disponibles
- Ventana de chat con un usuario
- Conexión WebSocket en tiempo real
- Compartir lugares desde el mapa al chat

### 2.4 Autenticación en el frontend
- Interceptor Axios: adjuntar `Authorization: Bearer <token>` en todas las peticiones
- Interceptor de respuesta: si 401 → limpiar sesión y redirigir a login
- Store de auth: `user`, `token`, `isAuthenticated`, `login()`, `logout()`

---

## Fase 3 — Docker: Entorno Local

### 3.1 Dockerfile del backend

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 3.2 Dockerfile del frontend

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
```

### 3.3 docker-compose.yml (desarrollo local)

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/mapapp
      - GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_GOOGLE_MAPS_KEY=${GOOGLE_MAPS_API_KEY}
    depends_on:
      - backend

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mapapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### 3.4 Tareas Docker pendientes
- [ ] Reorganizar monorepo: mover código actual al subdirectorio `backend/`
- [ ] Crear `backend/Dockerfile`
- [ ] Crear `frontend/Dockerfile`
- [ ] Crear `docker-compose.yml` en raíz
- [ ] Crear `.env.example` con todas las variables necesarias
- [ ] Migrar backend de SQLite → PostgreSQL (apuntando al contenedor `db`)
- [ ] Añadir Alembic y ejecutar migración inicial
- [ ] Añadir `Adminer` como servicio opcional para inspeccionar la BD en local

---

## Fase 4 — Despliegue (Producción)

### 4.1 Infraestructura objetivo
| Servicio | Plataforma sugerida |
|----------|---------------------|
| Backend API | Railway / Render / VPS (DigitalOcean) |
| Frontend | Vercel / Netlify / Nginx en VPS |
| Base de datos | Railway PostgreSQL / Supabase / RDS |

### 4.2 Dockerfile.prod del frontend (multistage)

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

# Serve stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

### 4.3 nginx.conf (reverse proxy en prod)

```nginx
server {
  listen 80;

  location /api {
    proxy_pass http://backend:8000;
  }

  location /ws {
    proxy_pass http://backend:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
  }

  location / {
    root /usr/share/nginx/html;
    try_files $uri $uri/ /index.html;
  }
}
```

### 4.4 Variables de entorno en producción
- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — clave secreta JWT (generada con `openssl rand -hex 32`)
- `GOOGLE_MAPS_API_KEY` — restringida por dominio en Google Cloud Console
- `VITE_API_URL` — URL pública del backend
- `VITE_GOOGLE_MAPS_KEY` — clave pública de Maps JS API

### 4.5 Tareas de despliegue
- [ ] Elegir plataforma de hosting
- [ ] Configurar dominio y HTTPS (Let's Encrypt / Certbot)
- [ ] Crear `Dockerfile.prod` para frontend (nginx multistage)
- [ ] Crear `nginx.conf` con reverse proxy y soporte WebSocket
- [ ] Configurar CI/CD (GitHub Actions: test → build → deploy)
- [ ] Configurar secrets en el repositorio

---

## Orden de Implementación Recomendado

```
[AHORA]     Fase 3.4 → Docker local + migración a PostgreSQL + Alembic
            Reorganizar monorepo (mover código a backend/)

[SIGUIENTE] Fase 1.2 → Maps endpoints
            Fase 1.3 → Preferences endpoints
            Fase 1.4 → Locations endpoints
            Fase 1.5 → Recommendations engine

[LUEGO]     Fase 2.1 → Setup frontend Vue
            Fase 2.2–2.4 → Implementar vistas y composables

[FINAL DEV] Fase 1.7 → WebSocket chat
            Fase 2.3 (ChatView) → Chat en frontend

[DEPLOY]    Fase 4 → Despliegue en producción
```

---

## Estado Global del Proyecto

| Módulo | Backend | Frontend | Docker | Deploy |
|--------|---------|----------|--------|--------|
| Autenticación | ✅ Completo | ⬜ Pendiente | ⬜ | ⬜ |
| Usuarios | ✅ Completo | ⬜ Pendiente | ⬜ | ⬜ |
| Maps API | 🔄 En progreso | ⬜ Pendiente | ⬜ | ⬜ |
| Preferencias | 🔄 En progreso | ⬜ Pendiente | ⬜ | ⬜ |
| Ubicaciones | ⬜ Pendiente | ⬜ Pendiente | ⬜ | ⬜ |
| Recomendaciones | ⬜ Pendiente | ⬜ Pendiente | ⬜ | ⬜ |
| Chat / WS | ⬜ Pendiente | ⬜ Pendiente | ⬜ | ⬜ |
| Docker local | ⬜ Pendiente | — | ⬜ | — |
| Despliegue | — | — | — | ⬜ |
