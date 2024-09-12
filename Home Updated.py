import customtkinter 
from CTkMessagebox import CTkMessagebox
import webbrowser
import tkinter
import os
from PIL import Image
import pyodbc
import pandas as pd
import customtkinter
from datetime import datetime
from PIL import Image, ImageTk
import tkinter as tk

login_successful = False
current_page = "home"

def return_to_previous_page():
    global current_page
    if current_page == "registration":
        if rt:
            rt.destroy()
        # Show the login page
        show_login()


def cafe():
    global login_successful, cur, conn, item_frame, entry, prices, item_descriptions, item_images, cart 
    if login_successful:
            
        cafe = customtkinter.CTkToplevel()
        cafe.geometry(f"{1100}x580")

            # Initialize database
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
        cur = conn.cursor()
        

            #Banner
        cafe_banner_path = "cafe_banner.png"
        banner_height = 150  
        cafe_banner = customtkinter.CTkImage(dark_image=Image.open(cafe_banner_path), size=(1780, banner_height))
        cafe_banner_label = customtkinter.CTkLabel(cafe, image=cafe_banner, text="")
        cafe_banner_label.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10)

                    
            # Sidebar frame
        sidebar_frame = customtkinter.CTkFrame(cafe, width=140, corner_radius=0)
        sidebar_frame.grid(row=1, column=0, rowspan=3, sticky="nsew")
        sidebar_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        categories = ["Main Menu", "Breakfast", "Lunch", "Snacks", "Beverages", "View Cart"]
        for i, category in enumerate(categories):
            category_button = customtkinter.CTkButton(sidebar_frame, width=180, height=40, text=category,
                                            command=lambda cat=category: show_category(cat))
            category_button.grid(row=i, column=0, padx=1, pady=10)

            # create main entry
            entry = customtkinter.CTkEntry(cafe, placeholder_text="Search")
            entry.grid(row=1, column=1, columnspan=1, padx=(10, 0), pady=(20, 20), sticky="nsew")
            entry.bind("<Return>", lambda event: search_items())

            # User balance
            balance = get_balance_from_db()

            # Balance label
            balance_label = customtkinter.CTkLabel(cafe, text=f"Balance: ${balance:.2f}", font=("Arial", 12))
            balance_label.grid(row=1, column=3, padx=10, pady=10, sticky="ne")

            # Item frame
            item_frame = customtkinter.CTkFrame(cafe, width=900, height=500, bg_color="black")
            item_frame.grid(row=3, column=1, rowspan=3, padx=10, pady=10)
            item_frame.grid_propagate(False)  # Prevent item frame from resizing based on its content

            cart = get_cart_from_db()



            
            # Item descriptions
            item_descriptions = {
                "Journey Cake": "A journey cake is a staple Belizean food item most eaten for breakfast. At Cait’s Oasis, the journey cake is served warm every morning with a slice of cheese inside.",
                "Pancake": "Delicious pancake served daily with Ham and Cheese filling.",
                "Stuff Jack (Beans)": "Golden brown stuffed jack with beans and happy cow cheese filling.",
                "Stuff Jack (Meat)": "Golden brown stuffed jack with ground chicken.",
                "Nachos": "Canned nacho cheese dip with chips and ground chicken.",
                "Burger": "Burger with chicken patty.",
                "Pizza": "Half pita bread pizza with tomato sauce, cheese, and pepperoni.",
                "Special (The café offers different special items each day)": "SCA Special changes each day. Kindly drop by the café to view today’s special!",
                "$1.50 Chips": "Cait’s Oasis has a variety of different chip brands and flavors. Choose your chip option upon pickup.",
                "$1.50 Biscuits": "Cait’s Oasis has a variety of different biscuit / cookie brands and flavors. Choose your biscuit option upon pickup.",
                "Skittles": "Colorful, bite-sized candies with a hard shell and a chewy center.",
                "Welches": "Fruit snack gummies made with real fruits!",
                "Coca-Cola": "Flavored carbonated beverage.",
                "Caribbean Pride": "Natural fruit juice. Choose flavor option upon arrival.",
                "Yogurt": "LALA strawberry flavored yogurt."
            }

            # Item prices
            prices = {
                "Journey Cake": 1,
                "Pancake": 2.5,
                "Stuff Jack (Beans)": 2,
                "Stuff Jack (Meat)": 2,
                "Nachos": 4,
                "Burger": 5,
                "Pizza": 3,
                "Special (The café offers different special items each day)": 8,
                "$1.50 Chips": 1.5,
                "$1.50 Biscuits": 1.5,
                "Skittles": 1,
                "Welches": 3.5,
                "Coca-Cola": 2,
                "Caribbean Pride": 1.5,
                "Yogurt": 2
            }

            # Item images
            item_images = {
                "Journey Cake": "journey_cake.png",
                "Pancake": "pancake.png",
                "Stuff Jack (Beans)": "stuff_jack_beans.png",
                "Stuff Jack (Meat)": "stuff_jack_meat.png",
                "Nachos": "nachos.png",
                "Burger": "burger.png",
                "Pizza": "pizza.png",
                "Special (The café offers different special items each day)": "special.png",
                "$1.50 Chips": "chips.png",
                "$1.50 Biscuits": "biscuits.png",
                "Skittles": "skittles.png",
                "Welches": "welches.png",
                "Coca-Cola": "coke.png",
                "Caribbean Pride": "caribbeanpride.png",
                "Yogurt": "yogurt.png"
            }

           
            # Checkout button
            checkout_button = customtkinter.CTkButton(cafe, text="Top Up Card", command=checkout)
            checkout_button.grid(row=1, column=3, padx=10, pady=10, sticky="se")

            # Cash Out
            cashout_button = customtkinter.CTkButton(cafe, text="Cash Out", command=cashout)
            cashout_button.grid(row=2, column=3, padx=10, pady=10, sticky="se")


            # Show Main Menu by default
            show_category("Main Menu")
        else:
            CTkMessagebox(title="Error", message="Please login first.")

                

