import os
import glob
import datetime
from typing import Iterable
from server import ASSETS_DIR, CHUNK_SIZE

class FileServices:

    def listFiles(self):
        collection = []
        for filename in os.listdir(ASSETS_DIR):
            file_info = {}
            file_path = os.path.join(ASSETS_DIR, filename)

            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                time = os.path.getmtime(file_path)
                timestamp = datetime.datetime.fromtimestamp(time)
                formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")

                file_info["name"] = filename
                file_info["size"] = size
                file_info["timestamp"] = formatted_date
                collection.append(file_info)
        return collection

    def findFiles(self, search: str) -> list:
        try:
            validate_path_traversal(search)
            collection = []
            for filename in glob.glob(f"{ASSETS_DIR}/{search}"):
                file_info = {}

                size = os.path.getsize(filename)
                time = os.path.getmtime(filename)
                timestamp = datetime.datetime.fromtimestamp(time)
                formatted_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")

                file_info["name"] = os.path.basename(filename)
                file_info["size"] = size
                file_info["timestamp"] = formatted_date
                collection.append(file_info)
            return collection, None
        except (PermissionError, Exception) as e:
            return [], e

    def putFile(self, name: str, chunks: Iterable[bytes]) -> tuple:
        try:
            with open(os.path.join(ASSETS_DIR, name), 'wb') as f:
                for chunk in chunks:
                    f.write(chunk)
            return "File uploaded successfully", None
        except FileNotFoundError as e:
            return "File not found", e
        except PermissionError as e:
            return "Permission denied", e
        except IOError as e:
            return f"IO Error: {str(e)}", e
        except Exception as e:
            return f"Unexpected error: {str(e)}", e

    def getFile(self, name: str) -> tuple:
        try:
            validate_path_traversal(name)
            with open(os.path.join(ASSETS_DIR, name), 'rb') as f:
                while (chunk := f.read(int(CHUNK_SIZE))):
                    yield name, chunk, None
        except (PermissionError, FileNotFoundError, Exception) as e:
            yield '', b'', e

def validate_path_traversal(name: str):
    abs_path = os.path.abspath(os.path.join(ASSETS_DIR, name))
    authorized_path = os.path.abspath(ASSETS_DIR)
    if not abs_path.startswith(authorized_path):
        raise PermissionError

Service = FileServices()
