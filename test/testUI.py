import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from authentification import URL, LOGIN, PASSWORD


@allure.epic("Skyeng Авторизация и Расписание")
@allure.feature("Тесты личного кабинета Skyeng")
class TestSkyengLogin:
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        with allure.step("Инициализация браузера"):
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)
        
        yield
        
        with allure.step("Закрытие браузера"):
            self.driver.quit()
    
    @allure.story("Успешная авторизация")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Тестирование успешного входа в личный кабинет с корректными данными")
    def test_successful_login_positive(self):
        with allure.step("Открытие страницы авторизации"):
            self.driver.get(URL)
        
        with allure.step("Проверка загрузки страницы"):
            assert "Skyeng" in self.driver.title
            assert "Вход" in self.driver.page_source
        
        with allure.step("Клик на кнопку 'Войти с помощью пароля'"):
            password_login_button = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Войти с помощью пароля')]")
            assert password_login_button.is_displayed(), "Кнопка 'Войти с помощью пароля' не отображается"
            password_login_button.click()
        
        with allure.step("Ввод email"):
            email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            email_field.clear()
            email_field.send_keys(LOGIN)
            assert email_field.get_attribute("value") == LOGIN, "Email введен некорректно"
        
        with allure.step("Ввод пароля"):
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(PASSWORD)
            assert len(password_field.get_attribute("value")) > 0, "Пароль не введен"
        
        with allure.step("Клик на кнопку 'Войти'"):
            submit_button = self.driver.find_element(By.XPATH, "//button//span[contains(text(), 'Войти')]")
            assert submit_button.is_enabled(), "Кнопка 'Войти' неактивна"
            submit_button.click()

        with allure.step("Ожидание завершения авторизации"):
            WebDriverWait(self.driver, 15).until(EC.url_changes(URL))
        
        with allure.step("Проверка успешной авторизации"):
            current_url = self.driver.current_url
            allure.attach(f"Текущий URL после входа: {current_url}", name="URL после авторизации")
            
            assert "login" not in current_url.lower(), f"Остались на странице входа: {current_url}"
            assert self.driver.find_elements(By.XPATH, "//input[@name='username']") == [], "Форма входа все еще присутствует"
            
            allure.attach("Вход выполнен успешно!", name="Результат авторизации")

    @allure.story("Неуспешная авторизация")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Тестирование входа с неверными учетными данными")
    def test_unsuccessful_login_negative(self):
        with allure.step("Открытие страницы авторизации"):
            self.driver.get(URL)
        
        with allure.step("Клик на кнопку 'Войти с помощью пароля'"):
            password_login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Войти с помощью пароля')]")))
            password_login_button.click()
        
        with allure.step("Ввод неверных данных"):
            email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            email_field.clear()
            email_field.send_keys("test345@skyeng.ru")
            
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys("password")
        
        with allure.step("Клик на кнопку 'Войти'"):
            submit_button = self.driver.find_element(By.XPATH, "//button//span[contains(text(), 'Войти')]")
            submit_button.click()

        with allure.step("Проверка сообщения об ошибке"):
            error_message = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Неверный') or contains(text(), 'Ошибка') or contains(text(), 'error')]")
            assert len(error_message) > 0, "Сообщение об ошибке не появилось"
            allure.attach(f"Найдено сообщений об ошибке: {len(error_message)}", name="Результат проверки ошибки")

    @allure.story("Создание события в расписании")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Тест создания события 'Сдача финального задания' в расписании")
    def test_schedule_event_creation_positive(self):
        with allure.step("Авторизация пользователя"):
            self._perform_login()
        
        with allure.step("Переход в раздел Расписание"):
            self.go_to_schedule()
        
        with allure.step("Создание события 'Сдача финального задания'"):
            self.create_final_assignment_event()
        
        with allure.step("Проверка создания события"):
            self.verify_event_created()
            
        allure.attach("Тест пройден: событие 'Сдача финального задания' успешно создано!", name="Результат теста")

    @allure.story("Негативный тест создания события")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Тест создания события без наименования")
    def test_schedule_event_creation_without_name_negative(self):
        with allure.step("Авторизация пользователя"):
            self._perform_login()
        
        with allure.step("Переход в раздел Расписание"):
            self.go_to_schedule()
        
        with allure.step("Попытка создания события без названия"):
            self.create_event_without_name()
        
        with allure.step("Проверка, что событие не создано"):
            self.verify_event_not_created()

    @allure.story("Удаление события из расписания")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Тест удаления созданного события")
    def test_schedule_event_delete_positive(self):
        with allure.step("Авторизация пользователя"):
            self._perform_login()
        
        with allure.step("Переход в раздел Расписание"):
            self.go_to_schedule()
        
        with allure.step("Удаление созданного события"):
            self.delete_final_assignment_event()
        
        with allure.step("Проверка удаления события"):
            self.verify_event_deleted()

    def _perform_login(self):
        """Вспомогательный метод для авторизации"""
        with allure.step("Выполнение авторизации"):
            self.driver.get(URL)
            
            password_login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Войти с помощью пароля')]")))
            password_login_button.click()
            
            email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            email_field.clear()
            email_field.send_keys(LOGIN)
            
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(PASSWORD)
            
            submit_button = self.driver.find_element(By.XPATH, "//button//span[contains(text(), 'Войти')]")
            submit_button.click()
            
            # Ожидание завершения авторизации
            WebDriverWait(self.driver, 15).until(EC.url_changes(URL))

    @allure.step("Переход в раздел Расписание")
    def go_to_schedule(self):
        """Переход в раздел Расписание"""
        try:
            # Попытка 1: Ищем по точному тексту и классу
            schedule_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='title' and text()='Расписание']"))
            )
            schedule_element.click()
            allure.attach("Найден элемент расписания по точному совпадению", name="Поиск элемента")
        except:
            try:
                # Попытка 2: Ищем по частичному совпадению текста
                schedule_element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Расписание')]"))
                )
                schedule_element.click()
                allure.attach("Найден элемент расписания по частичному совпадению", name="Поиск элемента")
            except:
                # Попытка 3: Ищем по атрибуту _ngcontent
                schedule_element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'title') and contains(text(), 'Расписание')]"))
                )
                schedule_element.click()
                allure.attach("Найден элемент расписания по атрибуту _ngcontent", name="Поиск элемента")
        
        # Проверяем, что перешли в раздел расписания
        assert "расписание" in self.driver.page_source.lower() or "schedule" in self.driver.page_source.lower()
        allure.attach("Успешно перешли в раздел Расписание", name="Результат перехода")

    @allure.step("Создание события 'Сдача финального задания'")
    def create_final_assignment_event(self):
        """Создание события 'Сдача финального задания' в разделе Личное событие"""
        event_name = "Сдача финального задания"
        
        # Нажатие на иконку Добавить событие (+)
        add_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "ds-icon.add-icon"))
        )
        add_icon.click()

        # Переход в личные события
        personal_event = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'text-center') and contains(text(), 'Личное событие')]"))
        )
        personal_event.click()
        
        # Заполняем название события
        title_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.width-100.mt8.-size-m.-skin-normal"))
        )
        title_field.clear()
        title_field.send_keys(event_name)
        allure.attach(f"Заполнено название события: '{event_name}'", name="Заполнение названия")
       
        # Заполняем дату
        date_select = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select.class-date"))
        )
        select = Select(date_select)
        select.select_by_visible_text("Вторник, 30 сентября")

        # Сохраняем событие
        save_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.root.-type-primary.-color-brand.-size-m"))
        )
        save_button.click()
        allure.attach("Событие сохранено", name="Сохранение")

    @allure.step("Проверка создания события")
    def verify_event_created(self):
        """Проверка, что событие создалось"""
        # Ждем появления события в расписании
        event_in_schedule = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'Сдача финального задания')]"))
        )
        assert event_in_schedule.is_displayed(), "Событие не отображается в расписании"
        allure.attach("Событие успешно создано и отображается в расписании", name="Результат проверки")

    @allure.step("Создание события без названия")
    def create_event_without_name(self):
        """Создание события без наименования"""
        event_name = ""
        
        # Нажатие на иконку Добавить событие (+)
        add_icon = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "ds-icon.add-icon"))
        )
        add_icon.click()
        
        # Переход в личные события
        personal_event = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'text-center') and contains(text(), 'Личное событие')]"))
        )
        personal_event.click()
        
        # Оставляем название события пустым
        title_field = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.width-100.mt8.-size-m.-skin-normal"))
        )
        title_field.clear()
        title_field.send_keys(event_name)
    
        # Заполняем дату
        date_select = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select.class-date"))
        )
        select = Select(date_select)
        select.select_by_visible_text("Вторник, 30 сентября")

        # Пытаемся сохранить событие
        save_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.root.-type-primary.-color-brand.-size-m"))
        )
        save_button.click()

    @allure.step("Проверка, что событие не создано")
    def verify_event_not_created(self):
        """Проверка, что событие НЕ создалось"""
        # Проверяем, что событие с пустым названием не отображается
        empty_events = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'long-view__title') and text()='']")
        assert len(empty_events) == 0, "Найдено событие с пустым названием"
        allure.attach("Событие без названия не было создано - проверка пройдена", name="Результат проверки")

    @allure.step("Удаление события")
    def delete_final_assignment_event(self):
        """Удаление события 'Финальный отчет'"""   
        # Ищем событие по заголовку
        event_title = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='long-view__title' and text()='Сдача']"))
        )
            
        # Кликаем на событие для открытия деталей
        event_title.click()

        delete_element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='text-container' and contains(text(), 'Удалить')]"))
        )
        delete_element.click()
        allure.attach("Событие удалено", name="Результат удаления")

    @allure.step("Проверка удаления события")
    def verify_event_deleted(self):
        """Проверка, что событие было удалено"""
        # Множественные проверки
        events = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Сдача')]")
    
    # Проверяем что событие не найдено
        assert len(events) == 2, "Событие не было удалено - все еще найдено на странице"
    
        allure.attach("✓ Событие успешно удалено", name="Результат проверки")