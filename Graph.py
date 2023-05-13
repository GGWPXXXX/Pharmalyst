import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Customer import Customer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from OrderRepository import OrderRepository
import tkinter as tk
import networkx as nx
import matplotlib.cm as cm


class Graph:
    def __init__(self) -> None:
        self.__med_db = pd.read_excel('./Data/DataSet/Medicine_description.xlsx')
        self.__order_db = pd.read_csv("./Data/Admin/Order.csv")
        self.__order_repo = OrderRepository()
        self.__plt_list = []
        self.__canvas_list = []
        self.__descriptive = {}

    @property
    def descriptive(self) -> dict:
        return self.__descriptive

    @property
    def plt_list(self) -> list:
        return self.__plt_list
    
    @property
    def canvas_list(self)   -> list:
        return self.__canvas_list
      
    def distribution_graph(self, type:str, main_canvas:tk.Canvas) -> None:
        """This method generates a distribution graph based on medication quantity data stored in the system. 
        The type parameter specifies the type of graph to be generated, either a histogram or a box plot. The graph 
        is displayed in the main_canvas tkinter canvas object. The method also calculates and stores several descriptive 
        statistics for the data, including mean, median, standard deviation, variance, minimum, and maximum. The matplotlib 
        library is used to generate the graph and the FigureCanvasTkAgg class is used to embed the graph in the tkinter canvas.
          The plt and canvas objects are stored in instance variables __plt_list and __canvas_list respectively.

        Args:

        type (str): The type of graph to be generated. Either "histogram" or "boxplot".
        main_canvas (tk.Canvas): The tkinter canvas object to display the generated graph.
        Returns:

        None. The generated graph is displayed in the main_canvas object and the descriptive statistics are stored in the instance variable __descriptive."""
        x = np.arange(500, 1001, 50)
        llist = [((self.__med_db.Quantity > i) & (self.__med_db.Quantity < i+50)).sum() for i in x]
        llist.remove(0)
        self.__descriptive["mean"] = np.mean(llist)
        self.__descriptive["median"] = np.median(llist)
        self.__descriptive["std"] = np.std(llist)
        self.__descriptive["variance"] = np.var(llist)
        self.__descriptive["min"] = np.min(llist)
        self.__descriptive["max"] = np.max(llist) 
        fig = plt.figure(figsize=(6, 4), dpi=100)

        if type == "histogram":
            bin_edges = np.arange(500, 1050, 50)
            plt.hist(x=x[:-1], weights=llist, bins=bin_edges, range=(500, 1000))  
            plt.xlabel('Amount of medications')
            plt.ylabel("Frequency")
            plt.title("Graph Show Distribution")
            plt.grid(True)
            plt.xticks(bin_edges[:-1] + 25, [f"[{bin_edges[i]}, {bin_edges[i+1]})" for i in range(len(bin_edges) - 1)], rotation=90)

        else:
            plt.boxplot(self.__med_db.Quantity, showfliers=True, showmeans=True)
            plt.xticks([1], ['Quantity'])
            plt.ylabel("Amount of medications")
            plt.title("Graph Show Distribution")
            plt.grid(True)
            summary_stats = plt.boxplot(self.__med_db.Quantity, showfliers=False, showmeans=True)
            for line in summary_stats['medians']:
                plt.text(1.1, line.get_ydata()[0]+0.5, f"Median: {line.get_ydata()[0]:.2f}")
            for line in summary_stats['boxes']:
                plt.text(1.1, line.get_ydata()[0], f"Q1: {line.get_ydata()[0]:.2f}")
                plt.text(1.1, line.get_ydata()[3], f"Q3: {line.get_ydata()[3]:.2f}")

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=main_canvas)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=150, y=230)
        self.__plt_list.append(plt)
        self.__canvas_list.append(canvas_widget)
        
    def time_series_graph(self, type:str, main_canvas:tk.Canvas) -> None:
        """This method generates a time series graph based on the number of orders per month from 2021 to 2023. 
        The graph can be either a line graph or a bar graph. The method takes two parameters: the type of graph
          (either "line graph" or "bar graph") and the canvas where the graph will be displayed.

        Args:
        type (str): The type of graph to be displayed. Must be either "line graph" or "bar graph".
        main_canvas (tk.Canvas): The canvas where the graph will be displayed.

        Returns:
        None"""
        self.__order_db['Date'] = pd.to_datetime(self.__order_db['Date'])
        #create a new dataframe with the number of orders per month from 2021-2023
        self.__year_sales = self.__order_db.groupby([self.__order_db.Date.dt.year, self.__order_db.Date.dt.month]).size().unstack(level=0)
        fig = plt.figure(figsize=(6, 4), dpi=100)

        for num in range(2021, 2024):
            self.__descriptive["mean_" + str(num)] = self.__year_sales[num].mean()
            self.__descriptive["median_" + str(num)] = self.__year_sales[num].median()
            self.__descriptive["std_" + str(num)] = self.__year_sales[num].std()
            self.__descriptive["variance_" + str(num)] = self.__year_sales[num].var()
            self.__descriptive["min_" + str(num)] = self.__year_sales[num].min()
            self.__descriptive["max_" + str(num)] = self.__year_sales[num].max()
        
        if type == "line graph":
            plt.plot(self.__year_sales, marker="o")
            plt.xlabel("Month")
            plt.ylabel("Number of orders")
            plt.title("Show number of orders per month from 2021-2023")
            plt.xticks(np.arange(1, 13, 1), rotation=45)
            plt.yticks(np.arange(0, 170, 20))
            plt.legend(self.__year_sales.columns)
            plt.grid(True)
            
        elif type == "bar graph":
            x = np.arange(len(self.__year_sales.index))
            width = 0.2
            for i, year in enumerate(self.__year_sales.columns):
                height = self.__year_sales[year]
                plt.bar(x + i*width, height, width=width, label=year)
            plt.xlabel("Month")
            plt.ylabel("Number of orders")
            plt.title("Show number of orders per month from 2021-2023")
            plt.xticks(ticks=x + width, labels=self.__year_sales.index, rotation=45)
            plt.legend(self.__year_sales.columns)
            plt.grid(True)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=main_canvas)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=150, y=230)
        self.__plt_list.append(plt)
        self.__canvas_list.append(canvas_widget)
    
    def network_graph(self, type: str, canvas: tk.Tk) -> None:
        """This method network_graph creates and displays a network graph using the NetworkX 
        library based on the customer's medication orders. The graph can be displayed in either a "category" 
        or "medication" view.

        Parameters:

        type: A string that specifies the type of network graph to display, either "category" or "medication".
        canvas: A Tkinter canvas object where the graph will be displayed.
        Returns: None"""
        c1 = Customer("John Doe", "1234567890", "123 Main St")
        medications = self.__order_repo.load_customer_order(c1)
        G = nx.Graph()

        if type == "category":
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
        else:
            for i, med in enumerate(medications):
                name, category = med[1], med[2]
                node_id = f"{name}_{category}_{i}"
                G.add_node(node_id, label=category)

            connected_categories = set()
            for i, med in enumerate(medications):
                name, category = med[1], med[2]
                if category not in connected_categories:
                    node_id = f"{name}_{category}_{i}"
                    for j, other_med in enumerate(medications[i+1:], start=i+1):
                        other_name, other_category = other_med[1], other_med[2]
                        if category == other_category:
                            other_node_id = f"{other_name}_{other_category}_{j}"
                            G.add_edge(node_id, other_node_id)
                    connected_categories.add(category)
        pos = nx.circular_layout(G)
        fig = plt.figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(1, 1, 1)

        # Define a color map using the rainbow colormap
        cmap = cm.rainbow
        num_nodes = len(G.nodes)
        node_colors = [cmap(i/num_nodes) for i in range(num_nodes)]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='black', font_size=7, width=1, alpha=0.7, node_shape="d", ax=ax)
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=canvas)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas.get_tk_widget().place(x=150, y=230)
        self.__plt_list.append(plt)
        self.__canvas_list.append(canvas_widget)
