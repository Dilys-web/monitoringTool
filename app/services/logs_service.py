# app/db/crud.py
from platform import platform
from typing import List
from sqlalchemy.orm import Session
from app.models.logs import Log
from app.schemas.log_schema import LogCreate
import subprocess
import win32evtlog


# Create log
def create_log(db: Session, log: LogCreate):
    db_log = Log(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# Get logs
def get_logs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Log).offset(skip).limit(limit).all()

def get_log():
    return {"logger":"Info"}

def fetch_linux_logs():
    try:
        # Example: Tail the syslog
        logs = subprocess.check_output(["tail", "-n", "10", "/var/log/syslog"]).decode("utf-8")
        return logs.split("\n")
    except Exception as e:
        return [f"Error fetching Linux logs: {str(e)}"]


def fetch_windows_logs():
    try:
        # Example: Fetch Windows logs (requires `win32evtlog` or similar library)
         # pip install pywin32
        server = 'localhost'
        log_type = 'Application'
        handler = win32evtlog.OpenEventLog(server, log_type)
        print(handler)
        print("handler")
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(handler, flags, 0)
        logs = [f"{event.SourceName}: {event.StringInserts}" for event in events if event.StringInserts]
        # print(logs)
        print("logsss")
        return logs[:10]  # Return the last 10 logs
    except Exception as e:
        return [f"Error fetching Windows logs: {str(e)}"]
    
    
async def fetch_all_logs(log_types:List[str]):
        try:
            # Specify the target machine (local or remote)
            server = 'localhost'  # Use the machine name or IP address for remote logs
            
            # Get a list of all available event log types on the server
            # log_types = ["Application","System"]

            all_logs = []

            for log_type in log_types:
                print(f"Fetching logs from: {log_type}")
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
            
            # Return all logs
            return all_logs

        except Exception as e:
            return [f"Error fetching Windows logs: {str(e)}"]
        
        
async def fetch_all_logs(log_types: List[str]):
    try:
        # Initialize an empty list to store logs
        all_logs = []

        # Check if the platform is Windows
        if platform.system() == "Windows":
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

        # Check if the platform is Linux
        elif platform.system() == "Linux":
            print("Fetching logs from: Linux")

            # For Linux, you can scan /var/log for logs like syslog, dmesg, etc.
            # Example logs you may want to access on Linux
            log_files = ["/var/log/syslog", "/var/log/dmesg", "/var/log/auth.log"]

            for log_file in log_files:
                if log_file in log_types:  # Only process logs that are specified
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
        
        # Return all collected logs
        return all_logs

    except Exception as e:
        return [f"Error fetching logs: {str(e)}"]


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
    

async def fetch_all_logs(log_types: List[str]) -> List[dict]:
    """
    Fetch logs from the system based on the platform (Windows or Linux).
    """
    if platform.system() == "Windows":
        return fetch_logs_from_windows(log_types)
    elif platform.system() == "Linux":
        return fetch_logs_from_linux(log_types)
    else:
        return [{"error": "Unsupported platform"}]