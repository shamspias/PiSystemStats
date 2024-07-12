import os
import time
import subprocess
import psutil


def get_cpu_usage():
    """Return the CPU usage percentage."""
    return psutil.cpu_percent(interval=1)


def get_temperature():
    """Retrieve the system temperature using 'sensors' command."""
    try:
        result = subprocess.run(['sensors'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Failed to get temperature: {str(e)}"


def get_power_consumption():
    """Retrieve the system power consumption from '/sys/class/power_supply/'."""
    power_path = "/sys/class/power_supply/battery/power_now"
    try:
        with open(power_path, "r") as file:
            power = int(file.read().strip()) / 1_000_000  # Convert microWatts to Watts
        return f"{power} W"
    except FileNotFoundError:
        return "Power data not available"
    except Exception as e:
        return f"Failed to read power data: {str(e)}"


def get_gpu_usage():
    """Mock function to get GPU usage. Replace with actual method depending on your GPU."""
    return "GPU usage functionality needs to be implemented based on specific hardware."


def get_npu_usage():
    """Mock function to get NPU usage. Replace with actual method depending on your NPU."""
    return "NPU usage functionality needs to be implemented based on specific hardware."


def display_data():
    """Function to display all collected system data."""
    while True:
        cpu_usage = get_cpu_usage()
        temp_output = get_temperature()
        power_consumption = get_power_consumption()
        gpu_usage = get_gpu_usage()
        npu_usage = get_npu_usage()

        print(f"CPU Usage: {cpu_usage}%")
        print(f"Temperature:\n{temp_output}")
        print(f"Power Consumption: {power_consumption}")
        print(f"GPU Usage: {gpu_usage}")
        print(f"NPU Usage: {npu_usage}")
        print("-" * 20)
        time.sleep(1)


if __name__ == "__main__":
    display_data()
