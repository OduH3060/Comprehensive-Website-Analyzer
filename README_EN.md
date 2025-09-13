# 🔍 Comprehensive Website Analyzer

Professional tool for analyzing anti-scraping protection and website structure with multilingual graphical interface.

## 🎯 Features

### 🔒 Anti-Scraping Protection Analysis
- **Protection mechanism detection**: Cloudflare, CAPTCHA, rate limiting, JavaScript
- **User-Agent analysis**: Testing blocking of various user agents
- **Bypass method testing**: requests, cloudscraper, Selenium, undetected-chrome
- **Complexity assessment**: Automatic protection level determination (LOW/MEDIUM/HIGH/CRITICAL)

### 🏗️ Website Structure Analysis
- **DOM structure**: Element count, tags, classes, IDs
- **Content detection**: Automatic identification of products, articles, forms, navigation
- **Link analysis**: Internal/external links, forms, images
- **JavaScript analysis**: Framework detection, AJAX requests, dynamic content
- **Selector generation**: Optimized CSS/XPath selectors for scraping

### 🎯 Intelligent Recommendations
- **Scraping strategy selection**: Automatic tool recommendations
- **Ready-to-use selectors**: Tested CSS selectors for each content type
- **Complexity assessment**: Time and effort prediction for parser development
- **Bypass methods**: Specific techniques for protection circumvention

### 🌐 Multilingual Support
- **Languages**: Russian and English interface
- **Dynamic switching**: Real-time language switching without restart
- **Localized output**: All analysis results in selected language
- **Cultural adaptation**: Region-appropriate recommendations and terminology

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Automatic installation
python install_dependencies.py

# Or manual installation
pip install -r requirements.txt
```

### 2. Run Analyzer
```bash
python comprehensive_analyzer.py
```

### 3. Usage
1. Enter website URL in the input field
2. Select analysis type (protection/structure/full)
3. Choose interface language (🌐 Language dropdown)
4. Click "🔍 Analyze"
5. Review results in different tabs
6. Export reports in preferred format

## 📋 Requirements

### System Requirements
- **Python**: 3.7 or higher
- **OS**: Windows, macOS, Linux
- **RAM**: Minimum 4 GB (recommended 8 GB)
- **Disk Space**: 500 MB free space

### Core Dependencies
```
requests>=2.25.1         # HTTP requests
beautifulsoup4>=4.9.3    # HTML parsing
fake-useragent>=0.1.11   # User-Agent generation
cloudscraper>=1.2.60     # Cloudflare bypass
```

### Optional Dependencies
```
selenium>=4.0.0                    # Browser automation
undetected-chromedriver>=3.5.0     # Anti-detection Chrome
selenium-wire>=5.1.0               # Traffic interception
pandas>=1.3.0                      # Data processing
```

## 🏗️ Project Structure

```
C:\src\last\
├── comprehensive_analyzer.py    # Main module
├── protection_analyzer.py       # Protection analysis
├── structure_analyzer.py        # Structure analysis
├── gui_components.py           # GUI interface
├── utils.py                    # Utility functions
├── languages.py                # Multilingual support
├── requirements.txt            # Dependencies
├── install_dependencies.py     # Installer
├── README.md                   # Russian documentation
├── README_EN.md               # English documentation
└── logs/                       # Work logs
    └── analyzer_YYYYMMDD.log
```

## 🎮 User Interface

### Main Window
- **URL Field**: Input address for analysis
- **Analysis Type**: Choose between protection, structure, or full analysis
- **Language Selector**: Switch between Russian and English
- **Control Buttons**: Analyze, export, clear

### Result Tabs
1. **📋 Summary**: Brief overview with recommendations
2. **🔒 Protection**: Detailed protection mechanism analysis
3. **🏗️ Structure**: DOM structure and content analysis
4. **🎯 Selectors**: Ready-to-use CSS selectors for scraping
5. **📄 Full Report**: Comprehensive report with all data

## 🔧 Usage Examples

### E-commerce Site Analysis
```python
from comprehensive_analyzer import ComprehensiveWebsiteAnalyzer

analyzer = ComprehensiveWebsiteAnalyzer()
results = analyzer.analyze_website("https://shop.example.com", "both", "en")

# Get recommended selectors for products
product_selectors = results['structure']['suggested_selectors']['products']
print("Product selectors:", product_selectors)
```

### Protection-Only Check
```python
# Analyze only protection mechanisms
protection_results = analyzer.analyze_website("https://example.com", "protection", "en")

complexity = protection_results['protection']['complexity_level']
print(f"Protection level: {complexity}")
```

### Export Results
```python
# Save results to file
analyzer.export_results("analysis_report.json", results, "json")
analyzer.export_results("analysis_report.txt", results, "txt")
```

### Language Switching
```python
from languages import set_language, get_text

# Switch to English
set_language('en')
print(get_text('app_title'))  # "🔍 Comprehensive Website Analyzer"

