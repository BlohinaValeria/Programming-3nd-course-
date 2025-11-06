# Лабораторная работа 6 Использование шаблона «Наблюдатель»

Необходимо создать программу на языке Python, которая использует паттерн проектирования "Наблюдатель" для отслеживания изменений курсов валют через API Центробанка РФ. Программа должна запрашивать курсы валют и уведомлять зарегистрированных наблюдателей о изменении курсов в реальном времени или через заданные интервалы времени.
Структура реализованного задания должна представлять

Объект — веб-сервер Flask или FastAPI, Tornado.
Наблюдатели - клиенты, представляющие HTML-страницы, связывающиеся с объектом с помощью веб-сокетов. На странице должен отображаться идентификатор клиента.
Комментарии по выполнению
Изучите пример реализации схемы шаблона «Наблюдатель»: https://refactoringguru.cn/ru/design-patterns/observer/python/example. 

Проанализируйте код: 

https://github.com/tornadoweb/tornado/tree/stable/demos/chat
https://github.com/tornadoweb/tornado/tree/stable/demos/websocket
Назначение: 

Объект (Subject) будет запрашивать данные с API и отслеживать изменения курсов.
Наблюдатели (Observers) будут получать уведомления об изменении курса и отображать информацию. Например, наблюдателями могут быть различные компоненты системы, которые отслеживают конкретные валюты (например, USD, EUR, GBP).


## Полученный сайт
![]()


