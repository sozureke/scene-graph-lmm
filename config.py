from scene_graph.model import GenerativeModel
from dotenv import load_dotenv
from pathlib import Path
from scene_graph.utils import Utils
import os

load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')
LOGGING_CONFIG_FILE: str = 'data/logging_config.json'
SYSTEM_MESSAGE = Utils.read_file_content('./source/system.txt')
QUERY_MESSAGE = "./source/query.txt"
IMAGE_LIST = ["data/images/001.png", "data/images/002.png"]


generative_model = GenerativeModel(API_KEY=API_KEY, MODEL_NAME="models/gemini-1.5-pro-latest", SYSTEM_MESSAGE=SYSTEM_MESSAGE)

