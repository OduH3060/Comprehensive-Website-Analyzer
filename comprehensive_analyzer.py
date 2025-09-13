#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 КОМПЛЕКСНЫЙ АНАЛИЗАТОР ВЕБ-САЙТОВ С МНОГОЯЗЫЧНОЙ ПОДДЕРЖКОЙ
=============================================================
Главный модуль, объединяющий анализ защиты и структуры сайтов
с поддержкой русского и английского языков

Автор: Senior Python Developer  
Версия: 3.1.0
Дата: 2025-09-14
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from datetime import datetime
import sys
import os
import json

# Импорты модулей анализатора
from protection_analyzer import ProtectionAnalyzer
from structure_analyzer import StructureAnalyzer
from gui_components import AnalyzerGUI
from utils import setup_logging, validate_url
from languages import get_text, set_language, get_current_language

class ComprehensiveWebsiteAnalyzer:
    """Главный класс комплексного анализатора веб-сайтов с многоязычной поддержкой"""

    def __init__(self):
        self.logger = setup_logging()
        self.logger.info(f"{get_text('app_title')} v3.1 - {get_text('status_ready')}")
        
        # Инициализация анализаторов
        self.protection_analyzer = ProtectionAnalyzer()
        self.structure_analyzer = StructureAnalyzer()
        
        # Статистика
        self.analysis_count = 0
        self.start_time = datetime.now()

    def analyze_website(self, url, analysis_type="both", language=None):
        """
        Комплексный анализ веб-сайта
        
        Args:
            url (str): URL для анализа
            analysis_type (str): Тип анализа ("protection", "structure", "both")
            language (str): Язык вывода ("ru", "en") - если None, используется текущий
            
        Returns:
            dict: Результаты анализа
        """
        if language:
            set_language(language)
            
        self.logger.info(f"{get_text('status_analyzing')}: {url}")
        
        # Валидация URL
        if not validate_url(url):
            raise ValueError(get_text('invalid_url'))
        
        results = {
            'url': url,
            'analysis_type': analysis_type,
            'language': get_current_language(),
            'timestamp': datetime.now().isoformat(),
            'version': '3.1.0'
        }
        
        try:
            # Анализ защиты
            if analysis_type in ['protection', 'both']:
                self.logger.info(f"{get_text('tab_protection')} - {get_text('status_analyzing')}")
                protection_results = self.protection_analyzer.analyze(url)
                results['protection'] = protection_results
                
                # Переводим результаты защиты
                results['protection'] = self._translate_protection_results(protection_results)
            
            # Анализ структуры
            if analysis_type in ['structure', 'both']:
                self.logger.info(f"{get_text('tab_structure')} - {get_text('status_analyzing')}")
                structure_results = self.structure_analyzer.analyze(url)
                results['structure'] = structure_results
                
                # Переводим результаты структуры
                results['structure'] = self._translate_structure_results(structure_results)
            
            # Генерация рекомендаций
            results['recommendations'] = self._generate_recommendations(results)
            results['summary'] = self._generate_summary(results)
            
            self.analysis_count += 1
            self.logger.info(f"{get_text('analysis_complete')} ({self.analysis_count})")
            
            return results
            
        except Exception as e:
            error_msg = get_text('analysis_error').format(error=str(e))
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def _translate_protection_results(self, results):
        """Перевод результатов анализа защиты"""
        translated = results.copy()
        
        # Переводим уровень сложности
        if 'complexity_level' in translated:
            level_map = {
                'LOW': get_text('protection_low'),
                'MEDIUM': get_text('protection_medium'), 
                'HIGH': get_text('protection_high'),
                'CRITICAL': get_text('protection_critical')
            }
            translated['complexity_level_localized'] = level_map.get(
                translated['complexity_level'], 
                translated['complexity_level']
            )
        
        # Переводим методы обхода
        if 'bypass_methods' in translated:
            bypass_map = {
                'requests': get_text('bypass_requests'),
                'cloudscraper': get_text('bypass_cloudscraper'),
                'selenium': get_text('bypass_selenium'),
                'undetected': get_text('bypass_undetected'),
                'proxy': get_text('bypass_proxy')
            }
            
            translated['bypass_methods_localized'] = []
            for method in translated['bypass_methods']:
                localized = bypass_map.get(method, method)
                translated['bypass_methods_localized'].append(localized)
        
        # Переводим детекции защиты
        protection_map = {
            'cloudflare_detected': get_text('cloudflare_detected'),
            'javascript_required': get_text('javascript_required'),
            'rate_limiting': get_text('rate_limiting'),
            'user_agent_blocking': get_text('user_agent_blocking'),
            'captcha_detected': get_text('captcha_detected'),
            'cookies_required': get_text('cookies_required')
        }
        
        translated['protection_details_localized'] = {}
        for key, value in translated.get('protection_details', {}).items():
            localized_key = protection_map.get(key, key)
            translated['protection_details_localized'][localized_key] = value
            
        return translated

    def _translate_structure_results(self, results):
        """Перевод результатов анализа структуры"""
        translated = results.copy()
        
        # Переводим типы контента
        if 'content_types' in translated:
            content_map = {
                'products': get_text('products_detected'),
                'articles': get_text('articles_detected'),
                'navigation': get_text('navigation_detected'),
                'forms': get_text('forms_detected'),
                'pagination': get_text('pagination_detected')
            }
            
            translated['content_types_localized'] = {}
            for content_type, detected in translated['content_types'].items():
                localized_type = content_map.get(content_type, content_type)
                translated['content_types_localized'][localized_type] = detected
        
        # Переводим статистику DOM
        if 'dom_stats' in translated:
            dom_stats = translated['dom_stats']
            translated['dom_stats_localized'] = {
                get_text('total_elements'): dom_stats.get('total_elements', 0),
                get_text('unique_tags'): dom_stats.get('unique_tags', 0),
                get_text('classes_count'): dom_stats.get('classes_count', 0),
                get_text('ids_count'): dom_stats.get('ids_count', 0),
                get_text('forms_count'): dom_stats.get('forms_count', 0),
                get_text('links_count'): dom_stats.get('links_count', 0),
                get_text('images_count'): dom_stats.get('images_count', 0)
            }
        
        # Переводим селекторы
        if 'suggested_selectors' in translated:
            selector_map = {
                'products': get_text('selector_products'),
                'prices': get_text('selector_prices'),
                'titles': get_text('selector_titles'),
                'descriptions': get_text('selector_descriptions'),
                'links': get_text('selector_links'),
                'images': get_text('selector_images')
            }
            
            translated['suggested_selectors_localized'] = {}
            for selector_type, selectors in translated['suggested_selectors'].items():
                localized_type = selector_map.get(selector_type, selector_type)
                translated['suggested_selectors_localized'][localized_type] = selectors
                
        return translated

    def _generate_recommendations(self, results):
        """Генерация рекомендаций на текущем языке"""
        recommendations = []
        
        # Рекомендации по защите
        if 'protection' in results:
            protection = results['protection']
            complexity_score = protection.get('complexity_score', 0)
            
            if complexity_score < 40:
                if get_current_language() == 'ru':
                    recommendations.append("✅ Простой парсинг: используйте requests + BeautifulSoup")
                    recommendations.append("🔧 Добавьте User-Agent заголовки для стабильности")
                else:
                    recommendations.append("✅ Simple scraping: use requests + BeautifulSoup")
                    recommendations.append("🔧 Add User-Agent headers for stability")
                    
            elif complexity_score < 60:
                if get_current_language() == 'ru':
                    recommendations.append("⚠️ Средняя сложность: требуется cloudscraper или fake-useragent")
                    recommendations.append("🛡️ Добавьте задержки между запросами")
                else:
                    recommendations.append("⚠️ Medium complexity: requires cloudscraper or fake-useragent")
                    recommendations.append("🛡️ Add delays between requests")
                    
            elif complexity_score < 80:
                if get_current_language() == 'ru':
                    recommendations.append("🚨 Высокая сложность: обязательно Selenium или undetected-chrome")
                    recommendations.append("🔄 Используйте ротацию прокси и User-Agent")
                else:
                    recommendations.append("🚨 High complexity: mandatory Selenium or undetected-chrome")
                    recommendations.append("🔄 Use proxy and User-Agent rotation")
                    
            else:
                if get_current_language() == 'ru':
                    recommendations.append("💥 Критическая защита: нужны продвинутые методы обхода")
                    recommendations.append("🤖 Рассмотрите использование капча-сервисов")
                    recommendations.append("⏱️ Значительные задержки и ручная обработка")
                else:
                    recommendations.append("💥 Critical protection: need advanced bypass methods")
                    recommendations.append("🤖 Consider using captcha-solving services")
                    recommendations.append("⏱️ Significant delays and manual processing")
        
        # Рекомендации по структуре
        if 'structure' in results:
            structure = results['structure']
            
            if structure.get('content_types', {}).get('products'):
                if get_current_language() == 'ru':
                    recommendations.append("🛒 Обнаружены товары: используйте готовые селекторы")
                else:
                    recommendations.append("🛒 Products detected: use provided selectors")
            
            if structure.get('content_types', {}).get('pagination'):
                if get_current_language() == 'ru':
                    recommendations.append("📄 Пагинация найдена: автоматизируйте переход по страницам")
                else:
                    recommendations.append("📄 Pagination found: automate page navigation")
        
        return recommendations

    def _generate_summary(self, results):
        """Генерация краткой сводки"""
        summary = {
            'url': results['url'],
            'analysis_time': datetime.now().isoformat(),
            'language': get_current_language()
        }
        
        if 'protection' in results:
            protection = results['protection']
            summary['protection_level'] = protection.get('complexity_level', 'UNKNOWN')
            summary['protection_score'] = protection.get('complexity_score', 0)
            summary['protection_level_localized'] = protection.get('complexity_level_localized', 'UNKNOWN')
        
        if 'structure' in results:
            structure = results['structure']
            summary['dom_elements'] = structure.get('dom_stats', {}).get('total_elements', 0)
            summary['content_types_found'] = len([
                k for k, v in structure.get('content_types', {}).items() if v
            ])
            summary['selectors_generated'] = sum([
                len(v) for v in structure.get('suggested_selectors', {}).values()
            ])
        
        # Оценка сложности парсинга
        complexity_score = results.get('protection', {}).get('complexity_score', 0)
        
        if complexity_score < 40:
            difficulty = get_text('protection_low')
            time_estimate = "1-2 " + ("дня" if get_current_language() == 'ru' else "days")
        elif complexity_score < 60:
            difficulty = get_text('protection_medium')
            time_estimate = "3-5 " + ("дней" if get_current_language() == 'ru' else "days")
        elif complexity_score < 80:
            difficulty = get_text('protection_high')
            time_estimate = "1-2 " + ("недели" if get_current_language() == 'ru' else "weeks")
        else:
            difficulty = get_text('protection_critical')
            time_estimate = "2+ " + ("недели" if get_current_language() == 'ru' else "weeks")
        
        summary['scraping_difficulty'] = difficulty
        summary['estimated_development_time'] = time_estimate
        
        return summary

    def export_results(self, filename, results, format='json'):
        """
        Экспорт результатов в файл
        
        Args:
            filename (str): Имя файла
            results (dict): Результаты анализа
            format (str): Формат экспорта ('json', 'txt')
        """
        try:
            if format == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
            
            elif format == 'txt':
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"{get_text('app_title')} v3.1\n")
                    f.write("=" * 50 + "\n\n")
                    
                    f.write(f"URL: {results['url']}\n")
                    f.write(f"{get_text('analysis_type_label')}: {results['analysis_type']}\n")
                    f.write(f"{get_text('language_label')}: {results['language']}\n")
                    f.write(f"Timestamp: {results['timestamp']}\n\n")
                    
                    if 'protection' in results:
                        f.write(f"{get_text('tab_protection')}:\n")
                        f.write("-" * 20 + "\n")
                        protection = results['protection']
                        f.write(f"{get_text('protection_level')}: {protection.get('complexity_level_localized', 'N/A')}\n")
                        f.write(f"{get_text('protection_score').format(score=protection.get('complexity_score', 0))}\n\n")
                    
                    if 'structure' in results:
                        f.write(f"{get_text('tab_structure')}:\n")
                        f.write("-" * 20 + "\n")
                        structure = results['structure']
                        dom_stats = structure.get('dom_stats_localized', {})
                        for stat_name, value in dom_stats.items():
                            f.write(f"{stat_name.format(count=value)}\n")
                        f.write("\n")
                    
                    if 'recommendations' in results:
                        f.write(f"{get_text('recommendations')}:\n")
                        f.write("-" * 20 + "\n")
                        for rec in results['recommendations']:
                            f.write(f"• {rec}\n")
            
            self.logger.info(get_text('export_success').format(filename=filename))
            
        except Exception as e:
            error_msg = get_text('export_error').format(error=str(e))
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def get_statistics(self):
        """Получение статистики работы"""
        uptime = datetime.now() - self.start_time
        
        stats = {
            'analysis_count': self.analysis_count,
            'uptime_seconds': uptime.total_seconds(),
            'current_language': get_current_language(),
            'version': '3.1.0'
        }
        
        return stats

def main():
    """Главная функция запуска приложения"""
    try:
        # Создание главного окна
        root = tk.Tk()
        
        # Создание анализатора
        analyzer = ComprehensiveWebsiteAnalyzer()
        
        # Создание GUI
        gui = AnalyzerGUI(root, analyzer)
        
        # Запуск приложения
        analyzer.logger.info(f"{get_text('app_title')} {get_text('status_ready')}")
        root.mainloop()
        
    except Exception as e:
        error_msg = f"Critical error: {str(e)}"
        print(error_msg)
        if 'messagebox' in globals():
            messagebox.showerror("Critical Error", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()