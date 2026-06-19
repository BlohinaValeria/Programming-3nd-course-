# **Разработка ML-сервиса для предсказания одобрения ипотеки**

Необходимо разработать консультирующий сервис, который предсказывает вероятность **одобрения или отказа в выдаче ипотеки** на основе предоставленных данных клиента.

Сервис должен быть реализован в виде веб-приложения с использованием **FastAPI**, предоставляющего API для взаимодействия с моделью машинного обучения.

[Ссылка на ML-сервис](https://prig6ivt.sourcecraft.site/mlprojectbsm/)

## Команда ("Хеш - это не кеш")

#|
||

**Роль**

|

**Ответственность**

|

**Ответственный**

||
||

**ML Engineer**

|

Обработка данных, обучение моделей, отбор признаков, сериализация

|

Блохина Валерия

||
||

**Backend Developer**

|

FastAPI, интеграция модели, обработка запросов

|

Мельник Наталья

||
||

**Frontend Developer**

|

HTML/CSS/JS интерфейс, интеграция с API

|

Степанова Анна

||
|#

## **ML** Engineer

### **Обработка данных**

```
# Очистка выбросов
df = df[df['person_age'] <= 100]      # аномальный возраст
df = df[df['person_emp_exp'] <= 60]   # аномальный стаж
df['person_income'] = df['person_income'].clip(upper=cap)  # ограничение дохода (99%)
```

### **Кодирование и масштабирование**

```
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])
```

### **Разделение данных**

* **Train/Test:** 80/20 со стратификацией

* **Обучающая выборка:** 35 992 записи

* **Тестовая выборка:** 8 998 записей

### **Сравнение моделей**

#|
||

**Модель**

|

**ROC-AUC**

||
||

Logistic Regression

|

0\.9039

||
||

Random Forest

|

0\.9233

||
||

**XGBoost**

|

**0.9378**

||
|#

### **Выбранная модель**

* **Алгоритм:** XGBoost (градиентный бустинг)

* **ROC-AUC:** 0.9378 

* **Формат:** Pipeline с предобработкой

* **Сериализация:** `joblib.dump()` → `models/loan_pipeline.pkl`

## **Backend Developer**

### **API Эндпоинты**

#|
||

**Метод**

|

**Эндпоинт**

|

**Описание**

||
||

POST

|

/upload-model

|

Загрузка .pkl модели

||
||

POST

|

/predict

|

Предсказание для 1\+ клиентов

||
||

POST

|

/predict-from-csv

|

Batch-предсказание из CSV

||
||

GET

|

/health

|

Проверка статуса

||
||

GET

|

/docs

|

Swagger документация

||
|#

### **Автоматическая загрузка модели**

```
@app.on_event("startup")
async def startup_event():
    global model
    model_path = Path("models/loan_pipeline.pkl")
    if model_path.exists():
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print(f"Модель автоматически загружена из {model_path}")
    else:
        print("Модель не найдена, загрузите через /upload-model")
```

## **Frontend Developer**

### **Структура**

text

```
frontend/
├── static/
│   └── style.css
└── templates/
    └── index.html
```

### **Интерфейс**

* **Секция 1:** Загрузка модели (.pkl файл)

* **Секция 2:** Форма с 13 полями для ручного ввода

* **Секция 3:** Загрузка CSV для массовых предсказаний

## **CI/CD (SourceCraft)**

### **Файл конфигурации `.sourcecraft/ci.yaml`**

```
on:
  push:
    - workflows: [quality-gate]
      filter:
        branches: ["main", "master"]

workflows:
  quality-gate:
    tasks:
      - name: python-syntax-check      # проверка синтаксиса Python
      - name: python-lint              # линтинг (ruff)
      - name: check-requirements       # проверка зависимостей
      - name: frontend-check           # проверка HTML/CSS
      - name: project-structure        # проверка структуры проекта
      - name: run-tests                # запуск pytest
```
