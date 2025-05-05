import tkinter as tk
import backend

tables = {
    "Users": ["Username", "Soc_Med", "Name", "Verified", "Country_Birth", "Country_Res", "Age", "Gender"],
    "Post": ["Username", "Soc_Med", "Time_Posted", "City", "State", "Country", "Multimedia", "Likes", "Dislikes", "Text", "Poster_OG", "Time_OG"],
    "Project": ["Name", "Manager", "Institute", "Start_Date", "End_Date"],
    "Record": ["Project", "Text", "Fields", "Username", "Time_Posted", "Soc_Med"]
}

root = tk.Tk()
root.geometry("750x800")
root.title("Databases")

def change_frame(*args):
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
    print("SUBMITTED")
    entries = []
    for i in i_entries:
        entries.append(i.get())
        i.delete(0, tk.END)
    print(entries)
    # backend call to actually query db for insert
    ec = backend.enterTuple(entries)
    if ec == 1:
        # show input invalid
        pass
    
    # for e in entries:
    #     print(e)


def update_columns(*args):
    if from_var.get() == "Users":
        # print("Hello")
        #show usersQ_frame
        qframe_users.pack()
    else:
        # print("Goodbye")
        qframe_users.pack_forget()

def do_something(table):
    # print(q_users_entry.get())
    # q_users_entry.delete(0, tk.END)
    entries = [e.get() for e in q_entries]
    print(table.get())
    for e in entries:
        # if isinstance(e, tk.Entry):
        print(e)
        # else:
        #     print(e.get())
    
def show_more(*args):
    global checked 
    if not checked:
        qframe_users_more.pack()
        checked = not checked
    else:
        qframe_users_more.pack_forget()
        checked = not checked

iframe = tk.Frame(root)
qframe = tk.Frame(root)

IQ_selected = tk.StringVar(value="Select")
IQ_selected.trace_add('write', change_frame)
drop = tk.OptionMenu(root, IQ_selected, "Insert", "Query")
drop.pack(pady=10)

# word = tk.StringVar(value="Hello")
# label = tk.Label(iframe, text="hello")
# label.pack()
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
from_label = tk.Label(qframe, text="FROM")
from_label.pack()
from_var = tk.StringVar(qframe, value="Choose")
from_var.trace_add('write', update_columns)
from_drop = tk.OptionMenu(qframe, from_var, *tables.keys())
from_drop.pack()

q_entries = []

"""USERS"""
qframe_users = tk.Frame(qframe)
qframe_users_more = tk.Frame(qframe_users)


q_users_drop_var = tk.StringVar(qframe_users, value="Choose")
q_users_drop = tk.OptionMenu(qframe_users, q_users_drop_var, "=", "<", "<=", ">=", ">", "!=")

q_users_label_value = tk.Label(qframe_users, text="VALUE")
q_users_entry_value = tk.Entry(qframe_users)
q_users_label_socmed = tk.Label(qframe_users, text="Social Media")
button = tk.Button(qframe_users, text="button", command=lambda: do_something(from_var))


q_users_label_value.pack()
q_users_entry_value.pack()
button.pack()

"""MORE"""
checked = False
check_button = tk.Button(qframe_users, text="more", command=show_more)
check_button.pack()

l = tk.Label(qframe_users_more, text="MORE")
l.pack()


root.mainloop()