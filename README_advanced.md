# Advanced Email Scraper v2.0

**NaufalNyaa x MbullHexWorld**

An advanced email scraping tool with multi-threading, anti-bot protection, and comprehensive reporting features.

## 🚀 Features

### 1. **Enhanced UI/UX**
- ✅ Command-line arguments support (argparse)
- ✅ Interactive mode for easy usage
- ✅ Colored terminal output (termcolor)
- ✅ Real-time progress bar (tqdm)
- ✅ Beautiful ASCII banner

### 2. **Advanced Crawling**
- ✅ Recursive crawling with depth control
- ✅ Multi-threaded crawling (ThreadPoolExecutor)
- ✅ Domain filtering (same domain only option)
- ✅ Smart file type filtering (skip .pdf, .zip, .png, etc.)
- ✅ URL normalization and validation

### 3. **Anti-Bot Protection**
- ✅ User-Agent rotation (8 different agents)
- ✅ Random delays between requests
- ✅ Cloudflare bypass support (cloudscraper)
- ✅ Robots.txt respect (optional)
- ✅ Request timeout handling
- ✅ Error handling and retry logic

### 4. **Data Storage & Export**
- ✅ Multiple export formats:
  - **TXT**: Simple text format
  - **CSV**: Spreadsheet compatible
  - **JSON**: Structured data format
  - **XLSX**: Excel format with multiple sheets
- ✅ Email source tracking (which URL found each email)
- ✅ Comprehensive statistics
- ✅ Timestamped output files

### 5. **Comprehensive Reporting**
- ✅ Real-time statistics display
- ✅ Final summary report
- ✅ Processing duration tracking
- ✅ Success/failure rates
- ✅ Live progress updates

## 📦 Installation

### Prerequisites
```bash
# For Termux
pkg update && pkg upgrade -y
pkg install git python -y

# For Linux (Debian/Ubuntu)
sudo apt update && sudo apt upgrade -y
sudo apt install git python3 python3-pip -y
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install beautifulsoup4 requests tqdm termcolor cloudscraper selenium pandas openpyxl
```

## 🎯 Usage

### Command Line Mode
```bash
# Basic usage
python mail_advanced.py -u https://example.com

# Advanced usage with custom settings
python mail_advanced.py -u https://example.com -d 5 -t 10 --cloudflare

# Multiple output formats
python mail_advanced.py -u https://example.com -o txt,csv,json,xlsx

# Allow external domains
python mail_advanced.py -u https://example.com --allow-external

# Ignore robots.txt
python mail_advanced.py -u https://example.com --no-robots
```

### Interactive Mode
Simply run without arguments:
```bash
python mail_advanced.py
```

## 🔧 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-u, --url` | Target URL to scrape | Required |
| `-d, --depth` | Maximum crawling depth | 3 |
| `-t, --threads` | Number of threads | 5 |
| `--delay-min` | Minimum delay between requests (seconds) | 1.0 |
| `--delay-max` | Maximum delay between requests (seconds) | 3.0 |
| `--cloudflare` | Use Cloudflare bypass | False |
| `--no-robots` | Ignore robots.txt restrictions | False |
| `--allow-external` | Allow crawling external domains | False |
| `-o, --output` | Output formats (txt,csv,json,xlsx) | txt,csv |
| `--output-dir` | Output directory for results | . |
| `-v, --verbose` | Enable verbose output | False |

## 📊 Output Files

The tool generates timestamped files in the following formats:

### TXT Format
```
Email Scraping Results
Target URL: https://example.com
Scraping Date: 2024-01-15 10:30:45
Total Emails Found: 25
==================================================

EMAILS FOUND:
--------------------
admin@example.com
contact@example.com
info@example.com
...

EMAIL SOURCES:
--------------------
admin@example.com:
  - https://example.com/contact
  - https://example.com/about

STATISTICS:
--------------------
Pages Visited: 45
Pages Failed: 2
Duration: 120.50 seconds
Emails Found: 25
```

### CSV Format
| Email | Source URLs | Source Count |
|-------|-------------|--------------|
| admin@example.com | https://example.com/contact; https://example.com/about | 2 |
| info@example.com | https://example.com/contact | 1 |

### JSON Format
```json
{
  "metadata": {
    "target_url": "https://example.com",
    "scraping_date": "2024-01-15T10:30:45",
    "total_emails": 25
  },
  "emails": ["admin@example.com", "info@example.com"],
  "email_sources": {
    "admin@example.com": ["https://example.com/contact"]
  },
  "statistics": {
    "pages_visited": 45,
    "duration": 120.50
  }
}
```

### XLSX Format
Multi-sheet Excel file with:
- **Emails**: Email list with sources
- **Statistics**: Scraping statistics
- **Metadata**: General information

## 🛡️ Anti-Bot Features

### User-Agent Rotation
The tool rotates between 8 different user agents:
- Chrome (Windows, macOS, Linux)
- Firefox (Windows, macOS, Linux)
- Edge (Windows)
- Safari (macOS)

### Request Delays
- Random delays between 1-3 seconds (configurable)
- Prevents overwhelming target servers
- Reduces detection probability

### Cloudflare Bypass
- Uses `cloudscraper` library
- Automatically handles JavaScript challenges
- Bypasses basic anti-bot protection

### Robots.txt Respect
- Checks robots.txt before crawling
- Respects crawl-delay directives
- Can be disabled with `--no-robots`

## 📈 Performance Tips

1. **Adjust Thread Count**: More threads = faster scraping, but higher resource usage
2. **Set Appropriate Delays**: Balance speed vs. politeness
3. **Use Domain Filtering**: Limit to target domain for focused results
4. **Monitor Progress**: Use progress bar to track performance
5. **Handle Large Sites**: Use reasonable depth limits for large websites

## 🚨 Ethical Usage

This tool should be used responsibly and ethically:

- ✅ Respect robots.txt files
- ✅ Use reasonable delays between requests
- ✅ Don't overwhelm target servers
- ✅ Comply with website terms of service
- ✅ Use for legitimate purposes only
- ❌ Don't use for spam or malicious activities
- ❌ Don't ignore rate limiting

## 🐛 Troubleshooting

### Common Issues

1. **SSL Certificate Errors**
   ```bash
   pip install --upgrade certifi
   ```

2. **Permission Denied**
   ```bash
   chmod +x mail_advanced.py
   ```

3. **Module Not Found**
   ```bash
   pip install -r requirements.txt
   ```

4. **Cloudflare Issues**
   - Try without `--cloudflare` flag
   - Update cloudscraper: `pip install --upgrade cloudscraper`

## 📝 Examples

### Basic University Email Scraping
```bash
python mail_advanced.py -u https://university.edu -d 4 -t 8
```

### Corporate Website with Anti-Bot Protection
```bash
python mail_advanced.py -u https://company.com --cloudflare --delay-min 2 --delay-max 5
```

### Comprehensive Scraping with All Formats
```bash
python mail_advanced.py -u https://example.com -d 5 -t 10 -o txt,csv,json,xlsx --output-dir results/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 👥 Authors

- **NaufalNyaa** - Original concept and development
- **MbullHexWorld** - Advanced features and enhancements

## 🔗 Links

- [GitHub Repository](https://github.com/NaufalNyaa/email-scrapping)
- [Report Issues](https://github.com/NaufalNyaa/email-scrapping/issues)

---

**⚠️ Disclaimer**: This tool is for educational and legitimate purposes only. Users are responsible for complying with applicable laws and website terms of service.