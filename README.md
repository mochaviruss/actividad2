# Actividad 2 - Bot IA con memoria

Bot de Telegram que usa inteligencia artificial para responder mensajes y guarda el historial de conversacion en una base de datos PostgreSQL.

## Como funciona

El bot recibe mensajes por Telegram, los guarda en la base de datos junto con el historial previo, y los manda a un modelo de lenguaje (LLaMA via Groq) para generar una respuesta. De esta forma el bot recuerda lo que se habló antes en la conversacion.

## Stack usado

| Componente | Herramienta |
|---|---|
| Lenguaje | Python 3.11 |
| Bot | Telegram |
| Modelo IA | LLaMA 3 (Groq) |
| Base de datos | PostgreSQL (Supabase) |
| Contenedor | Docker |
| CI/CD | GitHub Actions |
| Deploy | Render |

## Estructura

```
actividad2/
├── app/
│   └── main.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── requerimientos.txt
├── .env.example
├── .gitignore
└── README.md
```

## Configuracion

Primero clonar el repo e instalar dependencias:

```bash
git clone https://github.com/mochaviruss/actividad2.git
cd actividad2
pip install -r requerimientos.txt
```

Crear el archivo `.env` basado en `.env.example` y completar las variables:

```
TELEGRAM_TOKEN=token del bot (se obtiene con @BotFather en Telegram)
GROQ_API_KEY=api key de groq.com
DATABASE_URL=url de conexion de supabase
```

## Correr localmente

```bash
python app/main.py
```

O con Docker:

```bash
docker build -t actividad2 .
docker run --env-file .env actividad2
```

## Despliegue en Render

1. Crear cuenta en render.com
2. New > Web Service > conectar el repo
3. Environment: Docker
4. Agregar las variables de entorno en el panel
5. Deploy

El CI/CD esta configurado para que cada push a master ejecute los tests y luego dispare el deploy automaticamente en Render usando un webhook.

## Comandos del bot

| Comando | Funcion |
|---|---|
| /start | Inicia la conversacion |
| /clear | Borra el historial |
| cualquier texto | Responde con IA |

## Variables de entorno

Las credenciales nunca se suben al repositorio. El archivo `.env` esta en el `.gitignore`. Para produccion las variables se configuran directamente en el panel de Render.
