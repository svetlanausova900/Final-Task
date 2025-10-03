# FINAL-TASK 

# Задача: автоматизировать UI- и API-тесты из вашей финальной работы по ручному тестированию.
Для работы тестов необходимы действительные учетные данные Skyeng и стабильное интернет-соединение.

## Стек:
- Python 3.7+ - язык программирования
- Selenium WebDriver - автоматизация браузера
- Pytest - фреймворк для тестирования
- Allure - система отчетности

## Файлы *py:
- authentification.py - Файл с данными для авторизации отправлен отдельно, в репозиторий не выложен
- testUI.py - тесты User Interface
- testAPI.py - тесты API
- defects.txt - багрепорты
- requirements.txt - зависимости проекта
- readme.md  - документация

### authentification.py
Файл с данными для авторизации. Отправлен отдельно, в репозиторий не выложен

### testUI.py
Тесты проверяют функциональность авторизации и управления расписанием в личном кабинете Skyeng, включая позитивные и негативные сценарии работы с личными событиями.

### testAPI.py
Тесты проверяют функциональность создания и удаления личных событий через REST API, включая позитивные и негативные сценарии, а также проверку производительности.

## Запуск тестов:
Шаги:
1. Склонировать проект 'git clone https://github.com/svetlanausova900/Final-Task.git'
2. Установить зависимости
3. Запустить тесты через команду 'pytest -s -v'
4. Сгенерировать отчет через команду 'allure generate allure-files -o allure-report'
5. Открыть отчет через команду 'allure open allure-report'


## Запуск ТОЛЬКО API тестов:

Все API тесты - pytest -v test_api.py --alluredir=allure-results
Конкретный API тестовый класс - pytest -v test_api.py::TestCreatePersonalEvent --alluredir=allure-results
Конкретный API тест - pytest -v test_api.py::TestCreatePersonalEvent::test_create_personal_event_positive --alluredir=allure-results
Только критические API тесты - pytest -v test_api.py -m "critical" --alluredir=allure-results

## Запуск ТОЛЬКО UI тестов:

Все UI тесты - pytest -v test_ui.py --alluredir=allure-results 
Конкретный UI тестовый класс - pytest -v test_ui.py::TestSkyengLogin --alluredir=allure-results
Конкретный UI тест - pytest -v test_ui.py::TestSkyengLogin::test_successful_login_positive --alluredir=allure-results
Только критические UI тесты - pytest -v test_ui.py -m "critical" --alluredir=allure-results

### Allure отчеты
Тесты используют декораторы Allure для создания детализированных отчетов:
- @allure.epic("Skyeng Авторизация и Расписание") - основная категория
- @allure.feature("Тесты личного кабинета Skyeng") - функциональная группа
- @allure.story() - пользовательские истории
- @allure.severity() - уровень важности теста
- @allure.step() - шаги выполнения теста
- @allure.attach() - прикрепление дополнительной информации
- @allure.issue() - краткое описание бага
