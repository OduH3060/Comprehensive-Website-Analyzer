#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛠️ МОДУЛЬ УТИЛИТ
================
Вспомогательные функции для комплексного анализатора веб-сайтов

Автор: Senior Python Developer
Версия: 3.0.0
"""

import logging
import re
from urllib.parse import urlparse
import os
import sys
from datetime import datetime

def setup_logging(level=logging.INFO):
    """Настройка системы логирования"""
    
    # Создаем директорию для логов
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Имя файла лога с датой
    log_filename = os.path.join(log_dir, f"analyzer_{datetime.now().strftime('%Y%m%d')}.log")
    
    # Настройка форматирования
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Обработчик для файла
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Настройка логгера
    logger = logging.getLogger('WebsiteAnalyzer')
    logger.setLevel(level)
    
    # Очищаем существующие обработчики
    logger.handlers.clear()
    
    # Добавляем новые обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Отключаем propagation чтобы избежать дублирования
    logger.propagate = False
    
    logger.info("Система логирования инициализирована")
    return logger

def validate_url(url: str) -> str:
    """
    Валидация и нормализация URL
    
    Args:
        url: URL для валидации
        
    Returns:
        str: Нормализованный URL
        
    Raises:
        ValueError: Если URL невалидный
    """
    
    if not url or not isinstance(url, str):
        raise ValueError("URL не может быть пустым")
    
    # Удаляем пробелы
    url = url.strip()
    
    # Добавляем схему если отсутствует
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Парсим URL
    try:
        parsed = urlparse(url)
        
        # Проверяем обязательные компоненты
        if not parsed.netloc:
            raise ValueError("Невалидный URL: отсутствует домен")
        
        # Проверяем схему
        if parsed.scheme not in ['http', 'https']:
            raise ValueError("Поддерживаются только HTTP и HTTPS схемы")
        
        # Базовая проверка домена
        domain_pattern = re.compile(
            r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?'
            r'(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        )
        
        if not domain_pattern.match(parsed.netloc.split(':')[0]):
            raise ValueError("Невалидный формат домена")
        
        return url
        
    except Exception as e:
        raise ValueError(f"Ошибка валидации URL: {e}")

def format_bytes(bytes_count: int) -> str:
    """
    Форматирование размера в байтах в читаемый вид
    
    Args:
        bytes_count: Количество байт
        
    Returns:
        str: Отформатированный размер
    """
    
    if bytes_count == 0:
        return "0 Б"
    
    units = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
    unit_index = 0
    size = float(bytes_count)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"

def format_number(number: int) -> str:
    """
    Форматирование числа с разделителями тысяч
    
    Args:
        number: Число для форматирования
        
    Returns:
        str: Отформатированное число
    """
    
    return f"{number:,}".replace(',', ' ')

def clean_text(text: str, max_length: int = None) -> str:
    """
    Очистка и нормализация текста
    
    Args:
        text: Текст для очистки
        max_length: Максимальная длина результата
        
    Returns:
        str: Очищенный текст
    """
    
    if not text:
        return ""
    
    # Удаляем лишние пробелы и переносы строк
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Ограничиваем длину
    if max_length and len(text) > max_length:
        text = text[:max_length-3] + "..."
    
    return text

def extract_domain(url: str) -> str:
    """
    Извлечение домена из URL
    
    Args:
        url: URL для обработки
        
    Returns:
        str: Доменное имя
    """
    
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except:
        return ""

def is_internal_url(url: str, base_domain: str) -> bool:
    """
    Проверка является ли URL внутренним
    
    Args:
        url: URL для проверки
        base_domain: Базовый домен сайта
        
    Returns:
        bool: True если URL внутренний
    """
    
    try:
        url_domain = extract_domain(url)
        return url_domain == base_domain.lower() or not url_domain
    except:
        return False

def safe_filename(filename: str) -> str:
    """
    Создание безопасного имени файла
    
    Args:
        filename: Исходное имя файла
        
    Returns:
        str: Безопасное имя файла
    """
    
    # Удаляем небезопасные символы
    safe_chars = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Ограничиваем длину
    if len(safe_chars) > 200:
        safe_chars = safe_chars[:200]
    
    # Удаляем точки в начале и конце
    safe_chars = safe_chars.strip('.')
    
    # Если имя пустое, генерируем стандартное
    if not safe_chars:
        safe_chars = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return safe_chars

def get_file_extension(content_type: str) -> str:
    """
    Получение расширения файла по MIME типу
    
    Args:
        content_type: MIME тип
        
    Returns:
        str: Расширение файла
    """
    
    mime_extensions = {
        'text/html': '.html',
        'text/css': '.css',
        'text/javascript': '.js',
        'application/javascript': '.js',
        'application/json': '.json',
        'application/xml': '.xml',
        'text/xml': '.xml',
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/svg+xml': '.svg',
        'application/pdf': '.pdf',
        'text/plain': '.txt'
    }
    
    return mime_extensions.get(content_type.lower(), '')

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Вычисление схожести двух текстов
    
    Args:
        text1: Первый текст
        text2: Второй текст
        
    Returns:
        float: Коэффициент схожести от 0 до 1
    """
    
    try:
        from difflib import SequenceMatcher
        return SequenceMatcher(None, text1, text2).ratio()
    except:
        return 0.0

