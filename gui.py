import tkinter as tk
from tkinter import ttk
import datetime
# import backend

tables = {
    "User": ["Username", "Soc_Med", "Name", "Verified", "Country_Birth", "Country_Res", "Age", "Gender"],
    "Post": ["Username", "Soc_Med", "Time_Posted", "City", "State", "Country", "Multimedia", "Name_F", "Name_L", "Likes", "Dislikes", "Text", "Poster_OG", "Time_OG"],
    "Project": ["Name", "Manager", "Institute", "Start_Date (Yr-M-D)", "End_Date (Yr-M-D)"],
    "Record": ["Project", "Text", "Fields", "Username", "Time_Posted", "Soc_Med"]
}

root = tk.Tk()
root.geometry("750x800")
root.title("Databases")

def IQ_change_frame(*args):
    # print("hello")
    x = IQ_selected.get()
    if x == "Insert":
        # clear_frame(qframe)
        pi_frame.pack_forget()
        qframe.pack_forget()
        rframe.pack_forget()
        iframe.pack()
    elif x == "Query":
        # clear_frame(iframe)
        pi_frame.pack_forget()
        iframe.pack_forget()
        rframe.pack_forget()
        qframe.pack()
    elif x == "Project":
        iframe.pack_forget()
        qframe.pack_forget()
        rframe.pack_forget()
        pi_frame.pack()
    else:
        iframe.pack_forget()
        qframe.pack_forget()
        pi_frame.pack_forget()
        rframe.pack()

def get_posts():
    name = pi_proj_entry.get()
    print(name)
    
    #send query to retrieve all posts
    #get (SELECT username, soc_med, time_posted FROM post)

def p_submit(*args):
    entries = []
    for i in p_entries:
        entries.append(i.get())
        print(i.get())
        i.delete(0,tk.END)

def r_submit(*args):
    #can do the smae thing of saying if it was successful or not
    pass

def i_table_frame(*args):
    x = i_table_drop_var.get()
    # print(x)
    if x == "User":
        i_entries.clear()
        i_button.pack_forget()
        iframe_post.pack_forget()
        iframe_project.pack_forget()
        iframe_record.pack_forget()
        iframe_users.pack()
        for widget in iframe_users.winfo_children():
            if isinstance(widget, tk.Entry):
                i_entries.append(widget)
    elif x == "Post":
        i_entries.clear()
        i_button.pack_forget()
        iframe_users.pack_forget()
        iframe_project.pack_forget()
        iframe_record.pack_forget()
        iframe_post.pack()
        for widget in iframe_post.winfo_children():
            if isinstance(widget, tk.Entry):
                i_entries.append(widget)
    elif x == "Project":
        i_entries.clear()
        i_button.pack_forget()
        iframe_users.pack_forget()
        iframe_post.pack_forget()
        iframe_record.pack_forget()
        iframe_project.pack()
        for widget in iframe_project.winfo_children():
            if isinstance(widget, tk.Entry):
                i_entries.append(widget)
    elif x == "Record":
        i_entries.clear()
        i_button.pack_forget()
        iframe_users.pack_forget()
        iframe_post.pack_forget()
        iframe_project.pack_forget()
        iframe_record.pack()
        for widget in iframe_record.winfo_children():
            if isinstance(widget, tk.Entry):
                i_entries.append(widget)
    i_button.pack()

# ec = 1

def i_submit(*args):
    # global ec
    # print("SUBMITTED")
    x = i_table_drop_var.get()
    print("Table: ", x)
    entries = []
    for i in i_entries:
        entries.append(i.get())
        i.delete(0, tk.END)
    for i in range(len(entries)):
        print(tables[x][i], ": ", entries[i])

    # backend call to actually query db for insert
    # ec = backend.enterTuple(entries)
    # ec = 1
    # if ec == 1:
    #     # show input invalid
    #     failed.pack()
    #     success.pack_forget()
    # else:
    #     failed.pack_forget()
    #     success.pack()


