#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖥️ МОДУЛЬ GUI КОМПОНЕНТОВ С МНОГОЯЗЫЧНОЙ ПОДДЕРЖКОЙ
==================================================
Графический интерфейс для комплексного анализатора веб-сайтов
с поддержкой русского и английского языков

Автор: Senior Python Developer
Версия: 3.1.0
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
from datetime import datetime
from languages import get_text, set_language, get_current_language

class AnalyzerGUI:
    """Класс графического интерфейса анализатора с многоязычной поддержкой"""

    def __init__(self, root, analyzer):
        self.root = root
        self.analyzer = analyzer

        # Переменные
        self.url_var = tk.StringVar()
        self.analysis_type_var = tk.StringVar(value="both")
        self.progress_var = tk.DoubleVar()
        self.language_var = tk.StringVar(value=get_current_language())

        # Результаты анализа
        self.current_results = None
        
        # Виджеты для обновления текста
        self.text_widgets = {}

        self.setup_gui()

    def setup_gui(self):
        """Настройка графического интерфейса"""

        # Настройка главного окна
        self.update_window_title()
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')

        # Создание виджетов
        self.create_header()
        self.create_input_panel()
        self.create_progress_panel()
        self.create_results_panel()

        # Горячие клавиши
        self.root.bind('<Control-Return>', lambda e: self.start_analysis())
        self.root.bind('<F5>', lambda e: self.start_analysis())

    def update_window_title(self):
        """Обновить заголовок окна"""
        title = get_text('app_title') + " v3.1"
        self.root.title(title)

    def create_header(self):
        """Создание заголовка"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        # Заголовок
        title_label = tk.Label(
            header_frame,
            text=get_text('app_title'),
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(pady=(10, 5))
        self.text_widgets['title'] = title_label

        # Подзаголовок
        if get_current_language() == 'ru':
            subtitle_text = "Анализ защиты и структуры • Генерация селекторов • Рекомендации по парсингу"
        else:
            subtitle_text = "Protection & Structure Analysis • Selector Generation • Scraping Recommendations"
            
        subtitle_label = tk.Label(
            header_frame,
            text=subtitle_text,
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        self.text_widgets['subtitle'] = subtitle_label

    def create_input_panel(self):
        """Создание панели ввода"""
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Панель ввода
        input_frame = tk.LabelFrame(
            main_frame,
            text=f"🎯 {get_text('analysis_type_label')}",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        input_frame.pack(fill='x', pady=(0, 10))
        self.text_widgets['input_frame'] = input_frame

        # Создание строки с элементами управления
        control_frame = tk.Frame(input_frame, bg='#f0f0f0')
        control_frame.pack(fill='x', padx=10, pady=10)

        # URL ввод
        self.create_url_input(control_frame)
        
        # Селектор языка
        self.create_language_selector(control_frame)
        
        # Тип анализа
        self.create_analysis_selector(control_frame)
        
        # Кнопки управления
        self.create_control_buttons(control_frame)

        # Сохранение главного фрейма для результатов
        self.main_frame = main_frame

    def create_url_input(self, parent):
        """Создание поля ввода URL"""
        url_frame = tk.Frame(parent, bg='#f0f0f0')
        url_frame.pack(side='left', padx=(0, 10))

        url_label = tk.Label(
            url_frame,
            text=get_text('url_label'),
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        url_label.pack(anchor='w')
        self.text_widgets['url_label'] = url_label

        url_entry = tk.Entry(
            url_frame,
            textvariable=self.url_var,
            font=('Arial', 10),
            width=50,
            relief='solid',
            borderwidth=1
        )
        url_entry.pack(pady=(2, 0))
        url_entry.insert(0, get_text('url_placeholder'))
        self.text_widgets['url_entry'] = url_entry

    def create_language_selector(self, parent):
        """Создание селектора языка"""
        lang_frame = tk.Frame(parent, bg='#f0f0f0')
        lang_frame.pack(side='left', padx=(0, 10))

        lang_label = tk.Label(
            lang_frame,
            text=get_text('language_label'),
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        lang_label.pack(anchor='w')
        self.text_widgets['lang_label'] = lang_label

        lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.language_var,
            values=[get_text('russian'), get_text('english')],
            state='readonly',
            width=15,
            font=('Arial', 10)
        )
        lang_combo.pack(pady=(2, 0))
        lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        self.text_widgets['lang_combo'] = lang_combo

    def create_analysis_selector(self, parent):
        """Создание селектора типа анализа"""
        analysis_frame = tk.Frame(parent, bg='#f0f0f0')
        analysis_frame.pack(side='left', padx=(0, 10))

        analysis_label = tk.Label(
            analysis_frame,
            text=get_text('analysis_type_label'),
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        analysis_label.pack(anchor='w')
        self.text_widgets['analysis_label'] = analysis_label

        analysis_combo = ttk.Combobox(
            analysis_frame,
            textvariable=self.analysis_type_var,
            values=[
                get_text('analysis_protection'),
                get_text('analysis_structure'),
                get_text('analysis_both')
            ],
            state='readonly',
            width=20,
            font=('Arial', 10)
        )
        analysis_combo.pack(pady=(2, 0))
        analysis_combo.set(get_text('analysis_both'))
        self.text_widgets['analysis_combo'] = analysis_combo

    def create_control_buttons(self, parent):
        """Создание кнопок управления"""
        button_frame = tk.Frame(parent, bg='#f0f0f0')
        button_frame.pack(side='right')

        # Кнопка анализа
        analyze_btn = tk.Button(
            button_frame,
            text=get_text('analyze_button'),
            command=self.start_analysis,
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        analyze_btn.pack(side='left', padx=(0, 5))
        self.text_widgets['analyze_btn'] = analyze_btn

        # Кнопка очистки
        clear_btn = tk.Button(
            button_frame,
            text=get_text('clear_button'),
            command=self.clear_results,
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        clear_btn.pack(side='left', padx=(0, 5))
        self.text_widgets['clear_btn'] = clear_btn

        # Кнопка экспорта
        export_btn = tk.Button(
            button_frame,
            text=get_text('export_button'),
            command=self.export_results,
            font=('Arial', 10),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        export_btn.pack(side='left')
        self.text_widgets['export_btn'] = export_btn

    def create_progress_panel(self):
        """Создание панели прогресса"""
        self.progress_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        
        self.status_label = tk.Label(
            self.progress_frame,
            text=get_text('status_ready'),
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.status_label.pack(pady=(5, 0))
        self.text_widgets['status_label'] = self.status_label

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=(5, 10))

    def create_results_panel(self):
        """Создание панели результатов"""
        self.results_frame = tk.LabelFrame(
            self.main_frame,
            text=f"📊 {get_text('tab_full_report')}",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        self.text_widgets['results_frame'] = self.results_frame

        # Создание вкладок
        self.create_tabs()

    def create_tabs(self):
        """Создание системы вкладок"""
        self.notebook = ttk.Notebook(self.results_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Создание вкладок
        self.create_summary_tab()
        self.create_protection_tab()
        self.create_structure_tab()
        self.create_selectors_tab()
        self.create_full_report_tab()

    def create_summary_tab(self):
        """Вкладка сводки"""
        self.summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text=get_text('tab_summary'))
        
        self.summary_text = scrolledtext.ScrolledText(
            self.summary_frame,
            height=20,
            font=('Consolas', 10),
            wrap='word'
        )
        self.summary_text.pack(fill='both', expand=True, padx=5, pady=5)

    def create_protection_tab(self):
        """Вкладка защиты"""
        self.protection_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.protection_frame, text=get_text('tab_protection'))
        
        self.protection_text = scrolledtext.ScrolledText(
            self.protection_frame,
            height=20,
            font=('Consolas', 10),
            wrap='word'
        )
        self.protection_text.pack(fill='both', expand=True, padx=5, pady=5)

    def create_structure_tab(self):
        """Вкладка структуры"""
        self.structure_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.structure_frame, text=get_text('tab_structure'))
        
        self.structure_text = scrolledtext.ScrolledText(
            self.structure_frame,
            height=20,
            font=('Consolas', 10),
            wrap='word'
        )
        self.structure_text.pack(fill='both', expand=True, padx=5, pady=5)

    def create_selectors_tab(self):
        """Вкладка селекторов"""
        self.selectors_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.selectors_frame, text=get_text('tab_selectors'))
        
        self.selectors_text = scrolledtext.ScrolledText(
            self.selectors_frame,
            height=20,
            font=('Consolas', 10),
            wrap='word'
        )
        self.selectors_text.pack(fill='both', expand=True, padx=5, pady=5)

    def create_full_report_tab(self):
        """Вкладка полного отчета"""
        self.full_report_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.full_report_frame, text=get_text('tab_full_report'))
        
        self.full_report_text = scrolledtext.ScrolledText(
            self.full_report_frame,
            height=20,
            font=('Consolas', 10),
            wrap='word'
        )
        self.full_report_text.pack(fill='both', expand=True, padx=5, pady=5)

    def on_language_change(self, event=None):
        """Обработчик смены языка"""
        selected_lang = self.language_var.get()
        
        # Определяем код языка
        if selected_lang == 'Русский' or selected_lang == get_text('russian'):
            new_lang = 'ru'
        else:
            new_lang = 'en'
        
        # Устанавливаем новый язык
        if set_language(new_lang):
            self.update_interface_language()

    def update_interface_language(self):
        """Обновление языка интерфейса"""
        # Обновляем заголовок окна
        self.update_window_title()
        
        # Обновляем все текстовые элементы
        self.update_text_widgets()
        
        # Обновляем вкладки
        self.update_tabs()
        
        # Обновляем комбобоксы
        self.update_comboboxes()

    def update_text_widgets(self):
        """Обновление текстовых виджетов"""
        # Заголовки
        if 'title' in self.text_widgets:
            self.text_widgets['title'].config(text=get_text('app_title'))
        
        # Подзаголовок
        if 'subtitle' in self.text_widgets:
            if get_current_language() == 'ru':
                subtitle_text = "Анализ защиты и структуры • Генерация селекторов • Рекомендации по парсингу"
            else:
                subtitle_text = "Protection & Structure Analysis • Selector Generation • Scraping Recommendations"
            self.text_widgets['subtitle'].config(text=subtitle_text)
        
        # Метки
        if 'url_label' in self.text_widgets:
            self.text_widgets['url_label'].config(text=get_text('url_label'))
        
        if 'lang_label' in self.text_widgets:
            self.text_widgets['lang_label'].config(text=get_text('language_label'))
        
        if 'analysis_label' in self.text_widgets:
            self.text_widgets['analysis_label'].config(text=get_text('analysis_type_label'))
        
        # Кнопки
        if 'analyze_btn' in self.text_widgets:
            self.text_widgets['analyze_btn'].config(text=get_text('analyze_button'))
        
        if 'clear_btn' in self.text_widgets:
            self.text_widgets['clear_btn'].config(text=get_text('clear_button'))
        
        if 'export_btn' in self.text_widgets:
            self.text_widgets['export_btn'].config(text=get_text('export_button'))
        
        # Статус
        if 'status_label' in self.text_widgets:
            self.text_widgets['status_label'].config(text=get_text('status_ready'))
        
        # Фреймы
        if 'input_frame' in self.text_widgets:
            self.text_widgets['input_frame'].config(text=f"🎯 {get_text('analysis_type_label')}")
        
        if 'results_frame' in self.text_widgets:
            self.text_widgets['results_frame'].config(text=f"📊 {get_text('tab_full_report')}")

    def update_tabs(self):
        """Обновление названий вкладок"""
        if hasattr(self, 'notebook'):
            tabs = [
                get_text('tab_summary'),
                get_text('tab_protection'),
                get_text('tab_structure'),
                get_text('tab_selectors'),
                get_text('tab_full_report')
            ]
            
            for i, tab_text in enumerate(tabs):
                try:
                    self.notebook.tab(i, text=tab_text)
                except:
                    pass

    def update_comboboxes(self):
        """Обновление содержимого комбобоксов"""
        # Языковой селектор
        if 'lang_combo' in self.text_widgets:
            self.text_widgets['lang_combo']['values'] = [get_text('russian'), get_text('english')]
            
            # Обновляем выбранное значение
            if get_current_language() == 'ru':
                self.text_widgets['lang_combo'].set(get_text('russian'))
            else:
                self.text_widgets['lang_combo'].set(get_text('english'))
        
        # Селектор типа анализа
        if 'analysis_combo' in self.text_widgets:
            self.text_widgets['analysis_combo']['values'] = [
                get_text('analysis_protection'),
                get_text('analysis_structure'),
                get_text('analysis_both')
            ]
            self.text_widgets['analysis_combo'].set(get_text('analysis_both'))

    def start_analysis(self):
        """Запуск анализа в отдельном потоке"""
        url = self.url_var.get().strip()
        
        if not url or url == get_text('url_placeholder'):
            messagebox.showwarning(
                get_text('invalid_url'),
                get_text('enter_url')
            )
            return

        # Показываем панель прогресса
        self.progress_frame.pack(fill='x', pady=(0, 10))
        
        # Обновляем статус
        self.status_label.config(text=get_text('status_analyzing'))
        self.progress_var.set(0)

        # Определяем тип анализа
        analysis_type = self.get_analysis_type()

        # Запускаем анализ в отдельном потоке
        thread = threading.Thread(
            target=self.run_analysis,
            args=(url, analysis_type),
            daemon=True
        )
        thread.start()

    def get_analysis_type(self):
        """Определение типа анализа"""
        selected = self.analysis_type_var.get()
        
        if selected == get_text('analysis_protection'):
            return 'protection'
        elif selected == get_text('analysis_structure'):
            return 'structure'
        else:
            return 'both'

    def run_analysis(self, url, analysis_type):
        """Выполнение анализа"""
        try:
            # Имитация прогресса
            for i in range(0, 101, 10):
                self.progress_var.set(i)
                self.root.update_idletasks()
                threading.Event().wait(0.1)

            # Выполняем анализ
            results = self.analyzer.analyze_website(url, analysis_type)
            self.current_results = results

            # Обновляем интерфейс в главном потоке
            self.root.after(0, self.display_results, results)

        except Exception as e:
            error_msg = get_text('analysis_error').format(error=str(e))
            self.root.after(0, self.show_error, error_msg)

    def display_results(self, results):
        """Отображение результатов анализа"""
        # Скрываем прогресс
        self.progress_frame.pack_forget()
        
        # Показываем панель результатов
        self.results_frame.pack(fill='both', expand=True)
        
        # Обновляем статус
        self.status_label.config(text=get_text('status_completed'))

        # Заполняем вкладки
        self.fill_summary_tab(results)
        self.fill_protection_tab(results)
        self.fill_structure_tab(results)
        self.fill_selectors_tab(results)
        self.fill_full_report_tab(results)

        # Показываем сообщение об успехе
        messagebox.showinfo(
            get_text('status_completed'),
            get_text('analysis_complete')
        )

    def fill_summary_tab(self, results):
        """Заполнение вкладки сводки"""
        self.summary_text.delete(1.0, tk.END)
        
        summary = f"""
{get_text('tab_summary')}
{'=' * 50}

