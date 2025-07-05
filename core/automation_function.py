import os
import webbrowser
import psutil
import subprocess
import time
from pathlib import Path

def open_chrome():
    webbrowser.open("https://www.google.com")
    return "Chrome opened"

def open_calculator():
    os.system("calc" if os.name == "nt" else "gnome-calculator")
    return "Calculator opened"

def open_notepad():
    os.system("notepad" if os.name == "nt" else "gedit")
    return "Notepad opened"

def get_cpu_usage():
    return f"CPU: {psutil.cpu_percent(interval=1)}%"

def get_ram_usage():
    return f"RAM: {psutil.virtual_memory().percent}%"

def get_system_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    return f"Uptime: {hours}h {minutes}m"

def run_shell_command(command: str):
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=30)
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Command timed out"

# New features
def get_system_info():
    cpu_count = psutil.cpu_count()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu_cores": cpu_count,
        "total_ram": f"{memory.total // (1024**3)}GB",
        "available_ram": f"{memory.available // (1024**3)}GB",
        "disk_usage": f"{disk.percent}%"
    }

def kill_process(process_name: str):
    killed = []
    for proc in psutil.process_iter(['pid', 'name']):
        if process_name.lower() in proc.info['name'].lower():
            try:
                proc.kill()
                killed.append(proc.info['name'])
            except:
                pass
    return f"Killed: {', '.join(killed)}" if killed else "No matching processes found"

def list_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            if proc.info['cpu_percent'] > 0:
                processes.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
        except:
            pass
    return processes[:10]  # Top 10 active processes

def open_file_explorer():
    if os.name == "nt":
        os.system("explorer")
    else:
        os.system("nautilus" if os.system("which nautilus") == 0 else "thunar")
    return "File explorer opened"

def create_file(filename: str, content: str = ""):
    try:
        Path(filename).write_text(content)
        return f"File '{filename}' created"
    except Exception as e:
        return f"Error creating file: {str(e)}"

def shutdown_system():
    if os.name == "nt":
        os.system("shutdown /s /t 1")
    else:
        os.system("sudo shutdown -h now")
    return "System shutting down"

def restart_system():
    if os.name == "nt":
        os.system("shutdown /r /t 1")
    else:
        os.system("sudo reboot")
    return "System restarting"