# Switch to Russian
set_language('ru')
print(get_text('app_title'))  # "🔍 Комплексный анализатор веб-сайтов"
```

## 📊 Supported Website Types

### ✅ Excellent for
- **E-commerce**: Online stores, product catalogs
- **News sites**: Portals, blogs, media
- **Corporate sites**: Companies, services, contacts
- **Social networks**: Profiles, posts (public)
- **Forums and communities**: Discussions, topics

### ⚠️ Limitations
- **SPA applications**: Complex Single Page Applications require Selenium
- **Authenticated sites**: Only public content analysis
- **API endpoints**: Direct API analysis not supported
- **CAPTCHA sites**: Manual CAPTCHA solving required

## 🛡️ Protection Mechanisms

### Detectable Protections
| Mechanism | Description | Complexity Level |
|-----------|-------------|------------------|
| **Cloudflare** | DDoS protection, bot filtering | HIGH |
| **JavaScript Required** | Content loaded via JS | MEDIUM-HIGH |
| **Rate Limiting** | Request frequency limits | MEDIUM |
| **User-Agent Filtering** | Header-based blocking | LOW-MEDIUM |
| **CAPTCHA** | reCAPTCHA, hCaptcha, etc. | HIGH-CRITICAL |
| **Cookie Requirements** | Mandatory cookies | LOW |

### Bypass Methods
1. **requests** - Simple HTTP requests
2. **cloudscraper** - Cloudflare bypass
3. **Selenium** - Full browser emulation
4. **undetected-chrome** - Anti-detection browser
5. **fake-useragent** - User-Agent rotation

## 🎯 Generated Selectors

### Selector Types
- **Products**: `[class*="product"]`, `[data-product]`, `.item-card`
- **Prices**: `[class*="price"]`, `.cost`, `[data-price]`
- **Titles**: `h1`, `h2`, `[class*="title"]`
- **Descriptions**: `[class*="description"]`, `.content`, `p`
- **Links**: `a[href]`, `[class*="link"]`
- **Images**: `img[src]`, `[class*="image"]`

### Selector Usage Example
```python
from bs4 import BeautifulSoup
import requests

# Use recommended selectors
url = "https://example-shop.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Products
products = soup.select('[class*="product"]')
for product in products:
    title = product.select_one('[class*="title"]')
    price = product.select_one('[class*="price"]')
    
    print(f"Product: {title.text if title else 'N/A'}")
    print(f"Price: {price.text if price else 'N/A'}")
```

## 📈 Result Interpretation

### Protection Complexity Levels
- **LOW (0-39 points)**: Simple requests sufficient
- **MEDIUM (40-59 points)**: Requires requests + additional headers
- **HIGH (60-79 points)**: Selenium or cloudscraper recommended
- **CRITICAL (80-100 points)**: Advanced bypass methods mandatory

### Tool Selection Recommendations
```
Protection Score 0-39:   requests + BeautifulSoup
Protection Score 40-59:  requests + cloudscraper + fake-useragent
Protection Score 60-79:  Selenium + undetected-chromedriver
Protection Score 80-100: Selenium + proxies + captcha services
```

## 🌐 Language Support

### Available Languages
- **Russian (русский)**: Complete interface and documentation
- **English**: Full interface and documentation
- **Dynamic Switching**: Change language without restart

### Language-Specific Features
- **Localized UI**: All interface elements translated
- **Cultural Adaptation**: Region-appropriate recommendations
- **Export Formats**: Reports in selected language
- **Error Messages**: Localized error handling

### Adding New Languages
```python
# In languages.py, add new translation dictionary
NEW_LANGUAGE_TRANSLATIONS = {
    'app_title': 'Your Translation',
    'analyze_button': 'Your Translation',
    # ... other translations
}

# Update TRANSLATIONS dictionary
TRANSLATIONS = {
    'ru': RUSSIAN_TRANSLATIONS,
    'en': ENGLISH_TRANSLATIONS,
    'xx': NEW_LANGUAGE_TRANSLATIONS  # Your language code
}
```

## 🔍 Troubleshooting

### Common Errors

#### "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### "Chrome driver not found"
```bash
# Install Chrome
# Windows: download from https://www.google.com/chrome/
# Linux: sudo apt install google-chrome-stable
# macOS: brew install --cask google-chrome
```

#### "Timeout errors"
```python
# Increase timeouts in code
session.get(url, timeout=30)  # instead of 15
```

#### "Access denied / 403 Forbidden"
```python
# Check headers and use random User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
```

#### "Language not switching"
```python
# Force language update
from languages import set_language
set_language('en')  # or 'ru'

# Restart GUI if needed
gui.update_interface_language()
```

### Logging
All operations are logged to files:
```
logs/analyzer_YYYYMMDD.log
```

For debug mode:
```python
import logging
logging.getLogger('WebsiteAnalyzer').setLevel(logging.DEBUG)
```

## 🤝 Support and Development

### Bug Reports
When reporting bugs, please provide:
1. Problematic website URL
2. Error log from `logs/` directory
3. Python version and OS
4. Steps to reproduce
5. Selected language

### Development Roadmap
- [ ] Playwright support
- [ ] Mobile website analysis
- [ ] Proxy service integration
- [ ] API for automation
- [ ] Popular CMS plugins
- [ ] Scrapy project export
- [ ] Additional languages (Spanish, French, German)
- [ ] Cloud-based analysis
- [ ] Machine learning protection detection

## 📄 License

This project is created for educational and research purposes.

**Important**: Comply with robots.txt, website terms of service, and applicable laws when scraping data.

## 🔗 Useful Resources

### Library Documentation
- [Requests](https://docs.python-requests.org/): HTTP requests
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): HTML parsing
- [Selenium](https://selenium-python.readthedocs.io/): Browser automation
- [CloudScraper](https://github.com/VeNoMouS/cloudscraper): Cloudflare bypass

### Web Scraping Tools
- [Scrapy](https://scrapy.org/): Scraping framework
- [Playwright](https://playwright.dev/python/): Modern browser automation
- [httpx](https://www.python-httpx.org/): Async HTTP requests

### Multilingual Development
- [Python Internationalization](https://docs.python.org/3/library/i18n.html): Built-in i18n support
- [Babel](http://babel.pocoo.org/): Python localization toolkit
- [GNU gettext](https://www.gnu.org/software/gettext/): Translation utilities

---

**Author**: OduH  
**Version**: 3.1.0  
**Date**: 2025-09-14  

🎯 **Project Goal**: Simplify website analysis and create effective scrapers through automated analysis and intelligent recommendations with full multilingual support.