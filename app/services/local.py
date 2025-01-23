import re
from datetime import datetime

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
