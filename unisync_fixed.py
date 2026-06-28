import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import calendar
import webbrowser
import os

BASE_IDR = os.path.dirname(os.path.abspath(__file__))

current_user = None  # Global variable to track logged-in user

# Function to convert RGB to hex
def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

# Welcome page
def show_welcome(name):
    clear_screen()

    canvas.config(bg=rgb_to_hex((249, 246, 241)))

    sprinkles = []
    colors = ["#ff6f61", "#6b5b95", "#88b04b", "#f7cac9", "#92a8d1", "#955251", "#b565a7"]

    for _ in range(50):
        x = random.randint(0, screen_width)
        y = random.randint(-screen_height, 0)
        color = random.choice(colors)
        sprinkle = canvas.create_oval(x, y, x+10, y+10, fill=color, outline="")
        speed = random.randint(5, 10)
        sprinkles.append((sprinkle, speed))

    def animate_sprinkles():
        for sprinkle, speed in sprinkles:
            pos = canvas.coords(sprinkle)
            if len(pos) < 2:
                continue

            canvas.move(sprinkle, 0, speed)
            pos = canvas.coords(sprinkle)

            if len(pos) >= 2 and pos[1] > screen_height:
                canvas.move(sprinkle, 0, -screen_height)

        canvas.after(40, animate_sprinkles)

    animate_sprinkles()

    # Display welcome message
    welcome_label = tk.Label(root, text=f"Welcome {name}!", font=("Century Schoolbook L", 28, "bold"),
                             bg=rgb_to_hex((249, 246, 241)), fg=rgb_to_hex((27, 100, 152)))
    welcome_label.place(relx=0.5, rely=0.3, anchor="center")

    # After 5 seconds, go to homepage
    root.after(5000, lambda: fade_to_homepage(name, sprinkles))

# Function to fade out and go to homepage
def fade_to_homepage(name, sprinkles):
    for sprinkle, _ in sprinkles:
        canvas.delete(sprinkle)

    show_homepage(name)

# Cards 
def create_card(title, emoji, relx, rely, command):

    card_width = 450
    card_height = 350
    card_frame = tk.Frame(root, bg=rgb_to_hex((240, 240, 240)), bd=5, relief="groove", width=card_width, height=card_height)
    card_frame.place(relx=relx, rely=rely, anchor="center")
    
    card_img = Image.open(os.path.join(BASE_IDR, f"{title.lower()}_img.png"))
    card_img = card_img.resize((300, 300))
    card_img_tk = ImageTk.PhotoImage(card_img)
    
    card_img_label = tk.Label(card_frame, image=card_img_tk)
    card_img_label.image = card_img_tk
    card_img_label.pack(pady=10)

    card_text = tk.Label(card_frame, text=f"{emoji} {title}", font=("Helvetica", 20), bg=rgb_to_hex((240, 240, 240)))
    card_text.pack()

    card_frame.bind("<Button-1>", command)
    card_img_label.bind("<Button-1>", command)

# Logout function
def logout():
    clear_screen()
    
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.image = bg_photo

    # Login form
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    messagebox.showinfo("Logged out", "Successfully logged out!")

# Homepage function
def show_homepage(name):
    clear_screen()

    home_bg_image = Image.open(os.path.join(BASE_IDR, "home_bg.jpeg"))
    home_bg_image = home_bg_image.resize((screen_width, screen_height))
    home_bg_photo = ImageTk.PhotoImage(home_bg_image)

    canvas.create_image(0, 0, image=home_bg_photo, anchor="nw")
    canvas.image = home_bg_photo

    # Welcome text
    welcome_label = tk.Label(root, text=f"Welcome {name}! 😊", font=("Century Schoolbook L", 28, "bold"),
                             bg=rgb_to_hex((167, 214, 224)), fg=rgb_to_hex((27, 100, 152)))
    welcome_label.place(relx=0.5, rely=0.2, anchor="center")

    # Create cards for Calendar, events, To-Do List
    create_card("Calendar", "📅", 0.2, 0.6, lambda event: show_calendar(event, name))
    create_card("Events", "📝", 0.5, 0.6, lambda event: events_click(event, name))
    create_card("Todo", "✅", 0.8, 0.6, lambda event: todo_click(event, name))

    logout_button = tk.Button(root, text="Logout", font=("Helvetica", 14, "bold"), bg=rgb_to_hex((127, 130, 187)), fg="white",
                              command=logout)
    logout_button.place(relx=0.95, rely=0.05, anchor="ne")

