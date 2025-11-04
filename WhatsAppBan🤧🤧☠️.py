import os
import time
import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.align import Align
from rich.prompt import Prompt
import json
import subprocess
import random
import threading
from datetime import datetime, timedelta
from fake_useragent import UserAgent
import string
import uuid

console = Console()

USER_LOGO = """[bold red]⢀⣠⣴⣖⣺⣿⣍⠙⠛⠒⠦⣤⣀                        ⢀⣠⡤⠖⠚⠋⠉⣿⣟⣒⣶⣤⣀
⠙⠉⠉⠉⠉⠙⠛⢶⣶⡦  ⠉⠳⣤                    ⢀⡴⠛⠁  ⣶⣶⠞⠛⠉⠉⠉⠉⠙
        ⠈⠛⢿⣟⣀⡀⠈⠳⣄                ⢀⡴⠋ ⢀⢐⣿⠟⠋        
           ⠙⢿⡟  ⠘⢷⡀    ⡀        ⣰⠟⠁ ⠘⣿⠟⠁          
             ⠻⣿⠃  ⢻⣆⠼⣷⣤⣇⣱⣶⣸⣧⣴⡦⢔⣶⠃  ⢻⡿⠃            
              ⠘⣿⠿⠉⠛⣿⣷⣿⣿⣿⣿⣼⣿⣿⣿⣷⣿⡟⠋⠹⣿⡟⠁             
               ⣸⣦⡶⠟⠛⠛⠿⠿⠋  ⠈⠻⠿⠟⠋⠛⠷⣦⣞⡀              
            ⢀⣴⠟⠛⢻⡄               ⣼⠛⠛⠷⣄            
           ⣠⠟   ⠈⣷ ⣀⣀⡀      ⢀⣀⣤⡀⢰⡏   ⠈⠳⡄          
         ⣠⠞⣁⣠⣤⣤⡤⠴⣿ ⢸⣨⣿⣧⣀⣀⣀⣀⣠⣾⣧⣸ ⢸⡷⠦⣤⣤⣤⣄⡘⢦⡀        
      ⣀⡤⣞⣷⣾⣿⠿⠛⠁  ⣿⡀ ⠛⠿⠿⠋⣉⢋⣉⠙⠿⠟⠃ ⣸⡇  ⠙⠻⢿⣿⣶⣝⣦⣄⡀     
  ⠈⠛⠛⠛⠓⠛⠛⠉⠁      ⠘⢷⡀⠠⣀  ⠈⡟⠁ ⢀⡠ ⣰⠟       ⠉⠙⠛⠛⠛⠛⠛⠋  
                   ⠙⢦⡈⢳⡀ ⠁ ⡰⠋⣰⠞⠁                  
                 ⣀⣤⣤⣾⣿⡖⠃   ⠃⣾⣿⣦⣤⣄⡀                
               ⣴⣿⣿⣿⣿⣿⣿⣟⠓⢶⣴⠞⠚⣿⣿⣿⣿⣿⣿⣷⡀              
           ⠤⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⡛⠲⣶⣿⡶⠚⣹⣿⣿⣿⣿⣿⣿⣿⣦⣀⡀           
        ⠈⠙⠒⠒⠋⣹⣿⠟⢹⣿⣿⣿⣿⣿⣷⣤⣬⣥⣤⣴⣿⣿⣿⣿⣿⣿⡙⣿⣿⡉⠑⠒⠂         
         ⠑⠂⢤⣴⣏⣾⣴⡿⣿⣿⣿⣿⣿⣿⣿⠞⠙⢾⣿⣿⣿⣻⣿⣿⣿⣧⣼⣏⣷⣤⠄⠂         
        ⠒⠒⠚⠉ ⢹⢋⡿⠉⢹⢻⡟⣿⣿⣯⢿⣆⢀⣾⢯⣿⣿⡟⣿⢻⡉⠹⣏⢻⠁ ⠙⠒⠒        
            ⣠⠋⠁⢀⡴⣻⣸⡿⠿⡏⡇⠈⣿⣿⡏⠈⡛⡿⠿⣿⣘⡷⣄⡀⠉⢳⡀           
           ⠊⠉⠉⠉⠁⠙⢁⠞  ⡷⠁⣠⠋⡟⢣⡀⠱⡇ ⠈⢆⠙⠁⠉⠉⠉⠉⠒          
              ⢀⡠⠖⠁  ⢠⡿⠚⠁   ⠙⠲⣤   ⠑⠢⢄              
                   ⢀⡜        ⠑⠄                   
[bold white]          WHATSAPP REPORTER - BANGLADESH[/bold white]"""

