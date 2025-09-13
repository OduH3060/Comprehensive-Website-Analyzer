"""
🌐 Многоязычная поддержка для анализатора веб-сайтов
Multilingual support for website analyzer
"""

class LanguageManager:
    """Менеджер языков для переключения между русским и английским"""
    
    def __init__(self, default_language='ru'):
        self.current_language = default_language
        self.translations = {
            'ru': RUSSIAN_TRANSLATIONS,
            'en': ENGLISH_TRANSLATIONS
        }
    
    def set_language(self, language):
        """Установить текущий язык"""
        if language in self.translations:
            self.current_language = language
            return True
        return False
    
    def get_text(self, key, **kwargs):
        """Получить переведенный текст по ключу"""
        try:
            text = self.translations[self.current_language].get(key, key)
            if kwargs:
                return text.format(**kwargs)
            return text
        except Exception:
            return key
    
    def get_current_language(self):
        """Получить текущий язык"""
        return self.current_language
    
    def get_available_languages(self):
        """Получить список доступных языков"""
        return list(self.translations.keys())

# 🇷🇺 Русские переводы
RUSSIAN_TRANSLATIONS = {
    # GUI элементы
    'app_title': '🔍 Комплексный анализатор веб-сайтов',
    'url_label': 'URL для анализа:',
    'url_placeholder': 'https://example.com',
    'analysis_type_label': 'Тип анализа:',
    'analyze_button': '🔍 Анализировать',
    'clear_button': '🗑️ Очистить',
    'export_button': '💾 Экспорт',
    'language_label': '🌐 Язык:',
    
    # Типы анализа
    'analysis_protection': 'Защита от парсинга',
    'analysis_structure': 'Структура сайта',
    'analysis_both': 'Полный анализ',
    
    # Вкладки
    'tab_summary': '📋 Сводка',
    'tab_protection': '🔒 Защита',
    'tab_structure': '🏗️ Структура',
    'tab_selectors': '🎯 Селекторы',
    'tab_full_report': '📄 Полный отчет',
    
    # Состояния анализа
    'status_ready': 'Готов к анализу',
    'status_analyzing': 'Анализирую... Пожалуйста, подождите',
    'status_completed': 'Анализ завершен',
    'status_error': 'Ошибка анализа',
    
    # Сообщения
    'enter_url': 'Введите URL для анализа',
    'invalid_url': 'Неверный URL. Введите корректный адрес',
    'analysis_complete': 'Анализ завершен успешно!',
    'analysis_error': 'Ошибка при анализе: {error}',
    'export_success': 'Результаты экспортированы в {filename}',
    'export_error': 'Ошибка экспорта: {error}',
    
    # Защита от парсинга
    'protection_level': 'Уровень защиты',
    'protection_low': 'НИЗКИЙ',
    'protection_medium': 'СРЕДНИЙ',
    'protection_high': 'ВЫСОКИЙ',
    'protection_critical': 'КРИТИЧЕСКИЙ',
    'protection_score': 'Балл защиты: {score}/100',
    
    'cloudflare_detected': 'Обнаружен Cloudflare',
    'javascript_required': 'Требуется JavaScript',
    'rate_limiting': 'Ограничение частоты запросов',
    'user_agent_blocking': 'Блокировка User-Agent',
    'captcha_detected': 'Обнаружена капча',
    'cookies_required': 'Требуются cookies',
    
    # Методы обхода
    'bypass_methods': 'Рекомендуемые методы обхода',
    'bypass_requests': 'Простые HTTP запросы (requests)',
    'bypass_cloudscraper': 'CloudScraper для обхода Cloudflare',
    'bypass_selenium': 'Selenium WebDriver',
    'bypass_undetected': 'Undetected Chrome Driver',
    'bypass_proxy': 'Прокси-серверы',
    
    # Структура сайта
    'dom_structure': 'DOM структура',
    'total_elements': 'Всего элементов: {count}',
    'unique_tags': 'Уникальных тегов: {count}',
    'classes_count': 'CSS классов: {count}',
    'ids_count': 'ID элементов: {count}',
    'forms_count': 'Форм: {count}',
    'links_count': 'Ссылок: {count}',
    'images_count': 'Изображений: {count}',
    
    # Типы контента
    'content_types': 'Типы контента',
    'products_detected': 'Товары обнаружены',
    'articles_detected': 'Статьи обнаружены',
    'navigation_detected': 'Навигация обнаружена',
    'forms_detected': 'Формы обнаружены',
    'pagination_detected': 'Пагинация обнаружена',
    
    # Селекторы
    'suggested_selectors': 'Рекомендуемые селекторы',
    'selector_products': 'Товары',
    'selector_prices': 'Цены',
    'selector_titles': 'Заголовки',
    'selector_descriptions': 'Описания',
    'selector_links': 'Ссылки',
    'selector_images': 'Изображения',
    
    # Рекомендации
    'recommendations': 'Рекомендации',
    'complexity_assessment': 'Оценка сложности парсинга',
    'recommended_tools': 'Рекомендуемые инструменты',
    'estimated_time': 'Ориентировочное время разработки',
    
    # Экспорт
    'export_format': 'Формат экспорта',
    'export_json': 'JSON отчет',
    'export_text': 'Текстовый отчет',
    'export_csv': 'CSV данные',
    
    # Ошибки и предупреждения
    'connection_error': 'Ошибка подключения к сайту',
    'timeout_error': 'Превышено время ожидания',
    'access_denied': 'Доступ запрещен',
    'server_error': 'Ошибка сервера',
    'unknown_error': 'Неизвестная ошибка',
    
    # Языки
    'russian': 'Русский',
    'english': 'English',
}

