# 🔔 Price Alert Bot

Bot que **vigila precios de productos** (por ejemplo, en Amazon), guarda un historial de precios en SQLite y envía una **alerta por Telegram** cuando el precio cae por debajo de un objetivo definido por el usuario.

Expone una API REST (FastAPI) para añadir, listar y eliminar productos a vigilar, y un scheduler en segundo plano que revisa los precios periódicamente.

---

## ✨ Features

- 📦 **API REST** para gestionar productos a vigilar (crear, listar, eliminar)
- ⏱️ **Scheduler automático** (APScheduler) que revisa precios cada 6 horas
- 🕷️ **Scraper** (BeautifulSoup) que extrae el precio actual de la página del producto
- 📈 **Historial de precios** persistido en SQLite (`price_history`)
- 📲 **Notificaciones por Telegram** con nombre del producto, precio y enlace, en cuanto se alcanza el precio objetivo

---

## 🧱 Stack técnico

| Componente      | Tecnología                         |
|-----------------|-------------------------------------|
| API             | FastAPI + Uvicorn                  |
| Base de datos   | SQLite + SQLAlchemy                |
| Scraping        | requests + BeautifulSoup4          |
| Programación de tareas | APScheduler (BackgroundScheduler) |
| Notificaciones  | python-telegram-bot                |
| Validación      | Pydantic                           |

---

## 📁 Estructura del proyecto

```
price-alert-bot/
├── main.py          # API FastAPI: endpoints de productos
├── models.py        # Modelos SQLAlchemy (Product, PriceHistory)
├── database.py      # Configuración de la conexión a SQLite
├── scraper.py        # Extracción del precio desde la URL del producto
├── scheduler.py      # Job periódico que revisa precios y dispara alertas
├── bot.py            # Envío de mensajes por Telegram
├── requirements.txt
├── prices.db          # Base de datos SQLite (se genera al ejecutar)
└── .gitignore
```

---

## ⚙️ Instalación

### 1. Clonar y crear entorno virtual

```bash
git clone <url-del-repo>
cd price-alert-bot
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 2. Instalar dependencias

> ⚠️ El `requirements.txt` actual incluye muchas librerías que **no usa este proyecto** (parece un volcado completo de un entorno con `torch`, `selenium`, `pygame`, librerías de trading, etc.). Lo recomendable es instalar solo lo necesario:

```bash
pip install fastapi uvicorn sqlalchemy pydantic apscheduler requests beautifulsoup4 python-telegram-bot python-dotenv
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
TELEGRAM_TOKEN=tu_token_de_telegram
```

> 🔒 **Importante:** actualmente `bot.py` tiene el token de Telegram **hardcodeado** en el código. Esto es un riesgo de seguridad grave si el repo se sube a GitHub o se comparte. Reemplázalo por:
>
> ```python
> import os
> from dotenv import load_dotenv
>
> load_dotenv()
> TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
> ```
>
> Y si este token ya estuvo expuesto en algún repositorio público, chat o conversación, **revócalo en @BotFather (`/revoke`) y genera uno nuevo** antes de seguir usándolo.

### 4. Ejecutar el servidor

```bash
uvicorn main:app --reload
```

La API quedará disponible en `http://localhost:8000`. Al arrancar, `main.py` crea las tablas en SQLite (si no existen) y lanza el scheduler en segundo plano.

---

## 📡 Endpoints de la API

### Añadir producto a vigilar

```http
POST /products
```

```json
{
  "url": "https://www.amazon.es/dp/EJEMPLO",
  "name": "Auriculares XYZ",
  "target_price": 49.99,
  "chat_id": "123456789"
}
```

> `chat_id` es el ID de chat de Telegram al que se enviará la alerta.

### Listar productos vigilados

```http
GET /products
```

### Eliminar un producto

```http
DELETE /products/{product_id}
```

---

## 🔄 Cómo funciona

1. Registras un producto con su URL, nombre, precio objetivo y tu `chat_id` de Telegram.
2. Cada **6 horas** (`scheduler.py`), el bot:
   - Visita la URL de cada producto registrado.
   - Extrae el precio actual (`scraper.py`) probando varios selectores típicos de Amazon.
   - Guarda el precio en `price_history`.
   - Si el precio ≤ precio objetivo, envía una alerta por Telegram (`bot.py`).
3. Puedes consultar/eliminar productos en cualquier momento vía la API.

---

## ⚠️ Notas y limitaciones

- El scraper depende de selectores HTML específicos de Amazon (`a-price-whole`, `priceblock_ourprice`, etc.). Amazon cambia su HTML con frecuencia, así que **puede dejar de funcionar** sin aviso.
- Hacer scraping de Amazon puede ir en contra de sus términos de servicio; usa esto bajo tu propia responsabilidad y con moderación (el scraper ya añade un delay aleatorio entre peticiones).
- El intervalo del scheduler está fijo en 6 horas dentro de `scheduler.py` (`scheduler.add_job(check_prices, "interval", hours=6)`); cámbialo ahí si lo necesitas distinto.
- No hay autenticación en la API: cualquiera con acceso a la URL del servidor puede crear/borrar productos. Si lo vas a exponer públicamente, añade algún tipo de auth.

---

## 🗺️ Posibles mejoras

- [ ] Mover `TELEGRAM_TOKEN` y otras configuraciones a variables de entorno (`.env`)
- [ ] Limpiar `requirements.txt` con solo las dependencias reales
- [ ] Endpoint para editar un producto existente
- [ ] Soporte para más tiendas además de Amazon
- [ ] Autenticación básica en la API
- [ ] Tests automatizados

---

## 📄 Licencia

Este proyecto no especifica licencia. Añade un archivo `LICENSE` si planeas compartirlo públicamente.
