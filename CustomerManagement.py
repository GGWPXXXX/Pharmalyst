from CustomerRepository import CustomerRepository
from Customer import Customer
import networkx as nx
from OrderRepository import OrderRepository


class CustomerManagement(Customer):
    def __init__(self) -> None:
        self.__customer_repo = CustomerRepository()
        self.__customer_list = []
        self.__order_repo = OrderRepository()

    def insert_customer_list(self)-> None:
        """
        This method updates the customer list by loading data from the customer 
        repository and merging it with the current list. It returns nothing.

        Parameters: None

        Returns: None

        Raises: None"""
        customer_set = set(self.__customer_list)
        customer_set.update(set(self.__customer_repo.load_data()))
        self.__customer_list = list(customer_set)

    def return_record(self, customer_name:str) -> Customer:
        """
        Returns the customer record for a given name. Searches through the customer list and returns the first
        customer record found with matching name. If no record is found, returns None.
        
        Args:
        - customer_name (str): name of the customer to search for
        
        Returns:
        - (Customer or None): the customer record for the given name, or None if no record is found
        """
        self.insert_customer_list()
        for i in self.__customer_list:
            if i.name == customer_name:
                return i
        return None

    def find_record(self, customer:Customer) -> bool:
        """This method takes a Customer object as input and searches for it in the customer list. If the Customer is found, it returns True, otherwise, it returns False. The method also inserts the loaded customer data from the repository into the customer list before performing the search.

        Args:

        customer (Customer): A Customer object to search for in the customer list.
        Returns:

        bool: True if the Customer object is found in the customer list, False otherwise."""
        self.insert_customer_list()
        for i in self.__customer_list:
            if i.name == customer.name and i.password == customer.password: return True             
        return False
    
    def add(self, customer: Customer) -> bool:
        """    
        Add a new customer to the list and save the updated list to file.

        Args:
            customer (Customer): The new customer object to be added to the list.

        Returns:
            bool: True if the new customer was added successfully, False if it already exists in the list.
        """
        if self.find_record(customer):
            return False
        else:
            self.__customer_list.append(customer)
            self.__customer_repo.save_data(self.__customer_list)
            return True
        
    def create_recommendation(self, customer: Customer) -> str:
        """This method takes a Customer object and uses their past medication order history to create a 
        recommendation for the category of medication they may be interested in purchasing in the future. 
        It returns a string representing the category with the most medications ordered in the past.

        Args:

        customer: A Customer object for whom the recommendation is being generated.
        Returns:

        A string representing the category of medication with the most orders in the past."""
        medications = self.__order_repo.load_customer_order(customer)
        G = nx.Graph()
        category_nodes = {}
        for i, med in enumerate(medications):
            name, category = med[1], med[2]
            if category not in category_nodes:
                category_nodes[category] = []
            node_id = f"{category}_{i}"
            G.add_node(node_id, label=category)
            category_nodes[category].append(node_id)

        # Add edges between medications of the same category
        connected_categories = set()
        for i, med in enumerate(medications):
            name, category = med[1], med[2]
            if category not in connected_categories:
                node_ids = [node_id for node_id in category_nodes[category] if node_id != f"{category}_{i}"]
                for other_node_id in node_ids:
                    G.add_edge(f"{category}_{i}", other_node_id)
                connected_categories.add(category)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='black', font_size=8, width=1, alpha=0.7)

        # Compute shortest paths using non-negative Dijkstra's algorithm
        most_common_category = None
        max_order_count = -1
        for node in G.nodes():
            # Compute shortest paths from the current node to all other nodes
            distances = nx.single_source_dijkstra_path_length(G, node)
            order_count = sum(1 for distance in distances.values() if distance > 0)
            if order_count > max_order_count:
                max_order_count = order_count
                most_common_category = node.split('_')[0]
        return most_common_category

""" manage = CustomerManagement()
c1 = Customer()
c1.name = "John Doe"
print(manage.create_recommendation(c1)) """
