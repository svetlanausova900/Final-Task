import pytest
import requests
import json
import allure
import time
from authentification import API_URL_CREATE, API_URL_REMOVE, API_HEADERS


@allure.epic("API Tests")
@allure.feature("Personal Events Management")
class TestCreatePersonalEvent:
    
    # Тестовые данные для создания события
    BODY = {
        "backgroundColor": "#F4F5F6",
        "color": "#81888D",
        "description": "",
        "title": "Тренировка в бассейне",
        "startAt": "2025-09-30T19:00:00+03:00",
        "endAt": "2025-09-30T19:30:00+03:00"
    }

    @allure.story("Positive Tests")
    @allure.title("Успешное создание личного события")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Тест проверяет успешное создание личного события с валидными данными:
    - Статус код 200
    - Ответ в формате JSON
    """)
    def test_create_personal_event_positive(self):
        # Отправка POST запроса
        with allure.step("Отправка POST запроса для создания события"):
            response = requests.post(API_URL_CREATE, headers=API_HEADERS, json=self.BODY)
            allure.attach(f"Request URL: {API_URL_CREATE}", name="Request URL")
            allure.attach(json.dumps(self.BODY, indent=2), name="Request Body")
            allure.attach(f"Response status: {response.status_code}", name="Response Status")
            allure.attach(response.text, name="Response Body")
        
        # Проверка статус кода
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}. Response: {response.text}"
        
        # Проверка что ответ в формате JSON
        with allure.step("Проверка формата ответа"):
            assert response.headers['Content-Type'] == 'application/json', "Ответ не в формате JSON"

    @allure.story("Negative Tests")
    @allure.title("Создание события с отсутствующими обязательными полями")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.issue("BUG-1", "Система позволяет создавать события с отсутствующими обязательными полями")
    @pytest.mark.xfail(reason="Известный баг BUG-1: отсутствует валидация обязательных полей")
    @allure.description("""
    Тест проверяет обработку ошибки при отсутствии обязательного поля 'startAt'
    """)
    def test_create_personal_event_negative(self):
        # Создаем тело запроса без обязательного поля 'startAt'
        invalid_body = {
            "backgroundColor": "#F4F5F6",
            "color": "#81888D",
            "description": "",
            "title": "Тренировка в бассейне",
            "endAt": "2025-09-30T19:30:00+03:00"
        }
        
        with allure.step("Отправка POST запроса с невалидными данными"):
            response = requests.post(API_URL_CREATE, headers=API_HEADERS, json=invalid_body)
            allure.attach(json.dumps(invalid_body, indent=2), name="Invalid Request Body")
            allure.attach(f"Response status: {response.status_code}", name="Response Status")
            allure.attach(response.text, name="Response Body")
        
        # Проверяем что API возвращает ошибку
        with allure.step("Проверка кода ошибки"):
            assert response.status_code in [400, 422], f"Ожидалась ошибка 400 или 422, но получен {response.status_code}"

    @allure.story("Negative Tests")
    @allure.title("Создание события без аутентификации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_personal_event_without_authentication(self):
        # Создаем заголовки без Cookie
        headers_without_auth = {
            "Content-Type": "application/json"
        }
        
        with allure.step("Отправка запроса без аутентификации"):
            response = requests.post(API_URL_CREATE, headers=headers_without_auth, json=self.BODY)
            allure.attach(json.dumps(headers_without_auth, indent=2), name="Headers without Auth")
            allure.attach(f"Response status: {response.status_code}", name="Response Status")
        
        # Проверяем что API возвращает ошибку аутентификации
        with allure.step("Проверка ошибки аутентификации"):
            assert response.status_code in [401, 403], f"Ожидалась ошибка аутентификации 401 или 403, но получен {response.status_code}"

    @allure.story("Performance Tests")
    @allure.title("Проверка времени ответа API")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_personal_event_response_time(self):
        with allure.step("Измерение времени ответа"):
            start_time = time.time()
            response = requests.post(API_URL_CREATE, headers=API_HEADERS, json=self.BODY)
            end_time = time.time()
            
            response_time = end_time - start_time
            allure.attach(f"Response time: {response_time:.2f} seconds", name="Response Time")
        
        # Проверяем что время ответа меньше 5 секунд
        with allure.step("Проверка времени ответа"):
            assert response_time < 5, f"Время ответа слишком большое: {response_time} секунд"
            assert response.status_code == 200, f"Запрос не выполнен успешно: {response.status_code}"


@allure.epic("API Tests")
@allure.feature("Personal Events Management")
class TestRemovePersonalEvent:
    
    # ID события для удаления
    EVENT_ID = 101261661

    @allure.story("Positive Tests")
    @allure.title("Успешное удаление личного события")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Тест проверяет успешное удаление личного события:
    - Статус код 200
    - Ответ в формате JSON
    """)
    def test_remove_personal_event_success(self):
        # Тело запроса для удаления
        body = {
            "id": self.EVENT_ID,
            "startAt": "2025-09-28T19:00:00+03:00"
        }
        
        # Отправка POST запроса для удаления
        with allure.step("Отправка POST запроса для удаления события"):
            response = requests.post(API_URL_REMOVE, headers=API_HEADERS, json=body)
            allure.attach(json.dumps(body, indent=2), name="Request Body")
            allure.attach(f"Response status: {response.status_code}", name="Response Status")
            allure.attach(response.text, name="Response Body")
        
        # Проверка статус кода
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}. Response: {response.text}"
        
        # Проверка что ответ в формате JSON
        with allure.step("Проверка формата ответа"):
            assert 'application/json' in response.headers.get('Content-Type', ''), "Ответ не в формате JSON"
        
        # Парсинг JSON ответа
        with allure.step("Парсинг JSON ответа"):
            response_data = response.json()
            allure.attach(json.dumps(response_data, indent=2), name="Parsed Response")
            print(f"Ответ API: {response_data}")
