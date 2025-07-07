"""
Advanced Email Scraper Class
"""

import requests
import cloudscraper
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque
import time
import random
from urllib.parse import urljoin, urlparse
from tqdm import tqdm
from termcolor import colored
import threading

from utils import (
    get_random_user_agent, get_random_delay, extract_emails,
    normalize_url, should_skip_url, is_same_domain, can_fetch,
    print_colored
)
from config import DEFAULT_TIMEOUT

class EmailScraper:
    def __init__(self, target_url, max_depth=3, max_threads=5, 
                 delay_range=(1, 3), use_cloudflare_bypass=False,
                 respect_robots=True, same_domain_only=True):
        
        self.target_url = target_url
        self.max_depth = max_depth
        self.max_threads = max_threads
        self.delay_range = delay_range
        self.use_cloudflare_bypass = use_cloudflare_bypass
        self.respect_robots = respect_robots
        self.same_domain_only = same_domain_only
        
        # Initialize session
        if use_cloudflare_bypass:
            self.session = cloudscraper.create_scraper()
        else:
            self.session = requests.Session()
        
        # Data storage
        self.emails = set()
        self.email_sources = {}  # email -> [list of source URLs]
        self.visited_urls = set()
        self.failed_urls = set()
        self.urls_queue = deque([(target_url, 0)])  # (url, depth)
        
        # Statistics
        self.stats = {
            'pages_visited': 0,
            'pages_failed': 0,
            'emails_found': 0,
            'start_time': None,
            'end_time': None
        }
        
        # Thread lock for shared data
        self.lock = threading.Lock()
        
        # Progress bar
        self.pbar = None

    def _make_request(self, url):
        """Make HTTP request with error handling"""
        try:
            headers = {
                'User-Agent': get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = self.session.get(
                url, 
                headers=headers, 
                timeout=DEFAULT_TIMEOUT,
                allow_redirects=True
            )
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            with self.lock:
                self.failed_urls.add(url)
                self.stats['pages_failed'] += 1
            return None

    def _extract_links(self, html_content, base_url, current_url):
        """Extract links from HTML content"""
        links = set()
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            for tag in soup.find_all(['a', 'link']):
                href = tag.get('href')
                if href:
                    normalized_url = normalize_url(href, base_url, current_url)
                    if normalized_url and not should_skip_url(normalized_url):
                        if not self.same_domain_only or is_same_domain(normalized_url, self.target_url):
                            links.add(normalized_url)
                            
        except Exception as e:
            print_colored(f"Error extracting links from {current_url}: {str(e)}", 'red')
        
        return links

    def _process_url(self, url, depth):
        """Process a single URL"""
        if url in self.visited_urls or depth > self.max_depth:
            return []
        
        # Check robots.txt if enabled
        if self.respect_robots and not can_fetch(url):
            print_colored(f"Skipping {url} (blocked by robots.txt)", 'yellow')
            return []
        
        # Add delay between requests
        time.sleep(get_random_delay(*self.delay_range))
        
        # Make request
        response = self._make_request(url)
        if not response:
            return []
        
        with self.lock:
            self.visited_urls.add(url)
            self.stats['pages_visited'] += 1
            if self.pbar:
                self.pbar.set_description(f"Processing: {url[:50]}...")
                self.pbar.update(1)
        
        # Extract emails
        page_emails = extract_emails(response.text)
        if page_emails:
            with self.lock:
                for email in page_emails:
                    self.emails.add(email)
                    if email not in self.email_sources:
                        self.email_sources[email] = []
                    self.email_sources[email].append(url)
                    
                self.stats['emails_found'] = len(self.emails)
                print_colored(f"Found {len(page_emails)} emails on {url}", 'green')
        
        # Extract links for next depth level
        new_links = []
        if depth < self.max_depth:
            base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
            links = self._extract_links(response.text, base_url, url)
            
            for link in links:
                if link not in self.visited_urls:
                    new_links.append((link, depth + 1))
        
        return new_links

    def scrape(self):
        """Main scraping method"""
        print_colored(f"Starting email scraping for: {self.target_url}", 'cyan', 'bold')
        print_colored(f"Max depth: {self.max_depth}, Threads: {self.max_threads}", 'blue')
        print_colored(f"Same domain only: {self.same_domain_only}", 'blue')
        print()
        
        self.stats['start_time'] = time.time()
        
        # Initialize progress bar
        self.pbar = tqdm(desc="Initializing...", unit="pages")
        
        try:
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                while self.urls_queue:
                    # Submit batch of URLs to thread pool
                    futures = []
                    batch_size = min(len(self.urls_queue), self.max_threads * 2)
                    
                    for _ in range(batch_size):
                        if not self.urls_queue:
                            break
                        url, depth = self.urls_queue.popleft()
                        future = executor.submit(self._process_url, url, depth)
                        futures.append(future)
                    
                    # Process completed futures
                    for future in as_completed(futures):
                        try:
                            new_links = future.result()
                            for link, link_depth in new_links:
                                if link not in self.visited_urls:
                                    self.urls_queue.append((link, link_depth))
                        except Exception as e:
                            print_colored(f"Error processing URL: {str(e)}", 'red')
                    
                    # Update progress
                    if self.pbar:
                        self.pbar.set_postfix({
                            'Emails': len(self.emails),
                            'Queue': len(self.urls_queue),
                            'Failed': len(self.failed_urls)
                        })
        
        except KeyboardInterrupt:
            print_colored("\nScraping interrupted by user!", 'yellow', 'bold')
        
        finally:
            if self.pbar:
                self.pbar.close()
            self.stats['end_time'] = time.time()
        
        return self.get_results()

    def get_results(self):
        """Get scraping results"""
        duration = self.stats['end_time'] - self.stats['start_time'] if self.stats['end_time'] else 0
        
        return {
            'emails': list(self.emails),
            'email_sources': self.email_sources,
            'statistics': {
                **self.stats,
                'duration': duration,
                'urls_in_queue': len(self.urls_queue),
                'failed_urls': len(self.failed_urls)
            }
        }

    def print_summary(self):
        """Print scraping summary"""
        duration = self.stats['end_time'] - self.stats['start_time'] if self.stats['end_time'] else 0
        
        print("\n" + "="*70)
        print_colored("SCRAPING SUMMARY", 'cyan', 'bold')
        print("="*70)
        print_colored(f"Target URL: {self.target_url}", 'white')
        print_colored(f"Total emails found: {len(self.emails)}", 'green', 'bold')
        print_colored(f"Pages visited: {self.stats['pages_visited']}", 'blue')
        print_colored(f"Pages failed: {self.stats['pages_failed']}", 'red')
        print_colored(f"Duration: {duration:.2f} seconds", 'yellow')
        print_colored(f"Average time per page: {duration/max(self.stats['pages_visited'], 1):.2f} seconds", 'yellow')
        print("="*70)