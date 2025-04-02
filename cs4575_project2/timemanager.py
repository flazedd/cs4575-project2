import json
import os
import time

class TimestampManager:
    def __init__(self, filename="timestamps.json"):
        self.filename = filename
        self.timestamps = self._load_timestamps()

    def _load_timestamps(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_timestamps(self):
        with open(self.filename, "w") as file:
            json.dump(self.timestamps, file, indent=4)

    def start(self, image, iteration):
        key = f"{image}{iteration}"
        current_time = int(time.time() * 1000)  # Milliseconds since Unix epoch
        if key not in self.timestamps:
            self.timestamps[key] = {"start": current_time, "stop": None}
            self._save_timestamps()
        else:
            print(f"Warning: {key} already has a start time.")

    def stop(self, image, iteration):
        key = f"{image}{iteration}"
        current_time = int(time.time() * 1000)
        if key in self.timestamps and self.timestamps[key]["stop"] is None:
            self.timestamps[key]["stop"] = current_time
            self._save_timestamps()
        else:
            print(f"Warning: {key} does not exist or already has a stop time.")

    def get_timestamps(self):
        return self.timestamps

# Example usage:
if __name__ == "__main__":
    tm = TimestampManager()
    tm.start("mlc", 0)
    time.sleep(2)  # Simulate some processing time
    tm.stop("mlc", 0)
    print(tm.get_timestamps())
