import plotly.graph_objects as go
from .utils import Utils
from .graph_manager import GraphManager

import logging

class SceneGraph:
	def __init__(self, json_file: str) -> None:
		data = Utils.load_json(json_file)
		self.graph_manager = GraphManager(data)

	def interactive_visualize(self) -> None:
		position = self.graph_manager.calculate_positions()
		edge_trace = self.graph_manager.create_edge_trace(position)
		node_trace = self.graph_manager.create_node_trace(position)
		self.show_figure(edge_trace, node_trace)
	
	def show_figure(self, edge_trace: go.Scatter, node_trace: go.Scatter) -> None:
		fig = go.Figure(data=[edge_trace, node_trace],
										layout=go.Layout(showlegend=False, hovermode='closest',
																			margin=dict(b=0, l=0, r=0, t=0),
																			xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
																			yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), plot_bgcolor='black'))
		logging.info("[!] Displaying the Scene Graph...")
		fig.show()
