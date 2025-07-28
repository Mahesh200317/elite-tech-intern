from port_scanner import run_port_scanner
from brute_forcer import run_brute_forcer

def main():
    print("🔧 Python Penetration Testing Toolkit")
    print("1. Port Scanner")
    print("2. Brute Forcer")
    choice = input("Select a tool (1/2): ")

    if choice == '1':
        run_port_scanner()
    elif choice == '2':
        run_brute_forcer()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()

