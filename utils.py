"""
Utility functions for Email Scraper
"""

import re
import random
import time
import urllib.parse
from urllib.robotparser import RobotFileParser
from termcolor import colored
from config import USER_AGENTS, SKIP_EXTENSIONS

def get_random_user_agent():
    """Get a random user agent from the list"""
    return random.choice(USER_AGENTS)

def get_random_delay(min_delay=1, max_delay=3):
    """Get a random delay between requests"""
    return random.uniform(min_delay, max_delay)

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def extract_emails(text):
    """Extract emails from text using improved regex"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text, re.IGNORECASE)
    return [email.lower() for email in emails if is_valid_email(email)]

def normalize_url(url, base_url, current_path):
    """Normalize and resolve relative URLs"""
    if not url:
        return None
    
    # Remove fragments and clean URL
    url = url.split('#')[0].strip()
    
    if url.startswith('mailto:'):
        return None
    
    if url.startswith('javascript:'):
        return None
    
    if url.startswith('//'):
        parsed_base = urllib.parse.urlparse(base_url)
        url = f"{parsed_base.scheme}:{url}"
    elif url.startswith('/'):
        url = base_url + url
    elif not url.startswith(('http://', 'https://')):
        url = urllib.parse.urljoin(current_path, url)
    
    return url

def should_skip_url(url):
    """Check if URL should be skipped based on extension"""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lower()
    
    for ext in SKIP_EXTENSIONS:
        if path.endswith(ext):
            return True
    
    return False

def is_same_domain(url1, url2):
    """Check if two URLs belong to the same domain"""
    domain1 = urllib.parse.urlparse(url1).netloc.lower()
    domain2 = urllib.parse.urlparse(url2).netloc.lower()
    return domain1 == domain2

def can_fetch(url, user_agent='*'):
    """Check if URL can be fetched according to robots.txt"""
    try:
        parsed = urllib.parse.urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        return rp.can_fetch(user_agent, url)
    except:
        return True  # If robots.txt can't be read, assume it's allowed

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                                                                      ║
    ║  ███████╗███╗   ███╗ █████╗ ██╗██╗         ███████╗ ██████╗██████╗   ║
    ║  ██╔════╝████╗ ████║██╔══██╗██║██║         ██╔════╝██╔════╝██╔══██╗  ║
    ║  █████╗  ██╔████╔██║███████║██║██║         ███████╗██║     ██████╔╝  ║
    ║  ██╔══╝  ██║╚██╔╝██║██╔══██║██║██║         ╚════██║██║     ██╔══██╗  ║
    ║  ███████╗██║ ╚═╝ ██║██║  ██║██║███████╗    ███████║╚██████╗██║  ██║  ║
    ║  ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝  ║
    ║                                                                      ║
    ║                    Advanced Email Scraper v2.0                      ║
    ║                  NaufalNyaa x MbullHexWorld                         ║
    ║                                                                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """
    print(colored(banner, 'cyan'))

def print_colored(text, color='white', style=None):
    """Print colored text"""
    attrs = []
    if style:
        attrs.append(style)
    print(colored(text, color, attrs=attrs))