# Advanced Gmail Password Brute Force Tool v2.0

## Overview

This is an advanced Gmail password brute-force tool implemented in Python with modern evasion techniques. It includes sophisticated features like proxy rotation, multi-threading, smart rate limiting, and advanced retry mechanisms to bypass common detection systems.

> **⚠️ DISCLAIMER:** This tool is intended for educational and authorized security testing purposes ONLY. Unauthorized access to accounts is illegal and unethical. Use responsibly and only on accounts you own or have explicit written permission to test.

##  New Features (v2.0)

### Advanced Evasion Techniques
- **Proxy Rotation**: Automatically rotates through SOCKS5/HTTP proxies to change IP addresses
- **Smart Rate Limiting**: Dynamic delays with jitter to avoid detection patterns
- **User-Agent Rotation**: Randomizes user agents to appear as different clients
- **Connection Pooling**: Maintains multiple connections for better performance

### Performance & Reliability
- **Multi-threading**: Concurrent password attempts with configurable thread pools
- **Advanced Retry Logic**: Exponential backoff and intelligent error handling
- **Session Management**: Maintains persistent connections where possible
- **Statistics Monitoring**: Real-time attack progress and performance metrics

### Utility Tools
- **Proxy Manager**: Test and validate proxy servers before use
- **Wordlist Generator**: Create targeted password lists based on OSINT
- **Configuration Management**: Easy-to-use config files for all settings

##  Requirements

- Python 3.7+
- Required Python packages (see requirements.txt)
- Proxy servers (optional but recommended)
- Password wordlists (rockyou.txt or custom)
- Target Gmail account (for authorized testing only)

##  Installation

1. Clone the repository:
```bash
git clone https://github.com/Saudadeeee/GmailPassword_BruteForce.git
cd GmailPassword_BruteForce
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure settings:
```bash
# Edit config.ini to customize behavior
notepad config.ini

# Setup proxy list (optional)
notepad proxies.txt
```

##  Usage

### Basic Usage
```bash
# Run the advanced brute forcer
python BruteForce3.py
```

### Utility Tools
```bash
# Test and manage proxies
python proxy_manager.py

# Generate custom wordlists
python wordlist_generator.py
```

##  Configuration

Edit `config.ini` to customize:

```ini
[DEFAULT]
# Rate limiting
min_delay = 2
max_delay = 8
retry_attempts = 3

# Threading
max_threads = 5
thread_delay = 1

# Proxy settings
use_proxy = true
proxy_rotation = true

# SMTP settings
smtp_server = smtp.gmail.com
smtp_port = 587
```

##  Advanced Features

### Proxy Management
- Supports HTTP and SOCKS5 proxies
- Automatic proxy testing and validation
- Proxy rotation for IP diversity
- Built-in proxy fetcher for free proxy lists

### Smart Wordlist Generation
- Target-specific password generation based on OSINT
- Rule-based password transformation
- Common pattern recognition
- Hybrid wordlist creation

### Monitoring & Logging
- Real-time statistics display
- Detailed logging to files
- Color-coded console output
- Attack progress tracking

##  Performance Tips

1. **Use Quality Proxies**: Premium proxies work better than free ones
2. **Optimize Thread Count**: Start with 3-5 threads, adjust based on response
3. **Smart Wordlists**: Use targeted lists instead of massive generic ones
4. **Monitor Rate Limits**: Adjust delays if getting blocked frequently

##  Detection Evasion

- **Variable Timing**: Random delays prevent pattern detection
- **IP Rotation**: Proxy switching distributes requests across IPs
- **Session Management**: Maintains realistic connection patterns
- **Error Handling**: Graceful handling of blocks and timeouts

##  File Structure

```
GmailPassword_BruteForce/
├── BruteForce2.py          # Original version
├── BruteForce3.py          # Advanced version with modern features
├── proxy_manager.py        # Proxy testing and management
├── wordlist_generator.py   # Custom wordlist creation
├── config.ini              # Configuration settings
├── proxies.txt            # Proxy server list
├── requirements.txt       # Python dependencies
├── rockyou.txt           # Password wordlist
└── README.md             # This file
```

##  Security Notes

- Gmail has sophisticated bot detection
- Use strong, unique passwords for your accounts
- Enable 2FA whenever possible
- Monitor your account for suspicious activity
- This tool demonstrates why strong passwords matter



