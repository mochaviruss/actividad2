# Bot IA con Memoria en Telegram

Bot de Telegram con IA que recuerda el contexto de la conversación usando PostgreSQL.

## Stack técnico

| Componente | Herramienta | Justificación |
|---|---|---|
| Lenguaje | Python 3.11 | Versátil, ideal para IA y automatización |
| IA | OpenAI GPT-4o-mini | API sencilla, bajo costo |
| Canal | Telegram Bot | Accesible desde celular sin frontend |
| Base de datos | PostgreSQL (Supabase) | Relacional, gratuito, guarda historial |
| Contenerización | Docker | Entorno reproducible |
| CI/CD | GitHub Actions | Automatiza tests y despliegue |
| Deploy | Render | Gratuito, conecta directo con GitHub |

## Estructura del proyecto

```
ai-bot/
├── app/
│   └── main.py          # Lógica del bot
├── .github/
│   └── workflows/
│       └── ci.yml       # Pipeline CI/CD
├── Dockerfile           # Contenerización
├── requirements.txt     # Dependencias Python
├── .env.example         # Variables de entorno (sin valores reales)
├── .gitignore
└── README.md
```

## Configuración paso a paso

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/ai-bot.git
cd ai-bot
```

### 2. Crear el bot en Telegram

1. Abre Telegram y busca `@BotFather`
2. Escribe `/newbot` y sigue las instrucciones
3. Guarda el token que te entrega

### 3. Crear la base de datos en Supabase

1. Crea una cuenta en [supabase.com](https://supabase.com)
2. Crea un proyecto nuevo
3. Ve a **Settings > Database** y copia la `Connection String (URI)`

### 4. Obtener API Key de OpenAI

1. Ve a [platform.openai.com](https://platform.openai.com)
2. Crea una API key en **API Keys**

### 5. Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env con tus valores reales
```

### 6. Ejecutar localmente con Docker

```bash
docker build -t ai-bot .
docker run --env-file .env ai-bot
```

### 7. Desplegar en Render

1. Crea cuenta en [render.com](https://render.com)
2. **New > Web Service** > conecta tu repo de GitHub
3. Configuración:
   - **Environment**: Docker
   - **Branch**: main
4. Agrega las variables de entorno en el panel de Render
5. Copia el **Deploy Hook URL** y agrégalo como secret en GitHub:
   - GitHub repo > **Settings > Secrets > New secret**
   - Nombre: `RENDER_DEPLOY_HOOK`

### 8. Activar CI/CD

Cada vez que hagas `git push` a `main`:
- GitHub Actions ejecuta los tests automáticamente
- Si pasan, dispara el deploy en Render

## Uso del bot

| Comando | Función |
|---|---|
| `/start` | Saluda e inicia la conversación |
| `/clear` | Borra el historial del chat |
| Cualquier texto | Responde con IA recordando el contexto |

## Variables de entorno

| Variable | Descripción |
|---|---|
| `TELEGRAM_TOKEN` | Token del bot (de @BotFather) |
| `OPENAI_API_KEY` | API Key de OpenAI |
| `DATABASE_URL` | URL de conexión PostgreSQL |

> **Seguridad**: Nunca subas el archivo `.env` al repositorio. Está en `.gitignore`.

## Decisiones técnicas

- Se eligió **Telegram** como canal porque no requiere construir un frontend y funciona perfectamente desde celular.
- Se usa **GPT-4o-mini** por su bajo costo manteniendo buena calidad.
- El historial se limita a los últimos **10 mensajes** para no exceder el contexto del modelo.
- **Supabase** provee PostgreSQL gratuito compatible con el stack propuesto en la actividad.
