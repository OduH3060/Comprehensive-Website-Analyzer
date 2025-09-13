#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 МОДУЛЬ АНАЛИЗА ЗАЩИТЫ ОТ ПАРСИНГА
===================================
Анализ механизмов защиты веб-сайтов от парсинга

Автор: Senior Python Developer
Версия: 3.0.0
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import random
from difflib import SequenceMatcher
import re
from urllib.parse import urlparse

try:
    from fake_useragent import UserAgent
    UA_AVAILABLE = True
except ImportError:
    UA_AVAILABLE = False

try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False

try:
    import undetected_chromedriver as uc
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

class ProtectionAnalyzer:
    """Анализатор защиты от парсинга"""
    
    def __init__(self):
        self.ua = UserAgent() if UA_AVAILABLE else None
        self.session = self.create_session()
        self.driver = None
        
    def create_session(self):
        """Создание HTTP сессии с retry стратегией"""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def get_random_headers(self):
        """Получение случайных заголовков"""
        if self.ua:
            user_agent = self.ua.random
        else:
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            ]
            user_agent = random.choice(user_agents)
        
        return {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def check_basic_access(self, url: str) -> dict:
        """Проверка базового доступа к сайту"""
        try:
            response = self.session.get(url, headers=self.get_random_headers(), timeout=15)
            
            return {
                'status_code': response.status_code,
                'accessible': response.status_code == 200,
                'content_length': len(response.content),
                'response_time': response.elapsed.total_seconds(),
                'headers': dict(response.headers)
            }
        except Exception as e:
            return {
                'status_code': 0,
                'accessible': False,
                'error': str(e),
                'content_length': 0,
                'response_time': 0,
                'headers': {}
            }
    
    def check_user_agent_protection(self, url: str) -> dict:
        """Проверка защиты по User-Agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',  # Обычный браузер
            'Python-requests/2.25.1',  # Requests библиотека
            'curl/7.68.0',  # cURL
            'bot/1.0',  # Очевидный бот
        ]
        
        results = []
        
        for ua in user_agents:
            try:
                headers = self.get_random_headers()
                headers['User-Agent'] = ua
                
                response = self.session.get(url, headers=headers, timeout=10)
                
                results.append({
                    'user_agent': ua,
                    'status_code': response.status_code,
                    'content_length': len(response.content),
                    'blocked': response.status_code in [403, 429, 503]
                })
                
                time.sleep(1)  # Пауза между запросами
                
            except Exception as e:
                results.append({
                    'user_agent': ua,
                    'status_code': 0,
                    'content_length': 0,
                    'blocked': True,
                    'error': str(e)
                })
        
        # Анализ результатов
        blocked_count = sum(1 for r in results if r['blocked'])
        
        return {
            'results': results,
            'protection_detected': blocked_count > 0,
            'protection_strength': blocked_count / len(results),
            'description': f"Заблокировано {blocked_count} из {len(results)} User-Agent"
        }
    
    def check_rate_limiting(self, url: str) -> dict:
        """Проверка ограничений скорости"""
        request_count = 10
        delay = 0.2  # 200ms между запросами
        
        results = []
        start_time = time.time()
        
        for i in range(request_count):
            try:
                response = self.session.get(url, headers=self.get_random_headers(), timeout=5)
                
                results.append({
                    'request_num': i + 1,
                    'status_code': response.status_code,
                    'response_time': response.elapsed.total_seconds(),
                    'blocked': response.status_code in [429, 503]
                })
                
                if i < request_count - 1:
                    time.sleep(delay)
                    
            except Exception as e:
                results.append({
                    'request_num': i + 1,
                    'status_code': 0,
                    'response_time': 0,
                    'blocked': True,
                    'error': str(e)
                })
        
        total_time = time.time() - start_time
        blocked_count = sum(1 for r in results if r['blocked'])
        
        return {
            'results': results,
            'total_requests': request_count,
            'blocked_requests': blocked_count,
            'total_time': total_time,
            'requests_per_second': request_count / total_time,
            'protection_detected': blocked_count > 0,
            'description': f"Заблокировано {blocked_count} из {request_count} запросов"
        }
    
    def check_cloudflare_protection(self, url: str) -> dict:
        """Проверка защиты Cloudflare"""
        try:
            response = self.session.get(url, headers=self.get_random_headers(), timeout=15)
            
            # Индикаторы Cloudflare
            cf_indicators = [
                'cloudflare' in response.headers.get('server', '').lower(),
                'cf-ray' in response.headers,
                '__cfduid' in response.headers.get('set-cookie', ''),
                'checking your browser' in response.text.lower(),
                'cloudflare ray id' in response.text.lower(),
                'cf-browser-verification' in response.text
            ]
            
            detected = any(cf_indicators)
            
            return {
                'detected': detected,
                'indicators_found': sum(cf_indicators),
                'server_header': response.headers.get('server', ''),
                'cf_ray': response.headers.get('cf-ray', ''),
                'description': "Cloudflare обнаружен" if detected else "Cloudflare не обнаружен"
            }
            
        except Exception as e:
            return {
                'detected': False,
                'error': str(e),
                'description': "Ошибка проверки Cloudflare"
            }
    
    def check_javascript_protection(self, url: str) -> dict:
        """Проверка JavaScript защиты"""
        try:
            # Запрос без JavaScript (обычный requests)
            response_no_js = self.session.get(url, headers=self.get_random_headers(), timeout=15)
            content_no_js = response_no_js.text
            
            # Если Selenium доступен, делаем запрос с JavaScript
            if SELENIUM_AVAILABLE:
                try:
                    if not self.driver:
                        options = Options()
                        options.add_argument('--headless')
                        options.add_argument('--no-sandbox')
                        options.add_argument('--disable-dev-shm-usage')
                        self.driver = uc.Chrome(options=options)
                    
                    self.driver.get(url)
                    time.sleep(3)  # Ждем загрузки JS
                    content_with_js = self.driver.page_source
                    
                    # Сравниваем содержимое
                    similarity = SequenceMatcher(None, content_no_js, content_with_js).ratio()
                    difference = 1 - similarity
                    
                    return {
                        'js_required': difference > 0.3,  # Более 30% различий
                        'content_difference': difference * 100,
                        'similarity': similarity * 100,
                        'description': f"Контент различается на {difference * 100:.1f}%"
                    }
                    
                except Exception as e:
                    return {
                        'js_required': False,
                        'error': str(e),
                        'description': "Ошибка проверки JavaScript"
                    }
            else:
                # Простая эвристическая проверка
                js_indicators = [
                    len(re.findall(r'<script', content_no_js, re.I)) > 10,
                    'loading' in content_no_js.lower(),
                    'please wait' in content_no_js.lower(),
                    'javascript' in content_no_js.lower(),
                    len(content_no_js) < 1000  # Подозрительно мало контента
                ]
                
                detected = sum(js_indicators) >= 2
                
                return {
                    'js_required': detected,
                    'indicators_found': sum(js_indicators),
                    'description': "JavaScript возможно требуется" if detected else "JavaScript не требуется"
                }
                
        except Exception as e:
            return {
                'js_required': False,
                'error': str(e),
                'description': "Ошибка проверки JavaScript"
            }
    
    def check_captcha_protection(self, url: str) -> dict:
        """Проверка наличия капчи"""
        try:
            response = self.session.get(url, headers=self.get_random_headers(), timeout=15)
            content = response.text.lower()
            
            # Индикаторы капчи
            captcha_indicators = [
                'recaptcha' in content,
                'captcha' in content,
                'hcaptcha' in content,
                'solve the puzzle' in content,
                'verify you are human' in content,
                'geetest' in content
            ]
            
            detected = any(captcha_indicators)
            
            return {
                'detected': detected,
                'indicators_found': sum(captcha_indicators),
                'description': "Капча обнаружена" if detected else "Капча не обнаружена"
            }
            
        except Exception as e:
            return {
                'detected': False,
                'error': str(e),
                'description': "Ошибка проверки капчи"
            }
    
    def check_cookie_requirements(self, url: str) -> dict:
        """Проверка требований к cookies"""
        try:
            # Запрос без cookies
            response_no_cookies = self.session.get(url, headers=self.get_random_headers(), timeout=15)
            
            # Запрос с cookies
            session_with_cookies = requests.Session()
            response_with_cookies = session_with_cookies.get(url, headers=self.get_random_headers(), timeout=15)
            
            cookies_count = len(response_with_cookies.cookies)
            
            return {
                'cookies_used': cookies_count > 0,
                'cookies_count': cookies_count,
                'description': f"Используется {cookies_count} cookies"
            }
            
        except Exception as e:
            return {
                'cookies_used': False,
                'error': str(e),
                'description': "Ошибка проверки cookies"
            }
    
    def test_bypass_methods(self, url: str) -> dict:
        """Тестирование методов обхода защиты"""
        methods = {}
        
        # Обычный requests
        try:
            response = self.session.get(url, headers=self.get_random_headers(), timeout=15)
            methods['requests'] = {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'description': 'Стандартный requests'
            }
        except Exception as e:
            methods['requests'] = {
                'success': False,
                'error': str(e),
                'description': 'Стандартный requests'
            }
        
        # Requests с сессией
        try:
            session = requests.Session()
            response = session.get(url, headers=self.get_random_headers(), timeout=15)
            methods['requests_session'] = {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'description': 'Requests с сессией'
            }
        except Exception as e:
            methods['requests_session'] = {
                'success': False,
                'error': str(e),
                'description': 'Requests с сессией'
            }
        
        # Fake User-Agent
        if UA_AVAILABLE:
            try:
                headers = self.get_random_headers()
                response = self.session.get(url, headers=headers, timeout=15)
                methods['fake_useragent'] = {
                    'success': response.status_code == 200,
                    'status_code': response.status_code,
                    'description': 'Fake User-Agent'
                }
            except Exception as e:
                methods['fake_useragent'] = {
                    'success': False,
                    'error': str(e),
                    'description': 'Fake User-Agent'
                }
        
        # CloudScraper
        if CLOUDSCRAPER_AVAILABLE:
            try:
                scraper = cloudscraper.create_scraper()
                response = scraper.get(url, timeout=15)
                methods['cloudscraper'] = {
                    'success': response.status_code == 200,
                    'status_code': response.status_code,
                    'description': 'CloudScraper'
                }
            except Exception as e:
                methods['cloudscraper'] = {
                    'success': False,
                    'error': str(e),
                    'description': 'CloudScraper'
                }
        
        # Undetected Chrome
        if SELENIUM_AVAILABLE:
            try:
                if not self.driver:
                    options = Options()
                    options.add_argument('--headless')
                    options.add_argument('--no-sandbox')
                    self.driver = uc.Chrome(options=options)
                
                self.driver.get(url)
                time.sleep(2)
                
                methods['undetected_chrome'] = {
                    'success': 'error' not in self.driver.page_source.lower(),
                    'description': 'Undetected Chrome'
                }
            except Exception as e:
                methods['undetected_chrome'] = {
                    'success': False,
                    'error': str(e),
                    'description': 'Undetected Chrome'
                }
        
        return methods
    
    def analyze(self, url: str) -> dict:
        """Главный метод анализа защиты"""
        results = {
            'url': url,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'mechanisms': {},
            'bypass_methods': {},
            'total_score': 0,
            'complexity_level': 'LOW'
        }
        
        # Базовый доступ
        basic_access = self.check_basic_access(url)
        results['mechanisms']['basic_access'] = {
            'detected': basic_access['accessible'],
            'score': 10 if basic_access['accessible'] else 0,
            'description': f"Статус: {basic_access['status_code']}, Размер: {basic_access['content_length']} байт"
        }
        
        if not basic_access['accessible']:
            results['total_score'] = 100
            results['complexity_level'] = 'CRITICAL'
            return results
        
        # User-Agent защита
        ua_protection = self.check_user_agent_protection(url)
        results['mechanisms']['user_agent'] = {
            'detected': ua_protection['protection_detected'],
            'score': 20 if ua_protection['protection_detected'] else 5,
            'description': ua_protection['description']
        }
        
        # Ограничение скорости
        rate_limiting = self.check_rate_limiting(url)
        results['mechanisms']['rate_limiting'] = {
            'detected': rate_limiting['protection_detected'],
            'score': 15 if rate_limiting['protection_detected'] else 5,
            'description': rate_limiting['description']
        }
        
        # Cloudflare
        cloudflare = self.check_cloudflare_protection(url)
        results['mechanisms']['cloudflare'] = {
            'detected': cloudflare['detected'],
            'score': 25 if cloudflare['detected'] else 0,
            'description': cloudflare['description']
        }
        
        # JavaScript
        javascript = self.check_javascript_protection(url)
        results['mechanisms']['javascript'] = {
            'detected': javascript['js_required'],
            'score': 30 if javascript['js_required'] else 10,
            'description': javascript['description']
        }
        
        # Капча
        captcha = self.check_captcha_protection(url)
        results['mechanisms']['captcha'] = {
            'detected': captcha['detected'],
            'score': 40 if captcha['detected'] else 0,
            'description': captcha['description']
        }
        
        # Cookies
        cookies = self.check_cookie_requirements(url)
        results['mechanisms']['cookies'] = {
            'detected': cookies['cookies_used'],
            'score': 10 if cookies['cookies_used'] else 5,
            'description': cookies['description']
        }
        
        # Тестирование методов обхода
        results['bypass_methods'] = self.test_bypass_methods(url)
        
        # Подсчет общего балла
        results['total_score'] = sum(
            mechanism['score'] for mechanism in results['mechanisms'].values()
        )
        
        # Определение уровня сложности
        if results['total_score'] >= 80:
            results['complexity_level'] = 'CRITICAL'
        elif results['total_score'] >= 60:
            results['complexity_level'] = 'HIGH'
        elif results['total_score'] >= 40:
            results['complexity_level'] = 'MEDIUM'
        else:
            results['complexity_level'] = 'LOW'
        
        # Лучший метод обхода
        successful_methods = [
            method for method, data in results['bypass_methods'].items()
            if data.get('success', False)
        ]
        
        if successful_methods:
            results['best_method'] = successful_methods[0]
            results['bypass_success_rate'] = len(successful_methods) / len(results['bypass_methods']) * 100
        else:
            results['best_method'] = 'selenium'
            results['bypass_success_rate'] = 0
        
        return results
    
    def cleanup(self):
        """Очистка ресурсов"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None