URL: {results.get('url', 'N/A')}
{get_text('analysis_type_label')}: {results.get('analysis_type', 'N/A')}

{get_text('protection_level')}: {results.get('protection', {}).get('complexity_level', 'N/A')}
{get_text('protection_score')}: {results.get('protection', {}).get('complexity_score', 'N/A')}

{get_text('recommendations')}:
{results.get('recommendations', get_text('unknown_error'))}
"""
        
        self.summary_text.insert(tk.END, summary)

    def fill_protection_tab(self, results):
        """Заполнение вкладки защиты"""
        self.protection_text.delete(1.0, tk.END)
        
        protection_data = results.get('protection', {})
        protection_text = json.dumps(protection_data, indent=2, ensure_ascii=False)
        
        self.protection_text.insert(tk.END, protection_text)

    def fill_structure_tab(self, results):
        """Заполнение вкладки структуры"""
        self.structure_text.delete(1.0, tk.END)
        
        structure_data = results.get('structure', {})
        structure_text = json.dumps(structure_data, indent=2, ensure_ascii=False)
        
        self.structure_text.insert(tk.END, structure_text)

    def fill_selectors_tab(self, results):
        """Заполнение вкладки селекторов"""
        self.selectors_text.delete(1.0, tk.END)
        
        selectors = results.get('structure', {}).get('suggested_selectors', {})
        
        selectors_content = f"""
{get_text('suggested_selectors')}
{'=' * 40}