## Код программы
```
import asyncio
import json
from datetime import datetime
from abc import ABC, abstractmethod

import aiohttp
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

# ----------- Паттерн "Наблюдатель" -----------

class Observer(ABC):
    @abstractmethod
    async def update(self, currency_data):
        pass


class CurrencySubject:
    """Субъект, который следит за изменениями курсов валют"""
    def __init__(self):
        self._observers = []
        self._currency_data = {}

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    async def notify_observers(self):
        """Отправка обновлений всем наблюдателям"""
        for observer in self._observers[:]:
            try:
                await observer.update(self._currency_data)
            except Exception as e:
                print(f"Ошибка при уведомлении: {e}")
                self.remove_observer(observer)

    async def update_currency_data(self):
        """Запрос актуальных курсов валют с сайта ЦБ РФ"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://www.cbr-xml-daily.ru/daily_json.js') as response:
                    if response.status == 200:
                        data = json.loads(await response.text())
                        currencies = {
                            'USD': data['Valute']['USD']['Value'],
                            'EUR': data['Valute']['EUR']['Value'],
                            'GBP': data['Valute']['GBP']['Value'],
                            'CNY': data['Valute']['CNY']['Value']
                        }

                        if currencies != self._currency_data:
                            self._currency_data = currencies
                            await self.notify_observers()
                            print(f"[{datetime.now().isoformat()}] Обновлены данные: {currencies}")

        except Exception as e:
            print(f"Ошибка при обновлении валют: {e}")


# ----------- Конкретный наблюдатель -----------

class WebSocketObserver(Observer):
    def __init__(self, websocket: WebSocket, client_id: str):
        self.websocket = websocket
        self.client_id = client_id

    async def update(self, currency_data):
        """Отправка данных клиенту"""
        message = {
            "client_id": self.client_id,
            "currency_data": currency_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.websocket.send_text(json.dumps(message, ensure_ascii=False))


# ----------- FastAPI приложение -----------

app = FastAPI()
currency_subject = CurrencySubject()
client_counter = 0

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Курсы валют ЦБ РФ</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body { 
            font-family: 'Roboto', sans-serif; 
            background-color: #b39adb;
            margin: 0;
            padding: 40px;
            color: black;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: #9adbb3;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            padding: 30px;
            position: relative;
            overflow: hidden;
        }


        h1 {
            text-align: center;
            color: white;
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
        }
        .status {
            padding: 12px;
            text-align: center;
            border-radius: 8px;
            font-weight: 500;
            margin-bottom: 15px;
            position: relative;
            z-index: 1;
        }
        .connected { background: #d4edda; color: #155724; }
        .disconnected { background: #f8d7da; color: #721c24; }
        #clientInfo {
            text-align: center;
            font-size: 16px;
            margin-bottom: 20px;
            color: white;
            position: relative;
            z-index: 1;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            position: relative;
            z-index: 1;
        }
        th, td {
            border: 1px solid #e0e0e0;
            padding: 12px;
            text-align: center;
            background: rgba(255, 255, 255, 0.9);
        }
        th {
            background-color: #dbb39a;
            color: white;
            font-weight: 600;
        }
        tr:nth-child(even) td {
            background-color: white;
        }
        #lastUpdate {
            text-align: right;
            margin-top: 15px;
            color: #666;
            font-size: 14px;
            position: relative;
            z-index: 1;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Курсы валют ЦБ РФ</h1>
        <div id="clientInfo">Загрузка...</div>
        <div id="status" class="status disconnected">Подключение...</div>

        <table id="currencyTable">
            <thead>
                <tr>
                    <th>Валюта</th>
                    <th>Курс (₽)</th>
                </tr>
            </thead>
            <tbody id="currencyBody">
                <tr><td colspan="2">Ожидание данных...</td></tr>
            </tbody>
        </table>

        <div id="lastUpdate">Последнее обновление: -</div>
    </div>

    <script>
        let clientId = null;
        let ws = null;

        function connect() {
            ws = new WebSocket("ws://localhost:8000/ws");

            ws.onopen = function() {
                document.getElementById("status").className = "status connected";
                document.getElementById("status").textContent = "✅ Подключено к серверу";
            };

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);

                if (data.client_id && !clientId) {
                    clientId = data.client_id;
                    document.getElementById("clientInfo").textContent = `Клиент: ${clientId}`;
                }

                if (data.currency_data) {
                    updateTable(data.currency_data, data.timestamp);
                }
            };

            ws.onclose = function() {
                document.getElementById("status").className = "status disconnected";
                document.getElementById("status").textContent = "❌ Отключено от сервера (переподключение...)";
                setTimeout(connect, 3000);
            };
        }

        function updateTable(data, timestamp) {
            const tbody = document.getElementById("currencyBody");
            tbody.innerHTML = "";
            for (const [currency, value] of Object.entries(data)) {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${getCurrencyName(currency)}</td>
                    <td>${value.toFixed(2)}</td>
                `;
                tbody.appendChild(row);
            }
            document.getElementById("lastUpdate").textContent = 
                "Последнее обновление: " + new Date(timestamp).toLocaleString();
        }

        function getCurrencyName(code) {
            const names = {
                "USD": "🇺🇸 Доллар США",
                "EUR": "🇪🇺 Евро",
                "GBP": "🇬🇧 Фунт стерлингов",
                "CNY": "🇨🇳 Китайский юань"
            };
            return names[code] || code;
        }

        connect();
    </script>
</body>
</html>
"""



@app.get("/")
async def index():
    return HTMLResponse(HTML_PAGE)


@app.websocket("/ws")
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket-соединение с клиентом"""
    global client_counter
    await websocket.accept()
    client_counter += 1
    client_id = f"client_{client_counter}"

    observer = WebSocketObserver(websocket, client_id)
    currency_subject.add_observer(observer)

    # Отправляем приветственное сообщение
    await websocket.send_text(json.dumps({
        "client_id": client_id,
        "message": "Подключение установлено"
    }, ensure_ascii=False))

    # ✅ Отправляем текущие курсы валют сразу при подключении (если уже есть данные)
    if currency_subject._currency_data:
        await observer.update(currency_subject._currency_data)
    else:
        # если данных пока нет, отправим сообщение ожидания
        await websocket.send_text(json.dumps({
            "client_id": client_id,
            "currency_data": {},
            "message": "Ожидание данных о курсах валют..."
        }, ensure_ascii=False))

    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        print(f"Клиент {client_id} отключился")
        currency_subject.remove_observer(observer)


# ----------- Фоновая задача обновления курсов -----------

async def currency_updater():
    while True:
        await currency_subject.update_currency_data()
        await asyncio.sleep(60)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(currency_updater())


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
```
