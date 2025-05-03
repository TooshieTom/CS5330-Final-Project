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

def update_ui(*args):
    clear_frame()
    selected_mode = mode_var.get()

    if selected_mode == "Insert":
        table_var.set("Choose table")
        table_dropdown = tk.OptionMenu(dynamic_frame, table_var, *tables.keys())
        table_dropdown.pack(pady=5)
        table_var.trace_add('write', show_table_entries)

    elif selected_mode == "Query":
        for field in ["SELECT", "FROM", "WHERE"]:
            label = tk.Label(dynamic_frame, text=field)
            label.pack()
            entry = tk.Entry(dynamic_frame)
            entry.pack(pady=2)
            entries.append(entry)
        
        submit_btn = tk.Button(dynamic_frame, text="Submit Query", command=submit_query)
        submit_btn.pack(pady=10)

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

def submit_query():
    parts = [e.get() for e in entries]
    print("Query:", f"SELECT {parts[0]} FROM {parts[1]} WHERE {parts[2]}")
    #Send info to other function

# --- Dropdown to choose Insert or Query ---

mode_dropdown = tk.OptionMenu(mode_frame, mode_var, "Insert", "Query")
mode_dropdown.pack()

mode_var.trace_add('write', update_ui)

root.mainloop()
