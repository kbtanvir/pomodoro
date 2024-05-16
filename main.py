import tkinter as tk
from tkinter import ttk


class PomodoroTimer:
    def __init__(self, master: tk.Tk):
        self.master = master

        self.master.title("Pomodoro Timer")
        self.master.geometry("320x300")
        self.master.attributes("-topmost", True)

        self.is_running = False
        self.is_fullscreen = False
        self.is_sticky = True
        self.remaining_time = 0

        self.timer_display = tk.Label(self.master, text="", font=("Helvetica", 30))
        self.timer_display.pack(pady=10)

        self.controls_frame = tk.Frame(self.master)
        self.controls_frame.pack(pady=10)

        # ? INPUTS
        # ? -------------------------------

        self.minutes_label = tk.Label(self.controls_frame, text="Minutes:", font=("Helvetica", 12))
        self.minutes_label.grid(row=0, column=0, padx=5)

        self.minutes_input = tk.Entry(self.controls_frame, width=5, font=("Helvetica", 12))
        self.minutes_input.insert(0, "0")
        self.minutes_input.grid(row=0, column=1, padx=5)

        self.seconds_label = tk.Label(self.controls_frame, text="Seconds:", font=("Helvetica", 12))
        self.seconds_label.grid(row=0, column=2, padx=5)

        self.seconds_input = tk.Entry(self.controls_frame, width=5, font=("Helvetica", 12))
        self.seconds_input.insert(0, "3")
        self.seconds_input.grid(row=0, column=3, padx=5)

        # ? BUTTONS
        # ? -------------------------------

        self.start_button = ttk.Button(self.controls_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=1, column=1, columnspan=1, padx=5, pady=5)

        self.pause_button = ttk.Button(self.controls_frame, text="Pause", command=self.pause_timer, state="disabled")
        self.pause_button.grid(row=1, column=2, columnspan=1, padx=5, pady=5)

        self.reset_button = ttk.Button(self.controls_frame, text="Reset", command=self.reset_timer, state="disabled")
        self.reset_button.grid(row=2, column=1, columnspan=1, padx=5, pady=5)

        self.full_screen_button = ttk.Button(
            self.controls_frame,
            text="Full Screen",
            command=self.toggle_fullscreen,
            state="normal"
        )
        self.full_screen_button.grid(row=2, column=2, columnspan=1, padx=5, pady=5)

        self.sticky = ttk.Button(
            self.controls_frame,
            text=f"Sticky:{self.is_sticky}",
            command=self.toggle_sticky,
            state="normal"
        )
        self.sticky.grid(row=3, column=1, columnspan=1, padx=5, pady=5)

        self.break_label = tk.Label(master, text="Take Break", font=("Helvetica", 30))

        self.update_timer_display()

    def toggle_sticky(self):

        if self.is_sticky == True:
            self.master.attributes("-topmost", True)
            # self.master.overrideredirect(False)

        else:
            self.master.geometry('100x50')
            self.master.attributes("-topmost", False)
            # self.master.overrideredirect(True)

        self.is_sticky = not self.is_sticky

    def toggle_fullscreen(self):
        self.exit_fullscreen() if self.is_fullscreen else self.go_fullscreen()

    def exit_fullscreen(self):
        # self.master.overrideredirect(True)
        self.master.attributes("-fullscreen", False)
        self.break_label.place_forget()
        self.break_label.lift()
        self.is_fullscreen = False

    def go_fullscreen(self):
        # self.master.overrideredirect(False)
        self.timer_display.lower()
        self.master.attributes("-fullscreen", True)
        self.break_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.is_fullscreen = True

    def start_timer(self):
        if not self.is_running:
            minutes = int(self.minutes_input.get())
            seconds = int(self.seconds_input.get())
            self.remaining_time = minutes * 60 + seconds
            self.is_running = True
            self.start_button["state"] = "disabled"
            self.pause_button["state"] = "normal"
            self.reset_button["state"] = "normal"
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

        if self.remaining_time == 0:

            self.go_fullscreen()

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_button["state"] = "normal"
            self.pause_button["state"] = "disabled"
            self.master.after_cancel(self.timer_id)

    def reset_timer(self):
        self.is_running = False
        self.start_button["state"] = "normal"
        self.pause_button["state"] = "disabled"
        self.reset_button["state"] = "disabled"
        self.master.after_cancel(self.timer_id)
        self.remaining_time = int(self.minutes_input.get()) * 60 + int(self.seconds_input.get())
        self.update_timer_display()

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