def update_columns(*args):
    x = from_var.get()
    # q_entries.clear()
    if x == "User":
        check_button.pack_forget()
        qframe_sub.pack_forget()
        qframe_post.pack_forget()
        qframe_project.pack_forget()
        qframe_record.pack_forget()
        q_columns_label.pack()
        qframe_users.pack()
        qframe_sub.pack()
        check_button.pack()
        q_entries[0] = q_columns_user_var
    elif x == "Post":
        check_button.pack_forget()
        qframe_sub.pack_forget()
        qframe_users.pack_forget()
        qframe_project.pack_forget()
        qframe_record.pack_forget()
        q_columns_label.pack()
        qframe_post.pack()
        qframe_sub.pack()
        check_button.pack()
        q_entries[0] = q_columns_post_var
    elif x == "Project":
        check_button.pack_forget()
        qframe_sub.pack_forget()
        qframe_users.pack_forget()
        qframe_post.pack_forget()
        qframe_record.pack_forget()
        q_columns_label.pack()
        qframe_project.pack()
        qframe_sub.pack()
        check_button.pack()
        q_entries[0] = q_columns_project_var
    elif x == "Record":
        check_button.pack_forget()
        qframe_sub.pack_forget()
        qframe_users.pack_forget()
        qframe_post.pack_forget()
        qframe_project.pack_forget()
        q_columns_label.pack()
        qframe_record.pack()
        qframe_sub.pack()
        check_button.pack()
        q_entries[0] = q_columns_record_var            


def create_qtable(table, data):
    tree_frame.pack_forget()
    columns = tables[table]

    for widget in tree_frame.winfo_children():
        widget.destroy()
    # print(columns)
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=5)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    for row in data:
        tree.insert("", tk.END, values=row)
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    tree_frame.pack()


def temp_db(arr): 
    x = from_var.get()
    if x == "User":
        # User table
        user_data = [
            ("jdoe92", "Twitter", "John Doe", True, "USA", "UK", 31, "Male"),
            ("asmith88", "Instagram", "Alice Smith", False, "Canada", "Canada", 29, "Female"),
        ]
        return user_data
    elif x == "Post":
        # Post table
        post_data = [
            ("jdoe92", "Twitter", "2025-04-01 12:34:00", "New York", "NY", "USA", "Image", "John", "Doe", 120, 5, "Loving this weather!", True, "2025-04-01 12:34:00"),
            ("asmith88", "Instagram", "2025-03-25 09:15:00", "Toronto", "ON", "Canada", "Video", "Alice", "Smith", 300, 2, "Morning workout done!", True, "2025-03-25 09:15:00"),
        ]
        return post_data
    elif x == "Project":
        # Project table
        project_data = [
            ("GreenTech", "Emma Wilson", "EcoLab Inc.", "2023-01-15", "2024-12-31"),
            ("AI4Good", "Daniel Chen", "TechU Research", "2022-09-01", "2025-05-30"),
        ]
        return project_data
    elif x == "Record":
        # Record table
        record_data = [
            ("GreenTech", "Installed solar panels in three locations.", "energy, sustainability", "jdoe92", "2024-11-22 10:00:00", "Twitter"),
            ("AI4Good", "Developed a sentiment analysis tool.", "AI, NLP", "asmith88", "2025-01-05 14:45:00", "Instagram"),
        ]
        return record_data
    return x


def better_q_submit():
    selected_table = from_var.get()
    
    q_words = ["Column", "Operator", "Value","Column", "Operator", "Value","Column", "Operator", "Value","Column", "Operator", "Value",
               "Column", "Operator", "Value","Column", "Operator", "Value","Column", "Operator", "Value","Column", "Operator", "Value"]
    print(f"Table: {selected_table}")
    submit = []
    for i in range(len(q_entries)):
        x = q_entries[i].get()
        submit.append(x)
        print(q_words[i], ": ", x)
    #Pass submit array
    data = temp_db(submit)#############################################################change line for database
    create_qtable(selected_table, data)

                
def add_field():
    selected_table = from_var.get()

    field_frame = tk.Frame(qframe_sub)
    field_frame.pack()

    column_label = tk.Label(field_frame, text="COLUMN")
    column_label.pack()
    column_var = tk.StringVar(field_frame, value="Choose")
    column_drop = tk.OptionMenu(field_frame, column_var, *tables[selected_table])
    column_drop.pack()

    op_label = tk.Label(field_frame, text="OPERATOR")
    op_label.pack()
    op_var = tk.StringVar(field_frame, value="Choose")
    op_drop = tk.OptionMenu(field_frame, op_var,  "=", "<", "<=", ">=", ">", "!=")
    op_drop.pack()

    value_label = tk.Label(field_frame, text="VALUE")
    value_label.pack()
    value_entry = tk.Entry(field_frame)
    value_entry.pack()

    # q_entries.append((column_var, op_var, value_entry))
    q_entries.append(column_var)
    q_entries.append(op_var)
    q_entries.append(value_entry)

