import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from Customer import Customer
from Admin import Admin
from CustomerManagement import CustomerManagement
from MedicationPage import MedicationPage
from AdminPage import AdminPage
from AdminManagemment import AdminManagemment


class FrontPage:
    def __init__(self, window: tk.Tk):
        self.__window = window
        self.__customer = Customer()
        self.__customer_manage = CustomerManagement()
        self.__admin = Admin()
        self.__admin_manage = AdminManagemment()
        self.__admin_page = AdminPage()
        self.__medication_page = MedicationPage(self.__window)
        self.__button_list = []
        self.__entry_list = []
        self.__label_list = []

    def clear_previous_page(self, canvas: tk.Canvas) -> None:
        """This method is to clear the previous page of the canvas by deleting all the items in it.
          It also clears the button, entry, and label list which contains the objects created by this class.

        Args:canvas: A tk.Canvas object representing the canvas to be cleared.
        Returns:None"""
        canvas.delete("all")
        if len(self.__button_list) != 0:
            for button in self.__button_list:
                button.destroy()
            self.__button_list = []
        if len(self.__entry_list) != 0:
            for entry in self.__entry_list:
                entry.destroy()
            self.__entry_list = []
        if len(self.__label_list) != 0:
            for label in self.__label_list:
                label.destroy()

    def open_image(self, path: str, size: tuple) -> ImageTk.PhotoImage:
        """Open image from the given path and resize it"""
        image = Image.open(path)
        if sum(size) != 0:
            image = image.resize(size, Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        return image

    def register_page(self, canvas: tk.Canvas) -> None:
        """The register_page method creates a register page for new customers. 
        It first clears the canvas and removes any previous widgets, then it creates and displays the necessary widgets 
        for the register page, including images, labels, entries, and a submit button. The add_customer function is called 
        when the submit button is clicked and it creates a new customer object with the information entered in the entries. 
        If the customer is successfully added to the system, a success message is displayed, and the user is redirected to 
        the login page. If the customer is already in the system, an error message is displayed and the user is redirected 
        to the login page.

        Args:

        canvas: a tkinter canvas object where the widgets will be displayed.
        Returns:

        None."""
        self.clear_previous_page(canvas)

        def add_customer(self, name: str, password: str, address: str):
            if len(name) == 0 or len(password) == 0 or len(address) == 0:
                messagebox.showerror(
                    title="Error404", message="Can't be blank.")
                return
            self.__customer = Customer(name, str(password), address)
            if self.__customer_manage.add(self.__customer):
                messagebox.showinfo(title=":)", message="Sign Up Complete :)")

                self.login_page(canvas)
                return
            else:
                messagebox.showerror(
                    title=":()", message="You're already on the system.")
                self.login_page(canvas)
                return

        self.__bg_img = self.open_image(
            r"./Picture/RegisterPage/bg.png", (1000, 800))
        canvas.create_image(0, 0, image=self.__bg_img, anchor='nw')

        self.__text_signup_img = self.open_image(
            r"./Picture/RegisterPage/text-signup.png", (500, 400))
        canvas.create_image(500, 100, image=self.__text_signup_img)

        self.__background_box_img = self.open_image(
            r"./Picture/RegisterPage/bg-signup.png", (0, 0))
        canvas.create_image(500, 430, image=self.__background_box_img)

        self.__doctor_img = self.open_image(
            r"./Picture/RegisterPage/doctor.png", (0, 0))
        canvas.create_image(680, 500, image=self.__doctor_img)

        self.__name_text = self.open_image(
            r"./Picture/RegisterPage/username.png", (250, 200))
        canvas.create_image(320, 230, image=self.__name_text)
        self.__name_entry = tk.Entry(width=25, border=0, font=("Arial", 18))
        self.__name_entry.place(x=150, y=270, height=50)
        self.__entry_list.append(self.__name_entry)

        self.__password_text = self.open_image(
            r"./Picture/RegisterPage/password.png", (250, 200))
        canvas.create_image(320, 360, image=self.__password_text)

        self.__password_entry = tk.Entry(
            width=25, border=0, font=("Arial", 18), show="*")
        self.__password_entry.place(x=150, y=400, height=50)
        self.__entry_list.append(self.__password_entry)

        self.__address_text = self.open_image(
            r"./Picture/RegisterPage/Adress.png", (250, 200))
        canvas.create_image(320, 500, image=self.__address_text)
        self.__address_entry = tk.Entry(width=25, border=0, font=("Arial", 18))
        self.__address_entry.place(x=150, y=540, height=50)
        self.__entry_list.append(self.__address_entry)

        self.__submit_img = self.open_image(
            r"./Picture/RegisterPage/bt-submit.png", (300, 220))
        self.__submit_btn_img = tk.Button(image=self.__submit_img, border=0,
                                          height=70, width=200, padx=0, pady=0,
                                          bg="#B9CAFA", command=lambda: add_customer(self, self.__name_entry.get(),
                                                                                     self.__password_entry.get(),
                                                                                     self.__address_entry.get()))
        self.__button_list.append(self.__submit_btn_img)
        self.__submit_btn_img.place(x=215, y=620)

    def login_system(self, name: str, password: str, canvas: tk.Canvas) -> None:
        """
        This method validates the login credentials of the customer by verifying the entered name and password against the
        customer records in the customer management system. If the entered name and password are valid, the customer is
        logged in and redirected to the medication page. Otherwise, an error message is displayed.

        :param name: A string representing the name of the customer to be logged in.
        :param password: A string representing the password of the customer to be logged in.
        :param canvas: A Tkinter canvas object representing the canvas on which the next page will be displayed.
        :return: None
        """
        if (len(name) == 0 or len(str(password)) == 0):
            messagebox.showerror(
                title="Error404", message="Can't be blank.")
            return
        self.__customer = Customer(name, str(password), "")
        if self.__customer_manage.find_record(self.__customer):
            messagebox.showinfo(
                title="Complete", message="Login Completed!")
            self.__customer = self.__customer_manage.return_record(name)
            self.__medication_page = MedicationPage(
                window=self.__window, customer=self.__customer)
            self.clear_previous_page(canvas)
            self.__medication_page.category_page(canvas)
            return
        else:
            messagebox.showerror(
                title="Error404", message="Can't find your record!")

    def login_page(self, canvas: tk.Canvas) -> None:
        """
        This method displays the login page where the user can enter their username and password to login to the system.

        Args:
            canvas (tk.Canvas): The canvas where the login page will be displayed.
        """
        self.clear_previous_page(canvas)
        self.__background_img = self.open_image(
            r"./Picture/LoginPage/bg-login.png", (1000, 800))
        canvas.create_image(0, 0, anchor="nw", image=self.__background_img)

        self.__text__login_img = self.open_image(
            r"./Picture/LoginPage/Login.png", (500, 400))
        canvas.create_image(500, 100, image=self.__text__login_img)

        self.__background_box_img = self.open_image(
            r"./Picture/LoginPage/two-block.png", (0, 0))
        canvas.create_image(500, 430, image=self.__background_box_img)

        self.__doctor_img = self.open_image(
            r"./Picture/LoginPage/vector-login.png", (0, 0))
        canvas.create_image(295, 585, image=self.__doctor_img)

        self.__name_text = self.open_image(
            r"./Picture/LoginPage/username.png", (250, 200))
        canvas.create_image(715, 290, image=self.__name_text)
        self.__name_entry = tk.Entry(width=25, border=0, font=("Arial", 18))
        self.__name_entry.place(x=545, y=320, height=50)
        self.__entry_list.append(self.__name_entry)

        self.__password_text = self.open_image(
            r"./Picture/LoginPage/password.png", (250, 200))
        canvas.create_image(715, 430, image=self.__password_text)
        self.__password_entry = tk.Entry(
            width=25, border=0, font=("Arial", 18), show="*")
        self.__password_entry.place(x=545, y=460, height=50)
        self.__entry_list.append(self.__password_entry)

        self.__submit_img = self.open_image(
            r"./Picture/LoginPage/submit.png", (300, 220))
        self.__submit_login_btn = tk.Button(image=self.__submit_img,
                                            border=0, height=70, width=200, padx=0, pady=0,
                                            bg="#F1E5CD",
                                            command=lambda: self.login_system(self.__name_entry.get(), self.__password_entry.get(), canvas))
        self.__submit_login_btn.place(x=600, y=560)
        self.__button_list.append(self.__submit_login_btn)

        self.__admin_img = self.open_image(
            r"./Picture/LoginPage/Bt-loginAdmin.png", (300, 230))
        self.__admin_login_btn = tk.Button(image=self.__admin_img,
                                           border=0, height=70, width=300, padx=0, pady=0,
                                           bg="#F1E5CD",
                                           command=lambda: self.admin_login_page(canvas), activebackground="#F1E5CD")
        self.__admin_login_btn.place(x=550, y=650)
        self.__button_list.append(self.__admin_login_btn)

    def welcome_page(self, canvas: tk.Canvas) -> None:
        """This method displays the welcome page of the application. It creates and places several widgets on the canvas, 
        such as images and buttons. The user can click on the login button to proceed to the 
        login page or the signup button to proceed to the registration page.
        Args:canvas: A Tkinter canvas object where the widgets will be placed.
        Returns:None."""
        self.clear_previous_page(canvas)
        self.__bg_img = self.open_image(
            r"./Picture/WelcomePage/h-bg.png", (1000, 800))
        canvas.create_image(0, 0, image=self.__bg_img, anchor="nw")

        self.__welcome_txt = self.open_image(
            r"./Picture/WelcomePage/h-text-wel.png", (650, 550))
        canvas.create_image(510, 110, image=self.__welcome_txt)

        self.__doctor = self.open_image(
            r"./Picture/WelcomePage/h-pic.png", (500, 400))
        canvas.create_image(500, 350, image=self.__doctor)

        self.__login_img = self.open_image(
            r"./Picture/WelcomePage/hbt-login.png", (300, 220))
        self.__login_btn = tk.Button(image=self.__login_img, background="#FBF7EF", border=0, width=250,
                                     height=130, command=lambda: self.login_page(canvas))
        self.__login_btn.place(x=360, y=560)
        self.__button_list.append(self.__login_btn)

        self.__signup_img = self.open_image(
            r"./Picture/WelcomePage/bt-signup.png", (170, 140))
        self.__signup_btn = tk.Button(background="#FBF7EF", border=0, width=180,
                                      height=100, image=self.__signup_img,
                                      padx=5, pady=5, command=lambda: self.register_page(canvas))
        self.__signup_btn.place(x=385, y=670)
        self.__button_list.append(self.__signup_btn)

    def admin_login_system(self, name: str, password: str, canvas: tk.Canvas) -> None:
        """This method checks the admin login system by creating an instance of the Admin class with the provided name and 
        password arguments and checking if it exists in the admin records using the find_record method from the AdminManagement class. 
        If the record is found, the user is redirected to the admin dashboard page. If not, an error message is displayed using messagebox.showerror.
        Args:
        name (str): The username entered by the user.
        password (str): The password entered by the user.
        canvas (tk.Canvas): The canvas on which the UI is drawn."""
        if (len(name) == 0 or len(str(password)) == 0):
            messagebox.showerror(
                title="Error404", message="Can't be blank.")
            return
        self.__admin = Admin(name, str(password))
        if self.__admin_manage.find_record(self.__admin):
            messagebox.showinfo(
                title="Complete", message="Login Completed!")
            self.clear_previous_page(canvas)
            self.__admin_page.dashboard(canvas)
            return
        else:
            messagebox.showerror(
                title="Error404", message="Can't find your record!")

    def admin_login_page(self, canvas: tk.Canvas) -> None:
        """The admin_login_page method is used to create the login page for an admin. 
        It sets up the necessary widgets and images and creates the UI for the admin login system.
        Args: canvas: A tkinter Canvas object on which the login page will be displayed.
        Returns:

        None"""
        self.clear_previous_page(canvas)

        self.__admin_bg_img = self.open_image(
            r"./Picture/AdminLoginPage/bg-admin-login.png", (0, 0))
        canvas.create_image(0, 0, image=self.__admin_bg_img, anchor="nw")

        self.__cartoon = self.open_image(
            r"./Picture/AdminLoginPage/vector-cartoon.png", (950, 800))
        canvas.create_image(250, 450, image=self.__cartoon)

        self.__login_text = self.open_image(
            r"./Picture/AdminLoginPage/text-admin-login.png", (450, 350))
        canvas.create_image(710, 150, image=self.__login_text)

        self.__rectangle = self.open_image(
            r"./Picture/AdminLoginPage/rectangle.png", (700, 500))
        canvas.create_image(720, 500, image=self.__rectangle)

        self.__welcome_txt = self.open_image(
            r"./Picture/AdminLoginPage/text-welcome.png", (350, 250))
        canvas.create_image(710, 350, image=self.__welcome_txt)

        self.__admin_name_entry = tk.Entry(
            width=20, border=0, font=("Arial", 18))
        self.__admin_name_entry.place(x=620, y=400, height=50)
        self.__entry_list.append(self.__admin_name_entry)
        self.__name_logo = self.open_image(
            r"./Picture/AdminLoginPage/usernamelogo.png", (60, 50))
        canvas.create_image(580, 425, image=self.__name_logo)

        self.__admin_password_entry = tk.Entry(
            width=20, border=0, font=("Arial", 18), show="*")
        self.__admin_password_entry.place(x=620, y=500, height=50)
        self.__entry_list.append(self.__admin_password_entry)
        self.__password_logo = self.open_image(
            r"./Picture/AdminLoginPage/passwordlogo.png", (60, 50))
        canvas.create_image(580, 525, image=self.__password_logo)

        self.__login_btn_img = self.open_image(
            r"./Picture/AdminLoginPage/login.png", (300, 220))
        self.__login_btn = tk.Button(image=self.__login_btn_img, background="#000", border=0, width=250,
                                     height=70, command=lambda: self.admin_login_system(self.__admin_name_entry.get(), self.__admin_password_entry.get(), canvas),
                                     activebackground="#000")
        self.__login_btn.place(x=600, y=580)
        self.__button_list.append(self.__login_btn)
