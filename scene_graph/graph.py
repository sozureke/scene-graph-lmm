import plotly.graph_objects as go
from .utils import Utils
from typing import List
from .graph_manager import GraphManager
import logging

class SceneGraph:
    """
    A class to represent and visualize a scene graph using Plotly.

    ### Attributes:
        - graph_manager (GraphManager): An instance of GraphManager to handle graph data and operations.
    """

    def __init__(self, json_file: str) -> None:
        """
        Initializes the SceneGraph with data from a JSON file.

        ### Args:
            - json_file (str): The path to the JSON file containing graph data.

        ### Raises:
            - IOError: If there is an error loading the JSON file.
            - JSONDecodeError: If the JSON file content is not valid.
        """
        self.data = Utils.load_json(json_file)
        self.graph_manager = GraphManager(self.data)

    def interactive_visualize(self) -> None:
        """
        Creates an interactive visualization of the scene graph.

        ### Process:
            - Calculates node positions.
            - Creates traces for edges and nodes.
            - Displays the graph using Plotly.
        """
        position = self.graph_manager.calculate_positions()
        edge_traces = self.graph_manager.create_edge_trace(position)
        node_trace = self.graph_manager.create_node_trace(position)
        self.show_figure(edge_traces, node_trace)
    
    def show_figure(self, edge_traces: List[go.Scatter], node_trace: go.Scatter) -> None:
        """
        Displays the figure with edge and node traces using Plotly.

        ### Args:
            - edge_traces (List[go.Scatter]): The edge traces created from graph data.
            - node_trace (go.Scatter): The node trace created from graph data.

        ### Visual Properties:
            - Disables legend.
            - Enables closest hover mode.
            - Removes grid lines, zero lines, and tick labels from both axes.
            - Sets the background color to white.

        ### Logs:
            - Logs an info message indicating that the scene graph is being displayed.
        """
        fig = go.Figure(
            data=edge_traces + [node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=0, l=0, r=0, t=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='white'
            )
        )
        logging.info("[!] Displaying the Scene Graph...")
        fig.show()

    def draw_graph_on_image(self, image_path: str) -> None:
        """
        Draws the graph on the provided image using the GraphManager.

        ### Args:
            - image_path (str): The path to the image file.
        """
        self.graph_manager.draw_graph_on_image(image_path, self.data)
