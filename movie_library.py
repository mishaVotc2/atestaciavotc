import json
import os
from tkinter import *
from tkinter import ttk, messagebox

DATA_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("800x500")

        # Данные
        self.movies = self.load_movies()

        # Виджеты ввода
        self.create_input_fields()

        # Таблица для отображения
        self.create_table()

        # Кнопки
        self.create_buttons()

        # Фильтры
        self.create_filters()

        # Обновить таблицу
        self.refresh_table()

    def create_input_fields(self):
        frame = LabelFrame(self.root, text="Добавить новый фильм", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        Label(frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.entry_title = Entry(frame, width=30)
        self.entry_title.grid(row=0, column=1, padx=5, pady=2)

        Label(frame, text="Жанр:").grid(row=0, column=2, sticky="w")
        self.entry_genre = Entry(frame, width=20)
        self.entry_genre.grid(row=0, column=3, padx=5, pady=2)

        Label(frame, text="Год выпуска:").grid(row=1, column=0, sticky="w")
        self.entry_year = Entry(frame, width=10)
        self.entry_year.grid(row=1, column=1, padx=5, pady=2)

        Label(frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w")
        self.entry_rating = Entry(frame, width=10)
        self.entry_rating.grid(row=1, column=3, padx=5, pady=2)

    def create_table(self):
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

    def create_buttons(self):
        frame = Frame(self.root)
        frame.pack(fill="x", padx=10, pady=5)

        Button(frame, text="➕ Добавить фильм", command=self.add_movie, bg="lightgreen").pack(side="left", padx=5)
        Button(frame, text="🗑 Удалить выбранный", command=self.delete_movie, bg="salmon").pack(side="left", padx=5)

    def create_filters(self):
        filter_frame = LabelFrame(self.root, text="Фильтрация", padx=10, pady=5)
        filter_frame.pack(fill="x", padx=10, pady=5)

        Label(filter_frame, text="Жанр:").grid(row=0, column=0)
        self.filter_genre = Entry(filter_frame, width=15)
        self.filter_genre.grid(row=0, column=1, padx=5)

        Label(filter_frame, text="Год:").grid(row=0, column=2)
        self.filter_year = Entry(filter_frame, width=8)
        self.filter_year.grid(row=0, column=3, padx=5)

        Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filter).grid(row=0, column=4, padx=10)
        Button(filter_frame, text="❌ Сбросить", command=self.reset_filter).grid(row=0, column=5)

    def validate_movie(self, title, genre, year_str, rating_str):
        if not title or not genre:
            return False, "Название и жанр не могут быть пустыми"
        try:
            year = int(year_str)
            if year < 1888 or year > 2026:
                return False, "Год должен быть от 1888 до 2026"
        except ValueError:
            return False, "Год должен быть целым числом"

        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                return False, "Рейтинг должен быть от 0 до 10"
        except ValueError:
            return False, "Рейтинг должен быть числом"
        return True, ""

    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year = self.entry_year.get().strip()
        rating = self.entry_rating.get().strip()

        valid, msg = self.validate_movie(title, genre, year, rating)
        if not valid:
            messagebox.showerror("Ошибка ввода", msg)
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": float(rating)
        }
        self.movies.append(movie)
        self.save_movies()
        self.refresh_table()

        # Очистить поля
        self.entry_title.delete(0, END)
        self.entry_genre.delete(0, END)
        self.entry_year.delete(0, END)
        self.entry_rating.delete(0, END)

        messagebox.showinfo("Успех", f"Фильм \"{title}\" добавлен!")

    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите фильм для удаления")
            return
        for item in selected:
            values = self.tree.item(item, "values")
            title = values[0]
            # Удаление по названию и году (упрощённо)
            self.movies = [m for m in self.movies if not (m["title"] == title and str(m["year"]) == values[2])]
        self.save_movies()
        self.refresh_table()

    def refresh_table(self, filtered_movies=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = filtered_movies if filtered_movies is not None else self.movies
        for m in data:
            self.tree.insert("", END, values=(m["title"], m["genre"], m["year"], m["rating"]))

    def apply_filter(self):
        genre_filter = self.filter_genre.get().strip().lower()
        year_filter = self.filter_year.get().strip()

        filtered = []
        for m in self.movies:
            genre_ok = genre_filter == "" or genre_filter in m["genre"].lower()
            year_ok = year_filter == "" or str(m["year"]) == year_filter
            if genre_ok and year_ok:
                filtered.append(m)
        self.refresh_table(filtered)

    def reset_filter(self):
        self.filter_genre.delete(0, END)
        self.filter_year.delete(0, END)
        self.refresh_table()

    def load_movies(self):
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_movies(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    root = Tk()
    app = MovieLibrary(root)
    root.mainloop()