def get_balance_from_db():
                        global item_frame, entry, prices, item_descriptions, item_images, cart
                        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
                        cur = conn.cursor()
                        cur.execute("SELECT balance FROM balance WHERE id = 1")
                        result = cur.fetchone()
                        if result:
                            return result[0]
                        else:
                            cur.execute("INSERT INTO balance (balance) VALUES (?)", (25.00,))
                            conn.commit()
                            return 25.00

def get_cart_from_db():
                        global item_frame, entry, prices, item_descriptions, item_images, cart
                        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
                        cur = conn.cursor()
                        cur.execute("SELECT item, price FROM cart")
                        return cur.fetchall()

def add_to_cart(item, price):
                        global item_frame, entry,prices, item_descriptions, item_images, cart
                        cart.append((item, price))
                        execute("INSERT INTO cart (item, price) VALUES (?, ?)", (item, price))
                        conn.commit()

def remove_from_cart(idx):
                        global item_frame, entry, prices, item_descriptions, item_images, cart
                        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
                        cur = conn.cursor()
                        del cart[idx]
                        cur.execute("DELETE FROM cart WHERE id = ?", (idx+1,))
                        conn.commit()
                        show_cart()  # Refresh the cart view after removing item

def checkout():
                        global item_frame, entry, prices, item_descriptions, item_images, cart
                        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ= C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
                        cur = conn.cursor()
                        # Open the checkout page in the web browser
                        checkout_url = "https://www.livedigi.com/topup-online"
                        webbrowser.open(checkout_url)

                        # Generate bill and reset cart
                        if cart:
                            bill_text = "Date: {}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            total_price = 0
                            for item, price in cart:
                                bill_text += f"{item} - ${price:.2f}\n"
                                total_price += price
                            bill_text += "\nTotal: ${:.2f}".format(total_price)

                            # Save bill to file or print
                            with open("bill.txt", "w") as file:
                                file.write(bill_text)

                            # Reset cart
                            cart = []
                            cur.execute("DELETE FROM cart")
                            conn.commit()
                            show_cart()
                            
