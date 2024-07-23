import tkinter as tk
from tkinter import ttk
from recipes_data import recipes

class MealPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Meal Planner")

        self.center_window(600, 400)  # Increased window size for additional input fields

        self.create_frames()
        self.style_widgets()

        self.show_frame(self.input_frame)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_frames(self):
        # Main frame for input page
        self.input_frame = ttk.Frame(self.root, padding="10")
        self.input_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.create_input_widgets()

        # Main frame for meal plan page with scrolling
        self.meal_plan_frame = ttk.Frame(self.root, padding="10")
        self.create_meal_plan_widgets()
        self.meal_plan_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.meal_plan_frame.lower() 

        # Main frame for meal details page with scrolling
        self.details_frame = ttk.Frame(self.root, padding="10")
        self.create_details_widgets()
        self.details_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.details_frame.lower()  

        # Configure grid weights for the root window and each frame
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.input_frame.grid_rowconfigure(0, weight=0)
        self.input_frame.grid_rowconfigure(1, weight=0)
        self.input_frame.grid_rowconfigure(2, weight=0)
        self.input_frame.grid_rowconfigure(3, weight=0)
        self.input_frame.grid_rowconfigure(4, weight=0)
        self.input_frame.grid_rowconfigure(5, weight=0)
        self.input_frame.grid_rowconfigure(6, weight=0)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.meal_plan_frame.grid_rowconfigure(1, weight=1)
        self.meal_plan_frame.grid_columnconfigure(0, weight=1)
        self.meal_plan_frame.grid_columnconfigure(1, weight=0)

        self.details_frame.grid_rowconfigure(1, weight=1)
        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_columnconfigure(1, weight=1)

    def create_input_widgets(self):
        self.label = ttk.Label(self.input_frame, text="Welcome to the Simple Meal Planner", font=("Helvetica", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        self.new_label = ttk.Label(self.input_frame, text="Please enter your Preferences:", font=("Helvetica", 12))
        self.new_label.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        self.pref_label = ttk.Label(self.input_frame, text="Dietary Preferences:", font=("Helvetica", 12), anchor="e")
        self.pref_label.grid(row=2, column=0, pady=5, sticky=tk.E)

        self.pref_options = ["All", "Vegetarian", "Vegan", "Gluten-Free", "Non-Vegetarian"]
        self.pref_combobox = ttk.Combobox(self.input_frame, values=self.pref_options, state="readonly", width=28)
        self.pref_combobox.set(self.pref_options[0]) 
        self.pref_combobox.grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))

        # Add a sentence before the allergy label
        self.pre_allergy_sentence = ttk.Label(self.input_frame, text="Please provide any allergies or dietary restrictions:", font=("Helvetica", 12))
        self.pre_allergy_sentence.grid(row=3, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        self.allergy_label = ttk.Label(self.input_frame, text="Allergies/Restrictions:", font=("Helvetica", 12), anchor="e")
        self.allergy_label.grid(row=4, column=0, pady=5, sticky=tk.E)

        # Add a sentence after the allergy label
        self.post_allergy_sentence = ttk.Label(self.input_frame, text="Make sure to list atleast two ingredients:", font=("Helvetica", 12))
        self.post_allergy_sentence.grid(row=5, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        self.allergy_entry = ttk.Entry(self.input_frame, width=30)
        self.allergy_entry.grid(row=4, column=1, pady=5, sticky=(tk.W, tk.E))

        # Create fields for multiple ingredients
        self.ingredient_labels = []
        self.ingredient_entries = []
        for i in range(3): 
            label = ttk.Label(self.input_frame, text=f"Ingredient {i+1}:", font=("Helvetica", 12), anchor="e")
            label.grid(row=6 + i, column=0, pady=5, sticky=tk.E)
            entry = ttk.Entry(self.input_frame, width=30)
            entry.grid(row=6 + i, column=1, pady=5, sticky=(tk.W, tk.E))
            self.ingredient_labels.append(label)
            self.ingredient_entries.append(entry)

        self.submit_button = ttk.Button(self.input_frame, text="Submit", command=self.show_meal_plan)
        self.submit_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.root.bind("<Return>", lambda event: self.submit_button.invoke())

    def create_meal_plan_widgets(self):
        self.meal_plan_label = ttk.Label(self.meal_plan_frame, text="Weekly Meal Plan", font=("Helvetica", 16, "bold"))
        self.meal_plan_label.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        # Scrollbar
        self.meal_plan_canvas = tk.Canvas(self.meal_plan_frame)
        self.meal_plan_scrollbar = ttk.Scrollbar(self.meal_plan_frame, orient="vertical", command=self.meal_plan_canvas.yview)
        self.meal_plan_content = ttk.Frame(self.meal_plan_canvas)

        self.meal_plan_content.bind("<Configure>", lambda e: self.meal_plan_canvas.configure(scrollregion=self.meal_plan_canvas.bbox("all")))

        self.meal_plan_canvas.create_window((0, 0), window=self.meal_plan_content, anchor="nw")
        self.meal_plan_canvas.grid(row=1, column=0, sticky="nsew")
        self.meal_plan_scrollbar.config(command=self.meal_plan_canvas.yview)
        self.meal_plan_scrollbar.grid(row=1, column=1, sticky="ns")

        self.meal_plan_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.back_to_input_button = ttk.Button(self.meal_plan_frame, text="Back", command=self.show_input_page)
        self.back_to_input_button.grid(row=2, column=0, columnspan=2, pady=10)

    def create_details_widgets(self):
        self.details_label = ttk.Label(self.details_frame, text="", font=("Helvetica", 16, "bold"))
        self.details_label.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        self.details_content = tk.Text(self.details_frame, wrap=tk.WORD, font=("Helvetica", 12), height=10)
        self.details_content.grid(row=1, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        self.details_scrollbar = ttk.Scrollbar(self.details_frame, orient="vertical", command=self.details_content.yview)
        self.details_scrollbar.grid(row=1, column=2, sticky="ns")
        self.details_content.config(yscrollcommand=self.details_scrollbar.set)

        self.back_to_meal_plan_button = ttk.Button(self.details_frame, text="Back", command=self.show_meal_plan)
        self.back_to_meal_plan_button.grid(row=2, column=0, columnspan=2, pady=10)

    def style_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton",
                        font=("Helvetica", 12),
                        padding=6,
                        relief="raised",
                        background="blue",  
                        foreground="black")    
        style.configure("TFrame", background="#f0f0f0")
        
        style.map("TButton",
                  background=[('active', 'blue')],  
                  foreground=[('active', 'black')])    

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.meal_plan_canvas.yview_scroll(-1, "units")
        else:
            self.meal_plan_canvas.yview_scroll(1, "units")

    def show_frame(self, frame):
        frame.tkraise()

    def show_input_page(self):
        self.show_frame(self.input_frame)

    def show_meal_plan(self):
        dietary_preferences = self.pref_combobox.get().strip().lower()  
        allergies = [allergy.strip().lower() for allergy in self.allergy_entry.get().strip().split(',') if allergy.strip()]
        available_ingredients = [entry.get().strip().lower() for entry in self.ingredient_entries if entry.get().strip()]

        if not available_ingredients:
            available_ingredients = []

        meal_plan = self.generate_meal_plan(dietary_preferences, available_ingredients, allergies)

        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for widget in self.meal_plan_content.winfo_children():
            widget.destroy()

        for i, meal in enumerate(meal_plan):
            day_name = days_of_week[i]  
            label = ttk.Label(self.meal_plan_content, text=f"{day_name}: {meal['name']}", font=("Helvetica", 12, "bold"), anchor="w")
            label.grid(row=i, column=0, padx=5, pady=2, sticky=(tk.W, tk.E))
            details_button = ttk.Button(self.meal_plan_content, text="Details", command=lambda meal=meal: self.show_meal_details(meal))
            details_button.grid(row=i, column=1, padx=5, pady=2, sticky=(tk.W, tk.E))

        self.show_frame(self.meal_plan_frame)

    def show_meal_details(self, meal):
        self.details_label.config(text=meal['name'])
        ingredients_text = f"Grocery list: {', '.join(meal['ingredients'])}"
        instructions_text = f"Instructions: {meal.get('instructions', 'No instructions available.')}"
        
        details_text = f"{ingredients_text}\n\n{instructions_text}"

        self.details_content.delete(1.0, tk.END) 
        self.details_content.insert(tk.END, details_text)

        self.show_frame(self.details_frame)

    def generate_meal_plan(self, dietary_preferences, available_ingredients, allergies):
        # Filter recipes based on dietary preferences
        if dietary_preferences == "all":
            filtered_recipes = recipes
        else:
            filtered_recipes = [recipe for recipe in recipes if dietary_preferences in recipe['diet'].lower()]

        # Function to check if recipe contains at least 2 of the available ingredients
        def contains_at_least_two_ingredients(recipe, ingredients):
            if not ingredients:
                return True
            recipe_ingredients = [i.lower() for i in recipe['ingredients']]
            return len([ingredient for ingredient in recipe_ingredients if ingredient in ingredients]) >= 2

        # Function to check if recipe contains any of the allergies
        def contains_allergies(recipe, allergies):
            if not allergies:
                return True
            recipe_ingredients = [i.lower() for i in recipe['ingredients']]
            return not any(allergy in recipe_ingredients for allergy in allergies)

        # Filter recipes based on available ingredients and allergies
        meal_plan = [recipe for recipe in filtered_recipes 
                    if contains_at_least_two_ingredients(recipe, available_ingredients) 
                    and contains_allergies(recipe, allergies)]

        # If no recipes are found, provide a placeholder meal
        if not meal_plan:
            return [{"name": "No meal plan available", "ingredients": [], "diet": ""}]

        return (meal_plan * (7 // len(meal_plan) + 1))[:7]

if __name__ == "__main__":
    root = tk.Tk()
    app = MealPlannerApp(root)
    root.mainloop()
