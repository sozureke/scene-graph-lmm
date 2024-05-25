from scene_graph.model import GenerativeModel
from dotenv import load_dotenv
from pathlib import Path
from scene_graph.utils import Utils
import os

load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')
SYSTEM_MESSAGE = Utils.read_file_content('./source/system.txt')
QUERY = Path("./source/query.txt")

generative_model = GenerativeModel(API_KEY=API_KEY, MODEL_NAME="models/gemini-1.5-pro-latest", SYSTEM_MESSAGE=SYSTEM_MESSAGE)