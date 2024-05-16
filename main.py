import tkinter as tk
import time


class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        master.title("Pomodoro Timer")
        master.attributes("-topmost", True)
        master.overrideredirect(True)
        master.attributes("-toolwindow", True)


        self.manual_reset = False
        # Set the icon
        icon_path = "app.ico"  # Replace this with the path to your icon
        master.iconbitmap(icon_path)
        
        self.break_window_visible = False
        self.is_running = False
        self.remaining_time = 25 * 60  # Initial time in seconds

        self.timer_minutes_entry = tk.Entry(master)
        self.timer_minutes_entry.pack(side=tk.LEFT)
        self.timer_minutes_entry.insert(0, "25")

        self.timer_seconds_entry = tk.Entry(master)
        self.timer_seconds_entry.pack(side=tk.LEFT)
        self.timer_seconds_entry.insert(0, "0")

        self.start_button = tk.Button(master, text="▶", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(master, text="⏸", command=self.pause_timer, state="disabled")
        self.pause_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(master, text="🍤", command=self.reset_timer, state="disabled")
        self.reset_button.pack(side=tk.LEFT)

        self.timer_display = tk.Label(master, text="", font=("Helvetica", 14))
        self.timer_display.pack(side=tk.LEFT)

        self.state_label = tk.Label(master, text="Timer", font=("Helvetica", 8))
        # self.state_label.pack(side=tk.LEFT)

        # Add minimize button
        self.minimize_button = tk.Button(master, text="➖", command=self.minimize_window)
        self.minimize_button.pack(side=tk.LEFT)

        # Add close button
        self.close_button = tk.Button(master, text="❌", command=self.close_window)
        self.close_button.pack(side=tk.LEFT)

        self.update_timer_display()

        # break window

        self.break_window = tk.Toplevel(master)
        self.break_window.attributes("-fullscreen", True)
        self.break_window.title("Take a Break")
        self.break_window.withdraw()
        self.break_label = tk.Label(self.break_window, text="Take a Break", font=("Helvetica", 36))
        self.break_label.pack()

    def show_break_window(self):
        
        self.break_label.pack(expand=True)

    def minimize_window(self):
        self.master.iconify()

    def close_window(self):
        self.master.destroy()

    def start_timer(self):
        if not self.is_running:
            timer_minutes = int(self.timer_minutes_entry.get())
            timer_seconds = int(self.timer_seconds_entry.get())
            self.remaining_time = timer_minutes * 60 + timer_seconds  # Convert minutes and seconds to seconds
            self.timer_minutes_entry.config(state="disabled")
            self.timer_seconds_entry.config(state="disabled")

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

        # Check if the timer has reached zero
        if self.remaining_time == 0:
            self.update_timer_display()  # Update the timer display to show "00:00"
            self.show_break_window()     # Show the break window if needed
        else:
            # Reset the remaining time to the initial value
            self.remaining_time = 25 * 60  # Initial time in seconds

        self.update_state_label("Timer Stopped")
        self.timer_minutes_entry.config(state="normal")
        self.timer_seconds_entry.config(state="normal")

    def update_state_label(self, state):
        self.state_label.config(text=state)

    def update_timer_display(self):
        mins, secs = divmod(self.remaining_time, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        self.timer_display.config(text=time_format)


def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