def show_calendar(event, name=None):
    clear_screen()

    calendar_bg_image = Image.open(os.path.join(BASE_IDR, "may_bg.png"))
    calendar_bg_image = calendar_bg_image.resize((screen_width, screen_height))
    calendar_bg_photo = ImageTk.PhotoImage(calendar_bg_image)

    canvas.create_image(0, 0, image=calendar_bg_photo, anchor="nw")
    canvas.image = calendar_bg_photo

    # Get the calendar for May 2025
    month_name = "May"
    year = 2025
    month = calendar.monthcalendar(year, 5)

    # Create buttons for each date
    button_width = 8  
    button_height = 2  
    x_start = 0.18      
    y_start = 0.42     
    x_gap = 0.11       
    y_gap = 0.12       

    for i, week in enumerate(month):
        for j, day in enumerate(week):
            if day != 0: 
                if j == 5 or j == 6: 
                    day_button = tk.Button(root, text=str(day), width=button_width, height=button_height,
                                           command=lambda day=day: show_relax_day(day),
                                           font=("Helvetica", 16, "bold"), bg="#F7CAC9", fg="#333",
                                           relief="ridge", bd=3)
                else:
                    day_button = tk.Button(root, text=str(day), width=button_width, height=button_height,
                                           command=lambda day=day, weekday=j: show_timetable(day, weekday),
                                           font=("Helvetica", 16, "bold"), bg="#92A8D1", fg="white",
                                           relief="ridge", bd=3)

                day_button.place(relx=x_start + j * x_gap, rely=y_start + i * y_gap, anchor="center")

    if name:
        back_button = tk.Button(root, text="← Back", font=("Helvetica", 14, "bold"),
                                bg=rgb_to_hex((54,126,127)), fg="white", command=lambda: show_homepage(name))
        back_button.place(relx=0.03, rely=0.04)

