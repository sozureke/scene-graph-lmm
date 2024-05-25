from typing import Dict, Any, List, Tuple
import networkx as nx
import plotly.graph_objects as go

class GraphManager:
	def __init__(self, data: Dict[str, Any]):
		self.graph = nx.Graph()
		self.build_graph(data)

	def build_graph(self, data: Dict[str, Any]) -> None:
		for obj in data['objects']:
			self.add_object(obj)
			for relation in obj.get('relations', []):
				self.add_relation(obj["id"], relation=relation)

	def add_object(self, obj: Dict[str, Any]) -> None:
		node_attributes = obj.get('attributes', {})
		node_attributes.update({'name': obj['name']})
		self.graph.add_node(obj['id'], **node_attributes)


	def add_relation(self, source_id: int, relation: Dict[str, Any]) -> None:
		self.graph.add_edge(source_id, relation["object_id"], relation_type=relation["relation_type"], description=relation["relation_description"])

	def find_objects_by_attribute(self, attribute: str, value: Any) -> List[int]:
		return [node for node, attributes in self.graph.nodes(data=True) if attributes.get(attribute) == value]
	

	def calculate_positions(self) -> Dict[int, Tuple[float, float]]:
		return nx.spring_layout(self.graph, k=1)
	
	def create_edge_trace(self, position: Dict[int, Tuple[float, float]]) -> go.Scatter:
		edge_x = []
		edge_y  = []

		for edge in self.graph.edges():
			x0, y0 = position[edge[0]]
			x1, y1 = position[edge[1]]
			edge_x.extend([x0, x1, None])
			edge_y.extend([y0, y1, None])

		return go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.3, color='#FFFFFF'), hoverinfo='none', mode='lines')
		
	def create_node_trace(self, position: Dict[int, Tuple[float, float]]) -> go.Scatter:
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
	


