import subprocess
import sys
import os

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

def main():
    print("""
    ███████╗██╗     ███████╗███████╗██╗  ██╗████████╗██████╗  █████╗ ██████╗ ███████╗
    ██╔════╝██║     ██╔════╝██╔════╝██║ ██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
    ███████╗██║     █████╗  █████╗  █████╔╝    ██║   ██████╔╝███████║██║  ██║█████╗  
    ╚════██║██║     ██╔══╝  ██╔══╝  ██╔═██╗    ██║   ██╔══██╗██╔══██║██║  ██║██╔══╝  
    ███████║███████╗███████╗███████╗██║  ██╗   ██║   ██║  ██║██║  ██║██████╔╝███████╗
    ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝
    """)
    print("🚀 Initializing SleekTrade Bot setup and launcher...\n")
    
    # 1. Check for .env file
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("⚠️  .env file not found. Creating a template from .env.example...")
            with open(".env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
            print("✅ .env created. Please make sure to add your API keys there.\n")
        else:
            print("❌ .env.example not found. Please create a .env file with your API keys.")

    # 2. Install requirements
    print("📦 Verifying dependencies...")
    run_command(f"{sys.executable} -m pip install -r requirements.txt")
    print("✅ Dependencies ready.\n")

    # 3. Choose Interface
    print("How would you like to run the bot?")
    print("1) Web Dashboard (Premium UI - Recommended)")
    print("2) CLI Interface (Terminal-based)")
    
    try:
        choice = input("\nEnter choice (1 or 2) [Default 1]: ").strip() or "1"
    except EOFError:
        choice = "1"

    if choice == "1":
        print("\n🌐 Starting Web Dashboard...")
        print("📍 Access it at: http://localhost:8000")
        run_command(f"{sys.executable} app.py")
    else:
        print("\n💻 Starting CLI Interface...")
        run_command(f"{sys.executable} cli.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 SleekTrade closed. Happy trading!")
        sys.exit(0)
