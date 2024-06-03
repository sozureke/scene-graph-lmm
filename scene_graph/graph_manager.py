import networkx as nx
from typing import Dict, Any, List, Tuple
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

class GraphManager:
    """
    A class to manage a graph representation and visualization using NetworkX and Plotly.

    ### Attributes:
        - graph (nx.Graph): The graph object representing the scene.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initializes the GraphManager with data and builds the graph.

        ### Args:
            - data (Dict[str, Any]): The data used to construct the graph, typically loaded from a JSON file.

        ### Raises:
            - KeyError: If required data is missing from the input.
        """
        self.graph = nx.Graph()
        self.build_graph(data)

    def build_graph(self, data: Dict[str, Any]) -> None:
        """
        Builds the graph from the provided data.

        ### Args:
            - data (Dict[str, Any]): The data used to construct the graph, containing objects and their relations.

        ### Process:
            - Iterates over objects in the data.
            - Adds each object as a node.
            - Adds each relation as an edge.
        """
        for obj in data['objects']:
            self.add_object(obj)
            for relation in obj.get('relations', []):
                self.add_relation(obj["id"], relation=relation)

    def add_object(self, obj: Dict[str, Any]) -> None:
        """
        Adds an object to the graph as a node with its attributes.

        ### Args:
            - obj (Dict[str, Any]): The object data, including its attributes and ID.

        ### Raises:
            - KeyError: If the object ID or name is missing.
        """
        node_attributes = obj.get('attributes', {})
        node_attributes.update({'name': obj['name']})
        self.graph.add_node(obj['id'], **node_attributes)

    def add_relation(self, source_id: int, relation: Dict[str, Any]) -> None:
        """
        Adds a relation to the graph as an edge.

        ### Args:
            - source_id (int): The ID of the source object.
            - relation (Dict[str, Any]): The relation data, including target object ID and relation type.

        ### Raises:
            - KeyError: If the relation data is incomplete.
        """
        self.graph.add_edge(source_id, relation["object_id"], relation_type=relation["relation_type"], description=relation["relation_description"])

    def find_objects_by_attribute(self, attribute: str, value: Any) -> List[int]:
        """
        Finds objects in the graph based on a specific attribute and its value.

        ### Args:
            - attribute (str): The attribute name to search for.
            - value (Any): The value of the attribute to match.

        ### Returns:
            - List[int]: A list of object IDs that match the attribute and value.
        """
        return [node for node, attributes in self.graph.nodes(data=True) if attributes.get(attribute) == value]

    def calculate_positions(self) -> Dict[int, Tuple[float, float]]:
        """
        Calculates positions for the nodes in the graph using a spring layout.

        ### Returns:
            - Dict[int, Tuple[float, float]]: A dictionary mapping node IDs to their positions.
        """
        raw_positions = nx.spring_layout(self.graph, k=1)
        positions = {int(node): (float(pos[0]), float(pos[1])) for node, pos in raw_positions.items()}
        
        return positions

    def create_edge_trace(self, position: Dict[int, Tuple[float, float]]) -> List[go.Scatter]:
        """
        Creates a Plotly scatter trace for the edges in the graph.

        ### Args:
            - position (Dict[int, Tuple[float, float]]): The positions of the nodes.

        ### Returns:
            - List[go.Scatter]: A list of edge traces for the graph visualization.
        """
        edge_traces = []
        label_offset = 0.04
        
        for edge in self.graph.edges(data=True):
            x0, y0 = position[edge[0]]
            x1, y1 = position[edge[1]]
            text = edge[2]['relation_type']

    
            edge_trace = go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                line=dict(width=2, color='#FF6347'),
                hoverinfo='none',
                mode='lines'
            )
            edge_traces.append(edge_trace)

            mid_x = (x0 + x1) / 2
            mid_y = (y0 + y1) / 2
            label_trace = go.Scatter(
                x=[mid_x], y=[mid_y + label_offset],
                text=[text],
                mode='text',
                hoverinfo='text',
                textposition='middle center',
                textfont=dict(
                    family="Helvetica",
                    size=12,
                    color='black'
                )
            )
            edge_traces.append(label_trace)

        return edge_traces

    def create_node_trace(self, position: Dict[int, Tuple[float, float]]) -> go.Scatter:
        """
        Creates a Plotly scatter trace for the nodes in the graph.

        ### Args:
            - position (Dict[int, Tuple[float, float]]): The positions of the nodes.

        ### Returns:
            - go.Scatter: The node trace for the graph visualization.
        """
        node_x = []
        node_y = []
        text = []
        node_colors = []

        for node, data in self.graph.nodes(data=True):
            x, y = position[node]
            node_x.append(x)
            node_y.append(y)
            hover_text = f"object: {data['name']}<br>" + "<br>".join([f"{key}: {value}" for key, value in data.items() if key != 'name'])
            text.append(data['name'])
            node_colors.append('skyblue')

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color=node_colors,
                size=22,
                line_width=2
            ),
            text=text,
            hovertext=hover_text,
            textposition="top center",
            textfont=dict(
                family="Helvetica",
                size=12,
                color='black'
            )
        )
        return node_trace

    def draw_graph_on_image(self, image_path: str, json_data: Dict[str, Any]) -> None:
        """
        Draws the graph on the provided image.

        ### Args:
            - image_path (str): The path to the image file.
            - json_data (Dict[str, Any]): The JSON data containing the graph information.
        """
        image = Image.open(image_path)
        width, height = image.size

        fig, ax = plt.subplots(figsize=(width / 100, height / 100))
        ax.imshow(image)

        for obj in json_data['objects']:
            bbox = obj['bounding_box']
            rect = patches.Rectangle(
                (bbox['x_min'] * width, bbox['y_min'] * height),
                (bbox['x_max'] - bbox['x_min']) * width,
                (bbox['y_max'] - bbox['y_min']) * height,
                linewidth=2, edgecolor='red', facecolor='none'
            )
            ax.add_patch(rect)
            ax.text(
                (bbox['x_min'] + bbox['x_max']) / 2 * width,
                bbox['y_min'] * height - 10,
                obj['name'],
                color='red', fontsize=12, ha='center'
            )

        # Building the graph
        for obj in json_data['objects']:
            self.graph.add_node(obj['id'], name=obj['name'])
            for rel in obj['relations']:
                self.graph.add_edge(obj['id'], rel['object_id'], label=rel['relation_type'])

        # Calculate positions for the nodes
        positions = self.calculate_positions()

        # Scaling positions to image size
        positions = {node: (pos[0] * width, pos[1] * height) for node, pos in positions.items()}

        # Drawing edges
        for edge in self.graph.edges(data=True):
            x0, y0 = positions[edge[0]]
            x1, y1 = positions[edge[1]]
            ax.plot([x0, x1], [y0, y1], 'k-', lw=2)

        # Drawing nodes and labels
        for node, (x, y) in positions.items():
            ax.plot(x, y, 'ro')
            ax.text(
                x, y, self.graph.nodes[node]['name'],
                fontsize=12, ha='center', va='center', color='black',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2')
            )

        plt.axis('off')
        plt.show()

