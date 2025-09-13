# 🔍 Комплексный анализатор веб-сайтов

Профессиональный инструмент для анализа защиты от парсинга и структуры веб-сайтов с графическим интерфейсом.

## 🎯 Возможности

### 🔒 Анализ защиты от парсинга
- **Детекция механизмов защиты**: Cloudflare, капча, rate limiting, JavaScript
- **Анализ User-Agent**: Проверка блокировки различных пользовательских агентов
- **Тестирование методов обхода**: requests, cloudscraper, Selenium, undetected-chrome
- **Оценка сложности**: Автоматическое определение уровня защиты (LOW/MEDIUM/HIGH/CRITICAL)

### 🏗️ Анализ структуры сайта
- **DOM структура**: Подсчет элементов, тегов, классов, ID
- **Детекция контента**: Автоматическое определение товаров, статей, форм, навигации
- **Анализ ссылок**: Внутренние/внешние ссылки, формы, изображения
- **JavaScript анализ**: Обнаружение фреймворков, AJAX запросов, динамического контента
- **Генерация селекторов**: Оптимизированные CSS/XPath селекторы для парсинга

### 🎯 Интеллектуальные рекомендации
- **Выбор стратегии парсинга**: Автоматические рекомендации инструментов
- **Готовые селекторы**: Протестированные CSS селекторы для каждого типа контента
- **Оценка сложности**: Прогнозирование времени и усилий на разработку парсера
- **Методы обхода**: Конкретные техники для преодоления защиты

## 🚀 Быстрый старт

### 1. Установка зависимостей
```bash
# Автоматическая установка
python install_dependencies.py

# Или ручная установка
pip install -r requirements.txt
```

### 2. Запуск анализатора
```bash
python comprehensive_analyzer.py
```

### 3. Использование
1. Введите URL сайта в поле ввода
2. Выберите тип анализа (защита/структура/полный)
3. Нажмите "🔍 Анализировать"
4. Изучите результаты на различных вкладках
5. Экспортируйте отчеты в нужном формате

## 📋 Требования

### Системные требования
- **Python**: 3.7 или выше
- **ОС**: Windows, macOS, Linux
- **ОЗУ**: Минимум 4 ГБ (рекомендуется 8 ГБ)
- **Место на диске**: 500 МБ свободного места

### Основные зависимости
```
requests>=2.25.1         # HTTP запросы
beautifulsoup4>=4.9.3    # Парсинг HTML
fake-useragent>=0.1.11   # Генерация User-Agent
cloudscraper>=1.2.60     # Обход Cloudflare
```

### Дополнительные зависимости (опционально)
```
selenium>=4.0.0                    # Автоматизация браузера
undetected-chromedriver>=3.5.0     # Антидетект Chrome
selenium-wire>=5.1.0               # Перехват трафика
pandas>=1.3.0                      # Обработка данных
```

## 🏗️ Структура проекта

```
C:\src\last\
├── comprehensive_analyzer.py    # Главный модуль
├── protection_analyzer.py       # Анализ защиты
├── structure_analyzer.py        # Анализ структуры
├── gui_components.py           # GUI интерфейс
├── utils.py                    # Вспомогательные функции
├── requirements.txt            # Зависимости
├── install_dependencies.py     # Установщик
├── README.md                   # Документация
└── logs/                       # Логи работы
    └── analyzer_YYYYMMDD.log
```

## 🎮 Интерфейс пользователя

### Главное окно
- **Поле URL**: Ввод адреса для анализа
- **Тип анализа**: Выбор между защитой, структурой или полным анализом
- **Кнопки управления**: Анализ, экспорт, очистка

### Вкладки результатов
1. **📋 Сводка**: Краткий обзор результатов с рекомендациями
2. **🔒 Защита**: Детальный анализ механизмов защиты
3. **🏗️ Структура**: Анализ DOM структуры и контента
4. **🎯 Селекторы**: Готовые CSS селекторы для парсинга
5. **📄 Полный отчет**: Комплексный отчет со всеми данными

## 🔧 Примеры использования

### Анализ e-commerce сайта
```python
from comprehensive_analyzer import ComprehensiveWebsiteAnalyzer

analyzer = ComprehensiveWebsiteAnalyzer()
results = analyzer.analyze_website("https://shop.example.com", "both")

# Получение рекомендованных селекторов для товаров
product_selectors = results['structure']['suggested_selectors']['products']
print("Селекторы товаров:", product_selectors)
```

### Проверка только защиты
```python
# Анализ только механизмов защиты
protection_results = analyzer.analyze_website("https://example.com", "protection")

complexity = protection_results['protection']['complexity_level']
print(f"Уровень защиты: {complexity}")
```

### Экспорт результатов
```python
# Сохранение результатов в файл
analyzer.export_results("analysis_report.json", results)
```

## 📊 Типы анализируемых сайтов

### ✅ Отлично подходит для
- **E-commerce**: Интернет-магазины, каталоги товаров
- **Новостные сайты**: Порталы, блоги, медиа
- **Корпоративные сайты**: Компании, услуги, контакты
- **Социальные сети**: Профили, посты (публичные)
- **Форумы и сообщества**: Обсуждения, темы

