import tkinter as tk
from tkinter import messagebox

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spēle: Reizināšana")

        self.start_number = tk.IntVar()
        self.current_number = tk.IntVar()
        self.total_points = tk.IntVar(value=0)
        self.bank = tk.IntVar(value=0)
        
        # Составление интерфейса
        tk.Label(root, text="Izvēlieties sākuma skaitli (20-30):").pack()
        self.entry = tk.Entry(root, textvariable=self.start_number)
        self.entry.pack()

        self.start_button = tk.Button(root, text="Sākt spēli", command=self.start_game)
        self.start_button.pack()

        # Отображение текущего состояния игры
        tk.Label(root, text="Pašreizējais skaitlis:").pack()
        self.current_label = tk.Label(root, textvariable=self.current_number)
        self.current_label.pack()

        tk.Label(root, text="Kopējie punkti:").pack()
        self.points_label = tk.Label(root, textvariable=self.total_points)
        self.points_label.pack()

        tk.Label(root, text="Banka:").pack()
        self.bank_label = tk.Label(root, textvariable=self.bank)
        self.bank_label.pack()

        # Кнопки для геймов
        self.move_buttons = []
        for multiplier in [3, 4, 5]:
            btn = tk.Button(root, text=f"Reizināt ar {multiplier}", command=lambda m=multiplier: self.make_move(m))
            btn.pack()
            self.move_buttons.append(btn)

        self.reset_button = tk.Button(root, text="Sākt no jauna", command=self.reset_game)
        self.reset_button.pack()

    def start_game(self):
        try:
            num = self.start_number.get()
            if 20 <= num <= 30:
                self.current_number.set(num)
                self.total_points.set(0)
                self.bank.set(0)
            else:
                messagebox.showerror("Kļūda", "Ievadiet skaitli no 20 līdz 30")
        except tk.TclError:
            messagebox.showerror("Kļūda", "Nederīga ievade")

    def make_move(self, multiplier):
        current = self.current_number.get()
        new_number = current * multiplier
        
        # Присвоение очков в зависимости от результата
        if new_number % 2 == 0:
            self.total_points.set(self.total_points.get() + 1)
        else:
            self.total_points.set(self.total_points.get() - 1)

        if new_number % 10 == 0 or new_number % 10 == 5:
            self.bank.set(self.bank.get() + 1)

        self.current_number.set(new_number)

        if new_number >= 3000:
            self.end_game()

    def end_game(self):
        final_score = self.total_points.get()
        if final_score % 2 == 0:
            final_score -= self.bank.get()
        else:
            final_score += self.bank.get()

        winner = "Pirmais spēlētājs" if final_score % 2 == 0 else "Otrais spēlētājs"
        messagebox.showinfo("Spēles beigas", f"Spēle beigusies! Uzvarētājs: {winner}")

    def reset_game(self):
        self.start_number.set(0)
        self.current_number.set(0)
        self.total_points.set(0)
        self.bank.set(0)
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
