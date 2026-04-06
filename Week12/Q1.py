# ============================================================
#  WEEK 12 LAB — Q1: SCANNER INHERITANCE
#  COMP2152 — Joshua Zaakir
# ============================================================

import socket
import urllib.request


class Scanner:
    """Parent class — shared by all scanner types."""

    def __init__(self, target):
        self.target = target
        self.results = []

    def display_results(self):
        """
        Shared method used by all scanner types to print results
        in a simple and readable format.
        """
        print(f"Results for {self.target}:")
        if not self.results:
            print("  (no results)")
        else:
            for result in self.results:
                print(f"  {result}")


class PortScanner(Scanner):
    """Child class — scans for open ports."""

    def __init__(self, target, ports):
        # Call the parent constructor so target and results are set up
        super().__init__(target)
        self.ports = ports

    def scan(self):
        """
        Loops through the given ports and checks whether each one is open.
        connect_ex() returns 0 when the connection succeeds.
        """
        for port in self.ports:
            scanner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scanner_socket.settimeout(1)

            result = scanner_socket.connect_ex((self.target, port))

            if result == 0:
                self.results.append(f"Port {port}: OPEN")
            else:
                self.results.append(f"Port {port}: closed")

            scanner_socket.close()


class HTTPScanner(Scanner):
    """Child class — scans HTTP paths for accessible pages."""

    def __init__(self, target, paths):
        # Reuse the parent setup
        super().__init__(target)
        self.paths = paths

    def scan(self):
        """
        Tries to open each HTTP path on the target.
        If the page responds, it gets marked accessible.
        If not, it is treated as not found.
        """
        for path in self.paths:
            try:
                response = urllib.request.urlopen(f"http://{self.target}{path}")
                self.results.append(f"{path} → {response.status} (accessible)")
            except Exception:
                self.results.append(f"{path} → NOT FOUND")


# --- Main (provided) ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Q1: SCANNER INHERITANCE")
    print("=" * 60)

    print("\n--- Port Scanner ---")
    ps = PortScanner("127.0.0.1", [22, 80, 443])
    print(f"  Scanning {ps.target} ports...")
    ps.scan()
    ps.display_results()

    print("\n--- HTTP Scanner ---")
    hs = HTTPScanner("127.0.0.1", ["/", "/admin", "/.git/config"])
    print(f"  Scanning {hs.target} paths...")
    hs.scan()
    hs.display_results()

    print("\n" + "=" * 60)