def cashout():
                        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
                        cur = conn.cursor()
                        global item_frame, entry, prices, item_descriptions, item_images, cart
                        # Generate bill
                        if cart:
                            bill_text = "Date: {}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            total_price = 0
                            for item, price in cart:
                                bill_text += f"{item} - ${price:.2f}\n"
                                total_price += price
                            bill_text += "\nTotal: ${:.2f}".format(total_price)

                            # Save bill to file
                            with open("bill.txt", "w") as file:
                                file.write(bill_text)

                            # Clear cart
                            cart = []
                            cur.execute("DELETE FROM cart")
                            conn.commit()
                    

def search_items():
                        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
                        cur = conn.cursor()
                        global item_frame, entry, prices, item_descriptions, item_images, cart
                        search_query = entry.get().strip().lower()
                        found = False

                        for item in prices:
                            if search_query in item.lower():
                                found = True
                                break

                        if found:
                            show_category("Search")
                        else:
                            # No matching items found, keep the item frame unchanged
                            pass

def show_category(category):
                        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
                        cur = conn.cursor()
                        global item_frame, entry, prices, item_descriptions, item_images, cart
                        # Clear the item frame
                        for widget in item_frame.winfo_children():
                            widget.destroy()

                        search_query = entry.get().strip().lower()
                        filtered_items = []

                        if search_query:
                            # Filter items based on search query
                            for item in prices:
                                if search_query in item.lower():
                                    filtered_items.append(item)
                        else:
                            # If no search query, show all items in the category
                            if category == "Main Menu":
                                filtered_items = ["Journey Cake", "Pancake", "Stuff Jack (Beans)", "Stuff Jack (Meat)", "Nachos", "Burger", "Pizza", "Special (The café offers different special items each day)",
                                         "$1.50 Chips", "$1.50 Biscuits", "Mamut", "Welches", "Coca-Cola", "Caribbean Pride", "Yogurt"]
                            elif category == "Breakfast":
                                filtered_items = ["Journey Cake", "Pancake", "Stuff Jack (Beans)", "Stuff Jack (Meat)"]
                            elif category == "Lunch":
                                filtered_items = ["Nachos", "Burger", "Pizza", "Special (The café offers different special items each day)"]
                            elif category == "Snacks":
                                filtered_items = ["$1.50 Chips", "$1.50 Biscuits", "Mamut", "Welches"]
                            elif category == "Beverages":
                                filtered_items = ["Coca-Cola", "Caribbean Pride", "Yogurt"]
                            elif category == "View Cart":
                                show_cart()

                        # Display filtered items and descriptions
                        placeholder_image = Image.open("pizza.png")
                        placeholder_image = placeholder_image.resize((100, 100), Image.LANCZOS)

                        for i, item in enumerate(filtered_items):
                            price = prices.get(item, 0)
                            item_image_path = item_images.get(item, "pizza.png")
                            item_image = Image.open(item_image_path)
                            item_image = item_image.resize((100, 100), Image.LANCZOS)

                            # Convert PIL Image to CTkImage
                            item_image = ImageTk.PhotoImage(item_image)

                            item_button = customtkinter.CTkButton(item_frame, text=f"{item} - ${price:.2f}", image=item_image, compound="left", width=30,
                                                     command=lambda it=item, pr=price: add_to_cart(it, pr))
                            item_button.grid(row=i+1, column=0, padx=10, pady=5)

                            # Display descriptions in columns 2-3
                            if item in item_descriptions:
                                description_label = customtkinter.CTkLabel(item_frame, text=item_descriptions[item], wraplength=300)
                                description_label.grid(row=i+1, column=1, columnspan=2, padx=10, pady=5, sticky="w")

