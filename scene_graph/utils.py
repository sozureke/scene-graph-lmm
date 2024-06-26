import logging.config
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional

import os
import json
import logging
import hashlib

class Utils:
    @staticmethod
    def read_file_content(file_path: str) -> str | None:
        """
        Reads and returns the content of a file.

        ### Args:
            - file_path (str): The path to the file to read.

        ### Returns:
            - str | None: The content of the file as a string, or None if an error occurs.

        ### Raises:
            - IOError: If an error occurs while reading the file.
        """
        try:
            with open(file_path, "r") as file:
                return file.read().strip()
        except IOError as error:
            logging.error(f"[*] Error reading file {file_path}: {error}")
            return None

    @staticmethod
    def save_result(model_output: str) -> str:
        """
        Saves the given model output to a file and returns the file path.

        The file is saved in the 'data/results' directory with a timestamped filename.

        ### Args:
            - model_output (str): The content to save to the file.

        ### Returns:
            - str: The path to the saved file.

        ### Raises:
            - IOError: If an error occurs while writing to the file.
            - Exception: If any other error occurs.
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
            logging.info(f"[!] Data successfully written to {file_path}")
            return file_path  
        except IOError as error:
            logging.error(f"[*] Error writing to file {file_path}: {error}")
            raise  
        except Exception as error:
            logging.error(f"[*] An error occurred: {error}")
            raise  

    @staticmethod
    def load_json(JSON_FILE: str) -> Dict[str, Any]:
        """
        Loads and returns the content of a JSON file.

        ### Args:
            - JSON_FILE (str): The path to the JSON file to read.

        ### Returns:
            - Dict[str, Any]: The content of the JSON file as a dictionary.

        ### Raises:
            - IOError: If an error occurs while reading the file.
            - JSONDecodeError: If the file content is not valid JSON.
        """
        try:
            with open(JSON_FILE, 'r') as json_file:
                return json.load(json_file)
        except IOError as error:
            logging.error(f"[*] Error reading JSON file {JSON_FILE}: {error}")
            raise
        except json.JSONDecodeError as error:
            logging.error(f"[*] Error decoding JSON file {JSON_FILE}: {error}")
            raise
    @staticmethod
    def generate_hash_key(text_prompt: str | None, image_paths: List[str]) -> str:
        """
        Generates a unique cache key based on the text prompt and image paths.

        ### Args:
            - text_prompt (str): The text prompt for the model.
            - image_paths (List[str]): A list of file paths to the images.

        ### Returns:
            - str: A unique cache key.
        """
        hasher = hashlib.md5()
        if text_prompt is not None:
            hasher.update(text_prompt.encode("utf-8"))
        for image_path in image_paths:
            with open(image_path, "rb") as file:
                hasher.update(file.read())
        return hasher.hexdigest()
    
    @staticmethod
    def save_cache_entry(key: str, value: str, cache_dir: str) -> None:
        """
        Saves a single cache entry to a file.

        ### Args:
            - key (str): The cache key.
            - value (str): The cache value.
            - cache_dir (str): The directory to save the cache files.

        ### Raises:
            - IOError: If an error occurs while writing to the file.
        """
        try:
            os.makedirs(cache_dir, exist_ok=True)
            with open(os.path.join(cache_dir, key + '.json'), 'w') as file:
                json.dump({key: value}, file)
            logging.info(f"[!] Cache entry successfully saved for key {key}")
        except IOError as error:
            logging.error(f"[*] Error writing cache entry for key {key}: {error}")
            raise

    @staticmethod
    def load_cache_entry(key: str, cache_dir: str) -> Dict[str, str]:
        """
        Loads a single cache entry from a file.

        ### Args:
            - key (str): The cache key.
            - cache_dir (str): The directory to load the cache files from.

        ### Returns:
            - Dict[str, str]: The loaded cache entry.

        ### Raises:
            - IOError: If an error occurs while reading the file.
            - JSONDecodeError: If the file content is not valid JSON.
        """
        try:
            cache_file_path = os.path.join(cache_dir, key + '.json')
            if os.path.exists(cache_file_path):
                with open(cache_file_path, 'r') as file:
                    return json.load(file)
            else:
                return {}
        except IOError as error:
            logging.error(f"Error reading cache entry for key {key}: {error}")
            raise
        except json.JSONDecodeError as error:
            logging.error(f"Error decoding cache entry for key {key}: {error}")
            raise

    @staticmethod
    def save_logging_config(logging_config: Dict[str, Any], config_file: str) -> None:
        """
        Saves the logging configuration to a file.

        ### Args:
            - logging_config (Dict[str, Any]): The logging configuration to save.
            - config_file (str): The path to the configuration file.

        ### Raises:
            - IOError: If an error occurs while writing to the file.
        """
        try:
            with open(config_file, 'w') as file:
                json.dump(logging_config, file)
            logging.info(f"[!] Logging configuration successfully saved to {config_file}")
        except IOError as error:
            logging.error(f"[*] Error writing to logging configuration file {config_file}: {error}")
            raise

    @staticmethod
    def load_logging_config(config_file: str) -> Optional[Dict[str, Any]]:
        """
        Loads the logging configuration from a file.

        ### Args:
            - config_file (str): The path to the configuration file.

        ### Returns:
            - Dict[str, Any] | None: The loaded logging configuration, or None if the file does not exist or is invalid.

        ### Raises:
            - IOError: If an error occurs while reading the file.
            - JSONDecodeError: If the file content is not valid JSON.
        """
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as file:
                    return json.load(file)
            else:
                return None
        except IOError as error:
            logging.error(f"[*] Error reading logging configuration file {config_file}: {error}")
            raise
        except json.JSONDecodeError as error:
            logging.error(f"[*] Error decoding logging configuration file {config_file}: {error}")
            raise

    @staticmethod
    def setup_logging(logging_config_file: str = "") -> None:
        """
        Sets up logging configuration.

        Logs are written to 'data/application.log' and also output to the console.

        ### Args:
            - logging_config_file (str | None): Optional path to a logging configuration file.

        ### Raises:
            - Exception: If any error occurs during the logging setup.
        """
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(Path("data/application.log"))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        if logging_config_file:
            logging_config = Utils.load_logging_config(logging_config_file)
            if logging_config:
                logging.config.dictConfig(logging_config)
                logging.info(f"[!] Logging configuration loaded from {logging_config_file}")


    @staticmethod
    def get_last_saved_result() -> str:
        """
        Returns the path to the last saved result file in the 'data/results' directory.

        ### Returns:
            - str: The path to the last saved result file.

        ### Raises:
            - FileNotFoundError: If no result files are found.
        """
        directory = 'data/results'
        if not os.path.exists(directory):
            raise FileNotFoundError(f"No results directory found at {directory}")
        
        files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]
        if not files:
            raise FileNotFoundError("No result files found")
        
        latest_file = max(files, key=os.path.getctime)
        return latest_file
