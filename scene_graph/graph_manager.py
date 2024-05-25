from typing import Dict, Any, List, Tuple
import networkx as nx
import plotly.graph_objects as go

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
        return nx.spring_layout(self.graph, k=1)

    def create_edge_trace(self, position: Dict[int, Tuple[float, float]]) -> go.Scatter:
        """
        Creates a Plotly scatter trace for the edges in the graph.

        ### Args:
            - position (Dict[int, Tuple[float, float]]): The positions of the nodes.

        ### Returns:
            - go.Scatter: The edge trace for the graph visualization.
        """
        edge_x = []
        edge_y = []

        for edge in self.graph.edges():
            x0, y0 = position[edge[0]]
            x1, y1 = position[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        return go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.3, color='#FFFFFF'), hoverinfo='none', mode='lines')

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

        for node in self.graph.nodes():
            x, y = position[node]
            node_x.append(x)
            node_y.append(y)
            text.append(f"ID: {node}<br>{self.graph.nodes[node]}")

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color='blue',
                size=20,
                line_width=2
            ),
            text=text,
            textposition="middle center",
            textfont=dict(
                family="Helvetica",
                size=12,
                color='white'
            )
        )
        node_trace.text = text
        return node_trace
