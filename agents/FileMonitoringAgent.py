
import time
from agents.TranscriptionAgent import process_video as transcribe
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return None
        else:
            filepath = event.src_path
            pool = ThreadPoolExecutor(max_workers=4)
            if filepath.endswith(".mp4") or filepath.endswith(".mov"):
                print(f"New video file added: {filepath}")
                pool.submit(transcribe, filepath)

def monitor_folder(folder_path):
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

