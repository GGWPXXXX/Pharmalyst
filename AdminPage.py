from Graph import Graph
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image


class AdminPage:
    def __init__(self) -> None:      
        self.__graph = Graph()
        self.__button_list = []

    def clear_previous_page(self, canvas: tk.Canvas) -> None:
        """This method is to clear the previous page of the canvas by deleting all the items in it. 
        It also clears the button, entry, and label list which contains the objects created by this class.

        Args:

        canvas: A tk.Canvas object representing the canvas to be cleared.
        Returns:None"""
        canvas.delete("all")
        if len(self.__button_list) != 0:
            for button in self.__button_list:
                button.destroy()
            self.__button_list = []
        if len(self.__graph.plt_list) != 0:
            for plt in self.__graph.plt_list:
                plt.clf()
                plt.close()
        if len(self.__graph.canvas_list) != 0:
            for canvas in self.__graph.canvas_list:
                canvas.destroy()
    
    def open_image(self, path: str, size: tuple) -> ImageTk.PhotoImage:
        """Open image and resize it"""
        image = Image.open(path)
        if sum(size) != 0 :
            image = image.resize(size, Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        return image
    
    def descriptive_stat(self, type:str) -> None:
        """This method descriptive_stat() displays descriptive statistics for the graph.
          It takes in one parameter type which specifies the type of graph that the statistics are to be calculated 
          for, and displays a message box containing the calculated statistics.

        type: A string specifying the type of graph to calculate statistics for. Possible values are 
        "distribution", "network", or "time series".
        If type is "distribution", it displays the mean, median, standard deviation, variance, minimum, 
        and maximum of the graph.

        If type is "network", it displays a message stating that there is no descriptive statistic for this type of graph.

        If type is "time series", it displays the mean, median, standard deviation, variance, minimum, 
        and maximum of each year's data in the time series graph, for the years 2021, 2022, and 2023."""
        if type == "distribution":
            messagebox.showinfo("Descriptive Statistic", 
            message=f"Mean: {(self.__graph.descriptive['mean']):.2f}\nMedian: {(self.__graph.descriptive['median']):.2f}\nStandard Deviation: {(self.__graph.descriptive['std']):.2f}\nVariance: {(self.__graph.descriptive['variance']):.2f} \nMin: {(self.__graph.descriptive['min']):.2f}\nMax: {(self.__graph.descriptive['max']):.2f}")
        elif type == "network":
            messagebox.showinfo("Descriptive Statistic", 
            message=f"This is a network graph, there is no descriptive statistic for this graph")
        else:
            message = ""
            for year in range(2021, 2024):
                message += f"Mean Year's {year}: {self.__graph.descriptive['mean_'+str(year)]:.2f} \n"\
                        f"Median Year's {year}: {self.__graph.descriptive['median_'+str(year)]:.2f}\n"\
                        f"Standard Deviation Year's {year}: {self.__graph.descriptive['std_'+str(year)]:.2f}\n"\
                        f"Variance Year's {year}: {(self.__graph.descriptive['variance_'+str(year)]):.2f} \n"\
                        f"Min Year's {year}: {(self.__graph.descriptive['min_'+str(year)]):.2f}\n"\
                        f"Max Year's {year}: {(self.__graph.descriptive['max_'+str(year)]):.2f}\n\n"
            messagebox.showinfo("Descriptive Statistic", message)
        
    def time_series_graph(self, type:str, canvas:tk.Canvas) -> None:   
        """This method displays a time series graph on a canvas, along with several buttons for navigating and 
        accessing additional information about the graph. The type of time series graph displayed can be controlled 
        by passing in the type argument. The canvas on which the graph is drawn is passed in as the canvas argument.

        The method first clears any previous page from the canvas, and then loads and displays several images, 
        including the background, banner, and buttons. The method then calls the time_series_graph method of the 
        Graph object to actually display the time series graph.

        Finally, the method creates an "info" button which, when clicked, will display descriptive statistics for 
        the time series graph.

        Parameters:

        type (str): The type of time series graph to display, either "line graph" or "bar graph".
        canvas (tk.Canvas): The canvas on which to display the graph and buttons.
        Returns:

        None. The method does not return anything, but instead modifies the canvas by adding the time 
        series graph and various buttons."""
        self.clear_previous_page(canvas)

        self.__bg_img = self.open_image("./Picture/GraphPage/bg2.png", (0, 0))
        canvas.create_image(0,0, image=self.__bg_img, anchor="nw")

        self.__right_panel = self.open_image("./Picture/DashboardPage/tab-admin.png", (850, 800))
        canvas.create_image(600,400, image=self.__right_panel)

        self.__banner = self.open_image("./Picture/GraphPage/bt-timeseries-graph.png", (500, 400))
        canvas.create_image(450, 130, image=self.__banner)

        self.__home_img = self.open_image("./Picture/Button/bt-h.png",(55, 50))
        self.__home_btn = tk.Button(canvas, image=self.__home_img, command=lambda: self.dashboard(canvas),
                                     border=0, bg="#000" ,activebackground="#000")
        self.__button_list.append(self.__home_btn)
        self.__home_btn.place(x=50, y=40)

        self.__bar_img = self.open_image("./Picture/GraphPage/bt-bar-graph.png", (250, 200))
        self.__bar_btn = tk.Button(canvas, image=self.__bar_img, command=lambda:self.__graph.time_series_graph("bar graph", canvas),
                                    border=0, height=130 ,bg="#080118", activebackground="#080118")
        self.__button_list.append(self.__bar_btn)
        self.__bar_btn.place(x=180, y=670)


        self.__line_img = self.open_image("./Picture/GraphPage/bt-line-graph.png", (250, 200))
        self.__line_btn = tk.Button(canvas, image=self.__line_img, command=lambda: self.__graph.time_series_graph("line graph", canvas),
                                    border=0, height=130 ,bg="#080118", activebackground="#080118")
        self.__button_list.append(self.__line_btn)
        self.__line_btn.place(x=480, y=670)
        self.__graph.time_series_graph(type, canvas)

        self.__info_img = self.open_image("./Picture/Button/bt-i.png", (40, 40))
        self.__info_btn = tk.Button(canvas, image=self.__info_img, command=lambda: self.descriptive_stat("time_series"),
                                    border=0, bg="#000", activebackground="#000")
        self.__button_list.append(self.__info_btn)
        self.__info_btn.place(x=100, y=200)

    def distribution_graph(self, type:str, canvas:tk.Canvas) -> None:
        """The distribution_graph method displays a distribution graph on a tkinter canvas based on 
        the type of graph specified. The canvas is first cleared and then the background image, banner image, 
        and right panel image are displayed on it. Buttons for navigating to other types of graphs and for 
        displaying descriptive statistics are also displayed on the canvas.

        Parameters:

        type (str): The type of distribution graph to be displayed, either "histogram" or "line".
        canvas (tk.Canvas): The tkinter canvas on which the distribution graph is to be displayed.
        Returns:

        None"""

        self.clear_previous_page(canvas)
        
        self.__bg_img = self.open_image("./Picture/GraphPage/bg2.png", (0, 0))
        canvas.create_image(0,0, image=self.__bg_img, anchor="nw")

        self.__right_panel = self.open_image("./Picture/DashboardPage/tab-admin.png", (850, 800))
        canvas.create_image(600,400, image=self.__right_panel)

        self.__banner = self.open_image("./Picture/GraphPage/bt-distribution-graph.png", (500, 400))
        canvas.create_image(450, 130, image=self.__banner)

        self.__home_img = self.open_image("./Picture/Button/bt-h.png",(55, 50))
        self.__home_btn = tk.Button(canvas, image=self.__home_img, command=lambda: self.dashboard(canvas),
                                     border=0, bg="#000", activebackground="#000")
        self.__button_list.append(self.__home_btn)
        self.__home_btn.place(x=50, y=40)

        self.__hist_img = self.open_image("./Picture/GraphPage/bt-hitogram-graph.png", (250, 200))
        self.__hist_btn = tk.Button(canvas, image=self.__hist_img, command=lambda:self.__graph.distribution_graph("histogram", canvas),
                                    border=0, height=130,bg="#080118", activebackground="#080118")
        self.__button_list.append(self.__hist_btn)
        self.__hist_btn.place(x=180, y=670)

        self.__box_img = self.open_image("./Picture/GraphPage/bt-box-graph.png", (250, 200))
        self.__box_btn = tk.Button(canvas, image=self.__box_img, command=lambda: self.__graph.distribution_graph("line", canvas),
                                    border=0, height=130,bg="#080118", activebackground="#080118")
        self.__button_list.append(self.__box_btn)
        self.__box_btn.place(x=480, y=670)

        self.__graph.distribution_graph(type, canvas)
                
        self.__info_img = self.open_image("./Picture/Button/bt-i.png", (40, 40))
        self.__info_btn = tk.Button(canvas, image=self.__info_img, command=lambda: self.descriptive_stat("distribution"),
                                    border=0, bg="#000", activebackground="#000")
        self.__button_list.append(self.__info_btn)
        self.__info_btn.place(x=100, y=200)


    def dashboard(self, canvas) -> None:
        """This method, dashboard(canvas), creates the dashboard page with three buttons, 
        each of which when clicked, displays a different graph page with additional functionality.

        Parameters:

        canvas: A tkinter.Canvas object on which to display the dashboard page.
        Returns:

        None"""
        self.clear_previous_page(canvas)

        self.__bg_img = self.open_image("./Picture/DashboardPage/bg-admin-dashboard.png", (0, 0))
        canvas.create_image(0, 0, image=self.__bg_img, anchor='nw')

        self.__right_panel = self.open_image("./Picture/DashboardPage/tab-admin.png", (850, 800))
        canvas.create_image(600,400, image=self.__right_panel)

        self.__banner = self.open_image("./Picture/DashboardPage/vector-dashboard.png", (600, 500))
        canvas.create_image(480, 150, image=self.__banner)

        self.__network_img = self.open_image("./Picture/DashboardPage/vector-networkgraph.png", (500, 400))
        self.__network_btn = tk.Button(canvas, image=self.__network_img, command=lambda: self.network_graph("category", canvas),
                                border=0, height=380, width=250, bg="#131241", activebackground="#131241")

        self.__button_list.append(self.__network_btn)
        self.__network_btn.place(x=30, y=280)

        self.__dist_graph = self.open_image("./Picture/DashboardPage/vector-distribution.png", (500, 400))
        self.__dist_btn = tk.Button(canvas, image=self.__dist_graph, command=lambda: self.distribution_graph("histogram", canvas),
                                    border=0, height=380, width=250, bg="#131241", activebackground="#131241")
        self.__button_list.append(self.__dist_btn)
        self.__dist_btn.place(x=280, y=280)
        
        self.__time_series = self.open_image("./Picture/DashboardPage/vector-timeseries.png", (500, 400))
        self.__time_series_btn = tk.Button(canvas, image=self.__time_series, command=lambda: self.time_series_graph("bar graph", canvas),
                                    border=0, height=380, width=250, bg="#131241" ,activebackground="#131241")
        self.__button_list.append(self.__time_series_btn)
        self.__time_series_btn.place(x=530, y=280)

    def network_graph(self, type:str, canvas:tk.Canvas) -> None:
        """This method displays the network graph based on the specified type and sets up the necessary buttons for interaction with the graph.

        Args:
        type (str): The type of data to be plotted on the graph, either "category" or "med_name".
        canvas (tk.Canvas): The canvas on which the graph and buttons will be displayed.

        Returns:
        None.

        Raises:
        None."""
        self.clear_previous_page(canvas)
        self.__graph.network_graph(type, canvas)

        self.__bg_img = self.open_image("./Picture/GraphPage/bg2.png", (0, 0))
        canvas.create_image(0,0, image=self.__bg_img, anchor="nw")

        self.__right_panel = self.open_image("./Picture/DashboardPage/tab-admin.png", (850, 800))
        canvas.create_image(600,400, image=self.__right_panel)

        self.__banner = self.open_image("./Picture/GraphPage/bt-network-graph.png", (500, 400))
        canvas.create_image(450, 130, image=self.__banner)

        self.__home_img = self.open_image("./Picture/Button/bt-h.png",(55, 50))
        self.__home_btn = tk.Button(canvas, image=self.__home_img, command=lambda: self.dashboard(canvas),
                                     border=0, bg="#000", activebackground="#000")
        self.__button_list.append(self.__home_btn)
        self.__home_btn.place(x=50, y=40)

        
        self.__cate_img = self.open_image("./Picture/GraphPage/category.png", (250, 200))
        self.__cate_btn = tk.Button(canvas, image=self.__cate_img, command=lambda:self.__graph.network_graph("category", canvas),
                                    border=0, height=130,bg="#080118", activebackground="#080118")
        self.__button_list.append(self.__cate_btn)
        self.__cate_btn.place(x=180, y=650)

        self.__med_name_img = self.open_image("./Picture/GraphPage/medName.png", (250, 200))
        self.__med_name_btn = tk.Button(canvas, image=self.__med_name_img, command=lambda: self.__graph.network_graph("med_name", canvas),
                                    border=0, height=130,bg="#080118", activebackground="#080118")
        self.__button_list.append(self.__med_name_btn)
        self.__med_name_btn.place(x=480, y=650)

        self.__info_img = self.open_image("./Picture/Button/bt-i.png", (40, 40))
        self.__info_btn = tk.Button(canvas, image=self.__info_img, command=lambda: self.descriptive_stat("network"),
                                    border=0, bg="#000", activebackground="#000")
        self.__button_list.append(self.__info_btn)
        self.__info_btn.place(x=100, y=200)
