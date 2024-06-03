import os
import sys
import logging
from config import generative_model, QUERY_MESSAGE, IMAGE_LIST, LOGGING_CONFIG_FILE
from scene_graph.graph import SceneGraph
from scene_graph.utils import Utils

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'scene_graph')))
Utils.setup_logging(logging_config_file=LOGGING_CONFIG_FILE)


def main() -> None:
    """
    Main function to generate the scene graph and visualize it interactively.
    """
    try:
        model_output = generative_model.generate_response(image_paths=IMAGE_LIST, prompt_path=QUERY_MESSAGE)
        file_path = Utils.get_last_saved_result()
        graph = SceneGraph(file_path)
        graph.interactive_visualize()
    except Exception as error:
        logging.error(f"[*] An error occurred in the main function: {error}")
        raise

if __name__ == "__main__":
    main()
