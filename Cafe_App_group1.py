import webbrowser
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk
import customtkinter
import tkinter as tk

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("The SCA Cafeteria")
        self.geometry(f"{1100}x580")

        # Initialize database
        self.conn = sqlite3.connect('sca_app.db')
        self.cur = self.conn.cursor()
        self.create_tables()

        # Initialize UI
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        #Banner
        cafe_banner_path = "cafe_banner.png"
        banner_height = 150  
        self.cafe_banner = customtkinter.CTkImage(dark_image=Image.open(cafe_banner_path), size=(1780, banner_height))
        self.cafe_banner_label = customtkinter.CTkLabel(self, image=self.cafe_banner, text="")
        self.cafe_banner_label.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10)

                
        # Sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=1, column=0, rowspan=3, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        self.categories = ["Main Menu", "Breakfast", "Lunch", "Snacks", "Beverages", "View Cart"]
        for i, category in enumerate(self.categories):
            category_button = customtkinter.CTkButton(self.sidebar_frame, width=180, height=40, text=category,
                                        command=lambda cat=category: self.show_category(cat))
            category_button.grid(row=i, column=0, padx=1, pady=10)

        # create main entry
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Search")
        self.entry.grid(row=1, column=1, columnspan=1, padx=(10, 0), pady=(20, 20), sticky="nsew")
        self.entry.bind("<Return>", lambda event: self.search_items())

        # User balance
        self.balance = self.get_balance_from_db()

        # Balance label
        self.balance_label = customtkinter.CTkLabel(self, text=f"Balance: ${self.balance:.2f}", font=("Arial", 12))
        self.balance_label.grid(row=1, column=3, padx=10, pady=10, sticky="ne")

        # Item frame
        self.item_frame = customtkinter.CTkFrame(self, width=900, height=500, bg_color="black")
        self.item_frame.grid(row=3, column=1, rowspan=3, padx=10, pady=10)
        self.item_frame.grid_propagate(False)  # Prevent item frame from resizing based on its content

        self.cart = self.get_cart_from_db()



        
        # Item descriptions
        self.item_descriptions = {
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
        self.prices = {
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
        self.item_images = {
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
        self.checkout_button = customtkinter.CTkButton(self, text="Top Up Card", command=self.checkout)
        self.checkout_button.grid(row=1, column=3, padx=10, pady=10, sticky="se")

        # Cash Out
        self.cashout_button = customtkinter.CTkButton(self, text="Cash Out", command=self.cashout)
        self.cashout_button.grid(row=2, column=3, padx=10, pady=10, sticky="se")


        # Show Main Menu by default
        self.show_category("Main Menu")

    def create_tables(self):
        # Create tables if not exist
        self.cur.execute('''CREATE TABLE IF NOT EXISTS cart (
                            id INTEGER PRIMARY KEY,
                            item TEXT,
                            price REAL
                            )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS balance (
                            id INTEGER PRIMARY KEY,
                            balance REAL
                            )''')
        self.conn.commit()

    def get_balance_from_db(self):
        self.cur.execute('''SELECT balance FROM balance WHERE id = 1''')
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            self.cur.execute('''INSERT INTO balance (balance) VALUES (?)''', (25.00,))
            self.conn.commit()
            return 25.00

    def get_cart_from_db(self):
        self.cur.execute('''SELECT item, price FROM cart''')
        return self.cur.fetchall()

    def add_to_cart(self, item, price):
        self.cart.append((item, price))
        self.cur.execute('''INSERT INTO cart (item, price) VALUES (?, ?)''', (item, price))
        self.conn.commit()

    def remove_from_cart(self, idx):
        del self.cart[idx]
        self.cur.execute('''DELETE FROM cart WHERE id = ?''', (idx+1,))
        self.conn.commit()
        self.show_cart()  # Refresh the cart view after removing item

    def checkout(self):
        # Open the checkout page in the web browser
        checkout_url = "https://www.livedigi.com/topup-online"
        webbrowser.open(checkout_url)

        # Generate bill and reset cart
        if self.cart:
            bill_text = "Date: {}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            total_price = 0
            for item, price in self.cart:
                bill_text += f"{item} - ${price:.2f}\n"
                total_price += price
            bill_text += "\nTotal: ${:.2f}".format(total_price)

            # Save bill to file or print
            with open("bill.txt", "w") as file:
                file.write(bill_text)

            # Reset cart
            self.cart = []
            self.cur.execute('''DELETE FROM cart''')
            self.conn.commit()
            self.show_cart()
            
    def cashout(self):
        # Generate bill
        if self.cart:
            bill_text = "Date: {}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            total_price = 0
            for item, price in self.cart:
                bill_text += f"{item} - ${price:.2f}\n"
                total_price += price
            bill_text += "\nTotal: ${:.2f}".format(total_price)

            # Save bill to file
            with open("bill.txt", "w") as file:
                file.write(bill_text)

            # Clear cart
            self.cart = []
            self.cur.execute('''DELETE FROM cart''')
            self.conn.commit()
    

    def search_items(self):
        search_query = self.entry.get().strip().lower()
        found = False

        for item in self.prices:
            if search_query in item.lower():
                found = True
                break

        if found:
            self.show_category("Search")
        else:
            # No matching items found, keep the item frame unchanged
            pass

    def show_category(self, category):
        # Clear the item frame
        for widget in self.item_frame.winfo_children():
            widget.destroy()

        search_query = self.entry.get().strip().lower()
        filtered_items = []

        if search_query:
            # Filter items based on search query
            for item in self.prices:
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
                self.show_cart()

        # Display filtered items and descriptions
        placeholder_image = Image.open("pizza.png")
        placeholder_image = placeholder_image.resize((100, 100), Image.LANCZOS)

        for i, item in enumerate(filtered_items):
            price = self.prices.get(item, 0)
            item_image_path = self.item_images.get(item, "pizza.png")
            item_image = Image.open(item_image_path)
            item_image = item_image.resize((100, 100), Image.LANCZOS)

            # Convert PIL Image to CTkImage
            item_image = ImageTk.PhotoImage(item_image)

            item_button = customtkinter.CTkButton(self.item_frame, text=f"{item} - ${price:.2f}", image=item_image, compound="left", width=30,
                                     command=lambda it=item, pr=price: self.add_to_cart(it, pr))
            item_button.grid(row=i+1, column=0, padx=10, pady=5)

            # Display descriptions in columns 2-3
            if item in self.item_descriptions:
                description_label = customtkinter.CTkLabel(self.item_frame, text=self.item_descriptions[item], wraplength=300)
                description_label.grid(row=i+1, column=1, columnspan=2, padx=10, pady=5, sticky="w")

    def show_cart(self):
        # Clear the item frame
        for widget in self.item_frame.winfo_children():
            widget.destroy()

        total_price = 0
        for i, (item, price) in enumerate(self.cart):
            item_label = customtkinter.CTkLabel(self.item_frame, text=f"{item} - ${price:.2f}", width=30)
            item_label.grid(row=i, column=0, padx=10, pady=5)
            total_price += price

            # Add remove button for each item
            remove_button = customtkinter.CTkButton(self.item_frame, text="Remove", width=10,
                                       command=lambda idx=i: self.remove_from_cart(idx))
            remove_button.grid(row=i, column=1, padx=10, pady=5)

        # Display total price
        total_label = customtkinter.CTkLabel(self.item_frame, text=f"Total: ${total_price:.2f}", width=30)
        total_label.grid(row=len(self.cart), column=0, columnspan=2, padx=10, pady=5)

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    app = App()
    app.mainloop()