iframe = tk.Frame(root)
qframe = tk.Frame(root)

IQ_selected = tk.StringVar(value="Select")
IQ_selected.trace_add('write', IQ_change_frame)
drop = tk.OptionMenu(root, IQ_selected, "Insert", "Query", "Project", "Update Record")
drop.pack(pady=10)

"""RECORD UPDATE"""
rframe = tk.Frame(root)

# rframe_top = tk.Frame(rframe)
# rframe_bottom = tk.Frame(rframe)

# rframe_top.pack()
# rframe_bottom.pack()

r_proj_label = tk.Label(rframe, text="Project Name")
r_usr_label = tk.Label(rframe, text="Username")
r_soc_label = tk.Label(rframe, text="Social Media")
r_time_label = tk.Label(rframe, text="Time")
r_field_label = tk.Label(rframe, text="Fields")

r_proj_entry = tk.Entry(rframe)
r_usr_entry  = tk.Entry(rframe)
r_soc_entry  = tk.Entry(rframe)
r_time_entry = tk.Entry(rframe)
r_field_entry = tk.Entry(rframe)

r_proj_label.pack()
r_proj_entry.pack()
r_usr_label.pack()
r_usr_entry.pack()
r_soc_label.pack()
r_soc_entry.pack()
r_time_label.pack()
r_time_entry.pack()
r_field_label.pack()
r_field_entry.pack()

r_button = tk.Button(rframe, text="Update", command=r_submit)
r_button.pack()

"""PROJECT INSERT FRAME"""
pi_frame = tk.Frame(root)
pi_label_frame = tk.Frame(pi_frame)
pi_entry_frame = tk.Frame(pi_frame)

p_entries = []

pi_proj_label = tk.Label(pi_frame, text="PROJECT NAME")
pi_proj_entry = tk.Entry(pi_frame)
pi_proj_button = tk.Button(pi_frame, text="update posts", command=get_posts)
pi_proj_submit = tk.Button(pi_frame, text="Submit", command=p_submit)

pi_po_usr_label = tk.Label(pi_label_frame, text="POST USERNAME")
pi_po_usr_entry = tk.Entry(pi_entry_frame)

pi_po_soc_label = tk.Label(pi_label_frame, text="POST SOC_MED")
pi_po_soc_entry = tk.Entry(pi_entry_frame)

pi_po_time_label = tk.Label(pi_label_frame, text="POST TIME")
pi_po_time_entry = tk.Entry(pi_entry_frame)

p_entries.append(pi_proj_entry)
p_entries.append(pi_po_usr_entry)
p_entries.append(pi_po_soc_entry)
p_entries.append(pi_po_time_entry)

pi_proj_label.pack()
pi_proj_entry.pack()

pi_label_frame.pack()
pi_entry_frame.pack()

pi_proj_button.pack(pady=20)
pi_proj_submit.pack()

pi_po_usr_label.pack(side="left", padx=40)
pi_po_soc_label.pack(side="left",padx=40)
pi_po_time_label.pack(side="left",padx=40)
pi_po_usr_entry.pack(side="left")
pi_po_soc_entry.pack(side="left")
pi_po_time_entry.pack(side="left")

pi_table_frame = tk.Frame(pi_frame)

"""INSERT FRAME"""
i_table_label = tk.Label(iframe, text="TABLE")
i_table_drop_var = tk.StringVar(value="Choose Table")
i_table_drop_var.trace_add('write', i_table_frame)
i_table_drop = tk.OptionMenu(iframe, i_table_drop_var, *tables.keys())

i_button = tk.Button(iframe, text="Submit Info" ,command=i_submit)

success = tk.Label(iframe, text="INSERT SUCCESSFUL")
failed = tk.Label(iframe, text="INSERT FAILED")

i_entries = []

i_table_label.pack()
i_table_drop.pack()

"""IFRAME USERS"""
iframe_users = tk.Frame(iframe)

for attribute in tables["User"]:
    i_users_label = tk.Label(iframe_users, text=attribute)
    i_users_entry = tk.Entry(iframe_users)
    i_users_label.pack()
    i_users_entry.pack()
    # i_entries.append(i_users_entry)

"""IFRAME POST"""
iframe_post = tk.Frame(iframe)

for attribute in tables["Post"]:
    i_post_label = tk.Label(iframe_post, text=attribute)
    i_post_entry = tk.Entry(iframe_post)
    i_post_label.pack()
    i_post_entry.pack()
    # i_entries.append(i_post_entry)

