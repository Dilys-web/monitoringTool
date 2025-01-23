import platform
import re
from datetime import datetime
from typing import List

def retrieve_logs(file_path: str) -> dict:
    log_entries = []
    log_pattern = re.compile(
        r'(?P<timestamp>\S+\s+\d+\s+\d+:\d+:\d+)\s+(?P<source>\S+)\s+(?P<message>.+)'
    )

    try:
        with open(file_path, "r") as file:
            for line in file:
                match = log_pattern.match(line)
                if match:
                    log_entry = {
                        "timestamp": match.group("timestamp"),
                        "source": "local",
                        "message": match.group("message"),
                    }
                    log_entries.append(log_entry)
                else:
                    log_entries.append({
                        "timestamp": None,
                        "source": None,
                        "message": line.strip(),
                    })

        return {"logs": log_entries}
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise IOError(f"An error occurred: {str(e)}")


def fetch_logs_from_windows(log_types: List[str]) -> List[dict]:
    """
    Fetch logs from Windows Event Viewer.
    """
    try:
        all_logs = []
        server = 'localhost'  # Can be customized for remote logs

        for log_type in log_types:
            print(f"Fetching logs from: {log_type} on Windows")

            # Open each event log
            handler = win32evtlog.OpenEventLog(server, log_type)

            # Define flags for reading logs
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

            # Read logs from the current log type
            while True:
                events = win32evtlog.ReadEventLog(handler, flags, 0)
                if not events:
                    break
                
                # Process each event and extract details
                for event in events:
                    source = event.SourceName
                    strings = event.StringInserts if event.StringInserts else []
                    event_id = event.EventID
                    time_generated = event.TimeGenerated.Format()  # Format as human-readable time

                    # Add formatted log to the list
                    log_entry = {
                        "log_type": log_type,
                        "source": source,
                        "event_id": event_id,
                        "time_generated": time_generated,
                        "details": strings,
                    }
                    all_logs.append(log_entry)

        return all_logs

    except Exception as e:
        return [f"Error fetching Windows logs: {str(e)}"]
    

def fetch_logs_from_linux(log_types: List[str]) -> List[dict]:
    """
    Fetch logs from Linux system log files.
    """
    try:
        all_logs = []
        log_files = ["/var/log/syslog", "/var/log/dmesg", "/var/log/auth.log"]

        for log_file in log_files:
            if log_file.split("/")[-1] in log_types:  # Only process logs that are specified
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                    
                    # Process each line as a log entry (example format)
                    for line in lines:
                        log_entry = {
                            "log_type": log_file,
                            "message": line.strip(),  # Strip whitespace/newlines
                        }
                        all_logs.append(log_entry)
                except FileNotFoundError:
                    print(f"Log file {log_file} not found, skipping.")
                except Exception as e:
                    print(f"Error reading {log_file}: {str(e)}")

        return all_logs

    except Exception as e:
        return [f"Error fetching Linux logs: {str(e)}"]
    

async def fetch_platform_logs(log_types: List[str]) -> List[dict]:
    """
    Fetch logs from the system based on the platform (Windows or Linux).
    """
    if platform.system() == "Windows":
        return fetch_logs_from_windows(log_types)
    elif platform.system() == "Linux":
        return fetch_logs_from_linux(log_types)
    else:
        return [{"error": "Unsupported platform"}]