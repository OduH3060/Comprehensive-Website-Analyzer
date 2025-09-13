#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏗️ МОДУЛЬ АНАЛИЗА СТРУКТУРЫ САЙТА
=================================
Анализ DOM структуры, селекторов и контента веб-сайтов

Автор: Senior Python Developer
Версия: 3.0.0
"""

import requests
from bs4 import BeautifulSoup, Comment
import re
from urllib.parse import urljoin, urlparse
from collections import Counter, defaultdict
import time

try:
    from fake_useragent import UserAgent
    UA_AVAILABLE = True
except ImportError:
    UA_AVAILABLE = False

class StructureAnalyzer:
    """Анализатор структуры веб-сайтов"""
    
    def __init__(self):
        self.ua = UserAgent() if UA_AVAILABLE else None
        self.session = requests.Session()
        
    def get_headers(self):
        """Получение заголовков для запросов"""
        if self.ua:
            user_agent = self.ua.random
        else:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        
        return {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def get_page_content(self, url: str) -> BeautifulSoup:
        """Получение и парсинг содержимого страницы"""
        try:
            response = self.session.get(url, headers=self.get_headers(), timeout=30)
            response.raise_for_status()
            
            # Определяем кодировку
            if response.encoding.lower() in ['iso-8859-1', 'windows-1252']:
                response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except Exception as e:
            raise Exception(f"Ошибка загрузки страницы: {e}")
    
    def analyze_basic_info(self, soup: BeautifulSoup) -> dict:
        """Анализ базовой информации страницы"""
        
        # Заголовок
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        # Мета-описание
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_desc_text = meta_desc.get('content', '') if meta_desc else ""
        
        # Язык
        html_tag = soup.find('html')
        language = html_tag.get('lang', 'unknown') if html_tag else 'unknown'
        
        # Кодировка
        meta_charset = soup.find('meta', attrs={'charset': True})
        if not meta_charset:
            meta_charset = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
            
        charset = 'unknown'
        if meta_charset:
            if meta_charset.get('charset'):
                charset = meta_charset.get('charset')
            elif meta_charset.get('content'):
                content = meta_charset.get('content', '')
                match = re.search(r'charset=([^;]+)', content)
                if match:
                    charset = match.group(1)
        
        return {
            'title': title_text,
            'meta_description': meta_desc_text,
            'language': language,
            'charset': charset
        }
    
    def analyze_dom_structure(self, soup: BeautifulSoup) -> dict:
        """Анализ DOM структуры"""
        
        # Получаем все элементы
        all_elements = soup.find_all()
        
        # Подсчет тегов
        tags = [elem.name for elem in all_elements if elem.name]
        unique_tags = list(set(tags))
        tag_counts = Counter(tags)
        
        # Подсчет классов и ID
        all_classes = []
        all_ids = []
        
        for elem in all_elements:
            if elem.get('class'):
                all_classes.extend(elem.get('class'))
            if elem.get('id'):
                all_ids.append(elem.get('id'))
        
        class_counts = Counter(all_classes)
        
        # Анализ глубины вложенности
        max_depth = self.calculate_max_depth(soup)
        
        # Семантические HTML5 теги
        semantic_tags = ['article', 'section', 'nav', 'header', 'footer', 'main', 'aside', 'figure']
        has_semantic = any(tag in unique_tags for tag in semantic_tags)
        
        return {
            'total_elements': len(all_elements),
            'unique_tags': sorted(unique_tags),
            'tag_distribution': dict(tag_counts.most_common(20)),
            'classes_count': len(set(all_classes)),
            'ids_count': len(set(all_ids)),
            'popular_classes': dict(class_counts.most_common(20)),
            'max_nesting_depth': max_depth,
            'has_semantic_html5': has_semantic,
            'semantic_tags_found': [tag for tag in semantic_tags if tag in unique_tags]
        }
    
    def calculate_max_depth(self, element, current_depth=0):
        """Вычисление максимальной глубины вложенности"""
        max_depth = current_depth
        
        for child in element.children:
            if hasattr(child, 'children'):
                child_depth = self.calculate_max_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
        
        return max_depth
    
    def detect_content_types(self, soup: BeautifulSoup) -> dict:
        """Детекция типов контента"""
        
        content_types = {}
        
        # Паттерны для поиска разных типов контента
        patterns = {
            'products': {
                'selectors': [
                    '[class*="product"]', '[class*="item"]', '[class*="card"]',
                    '[data-product]', '[data-item]', '[itemtype*="Product"]',
                    '[class*="goods"]', '[class*="catalog"]'
                ],
                'keywords': ['price', 'buy', 'cart', 'product', 'item', 'товар', 'цена']
            },
            'articles': {
                'selectors': [
                    'article', '[class*="article"]', '[class*="post"]',
                    '[class*="news"]', '[class*="blog"]', '[class*="content"]'
                ],
                'keywords': ['read', 'article', 'post', 'news', 'blog', 'статья', 'новости']
            },
            'navigation': {
                'selectors': [
                    'nav', '[class*="nav"]', '[class*="menu"]',
                    '[class*="breadcrumb"]', '[role="navigation"]',
                    'ul.menu', 'ul.nav'
                ],
                'keywords': ['menu', 'navigation', 'nav', 'breadcrumb', 'меню', 'навигация']
            },
            'forms': {
                'selectors': [
                    'form', '[class*="form"]', '[class*="search"]',
                    '[class*="contact"]', '[class*="subscribe"]', 'input', 'textarea'
                ],
                'keywords': ['form', 'search', 'contact', 'subscribe', 'login', 'форма', 'поиск']
            },
            'lists': {
                'selectors': [
                    '[class*="list"]', '[class*="grid"]', '[class*="catalog"]',
                    'ul', 'ol', '[class*="items"]', 'table'
                ],
                'keywords': ['list', 'grid', 'catalog', 'items', 'collection', 'список', 'каталог']
            },
            'media': {
                'selectors': [
                    'img', 'video', 'audio', '[class*="image"]',
                    '[class*="photo"]', '[class*="gallery"]', 'picture'
                ],
                'keywords': ['image', 'photo', 'gallery', 'video', 'media', 'изображение', 'фото']
            },
            'text_content': {
                'selectors': [
                    'p', 'div', 'span', '[class*="text"]',
                    '[class*="description"]', '[class*="content"]'
                ],
                'keywords': ['text', 'description', 'content', 'paragraph', 'текст', 'описание']
            }
        }
        
        for content_type, config in patterns.items():
            elements_found = set()
            
            # Поиск по CSS селекторам
            for selector in config['selectors']:
                try:
                    found = soup.select(selector)
                    elements_found.update(found)
                except Exception:
                    continue
            
            # Поиск по ключевым словам в классах и тексте
            for keyword in config['keywords']:
                # В классах
                class_elements = soup.find_all(attrs={'class': re.compile(keyword, re.I)})
                elements_found.update(class_elements)
                
                # В ID
                id_elements = soup.find_all(attrs={'id': re.compile(keyword, re.I)})
                elements_found.update(id_elements)
            
            content_types[content_type] = len(elements_found)
        
        return content_types
    
    def analyze_links_and_forms(self, soup: BeautifulSoup, base_url: str) -> dict:
        """Анализ ссылок и форм"""
        
        # Анализ ссылок
        links = soup.find_all('a', href=True)
        internal_links = []
        external_links = []
        
        base_domain = urlparse(base_url).netloc
        
        for link in links:
            href = link.get('href', '')
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue
                
            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)
            
            if parsed_url.netloc == base_domain or not parsed_url.netloc:
                internal_links.append(full_url)
            else:
                external_links.append(full_url)
        
        # Удаляем дубликаты
        internal_links = list(set(internal_links))
        external_links = list(set(external_links))
        
        # Анализ форм
        forms = []
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'GET').upper(),
                'inputs_count': len(form.find_all(['input', 'select', 'textarea'])),
                'has_file_upload': bool(form.find('input', type='file')),
                'classes': form.get('class', []),
                'id': form.get('id', '')
            }
            
            # Анализ полей формы
            inputs = []
            for input_elem in form.find_all(['input', 'select', 'textarea']):
                input_data = {
                    'tag': input_elem.name,
                    'type': input_elem.get('type', ''),
                    'name': input_elem.get('name', ''),
                    'placeholder': input_elem.get('placeholder', ''),
                    'required': input_elem.has_attr('required')
                }
                inputs.append(input_data)
            
            form_data['inputs'] = inputs
            forms.append(form_data)
        
        return {
            'internal_links': internal_links,
            'external_links': external_links,
            'forms': forms,
            'internal_links_count': len(internal_links),
            'external_links_count': len(external_links),
            'forms_count': len(forms)
        }
    
    def analyze_scripts_and_styles(self, soup: BeautifulSoup) -> dict:
        """Анализ скриптов и стилей"""
        
        # Анализ JavaScript
        scripts = []
        for script in soup.find_all('script'):
            script_info = {
                'src': script.get('src', ''),
                'inline': bool(script.string and script.string.strip()),
                'type': script.get('type', 'text/javascript'),
                'async': script.has_attr('async'),
                'defer': script.has_attr('defer')
            }
            scripts.append(script_info)
        
        # Анализ CSS
        styles = []
        for link in soup.find_all('link', rel='stylesheet'):
            style_info = {
                'href': link.get('href', ''),
                'media': link.get('media', 'all'),
                'type': link.get('type', 'text/css')
            }
            styles.append(style_info)
        
        # Inline стили
        inline_styles = len(soup.find_all(attrs={'style': True}))
        
        # Поиск фреймворков
        page_content = str(soup).lower()
        frameworks = {
            'jquery': 'jquery' in page_content,
            'react': 'react' in page_content or '_react' in page_content,
            'vue': 'vue.js' in page_content or 'vue.min.js' in page_content,
            'angular': 'angular' in page_content,
            'bootstrap': 'bootstrap' in page_content,
            'foundation': 'foundation' in page_content
        }
        
        return {
            'scripts': scripts,
            'scripts_count': len(scripts),
            'external_scripts': len([s for s in scripts if s['src']]),
            'inline_scripts': len([s for s in scripts if s['inline']]),
            'styles': styles,
            'styles_count': len(styles),
            'inline_styles_count': inline_styles,
            'frameworks_detected': {k: v for k, v in frameworks.items() if v}
        }
    
    def generate_selectors(self, soup: BeautifulSoup, content_types: dict) -> dict:
        """Генерация оптимизированных селекторов"""
        
        selectors = {}
        
        # Селекторы для разных типов контента
        content_patterns = {
            'products': ['[class*="product"]', '[class*="item"]', '[class*="card"]'],
            'articles': ['article', '[class*="article"]', '[class*="post"]'],
            'navigation': ['nav', '[class*="menu"]', '[class*="nav"]'],
            'forms': ['form', '[class*="form"]'],
            'lists': ['ul', 'ol', '[class*="list"]']
        }
        
        for content_type, patterns in content_patterns.items():
            type_selectors = []
            
            for pattern in patterns:
                try:
                    elements = soup.select(pattern)
                    if elements:
                        type_selectors.append({
                            'selector': pattern,
                            'count': len(elements),
                            'sample_text': elements[0].get_text().strip()[:100] if elements else ''
                        })
                except Exception:
                    continue
            
            if type_selectors:
                selectors[content_type] = sorted(type_selectors, key=lambda x: x['count'], reverse=True)
        
        # Общие полезные селекторы
        common_selectors = {
            'all_links': 'a[href]',
            'all_images': 'img[src]',
            'all_forms': 'form',
            'all_inputs': 'input, textarea, select',
            'headings': 'h1, h2, h3, h4, h5, h6',
            'paragraphs': 'p',
            'lists': 'ul, ol',
            'tables': 'table'
        }
        
        for name, selector in common_selectors.items():
            try:
                elements = soup.select(selector)
                if elements:
                    selectors[f'common_{name}'] = [{
                        'selector': selector,
                        'count': len(elements),
                        'description': f'Все {name.replace("_", " ")}'
                    }]
            except Exception:
                continue
        
        return selectors
    
    def analyze_performance_indicators(self, soup: BeautifulSoup) -> dict:
        """Анализ индикаторов производительности"""
        
        # Размер страницы
        page_size = len(str(soup))
        
        # Количество элементов разных типов
        images_count = len(soup.find_all('img'))
        scripts_count = len(soup.find_all('script'))
        styles_count = len(soup.find_all('link', rel='stylesheet'))
        
        # Внешние ресурсы
        external_resources = 0
        for elem in soup.find_all(['img', 'script', 'link']):
            src = elem.get('src') or elem.get('href', '')
            if src and (src.startswith('http') or src.startswith('//')):
                external_resources += 1
        
        # Оценка сложности
        complexity_score = (
            min(page_size / 1000, 100) +  # Размер страницы
            min(images_count * 2, 50) +   # Изображения
            min(scripts_count * 3, 50) +  # Скрипты
            min(external_resources, 50)   # Внешние ресурсы
        ) / 4
        
        return {
            'page_size_bytes': page_size,
            'images_count': images_count,
            'scripts_count': scripts_count,
            'styles_count': styles_count,
            'external_resources': external_resources,
            'complexity_score': round(complexity_score, 1),
            'loading_complexity': 'HIGH' if complexity_score > 70 else 'MEDIUM' if complexity_score > 40 else 'LOW'
        }
    
    def analyze(self, url: str) -> dict:
        """Главный метод анализа структуры"""
        
        results = {
            'url': url,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_type': 'structure'
        }
        
        try:
            # Получаем содержимое страницы
            soup = self.get_page_content(url)
            
            # Базовая информация
            basic_info = self.analyze_basic_info(soup)
            results.update(basic_info)
            
            # DOM структура
            dom_structure = self.analyze_dom_structure(soup)
            results.update(dom_structure)
            
            # Типы контента
            content_types = self.detect_content_types(soup)
            results['content_types'] = content_types
            
            # Ссылки и формы
            links_forms = self.analyze_links_and_forms(soup, url)
            results.update(links_forms)
            
            # Скрипты и стили
            scripts_styles = self.analyze_scripts_and_styles(soup)
            results['scripts'] = scripts_styles['scripts']
            results['styles'] = scripts_styles['styles']
            results['frameworks_detected'] = scripts_styles['frameworks_detected']
            
            # Селекторы
            selectors = self.generate_selectors(soup, content_types)
            results['suggested_selectors'] = selectors
            
            # Индикаторы производительности
            performance = self.analyze_performance_indicators(soup)
            results['performance'] = performance
            
            # Общая оценка сложности парсинга
            parsing_complexity = self.evaluate_parsing_complexity(results)
            results['parsing_complexity'] = parsing_complexity
            
            return results
            
        except Exception as e:
            results['error'] = str(e)
            results['success'] = False
            return results
    
    def evaluate_parsing_complexity(self, results: dict) -> dict:
        """Оценка сложности парсинга"""
        
        complexity_factors = []
        score = 0
        
        # JavaScript сложность
        js_count = len(results.get('scripts', []))
        if js_count > 10:
            complexity_factors.append("Много JavaScript файлов")
            score += 30
        elif js_count > 5:
            score += 15
        
        # Фреймворки
        frameworks = results.get('frameworks_detected', {})
        if frameworks:
            complexity_factors.append(f"Обнаружены фреймворки: {', '.join(frameworks.keys())}")
            score += 25
        
        # Формы
        forms_count = results.get('forms_count', 0)
        if forms_count > 3:
            complexity_factors.append("Много форм - может потребоваться аутентификация")
            score += 15
        
        # Внешние ресурсы
        performance = results.get('performance', {})
        if performance.get('loading_complexity') == 'HIGH':
            complexity_factors.append("Высокая сложность загрузки")
            score += 20
        
        # Глубина вложенности
        if results.get('max_nesting_depth', 0) > 15:
            complexity_factors.append("Глубокая вложенность DOM")
            score += 10
        
        # Определение уровня сложности
        if score >= 70:
            level = 'VERY_HIGH'
            recommendation = 'Selenium или Playwright обязательны'
        elif score >= 50:
            level = 'HIGH'
            recommendation = 'Рекомендуется Selenium'
        elif score >= 30:
            level = 'MEDIUM'
            recommendation = 'Requests + BeautifulSoup с осторожностью'
        else:
            level = 'LOW'
            recommendation = 'Простой requests + BeautifulSoup'
        
        return {
            'score': score,
            'level': level,
            'factors': complexity_factors,
            'recommendation': recommendation,
            'estimated_effort': {
                'VERY_HIGH': 'Очень высокие',
                'HIGH': 'Высокие', 
                'MEDIUM': 'Средние',
                'LOW': 'Низкие'
            }.get(level, 'Неизвестно')
        }
    
    def cleanup(self):
        """Очистка ресурсов"""
        if hasattr(self.session, 'close'):
            self.session.close()