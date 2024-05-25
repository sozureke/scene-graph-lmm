sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'scene_graph')))

import os
import sys
from config import generative_model, QUERY_MESSAGE, IMAGE_LIST
from scene_graph.graph import SceneGraph
from scene_graph.utils import Utils


def main() -> None:
	Utils.setup_logging()
	model_output = generative_model.generate_response(image_paths=IMAGE_LIST, prompt_path=QUERY_MESSAGE)
	file_path = Utils.save_result(model_output)

	graph = SceneGraph(file_path)
	graph.interactive_visualize()


if __name__ == "__main__":
	main()
	
