import os
import sys
from pathlib import Path
from config import generative_model, QUERY
from scene_graph.graph import SceneGraph
from scene_graph.utils import Utils

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'scene_graph')))

IMAGE = Path("data/images/001.jpg")

def main() -> None:
	Utils.setup_logging()
	model_output = generative_model.generate_response(image_path=IMAGE, prompt_path=QUERY)
	file_path = Utils.save_result(model_output)

	graph = SceneGraph(file_path)
	graph.interactive_visualize()


if __name__ == "__main__":
	main()
	
