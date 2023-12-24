import tkinter as tk
from tkinter import Toplevel, messagebox
from PIL import ImageTk, Image
from MedicationRepository import MedicationRepository
from OrderRepository import OrderRepository
from datetime import datetime
from CustomerManagement import CustomerManagement

class MedicationPage():
    def __init__(self, window:tk.Tk, customer=None) -> None:
        self.__window = window
        if customer is not None:
            self.__customer = customer
        self.__img_dict = {}
        self.__button_list = []
        self.__entry_list = []
        self.__label_list = []
        self.__customer_management = CustomerManagement()
        self.__category_list = []
        self.__order_repo = OrderRepository()
        self.__medication_repo = MedicationRepository()
        self.__curr_page = 0

    def open_image(self, path: str, size: tuple)-> ImageTk.PhotoImage   :
        """Open image and resize it"""
        image = Image.open(path)
        if sum(size) != 0 :
            image = image.resize(size, Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        return image
    
    def clear_previous_page(self, canvas: tk.Canvas) -> None:
        """This method is to clear the previous page of the canvas by deleting all the items in it. 
        It also clears the button, entry, and label list which contains the objects created by this class.

        Args:

        canvas: A tk.Canvas object representing the canvas to be cleared.
        Returns:

        None"""
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
    
    def medication_page(self, canvas: tk.Canvas, category: str) -> None:
        """This function is to create medication page with 15 medication per page."""

        self.clear_previous_page(canvas)
        self.__bg_img = Image.open(
            r"./Picture/MedicationPage/MedicationBg.png")
        self.__bg_img = ImageTk.PhotoImage(self.__bg_img)
        canvas.create_image(0, 0, image=self.__bg_img, anchor="nw")

        # load medication information and put it in dictionary.
        self.__medication_dict = {}
        self.__num = 0
        for med in self.__medication_repo.load_data(category):
            self.__medication_dict[self.__num] = {"Drug_Name": med.name,
                                                  "Description": str(med.description).replace("/xa0", ""),
                                                  "Quantity": med.quantity, "Category":med.category}
            self.__num += 1
        # create background mini window.
        self.__mini_screen = tk.Label(
            width=116, height=33, bg="#fff", padx=10, pady=10)
        self.__mini_screen.place(x=90, y=180)
        self.__label_list.append(self.__mini_screen)
    

        # create information button.
        self.__info_img = self.open_image(r"./Picture/Button/Information.png", (40, 40))

        # create buy button.
        self.__buy_img = self.open_image(r"./Picture/Button/Buy.png", (40, 40))

        self.__coordinates_dict = {1: {"x": 5, "y": 20}, 2: {"x": 280, "y": 20}, 3: {"x": 560, "y": 20}, 4: {"x": 5, "y": 120}, 5: {"x": 280, "y": 120}, 6: {"x": 560, "y": 120}, 7: {"x": 5, "y": 220}, 8: {
            "x": 280, "y": 220}, 9: {"x": 560, "y": 220}, 10: {"x": 5, "y": 320}, 11: {"x": 280, "y": 320}, 12: {"x": 560, "y": 320}, 13: {"x": 5, "y": 420}, 14: {"x": 280, "y": 420}, 15: {"x": 560, "y": 420}}
        # next button
        self.__next_img = self.open_image(r"./Picture/Button/Next.png", (50, 50))
        self.__next_btn = tk.Button(canvas, image=self.__next_img, border=0, bg="#FBF7EF",
                                    command=lambda: next_page(self.__old_label_list))
        self.__next_btn.place(x=870, y=40)
        self.__button_list.append(self.__next_btn)

        # previous button
        self.__previous_img = self.open_image(r"./Picture/Button/Back.png", (50, 50))
        self.__previous_btn = tk.Button(canvas, image=self.__previous_img, border=0, bg="#FBF7EF",
                                        command=lambda: previous_page(self.__old_label_list))
        self.__previous_btn.place(x=820, y=40)
        self.__button_list.append(self.__previous_btn)

        # home button
        self.__home_img = self.open_image(r"./Picture/Button/Home.png", (50, 50))
        self.__home_btn = tk.Button(canvas, image=self.__home_img, border=0,
                                    bg="#FBF7EF", command=lambda: self.category_page(canvas))
        self.__home_btn.place(x=930, y=40)
        self.__button_list.append(self.__home_btn)

        self.__old_label_list = []

        def next_page(old_label_list: list):
            # this sub function main purpose is to clear the previous page and lead to the next page.
            if len(old_label_list) > 0:
                for label in old_label_list:
                    label.destroy()
            self.next_page(category)

        def previous_page(old_label_list: list):
            """this sub function main purpose is to clear the previous page and lead to the previous page."""
            if len(old_label_list) > 0:
                for label in old_label_list:
                    label.destroy()
            self.previous_page()
        
        if self.__curr_page == 0:
            self.__previous_btn.config(state="disabled")

        for index in range(0, 15):
            self.__bg_name = f"background{index}"
            self.__bg_name = tk.Label(self.__mini_screen, padx=2, pady=2, height=5,
                                      width=36, bg="#D7DEF1")
            self.__bg_name.place(x=self.__coordinates_dict[index+1]["x"],
                                 y=self.__coordinates_dict[index+1]["y"])
            self.__old_label_list.append(self.__bg_name)
            self.__label_list.append(self.__bg_name)

            self.__label_name = f"text{index}"
            self.__label_name = tk.Label(self.__bg_name,
                                         text=self.__medication_dict[index]["Drug_Name"],
                                         bg="#D7DEF1", font=("Arial", 10),
                                         height=1, padx=10, pady=10)
            self.__label_name.place(relx=0, rely=0.5, anchor="sw")
            self.__old_label_list.append(self.__label_name)
            self.__label_list.append(self.__label_name)

            self.__info_btn = f"info_btn{index}"
            self.__info_btn = tk.Button(
                self.__bg_name, image=self.__info_img, border=0, bg="#D7DEF1",
                 command=lambda i=index: self.information_box(self.__medication_dict[i]["Drug_Name"], 
                                                            self.__medication_dict[i]["Description"]))
            self.__info_btn.place(relx=0.2, rely=0.45, anchor="ne")
            self.__button_list.append(self.__info_btn)
            self.__buy_btn = f"buy_btn{index}"
            self.__buy_btn = tk.Button(
                self.__bg_name, image=self.__buy_img, border=0, bg="#D7DEF1", 
                command=lambda i=index: self.confirmed_order_page(self.__medication_dict[i]["Drug_Name"], 
                                                            self.__medication_dict[i]["Description"],
                                                            self.__medication_dict[i]["Category"]))
            self.__buy_btn.place(relx=0.4, rely=0.45, anchor="ne")
            self.__button_list.append(self.__buy_btn)
        self.__med_index = 15

    def next_page(self, category: str) -> None:
        """This function is to create the next page of the medication list."""
        self.__window.update()
        self.__curr_page += 1
        if self.__curr_page != 0:
            self.__previous_btn.config(state="normal")
        else:
            self.__previous_btn.config(state="disabled")

        num = max(self.__medication_dict.keys()) + 1
        for med in self.__medication_repo.load_and_compare_data(category, self.__medication_dict):
            self.__medication_dict[num] = {"Drug_Name": med.name,
                                           "Description": med.description.replace("/xa0", ""),
                                           "Quantity": med.quantity, "Category":med.category}
            num += 1

        self.__old_label_list = []
        if len(self.__old_label_list) != 0:
            for label in self.__old_label_list:
                label.destroy()
        index = 1
        for num in range(len(self.__medication_dict) - 15, len(self.__medication_dict)):
            self.__bg_name = f"background{num}"
            self.__bg_name = tk.Label(self.__mini_screen, padx=2, pady=2, height=5,
                                      width=36, bg="#D7DEF1")
            self.__bg_name.place(x=self.__coordinates_dict[index]["x"],
                                 y=self.__coordinates_dict[index]["y"])
            self.__old_label_list.append(self.__bg_name)
            self.__label_list.append(self.__bg_name)

            self.__label_name = f"text{num}"
            self.__label_name = tk.Label(self.__bg_name,
                                         text=self.__medication_dict[num]["Drug_Name"],
                                         bg="#D7DEF1", font=("Arial", 10),
                                         height=1, padx=10, pady=10) 
            self.__label_name.place(relx=0, rely=0.5, anchor="sw")
            self.__old_label_list.append(self.__label_name)
            self.__label_list.append(self.__label_name)

            self.__info_btn = f"info_btn{num}"
            self.__info_btn = tk.Button(
                self.__bg_name, image=self.__info_img, border=0, bg="#D7DEF1",
                  command=lambda n=num:self.information_box(self.__medication_dict[n]["Drug_Name"], 
                                                            self.__medication_dict[n]["Description"]))
            self.__info_btn.place(relx=0.2, rely=0.45, anchor="ne")
            self.__button_list.append(self.__info_btn)

            self.__buy_btn = f"buy_btn{num}"
            self.__buy_btn = tk.Button(
                self.__bg_name, image=self.__buy_img, border=0, bg="#D7DEF1", 
                command=lambda i=num: self.confirmed_order_page(self.__medication_dict[i]["Drug_Name"], 
                                                            self.__medication_dict[i]["Description"],
                                                            self.__medication_dict[i]["Category"]))
            self.__buy_btn.place(relx=0.4, rely=0.45, anchor="ne")
            self.__button_list.append(self.__buy_btn)

            index += 1
        self.__med_index += 15
    
    def information_box(self, medication_name:str, medication_description: str) -> None:
        messagebox.showinfo(message=f"""Name: {medication_name} \n\nDescription: {medication_description}"""
                            , title="Medication Information")


    def previous_page(self)     -> None:
        """This function is to create the previous page of the medication list."""
        self.__window.update()
        self.__old_label_list = []
        self.__curr_page -= 1
        if self.__curr_page != 0:
            self.__previous_btn.config(state="normal")
        else:
            self.__previous_btn.config(state="disabled")
        if len(self.__old_label_list) != 0:
            for label in self.__old_label_list:
                label.destroy()
        index = 1
        for num in range(self.__med_index - 30, self.__med_index - 15):

            self.__bg_name = f"background{num}"
            self.__bg_name = tk.Label(self.__mini_screen, padx=2, pady=2, height=5,
                                      width=36, bg="#D7DEF1")
            self.__bg_name.place(x=self.__coordinates_dict[index]["x"],
                                 y=self.__coordinates_dict[index]["y"])

            self.__label_name = f"text{num}"
            self.__label_name = tk.Label(self.__bg_name,
                                         text=self.__medication_dict[num]["Drug_Name"],
                                         bg="#D7DEF1", font=("Arial", 10),
                                         height=1, padx=10, pady=10)
            self.__label_name.place(relx=0, rely=0.5, anchor="sw")
            self.__old_label_list.append(self.__label_name)
            self.__old_label_list.append(self.__bg_name)

            self.__info_btn = f"info_btn{num}"
            self.__info_btn = tk.Button(
                self.__bg_name, image=self.__info_img, border=0, bg="#D7DEF1",
                command= lambda n=num :self.information_box(self.__medication_dict[n]["Drug_Name"], 
                                                            self.__medication_dict[n]["Description"]))
            self.__info_btn.place(relx=0.2, rely=0.45, anchor="ne")
            self.__button_list.append(self.__info_btn)

            self.__buy_btn = f"buy_btn{num}"
            self.__buy_btn = tk.Button(
                self.__bg_name, image=self.__buy_img, border=0, bg="#D7DEF1", 
                command=lambda i=num: self.confirmed_order_page(self.__medication_dict[i]["Drug_Name"], 
                                                            self.__medication_dict[i]["Description"],
                                                            self.__medication_dict[i]["Category"]))
            self.__buy_btn.place(relx=0.4, rely=0.45, anchor="ne")
            self.__button_list.append(self.__buy_btn)

            index += 1
        self.__med_index -= 15

    def category_template(self, canvas:tk.Canvas) -> None:

        self.__pos_dict = {1:{"x":70, "y":200}, 2:{"x":370, "y":"200"}, 3:{"x":670, "y":200}, 
                           4:{"x":70, "y":450}, 5:{"x":370, "y":450}, 6:{"x":670, "y":450},
                           7:{"x":70, "y":200}, 8:{"x":370, "y":"200"}, 9:{"x":670, "y":200}, 
                           10:{"x":70, "y":450}, 11:{"x":370, "y":450}, 12:{"x":670, "y":450},
                           13:{"x":70, "y":200}}
        def on_click(self, num:int):
            if num == 1:
                self.skin_condi_page(canvas)
            elif num == 2:
                self.neurological_condi_page(canvas)
            elif num == 3:
                self.allergies_condi_page(canvas)
            elif num == 4:
                self.cardio_condi_page(canvas)
            elif num == 5:
                self.endocrine_condi_page(canvas)
            elif num == 6:
                self.infection_condi_page(canvas)
            elif num == 7:
                self.haemoto_condi_page(canvas)
            elif num == 8:
                self.pain_condi_page(canvas)
            elif num == 9:
                self.respiratory_condi_page(canvas)
            elif num == 10:
                self.reproductive_condi_page(canvas)
            elif num == 11:
                self.muscoloskeletal_condi_page(canvas)
            elif num == 12:
                self.eyes_condition_page(canvas)
            elif num == 13:
                self.others_condi_page(canvas)
        for num in range(min(self.__img_dict.keys()), max(self.__img_dict.keys())+1):
            if num in self.__img_dict:
                self.__btn_name = f"btn{num}"
                self.__btn_name = tk.Button(border=0, image=self.__img_dict[num],
                                            height=200, width=260, bg="#FBF7EF",
                                            command=lambda n=num: on_click(self, n))
                self.__btn_name.place(x=self.__pos_dict[num]["x"], y=self.__pos_dict[num]["y"])
                self.__button_list.append(self.__btn_name)


    def category_page(self, canvas: tk.Canvas) -> None:
        """This method create the category page of the application. Where you can find the 
        category of the medication."""
        self.__img_dict.clear()                               
        self.clear_previous_page(canvas)
        # background image
        self.__bg_img = Image.open(r"./Picture/CategoryPage/bg-cate.png")
        self.__bg_img = ImageTk.PhotoImage(self.__bg_img)
        canvas.create_image(0, 0, anchor="nw", image=self.__bg_img)

        # skin condition button
        skin_contidion_img = self.open_image("./Picture/CategoryPage/c01.png", (280, 230))
        self.__img_dict[1] = skin_contidion_img

        # neurological button
        neuro_condition_img = self.open_image("./Picture/CategoryPage/c02.png", (280, 230))
        self.__img_dict[2] = neuro_condition_img

        # allergy button
        allergy_condition_img = self.open_image("./Picture/CategoryPage/c03.png", (280, 230))
        self.__img_dict[3] = allergy_condition_img

        # cardio vascular button
        cardio_condition_img = self.open_image("./Picture/CategoryPage/c04.png", (280, 230))
        self.__img_dict[4] = cardio_condition_img

        # endocrine vascular button
        endocrine_condition_img = self.open_image("./Picture/CategoryPage/c05.png", (280, 230))
        self.__img_dict[5] = endocrine_condition_img

        # infection button
        infection_condition_img = self.open_image("./Picture/CategoryPage/c06.png", (280, 230))
        self.__img_dict[6] = infection_condition_img

        self.category_template(canvas)

        # next button
        self.__next_img = self.open_image(r"./Picture/CategoryPage/bt-next.png", (150, 120))

        self.__next_btn = tk.Button(border=0, image=self.__next_img,height=110, width=115, bg="#FBF7EF",
                                    padx=5, pady=5, command=lambda: self.category_page_2(canvas))
        self.__next_btn.place(x=730, y=670)
        self.__button_list.append(self.__next_btn)

        self.__recommen_img = self.open_image(r"./Picture/CategoryPage/bt-rec.png", (300, 230))
        self.__recommen_btn = tk.Button(border=0, image=self.__recommen_img,
                                        height=50, width=300, bg="#FBF7EF",
                                        padx=5, pady=5, command=lambda: self.medication_page(canvas, 
                                                                                             self.__customer_management.create_recommendation(self.__customer)))
        self.__recommen_btn.place(x=350, y=700)
        self.__button_list.append(self.__recommen_btn)

    def category_page_2(self, canvas: tk.Canvas)    -> None:
        """This method create the category page 2 of the application. Where you can find the
        rest category of the medication."""
        self.__img_dict.clear()
        self.clear_previous_page(canvas)
        self.__bg_img = self.open_image(r"./Picture/CategoryPage2/BG-cate2.png", (0, 0))
        canvas.create_image(0, 0, anchor="nw", image=self.__bg_img)

        # Haematological button
        haemato__img = self.open_image(r"./Picture/CategoryPage2/haematological.png", (280, 230))
        self.__img_dict[7] = haemato__img

        # pain button
        pain_img = self.open_image(r"./Picture/CategoryPage2/pain.png", (280, 230))
        self.__img_dict[8] = pain_img

        # respiratory button
        respiratory_img = self.open_image(r"./Picture/CategoryPage2/respiratory.png", (280, 230))
        self.__img_dict[9] = respiratory_img

        # reproductive button
        reproductive_img = self.open_image(r"./Picture/CategoryPage2/reproductive.png", (280, 230))
        self.__img_dict[10] = reproductive_img

        # musculoskeletal button
        musculoskeletal_img = self.open_image(r"./Picture/CategoryPage2/musculoskeletal.png",
                                               (280, 230))
        self.__img_dict[11] = musculoskeletal_img

        # eyes button
        eyes_img = self.open_image(r"./Picture/CategoryPage2/eye.png", (280, 230))
        self.__img_dict[12] = eyes_img

        # previous button
        self.__prev_img = self.open_image(r"./Picture/CategoryPage/bt-back.png", (150, 120))
        self.__prev_btn = tk.Button(border=0, image=self.__prev_img,
                                    height=110, width=115, bg="#FBF7EF",
                                    padx=5, pady=5, command=lambda: self.category_page(canvas))
        self.__prev_btn.place(x=680, y=670)
        self.__button_list.append(self.__prev_btn)

        #next button
        self.__next_img = self.open_image(r"./Picture/CategoryPage/bt-next.png", (150, 120))
        self.__next_btn = tk.Button(border=0, image=self.__next_img,
                                    height=110, width=115, bg="#FBF7EF",
                                    padx=5, pady=5, command=lambda: self.category_page_3(canvas))
        self.__next_btn.place(x=800, y=670)
        self.__button_list.append(self.__next_btn)
        
        self.__recommen_img = self.open_image(r"./Picture/CategoryPage/bt-rec.png", (300, 230))
        self.__recommen_btn = tk.Button(border=0, image=self.__recommen_img,
                                        height=50, width=300, bg="#FBF7EF",
                                        padx=5, pady=5, command=lambda: self.medication_page(canvas, 
                                                                                             self.__customer_management.create_recommendation(self.__customer)))
        self.__recommen_btn.place(x=350, y=700)
        self.__button_list.append(self.__recommen_btn)
        
        self.category_template(canvas)
    
    def category_page_3(self, canvas: tk.Canvas)   -> None:
        self.__img_dict.clear()
        self.clear_previous_page(canvas)

        self.__bg_img = self.open_image(r"./Picture/CategoryPage2/BG-cate2.png", (0, 0))
        canvas.create_image(0, 0, anchor="nw", image=self.__bg_img)

        #other condition button
        other_condition_img = self.open_image(r"./Picture/CategoryPage3/Other.png", (280, 230))
        self.__img_dict[13] = other_condition_img
        # previous button
        self.__prev_img = self.open_image(r"./Picture/CategoryPage/bt-back.png", (150, 120))
        self.__prev_btn = tk.Button(border=0, image=self.__prev_img,
                                    height=110, width=115, bg="#FBF7EF",
                                    padx=5, pady=5, command=lambda: self.category_page_2(canvas))
        self.__prev_btn.place(x=730, y=670)
        self.__button_list.append(self.__prev_btn)

        self.__recommen_img = self.open_image(r"./Picture/CategoryPage/bt-rec.png", (300, 230))
        self.__recommen_btn = tk.Button(border=0, image=self.__recommen_img,
                                        height=50, width=300, bg="#FBF7EF",
                                        padx=5, pady=5, command=lambda: self.medication_page(canvas, 
                                                                                             self.__customer_management.create_recommendation(self.__customer)))
        self.__recommen_btn.place(x=350, y=700)
        self.__button_list.append(self.__recommen_btn)
        
        self.category_template(canvas)
    
    def template_page(self, canvas:tk.Canvas, category_name:list) -> None:
        """This method generates a template page for the pharmacy 
        application using a provided tkinter canvas and a list of category names. 
        The method creates a dictionary containing the x and y coordinates for the category buttons, 
        creates a back button, places a background image on the canvas, and creates buttons for each 
        category name in the list. The category buttons are given an image from a dictionary of images 
        and a command to call the medication_page method when clicked with the corresponding category name. 
        The method also adds all created buttons to a list of buttons for later use.

        Args:

        canvas: A tkinter Canvas object where the template page will be created.
        category_name: A list of strings containing the names of the categories to be displayed.
        Returns:

        None. The method only creates the template page on the provided canvas."""
        self.__pos_dict = {1:{"x":100, "y":180}, 2:{"x":100, "y":280},
                            3:{"x": 100, "y": 380}, 4:{"x": 100, "y": 480},
                           5:{"x": 500, "y": 180}, 6:{"x":500, "y": 280},
                             7:{"x": 500, "y": 380}, 8:{"x": 500, "y": 480},
                           9:{"x":300, "y":580}}
        prev_img = self.open_image("./Picture/Button/bt-back.png", (150, 120))
        self.__prev_btn = tk.Button(canvas, image=prev_img, height=110, width=115, border=0, bg="#F1E5CD",
                                    command=lambda: self.category_page(canvas))
        self.__prev_btn.place(x=780, y=590)
        self.__button_list.append(self.__prev_btn)
        canvas.create_image(0, 0, image=self.__img_dict["bg_img"], anchor="nw")
        for num in range(1, len(category_name)+1):
            self.__category_btn = f"category_btn{num}"
            self.__category_btn = tk.Button(canvas, image=self.__img_dict[num],  height=80, width=380, border=0, 
                                       padx=5, pady=5,
                                         bg="#F1E5CD",
                                         command=lambda n=num:self.medication_page(canvas,
                                                                                    category_name[n-1]))
            self.__category_btn.place(x=self.__pos_dict[num]["x"], y=self.__pos_dict[num]["y"])
            self.__button_list.append(self.__category_btn)

    def neurological_condi_page(self, canvas:tk.Canvas) -> None:
        """This function is to create neurological condition page"""
        self.clear_previous_page(canvas)

        self.__img_dict.clear()
        self.__category_list = ["Adhd", "Alzheimer", "Anxiety", "Depression",
                                 "Migraine", "Hypnosis", "Parkinson", "Psychosis", "Vertigo"]
        bg_img = self.open_image("./Picture/NeurologicalPage/BG-NEUROLOGICAL.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img

        adhd_img = self.open_image("./Picture/NeurologicalPage/ADHD.png", (400, 300))
        self.__img_dict[1] = adhd_img

        alzheimer_img = self.open_image("./Picture/NeurologicalPage/ALZHEIMER.png", (400, 300))
        self.__img_dict[2] = alzheimer_img

        anxiety_img = self.open_image("./Picture/NeurologicalPage/ANXIETY.png", (400, 300))
        self.__img_dict[3] = anxiety_img

        depression_img = self.open_image("./Picture/NeurologicalPage/DEPRESSION.png", (400, 300))
        self.__img_dict[4] = depression_img

        migrane_img = self.open_image("./Picture/NeurologicalPage/MIGRAINE.png", (400, 300))
        self.__img_dict[5] = migrane_img
        
        hypnosis_img = self.open_image("./Picture/NeurologicalPage/HYPNOSIS.png", (400, 300))
        self.__img_dict[6] = hypnosis_img

        parkinson_img = self.open_image("./Picture/NeurologicalPage/PAKINSON.png", (400, 300))
        self.__img_dict[7] = parkinson_img

        psychosis_img = self.open_image("./Picture/NeurologicalPage/PHYCHOSIS.png", (400, 300))
        self.__img_dict[8] = psychosis_img

        vertigo_img = self.open_image("./Picture/NeurologicalPage/VERTIGO.png", (400, 300))
        self.__img_dict[9] = vertigo_img
        
        self.template_page(canvas, self.__category_list)

    def allergies_condi_page(self, canvas: tk.Canvas) -> None:
        """This function is to create allergies page"""
        
        self.clear_previous_page(canvas)
        self.__img_dict.clear()
        self.__category_list = ["Allergies"]

        background_img = self.open_image("./Picture/AllergyPage/BG-ALLERGIES.png", (0, 0))
        self.__img_dict["bg_img"] = background_img

        allergies_img = self.open_image("./Picture/AllergyPage/ALLERGIES.png", (400, 300))
        self.__img_dict[1] = allergies_img

        self.template_page(canvas, self.__category_list)

    def skin_condi_page(self, canvas: tk.Canvas) -> None:
        """This function is to create skin condition page"""
        
        self.clear_previous_page(canvas)
        self.__img_dict.clear()

        bg_img = self.open_image("./Picture/SkinPage/BG-skincondition.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img

        self.__category_list = ["Acne", "Cleanser", "Dandruff", "Hyperpigmentation", "Scabies", "Wound"]

        acne_img = self.open_image("./Picture/SkinPage/ACEN.png", (400, 300))
        self.__img_dict[1] = acne_img

        cleanser_img = self.open_image("./Picture/SkinPage/CLEANSER.png", (400, 300))
        self.__img_dict[2] = cleanser_img

        dandruff_img = self.open_image("./Picture/SkinPage/DANDRUFF.png", (400, 300))
        self.__img_dict[3] = dandruff_img

        hyperpigmentation_img = self.open_image("./Picture/SkinPage/HYPERPINMENTATION.png", (400, 300))
        self.__img_dict[4] = hyperpigmentation_img

        scabies_img = self.open_image("./Picture/SkinPage/SCABIES.png", (400, 300))
        self.__img_dict[5] = scabies_img

        wound_img = self.open_image("./Picture/SkinPage/WOUND.png", (400, 300))
        self.__img_dict[6] = wound_img

        self.template_page(canvas, self.__category_list)
    
    def cardio_condi_page(self, canvas) -> None:
        """This function is to create cardiovascular condition page"""
        self.clear_previous_page(canvas)
        self.__img_dict.clear()

        bg_img = self.open_image("./Picture/CardioPage/BG-CARDIOVACULAR.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img

        self.__category_list = ["Angina", "Arrhythmiasis", "Hypertension", "Hyperthyroidism", "Thrombolysis"]

        angina_img = self.open_image("./Picture/CardioPage/ANGINA.png", (400, 300))
        self.__img_dict[1] = angina_img

        arrhythmiasis_img = self.open_image("./Picture/CardioPage/ARRHYTHMIASIS.png", (400, 300))
        self.__img_dict[2] = arrhythmiasis_img

        hypertension_img = self.open_image("./Picture/CardioPage/HYPERTENSION.png", (400, 300))
        self.__img_dict[3] = hypertension_img

        hyperthyroidism_img = self.open_image("./Picture/CardioPage/HYPERTHYROIDISM.png", (400, 300))
        self.__img_dict[4] = hyperthyroidism_img

        thrombolysis_img = self.open_image("./Picture/CardioPage/THROMBOLYSIS.png", (400, 300))
        self.__img_dict[5] = thrombolysis_img

        self.template_page(canvas, self.__category_list)
    
    def endocrine_condi_page(self, canvas: tk.Canvas) -> None:
        """This function is to create endocrine condition page"""
        self.clear_previous_page(canvas)
        self.__img_dict.clear()

        bg_img = self.open_image("./Picture/EndocrinePage/BG-ENDOCRINE.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img

        self.__category_list = ["Diabetes", "Hypothyroidism", "Hyperthyroidism"]

        diabetes_img = self.open_image("./Picture/EndocrinePage/DIABETES.png", (400, 300))
        self.__img_dict[1] = diabetes_img

        hypothyroidism_img = self.open_image("./Picture/EndocrinePage/HYPOTHYROIDISM.png", (400, 300))
        self.__img_dict[2] = hypothyroidism_img

        hyperthyroidism_img = self.open_image("./Picture/EndocrinePage/HYPERTHYROIDISM.png", (400, 300))
        self.__img_dict[3] = hyperthyroidism_img

        self.template_page(canvas, self.__category_list)

    def infection_condi_page(self, canvas:tk.Canvas) -> None:
        """This function is to create infection condition page"""
        self.clear_previous_page(canvas)
        self.__img_dict.clear()

        bg_img = self.open_image("./Picture/InfectionPage/BG-INFECTION DISEASES.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img

        self.__category_list = ["Amoebiasis", "Infection", "Leprosy", "Malarial", "Viral"]

        amoebiasis_img = self.open_image("./Picture/InfectionPage/AMOEBIASIS.png", (400, 300))
        self.__img_dict[1] = amoebiasis_img

        infection_img = self.open_image("./Picture/InfectionPage/INFECTION.png", (400, 300))
        self.__img_dict[2] = infection_img

        leprosy_img = self.open_image("./Picture/InfectionPage/LEPROSY.png", (400, 300))
        self.__img_dict[3] = leprosy_img

        malarial_img = self.open_image("./Picture/InfectionPage/MALARIAL.png", (400, 300))
        self.__img_dict[4] = malarial_img

        viral_img = self.open_image("./Picture/InfectionPage/VIRAL.png", (400, 300))
        self.__img_dict[5] = viral_img

        self.template_page(canvas, self.__category_list)

    def haemoto_condi_page(self, canvas:tk.Canvas) -> None:
        """This function is to create haematological condition page"""
        self.clear_previous_page(canvas)
        self.__img_dict.clear()

        bg_img = self.open_image("./Picture/HaemotologyPage/BG-HAEMOTOLOGY.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img

        self.__category_list = ["Haematopoiesis", "Anaemia"]

        haematopoiesis_img = self.open_image("./Picture/HaemotologyPage/HAEMATOPOIESIS.png", (400, 300))
        self.__img_dict[1] = haematopoiesis_img

        anaemia_img = self.open_image("./Picture/HaemotologyPage/VIRAL.png", (400, 300))
        self.__img_dict[2] = anaemia_img

        self.template_page(canvas, self.__category_list)

    def pain_condi_page(self, canvas:tk.Canvas) -> None:
        """This function is to create pain condition page"""
        self.clear_previous_page(canvas)
        self.__img_dict.clear()

        bg_img = self.open_image("./Picture/PainPage/BG-PAIN.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img

        self.__category_list = ["Pain"]

        pain_img = self.open_image("./Picture/PainPage/PAIN.png", (400, 300))
        self.__img_dict[1] = pain_img

        self.template_page(canvas, self.__category_list)
    
    def respiratory_condi_page(self, canvas:tk.Canvas) -> None:
        """This method is to create respiratory condition page"""
        self.clear_previous_page(canvas)
        self.__img_dict.clear()

        bg_img = self.open_image("./Picture/RespiratoryPage/BG-RESPIRATORY.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img

        self.__category_list = ["General"]

        general_img = self.open_image("./Picture/RespiratoryPage/GENERAL.png", (300, 200))
        self.__img_dict[1] = general_img

        self.template_page(canvas, self.__category_list)

    def reproductive_condi_page(self, canvas:tk.Canvas) -> None:
        """This method is to create reproductive condition page"""
        self.clear_previous_page(canvas)
        self.__img_dict.clear()

        bg_img = self.open_image("./Picture/ReproductivePage/BG-REPRODUCTIVE.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img

        self.__category_list = ["Contraception"]

        general_img = self.open_image("./Picture/ReproductivePage/CONTRACEPTION.png", (400, 300))
        self.__img_dict[1] = general_img

        self.template_page(canvas, self.__category_list)
    
    def muscoloskeletal_condi_page(self, canvas:tk.Canvas) -> None:
        """This method is to create muscoloskeletal condition page"""
        self.clear_previous_page(canvas)
        self.__img_dict.clear()

        bg_img = self.open_image(r"./Picture/MuscoloskeletalPage/BGMUSCOLOSKELETAL.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img

        self.__category_list = ["Gout", "Osteoporosis", "Arthritis"]

        gout_img = self.open_image(r"./Picture/MuscoloskeletalPage/GOUT.png", (400, 300))
        self.__img_dict[1] = gout_img

        osteoporosis_img = self.open_image(r"./Picture/MuscoloskeletalPage/OSTEOPOROSIS.png", (400, 300))
        self.__img_dict[2] = osteoporosis_img

        arthritis_img = self.open_image(r"./Picture/MuscoloskeletalPage/ARTHRITIS.png", (400, 300))
        self.__img_dict[3] = arthritis_img

        self.template_page(canvas, self.__category_list)

    def eyes_condition_page(self, canvas:tk.Canvas) -> None:
        """This method is to create eyes condition page"""
        self.clear_previous_page(canvas)    
        self.__img_dict.clear()

        bg_img = self.open_image(r"./Picture/EyesPage/BG-EYES.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img

        self.__category_list = ["Glaucoma", "Mydriasis"]

        glaucoma_img = self.open_image(r"./Picture/EyesPage/GLAUCOMA.png", (400, 300))
        self.__img_dict[1] = glaucoma_img

        mydriasis_img = self.open_image(r"./Picture/EyesPage/MYDRIASIS.png", (400, 300))
        self.__img_dict[2] = mydriasis_img

        self.template_page(canvas, self.__category_list)

    def others_condi_page(self, canvas:tk.Canvas) -> None:
        """This method is to create others condition page for symptom such as fever, fungal etc."""
        self.clear_previous_page(canvas)
        self.__img_dict.clear()

        bg_img = self.open_image(r"./Picture/OthersPage/BG-OTHERS.png", (0, 0))
        self.__img_dict["bg_img"] = bg_img
        
        self.__category_list = ["Fever", "Fungal", "Haemorrhoid",
                                 "Schizophrenia", "Smoking", "Supplement",
                                 "Vaccines"]
        
        fever_img = self.open_image(r"./Picture/OthersPage/FEVER.png", (400, 300))
        self.__img_dict[1] = fever_img

        fungal_img = self.open_image(r"./Picture/OthersPage/FUNGAL.png", (400, 300))
        self.__img_dict[2] = fungal_img

        haemorrhoid_img = self.open_image(r"./Picture/OthersPage/HAEMORRHOID.png", (400, 300))
        self.__img_dict[3] = haemorrhoid_img

        schizophrenia_img = self.open_image(r"./Picture/OthersPage/SCHIZOPHRENIA.png", (400, 300))
        self.__img_dict[4] = schizophrenia_img

        smoking_img = self.open_image(r"./Picture/OthersPage/SMOKING.png", (400, 300))
        self.__img_dict[5] = smoking_img

        supplement_img = self.open_image(r"./Picture/OthersPage/SUPPLEMENT.png", (400, 300))
        self.__img_dict[6] = supplement_img

        vaccines_img = self.open_image(r"./Picture/OthersPage/VACCINES.png", (400, 300))
        self.__img_dict[7] = vaccines_img

        self.template_page(canvas, self.__category_list)

    def confirmed_order_page(self, med_name:str, med_des:str, med_cate:str) -> None:
        """This method creates a new window to confirm the customer's order. 
        It takes in the medication name, description, and category as arguments and allows the user to 
        input the quantity they want to order. Once the order is confirmed by the user, the method saves 
        the order information and displays a success message.

        Args:

        med_name (str): The name of the medication being ordered.
        med_des (str): The description of the medication being ordered.
        med_cate (str): The category of the medication being ordered.
        Returns:

        None. This method does not return anything. However, it saves the order information and displays a success message."""
        llist = []
        order_window = Toplevel()
        order_window.title("Confirm Order")

        # Add the medication name and description to the window
        med_label = tk.Label(order_window, text=f"Medication Name: {med_name}")
        med_label.pack()
        des_label = tk.Label(order_window, text=f"Description: {med_des}")
        des_label.pack()

        qty_label = tk.Label(order_window, text="Quantity:")
        qty_label.pack()
        qty_entry = tk.Entry(order_window)
        qty_entry.pack()

        def submit_order():
            qty = int(qty_entry.get())
            if qty > 10:
                messagebox.showerror("Error", "The maximum quantity is 10")
                order_window.destroy()
                return
            date_str = datetime.now().strftime("%Y-%m-%d")
            # Create a dictionary with the order information
            order = {
                "Customer Name": self.__customer.name,
                "Medication Name": med_name,
                "Medication Category": med_cate,
                "Quantity": qty,
                "Address": self.__customer.address,
                "Date": date_str
            }
            llist.append(order)
            self.__order_repo.save_data(llist)
            messagebox.showinfo("Success", "Order has been placed")
            order_window.destroy()

        submit_button = tk.Button(order_window, text="Submit", command=submit_order)
        submit_button.pack()
        