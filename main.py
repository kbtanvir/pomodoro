import sys
import tkinter as tk
from ttkthemes import ThemedTk, ThemedStyle
from tkinter import PhotoImage, ttk, filedialog
from PIL import Image, ImageTk


class AppState:
    def __init__(self):
        self.is_running = False
        self.is_fullscreen = False
        self.is_sticky = False
        self.remaining_time = 0
        self.geometry = "280x180"
        self.current_timer = 'main'  # Added attribute to track current timer type


class TimerDisplay(tk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.config(font=("Helvetica", 40, 'bold'))
        self.grid(row=0, column=1, padx=5)


class TimeInput(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.minutes_label = tk.Label(self, text="Work", font=("Helvetica", 12))
        self.minutes_label.grid(row=0, column=0, padx=5)

        self.work_duration_input = ttk.Entry(self, width=5, font=("Helvetica", 12))
        self.work_duration_input.insert(0, "25")
        self.work_duration_input.grid(row=0, column=1, padx=5)

        # self.seconds_label = tk.Label(self, text="Seconds:", font=("Helvetica", 12))
        # self.seconds_label.grid(row=0, column=2, padx=5)

        # self.seconds_input = ttk.Entry(self, width=5, font=("Helvetica", 12))
        # self.seconds_input.insert(0, "0")
        # self.seconds_input.grid(row=0, column=3, padx=5, pady=5)

        self.break_duration_label = tk.Label(self, text="Break", font=("Helvetica", 12))
        self.break_duration_label.grid(row=0, column=2, padx=5)

        self.break_duration_input = ttk.Entry(self, width=5, font=("Helvetica", 12))
        self.break_duration_input.insert(0, "5")  # Default break duration
        self.break_duration_input.grid(row=0, column=3, padx=5)

        self.grid(row=1, column=1, padx=5)


class App(ThemedTk):
    def __init__(self, state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state: AppState = state
        self.style = ThemedStyle(self)
        self.set_theme("arc")
        self.iconbitmap(default='app.ico')
        # self.wm_attributes('-transparentcolor', '#ab23ff')
        self.title("Pomodoro Timer")
        self.geometry(self.state.geometry)
        self.attributes("-topmost", True)

        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(pady=0)

        self.timer_display = TimerDisplay(self.controls_frame, text="00:00")
        self.time_input = TimeInput(self.controls_frame)
        self.control_handler = CommandHandler(self)
        self.control_buttons = Buttons(self.controls_frame, self.control_handler)
        self.timer_id = None

        self.bind("<Button-1>", self.toggle_sticky_on_click)

        # Initialize background label

        self.background_label = tk.Label(self)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Set default background image

        default_image_path = "R.jpg"  # Change this to the path of your default image
        default_image = Image.open(default_image_path)
        self.default_photo_image = ImageTk.PhotoImage(default_image)
        self.background_label.config(image=self.default_photo_image)

        # Raise background label to the bottom of the stacking order

        self.background_label.lower()

    def toggle_sticky_on_click(self, event):
        if self.state.is_sticky:
            self.control_handler.toggle_sticky()

    def run_timer(self):
        if self.state.remaining_time <= 0:
            if self.state.current_timer == 'main':
                # If main timer ends, switch to break timer
                self.state.remaining_time = int(self.time_input.break_duration_input.get()) * 60
                self.state.current_timer = 'break'
            else:
                # If break timer ends, switch back to main timer
                self.state.remaining_time = int(self.time_input.work_duration_input.get()) * 60
                # + int(self.time_input.seconds_input.get())
                self.state.current_timer = 'main'
            self.update_timer_display()

            self.run_timer()  # Start the new timer immediately
            return
        mins, secs = divmod(self.state.remaining_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.timer_display.config(text=time_format)
        self.state.remaining_time -= 1
        self.timer_id = self.after(1000, self.run_timer)
        if self.state.remaining_time == 0 and self.state.current_timer == 'main' and self.state.is_fullscreen == False:
            self.control_handler.toggle_fullscreen()

    def update_timer_display(self):
        mins, secs = divmod(self.state.remaining_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.timer_display.config(text=time_format)


class CommandHandler:
    def __init__(self, app: App):
        self.app = app

        self.break_label = None

    def select_background_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            try:
                image = Image.open(file_path)
                photo_image = ImageTk.PhotoImage(image)
                if self.app.background_label:
                    self.app.background_label.config(image=photo_image)
                else:
                    self.app.background_label = tk.Label(self.app, image=photo_image)
                    self.app.background_label.place(x=0, y=0, relwidth=1, relheight=1)
                    # Raise background label to the bottom of the stacking order
                    self.app.background_label.lower()
                self.app.background_label.image = photo_image
            except Exception as e:
                print("Error loading image:", e)

    def start_timer(self):
        if not self.app.state.is_running:
            if self.app.state.remaining_time == 0:
                # If no remaining time is stored, initialize from input fields
                minutes = int(self.app.time_input.work_duration_input.get())
                # seconds = int(self.app.time_input.seconds_input.get())
                self.app.state.remaining_time = minutes * 60
                # + seconds
            self.app.state.is_running = True
            self.app.control_buttons.start_button.config(state="disabled")
            self.app.control_buttons.pause_button.config(state="normal")
            self.app.control_buttons.reset_button.config(state="normal")
            self.app.run_timer()

    def pause_timer(self):
        if self.app.state.is_running:
            self.app.state.is_running = False
            self.app.control_buttons.start_button.config(state="normal")
            self.app.control_buttons.pause_button.config(state="disabled")
            self.app.after_cancel(self.app.timer_id)

    def reset_timer(self):
        self.app.state.is_running = False
        self.app.control_buttons.start_button.config(state="normal")
        self.app.control_buttons.pause_button.config(state="disabled")
        self.app.control_buttons.reset_button.config(state="disabled")
        self.app.after_cancel(self.app.timer_id)
        self.app.state.remaining_time = int(self.app.time_input.work_duration_input.get()) * 60
        # + int(self.app.time_input.seconds_input.get())
        self.app.update_timer_display()

    def toggle_fullscreen(self):
        # if self.app.state.current_timer == 'break':
        #     return

        if not self.app.state.is_fullscreen:
            self.app.overrideredirect(False)
            self.app.attributes("-fullscreen", True)
            self.app.state.is_fullscreen = True
            self.show_break_text()
        else:

            self.app.attributes("-fullscreen", False)
            self.app.state.is_fullscreen = False
            self.hide_break_text()

        self.app.control_buttons.sticky_button.config(state='disabled' if self.app.state.is_fullscreen else 'normal')

    def toggle_sticky(self):
        if not self.app.state.is_sticky:
            self.app.state.is_sticky = True
            self.app.attributes("-topmost", True)
            self.app.geometry('85x40')
            self.app.overrideredirect(True)
            # Adjust timer display font and position
            self.app.timer_display.config(font=("Helvetica", 20))
            self.app.timer_display.grid(row=0, column=0, padx=5)
        else:
            self.app.state.is_sticky = False
            self.app.attributes("-topmost", False)
            self.app.geometry(self.app.state.geometry)
            self.app.overrideredirect(False)
            # Restore timer display font and position
            self.app.timer_display.config(font=("Helvetica", 40, "bold"))
            self.app.timer_display.grid(row=0, column=1, padx=5)

    def show_break_text(self):
        if not self.break_label:
            # Create the label if it doesn't exist

            self.break_label = tk.Label(
                self.app,
                text="Take a break",
                font=("Helvetica", 30), fg="white", bg="black"
            )

        self.break_label.place(relx=0.5, rely=0.5, anchor="center")  # Centered both vertically and horizontally

    def hide_break_text(self):
        if self.break_label:
            # Hide the label if it exists
            self.break_label.place_forget()


class Buttons(tk.Frame):
    def __init__(self, master, command_handler: CommandHandler, **kwargs):
        super().__init__(master, **kwargs)
        self.command_handler = command_handler
        self.start_button = ttk.Button(self, text="Start", command=self.command_handler.start_timer)
        self.start_button.grid(row=0, column=0, padx=0, pady=0)

        self.pause_button = ttk.Button(self, text="Pause", state="disabled", command=self.command_handler.pause_timer)
        self.pause_button.grid(row=0, column=1, padx=0, pady=0)

        self.reset_button = ttk.Button(self, text="Reset", state="disabled", command=self.command_handler.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=0, pady=0)

        self.full_screen_button = ttk.Button(self, text="Full Screen", command=self.command_handler.toggle_fullscreen)
        self.full_screen_button.grid(row=1, column=0, padx=0, pady=0)

        self.sticky_button = ttk.Button(self, text="Sticky", command=self.command_handler.toggle_sticky)
        self.sticky_button.grid(row=1, column=1, padx=0, pady=0)

        self.select_image_button = ttk.Button(
            self, text="BG",
            command=self.command_handler.select_background_image
        )
        self.select_image_button.grid(row=1, column=2, padx=5, pady=5)

        self.grid(row=2, column=1, padx=10, pady=10)


def main():
    state = AppState()
    app = App(state)
    app.mainloop()


if __name__ == "__main__":
    main()
