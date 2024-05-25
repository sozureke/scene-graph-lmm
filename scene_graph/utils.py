from pathlib import Path
from datetime import datetime
from typing import Any, Dict

import os
import json
import logging

class Utils:
    @staticmethod
    def read_file_content(file_path: str) -> str | None:
        """
        Reads and returns the content of a file.

        Args:
            file_path (str): The path to the file to read.

        Returns:
            str | None: The content of the file as a string, or None if an error occurs.

        Raises:
            IOError: If an error occurs while reading the file.
        """
        try:
            with open(file_path, "r") as file:
                return file.read().strip()
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    def save_result(model_output: str) -> str:
        """
        Saves the given model output to a file and returns the file path.

        The file is saved in the 'data/results' directory with a timestamped filename.

        Args:
            model_output (str): The content to save to the file.

        Returns:
            str: The path to the saved file.

        Raises:
            IOError: If an error occurs while writing to the file.
            Exception: If any other error occurs.
        """
        directory = 'data/results'
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"output_{current_time}.json"
        file_path = os.path.join(directory, file_name)
        
        try:
            with open(file_path, 'w') as file:
                file.write(model_output)
            print(f"Data successfully written to {file_path}")
            return file_path  
        except IOError as e:
            print(f"Error writing to file {file_path}: {e}")
            raise  
        except Exception as e:
            print(f"An error occurred: {e}")
            raise  

    @staticmethod
    def load_json(JSON_FILE: str) -> Dict[str, Any]:
        with open(JSON_FILE, 'r') as json_file:
            return json.load(json_file)

    @staticmethod   
    def setup_logging() -> None:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(Path("data/application.log"))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