def show_cart():
                        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
                        cur = conn.cursor()
                        global item_frame, entry, prices, item_descriptions, item_images, cart
                        # Clear the item frame
                        for widget in item_frame.winfo_children():
                            widget.destroy()

                        total_price = 0
                        for i, (item, price) in enumerate(cart):
                            item_label = customtkinter.CTkLabel(item_frame, text=f"{item} - ${price:.2f}", width=30)
                            item_label.grid(row=i, column=0, padx=10, pady=5)
                            total_price += price

                            # Add remove button for each item
                            remove_button = customtkinter.CTkButton(item_frame, text="Remove", width=10,
                                                       command=lambda idx=i: remove_from_cart(idx))
                            remove_button.grid(row=i, column=1, padx=10, pady=5)

                        # Display total price
                        total_label = customtkinter.CTkLabel(item_frame, text=f"Total: ${total_price:.2f}", width=30)
                        total_label.grid(row=len(cart), column=0, columnspan=2, padx=10, pady=5)

def __del__():
            conn.close()

#LOGIN
def show_login():
    global rt
    global current_page
    current_page = "login"
    try:
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
        cursor = conn.cursor()
        
        customtkinter.set_default_color_theme("dark-blue")

        rt = customtkinter.CTk()
        rt.geometry(f"{1100}x{580}")

        login_window = None  # Variable to store the login window reference

        def insert_data():
            global conn, cursor, password_entry, name_entry, username_entry, role_entry
            conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
            cursor = conn.cursor()
            
            password = password_entry.get()
            name = name_entry.get()
            username = username_entry.get()
            role = role_entry.get()
            if not name or not password or not username:
                CTkMessagebox(title="Error", message="Please fill in all fields")
                return
            try:
                if conn is None or conn.closed:
                    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
                    cursor = conn.cursor()
            
                cursor.execute("INSERT INTO User_Data (Password, FullName, UserName, Role) VALUES (?, ?, ?, ?)", password, name, username,role)
                conn.commit()
                CTkMessagebox(title="Success", message="Data inserted successfully")
            except pyodbc.Error as e:
                print("Error inserting data:", e)

            except pyodbc.Error as e:
                sql_state = e.args[0].sqlstate
                error_message = e.args[0].message
                print(f"Error inserting data: {sql_state} - {error_message}")
            finally:
            # Close the cursor if it's open
                if cursor is not None:
                   cursor.close()

                password_entry.delete(0, customtkinter.END)
                name_entry.delete(0, customtkinter.END)
                username_entry.delete(0, customtkinter.END)
                role_entry.set("Select a role")
                        

        def clear_form():
            password_entry.delete(0, customtkinter.END)
            name_entry.delete(0, customtkinter.END)
            username_entry.delete(0, customtkinter.END)
            role_entry.set("Select a role")

        def close_login_window():
            global login_window
            if login_window:
                login_window.destroy()

        def reg():
            global name_entry, username_entry, password_entry, role_entry
            global current_page
            current_page = "registration"
            close_login_window()  # Close the login window
            reg = customtkinter.CTk()
            reg.geometry(f"{1920}x{1080}")
            global rt
            fr = customtkinter.CTkFrame(master=rt)
            fr.pack(pady=40, padx=120, fill="both", expand=True)
            
            label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="Register System", font=("Roboto", 24))
            label.pack(pady=12, padx=10)
            
            name_entry = customtkinter.CTkEntry(master=fr, width=240, height=32, placeholder_text="Full name")
            name_entry.pack(pady=12, padx=10)
            
            username_entry = customtkinter.CTkEntry(master=fr, width=240, height=32, placeholder_text="School Email")
            username_entry.pack(pady=12, padx=10)
            
            password_entry = customtkinter.CTkEntry(master=fr, width=240, height=32, placeholder_text="Password", show="*")
            password_entry.pack(pady=12, padx=10)

            role_entry = customtkinter.CTkComboBox(fr, values=["Student", "Teacher", "Staff", "Admin"])
            role_entry.pack(pady=12, padx=10)
            role_entry.set("Select a role")
                      
            checkbox = customtkinter.CTkCheckBox(master=fr, text="Remember me")
            checkbox.pack(pady=12, padx=10)
            
            button = customtkinter.CTkButton(master=fr, width=240, height=32, text="Register", command=insert_data)
            button.pack(pady=12, padx=10)
                        
            clear_button = customtkinter.CTkButton(master=fr, width=240, height=25, fg_color= "transparent", text="Clear", command=clear_form)
            clear_button.pack(pady=12, padx=10)

            return_button = customtkinter.CTkButton(master=fr, width=240, height=32, text="<-Back to previous page", command=return_to_previous_page)
            return_button.pack(pady=2, padx=10)

            
            rt.mainloop()

        def login_check():
            global conn, cursor, entry1, entry2, role_label
            conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
            cursor = conn.cursor()
            
            username = entry1.get()  # Assuming entry1 is the username entry widget
            password = entry2.get()# Assuming entry2 is the password entry widget
            role = role_label.get()

            try:
                if conn is None or conn.closed:
                    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
                    cursor = conn.cursor()
            
                query = "SELECT * FROM User_Data WHERE UserName = ? AND Password = ? AND Role = ?"
                cursor.execute(query, (username, password, role))
                row = cursor.fetchone()  # Fetch the first matching row
            
                if row:
                    CTkMessagebox(title="Success", message="Login Successful")
                    global login_successful
                    login_successful = True
                else:
                    CTkMessagebox(title="Error", message="Invalid email or password")
            except pyodbc.Error as e:
                print("Error checking login:", e)
            finally:
            # Close the cursor and connection if they're open
                if cursor is not None:
                    cursor.close()
                if conn is not None:
                    conn.close()

     

        def login():
            global login_window, entry1, entry2, role_label
            login_window = customtkinter.CTk()
            login_window.geometry(f"{1920}x{1080}")
            
            fr = customtkinter.CTkFrame(master=login_window)
            fr.pack(pady=40, padx=120, fill="both", expand=True)
            
            label = customtkinter.CTkLabel(master=fr, width=120, height=32, text="Login System", font=("Roboto", 24))
            label.pack(pady=12, padx=10)
            
            entry1 = customtkinter.CTkEntry(master=fr, width=240, height=32, placeholder_text="Email")
            entry1.pack(pady=12, padx=10)
            
            entry2 = customtkinter.CTkEntry(master=fr, width=240, height=32, placeholder_text="Password", show="*")
            entry2.pack(pady=12, padx=10)
                
            role_label = customtkinter.CTkComboBox(fr, values=["Student", "Teacher", "Staff", "Admin"])
            role_label.pack(pady=12, padx=10)
            role_label.set("Select a role")

            checkbox = customtkinter.CTkCheckBox(master=fr, text="Remember me")
            checkbox.pack(pady=10, padx=10)

            button = customtkinter.CTkButton(master=fr, width=240, height=32, text="Login", command=login_check)
            button.pack(pady=2, padx=10)

            clear_button = customtkinter.CTkButton(master=fr, width=240, height=25, text="Clear", command=clear_form)
            clear_button.pack(pady=12, padx=10)
           
            label1 = customtkinter.CTkLabel(master=fr, width=120, height=2, text="Do not have an account?", font=("Roboto",12))
            label1.pack(pady=10, padx=10)
            
            button2 = customtkinter.CTkButton(master=fr, width=240, height=25, text="Register", command=reg)
            button2.pack(pady=2, padx=10)

          
            login_window.mainloop()

        for i in cursor.tables(tableType="TABLE"):
            print(i.table_name)
        df = pd.read_sql("SELECT * FROM User_Data", conn)
        print(df)

    except pyodbc.Error as e:
        print("Error connecting to database:", e)
    finally:
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\amber\OneDrive\Documents\Group1_SCA_Cafeteria_App.zip\Group1_SCA_Cafeteria_App\Cafe.accdb;')
        cursor = conn.cursor()
        conn.close()

    login()