### ⚠️ Ограничения
- **SPA приложения**: Сложные Single Page Applications требуют Selenium
- **Сайты с авторизацией**: Анализируется только публичная часть
- **API endpoints**: Прямой анализ API не поддерживается
- **Сайты с капчей**: Требуется ручное решение капчи

## 🛡️ Механизмы защиты

### Обнаруживаемые защиты
| Механизм | Описание | Уровень сложности |
|----------|----------|------------------|
| **Cloudflare** | DDoS защита, фильтрация ботов | HIGH |
| **JavaScript обязательный** | Контент загружается через JS | MEDIUM-HIGH |
| **Rate Limiting** | Ограничение частоты запросов | MEDIUM |
| **User-Agent фильтрация** | Блокировка по заголовкам | LOW-MEDIUM |
| **Капча** | reCAPTCHA, hCaptcha и другие | HIGH-CRITICAL |
| **Cookie требования** | Обязательные cookies | LOW |

### Методы обхода
1. **requests** - Простые HTTP запросы
2. **cloudscraper** - Обход Cloudflare
3. **Selenium** - Полная эмуляция браузера
4. **undetected-chrome** - Антидетект браузер
5. **fake-useragent** - Ротация User-Agent

## 🎯 Генерируемые селекторы

### Типы селекторов
- **Товары**: `[class*="product"]`, `[data-product]`, `.item-card`
- **Цены**: `[class*="price"]`, `.cost`, `[data-price]`
- **Заголовки**: `h1`, `h2`, `[class*="title"]`
- **Описания**: `[class*="description"]`, `.content`, `p`
- **Ссылки**: `a[href]`, `[class*="link"]`
- **Изображения**: `img[src]`, `[class*="image"]`

### Пример использования селекторов
```python
from bs4 import BeautifulSoup
import requests

# Используем рекомендованные селекторы
url = "https://example-shop.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Товары
products = soup.select('[class*="product"]')
for product in products:
    title = product.select_one('[class*="title"]')
    price = product.select_one('[class*="price"]')
    
    print(f"Товар: {title.text if title else 'N/A'}")
    print(f"Цена: {price.text if price else 'N/A'}")
```

## 📈 Интерпретация результатов

### Уровни сложности защиты
- **LOW (0-39 баллов)**: Простой requests достаточен
- **MEDIUM (40-59 баллов)**: Требуется requests + дополнительные заголовки
- **HIGH (60-79 баллов)**: Рекомендуется Selenium или cloudscraper
- **CRITICAL (80-100 баллов)**: Обязательны продвинутые методы обхода

### Рекомендации по выбору инструментов
```
Балл защиты 0-39:   requests + BeautifulSoup
Балл защиты 40-59:  requests + cloudscraper + fake-useragent
Балл защиты 60-79:  Selenium + undetected-chromedriver
Балл защиты 80-100: Selenium + прокси + капча-сервисы
```

## 🔍 Устранение проблем

### Частые ошибки

#### "Модуль не найден"
```bash
# Переустановите зависимости
pip install -r requirements.txt --force-reinstall
```

#### "Chrome driver not found"
```bash
# Установите Chrome
# Windows: скачайте с https://www.google.com/chrome/
# Linux: sudo apt install google-chrome-stable
# macOS: brew install --cask google-chrome
```

#### "Timeout errors"
```python
# Увеличьте таймауты в коде
session.get(url, timeout=30)  # вместо 15
```

#### "Access denied / 403 Forbidden"
```python
# Проверьте заголовки и используйте случайные User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
```

### Логирование
Все операции записываются в файлы логов:
```
logs/analyzer_YYYYMMDD.log
```

Для включения отладочного режима:
```python
import logging
logging.getLogger('WebsiteAnalyzer').setLevel(logging.DEBUG)
```

## 🤝 Поддержка и развитие

### Сообщение об ошибках
При обнаружении ошибок предоставьте:
1. URL проблемного сайта
2. Лог ошибки из файла `logs/`
3. Версию Python и ОС
4. Шаги для воспроизведения

### Планы развития
- [ ] Поддержка Playwright
- [ ] Анализ мобильных версий сайтов
- [ ] Интеграция с прокси-сервисами
- [ ] API для автоматизации
- [ ] Плагины для популярных CMS
- [ ] Экспорт в Scrapy проекты

## 📄 Лицензия

Этот проект создан для образовательных и исследовательских целей. 

**Важно**: Соблюдайте robots.txt, условия использования сайтов и применимое законодательство при парсинге данных.

## 🔗 Полезные ресурсы

### Документация библиотек
- [Requests](https://docs.python-requests.org/): HTTP запросы
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Парсинг HTML
- [Selenium](https://selenium-python.readthedocs.io/): Автоматизация браузера
- [CloudScraper](https://github.com/VeNoMouS/cloudscraper): Обход Cloudflare

### Инструменты для веб-парсинга
- [Scrapy](https://scrapy.org/): Фреймворк для парсинга
- [Playwright](https://playwright.dev/python/): Современная автоматизация браузера
- [httpx](https://www.python-httpx.org/): Асинхронные HTTP запросы

---

**Автор**: OduH 
**Версия**: 3.0.0  
**Дата**: 2025-09-14  

🎯 **Цель проекта**: Упростить анализ веб-сайтов и создание эффективных парсеров с помощью автоматизированного анализа и интеллектуальных рекомендаций.