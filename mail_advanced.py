#!/usr/bin/env python3
"""
Advanced Email Scraper v2.0
NaufalNyaa x MbullHexWorld

Enhanced email scraping tool with advanced features:
- Multi-threaded crawling
- Anti-bot protection
- Multiple export formats
- Progress tracking
- Domain filtering
- Robots.txt respect
"""

import argparse
import sys
import os
from urllib.parse import urlparse

from utils import print_banner, print_colored
from scraper import EmailScraper
from exporter import DataExporter
from termcolor import colored
from config import OUTPUT_FORMATS, DEFAULT_DEPTH, DEFAULT_THREADS

def validate_url(url):
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description='Advanced Email Scraper v2.0 - NaufalNyaa x MbullHexWorld',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mail_advanced.py -u https://example.com
  python mail_advanced.py -u https://example.com -d 5 -t 10
  python mail_advanced.py -u https://example.com --cloudflare --no-robots
  python mail_advanced.py -u https://example.com -o txt,csv,json
        """
    )
    
    # Required arguments
    parser.add_argument('-u', '--url', 
                       required=True,
                       help='Target URL to scrape')
    
    # Optional arguments
    parser.add_argument('-d', '--depth',
                       type=int,
                       default=DEFAULT_DEPTH,
                       help=f'Maximum crawling depth (default: {DEFAULT_DEPTH})')
    
    parser.add_argument('-t', '--threads',
                       type=int,
                       default=DEFAULT_THREADS,
                       help=f'Number of threads (default: {DEFAULT_THREADS})')
    
    parser.add_argument('--delay-min',
                       type=float,
                       default=1.0,
                       help='Minimum delay between requests in seconds (default: 1.0)')
    
    parser.add_argument('--delay-max',
                       type=float,
                       default=3.0,
                       help='Maximum delay between requests in seconds (default: 3.0)')
    
    parser.add_argument('--cloudflare',
                       action='store_true',
                       help='Use Cloudflare bypass (cloudscraper)')
    
    parser.add_argument('--no-robots',
                       action='store_true',
                       help='Ignore robots.txt restrictions')
    
    parser.add_argument('--allow-external',
                       action='store_true',
                       help='Allow crawling external domains')
    
    parser.add_argument('-o', '--output',
                       default='txt,csv',
                       help=f'Output formats: {",".join(OUTPUT_FORMATS)} (default: txt,csv)')
    
    parser.add_argument('--output-dir',
                       default='.',
                       help='Output directory for results (default: current directory)')
    
    parser.add_argument('-v', '--verbose',
                       action='store_true',
                       help='Enable verbose output')
    
    return parser

def interactive_mode():
    """Interactive mode for user input"""
    print_colored("Interactive Mode", 'cyan', 'bold')
    print_colored("Enter the required information:", 'white')
    print()
    
    # Get URL
    while True:
        url = input(colored("Target URL: ", 'yellow')).strip()
        if not url:
            print_colored("URL cannot be empty!", 'red')
            continue
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        if validate_url(url):
            break
        else:
            print_colored("Invalid URL format! Please enter a valid URL.", 'red')
    
    # Get depth
    while True:
        try:
            depth_input = input(colored(f"Crawling depth (default: {DEFAULT_DEPTH}): ", 'yellow')).strip()
            depth = int(depth_input) if depth_input else DEFAULT_DEPTH
            if depth < 1:
                print_colored("Depth must be at least 1!", 'red')
                continue
            break
        except ValueError:
            print_colored("Please enter a valid number!", 'red')
    
    # Get threads
    while True:
        try:
            threads_input = input(colored(f"Number of threads (default: {DEFAULT_THREADS}): ", 'yellow')).strip()
            threads = int(threads_input) if threads_input else DEFAULT_THREADS
            if threads < 1:
                print_colored("Threads must be at least 1!", 'red')
                continue
            break
        except ValueError:
            print_colored("Please enter a valid number!", 'red')
    
    # Advanced options
    print_colored("\nAdvanced Options (y/n):", 'cyan')
    cloudflare = input(colored("Use Cloudflare bypass? (y/N): ", 'yellow')).strip().lower() == 'y'
    ignore_robots = input(colored("Ignore robots.txt? (y/N): ", 'yellow')).strip().lower() == 'y'
    allow_external = input(colored("Allow external domains? (y/N): ", 'yellow')).strip().lower() == 'y'
    
    # Output formats
    print_colored(f"\nAvailable output formats: {', '.join(OUTPUT_FORMATS)}", 'blue')
    output_input = input(colored("Output formats (default: txt,csv): ", 'yellow')).strip()
    output_formats = output_input.split(',') if output_input else ['txt', 'csv']
    output_formats = [fmt.strip() for fmt in output_formats if fmt.strip() in OUTPUT_FORMATS]
    
    return {
        'url': url,
        'depth': depth,
        'threads': threads,
        'delay_min': 1.0,
        'delay_max': 3.0,
        'cloudflare': cloudflare,
        'no_robots': ignore_robots,
        'allow_external': allow_external,
        'output': ','.join(output_formats),
        'output_dir': '.',
        'verbose': False
    }

def main():
    """Main function"""
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print banner
    print_banner()
    
    # Parse arguments or use interactive mode
    parser = create_parser()
    
    if len(sys.argv) == 1:
        # No arguments provided, use interactive mode
        args = argparse.Namespace(**interactive_mode())
    else:
        args = parser.parse_args()
    
    # Validate URL
    if not validate_url(args.url):
        print_colored("Error: Invalid URL format!", 'red', 'bold')
        sys.exit(1)
    
    # Validate output formats
    output_formats = [fmt.strip() for fmt in args.output.split(',')]
    invalid_formats = [fmt for fmt in output_formats if fmt not in OUTPUT_FORMATS]
    if invalid_formats:
        print_colored(f"Error: Invalid output formats: {', '.join(invalid_formats)}", 'red', 'bold')
        print_colored(f"Available formats: {', '.join(OUTPUT_FORMATS)}", 'yellow')
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print_colored(f"Created output directory: {args.output_dir}", 'green')
    
    # Initialize scraper
    scraper = EmailScraper(
        target_url=args.url,
        max_depth=args.depth,
        max_threads=args.threads,
        delay_range=(args.delay_min, args.delay_max),
        use_cloudflare_bypass=args.cloudflare,
        respect_robots=not args.no_robots,
        same_domain_only=not args.allow_external
    )
    
    try:
        # Start scraping
        results = scraper.scrape()
        
        # Print summary
        scraper.print_summary()
        
        # Export results
        if results['emails']:
            exporter = DataExporter(results, args.url)
            
            # Change to output directory
            original_dir = os.getcwd()
            os.chdir(args.output_dir)
            
            try:
                exported_files = exporter.export_all(output_formats)
                
                if exported_files:
                    print_colored(f"\nResults saved in: {os.path.abspath(args.output_dir)}", 'cyan', 'bold')
                
            finally:
                os.chdir(original_dir)
        else:
            print_colored("\nNo emails found!", 'yellow', 'bold')
    
    except KeyboardInterrupt:
        print_colored("\n\nScraping interrupted by user!", 'yellow', 'bold')
        sys.exit(0)
    except Exception as e:
        print_colored(f"\nError: {str(e)}", 'red', 'bold')
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()