MAIN_LOGO = USER_LOGO

class WhatsAppReporter:
    def __init__(self):
        self.device_id = self.get_device_id()
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
                
    def get_device_id(self):
        device_file = "/data/data/com.termux/files/usr/bin/device_id.txt"
        if os.path.exists(device_file):
            with open(device_file, "r") as f:
                return f.read().strip()
        else:
            new_device_id = str(uuid.uuid4())
            with open(device_file, "w") as f:
                f.write(new_device_id)
            return new_device_id
    
    def show_logo(self):
        self.clear_screen()
        console.print(
            Panel(
                Align.center(USER_LOGO),
                title="[bold cyan]WELCOME TO WHATSAPP REPORTER[/bold cyan]",
                style="bold red"
            )
        )
    
    def show_features(self):
        features_content = """    ┏┓┏┓┳┓┳┏┓┏┳┓  ┳┓┏┓┳┓┳┓┏┓┳┓  ┏┓┓┏┏┓┏┳┓┏┓┳┳┓    
━━  ┗┓┃ ┣┫┃┃┃ ┃   ┣┫┣┫┃┃┃┃┣ ┃┃  ┗┓┗┫┗┓ ┃ ┣ ┃┃┃  ━━
    ┗┛┗┛┛┗┻┣┛ ┻   ┻┛┛┗┛┗┛┗┗┛┻┛  ┗┛ ┗┗┛ ┻ ┗┛┛ ┗    

    -𝐌𝐨𝐝𝐢𝐟𝐢𝐞𝐝 𝐁𝐲 𝐑𝐢𝐝𝐡𝐰𝐚𝐧
                                                      
🎁 [bold white]FEATURES YOU GET AS A [bold white]FREE USER:[/bold white]

[bold green]▶ ⚡ AUTOMATED REPORTING SYSTEM[/bold green]
[bold green]▶ 👑 MULTIPLE PROXY SUPPORT[/bold green]
[bold green]▶ 🔄 RANDOM USER AGENTS[/bold green]
[bold green]▶ 🔥 24-HOUR COOLDOWN PROTECTION[/bold green]
[bold green]▶ 🍁 BANGLADESH NUMBERS ONLY[/bold green]
[bold green]▶ 🔐 SECURE & ANONYMOUS[/bold green]
[bold green]▶ 📤 AUTOMATED SPAM DETECTION BYPASS[/bold green]
[bold green]▶ 🤙 WORKS WITH BD NUMBERS (01XXXXXXXXX)[/bold green]

[bold white]🎯 THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY
[bold white]🚀 USE RESPONSIBLY AND AT YOUR OWN RISK"""

        console.print(
            Panel(
                features_content,
                title="[bold yellow]👋 WELCOME USER 😁[/bold yellow]",
                style="bold magenta"
            )
        )
        
        console.print(
            Panel(
                f"[bold white]🌐 DEVICE ID : {self.device_id}[/bold white]",
                title="[bold cyan]YOUR UNIQUE IDENTIFIER[/bold cyan]",
                style="bold white"
            )
        )
    
    def show_loading(self):
        with Progress(
            SpinnerColumn("dots", style="bold cyan"),
            TextColumn("[bold green]INITIALIZING SYSTEM[/bold green]"),
            BarColumn(bar_width=40, complete_style="bold cyan"),
            transient=True,
        ) as progress:
            task = progress.add_task("", total=100)
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.03)
    
    def start_system(self):
        self.show_logo()
        self.show_features()
        self.show_loading()
        
        console.print(
            Panel(
                "[bold green]✅ System Ready\n"
                "✅ Press ENTER to Continue![/bold green]",
                title="[bold green]👋 SYSTEM INITIALIZED 🍁[/bold green]",
                style="bold green"
            )
        )
        Prompt.ask("[bold white]Press ENTER[/bold white] to Continue")
        return True
    
    def run_main_script(self):
        self.clear_screen()
        self.main_script()
    
    def main_script(self):
        limit_hours = 24
        # FIXED: Changed log file location to Termux home directory
        log_file = "/data/data/com.termux/files/home/WhatsApp_Reporter_Log.json"

        def clear():
            os.system('clear' if os.name == 'posix' else 'cls')

        def setup_proxy(port):
            """Setup proxy without requiring tinyproxy installation"""
            # Use free proxy servers instead of local tinyproxy
            free_proxies = [
                "103.155.62.158:8080",
                "45.7.210.5:999",
                "186.67.26.181:999",
                "190.61.88.147:8080",
                "45.230.172.212:999",
                "103.148.39.50:8080",
                "45.231.221.1:999",
                "190.52.244.50:999",
                "45.175.239.25:999",
                "181.176.221.151:9812"
            ]
            return random.choice(free_proxies)

        def validate_proxy(proxy):
            """Validate if proxy is working"""
            try:
                test_url = "http://httpbin.org/ip"
                proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
                r = requests.get(test_url, proxies=proxies, timeout=10)
                return r.status_code == 200
            except:
                return False

        def get_working_proxies():
            """Get list of working proxies"""
            console.print("[bold yellow]╭───────────╯\n╰─> [ CHECKING PROXIES... ][/bold yellow]")
            
            proxies = []
            for i in range(10):
                proxy = setup_proxy(8888 + i)  # port parameter is now ignored
                if validate_proxy(proxy):
                    proxies.append(proxy)
                    console.print(f"[bold green]╰─> [ PROXY {i+1}: WORKING ][/bold green]")
                else:
                    console.print(f"[bold red]╰─> [ PROXY {i+1}: FAILED ][/bold red]")
                time.sleep(0.5)
            
            return proxies

        def random_user_agent():
            return UserAgent().random

        def random_cookies():
            csrf_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            return {
                'wa_csrf': csrf_token,
                'wa_lang_pref': 'en',
                'wa_ul': session_id
            }

        def random_string(length=10):
            return ''.join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(length))

        def send_report(phone_number, proxies):
            url = 'https://www.whatsapp.com/contact/noclient/'
            
            report_texts = [
                f"🌟 *VERIFIED ONLINE PLATFORM* 🌟\n\n✅ International License\n✅ Encrypted Security System\n✅ Fast Deposit & Withdrawal Process\n✅ 24/7 Professional Customer Service\n\n🎰 *JACKPOT UP TO 20 MILLION TAKA!* 🎰\nWith minimum deposit 500tk, big winning chances are wide open!\n\n📱 *CONTACT ADMIN ON WHATSAPP:*\n[+880{phone_number}]\n\n🔒 *Guaranteed Security & Trusted Since 2018* 🔒",
                f"🦅 *PREMIUM PLATFORM* 🦅\n\n⭐ *BEST BONUSES IN THE INDUSTRY:*\n• New Member Bonus 200%\n• Daily Bonus up to 500%\n• Weekly Cashback 15%\n• Lifetime Referral Bonus\n\n💎 *SUPERIOR FEATURES:*\n• Unlimited & Fast WD\n• Guaranteed Fair Play System\n• 100+ Complete Slot Games\n\n📞 *CONTACT ADMIN ON WHATSAPP:*\n[+880{phone_number}]\n\n🛡️ *Legal & Verified by International Body* 🛡️",
                f"🗽 *INTERNATIONAL STANDARD PLATFORM* 🗽\n\n🎯 *LATEST TECHNOLOGY:*\n• Highest RTP 99.9%\n• Verified Auto Win System\n• Minimum Deposit 100tk\n• Any Amount WD Guaranteed Paid\n\n✨ *ADVANTAGES:*\n• Professional 24 Hour Support\n• Instant Transaction Process\n• Progressive Jackpot Every Day\n\n📲 *CONTACT CUSTOMER SERVICE ON WHATSAPP:*\n[+880{phone_number}]\n\n💫 *Verified & Recommended by Bettors* 💫",
                f"👑 *PREMIUM CLASS PLATFORM* 👑\n\n🏆 *RECORDED ACHIEVEMENTS:*\n• Consistent Win Rate 95%\n• Thousands of Active Members\n• Rating ⭐⭐⭐⭐⭐ 4.9/5.0\n• Choice of Professional Bettors\n\n💰 *EXCLUSIVE BONUSES:*\n• Welcome Bonus 300%\n• Loss Cashback 20%\n• Special Birthday Bonus\n• Member Loyalty Bonus\n\n📞 *DEDICATED SUPPORT ADMIN ON WHATSAPP:*\n[+880{phone_number}]\n\n🎖️ *Trusted & Legally Verified* 🎖️",
                f"🔥 *BEST PLATFORM 2024* 🔥\n\n💎 *WORLD CLASS FACILITIES:*\n• Proven Winrate 97%\n• Anti-Loss System\n• Daily Jackpot Awaits\n• Minimum Deposit 200tk\n\n🚀 *PREMIUM SERVICE:*\n• Fast Response < 3 Minutes\n• 24/7 Transaction Assistance\n• Free Game Consultation\n• Winning Tips from Experts\n\n📱 *OFFICIAL MANAGEMENT CONTACT ON WHATSAPP:*\n[+880{phone_number}]\n\n🏅 *Verified & Recommended by Official Community* 🏅"
            ]
            
            headers = {
                'authority': 'www.whatsapp.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://www.whatsapp.com',
                'referer': 'https://www.whatsapp.com/contact/?subject=messenger',
                'sec-ch-ua': f'"{random.choice(["Not-A.Brand", "Chromium"])}";v="{random.randint(90, 99)}", "Chromium";v="{random.randint(110, 124)}"',
                'sec-ch-ua-mobile': random.choice(['?0', '?1']),
                'sec-ch-ua-platform': f'"{random.choice(["Windows", "Android", "iOS"])}"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': random_user_agent(),                
            }

            proxy = random.choice(proxies)
            proxy_config = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            
            data = {
                'country_selector': 'BD',
                'email': f'{random_string()}@gmail.com',
                'email_confirm': f'{random_string()}@gmail.com',
                'phone_number': phone_number,
                'platform': random.choice(['WHATS_APP_WEB_DESKTOP', 'WHATS_APP_ANDROID']),
                'your_message': random.choice(report_texts),
                'step': 'submit',
            }

            try:
                response = requests.post(url, headers=headers, data=data, proxies=proxy_config, cookies=random_cookies(), timeout=10)
                if response.status_code == 200:
                    console.print(f"\n[bold cyan]╭───────────╯\n╰─> [ 200 ] : +880{phone_number}[/bold cyan]")
                    return True
                else:
                    console.print(f"\n[bold red]╭───────────╯\n╰─> [ {response.status_code} ] : +880{phone_number}[/bold red]")
                    return False
            except Exception as e:
                console.print(f"\n[bold red]╭───────────╯\n╰─> [ ERROR: {str(e)[:50]} ][/bold red]")
                return False

        def load_log():
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    try:
                        return json.load(f)
                    except:
                        return {}
            return {}

        def save_log(phone_number):
            log_data = load_log()
            log_data[phone_number] = datetime.now().isoformat()
            with open(log_file, "w") as f:
                json.dump(log_data, f)

        def restart_countdown(remaining_time):
            total = int(remaining_time.total_seconds())
            try:
                from rich.live import Live
                from rich.text import Text
                
                countdown_message = Text("", style="bold yellow")
                
                with Live(countdown_message, refresh_per_second=4, console=console) as live:
                    while total > 0:
                        hours, remainder = divmod(total, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        countdown_message = Text(f"╰─> WAIT UNTIL: {hours:02}:{minutes:02}:{seconds:02}", style="bold yellow")
                        live.update(countdown_message)
                        time.sleep(1)
                        total -= 1
                
                console.print("[bold green]╭───────────╯\n╰─> [ STARTING REPORT SPAM ][/bold green]\n")
                main()
            except ImportError:
                try:
                    while total > 0:
                        hours, remainder = divmod(total, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        print(f"\r╰─> WAIT UNTIL: {hours:02}:{minutes:02}:{seconds:02}", end="", flush=True)
                        time.sleep(1)
                        total -= 1
                    print("\n")
                    console.print("[bold green]╭───────────╯\n╰─> [ STARTING REPORT SPAM ][/bold green]\n")
                    main()
                except KeyboardInterrupt:
                    console.print("\n[bold red]╭───────────╯\n╰─> [ STOPPED ][/bold red]")
            except KeyboardInterrupt:
                console.print("\n[bold red]╭───────────╯\n╰─> [ STOPPED ][/bold red]")

        def main():
            clear()
            console.print(Panel(MAIN_LOGO, style="bold red")) 
            # FIXED: Updated script info as requested
            console.print(Panel("""[bold white]CREATED : NOTCTBER
[bold white]VERSION : 1.1.0
[bold white]UPDATED : 24.10.2025""",
title="[bold cyan]SCRIPT INFO[/bold cyan]",
style="bold red"))
            console.print(Panel("""[bold white]Enter Target Number Without +880 and Without SPACES. Just plain 01XXXXXXXXX. Example: 01712345678 Then Press ENTER""",
title="[bold cyan]TARGET NUMBER[/bold cyan]",
style="bold red"))
            console.print("[bold red]╭───────────╯")
            phone_number = console.input("[bold red]╰─> [bold white]+880[/bold white][/bold red]")

            if not phone_number.isdigit() or not phone_number.startswith("01") or len(phone_number) != 11:
                console.print("[bold red]╰─> [ ENTER VALID BANGLADESH NUMBER! START WITH 01XXXXXXXXX ][/bold red]")
                time.sleep(2)
                main()
                return

            log_data = load_log()
            if phone_number in log_data:
                last_spam = datetime.fromisoformat(log_data[phone_number])
                remaining_time = timedelta(hours=limit_hours) - (datetime.now() - last_spam)
                if remaining_time.total_seconds() > 0:
                    console.print(f"[bold yellow]╭───────────╯\n╰─> [ COOLDOWN ACTIVE FOR THIS NUMBER ][/bold yellow]")
                    restart_countdown(remaining_time)
                    return

            save_log(phone_number)

            # Get working proxies
            proxy_list = get_working_proxies()

            if not proxy_list:
                console.print("[bold red]╭───────────╯\n╰─> [ NO WORKING PROXIES FOUND, USING DIRECT CONNECTION ][/bold red]")
                proxy_list = [None]  # Use direct connection as fallback

            console.print(f"[bold green]╭───────────╯\n╰─> [ {len(proxy_list)} PROXIES READY ][/bold green]")
            time.sleep(2)

            def spam_job():
                send_report(phone_number, proxy_list)

            with Progress() as progress:
                task = progress.add_task("[bold cyan]SENDING REPORTS |", total=10)
                threads = []
                successful_reports = 0
                
                for i in range(10):
                    t = threading.Thread(target=spam_job)
                    t.start()
                    threads.append(t)
                    progress.update(task, advance=1)
                    time.sleep(random.randint(2, 4))
                
                for t in threads:
                    t.join()

            console.print(f"[bold green]╭───────────╯\n╰─> [ REPORTS COMPLETED - 24H COOLDOWN STARTED ][/bold green]")
            restart_countdown(timedelta(hours=limit_hours))

        main()

    def run(self):
        if self.start_system():
            self.run_main_script()

if __name__ == "__main__":
    app = WhatsAppReporter()
    app.run()