def parse_robots_txt(robots_content: str) -> dict:
    """
    Парсинг содержимого robots.txt
    
    Args:
        robots_content: Содержимое файла robots.txt
        
    Returns:
        dict: Распarsенные правила
    """
    
    rules = {
        'user_agents': {},
        'sitemaps': [],
        'crawl_delay': None
    }
    
    current_user_agent = None
    
    for line in robots_content.split('\n'):
        line = line.strip()
        
        if not line or line.startswith('#'):
            continue
        
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            
            if key == 'user-agent':
                current_user_agent = value
                if current_user_agent not in rules['user_agents']:
                    rules['user_agents'][current_user_agent] = {
                        'disallow': [],
                        'allow': []
                    }
            
            elif key == 'disallow' and current_user_agent:
                rules['user_agents'][current_user_agent]['disallow'].append(value)
            
            elif key == 'allow' and current_user_agent:
                rules['user_agents'][current_user_agent]['allow'].append(value)
            
            elif key == 'sitemap':
                rules['sitemaps'].append(value)
            
            elif key == 'crawl-delay':
                try:
                    rules['crawl_delay'] = float(value)
                except:
                    pass
    
    return rules

def generate_user_agents():
    """
    Генерация списка популярных User-Agent строк
    
    Returns:
        list: Список User-Agent строк
    """
    
    return [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        
        # Firefox
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        
        # Safari
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        
        # Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
        
        # Opera
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.172'
    ]

def check_dependencies():
    """
    Проверка наличия всех необходимых зависимостей
    
    Returns:
        dict: Статус зависимостей
    """
    
    dependencies = {
        'requests': False,
        'beautifulsoup4': False,
        'fake_useragent': False,
        'selenium': False,
        'cloudscraper': False,
        'undetected_chromedriver': False
    }
    
    # Проверяем каждую зависимость
    for dep in dependencies:
        try:
            if dep == 'beautifulsoup4':
                import bs4
            elif dep == 'fake_useragent':
                import fake_useragent
            elif dep == 'undetected_chromedriver':
                import undetected_chromedriver
            else:
                __import__(dep)
            dependencies[dep] = True
        except ImportError:
            dependencies[dep] = False
    
    return dependencies

def get_system_info():
    """
    Получение информации о системе
    
    Returns:
        dict: Информация о системе
    """
    
    import platform
    
    return {
        'platform': platform.platform(),
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'python_implementation': platform.python_implementation()
    }

def create_progress_callback(total_steps: int):
    """
    Создание callback функции для отслеживания прогресса
    
    Args:
        total_steps: Общее количество шагов
        
    Returns:
        function: Callback функция
    """
    
    current_step = [0]  # Используем список для изменяемости
    
    def progress_callback(message: str = ""):
        current_step[0] += 1
        percentage = (current_step[0] / total_steps) * 100
        
        print(f"[{percentage:.1f}%] {message}")
        
        return {
            'current': current_step[0],
            'total': total_steps,
            'percentage': percentage,
            'message': message
        }
    
    return progress_callback

def error_handler(func):
    """
    Декоратор для обработки ошибок
    
    Args:
        func: Функция для декорирования
        
    Returns:
        function: Декорированная функция
    """
    
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger('WebsiteAnalyzer')
            logger.error(f"Ошибка в функции {func.__name__}: {e}")
            raise
    
    return wrapper

def retry_on_failure(max_attempts: int = 3, delay: float = 1.0):
    """
    Декоратор для повторных попыток при неудаче
    
    Args:
        max_attempts: Максимальное количество попыток
        delay: Задержка между попытками
        
    Returns:
        function: Декоратор
    """
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (attempt + 1))  # Увеличиваем задержку
                    continue
            
            # Если все попытки неудачны, поднимаем последнее исключение
            raise last_exception
        
        return wrapper
    return decorator

# Глобальные константы
USER_AGENTS = generate_user_agents()

HTTP_STATUS_CODES = {
    200: "OK",
    301: "Moved Permanently", 
    302: "Found",
    403: "Forbidden",
    404: "Not Found",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}

COMMON_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru,en-US;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0'
}

# Экспорт основных функций
__all__ = [
    'setup_logging',
    'validate_url', 
    'format_bytes',
    'format_number',
    'clean_text',
    'extract_domain',
    'is_internal_url',
    'safe_filename',
    'calculate_similarity',
    'check_dependencies',
    'get_system_info',
    'error_handler',
    'retry_on_failure',
    'USER_AGENTS',
    'HTTP_STATUS_CODES',
    'COMMON_HEADERS'
]