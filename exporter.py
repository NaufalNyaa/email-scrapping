"""
Data Export Module
"""

import json
import csv
import pandas as pd
from datetime import datetime
import os
from termcolor import colored
from utils import print_colored

class DataExporter:
    def __init__(self, results, target_url):
        self.results = results
        self.target_url = target_url
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.base_filename = f"email_scraping_{self.timestamp}"
        
    def export_txt(self, filename=None):
        """Export results to text file"""
        if not filename:
            filename = f"{self.base_filename}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Email Scraping Results\n")
                f.write(f"Target URL: {self.target_url}\n")
                f.write(f"Scraping Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Emails Found: {len(self.results['emails'])}\n")
                f.write("="*50 + "\n\n")
                
                f.write("EMAILS FOUND:\n")
                f.write("-"*20 + "\n")
                for email in sorted(self.results['emails']):
                    f.write(f"{email}\n")
                
                f.write("\n\nEMAIL SOURCES:\n")
                f.write("-"*20 + "\n")
                for email, sources in self.results['email_sources'].items():
                    f.write(f"\n{email}:\n")
                    for source in sources:
                        f.write(f"  - {source}\n")
                
                f.write("\n\nSTATISTICS:\n")
                f.write("-"*20 + "\n")
                stats = self.results['statistics']
                f.write(f"Pages Visited: {stats['pages_visited']}\n")
                f.write(f"Pages Failed: {stats['pages_failed']}\n")
                f.write(f"Duration: {stats['duration']:.2f} seconds\n")
                f.write(f"Emails Found: {stats['emails_found']}\n")
            
            print_colored(f"✓ Results exported to {filename}", 'green')
            return filename
            
        except Exception as e:
            print_colored(f"✗ Error exporting to TXT: {str(e)}", 'red')
            return None

    def export_csv(self, filename=None):
        """Export results to CSV file"""
        if not filename:
            filename = f"{self.base_filename}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Email', 'Source URLs', 'Source Count'])
                
                for email in sorted(self.results['emails']):
                    sources = self.results['email_sources'].get(email, [])
                    sources_str = '; '.join(sources)
                    writer.writerow([email, sources_str, len(sources)])
            
            print_colored(f"✓ Results exported to {filename}", 'green')
            return filename
            
        except Exception as e:
            print_colored(f"✗ Error exporting to CSV: {str(e)}", 'red')
            return None

    def export_json(self, filename=None):
        """Export results to JSON file"""
        if not filename:
            filename = f"{self.base_filename}.json"
        
        try:
            export_data = {
                'metadata': {
                    'target_url': self.target_url,
                    'scraping_date': datetime.now().isoformat(),
                    'total_emails': len(self.results['emails'])
                },
                'emails': self.results['emails'],
                'email_sources': self.results['email_sources'],
                'statistics': self.results['statistics']
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print_colored(f"✓ Results exported to {filename}", 'green')
            return filename
            
        except Exception as e:
            print_colored(f"✗ Error exporting to JSON: {str(e)}", 'red')
            return None

    def export_xlsx(self, filename=None):
        """Export results to Excel file"""
        if not filename:
            filename = f"{self.base_filename}.xlsx"
        
        try:
            # Prepare data for Excel
            email_data = []
            for email in sorted(self.results['emails']):
                sources = self.results['email_sources'].get(email, [])
                email_data.append({
                    'Email': email,
                    'Source Count': len(sources),
                    'First Source': sources[0] if sources else '',
                    'All Sources': '; '.join(sources)
                })
            
            # Create Excel file with multiple sheets
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Emails sheet
                df_emails = pd.DataFrame(email_data)
                df_emails.to_excel(writer, sheet_name='Emails', index=False)
                
                # Statistics sheet
                stats_data = []
                for key, value in self.results['statistics'].items():
                    stats_data.append({'Metric': key, 'Value': value})
                
                df_stats = pd.DataFrame(stats_data)
                df_stats.to_excel(writer, sheet_name='Statistics', index=False)
                
                # Metadata sheet
                metadata = [
                    {'Field': 'Target URL', 'Value': self.target_url},
                    {'Field': 'Scraping Date', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
                    {'Field': 'Total Emails', 'Value': len(self.results['emails'])}
                ]
                df_metadata = pd.DataFrame(metadata)
                df_metadata.to_excel(writer, sheet_name='Metadata', index=False)
            
            print_colored(f"✓ Results exported to {filename}", 'green')
            return filename
            
        except Exception as e:
            print_colored(f"✗ Error exporting to Excel: {str(e)}", 'red')
            return None

    def export_all(self, formats=['txt', 'csv', 'json', 'xlsx']):
        """Export results in all specified formats"""
        exported_files = []
        
        print_colored("\nExporting results...", 'cyan', 'bold')
        
        if 'txt' in formats:
            file = self.export_txt()
            if file:
                exported_files.append(file)
        
        if 'csv' in formats:
            file = self.export_csv()
            if file:
                exported_files.append(file)
        
        if 'json' in formats:
            file = self.export_json()
            if file:
                exported_files.append(file)
        
        if 'xlsx' in formats:
            file = self.export_xlsx()
            if file:
                exported_files.append(file)
        
        if exported_files:
            print_colored(f"\n✓ Successfully exported {len(exported_files)} files:", 'green', 'bold')
            for file in exported_files:
                print_colored(f"  - {file}", 'white')
        else:
            print_colored("✗ No files were exported successfully", 'red', 'bold')
        
        return exported_files