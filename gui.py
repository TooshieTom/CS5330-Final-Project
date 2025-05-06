import tkinter as tk
from tkinter import ttk
# import backend

tables = {
    "Users": ["Username", "Soc_Med", "Name", "Verified", "Country_Birth", "Country_Res", "Age", "Gender"],
    "Post": ["Username", "Soc_Med", "Time_Posted", "City", "State", "Country", "Multimedia", "Name_F", "Name_L", "Likes", "Dislikes", "Text", "Poster_OG", "Time_OG"],
    "Project": ["Name", "Manager", "Institute", "Start_Date", "End_Date"],
    "Record": ["Project", "Text", "Fields", "Username", "Time_Posted", "Soc_Med"]
}

root = tk.Tk()
root.geometry("750x800")
root.title("Databases")

def IQ_change_frame(*args):
    # print("hello")
    if IQ_selected.get() == "Insert":
        # clear_frame(qframe)
        qframe.pack_forget()
        iframe.pack()
    else:
        # clear_frame(iframe)
        iframe.pack_forget()
        qframe.pack()

# def clear_frame(frame):
#     for widgets in frame.winfo_children():
#         widgets.destroy()
def i_table_frame(*args):
    x = i_table_drop_var.get()
    # print(x)
    if x == "Users":
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

def i_submit(*args):
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
    # if ec == 1:
    #     # show input invalid
    #     pass


def update_columns(*args):
    x = from_var.get()
    # q_entries.clear()
    if x == "Users":
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

def q_submit(table):
    x = table.get()
    if checked:
        if x == "Users":
            print(x)
            print(q_columns_user_var.get())
            print(q_drop_op_var.get())
            print(q_entry_value.get())
            print(more_drop_op_var.get())
            print(more_entry_value.get())
        elif x == "Post":
            print(x)
            print(q_columns_post_var.get())
            print(q_drop_op_var.get())
            print(q_entry_value.get())
            print(more_drop_op_var.get())
            print(more_entry_value.get())
        elif x == "Project":
            print(x)
            print(q_columns_project_var.get())
            print(q_drop_op_var.get())
            print(q_entry_value.get())
            print(more_drop_op_var.get())
            print(more_entry_value.get())
        elif x == "Record":
            print(x)
            print(q_columns_record_var.get())
            print(q_drop_op_var.get())
            print(q_entry_value.get())
            print(more_drop_op_var.get())
            print(more_entry_value.get())
    else:
        q_words = ["COLUMN", "OPERATOR", "VALUE"]
        if x == "Users":
            print("Table: ", x)
            entries = []
            for q in q_entries:
                entries.append(q.get())
                if isinstance(q, tk.Entry):
                    q.delete(0, tk.END)
            for i in range(len(entries)):
                print(q_words[i], ": ", entries[i])
        elif x == "Post":
            print(x)
            print("Table: ", x)
            entries = []
            for q in q_entries:
                entries.append(q.get())
                if isinstance(q, tk.Entry):
                    q.delete(0, tk.END)
            for i in range(len(entries)):
                print(q_words[i], ": ", entries[i])
        elif x == "Project":
            print(x)
            print("Table: ", x)
            entries = []
            for q in q_entries:
                entries.append(q.get())
                if isinstance(q, tk.Entry):
                    q.delete(0, tk.END)
            for i in range(len(entries)):
                print(q_words[i], ": ", entries[i])
        elif x == "Record":
            print(x)
            print("Table: ", x)
            entries = []
            for q in q_entries:
                entries.append(q.get())
                if isinstance(q, tk.Entry):
                    q.delete(0, tk.END)
            for i in range(len(entries)):
                print(q_words[i], ": ", entries[i])
            
            
def better_q_submit():
    selected_table = from_var.get()
    
    q_words = ["Column", "Operator", "Value","Column", "Operator", "Value","Column", "Operator", "Value","Column", "Operator", "Value",
               "Column", "Operator", "Value","Column", "Operator", "Value","Column", "Operator", "Value","Column", "Operator", "Value"]
    print(f"Table: {selected_table}")

    for i in range(len(q_entries)):
        x = q_entries[i].get()
        print(q_words[i], ": ", x)            
        
    
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
    value_entry = tk.Entry(field_frame)
    value_entry.pack()

    # q_entries.append((column_var, op_var, value_entry))
    q_entries.append(column_var)
    q_entries.append(op_var)
    q_entries.append(value_entry)

def show_more(*args):
    global checked 

    #what table?
    x = from_var.get()
    print(x)
    #add column label
    q_more_column_label = tk.Label(more_frame, text="COLUMN")
    more_frame.pack_forget()
    q_more_column_label.pack()
    more_frame.pack()
    # button.pack_forget()
    if checked:
        more_frame.pack_forget()
        checked = not checked
    else:
        more_frame.pack()
        checked = not checked
    # button.pack()

iframe = tk.Frame(root)
qframe = tk.Frame(root)

IQ_selected = tk.StringVar(value="Select")
IQ_selected.trace_add('write', IQ_change_frame)
drop = tk.OptionMenu(root, IQ_selected, "Insert", "Query")
drop.pack(pady=10)


"""INSERT FRAME"""
i_table_label = tk.Label(iframe, text="TABLE")
i_table_drop_var = tk.StringVar(value="Choose Table")
i_table_drop_var.trace_add('write', i_table_frame)
i_table_drop = tk.OptionMenu(iframe, i_table_drop_var, *tables.keys())

i_button = tk.Button(iframe, text="Submit Info" ,command=i_submit)

i_entries = []

i_table_label.pack()
i_table_drop.pack()

"""IFRAME USERS"""
iframe_users = tk.Frame(iframe)

for attribute in tables["Users"]:
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
q_columns_user_drop = tk.OptionMenu(qframe_users, q_columns_user_var, *tables["Users"])


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


root.mainloop()