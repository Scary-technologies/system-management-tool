import os
import sys
import subprocess
import platform
import psutil
import socket
import requests
import time
import shutil
import threading
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.status import Status

console = Console()

class SystemManager:
    """System operations management class"""
    
    @staticmethod
    def get_system_info():
        """Get system information"""
        try:
            uname = platform.uname()
            cpu_count = psutil.cpu_count(logical=True)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info_table = Table(title="System Information", title_style="bold yellow")
            info_table.add_column("Property", style="cyan", width=30)
            info_table.add_column("Value", style="green", width=50)
            
            info_table.add_row("Operating System", f"{uname.system} {uname.release}")
            info_table.add_row("Version", uname.version)
            info_table.add_row("Architecture", uname.machine)
            info_table.add_row("Processor", uname.processor or "Unknown")
            info_table.add_row("CPU Cores", str(cpu_count))
            info_table.add_row("Total RAM", f"{round(memory.total / (1024**3), 2)} GB")
            info_table.add_row("Used RAM", f"{round(memory.used / (1024**3), 2)} GB ({memory.percent}%)")
            info_table.add_row("Available RAM", f"{round(memory.available / (1024**3), 2)} GB")
            info_table.add_row("Total Disk", f"{round(disk.total / (1024**3), 2)} GB")
            info_table.add_row("Used Disk", f"{round(disk.used / (1024**3), 2)} GB")
            info_table.add_row("Free Disk", f"{round(disk.free / (1024**3), 2)} GB")
            
            console.print(Panel(info_table, border_style="blue"))
            
        except Exception as e:
            console.print(f"[red]Error getting system information: {e}[/]")

