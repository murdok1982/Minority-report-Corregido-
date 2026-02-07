# 🕵️ Minority Report - Cyber Intelligence Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Advanced cyber intelligence application combining psychological analysis, OSINT tools, and AI to detect and assess radical behaviors and digital threats.

## 🌟 Features

- **🧠 Psychological Analysis**: Custom GPT integration for behavioral pattern detection
- **🔍 OSINT Intelligence**: Integration with Sherlock and Social-Searcher for comprehensive data gathering
- **📊 Threat Assessment**: Automated analysis of radical behaviors and digital footprints
- **📄 Comprehensive Reports**: PDF generation with psychological and digital threat profiles
- **🎯 Facial Expression Analysis**: Emotion detection and behavioral pattern recognition
- **🌐 Multi-Platform Scraping**: Facebook and terrorist watchlist monitoring
- **🤖 AI-Powered**: OpenAI integration for advanced threat intelligence

## 📋 Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Modules](#modules)
- [Configuration](#configuration)
- [Examples](#examples)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Git
- wkhtmltopdf (for PDF generation)

### Step 1: Clone the repository

```bash
git clone https://github.com/murdok1982/Minority-report-Corregido-.git
cd Minority-report-Corregido-
```

### Step 2: Create virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install wkhtmltopdf

**Windows:**
```bash
# Download from: https://wkhtmltopdf.org/downloads.html
```

**Linux:**
```bash
sudo apt-get install wkhtmltopdf
```

**MacOS:**
```bash
brew install wkhtmltopdf
```

## 📦 Requirements

- `requests` - HTTP library for API calls
- `beautifulsoup4` - Web scraping
- `pandas` - Data analysis
- `nltk` - Natural language processing
- `scikit-learn` - Machine learning algorithms
- `matplotlib` - Data visualization
- `reportlab` - PDF report generation
- `openai` - GPT integration
- `wkhtmltopdf` - HTML to PDF conversion
- `sqlalchemy` - Database management
- `aiohttp` - Async HTTP client
- `httpx` - Modern HTTP client
- `sherlock-project` - Username OSINT tool

## 💻 Usage

### Basic Usage

```python
python main.py
```

### Advanced Usage

```python
from AnalistaPsica import PsychologicalAnalyzer
from OsintAgent import OSINTAgent
from Expresiones import FacialAnalyzer

# Initialize analyzers
psych_analyzer = PsychologicalAnalyzer()
osint_agent = OSINTAgent()
facial_analyzer = FacialAnalyzer()

# Perform analysis
username = "target_username"
osint_data = osint_agent.investigate(username)
psych_profile = psych_analyzer.analyze(osint_data)
threat_level = psych_analyzer.assess_threat(psych_profile)

# Generate report
report = generate_comprehensive_report(osint_data, psych_profile, threat_level)
```

## 🧩 Modules

### 1. AnalistaPsica.py
Psychological analysis module using custom GPT models to assess behavioral patterns and potential threats.

### 2. OsintAgent.py
OSINT intelligence gathering using Sherlock and other tools for digital footprint analysis.

### 3. Expresiones.py
Facial expression analysis for emotion detection and behavioral pattern recognition.

### 4. RaspadorFacebook.py
Facebook data scraping module for social media intelligence gathering.

### 5. RaspadorTerroristas.py
Terrorist watchlist monitoring and cross-referencing module.

### 6. main.py
Main orchestration module coordinating all analysis components.

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
FACEBOOK_ACCESS_TOKEN=your_facebook_token_here
DATABASE_URL=sqlite:///minority_report.db
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT analysis | Yes |
| `FACEBOOK_ACCESS_TOKEN` | Facebook API token | Optional |
| `DATABASE_URL` | Database connection string | Optional |

## 📸 Examples

### Example 1: Username Investigation

```python
# Investigate a username across multiple platforms
results = osint_agent.sherlock_search("suspicious_user")
print(f"Found profiles on {len(results)} platforms")
```

### Example 2: Psychological Profile

```python
# Analyze behavioral patterns
profile = psych_analyzer.create_profile(user_data)
print(f"Threat Level: {profile['threat_level']}")
print(f"Risk Indicators: {profile['risk_indicators']}")
```

### Example 3: Generate Report

```python
# Create comprehensive PDF report
report_path = generate_report(
    target="username",
    osint_data=osint_results,
    psychological_profile=psych_profile,
    output="reports/analysis.pdf"
)
print(f"Report saved to: {report_path}")
```

## 🔒 Security Considerations

⚠️ **Important Security Notes:**

1. **Legal Use Only**: This tool is designed for lawful cyber intelligence and security research
2. **Privacy Laws**: Ensure compliance with GDPR, CCPA, and local privacy regulations
3. **API Keys**: Never commit API keys to version control
4. **Ethical Use**: Use responsibly and only with proper authorization
5. **Data Storage**: Encrypt sensitive data at rest and in transit

### Disclaimer

This software is provided for educational and authorized security research purposes only. Users are responsible for ensuring their use complies with all applicable laws and regulations. Unauthorized surveillance, data collection, or profiling may be illegal in your jurisdiction.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation for API changes
- Use meaningful commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 murdok1982

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👤 Author

**murdok1982**

- GitHub: [@murdok1982](https://github.com/murdok1982)
- Repository: [Minority-report-Corregido](https://github.com/murdok1982/Minority-report-Corregido-)

## 🙏 Acknowledgments

- [Sherlock Project](https://github.com/sherlock-project/sherlock) - Username OSINT tool
- OpenAI - GPT API for psychological analysis
- Social-Searcher - Social media intelligence
- The cybersecurity research community

## 📊 Project Status

🚀 **Active Development** - This project is actively maintained and improved.

### Roadmap

- [ ] Add support for more OSINT tools
- [ ] Implement real-time monitoring dashboard
- [ ] Enhance AI behavioral analysis models
- [ ] Add multi-language support
- [ ] Develop REST API interface
- [ ] Create Docker containerization

---

⭐ If you find this project useful, please consider giving it a star!

🐛 Found a bug? [Open an issue](https://github.com/murdok1982/Minority-report-Corregido-/issues)

💡 Have a feature request? [Start a discussion](https://github.com/murdok1982/Minority-report-Corregido-/discussions)