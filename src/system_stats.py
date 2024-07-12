import time
import subprocess
import psutil
import curses


class SystemMonitor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_curses()

    def setup_curses(self):
        curses.curs_set(0)  # Hide the cursor
        self.stdscr.nodelay(1)  # Make getch non-blocking

    def get_temperature(self):
        result = subprocess.run(['sensors'], capture_output=True, text=True)
        return result.stdout

    def get_power_consumption(self):
        try:
            with open("/sys/class/power_supply/battery/power_now", "r") as file:
                power = int(file.read().strip()) / 1_000_000  # Convert microWatts to Watts
            return f"{power} W"
        except FileNotFoundError:
            return "Power data not available"

    def display_metrics(self):
        while True:
            self.stdscr.clear()
            self.display_cpu_metrics()
            self.display_memory_metrics()
            self.display_disk_metrics()
            self.display_network_metrics()
            self.display_temperature()
            self.display_power_consumption()

            self.stdscr.refresh()
            time.sleep(1)
            if self.stdscr.getch() == ord('q'):  # Press 'q' to quit
                break

    def display_cpu_metrics(self):
        cpu_usage = psutil.cpu_percent()
        cpu_free = 100 - cpu_usage
        self.stdscr.addstr(0, 0, "CPU Usage:", curses.A_BOLD)
        self.stdscr.addstr(1, 0, f"{cpu_usage}% used, {cpu_free}% free")

    def display_memory_metrics(self):
        memory = psutil.virtual_memory()
        self.stdscr.addstr(3, 0, "RAM Usage:", curses.A_BOLD)
        self.stdscr.addstr(4, 0, f"{memory.percent}% used, {100 - memory.percent}% free")

    def display_disk_metrics(self):
        disk = psutil.disk_usage('/')
        self.stdscr.addstr(6, 0, "Disk Usage:", curses.A_BOLD)
        self.stdscr.addstr(7, 0, f"{disk.percent}% used, {100 - disk.percent}% free")

    def display_network_metrics(self):
        net_io = psutil.net_io_counters()
        sent_mb = net_io.bytes_sent / (1024 ** 2)
        recv_mb = net_io.bytes_recv / (1024 ** 2)
        self.stdscr.addstr(9, 0, "Network Usage:", curses.A_BOLD)
        self.stdscr.addstr(10, 0, f"Sent: {sent_mb:.2f} MB, Received: {recv_mb:.2f} MB")

    def display_temperature(self):
        temp_output = self.get_temperature()
        self.stdscr.addstr(12, 0, "Temperatures:", curses.A_BOLD)
        self.stdscr.addstr(13, 0, f"{temp_output}")

    def display_power_consumption(self):
        power_consumption = self.get_power_consumption()
        self.stdscr.addstr(15, 0, "Power Consumption:", curses.A_BOLD)
        self.stdscr.addstr(16, 0, f"{power_consumption}")


def main(stdscr):
    monitor = SystemMonitor(stdscr)
    monitor.display_metrics()


if __name__ == "__main__":
    curses.wrapper(main)
