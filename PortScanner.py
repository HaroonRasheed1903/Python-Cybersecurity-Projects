import pyfiglet
import sys
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def grab_banner(sock):
	try:
		sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
		return sock.recv(1024).decode(errors="ignore").strip()
	except:
		return None


def get_service_name(port):
	try:
		return socket.getservbyport(port)
	except:
		return "Unknown"


def scan_port(target, port):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(1)
		result = sock.connect_ex((target, port))
		if result == 0:
			banner = grab_banner(sock)
			service = get_service_name(port)

			if banner:
				first_line = banner.splitlines()[0][:80]
				print(f"[+] Port {port:5d}/tcp  open  {service:<12}  {first_line}")
			else:
				print(f"[+] Port {port:5d}/tcp  open  {service:<12}  (no banner)")

		sock.close()

	except socket.error as e:
		print(f"socket error occurred on port {port}: {e}")

	except Exception as e:
		print(f"An unexpected error occurred at port {port}: {e}")


def main():
	if len(sys.argv) == 2:
		target = sys.argv[1]
	else:
		print("Invalid number of arguments")
		print("Usage: python3 port_scanner.py <target>")
		sys.exit(1)

	try:
		target_ip = socket.gethostbyname(target)
	except:
		print(f"Unable to resolve target {target}")
		sys.exit(1)

	print("-" * 50)
	ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
	print(ascii_banner)
	print("-" * 50)
	print(f"Scanning the target: {target_ip}")
	print(f"Start time: {datetime.now()}")
	print("-" * 50)

	try:
		with ThreadPoolExecutor(max_workers=300) as executor:
			for port in range(1, 65536):
				executor.submit(scan_port, target_ip, port)

	except KeyboardInterrupt:
		print("\nScanning stopped by user")
		sys.exit(1)

	except socket.error as e:
		print(f"Socket error: {e}")


if __name__ == "__main__":
	main()
