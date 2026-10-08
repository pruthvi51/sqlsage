"""
NetworkX Relational Schema Graph and Steiner Tree Subgraph Extractor.
"""

import networkx as nx


class SchemaGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_table(self, table_name: str, columns: list[str]):
        self.graph.add_node(table_name, type="table", columns=columns)
        for col in columns:
            node_id = f"{table_name}.{col}"
            self.graph.add_node(node_id, type="column", table=table_name)
            self.graph.add_edge(table_name, node_id, weight=1.0)

    def add_foreign_key(self, from_table: str, to_table: str, join_condition: str):
        self.graph.add_edge(from_table, to_table, weight=2.0, join_condition=join_condition)

    def extract_connecting_subgraph(self, target_tables: list[str]) -> list[str]:
        """
        Extracts minimum Steiner-tree connecting path between target tables.
        """
        if len(target_tables) <= 1:
            return target_tables

        table_subgraph = nx.Graph()
        for u, v, data in self.graph.edges(data=True):
            if self.graph.nodes[u].get("type") == "table" and self.graph.nodes[v].get("type") == "table":
                table_subgraph.add_edge(u, v, weight=data.get("weight", 1.0))

        connecting_nodes = set(target_tables)
        for i in range(len(target_tables)):
            for j in range(i + 1, len(target_tables)):
                try:
                    path = nx.shortest_path(table_subgraph, target_tables[i], target_tables[j], weight="weight")
                    connecting_nodes.update(path)
                except nx.NetworkXNoPath:
                    pass
        return sorted(list(connecting_nodes))
