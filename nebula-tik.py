#!/usr/bin/env python3

import os
import sys
import time
import argparse
import re
import json
import random
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style, init

init()

class Colors:
    HEADER = Fore.CYAN
    TITLE = Fore.MAGENTA + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW
    ERROR = Fore.RED + Style.BRIGHT
    RESET = Style.RESET_ALL
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    PURPLE = Fore.MAGENTA
    BLACK = Fore.BLACK
    BG_CYAN = Back.CYAN
    BOLD = Style.BRIGHT

def clear_screen():
    os.system('clear')

def print_banner():
    banner = f"""
{Colors.TITLE}
╔╗╔╔═╗╔╗ ╦ ╦╦  ╔═╗  ╔╦╗╦ ╦╔═
║║║║╣ ╠╩╗║ ║║  ╠═╣   ║ ║ ╠╩╗
╝╚╝╚═╝╚═╝╚═╝╩═╝╩ ╩   ╩ ╩ ╩ ╩ v0.1
{Colors.RESET}{Colors.HEADER}
      ★ QUANTUM TIK DOWNLOADER ★
      Created By: Rip70022
      GitHub: https://www.github.com/Rip70022
{Colors.RESET}
"""
    print(banner)

def cyber_loading(text, duration=5):
    frames = [
        "⟨▰▱▱▱▱▱▱▱▱▱⟩", "⟨▰▰▱▱▱▱▱▱▱▱⟩", "⟨▰▰▰▱▱▱▱▱▱▱⟩", "⟨▰▰▰▰▱▱▱▱▱▱⟩", 
        "⟨▰▰▰▰▰▱▱▱▱▱⟩", "⟨▰▰▰▰▰▰▱▱▱▱⟩", "⟨▰▰▰▰▰▰▰▱▱▱⟩", "⟨▰▰▰▰▰▰▰▰▱▱⟩",
        "⟨▰▰▰▰▰▰▰▰▰▱⟩", "⟨▰▰▰▰▰▰▰▰▰▰⟩"
    ]
    
    colors = [Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    
    start_time = time.time()
    while time.time() - start_time < duration:
        for frame in frames:
            color = random.choice(colors)
            sys.stdout.write(f"\r{color}{text} {frame}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
            
    sys.stdout.write(f"\r{Fore.GREEN}{text} ⟨▰▰▰▰▰▰▰▰▰▰⟩ [COMPLETE]{Colors.RESET}\n")
    sys.stdout.flush()

def print_status(message, status_type="info"):
    prefix = {
        "info": f"{Colors.BLUE}[INFO]{Colors.RESET}",
        "success": f"{Colors.SUCCESS}[SUCCESS]{Colors.RESET}",
        "warning": f"{Colors.WARNING}[WARNING]{Colors.RESET}",
        "error": f"{Colors.ERROR}[ERROR]{Colors.RESET}"
    }
    
    print(f"\n{prefix.get(status_type, prefix['info'])} {message}")

def is_valid_tiktok_url(url):
    parsed_url = urlparse(url)
    return 'tiktok.com' in parsed_url.netloc and '/video/' in parsed_url.path

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(user_agents)

def download_tiktok_video(url, custom_filename=None, download_path="./"):
    try:
        if not is_valid_tiktok_url(url):
            raise ValueError(f"{Colors.ERROR}Invalid TikTok URL. Please provide a valid TikTok video URL.{Colors.RESET}")
        
        print_status("Initializing download process", "info")
        cyber_loading("Analyzing TikTok URL", 3)
        
        ssstik_url = f"https://ssstik.io/download?url={url}"
        
        headers = {
            "User-Agent": get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://ssstik.io/",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }
        
        print_status("Connecting to download service", "info")
        cyber_loading("Establishing secure connection", 2)
        
        try:
            response = requests.get(ssstik_url, headers=headers, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"{Colors.ERROR}Connection error: {str(e)}{Colors.RESET}")
        
        print_status("Extracting video metadata", "info")
        cyber_loading("Parsing response data", 2)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            video_details = soup.select_one(".result_overlay")
            username = video_details.select_one(".username").text.strip() if video_details and video_details.select_one(".username") else "Unknown"
            description = video_details.select_one(".desc").text.strip() if video_details and video_details.select_one(".desc") else "No description"
            
            print(f"\n{Colors.HEADER}Username: {Colors.RESET}{username}")
            print(f"{Colors.HEADER}Description: {Colors.RESET}{description[:50]}{'...' if len(description) > 50 else ''}")
        except Exception:
            print_status("Could not extract full video details", "warning")
        
        download_link = None
        try:
            download_buttons = soup.select(".download-link")
            for button in download_buttons:
                if "without watermark" in button.text.lower():
                    download_link = button.get("href")
                    break
            
            if not download_link:
                download_link = soup.select_one(".download-link").get("href")
        except Exception:
            raise ValueError(f"{Colors.ERROR}Could not find download link. The service might have changed or the video is not available.{Colors.RESET}")
        
        if not download_link:
            raise ValueError(f"{Colors.ERROR}No download link found. The service might be temporarily unavailable.{Colors.RESET}")
        
        if not custom_filename:
            custom_filename = input(f"\n{Colors.BLUE}Enter a name for the file (leave blank to use auto-generated name): {Colors.RESET}")
        
        if not custom_filename.strip():
            video_id = url.split("/video/")[1].split("?")[0] if "/video/" in url else "tiktok_video"
            custom_filename = f"tiktok_{video_id}"
        
        custom_filename = sanitize_filename(custom_filename)
        
        if not custom_filename.lower().endswith('.mp4'):
            custom_filename += '.mp4'
        
        file_path = os.path.join(download_path, custom_filename)
        
        print_status(f"Downloading video as: {custom_filename}", "info")
        cyber_loading("Transferring data packets", 4)
        
        try:
            video_response = requests.get(download_link, headers=headers, stream=True, timeout=30)
            video_response.raise_for_status()
            
            total_size = int(video_response.headers.get('content-length', 0))
            
            os.makedirs(download_path, exist_ok=True)
            
            with open(file_path, 'wb') as f:
                if total_size == 0:
                    f.write(video_response.content)
                else:
                    downloaded = 0
                    total_size_mb = total_size / (1024 * 1024)
                    for chunk in video_response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            percent = int(100 * downloaded / total_size)
                            
                            bar_length = 30
                            filled_length = int(bar_length * percent // 100)
                            bar = '█' * filled_length + '░' * (bar_length - filled_length)
                            
                            sys.stdout.write(f'\r{Colors.CYAN}Progress: |{bar}| {percent}% ({downloaded/(1024*1024):.1f}/{total_size_mb:.1f}MB){Colors.RESET}')
                            sys.stdout.flush()
            
            print("\n")
            print_status("Download completed successfully! ✓", "success")
            print(f"{Colors.HEADER}File location: {Colors.RESET}{file_path}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"{Colors.ERROR}Failed to download video: {str(e)}{Colors.RESET}")
        
    except ValueError as e:
        print_status(str(e), "error")
    except ConnectionError as e:
        print_status(str(e), "error")
    except Exception as e:
        print_status(f"An unexpected error occurred: {str(e)}", "error")
    
    return False

def main():
    parser = argparse.ArgumentParser(description='Download TikTok videos via ssstik.io from Termux')
    parser.add_argument('-u', '--url', help='TikTok video URL')
    parser.add_argument('-n', '--name', help='Custom filename for the video')
    parser.add_argument('-p', '--path', help='Destination path to save the file', default='./')
    
    args = parser.parse_args()
    
    clear_screen()
    print_banner()
    
    print(f"{Colors.CYAN}╔════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.CYAN}║ {Colors.TITLE}NEBULA TIK{Colors.RESET}{Colors.CYAN} - QUANTUM VIDEO EXTRACTION ║{Colors.RESET}")
    print(f"{Colors.CYAN}╚════════════════════════════════════════╝{Colors.RESET}")
    print(f"\n{Colors.HEADER}Ready to download TikTok videos without watermark{Colors.RESET}")
    
    while True:
        try:
            if not args.url:
                url = input(f"\n{Colors.BLUE}Enter TikTok video URL (or 'exit' to quit): {Colors.RESET}")
                if url.lower() in ['exit', 'quit', 'q']:
                    print(f"\n{Colors.SUCCESS}FOLLOW ME ON GITHUB FOR MORE TOOLS: https://www.github.com/Rip70022 {Colors.RESET}")
                    sys.exit(0)
            else:
                url = args.url
            
            result = download_tiktok_video(url, args.name, args.path)
            
            if args.url:
                break
            
            choice = input(f"\n{Colors.BLUE}Do you want to download another video? (y/n): {Colors.RESET}")
            if choice.lower() not in ['y', 'yes']:
                print(f"\n{Colors.SUCCESS}FOLLOW ME ON GITHUB FOR MORE TOOLS: https://www.github.com/Rip70022 {Colors.RESET}")
                break
            
            clear_screen()
            print_banner()
            
            args.url = None
            args.name = None
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.WARNING}Operation canceled by user.{Colors.RESET}")
            print(f"{Colors.SUCCESS}FOLLOW ME ON GITHUB FOR MORE TOOLS: https://www.github.com/Rip70022 {Colors.RESET}")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n{Colors.ERROR}Critical error: {str(e)}{Colors.RESET}")
        sys.exit(1)