# 🇺🇸 English translations
ENGLISH_TRANSLATIONS = {
    # GUI elements
    'app_title': '🔍 Comprehensive Website Analyzer',
    'url_label': 'URL to analyze:',
    'url_placeholder': 'https://example.com',
    'analysis_type_label': 'Analysis type:',
    'analyze_button': '🔍 Analyze',
    'clear_button': '🗑️ Clear',
    'export_button': '💾 Export',
    'language_label': '🌐 Language:',
    
    # Analysis types
    'analysis_protection': 'Anti-scraping protection',
    'analysis_structure': 'Website structure',
    'analysis_both': 'Full analysis',
    
    # Tabs
    'tab_summary': '📋 Summary',
    'tab_protection': '🔒 Protection',
    'tab_structure': '🏗️ Structure',
    'tab_selectors': '🎯 Selectors',
    'tab_full_report': '📄 Full Report',
    
    # Analysis states
    'status_ready': 'Ready to analyze',
    'status_analyzing': 'Analyzing... Please wait',
    'status_completed': 'Analysis completed',
    'status_error': 'Analysis error',
    
    # Messages
    'enter_url': 'Enter URL to analyze',
    'invalid_url': 'Invalid URL. Please enter a valid address',
    'analysis_complete': 'Analysis completed successfully!',
    'analysis_error': 'Analysis error: {error}',
    'export_success': 'Results exported to {filename}',
    'export_error': 'Export error: {error}',
    
    # Protection levels
    'protection_level': 'Protection Level',
    'protection_low': 'LOW',
    'protection_medium': 'MEDIUM',
    'protection_high': 'HIGH',
    'protection_critical': 'CRITICAL',
    'protection_score': 'Protection Score: {score}/100',
    
    'cloudflare_detected': 'Cloudflare detected',
    'javascript_required': 'JavaScript required',
    'rate_limiting': 'Rate limiting detected',
    'user_agent_blocking': 'User-Agent blocking',
    'captcha_detected': 'CAPTCHA detected',
    'cookies_required': 'Cookies required',
    
    # Bypass methods
    'bypass_methods': 'Recommended bypass methods',
    'bypass_requests': 'Simple HTTP requests (requests)',
    'bypass_cloudscraper': 'CloudScraper for Cloudflare bypass',
    'bypass_selenium': 'Selenium WebDriver',
    'bypass_undetected': 'Undetected Chrome Driver',
    'bypass_proxy': 'Proxy servers',
    
    # Website structure
    'dom_structure': 'DOM Structure',
    'total_elements': 'Total elements: {count}',
    'unique_tags': 'Unique tags: {count}',
    'classes_count': 'CSS classes: {count}',
    'ids_count': 'Element IDs: {count}',
    'forms_count': 'Forms: {count}',
    'links_count': 'Links: {count}',
    'images_count': 'Images: {count}',
    
    # Content types
    'content_types': 'Content Types',
    'products_detected': 'Products detected',
    'articles_detected': 'Articles detected',
    'navigation_detected': 'Navigation detected',
    'forms_detected': 'Forms detected',
    'pagination_detected': 'Pagination detected',
    
    # Selectors
    'suggested_selectors': 'Suggested Selectors',
    'selector_products': 'Products',
    'selector_prices': 'Prices',
    'selector_titles': 'Titles',
    'selector_descriptions': 'Descriptions',
    'selector_links': 'Links',
    'selector_images': 'Images',
    
    # Recommendations
    'recommendations': 'Recommendations',
    'complexity_assessment': 'Scraping complexity assessment',
    'recommended_tools': 'Recommended tools',
    'estimated_time': 'Estimated development time',
    
    # Export
    'export_format': 'Export format',
    'export_json': 'JSON report',
    'export_text': 'Text report',
    'export_csv': 'CSV data',
    
    # Errors and warnings
    'connection_error': 'Connection error to website',
    'timeout_error': 'Request timeout',
    'access_denied': 'Access denied',
    'server_error': 'Server error',
    'unknown_error': 'Unknown error',
    
    # Languages
    'russian': 'Русский',
    'english': 'English',
}

# Глобальный экземпляр менеджера языков
language_manager = LanguageManager()

def get_text(key, **kwargs):
    """Удобная функция для получения переведенного текста"""
    return language_manager.get_text(key, **kwargs)

def set_language(language):
    """Удобная функция для установки языка"""
    return language_manager.set_language(language)

def get_current_language():
    """Получить текущий язык"""
    return language_manager.get_current_language()