# Day-wise timetable function
def show_timetable(day, weekday):
    timetable_window = tk.Toplevel(root)
    timetable_window.title(f"Timetable for {day} May 2025")
    timetable_window.geometry("600x400")
    timetable_window.resizable(False, False)

    bg_image = Image.open(os.path.join(BASE_IDR, "tt_bg_2.png"))
    bg_image = bg_image.resize((600, 400))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(timetable_window, width=600, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.image = bg_photo

    timetable_dict = {
        0: "▪️Timetable for Monday▪️\n\n9:00 AM - MVC🔢\n11:00 AM - Physics📚\n1:00 PM - NE🛜\n3:00 PM - SE🌏",
        1: "▪️Timetable for Tuesday▪️\n\n9:00 AM - Chemistry🧪\n11:00 AM - MVC🔢\n1:00 PM - Physics📚\n3:00 PM - EG✏️",
        2: "▪️Timetable for Wednesday▪️\n\n9:00 AM - SE🌏\n11:00 AM - Physics lab👩🏻‍🔬\n1:00 PM - NE🛜\n3:00 PM - EG lab👩🏻‍💻",
        3: "▪️Timetable for Thursday▪️\n\n9:00 AM - MVC🔢\n11:00 AM - Physics📚\n1:00 PM - EG✏️\n3:00 PM - PSP💻",
        4: "▪️Timetable for Friday▪️\n\n9:00 AM - Physics📚\n11:00 AM - Chemistry🧪\n1:00 PM - MVC🔢\n3:00 PM - PSP💻",
    }

    timetable = timetable_dict.get(weekday, "No timetable available")

    # Add timetable
    canvas.create_text(
        300, 200,
        text=timetable,
        font=("Segoe UI Emoji", 22, "bold"),
        fill=rgb_to_hex((0,12,123)),
        justify="center"
    )

# Function for weekends
def show_relax_day(day):
    relax_window = tk.Toplevel(root)
    relax_window.title(f"Relax Day for {day} May 2025")
    relax_window.geometry("400x400")
    relax_window.resizable(False, False)

    bg_image = Image.open(os.path.join(BASE_IDR, "relax_bg.jpg"))
    bg_image = bg_image.resize((400, 400))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(relax_window, width=400, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.image = bg_photo

# Function to add new task in to-do list
def add_new_task(event):
    add_task_window = tk.Toplevel(root)
    add_task_window.title("New Task")
    add_task_window.geometry("300x150")
    add_task_window.resizable(False, False)

    tk.Label(add_task_window, text="Enter task:").pack(pady=5)
    new_task_entry = tk.Entry(add_task_window, width=30)
    new_task_entry.pack(pady=10)

    # Function to save task info
    def save_new_task():
        task_name = new_task_entry.get()
        if task_name.strip() == "":
            return  # Don't save empty tasks

        filename = f"{current_user}_tasks.txt"
        with open(filename, "a+") as f:
            f.write(task_name + "\n")

        with open(filename, "r") as f:
            tasks = f.readlines()

        index = len(tasks) - 1

        # Create task label
        task_label = tk.Label(root, text=task_name, width=25, height=2, font=("Times New Roman", 20),
                           anchor="w")
        task_label.place(relx=0.4, rely=(0.2 + index * 0.1))
        task_label.config(bg=rgb_to_hex((195, 184, 214)))

        delete_button = tk.Button(root, text="✅", fg="white", bg="green", font=("Helvetica", 16, "bold"),
                              command=lambda t=task_name, l=task_label: delete_task(t, l))
        delete_button.place(relx=0.6, rely=(0.205 + index * 0.1))

        add_task_window.destroy()

    save_button = tk.Button(add_task_window, text="Save", width=10, height=2, command=save_new_task)
    save_button.pack(pady=10)

def delete_task(task, label_widget, delete_button_widget):
    messagebox.showinfo("Task successful", "Well Done! Task completed! 🥳")
    label_widget.destroy()
    delete_button_widget.destroy()
    if current_user:
        filename = f"{current_user}_tasks.txt"
        with open(filename, "r") as f:
            tasks = f.readlines()
        tasks = [t for t in tasks if t.strip() != task]
        with open(filename, "w") as f:
            f.writelines(tasks)

# Events function
def events_click(event, name=None):
    clear_screen()

    events_bg_image = Image.open(os.path.join(BASE_IDR, "events_bg_2.jpg"))
    events_bg_image = events_bg_image.resize((screen_width, screen_height))
    events_bg_photo = ImageTk.PhotoImage(events_bg_image)

    canvas.create_image(0, 0, image=events_bg_photo, anchor="nw")
    canvas.image = events_bg_photo

    title_label = tk.Label(root, text="Upcoming Events", width=20, height=2, font=("French Script MT", 34, "bold"))    
    title_label.place(relx=0.36, rely=0.2)
    title_label.config(bg=rgb_to_hex((254, 241, 224)))

    # Container for scrollable area
    container = tk.Frame(root)
    container.place(relx=0.24, rely=0.4)

    scroll_canvas = tk.Canvas(container, width=820, height=300, bg=rgb_to_hex((254, 241, 224)), highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    scroll_canvas.pack(side="left", fill="both", expand=True)

    # Frame inside Canvas
    scroll_frame = tk.Frame(scroll_canvas, bg=rgb_to_hex((255, 229, 189)))
    window = scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    def on_frame_configure(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    scroll_frame.bind("<Configure>", on_frame_configure)

    # Function for mousewheel scrolling
    def _on_mousewheel(event):
        scroll_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    scroll_canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Add events
    events_data = [
        {"text": "▪️5G Innovation Hackathon 2025: A nationwide initiative to develop 5G solutions.", "url": "https://eservices.dot.gov.in/5ghackathon/"},
        {"text": "▪️Smart India Hackathon (SIH): A platform for students to solve real-world problems. ", "url": "https://scholarshiplearn.com/smart-india-hackathon-sih/"},
        {"text": "▪️Goldman Sachs India Hackathon (GSIH): A coding challenge for undergraduate students. ", "url": "https://www.goldmansachs.com/careers/students/programs-and-internships/india/hackathon"},
        {"text": "▪️Generative AI Hackathon 2025: Part of the BharatGen Summit.", "url": "https://vision.hack2skill.com/event/informatica2025?utm_source=hack2skill&utm_medium=homepage&sectionid=6751859692dd35342702d4d9"},
        {"text": "▪️HackStasy 2025: A high-energy coding marathon designed for tech enthusiasts. ", "url": "https://reskilll.com/hack/hackstasy"},
        {"text": "▪️CSAY India Hackathon 2025: Part of Cyber & Social Awareness Yatra 1.0.", "url": "https://unstop.com/hackathons/csay-india-hackathon-cyber-social-awareness-yatra-csay-10-singhtek-1428144"},
        {"text": "▪️Ideathon 2.0 2025 ", "url": "https://unstop.com/hackathons/ideathon-20-2025-pimpri-chinchwad-university-maharashtra-1433066"},
        {"text": "▪️College Youth Ideathon", "url": "https://youthideathon.in/"}
    ]

    for event_info in events_data:
        label = tk.Label(scroll_frame, text=event_info["text"], font=("Arial", 14),
                         bg=rgb_to_hex((255, 229, 189)), cursor='hand2', anchor="w", justify="left")
        label.pack(pady=10, padx=20, anchor="w")
        label.bind('<Button-1>', lambda e, url=event_info["url"]: webbrowser.open_new(url))
    
    if name:
        back_button = tk.Button(root, text="← Back", font=("Helvetica", 14, "bold"),
                                bg=rgb_to_hex((93,56,29)), fg="white", command=lambda: show_homepage(name))
        back_button.place(relx=0.1, rely=0.12)

def todo_click(event, name=None):
    clear_screen()

    todo_bg_image = Image.open(os.path.join(BASE_IDR, "todo_bg_final.jpeg"))
    todo_bg_image = todo_bg_image.resize((screen_width, screen_height))
    todo_bg_photo = ImageTk.PhotoImage(todo_bg_image)

    canvas.create_image(0, 0, image=todo_bg_photo, anchor="nw")
    canvas.image = todo_bg_photo

    add_task = tk.Button(root, text="Add task +", width=9, height=2, command=lambda: add_new_task(event))
    add_task.place(relx=0.18, rely=0.27)
    add_task.config(bg=rgb_to_hex((247,220,213)), font=("Helvetica", 14, "bold"))

    # Load tasks for current user
    tasks = []
    if current_user:
        filename = f"{current_user}_tasks.txt"
        try:
            with open(filename, "r") as f:
                tasks = f.readlines()
        except FileNotFoundError:
            tasks = []

        for i, task in enumerate(tasks):
            task = task.strip()

            task_label = tk.Label(root, text=task, width=25, height=2, font=("Times New Roman", 20),
                                  anchor="w")
            task_label.place(relx=0.4, rely=(0.2 + i * 0.1))
            task_label.config(bg=rgb_to_hex((195, 184, 214)))

            delete_button = tk.Button(root, text="✅", fg="white", bg="green", font=("Helvetica", 16, "bold"))
            delete_button.place(relx=0.6, rely=(0.205 + i * 0.1))
            delete_button.config(command=lambda t=task, l=task_label, db=delete_button: delete_task(t, l, db))

    if name:
        back_button = tk.Button(root, text="← Back", font=("Helvetica", 14, "bold"),
                                bg=rgb_to_hex((54,126,127)), fg="white", command=lambda: show_homepage(name))
        back_button.place(relx=0.03, rely=0.04)


# Function to clear current screen
def clear_screen():
    for widget in root.winfo_children():
        widget.place_forget()

# Function to validate login
def validate_login():
    global current_user
    username = entry_name.get()
    password = entry_password.get()

    if username == "Anushree" and password == "961":
        current_user = "Anushree"
        show_welcome("Anushree")
    elif username == "Anushka" and password == "971":
        current_user = "Anushka"
        show_welcome("Anushka")
    elif username == "Tanvi" and password == "963":
        current_user = "Tanvi"
        show_welcome("Tanvi")
    elif username == "Hiral" and password == "964":
        current_user = "Hiral"
        show_welcome("Hiral")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Splash screen
splash = tk.Tk()
splash.overrideredirect(True)  # Hide window borders
splash.state('zoomed')

screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()

logo_image = Image.open(os.path.join(BASE_IDR, "logo.png"))
logo_image = logo_image.resize((screen_width, screen_height))
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(splash, image=logo_photo)
logo_label.pack(fill="both", expand=True)

# After 4 seconds, destroy splash and show login page
splash.after(4000, splash.destroy)
splash.mainloop()

# Main app window
root = tk.Tk()
root.title("UniSync")
root.state('zoomed')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

bg_image = Image.open(os.path.join(BASE_IDR, "login_bg_2.jpeg"))
bg_image = bg_image.resize((screen_width, screen_height))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

form_frame = tk.Frame(root, bg=rgb_to_hex((249,246,241)), bd=5)
form_frame.place(relx=0.5, rely=0.5, anchor="center")

label_font = ("Helvetica", 28)
entry_font = ("Helvetica", 18)
button_font = ("Helvetica", 20)

label_name = tk.Label(form_frame, text="Name", font=label_font, bg=rgb_to_hex((249,246,241)))
entry_name = tk.Entry(form_frame, font=entry_font, width=20, bg=rgb_to_hex((240, 240, 240)))

label_password = tk.Label(form_frame, text="Password", font=label_font, bg=rgb_to_hex((249,246,241)))
entry_password = tk.Entry(form_frame, show="*", font=entry_font, width=20, bg=rgb_to_hex((240, 240, 240)))

button_login = tk.Button(form_frame, text="Login", command=validate_login, font=button_font, bg=rgb_to_hex((77, 177, 174)), fg="white", width=10, height=1)

label_name.grid(row=0, column=0, pady=15, padx=15, sticky="e")
entry_name.grid(row=0, column=1, pady=15, padx=15)

label_password.grid(row=1, column=0, pady=15, padx=15, sticky="e")
entry_password.grid(row=1, column=1, pady=15, padx=15)

button_login.grid(row=2, column=0, columnspan=2, pady=30)

root.mainloop()