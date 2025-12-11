import psutil


def is_process_running(process_name):
    for process in psutil.process_iter():
        try:
            if process_name.lower() == process.name().lower():
                return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
