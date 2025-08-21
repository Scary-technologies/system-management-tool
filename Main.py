from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import track
import platform
import psutil
from rich.prompt import Prompt

console = Console()



List_Main_Menu=['1 = Windows','2 = Network','3 = Backup','4 = Software','5 = Internet','0 =📤 Exit']


def Windows():
    
    
    
    List_Menu_Windows=['1 = Windows Defender ','2 = Windows Firewall','3 = Windows Active Status','4 = Windows Update','5 = Windows User Manager']
    for Item in List_Menu_Windows:
        console.print(Item,justify="center")

    
    
    selected=console.input('[blue]Select -----> : [/]')

    if selected == '' or selected == '0' :
        console.clear(True)
    elif selected =='1':
        console.print(f'[green]You Selected {List_Menu_Windows[int(selected)-1]}[/]')
        console.clear(True)
        pass
    elif selected =='2':
        console.print(f'[green]You Selected {List_Menu_Windows[int(selected)-1]}[/]')
        console.clear(True)
        pass
    elif selected =='3':
        console.print(f'[green]You Selected {List_Menu_Windows[int(selected)-1]}[/]')
        console.clear(True)
        pass        
    elif selected =='4':
        console.print(f'[green]You Selected {List_Menu_Windows[int(selected)-1]}[/]')
        console.clear(True)
        pass
    elif selected =='5':
        console.print(f'[green]You Selected {List_Menu_Windows[int(selected)-1]}[/]')
        console.clear(True)
        pass        


def Network():
    List_Menu_Network=[]
    for Item in List_Menu_Network:
        console.print(Item,justify="center")  
    
    
    selected=console.input('[blue]Select -----> : [/]')

    if selected == '' or selected == '0' :
        console.clear(True)
    pass




def Backup():
    List_Menu_Backup=[]
    for Item in List_Menu_Backup:
        console.print(Item,justify="center")  
    
    selected=console.input('[blue]Select -----> : [/]')

    if selected == '' or selected == '0' :
        console.clear(True)
    pass



def Software():
    List_Menu_Software=[]
    for Item in List_Menu_Software:
        console.print(Item,justify="center")  
    
    pass



def Internet():
    pass




    
    
    
    
def show_menu():








    console.rule('''[link=https://github.com/Scary-technologies][blue]Ｓｃａｒｙ－ｔｅｃｈｎｏｌｏｇｉｅｓ By PR-M[/]''')
    console.print('\n')
    
    
    # uname = platform.uname()
    # cpu_count = psutil.cpu_count(logical=True)
    # memory = psutil.virtual_memory()
    
    
    



 
    # Status_Table = Table( show_header=False, header_style="bold magenta",title_justify='center',width=100,)
 

    # Status_Table = Table(title="System Information", title_style="bold yellow")
    # Status_Table.add_column("Property", style="cyan", width=50)
    # Status_Table.add_column("Value", style="green", width=50)

    # Status_Table.add_row("Operating System", f"{uname.system} {uname.release}")
    # Status_Table.add_row("Version", uname.version)
    # Status_Table.add_row("Architecture", uname.machine)
    # Status_Table.add_row("Processor", uname.processor)
    # Status_Table.add_row("CPU Cores", str(cpu_count))
    # Status_Table.add_row("Total RAM", f"{round(memory.total / (1024**3), 2)} GB")
    # Status_Table.add_row("Used RAM", f"{round(memory.used / (1024**3), 2)} GB")
    # Status_Table.add_row("Available RAM", f"{round(memory.available / (1024**3), 2)} GB")

    # console.print(Panel(Status_Table, title="[bold yellow]Status[/bold yellow]", border_style="red")
                  
                  
                   
                #   ,width=50)

    for Item in List_Main_Menu :
        console.print(f'[red][/] {Item} ',justify="center")
        Item.index

    
    
    
    
    
def main():
    while True:
        
        show_menu()
        choice = Prompt.ask("[bold cyan]Select Number: [/] ")

        if choice == "1":
           console.clear(True)
           Windows()
           
        elif choice == "2":
            console.clear(True)
            Network()
            console.print(f"[green]{choice}[/green]")
        elif choice == "3":
            console.clear(True)
            Backup()
            console.print(f"[green]{choice}[/green]")
        elif choice == "4":
            Software()
            console.clear(True)
            console.print(f"[green]{choice}[/green]")
        elif choice == "5":
            Internet()
            console.clear(True)
            console.print(f"[green]{choice}[/green]")
        elif choice == "6":
            console.clear(True)
            console.print(f"[green]{choice}[/green]")
        elif choice == "7":
            console.clear(True)
            console.print(f"[green]{choice}[/green]")
        elif choice == "2":
            console.clear(True)
            console.print(f"[green]{choice}[/green]")
        elif choice == "0" :
            break         
        else:
            console.print("[bold red]Not Find[/bold red]")
            console.clear(True)
        
        
        
        
if __name__ == "__main__":
    main()
