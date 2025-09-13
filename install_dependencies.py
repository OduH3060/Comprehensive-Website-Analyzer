#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 УСТАНОВЩИК ЗАВИСИМОСТЕЙ
==========================
Автоматическая установка всех необходимых пакетов для комплексного анализатора

Автор: Senior Python Developer
Версия: 3.0.0
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def print_header():
    """Печать заголовка"""
    print("🚀 УСТАНОВЩИК КОМПЛЕКСНОГО АНАЛИЗАТОРА ВЕБ-САЙТОВ")
    print("=" * 70)
    print("Автоматическая установка всех необходимых зависимостей")
    print()

def check_python_version():
    """Проверка версии Python"""
    print("🐍 Проверка версии Python...")
    
    version = sys.version_info
    print(f"   Текущая версия: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Требуется Python 3.7 или выше!")
        print("   Пожалуйста, обновите Python: https://www.python.org/downloads/")
        return False
    else:
        print("✅ Версия Python подходит")
        return True

def check_pip():
    """Проверка наличия pip"""
    print("\n📦 Проверка pip...")
    
    try:
        import pip
        print("✅ pip доступен")
        return True
    except ImportError:
        print("❌ pip не найден!")
        print("   Установите pip: https://pip.pypa.io/en/stable/installing/")
        return False

def upgrade_pip():
    """Обновление pip"""
    print("\n🔄 Обновление pip...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        print("✅ pip обновлен")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Не удалось обновить pip: {e}")
        return False

def install_package(package_name, description=""):
    """Установка одного пакета"""
    print(f"🔄 Установка {package_name}...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name, "--quiet"
        ])
        print(f"✅ {package_name} - Успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {package_name} - Ошибка: {e}")
        return False

def install_requirements():
    """Установка пакетов из requirements.txt"""
    print("\n📦 УСТАНОВКА ОСНОВНЫХ ЗАВИСИМОСТЕЙ")
    print("=" * 50)
    
    # Основные пакеты
    essential_packages = [
        ("requests", "HTTP библиотека"),
        ("beautifulsoup4", "Парсинг HTML"),
        ("lxml", "XML/HTML парсер"),
        ("fake-useragent", "Генерация User-Agent"),
        ("urllib3", "HTTP клиент"),
        ("certifi", "SSL сертификаты")
    ]
    
    success_count = 0
    
    for package, description in essential_packages:
        if install_package(package, description):
            success_count += 1
    
    print(f"\n📊 Основные пакеты: {success_count}/{len(essential_packages)} установлены")
    
    # Дополнительные пакеты
    print("\n📦 УСТАНОВКА ДОПОЛНИТЕЛЬНЫХ ПАКЕТОВ")
    print("=" * 50)
    
    optional_packages = [
        ("cloudscraper", "Обход Cloudflare"),
        ("selenium", "Автоматизация браузера"),
        ("selenium-wire", "Перехват трафика"),
        ("undetected-chromedriver", "Антидетект Chrome"),
        ("requests-toolbelt", "Расширения для requests"),
        ("pandas", "Обработка данных"),
        ("Pillow", "Работа с изображениями")
    ]
    
    optional_success = 0
    
    for package, description in optional_packages:
        if install_package(package, description):
            optional_success += 1
    
    print(f"\n📊 Дополнительные пакеты: {optional_success}/{len(optional_packages)} установлены")
    
    return success_count, optional_success

