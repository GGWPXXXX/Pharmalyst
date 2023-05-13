    def recommendation(self, customer: Customer) -> str:
        medications = self.__order_repo.load_customer_order(customer)
        G = nx.Graph()

        # Add nodes for each medication
        for i, med in enumerate(medications):
            name, category = med[1], med[2]
            node_id = f"{name}_{category}_{i}"
            G.add_node(node_id, label=name)

        # Add edges between medications of the same category
        for i, med in enumerate(medications):
            name, category = med[1], med[2]
            node_id = f"{name}_{category}_{i}"
            for j, other_med in enumerate(medications[i + 1:], start=i + 1):
                other_name, other_category = other_med[1], other_med[2]
                other_node_id = f"{other_name}_{other_category}_{j}"
                if category == other_category:
                    G.add_edge(node_id, other_node_id, weight=1.0)

        # Compute shortest paths using non-negative Dijkstra's algorithm
        most_common_category = None
        max_order_count = -1
        for node in G.nodes():
            # Compute shortest paths from the current node to all other nodes
            distances = nx.single_source_dijkstra_path_length(G, node)
            order_count = sum(1 for distance in distances.values() if distance > 0)
            if order_count > max_order_count:
                max_order_count = order_count
                most_common_category = node.split('_')[1]

        # Return the medication name that has the most orders
        medication_names = [med[1] for med in medications if med[2] == most_common_category]
        most_ordered_medication = max(set(medication_names), key=medication_names.count)
        return most_ordered_medication