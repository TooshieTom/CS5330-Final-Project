import tkinter as tk

root = tk.Tk()
root.title("Database GUI")
root.geometry("800x600")

# Tables
tables = {
    "Users": ["Username", "Soc_Med", "Name", "Verified", "Country_Birth", "Country_Res", "Age", "Gender"],
    "Post": ["Username", "Soc_Med", "Time_Posted", "City", "State", "Country", "Multimedia", "Likes", "Dislikes", "Text", "Poster_OG", "Time_OG"],
    "Project": ["Name", "Manager", "Institute", "Start_Date", "End_Date"],
    "Record": ["Project", "Text", "Fields", "Username", "Time_Posted", "Soc_Med"]
}

# Variables
mode_var = tk.StringVar(value="Choose action")
table_var = tk.StringVar(value="Choose table")

entries = []  # To store current entries

# Frames
mode_frame = tk.Frame(root)
mode_frame.pack(pady=10)

dynamic_frame = tk.Frame(root)
dynamic_frame.pack(pady=10)

# --- Functions ---

def clear_frame():
    for widget in dynamic_frame.winfo_children():
        widget.destroy()
    entries.clear()

trace_id = None

def add_select_field():
    """Adds another set of SELECT column, operator, and value entry fields."""
    # SELECT column dropdown
    select_label = tk.Label(dynamic_frame, text="SELECT")
    select_label.pack()

    new_column_var = tk.StringVar()
    new_column_var.set("Choose column")
    column_drop = tk.OptionMenu(dynamic_frame, new_column_var, *tables[table_var.get()])
    column_drop.pack()

    # Operator dropdown
    operator_label = tk.Label(dynamic_frame, text="Choose Operator")
    operator_label.pack()
    new_operator_var = tk.StringVar()
    new_operator_var.set("=")  # Default to equals operator
    operator_drop = tk.OptionMenu(dynamic_frame, new_operator_var, '=', '<', '<=', '>', '>=', '!=')
    operator_drop.pack(pady=5)

    # Value input field
    value_label = tk.Label(dynamic_frame, text="Enter Value")
    value_label.pack()
    new_value_entry = tk.Entry(dynamic_frame)
    new_value_entry.pack(pady=5)

def update_ui(*args):
    global trace_id ####
    clear_frame()
    selected_mode = mode_var.get()

    if selected_mode == "Insert":
        table_var.set("Choose table")
        table_dropdown = tk.OptionMenu(dynamic_frame, table_var, *tables.keys())
        table_dropdown.pack(pady=5)
        table_var.trace_add('write', show_table_entries)

    elif selected_mode == "Query": 
        #clear
        if trace_id is not None:
            table_var.trace_remove('write', trace_id)


        #select table dropdown
        from_label = tk.Label(dynamic_frame, text="FROM")
        from_label.pack()
        table_var.set("Choose table")
        select_drop = tk.OptionMenu(dynamic_frame, table_var, *tables.keys())
        select_drop.pack()

         # Function to update select column options based on the selected table
        def update_columns(*args):
            selected_table = table_var.get()
            # if selected_table != "Choose table":
            select_label = tk.Label(dynamic_frame, text="SELECT")
            select_label.pack()

            # Update the columns dropdown to show the columns of the selected table
            column_var.set("Choose column")
            column_drop = tk.OptionMenu(dynamic_frame, column_var, *tables[selected_table])
            column_drop.pack()

            # Operator dropdown
            operator_label = tk.Label(dynamic_frame, text="Choose Operator")
            operator_label.pack()
            operator_var.set("=")  # Default to equals operator
            operator_drop = tk.OptionMenu(dynamic_frame, operator_var, '=', '<', '<=', '>', '>=', '!=')
            operator_drop.pack(pady=5)

            # Value input field
            value_label = tk.Label(dynamic_frame, text="Enter Value")
            value_label.pack()
            value_entry = tk.Entry(dynamic_frame)
            value_entry.pack(pady=5)


            def submit_query():
                selected_table = table_var.get()
                selected_column = column_var.get()
                selected_operator = operator_var.get()
                entered_value = value_entry.get()

                # Print all the inputs to the terminal
                print(f"Table: {selected_table}")
                print(f"Column: {selected_column}")
                print(f"Operator: {selected_operator}")
                print(f"Value: {entered_value}")
                clear_frame()
            # def submit_query():
            #     """Collects all inputs from dynamically added fields and prints the query."""
            #     selected_table = table_var.get()
            #     query_conditions = []

            #     # Iterate through all widgets in the dynamic_frame to collect inputs
            #     for widget in dynamic_frame.winfo_children():
            #         if isinstance(widget, tk.OptionMenu):  # Dropdowns
            #             # Get the associated StringVar for the dropdown
            #             var = widget.cget("textvariable")
            #             value = root.nametowidget(var).get()
            #             query_conditions.append(value)
            #         elif isinstance(widget, tk.Entry):  # Entry fields
            #             value = widget.get()
            #             query_conditions.append(value)

            #     # Print the collected query conditions
            #     print(f"Table: {selected_table}")
            #     print("Query Conditions:")
            #     for i in range(0, len(query_conditions), 3):  # Group by SELECT, Operator, Value
            #         print(f"Column: {query_conditions[i]}, Operator: {query_conditions[i+1]}, Value: {query_conditions[i+2]}")

            #     clear_frame()


            # Add a checkmark button to add more fields
            add_field_btn = tk.Button(dynamic_frame, text="✔ Add Field", command=add_select_field)
            add_field_btn.pack(pady=10)

            submit_btn = tk.Button(dynamic_frame, text="Submit Query", command=submit_query)
            submit_btn.pack(pady=10)

        # Add a trace to the table_var to update the columns dropdown when a table is selected
        column_var = tk.StringVar()
        column_var.set("Choose column")
        operator_var = tk.StringVar()
        value_var = tk.StringVar()
        table_var.trace_add('write', update_columns)

        
def show_table_entries(*args):
    clear_frame()
    
    table_name = table_var.get()
    attributes = tables.get(table_name, [])

    for attr in attributes:
        label = tk.Label(dynamic_frame, text=attr)
        label.pack()
        entry = tk.Entry(dynamic_frame)
        entry.pack(pady=2)
        entries.append(entry)

    submit_btn = tk.Button(dynamic_frame, text="Submit Insert", command=submit_insert)
    submit_btn.pack(pady=10)

def submit_insert():
    values = [e.get() for e in entries]
    print("Insert into", table_var.get(), "values:", values)
    #Send info to other function 
    clear_frame()

# def submit_query():
#     parts = [e.get() for e in entries]
#     print("Query:", f"SELECT {parts[0]} FROM {parts[1]} WHERE {parts[2]}")
#     #Send info to other function



# --- Dropdown to choose Insert or Query ---

mode_dropdown = tk.OptionMenu(mode_frame, mode_var, "Insert", "Query")
mode_dropdown.pack()

mode_var.trace_add('write', update_ui)

# print(tables["Users"])
# print(*tables.keys())

root.mainloop()
