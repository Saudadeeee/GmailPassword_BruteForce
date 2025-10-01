#!/usr/bin/env python3
"""
Proxy Management Utility
Helps test and manage proxy servers for the brute force tool
"""

import requests
import socket
import socks
import time
import threading
from queue import Queue
from colorama import init, Fore, Style

init(autoreset=True)

class ProxyTester:
    def __init__(self):
        self.working_proxies = []
        self.failed_proxies = []
        self.test_url = "http://httpbin.org/ip"
        self.timeout = 10
        
    def test_proxy(self, proxy_string):
        """Test a single proxy"""
        try:
            parts = proxy_string.split(':')
            proxy_ip = parts[0]
            proxy_port = int(parts[1])
            
            # Test HTTP proxy
            proxies = {
                'http': f'http://{proxy_ip}:{proxy_port}',
                'https': f'http://{proxy_ip}:{proxy_port}'
            }
            
            response = requests.get(
                self.test_url,
                proxies=proxies,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}✓ Working: {proxy_string}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}✗ Failed: {proxy_string} (Status: {response.status_code}){Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}✗ Failed: {proxy_string} ({str(e)}){Style.RESET_ALL}")
            return False
            
    def test_socks_proxy(self, proxy_string):
        """Test SOCKS proxy"""
        try:
            parts = proxy_string.split(':')
            proxy_ip = parts[0]
            proxy_port = int(parts[1])
            
            # Test SOCKS5 connection
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, proxy_ip, proxy_port)
            s.settimeout(self.timeout)
            s.connect(("google.com", 80))
            s.close()
            
            print(f"{Fore.GREEN}✓ Working SOCKS: {proxy_string}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}✗ Failed SOCKS: {proxy_string} ({str(e)}){Style.RESET_ALL}")
            return False
            
    def test_all_proxies(self, proxy_file="proxies.txt"):
        """Test all proxies from file"""
        try:
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                
            print(f"Testing {len(proxies)} proxies...\n")
            
            working = []
            for proxy in proxies:
                if self.test_proxy(proxy):
                    working.append(proxy)
                time.sleep(0.5)  # Small delay between tests
                
            print(f"\n{Fore.CYAN}Results:{Style.RESET_ALL}")
            print(f"Working proxies: {len(working)}")
            print(f"Failed proxies: {len(proxies) - len(working)}")
            
            # Save working proxies
            if working:
                with open('working_proxies.txt', 'w') as f:
                    for proxy in working:
                        f.write(f"{proxy}\n")
                print(f"Working proxies saved to working_proxies.txt")
                
        except FileNotFoundError:
            print(f"Proxy file {proxy_file} not found!")

def fetch_free_proxies():
    """Fetch free proxies from online sources"""
    print("Fetching free proxies from online sources...")
    
    # This is a basic example - you can add more proxy sources
    proxy_sources = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    ]
    
    all_proxies = set()
    
    for source in proxy_sources:
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                proxies = response.text.strip().split('\n')
                all_proxies.update(proxies)
                print(f"Fetched {len(proxies)} proxies from {source}")
        except Exception as e:
            print(f"Failed to fetch from {source}: {e}")
            
    # Save to file
    if all_proxies:
        with open('fetched_proxies.txt', 'w') as f:
            for proxy in sorted(all_proxies):
                if proxy.strip():
                    f.write(f"{proxy.strip()}\n")
        print(f"Total {len(all_proxies)} unique proxies saved to fetched_proxies.txt")
    else:
        print("No proxies fetched!")

def main():
    print(f"{Fore.CYAN}=== Proxy Management Utility ==={Style.RESET_ALL}")
    print()
    
    while True:
        print("Options:")
        print("1. Test existing proxy list")
        print("2. Fetch free proxies")
        print("3. Test specific proxy")
        print("4. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            tester = ProxyTester()
            proxy_file = input("Proxy file (default: proxies.txt): ").strip() or "proxies.txt"
            tester.test_all_proxies(proxy_file)
            
        elif choice == '2':
            fetch_free_proxies()
            
        elif choice == '3':
            tester = ProxyTester()
            proxy = input("Enter proxy (ip:port): ").strip()
            if proxy:
                print(f"Testing {proxy}...")
                if tester.test_proxy(proxy):
                    print("Proxy is working!")
                else:
                    print("Proxy failed!")
                    
        elif choice == '4':
            break
            
        else:
            print("Invalid option!")
            
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()