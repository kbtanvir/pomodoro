import tkinter as tk

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        master.title("Pomodoro Timer")

        self.is_running = False

        self.state_label = tk.Label(master, text="Timer Stopped", font=("Helvetica", 16))
        self.state_label.pack()

        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_timer, state="disabled")
        self.pause_button.pack()

    def start_timer(self):
        self.is_running = True
        self.start_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.update_state_label("Timer Running")

    def pause_timer(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.update_state_label("Timer Paused")

    def update_state_label(self, state):
        self.state_label.config(text=state)

def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
