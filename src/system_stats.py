import time
import subprocess
import psutil
import curses
import csv
from datetime import datetime


class SystemMonitor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_curses()
        self.recording = False
        self.log_file = None

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

    def start_recording(self):
        if not self.recording:
            self.log_file = open('system_metrics_log.csv', 'w', newline='')
            self.writer = csv.writer(self.log_file)
            headers = ['Timestamp', 'CPU Usage', 'RAM Usage', 'Disk Usage', 'Network Sent', 'Network Received',
                       'Temperature', 'Power Consumption']
            self.writer.writerow(headers)
            self.recording = True

    def stop_recording(self):
        if self.recording:
            self.log_file.close()
            self.recording = False

    def log_data(self, data):
        if self.recording:
            self.writer.writerow(data)

    def display_metrics(self):
        while True:
            self.stdscr.clear()
            data = self.collect_data()
            self.display_data(data)
            self.log_data(data)
            self.stdscr.refresh()
            time.sleep(1)
            key = self.stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('R'):  # Shift + R to start recording
                self.start_recording()
            elif key == ord('S'):  # Shift + S to stop recording
                self.stop_recording()

    def collect_data(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        net_io = psutil.net_io_counters()
        sent_mb = net_io.bytes_sent / (1024 ** 2)
        recv_mb = net_io.bytes_recv / (1024 ** 2)
        temp_output = self.get_temperature()
        power_consumption = self.get_power_consumption()
        return [timestamp, cpu_usage, ram_usage, disk_usage, sent_mb, recv_mb, temp_output, power_consumption]

    def display_data(self, data):
        self.stdscr.addstr(0, 0, f"CPU Usage: {data[1]}%")
        self.stdscr.addstr(1, 0, f"RAM Usage: {data[2]}%")
        self.stdscr.addstr(2, 0, f"Disk Usage: {data[3]}%")
        self.stdscr.addstr(3, 0, f"Network Sent: {data[4]:.2f} MB, Received: {data[5]:.2f} MB")
        self.stdscr.addstr(4, 0, "Temperatures:")
        self.stdscr.addstr(5, 0, data[6])
        self.stdscr.addstr(6, 0, f"Power Consumption: {data[7]}")


def main(stdscr):
    monitor = SystemMonitor(stdscr)
    monitor.display_metrics()


if __name__ == "__main__":
    curses.wrapper(main)
