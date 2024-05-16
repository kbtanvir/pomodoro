import tkinter as tk

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        master.title("Pomodoro Timer")
        master.attributes("-topmost", True)
        # master.overrideredirect(True)
        master.attributes("-toolwindow", True)

        # Set the icon
        icon_path = "app.ico"  # Replace this with the path to your icon
        master.iconbitmap(icon_path)

        self.is_running = False
        self.remaining_time = 25 * 60  # Initial time in seconds

        self.minutes_input = tk.Entry(master, width=5)
        self.minutes_input.insert(0, "0")
        self.minutes_input.pack(side=tk.LEFT)

        self.seconds_input = tk.Entry(master, width=5)
        self.seconds_input.insert(0, "3")
        self.seconds_input.pack(side=tk.LEFT)

        self.start_button = tk.Button(master, text="▶", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(master, text="⏸", command=self.pause_timer, state="disabled")
        self.pause_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(master, text="🍤", command=self.reset_timer, state="disabled")
        self.reset_button.pack(side=tk.LEFT)

        self.timer_display = tk.Label(master, text="", font=("Helvetica", 14))
        self.timer_display.pack(side=tk.LEFT)

        self.break_label = tk.Label(master, text="Take Break", font=("Helvetica", 14))
        self.break_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.break_label.place_forget()

        self.state_label = tk.Label(master, text="Timer", font=("Helvetica", 8))
        # self.state_label.pack(side=tk.LEFT)

        # Add minimize button
        self.minimize_button = tk.Button(master, text="➖", command=self.minimize_window)
        self.minimize_button.pack(side=tk.LEFT)

        # Add close button
        self.close_button = tk.Button(master, text="❌", command=self.close_window)
        self.close_button.pack(side=tk.LEFT)

        self.update_timer_display()

    def minimize_window(self):
        self.master.iconify()

    def close_window(self):
        self.master.destroy()

    def start_timer(self):
        self.master.attributes("-fullscreen", False)
        self.break_label.place_forget()

        if not self.is_running:
            minutes = int(self.minutes_input.get())
            seconds = int(self.seconds_input.get())
            self.remaining_time = minutes * 60 + seconds
            self.is_running = True
            self.start_button.config(state="disabled")
            self.pause_button.config(state="normal")
            self.reset_button.config(state="normal")
            self.update_state_label("Timer Running")
            self.run_timer()

    def run_timer(self):
        if self.remaining_time <= 0:
            self.reset_timer()
            return
        mins, secs = divmod(self.remaining_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.timer_display.config(text=time_format)
        self.remaining_time -= 1

        if self.remaining_time == 0:
            self.master.attributes("-fullscreen", True)
            self.timer_display.lower()  # Lower timer_display
            self.break_label.lift()  # Raise break_label

        self.timer_id = self.master.after(1000, self.run_timer)

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(state="normal")
            self.pause_button.config(state="disabled")
            self.master.after_cancel(self.timer_id)  # Cancel the scheduled update
            self.update_state_label("Timer Paused")

    def reset_timer(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.master.after_cancel(self.timer_id)  # Cancel the scheduled update
        # self.master.attributes("-fullscreen", False)  # Exit full-screen mode
        self.remaining_time = 25 * 60
        self.update_timer_display()
        self.update_state_label("Timer Stopped")
        self.break_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Hide break_label

    def update_state_label(self, state):
        self.state_label.config(text=state)

    def update_timer_display(self):
        mins, secs = divmod(self.remaining_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.timer_display.config(text=time_format)


def main():
    root = tk.Tk()
    PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