"""
        
        for selector_type, selector_list in selectors.items():
            selectors_content += f"\n{selector_type.upper()}:\n"
            for selector in selector_list:
                selectors_content += f"  • {selector}\n"
        
        self.selectors_text.insert(tk.END, selectors_content)

    def fill_full_report_tab(self, results):
        """Заполнение вкладки полного отчета"""
        self.full_report_text.delete(1.0, tk.END)
        
        full_report = json.dumps(results, indent=2, ensure_ascii=False)
        self.full_report_text.insert(tk.END, full_report)

    def show_error(self, error_msg):
        """Показ ошибки"""
        self.progress_frame.pack_forget()
        self.status_label.config(text=get_text('status_error'))
        
        messagebox.showerror(
            get_text('status_error'),
            error_msg
        )

    def clear_results(self):
        """Очистка результатов"""
        self.current_results = None
        self.results_frame.pack_forget()
        self.progress_frame.pack_forget()
        self.status_label.config(text=get_text('status_ready'))
        
        # Очищаем URL
        self.url_var.set("")

    def export_results(self):
        """Экспорт результатов"""
        if not self.current_results:
            messagebox.showwarning(
                get_text('export_error'),
                get_text('enter_url')
            )
            return

        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[
                    ("JSON files", "*.json"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.current_results, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo(
                    get_text('export_success'),
                    get_text('export_success').format(filename=filename)
                )
        
        except Exception as e:
            messagebox.showerror(
                get_text('export_error'),
                get_text('export_error').format(error=str(e))
            )

if __name__ == "__main__":
    # Тестирование GUI
    root = tk.Tk()
    
    # Мок анализатора для тестирования
    class MockAnalyzer:
        def analyze_website(self, url, analysis_type):
            return {
                'url': url,
                'analysis_type': analysis_type,
                'protection': {
                    'complexity_level': 'MEDIUM',
                    'complexity_score': 45
                },
                'structure': {
                    'suggested_selectors': {
                        'products': ['.product', '[data-product]'],
                        'prices': ['.price', '.cost']
                    }
                },
                'recommendations': 'Use requests with User-Agent rotation'
            }
    
    analyzer = MockAnalyzer()
    gui = AnalyzerGUI(root, analyzer)
    
    root.mainloop()