class App(customtkinter.CTk):
    def __init__(app):
        super().__init__()
        app.title("The SCA App")
        app.geometry(f"{1920}x{1080}")
        global current_page
        current_page = "home"
        

        app.grid_columnconfigure(1, weight=1)
        app.grid_columnconfigure((2, 3), weight=0)
        app.grid_rowconfigure((0, 1, 2), weight=1)

        app.sidebar_frame = customtkinter.CTkFrame(app, width=140, corner_radius=0)
        app.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        app.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        login_button = customtkinter.CTkButton(app.sidebar_frame,width = 180, height = 40, text = "Login",command = show_login )
        login_button.grid(row =2, column = 0, padx = 1, pady=10)

        
        cafe_button = customtkinter.CTkButton(app.sidebar_frame,width = 180, height = 40, text = "Cafeteria",command = cafe )
        cafe_button.grid(row =3, column = 0, padx = 10, pady=10)
        
        appearance_mode_label = customtkinter.CTkLabel(app.sidebar_frame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        appearance_mode_optionemenu = customtkinter.CTkOptionMenu(app.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=app.change_appearance_mode_event)
        appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        scaling_label = customtkinter.CTkLabel(app.sidebar_frame, text="UI Scaling:", anchor="w")
        scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        scaling_optionemenu = customtkinter.CTkOptionMenu(app.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=app.change_scaling_event)
        scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        app.load_logo()
                
        
        frame = customtkinter.CTkFrame(app,border_width= 1,fg_color = "transparent")
        frame.grid(row=2, column=1, padx=10)

        abacus_button= customtkinter.CTkButton(frame, width = 180, height = 40, text = "Abacus", command = lambda :  webbrowser. open("sca.abacus.bz") )
        abacus_button.grid(row =1, column = 2, padx = 10,pady=10)

        website_button = customtkinter.CTkButton(frame,width = 180, height = 40, text = "SCA's Website", command = lambda :  webbrowser. open("sca.edu.bz") )
        website_button.grid(row =0, column = 2, padx = 10,pady=10)
    
        FB_button =customtkinter.CTkButton(frame,width = 180, height = 40, text = "SCA's Facebook", command = lambda :  webbrowser. open("https://www.facebook.com/SCAHighSchoolBelize/") )
        FB_button.grid(row =0, column = 1, padx = 10,pady=10)

        SC_button =customtkinter.CTkButton(frame,width = 180, height = 40, text = "SCA's Student Council", command = lambda :  webbrowser. open("https://www.instagram.com/_scacouncil_/?hl=en'") )
        SC_button.grid(row =1, column = 1, padx = 10,pady=10)


        
    def load_logo(app):
        global banner_path
        banner_path = "scagallery.png"
        original_image = Image.open(banner_path)
        
            
        app.banner = customtkinter.CTkImage(dark_image=Image.open(banner_path),size=(1780, 850))
        app.banner_label = customtkinter.CTkLabel(app, image=app.banner, text="")
        app.banner_label.grid(row=0, column=1, rowspan=4, columnspan=4, sticky="nsew", padx=10)

                
    def open_input_dialog_event(app):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(app, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(app, new_scaling: str):
        global banner_path
        app.banner = customtkinter.CTkImage(dark_image=Image.open(banner_path),size=(1780, 850))
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(app):
        print("sidebar_button click")

        

        


if __name__ == "__main__":
    app1 = App()
    app1.mainloop()



