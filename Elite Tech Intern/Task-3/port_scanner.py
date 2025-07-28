import socket

def run_port_scanner():
    target = "127.0.0.1"
    start_port = 75
    end_port = 85

    print(f"\n🔎 Scanning {target} from port {start_port} to {end_port}...\n")

    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((target, port))
            if result == 0:
                print(f"✅ Port {port} is OPEN")

if __name__ == "__main__":
    run_port_scanner()
