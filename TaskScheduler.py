import tkinter as tk
import tkinter.messagebox
from tkinter import Canvas, PhotoImage
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import pickle
from twilio.rest import Client


# Create the GUI window
root = tk.Tk()
root.title("Task Scheduler" + " - " + time.strftime("%x"))
root.geometry("600x400")


# Load the background image
bg_image = tk.PhotoImage(file="bg.png")  # Replace with the actual path to your image

# Resize the image to fit the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
bg_image = bg_image.subsample(bg_image.width() // screen_width, bg_image.height() // screen_height)

# Create a label with the background image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place the label in the root window to cover the entire window

# Twilio configuration
twilio_account_sid = "AC78313ef28f483346a9877aa8c1a4f150"  # Replace with your Twilio Account SID
twilio_auth_token = "498fd9f47160e2b64183144329c47ed3"    # Replace with your Twilio Auth Token
twilio_phone_number = "+18559222977"  # Replace with your Twilio phone number   

def send_email(subject, message, sender_email, receiver_email, password):
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    # Create SMTP session
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)

        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())

def send_sms(to_phone_number, body):
    # Create a Twilio client
    client = Client(twilio_account_sid, twilio_auth_token)

    # Send SMS
    client.messages.create(
        to=to_phone_number,
        from_=twilio_phone_number,
        body=body
    )

def task():
    # Update the label text
    status_label.config(text="Running task...")

    # Add your task logic here
    print("Running task...")
    # Send email notification
    sender_email = "raffp737@gmail.com"
    receiver_email = "helmervaldivia@gmail.com"
    password = "yyxnozacwqebosfo"
    subject = "Am Your Daddy!"
    message = "You come here often? 😉"
    send_email(subject, message, sender_email, receiver_email, password)

    # Update the label text
    status_label.config(text="Task completed.")

def update_status_label():
    while True:
        schedule.run_pending()
        time.sleep(1)
        root.update()

def email_to_do_list():
    # Get the list of tasks from the listbox
    tasks = listbox_tasks.get(0, tk.END)
    
    # Convert the list of tasks to a string
    task_list_str = "\n".join(tasks)

    # Email details
    sender_email = "your_email@gmail.com"  # Replace with your Gmail email
    receiver_email = "receiver_email@example.com"  # Replace with the recipient's email
    password = "your_gmail_password"  # Replace with your Gmail password
    subject = "To-Do List"
    message = f"Here is your To-Do List:\n\n{task_list_str}"

    # Send the email
    send_email(subject, message, sender_email, receiver_email, password)

    # Update the label text
    status_label.config(text="To-Do List sent.")

def text_to_do_list():
    # Get the list of tasks from the listbox
    tasks = listbox_tasks.get(0, tk.END)

    # Convert the list of tasks to a string
    task_list_str = "\n".join(tasks)

    # Phone number to send SMS (replace with your phone number)
    phone_number = "+17759902821"  # Replace with your phone number

    # Text message body
    message = f"Rafa1:\n\n{task_list_str}"

    # Send the SMS
    send_sms(phone_number, message)

    # Update the label text
    status_label.config(text="To-Do List sent via SMS.")




# Style for the labels and buttons
label_style = ("Arial", 12)
button_style = ("Arial", 12, "bold", "underline")

# Label to display task status
status_label = tk.Label(root, text="What are we doing today ✅", font=label_style)
status_label.pack(pady=20)

# Start button
start_button = tk.Button(root, text="Start", font=button_style, width=10, command=lambda: start_scheduler())
start_button.pack(pady=10)

# Scroll bar
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Schedule your task at 5:00 PM
schedule.every().day.at("17:20").do(task)

# Function to start the task scheduler
def start_scheduler():
    start_button.config(state="disabled")
    status_label.config(text="Task scheduler started.")
    status_thread = threading.Thread(target=update_status_label)
    status_thread.start()

def add_task():
    task_text = entry_task.get().strip()  # Get the task string from the entry box and remove leading/trailing spaces
    if task_text:
        listbox_tasks.insert(tk.END, task_text)
        entry_task.delete(0, tk.END)  # Clear the entry box
    else:
        tk.messagebox.showwarning(title="Warning!", message="You must enter a task.")

def delete_task():
    try:
        task_index = listbox_tasks.curselection()[0]  # Get the selected task index
        listbox_tasks.delete(task_index)  # Delete the selected task from the list
    except IndexError:
        pass

def load_tasks():
    try:
        tasks = pickle.load(open("tasks.txt", "rb"))  # Load the saved tasks from the tasks.txt file
        for task in tasks:
            listbox_tasks.insert(tk.END, task)  # Insert each task into the listbox
    except FileNotFoundError:
        tk.messagebox.showwarning(title="File Not Found", message="No saved tasks found.")

def save_tasks():
    tasks = listbox_tasks.get(0, tk.END)
    pickle.dump(tasks, open("tasks.txt", "wb"))
    
    # Update the label text
    status_label.config(text="Tasks saved.")

# Bind the start_scheduler function to the Start button
start_button.config(command=start_scheduler)

listbox_tasks = tk.Listbox(root, height=5, width=50)
listbox_tasks.pack()

# Create a text box to enter new tasks and bind it to the add_task function by pressing Enter key
entry_task = tk.Entry(root, width=50)
entry_task.pack()

# Create a button to add new tasks to the list
button_add_task = tk.Button(root, text="Add task", width=48, command=add_task, relief=tk.SOLID)
button_add_task.pack()

# Create a button to delete selected tasks from the list
button_delete_task = tk.Button(root, text="Delete task", width=48, command=delete_task, relief=tk.SOLID)
button_delete_task.pack()

# Load saved tasks from the tasks.txt file
button_load_tasks = tk.Button(root, text="Load tasks", width=48, command=load_tasks, relief=tk.SOLID)
button_load_tasks.pack()

button_save_tasks = tk.Button(root, text="Save tasks", width=48, command=save_tasks, relief=tk.SOLID)
button_save_tasks.pack()

# Create a button to email the to-do list
button_email_list = tk.Button(root, text="Email To-Do List", width=48, command=email_to_do_list, relief=tk.SOLID)
button_email_list.pack()

# Create a button to text the to-do list
button_text_list = tk.Button(root, text="Text To-Do List", width=48, command=text_to_do_list, relief=tk.SOLID)
button_text_list.pack()

  
# Run the GUI event loop
root.mainloop()

