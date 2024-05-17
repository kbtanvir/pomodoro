import tkinter as tk
from tkinter import ttk


class AppState:
    def __init__(self):
        self.is_running = False
        self.is_fullscreen = False
        self.is_sticky = False
        self.remaining_time = 0
        self.geometry = "320x180"


class TimerDisplay(tk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.config(font=("Helvetica", 40))
        self.grid(row=0, column=1, padx=5)


class TimeInput(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.minutes_label = tk.Label(self, text="Minutes:", font=("Helvetica", 12))
        self.minutes_label.grid(row=0, column=0, padx=5)

        self.minutes_input = tk.Entry(self, width=5, font=("Helvetica", 12), bd=2, relief="solid")
        self.minutes_input.insert(0, "0")
        self.minutes_input.grid(row=0, column=1, padx=5)

        self.seconds_label = tk.Label(self, text="Seconds:", font=("Helvetica", 12))
        self.seconds_label.grid(row=0, column=2, padx=5)

        self.seconds_input = tk.Entry(self, width=5, font=("Helvetica", 12), bd=2, relief="solid")
        self.seconds_input.insert(0, "3")
        self.seconds_input.grid(row=0, column=3, padx=5, pady=5)

        self.grid(row=1, column=1, padx=5)


class App(tk.Tk):
    def __init__(self, state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state: AppState = state

        self.title("Pomodoro Timer")
        self.geometry(self.state.geometry)
        self.attributes("-topmost", True)

        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(pady=0)

        self.timer_display = TimerDisplay(self.controls_frame, text="00:00")

        self.time_input = TimeInput(self.controls_frame)

        self.control_handler = CommandHandler(self)

        self.control_buttons = ControlButtons(self.controls_frame, self.control_handler)

        self.timer_id = None

        self.bind("<Button-1>", self.toggle_sticky_on_click)

    def toggle_sticky_on_click(self, event):
        if self.state.is_sticky:
            self.control_handler.toggle_sticky()

    def run_timer(self):
        if self.state.remaining_time <= 0:
            self.control_handler.reset_timer()
            return
        mins, secs = divmod(self.state.remaining_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.timer_display.config(text=time_format)
        self.state.remaining_time -= 1
        self.timer_id = self.after(1000, self.run_timer)
        if self.state.remaining_time == 0:
            self.control_handler.toggle_fullscreen()

    def update_timer_display(self):
        mins, secs = divmod(self.state.remaining_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.timer_display.config(text=time_format)


class CommandHandler:
    def __init__(self, app: App):
        self.app = app

    def start_timer(self):
        if not self.app.state.is_running:
            if self.app.state.remaining_time == 0:
                # If no remaining time is stored, initialize from input fields
                minutes = int(self.app.time_input.minutes_input.get())
                seconds = int(self.app.time_input.seconds_input.get())
                self.app.state.remaining_time = minutes * 60 + seconds
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
        self.app.state.remaining_time = int(self.app.time_input.minutes_input.get()) * 60 + int(
            self.app.time_input.seconds_input.get())
        self.app.update_timer_display()

    def toggle_fullscreen(self):
        if not self.app.state.is_fullscreen:
            self.app.overrideredirect(False)
            self.app.attributes("-fullscreen", True)
            self.app.state.is_fullscreen = True
        else:

            self.app.attributes("-fullscreen", False)
            self.app.state.is_fullscreen = False

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
            self.app.timer_display.config(font=("Helvetica", 40))
            self.app.timer_display.grid(row=0, column=1, padx=5)


class ControlButtons(tk.Frame):
    def __init__(self, master, command_handler: CommandHandler, **kwargs):
        super().__init__(master, **kwargs)
        self.command_handler = command_handler
        self.start_button = ttk.Button(self, text="Start", command=self.command_handler.start_timer)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.pause_button = ttk.Button(self, text="Pause", state="disabled", command=self.command_handler.pause_timer)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)

        self.reset_button = ttk.Button(self, text="Reset", state="disabled", command=self.command_handler.reset_timer)
        self.reset_button.grid(row=1, column=0, padx=5, pady=5)

        self.full_screen_button = ttk.Button(self, text="Full Screen", command=self.command_handler.toggle_fullscreen)
        self.full_screen_button.grid(row=1, column=1, padx=5, pady=5)

        self.sticky_button = ttk.Button(self, text="Sticky", command=self.command_handler.toggle_sticky)
        self.sticky_button.grid(row=2, column=1, padx=5, pady=5)

        self.grid(row=2, column=1, padx=5, pady=5)


def main():
    state = AppState()
    app = App(state)
    app.mainloop()


if __name__ == "__main__":
    main()
