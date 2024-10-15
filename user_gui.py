import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkcalendar import DateEntry
from connection import ConnectionManager

# Sample list of food items with nutritional values
food_items1 = {
    "Apple": {"calories": 95, "protein": 0.5, "fat": 0.3, "carbs": 25},
    "Banana": {"calories": 105, "protein": 1.3, "fat": 0.3, "carbs": 27},
    "Carrot": {"calories": 41, "protein": 0.9, "fat": 0.2, "carbs": 10},
    "Doughnut": {"calories": 300, "protein": 2.0, "fat": 15, "carbs": 36},
    "Eggplant": {"calories": 20, "protein": 1.0, "fat": 0.2, "carbs": 5},
    "Fries": {"calories": 365, "protein": 3.4, "fat": 17, "carbs": 63},
    "Grapes": {"calories": 104, "protein": 1.1, "fat": 0.2, "carbs": 27},
    "Hamburger": {"calories": 250, "protein": 12, "fat": 10, "carbs": 32},
    "Ice Cream": {"calories": 207, "protein": 3.5, "fat": 11, "carbs": 24},
    "Jelly": {"calories": 50, "protein": 0, "fat": 0, "carbs": 13},
}

class FoodTrackingApp:
    def __init__(self, root, db_manager):
        self.root = root
        self.root.title("Food Tracker")
        self.db_manager = db_manager

        self.email_label = tk.Label(root, text="Enter Your Email:")
        self.email_label.pack(pady=10)

        self.email_entry = tk.Entry(root)
        self.email_entry.pack(pady=5)

        self.label = tk.Label(root, text="Select a Date:")
        self.label.pack(pady=10)

        self.date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)

        self.pull_button = tk.Button(root, text="Enter", command=self.pull_entries)
        self.pull_button.pack(pady=5)

        self.search_label = tk.Label(root, text="Search for food:")
        self.search_label.pack(pady=10)

        self.search_entry = tk.Entry(root)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(root, text="Search", command=self.update_list)
        self.search_button.pack(pady=5)

        self.food_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=30, height=10)
        self.food_listbox.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Food", command=self.select_food)
        self.select_button.pack(pady=5)

        self.log_label = tk.Label(root, text="Food Log:")
        self.log_label.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(root, width=30, height=10, state='disabled')
        self.log_text.pack(pady=5)

        self.nutrition_label = tk.Label(root, text="Total Nutrition:")
        self.nutrition_label.pack(pady=10)

        self.nutrition_text = tk.Text(root, width=30, height=5, state='disabled')
        self.nutrition_text.pack(pady=5)

        self.food_item = self.db_manager.search_foods()
        self.dictionary = dict()

        self.reset_nutrition()
        self.update_list()  # Initialize the listbox with all items

    #Add DB search vs using dummy data
    def update_list(self, event=None):
        search_term = self.search_entry.get().lower()
        self.food_listbox.delete(0, tk.END)

        for description, fdc_id in self.food_item:
            self.dictionary.setdefault(description, fdc_id)
        print(self.dictionary)
        for entry in self.dictionary.keys():
            if search_term in entry.lower():
                self.food_listbox.insert(tk.END, f"{entry}\n")


    def select_food(self):
        selected_food = self.food_listbox.curselection()
        if selected_food:
            food = self.food_listbox.get(selected_food)
            print(f"key:{food}")
            fdc_id = self.dictionary.get('Pork, loin, tenderloin, boneless, raw')
            print(f"id:{fdc_id}")
            self.log_selection(food)
            self.update_nutrition()
            email = self.email_entry.get()
            error = self.db_manager.insert_food(self.date_entry.get_date(), fdc_id, email)
            if error:
                messagebox.showerror("Database Error", error)
            else:
                messagebox.showinfo("Selected Food", f"You selected: {food}")
        else:
            messagebox.showwarning("No Selection", "Please select a food item.")

    def log_selection(self, food):
        selected_date = self.date_entry.get_date()
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{selected_date}: {food}\n")
        self.log_text.config(state='disabled')

    def reset_nutrition(self):
        self.total_protein = 0
        self.total_fat = 0
        self.total_carbs = 0
        self.update_nutrition_display()

    def update_nutrition(self):
        data = db_manager.get_totals(self.date_entry.get_date())
        for entry in data:
            protein, fat, carbs = entry
            self.total_protein = protein
            self.total_fat = fat
            self.total_carbs = carbs
            self.update_nutrition_display()

    def update_nutrition_display(self):
        self.nutrition_text.config(state='normal')
        self.nutrition_text.delete(1.0, tk.END)
        self.nutrition_text.insert(tk.END, f"Protein: {self.total_protein}g\n")
        self.nutrition_text.insert(tk.END, f"Fat: {self.total_fat}g\n")
        self.nutrition_text.insert(tk.END, f"Carbs: {self.total_carbs}g\n")
        self.nutrition_text.config(state='disabled')

    def pull_entries(self):
        selected_date = self.date_entry.get_date()
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)  # Clear previous entries
        entries = self.db_manager.pull_entries(selected_date)
        if isinstance(entries, str):  # Check for an error
            messagebox.showerror("Database Error", entries)
        else:
            if entries:
                for entry in entries:
                    description, protein, fat, carbs = entry
                    self.log_text.insert(tk.END, f"{description} - Protein: {protein}g, Fat: {fat}g, Carbs: {carbs}g\n")
            else:
                self.log_text.insert(tk.END, "No entries found for this date.\n")
        self.log_text.config(state='disabled')

    def __del__(self):
        self.db_manager.close()

if __name__ == "__main__":
    root = tk.Tk()
    db_manager = ConnectionManager(connection_string="postgresql://postgres:1234@localhost:5433")
    app = FoodTrackingApp(root, db_manager)
    root.mainloop()