def check_chrome():
    """Проверка наличия Google Chrome"""
    print("\n🚗 ПРОВЕРКА GOOGLE CHROME")
    print("=" * 40)
    
    system = platform.system()
    chrome_paths = []
    
    if system == "Windows":
        chrome_paths = [
            "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
        ]
    elif system == "Darwin":  # macOS
        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        ]
    elif system == "Linux":
        chrome_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium"
        ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome найден: {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        print("⚠️ Google Chrome не найден")
        print("📥 Рекомендуется установить:")
        if system == "Windows":
            print("   • https://www.google.com/chrome/")
        elif system == "Darwin":
            print("   • https://www.google.com/chrome/")
            print("   • brew install --cask google-chrome")
        elif system == "Linux":
            print("   • sudo apt install google-chrome-stable")
            print("   • sudo dnf install google-chrome-stable")
        print("💡 Selenium будет работать с Chromium как альтернатива")
    
    return chrome_found

def test_imports():
    """Тестирование импорта установленных пакетов"""
    print("\n🧪 ТЕСТИРОВАНИЕ УСТАНОВЛЕННЫХ ПАКЕТОВ")
    print("=" * 50)
    
    test_packages = [
        ("requests", "import requests"),
        ("beautifulsoup4", "from bs4 import BeautifulSoup"),
        ("fake_useragent", "from fake_useragent import UserAgent"),
        ("cloudscraper", "import cloudscraper"),
        ("selenium", "from selenium import webdriver"),
        ("undetected_chromedriver", "import undetected_chromedriver")
    ]
    
    success_count = 0
    
    for package_name, import_statement in test_packages:
        try:
            exec(import_statement)
            print(f"✅ {package_name} - OK")
            success_count += 1
        except ImportError as e:
            print(f"❌ {package_name} - Ошибка: {e}")
        except Exception as e:
            print(f"⚠️ {package_name} - Предупреждение: {e}")
    
    print(f"\n📊 Работающие пакеты: {success_count}/{len(test_packages)}")
    return success_count

def create_test_script():
    """Создание тестового скрипта"""
    print("\n📝 Создание тестового скрипта...")
    
    test_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Тест зависимостей комплексного анализатора
"""

def test_dependencies():
    """Тестирование всех зависимостей"""
    
    results = {}
    
    # Основные пакеты
    try:
        import requests
        results['requests'] = '✅ OK'
    except ImportError:
        results['requests'] = '❌ Не установлен'
    
    try:
        from bs4 import BeautifulSoup
        results['beautifulsoup4'] = '✅ OK'
    except ImportError:
        results['beautifulsoup4'] = '❌ Не установлен'
    
    try:
        from fake_useragent import UserAgent
        results['fake_useragent'] = '✅ OK'
    except ImportError:
        results['fake_useragent'] = '❌ Не установлен'
    
    # Дополнительные пакеты
    try:
        import cloudscraper
        results['cloudscraper'] = '✅ OK'
    except ImportError:
        results['cloudscraper'] = '❌ Не установлен'
    
    try:
        from selenium import webdriver
        results['selenium'] = '✅ OK'
    except ImportError:
        results['selenium'] = '❌ Не установлен'
    
    try:
        import undetected_chromedriver
        results['undetected_chromedriver'] = '✅ OK'
    except ImportError:
        results['undetected_chromedriver'] = '❌ Не установлен'
    
    # Вывод результатов
    print("🧪 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ЗАВИСИМОСТЕЙ")
    print("=" * 50)
    
    for package, status in results.items():
        print(f"{package:25} {status}")
    
    # Быстрый тест requests
    print("\\n🌐 Тест HTTP запроса...")
    try:
        response = requests.get("https://httpbin.org/get", timeout=10)
        if response.status_code == 200:
            print("✅ HTTP запросы работают")
        else:
            print(f"⚠️ HTTP статус: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка HTTP: {e}")
    
    print("\\n✅ Тестирование завершено!")

if __name__ == "__main__":
    test_dependencies()
'''
    
    try:
        with open("test_dependencies.py", "w", encoding="utf-8") as f:
            f.write(test_script)
        print("✅ Создан test_dependencies.py")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания файла: {e}")
        return False

def print_final_instructions():
    """Вывод финальных инструкций"""
    print("\n🎉 УСТАНОВКА ЗАВЕРШЕНА!")
    print("=" * 40)
    print("📋 Что дальше:")
    print("1. Запустите: python test_dependencies.py")
    print("2. Если тесты прошли успешно:")
    print("3. Запустите: python comprehensive_analyzer.py")
    print()
    print("💡 Дополнительная информация:")
    print("   • README.md - подробные инструкции")
    print("   • Логи в папке logs/")
    print("   • Примеры в examples/")
    print()
    
    # Системная информация
    system_info = {
        'Система': platform.system(),
        'Версия': platform.release(),
        'Python': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'Архитектура': platform.machine()
    }
    
    print("🖥️ Системная информация:")
    for key, value in system_info.items():
        print(f"   {key}: {value}")

def main():
    """Главная функция установщика"""
    print_header()
    
    # Проверки
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # Обновление pip
    upgrade_pip()
    
    # Установка пакетов
    essential_count, optional_count = install_requirements()
    
    # Проверка браузера
    chrome_found = check_chrome()
    
    # Тестирование импортов
    working_packages = test_imports()
    
    # Создание тестового скрипта
    create_test_script()
    
    # Финальные инструкции
    print_final_instructions()
    
    # Итоговая оценка
    print("\n📊 ИТОГОВАЯ ОЦЕНКА")
    print("=" * 30)
    
    if essential_count >= 4 and working_packages >= 3:
        print("🟢 Отлично! Анализатор готов к работе")
        success_level = "excellent"
    elif essential_count >= 3 and working_packages >= 2:
        print("🟡 Хорошо! Основные функции доступны")
        success_level = "good"
    else:
        print("🔴 Требуется внимание! Не все пакеты установлены")
        success_level = "needs_attention"
    
    if not chrome_found:
        print("⚠️ Рекомендуется установить Google Chrome для полной функциональности")
    
    return success_level in ["excellent", "good"]

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎯 Установка успешна! Можно запускать анализатор.")
        else:
            print("\n⚠️ Установка завершена с предупреждениями.")
            print("   Проверьте сообщения выше и устраните проблемы.")
    except KeyboardInterrupt:
        print("\n\n🛑 Установка прервана пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка установки: {e}")
        print("   Обратитесь к документации или создайте issue")