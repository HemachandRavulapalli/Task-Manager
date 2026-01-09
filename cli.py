import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt
from rich.table import Table
from bot import BasicBot

load_dotenv()

console = Console()

def display_menu():
    table = Table(title="Binance Futures Testnet Bot", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="dim", width=12)
    table.add_column("Description")
    
    table.add_row("1", "View Balance (USDT)")
    table.add_row("2", "Place Market Order")
    table.add_row("3", "Place Limit Order")
    table.add_row("4", "Place Stop-Limit Order")
    table.add_row("5", "View Open Orders")
    table.add_row("6", "Exit")
    
    console.print(table)

def main():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret or "your_testnet" in api_key:
        console.print("[bold red]Error:[/] API credentials not found or placeholder in .env file.")
        api_key = Prompt.ask("Enter your Binance Testnet API Key")
        api_secret = Prompt.ask("Enter your Binance Testnet API Secret", password=True)

    try:
        bot = BasicBot(api_key, api_secret)
        console.print("[bold green]Success:[/] Connected to Binance Futures Testnet.")
    except Exception as e:
        console.print(f"[bold red]Initialization Failed:[/] {str(e)}")
        return

    while True:
        display_menu()
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6"])

        try:
            if choice == "1":
                balance = bot.get_futures_balance()
                if balance:
                    console.print(Panel(f"Asset: [bold]{balance['asset']}[/]\nBalance: [bold]{balance['balance']}[/]\nAvailable: [bold]{balance['availableBalance']}[/]", title="Account Balance"))
                else:
                    console.print("[yellow]No USDT balance found.[/]")

            elif choice == "2":
                symbol = Prompt.ask("Symbol (e.g., BTCUSDT)", default="BTCUSDT").upper()
                side = Prompt.ask("Side", choices=["BUY", "SELL"])
                quantity = FloatPrompt.ask("Quantity")
                order = bot.place_market_order(symbol, side, quantity)
                console.print(f"[bold green]Order Placed![/] ID: {order['orderId']}")

            elif choice == "3":
                symbol = Prompt.ask("Symbol (e.g., BTCUSDT)", default="BTCUSDT").upper()
                side = Prompt.ask("Side", choices=["BUY", "SELL"])
                quantity = FloatPrompt.ask("Quantity")
                price = FloatPrompt.ask("Price")
                order = bot.place_limit_order(symbol, side, quantity, price)
                console.print(f"[bold green]Order Placed![/] ID: {order['orderId']}")

            elif choice == "4":
                symbol = Prompt.ask("Symbol (e.g., BTCUSDT)", default="BTCUSDT").upper()
                side = Prompt.ask("Side", choices=["BUY", "SELL"])
                quantity = FloatPrompt.ask("Quantity")
                price = FloatPrompt.ask("Price")
                stop_price = FloatPrompt.ask("Stop Price")
                order = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                console.print(f"[bold green]Order Placed![/] ID: {order['orderId']}")

            elif choice == "5":
                symbol = Prompt.ask("Symbol (optional, press enter for all)", default="")
                orders = bot.get_open_orders(symbol=symbol if symbol else None)
                if not orders:
                    console.print("[yellow]No open orders found.[/]")
                else:
                    order_table = Table(title="Open Orders")
                    order_table.add_column("ID")
                    order_table.add_column("Symbol")
                    order_table.add_column("Type")
                    order_table.add_column("Side")
                    order_table.add_column("Price")
                    order_table.add_column("Qty")
                    
                    for o in orders:
                        order_table.add_row(str(o['orderId']), o['symbol'], o['type'], o['side'], o['price'], o['origQty'])
                    console.print(order_table)

            elif choice == "6":
                console.print("[bold blue]Goodbye![/]")
                break

        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")

if __name__ == "__main__":
    main()
