import ttkbootstrap as ttk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
import tkinter.font as tkFont
import Task

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Tracker with Checkboxes")

        # Подключение шрифта Open Sans
        font_path = "fonts/OpenSans_Condensed-Light.ttf"  # Укажите путь к скачанному файлу шрифта
        open_sans_font = tkFont.Font(family="Open Sans", size=10)
        self.root.option_add("*Font", open_sans_font)

        # Настройка стиля заголовков
        style = ttk.Style()
        style.configure("Treeview.Heading",
                        background="lightgray",
                        foreground="black",
                        borderwidth=1,
                        relief="raised",
                        font=("Open Sans", 10, "bold"))
        style.map("Treeview.Heading",
                  relief=[("pressed", "sunken"), ("active", "raised")])

        # Загружаем задачи из базы данных
        Task.Task.initialize_db()

        # Поля ввода для добавления задач
        ttk.Label(root, text="Название задачи:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(root, width=30, bootstyle="info")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(root, text="Описание задачи:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(root, width=50, bootstyle="info")
        self.description_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Кнопки управления
        ttk.Button(root, text="Добавить задачу", command=self.add_task, bootstyle="success").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Button(root, text="Удалить задачу", command=self.delete_task, bootstyle="danger").grid(row=2, column=1, padx=5, pady=5, sticky="w")
        #ttk.Button(root, text="Обновить статус", command=self.update_task_status, bootstyle="primary").grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # Создание Treeview с чекбоксами
        self.task_table = ttk.Treeview(root, columns=("Description"), show="tree headings", bootstyle="info")
        self.task_table.heading("#0", text="Название и Статус")
        self.task_table.heading("Description", text="Описание")
        self.task_table.column("#0", width=200)
        self.task_table.column("Description", width=300)
        self.task_table.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Заполнение таблицы задач
        self.refresh_task_table()

        # Привязка клика для изменения статуса задачи
        self.task_table.bind("<Button-1>", self.on_checkbox_click)

    def refresh_task_table(self):
        """Обновить таблицу задач."""
        # Очищаем таблицу
        for row in self.task_table.get_children():
            self.task_table.delete(row)

        # Загружаем задачи из базы данных
        Task.Task.reload_tasks()

        # Заполняем таблицу с использованием изображений для статуса
        for task in Task.Task.tasks:
            checkbox_image = self.get_checkbox(task.status)
            self.task_table.insert("", "end", text=task.name, image=checkbox_image, values=(task.description,))

    def get_checkbox(self, checked):
        """Возвращает масштабированное изображение чекбокса."""
        if not hasattr(self, '_checkbox_empty') or not hasattr(self, '_checkbox_checked'):
            # Масштабируем изображения при загрузке
            empty_image = Image.open("empty.png").resize((16, 16), Image.Resampling.LANCZOS)
            checked_image = Image.open("no_empty.png").resize((16, 16), Image.Resampling.LANCZOS)

            # Конвертируем их для использования в tkinter
            self._checkbox_empty = ImageTk.PhotoImage(empty_image)
            self._checkbox_checked = ImageTk.PhotoImage(checked_image)

        return self._checkbox_checked if checked else self._checkbox_empty

    def on_checkbox_click(self, event):
        """Обработка клика по чекбоксу."""
        region = self.task_table.identify("region", event.x, event.y)
        if region == "tree":  # Клик внутри дерева
            item_id = self.task_table.identify_row(event.y)
            if item_id:
                task_name = self.task_table.item(item_id, "text")  # Получаем название задачи
                for task in Task.Task.tasks:
                    if task.name == task_name:
                        task.status = not task.status  # Инвертируем статус
                        Task.Task.update_db_status(task)  # Сохраняем изменения в базе
                        self.refresh_task_table()  # Обновляем таблицу
                        return

    def add_task(self):
        """Добавить задачу."""
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        if name:
            Task.Task.create_task(name, description)
            self.refresh_task_table()
            self.name_entry.delete(0, "end")
            self.description_entry.delete(0, "end")
            messagebox.showinfo("Успех", f"Задача '{name}' добавлена!")
        else:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым!")

    def delete_task(self):
        """Удалить задачу."""
        selected_item = self.task_table.focus()  # Получаем ID выбранного элемента
        if selected_item:
            task_name = self.task_table.item(selected_item, "text")  # Извлекаем имя задачи
            Task.Task.delete_task(task_name)
            self.refresh_task_table()
            messagebox.showinfo("Успех", f"Задача '{task_name}' удалена!")
        else:
            messagebox.showerror("Ошибка", "Выберите задачу для удаления!")

    def update_task_status(self):
        """Обновить статус задачи."""
        selected_item = self.task_table.focus()  # Получаем ID выбранного элемента
        if selected_item:
            task_name = self.task_table.item(selected_item, "text")  # Извлекаем имя задачи
            Task.Task.update_status(task_name)
            self.refresh_task_table()
            messagebox.showinfo("Успех", f"Статус задачи '{task_name}' обновлен!")
        else:
            messagebox.showerror("Ошибка", "Выберите задачу для обновления!")

if __name__ == "__main__":
    root = ttk.Window(themename="journal")
    app = TaskApp(root)
    root.mainloop()