"""IFRAME PROJECT"""
iframe_project = tk.Frame(iframe)

for attribute in tables["Project"]:
    i_project_label = tk.Label(iframe_project, text=attribute)
    i_project_entry = tk.Entry(iframe_project)
    i_project_label.pack()
    i_project_entry.pack()
    # i_entries.append(i_project_entry)

"""IFRAME RECORD"""
iframe_record = tk.Frame(iframe)

for attribute in tables["Record"]:
    i_record_label = tk.Label(iframe_record, text=attribute)
    i_record_entry = tk.Entry(iframe_record)
    i_record_label.pack()
    i_record_entry.pack()
    # i_entries.append(i_record_entry)


"""QUERY FRAME"""
qframe_sub = tk.Frame(qframe)
# qframe_sub.pack()


#table dropdown
from_label = tk.Label(qframe, text="FROM")
from_var = tk.StringVar(qframe, value="Choose")
from_var.trace_add('write', update_columns)
from_drop = tk.OptionMenu(qframe, from_var, *tables.keys())


#operator dropdown
q_drop_op_label = tk.Label(qframe_sub, text="OPERATOR")
q_drop_op_var = tk.StringVar(qframe_sub, value="Choose")
q_drop_op = tk.OptionMenu(qframe_sub, q_drop_op_var, "=", "<", "<=", ">=", ">", "!=")

#value entry
q_label_value = tk.Label(qframe_sub, text="VALUE")
q_entry_value = tk.Entry(qframe_sub)
button = tk.Button(qframe_sub, text="Submit", command=better_q_submit)

q_columns_label = tk.Label(qframe, text="COLUMN")

#qframe packing
from_label.pack()
from_drop.pack()

#qframe_sub pack
# q_columns_label.pack()#############
q_drop_op_label.pack()
q_drop_op.pack()
q_label_value.pack()
q_entry_value.pack()
button.pack()

#subframes
qframe_users = tk.Frame(qframe)
# qframe_users_more = tk.Frame(qframe_users)############################
qframe_post = tk.Frame(qframe)
qframe_project = tk.Frame(qframe)
qframe_record = tk.Frame(qframe)

"""USERS"""
q_columns_user_var = tk.StringVar(qframe_users, value="Choose")
q_columns_user_drop = tk.OptionMenu(qframe_users, q_columns_user_var, *tables["User"])


q_columns_user_drop.pack()

"""POST"""
q_columns_post_var = tk.StringVar(qframe_post, value="Choose")
q_columns_post_drop = tk.OptionMenu(qframe_post, q_columns_post_var, *tables["Post"])

q_columns_post_drop.pack()

"""PROJECT"""
q_columns_project_var = tk.StringVar(qframe_project, value="Choose")
q_columns_project_drop = tk.OptionMenu(qframe_project, q_columns_project_var, *tables["Project"])

q_columns_project_drop.pack()

""""RECORD"""
q_columns_record_var = tk.StringVar(qframe_record, value="Choose")
q_columns_record_drop = tk.OptionMenu(qframe_record, q_columns_record_var, *tables["Record"])

q_columns_record_drop.pack()


"""ENTRIES"""
#entries
q_entries = []
q_entries.append(q_columns_user_var)###GETS CHANGED IN UPDATE COLUMNS
q_entries.append(q_drop_op_var)
q_entries.append(q_entry_value)

"""MORE"""
more_frame = tk.Frame(qframe)

checked = False
check_button = tk.Button(qframe, text="more", command=add_field)

#operator dropdown
more_drop_op_label = tk.Label(more_frame, text="OPERATOR")
more_drop_op_var = tk.StringVar(more_frame, value="Choose")
more_drop_op = tk.OptionMenu(more_frame, more_drop_op_var, "=", "<", "<=", ">=", ">", "!=")

#value entry
more_label_value = tk.Label(more_frame, text="VALUE")
more_entry_value = tk.Entry(more_frame)

# q_columns_label = tk.Label(qframe, text="COLUMN")

more_drop_op_label.pack()
more_drop_op.pack()
more_label_value.pack()
more_entry_value.pack()

"""TABLE"""
tree_frame = tk.Frame(qframe)
# apsdoifj = tk.Label(tree_frame, text="HOAIWEHFPOIADHFPOIA")
# apsdoifj.pack()
# tree = ttk.Treeview(tree_frame)

root.mainloop()