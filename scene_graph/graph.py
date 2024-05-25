import plotly.graph_objects as go
from .utils import Utils
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
        data = Utils.load_json(json_file)
        self.graph_manager = GraphManager(data)

    def interactive_visualize(self) -> None:
        """
        Creates an interactive visualization of the scene graph.

        ### Process:
            - Calculates node positions.
            - Creates traces for edges and nodes.
            - Displays the graph using Plotly.
        """
        position = self.graph_manager.calculate_positions()
        edge_trace = self.graph_manager.create_edge_trace(position)
        node_trace = self.graph_manager.create_node_trace(position)
        self.show_figure(edge_trace, node_trace)
    
    def show_figure(self, edge_trace: go.Scatter, node_trace: go.Scatter) -> None:
        """
        Displays the figure with edge and node traces using Plotly.

        ### Args:
            - edge_trace (go.Scatter): The edge trace created from graph data.
            - node_trace (go.Scatter): The node trace created from graph data.

        ### Visual Properties:
            - Disables legend.
            - Enables closest hover mode.
            - Removes grid lines, zero lines, and tick labels from both axes.
            - Sets the background color to black.

        ### Logs:
            - Logs an info message indicating that the scene graph is being displayed.
        """
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=0, l=0, r=0, t=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='black'
            )
        )
        logging.info("[!] Displaying the Scene Graph...")
        fig.show()
