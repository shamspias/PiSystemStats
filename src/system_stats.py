import time
import subprocess
import psutil
import curses


def get_temperature():
    result = subprocess.run(['sensors'], capture_output=True, text=True)
    return result.stdout


def get_power_consumption():
    try:
        with open("/sys/class/power_supply/battery/power_now", "r") as file:
            power = int(file.read().strip()) / 1_000_000  # Convert microWatts to Watts
        return f"{power} W"
    except FileNotFoundError:
        return "Power data not available"


def draw_screen(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)  # Make getch non-blocking
    while True:
        stdscr.clear()  # Clear the screen
        cpu_usage = psutil.cpu_percent()
        temp_output = get_temperature()
        power_consumption = get_power_consumption()

        # Display Headers
        stdscr.addstr(0, 0, "CPU Usage:", curses.A_BOLD)
        stdscr.addstr(1, 0, f"{cpu_usage}%\n")
        stdscr.addstr(3, 0, "Temperatures:", curses.A_BOLD)
        stdscr.addstr(4, 0, f"{temp_output}")
        stdscr.addstr(15, 0, "Power Consumption:", curses.A_BOLD)
        stdscr.addstr(16, 0, f"{power_consumption}\n")

        stdscr.refresh()  # Refresh the screen
        time.sleep(1)  # Update every 1 second
        if stdscr.getch() == ord('q'):  # Press 'q' to quit
            break


def main():
    curses.wrapper(draw_screen)


if __name__ == "__main__":
    main()