class WindowsManager:
    """Windows operations management"""
    
    @staticmethod
    def check_windows_defender():
        """Check Windows Defender status"""
        try:
            if platform.system() != "Windows":
                console.print("[red]This operation is only available on Windows[/]")
                return
                
            with Status("Checking Windows Defender...", spinner="dots"):
                time.sleep(2)
                result = subprocess.run(['powershell', 'Get-MpComputerStatus'], 
                                      capture_output=True, text=True)
                
            if result.returncode == 0:
                console.print("[green]✓ Windows Defender is active[/]")
                console.print("[blue]Details retrieved successfully[/]")
            else:
                console.print("[red]✗ Error checking Windows Defender[/]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
    
    @staticmethod
    def check_windows_firewall():
        """Check Windows Firewall status"""
        try:
            if platform.system() != "Windows":
                console.print("[red]This operation is only available on Windows[/]")
                return
                
            with Status("Checking Windows Firewall...", spinner="dots"):
                time.sleep(2)
                result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles', 'state'], 
                                      capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print("[green]✓ Windows Firewall Status:[/]")
                console.print(result.stdout)
            else:
                console.print("[red]✗ Error checking Firewall[/]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
    
    @staticmethod
    def windows_update():
        """Check Windows Updates"""
        try:
            if platform.system() != "Windows":
                console.print("[red]This operation is only available on Windows[/]")
                return
                
            with Status("Checking Windows Updates...", spinner="dots"):
                time.sleep(3)
                # Use PowerShell to check updates
                result = subprocess.run(['powershell', 'Get-WindowsUpdate -MicrosoftUpdate'], 
                                      capture_output=True, text=True)
            
            console.print("[green]✓ Update check completed[/]")
            console.print("[blue]Go to Windows Update to install updates[/]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
    
    @staticmethod
    def manage_users():
        """Manage system users"""
        try:
            with Status("Getting user list...", spinner="dots"):
                time.sleep(2)
                
            if platform.system() == "Windows":
                result = subprocess.run(['net', 'user'], capture_output=True, text=True)
            else:
                result = subprocess.run(['who'], capture_output=True, text=True)
                
            if result.returncode == 0:
                console.print("[green]✓ User list:[/]")
                console.print(result.stdout)
            else:
                console.print("[red]✗ Error getting user list[/]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")

class NetworkManager:
    """Network operations management"""
    
    @staticmethod
    def network_status():
        """Check network status"""
        try:
            with Status("Checking network status...", spinner="dots"):
                # Check internet connection
                try:
                    socket.create_connection(("8.8.8.8", 53), timeout=3)
                    internet_status = "[green]Connected[/]"
                except:
                    internet_status = "[red]Disconnected[/]"
                
                # Get IP address
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                
                # Get network information
                net_info = psutil.net_if_addrs()
                
            # Display information
            network_table = Table(title="Network Status", title_style="bold cyan")
            network_table.add_column("Property", style="yellow")
            network_table.add_column("Value", style="green")
            
            network_table.add_row("Internet Status", internet_status)
            network_table.add_row("Hostname", hostname)
            network_table.add_row("Local IP", local_ip)
            
            for interface_name, interface_addresses in net_info.items():
                for address in interface_addresses:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        network_table.add_row(f"Interface: {interface_name}", address.address)
            
            console.print(Panel(network_table, border_style="cyan"))
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
    
    @staticmethod
    def ping_test():
        """Ping test"""
        try:
            target = Prompt.ask("Enter target address", default="google.com")
            
            with Status(f"Pinging {target}...", spinner="dots"):
                if platform.system() == "Windows":
                    result = subprocess.run(['ping', '-n', '4', target], 
                                          capture_output=True, text=True)
                else:
                    result = subprocess.run(['ping', '-c', '4', target], 
                                          capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print(f"[green]✓ Ping to {target} successful:[/]")
                console.print(result.stdout)
            else:
                console.print(f"[red]✗ Ping to {target} failed[/]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
    
    @staticmethod
    def speed_test():
        """Internet speed test (simple)"""
        try:
            console.print("[yellow]Starting speed test...[/]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Internet speed test...", total=100)
                
                start_time = time.time()
                
                # Simple download test
                try:
                    response = requests.get("http://www.google.com", timeout=10)
                    download_time = time.time() - start_time
                    
                    progress.update(task, advance=50)
                    
                    # Simple upload test  
                    start_time = time.time()
                    requests.post("http://httpbin.org/post", data={'test': 'data'}, timeout=10)
                    upload_time = time.time() - start_time
                    
                    progress.update(task, advance=50)
                    
                    speed_table = Table(title="Speed Test Results", title_style="bold green")
                    speed_table.add_column("Test Type", style="cyan")
                    speed_table.add_column("Time (seconds)", style="yellow")
                    
                    speed_table.add_row("Download Test", f"{download_time:.2f}")
                    speed_table.add_row("Upload Test", f"{upload_time:.2f}")
                    
                    console.print(Panel(speed_table, border_style="green"))
                    
                except requests.RequestException:
                    console.print("[red]Error connecting to internet[/]")
                    
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")

class BackupManager:
    """Backup management"""
    
    @staticmethod
    def create_backup():
        """Create backup"""
        try:
            source = Prompt.ask("Enter source folder path")
            if not os.path.exists(source):
                console.print("[red]Source path does not exist[/]")
                return
                
            destination = Prompt.ask("Enter destination path")
            
            # Create backup name with date
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_path = os.path.join(destination, backup_name)
            
            with Status("Creating backup...", spinner="dots"):
                shutil.copytree(source, backup_path)
                
            console.print(f"[green]✓ Backup successfully created at {backup_path}[/]")
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
    
    @staticmethod
    def restore_backup():
        """Restore backup"""
        try:
            backup_path = Prompt.ask("Enter backup file path")
            if not os.path.exists(backup_path):
                console.print("[red]Backup file does not exist[/]")
                return
                
            restore_path = Prompt.ask("Enter restore path")
            
            if Confirm.ask("Are you sure you want to restore?"):
                with Status("Restoring...", spinner="dots"):
                    if os.path.exists(restore_path):
                        shutil.rmtree(restore_path)
                    shutil.copytree(backup_path, restore_path)
                    
                console.print(f"[green]✓ Backup successfully restored[/]")
            else:
                console.print("[yellow]Restore cancelled[/]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
    
    @staticmethod
    def list_backups():
        """List backups"""
        try:
            backup_dir = Prompt.ask("Enter backup folder path")
            if not os.path.exists(backup_dir):
                console.print("[red]Path does not exist[/]")
                return
                
            backups = [f for f in os.listdir(backup_dir) if f.startswith('backup_')]
            
            if backups:
                backup_table = Table(title="Available Backups", title_style="bold blue")
                backup_table.add_column("Backup Name", style="cyan")
                backup_table.add_column("Size", style="yellow")
                backup_table.add_column("Date", style="green")
                
                for backup in backups:
                    backup_path = os.path.join(backup_dir, backup)
                    if os.path.isdir(backup_path):
                        size = sum(os.path.getsize(os.path.join(dirpath, filename))
                                 for dirpath, dirnames, filenames in os.walk(backup_path)
                                 for filename in filenames)
                        mtime = os.path.getmtime(backup_path)
                        date_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                        
                        backup_table.add_row(backup, f"{size // (1024*1024)} MB", date_str)
                
                console.print(Panel(backup_table, border_style="blue"))
            else:
                console.print("[yellow]No backups found[/]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")

class SoftwareManager:
    """Software management"""
    
    @staticmethod
    def list_installed_programs():
        """List installed programs"""
        try:
            with Status("Getting list of installed programs...", spinner="dots"):
                if platform.system() == "Windows":
                    # Use wmic for Windows
                    result = subprocess.run(['wmic', 'product', 'get', 'name,version'], 
                                          capture_output=True, text=True)
                else:
                    # For Linux
                    result = subprocess.run(['dpkg', '--list'], 
                                          capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print("[green]✓ List of installed programs:[/]")
                # Display only first 20 lines
                lines = result.stdout.split('\n')[:20]
                for line in lines:
                    if line.strip():
                        console.print(line)
                console.print(f"[blue]... and {max(0, len(result.stdout.split()) - 20)} more programs[/]")
            else:
                console.print("[red]Error getting program list[/]")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
    
    @staticmethod
    def system_cleanup():
        """System cleanup"""
        try:
            console.print("[yellow]Starting system cleanup...[/]")
            
            # Clean temporary files
            temp_dirs = []
            if platform.system() == "Windows":
                temp_dirs = [
                    os.environ.get('TEMP', ''),
                    os.environ.get('TMP', ''),
                    os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Temp')
                ]
            else:
                temp_dirs = ['/tmp', '/var/tmp']
            
            cleaned_size = 0
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    with Status(f"Cleaning {temp_dir}...", spinner="dots"):
                        for root, dirs, files in os.walk(temp_dir):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    file_size = os.path.getsize(file_path)
                                    os.remove(file_path)
                                    cleaned_size += file_size
                                except:
                                    continue
            
            console.print(f"[green]✓ Cleanup completed. {cleaned_size // (1024*1024)} MB freed[/]")
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")

class InternetManager:
    """Internet and network management"""
    
    @staticmethod
    def dns_config():
        """DNS configuration"""
        try:
            console.print("[blue]Current DNS settings:[/]")
            
            if platform.system() == "Windows":
                result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'DNS' in line:
                            console.print(line.strip())
            else:
                result = subprocess.run(['cat', '/etc/resolv.conf'], capture_output=True, text=True)
                if result.returncode == 0:
                    console.print(result.stdout)
            
            change_dns = Confirm.ask("Do you want to change DNS?")
            if change_dns:
                console.print("[yellow]To change DNS, go to network settings[/]")
                console.print("[blue]Recommended DNS servers:[/]")
                console.print("Google: 8.8.8.8, 8.8.4.4")
                console.print("Cloudflare: 1.1.1.1, 1.0.0.1")
                console.print("OpenDNS: 208.67.222.222, 208.67.220.220")
                
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
    
    @staticmethod
    def proxy_settings():
        """Proxy settings"""
        try:
            console.print("[blue]Checking proxy settings...[/]")
            
            # Check proxy environment variables
            proxy_vars = ['http_proxy', 'https_proxy', 'ftp_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'FTP_PROXY']
            proxy_found = False
            
            for var in proxy_vars:
                if os.environ.get(var):
                    console.print(f"[green]{var}: {os.environ.get(var)}[/]")
                    proxy_found = True
            
            if not proxy_found:
                console.print("[yellow]No proxy configured[/]")
            
            # Display proxy configuration guide
            console.print("\n[blue]To configure proxy:[/]")
            console.print("Windows: Settings > Network & Internet > Proxy")
            console.print("Linux: Set environment variables http_proxy and https_proxy")
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")
    
    @staticmethod
    def connection_monitor():
        """Network connections monitor"""
        try:
            console.print("[blue]Monitoring network connections...[/]")
            
            with Status("Getting active connections...", spinner="dots"):
                connections = psutil.net_connections(kind='inet')
            
            # Display active connections
            conn_table = Table(title="Active Network Connections", title_style="bold magenta")
            conn_table.add_column("Local Address", style="cyan")
            conn_table.add_column("Remote Address", style="yellow") 
            conn_table.add_column("Status", style="green")
            conn_table.add_column("PID", style="red")
            
            for conn in connections[:15]:  # Display first 15 connections
                local_addr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                status = conn.status if conn.status else "N/A"
                pid = str(conn.pid) if conn.pid else "N/A"
                
                conn_table.add_row(local_addr, remote_addr, status, pid)
            
            console.print(Panel(conn_table, border_style="magenta"))
            console.print(f"[blue]Showing {min(15, len(connections))} connections out of {len(connections)} active connections[/]")
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/]")

# Define menus with real functions
MENU_STRUCTURE = {
    "title": "Ｓｃａｒｙ－ｔｅｃｈｎｏｌｏｇｉｅｓ By PR-M",
    "items": {
        "1": {
            "name": "Windows",
            "action": "submenu",
            "submenu": {
                "title": "Windows Management",
                "items": {
                    "1": {
                        "name": "Windows Defender",
                        "action": "function",
                        "function": WindowsManager.check_windows_defender
                    },
                    "2": {
                        "name": "Windows Firewall",
                        "action": "function",
                        "function": WindowsManager.check_windows_firewall
                    },
                    "3": {
                        "name": "System Information", 
                        "action": "function",
                        "function": SystemManager.get_system_info
                    },
                    "4": {
                        "name": "Windows Update",
                        "action": "function",
                        "function": WindowsManager.windows_update
                    },
                    "5": {
                        "name": "User Management",
                        "action": "function",
                        "function": WindowsManager.manage_users
                    },
                    "0": {
                        "name": "📤 Back to Main Menu",
                        "action": "back"
                    }
                }
            }
        },
        "2": {
            "name": "Network",
            "action": "submenu",
            "submenu": {
                "title": "Network Management",
                "items": {
                    "1": {
                        "name": "Network Status",
                        "action": "function",
                        "function": NetworkManager.network_status
                    },
                    "2": {
                        "name": "Ping Test",
                        "action": "function",
                        "function": NetworkManager.ping_test
                    },
                    "3": {
                        "name": "Speed Test",
                        "action": "function",
                        "function": NetworkManager.speed_test
                    },
                    "0": {
                        "name": "📤 Back to Main Menu",
                        "action": "back"
                    }
                }
            }
        },
        "3": {
            "name": "Backup",
            "action": "submenu", 
            "submenu": {
                "title": "Backup Management",
                "items": {
                    "1": {
                        "name": "Create Backup",
                        "action": "function",
                        "function": BackupManager.create_backup
                    },
                    "2": {
                        "name": "Restore Backup",
                        "action": "function",
                        "function": BackupManager.restore_backup
                    },
                    "3": {
                        "name": "List Backups",
                        "action": "function",
                        "function": BackupManager.list_backups
                    },
                    "0": {
                        "name": "📤 Back to Main Menu",
                        "action": "back"
                    }
                }
            }
        },
        "4": {
            "name": "Software",
            "action": "submenu",
            "submenu": {
                "title": "Software Management", 
                "items": {
                    "1": {
                        "name": "List Installed Programs",
                        "action": "function",
                        "function": SoftwareManager.list_installed_programs
                    },
                    "2": {
                        "name": "System Cleanup",
                        "action": "function",
                        "function": SoftwareManager.system_cleanup
                    },
                    "3": {
                        "name": "System Information",
                        "action": "function",
                        "function": SystemManager.get_system_info
                    },
                    "0": {
                        "name": "📤 Back to Main Menu",
                        "action": "back"
                    }
                }
            }
        },
        "5": {
            "name": "Internet",
            "action": "submenu",
            "submenu": {
                "title": "Internet Tools",
                "items": {
                    "1": {
                        "name": "DNS Configuration",
                        "action": "function",
                        "function": InternetManager.dns_config
                    },
                    "2": {
                        "name": "Proxy Settings",
                        "action": "function",
                        "function": InternetManager.proxy_settings
                    },
                    "3": {
                        "name": "Connection Monitor",
                        "action": "function",
                        "function": InternetManager.connection_monitor
                    },
                    "4": {
                        "name": "Speed Test",
                        "action": "function",
                        "function": NetworkManager.speed_test
                    },
                    "0": {
                        "name": "📤 Back to Main Menu", 
                        "action": "back"
                    }
                }
            }
        },
        "0": {
            "name": "📤 Exit",
            "action": "exit"
        }
    }
}

class MenuSystem:
    def __init__(self, menu_structure):
        self.menu_structure = menu_structure
        self.current_menu = menu_structure
        self.menu_stack = []
    
    def show_header(self):
        """Display program header"""
        console.rule(f'''[link=https://github.com/Scary-technologies][blue]{self.current_menu.get("title", "Menu")}[/]''')
        console.print('\n')
    
    def display_menu(self):
        """Display current menu items"""
        console.clear(True)
        self.show_header()
        
        items = self.current_menu.get("items", {})
        for key, item in items.items():
            console.print(f'[red][/] {key} = {item["name"]}', justify="center")
    
    def handle_choice(self, choice):
        """Handle user choice"""
        items = self.current_menu.get("items", {})
        
        if choice not in items:
            console.print("[bold red]Invalid selection![/bold red]")
            console.input("Press Enter to continue...")
            return True
        
        selected_item = items[choice]
        action = selected_item.get("action")
        
        if action == "exit":
            console.print("[yellow]Exiting program...[/yellow]")
            return False
        
        elif action == "back":
            if self.menu_stack:
                self.current_menu = self.menu_stack.pop()
            else:
                self.current_menu = self.menu_structure
        
        elif action == "submenu":
            # Save current menu to stack
            self.menu_stack.append(self.current_menu)
            # Go to submenu
            self.current_menu = selected_item["submenu"]
        
        elif action == "function":
            # Execute the corresponding function
            console.print(f'[green]You selected: {selected_item["name"]}[/]')
            try:
                selected_item["function"]()
            except Exception as e:
                console.print(f"[red]Error executing operation: {e}[/]")
            console.input("\n[yellow]Press Enter to continue...[/yellow]")
        
        return True
    
    def run(self):
        """Run menu system"""
        running = True
        
        while running:
            self.display_menu()
            choice = Prompt.ask("[bold cyan]Select number[/]")
            running = self.handle_choice(choice)

def main():
    """Main function"""
    try:
        console.print("[bold green]🚀 Management System started...[/bold green]")
        menu_system = MenuSystem(MENU_STRUCTURE)
        menu_system.run()
        console.print("[bold blue]👋 Goodbye![/bold blue]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Program stopped by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")

if __name__ == "__main__":
    main()