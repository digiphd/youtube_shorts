import argparse
from agents.FileMonitoringAgent import monitor_folder

def run(path):
    monitor_folder(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor a folder for new video files.")
    parser.add_argument("folder_path", type=str, help="Path to the folder to monitor.")
    args = parser.parse_args()

    folder_path = args.folder_path
    monitor_folder(folder_path)