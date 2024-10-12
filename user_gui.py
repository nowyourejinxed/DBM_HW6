import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

# Sample list of food items with nutritional values
food_items = {
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

class FoodSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Selector")

        self.label = tk.Label(root, text="Select a Date:")
        self.label.pack(pady=10)

        # Date selection using DateEntry
        self.date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)

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

        self.log_label = tk.Label(root, text="Selection Log:")
        self.log_label.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(root, width=30, height=10, state='disabled')
        self.log_text.pack(pady=5)

        self.nutrition_label = tk.Label(root, text="Total Nutrition:")
        self.nutrition_label.pack(pady=10)

        self.nutrition_text = tk.Text(root, width=30, height=5, state='disabled')
        self.nutrition_text.pack(pady=5)

        self.reset_nutrition()

        self.update_list()  # Initialize the listbox with all items

    def update_list(self, event=None):
        search_term = self.search_entry.get().lower()
        self.food_listbox.delete(0, tk.END)

        for food in food_items.keys():
            if search_term in food.lower():
                self.food_listbox.insert(tk.END, food)

    def select_food(self):
        selected_food = self.food_listbox.curselection()
        if selected_food:
            food = self.food_listbox.get(selected_food)
            self.log_selection(food)
            self.update_nutrition(food)
            messagebox.showinfo("Selected Food", f"You selected: {food}")
        else:
            messagebox.showwarning("No Selection", "Please select a food item.")

    def log_selection(self, food):
        selected_date = self.date_entry.get_date()  # Get the selected date
        self.log_text.config(state='normal')  # Enable editing
        self.log_text.insert(tk.END, f"{selected_date}: {food}\n")  # Add the food and date to the log
        self.log_text.config(state='disabled')  # Disable editing

    def reset_nutrition(self):
        self.total_calories = 0
        self.total_protein = 0
        self.total_fat = 0
        self.total_carbs = 0
        self.update_nutrition_display()

    def update_nutrition(self, food):
        self.total_calories += food_items[food]["calories"]
        self.total_protein += food_items[food]["protein"]
        self.total_fat += food_items[food]["fat"]
        self.total_carbs += food_items[food]["carbs"]
        self.update_nutrition_display()

    def update_nutrition_display(self):
        self.nutrition_text.config(state='normal')  # Enable editing
        self.nutrition_text.delete(1.0, tk.END)  # Clear previous text
        self.nutrition_text.insert(tk.END, f"Calories: {self.total_calories}\n")
        self.nutrition_text.insert(tk.END, f"Protein: {self.total_protein}g\n")
        self.nutrition_text.insert(tk.END, f"Fat: {self.total_fat}g\n")
        self.nutrition_text.insert(tk.END, f"Carbs: {self.total_carbs}g\n")
        self.nutrition_text.config(state='disabled')  # Disable editing

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodSelectorApp(root)
    root.mainloop()
