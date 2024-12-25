import sqlite3


def display_all_tasks(self):
    for task in self.tasks:
        task.display_task()

class Task(object):

    tasks = []

    def __init__(self, name, description, status: bool = False):
        self.name = name
        self.description = description
        self.status = status

    @classmethod
    def initialize_db(cls):
        """Инициализация базы данных."""
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute('''
               CREATE TABLE IF NOT EXISTS tasks (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   description TEXT,
                   status BOOLEAN DEFAULT 0
               )
           ''')
        conn.commit()
        conn.close()
        cls.load_from_db()

    @classmethod
    def load_from_db(cls):
        """Загрузка задач из базы данных."""
        cls.tasks = []
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, description, status FROM tasks")
        rows = cursor.fetchall()
        for name, description, status in rows:
            cls.tasks.append(cls(name, description, bool(status)))
        conn.close()

    @classmethod
    def create_task(cls, name, description):
        """Создает задачу и сохраняет её в базу данных."""
        task = cls(name, description)
        cls.tasks.append(task)
        cls.save_to_db(task)

    @staticmethod
    def save_to_db(task):
        """Сохраняет задачу в базу данных."""
        import sqlite3
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (name, description, status) VALUES (?, ?, ?)",
                       (task.name, task.description, task.status))
        conn.commit()
        conn.close()

    @classmethod
    def reload_tasks(cls):
        """Перезагрузка задач из базы данных."""
        cls.load_from_db()

    @staticmethod
    def update_status(task_name):
        tasks = Task.tasks
        for task in tasks:
            if task.name == task_name:
                task.status = True
                task.update_db_status(task)
                return

        print(f"Задача с название '{task_name}' не найдена.")

    @staticmethod
    def delete_task(task_name):
        tasks = Task.tasks
        for task in tasks:
            if task.name == task_name:
                tasks.remove(task)
                task.delete_db_task(task)
                print(f"Задача с именем '{task_name}' успешно удалена !")
                return
        print(f"Задача с именем '{task_name}' не найдена.")

    @staticmethod
    def update_db_status(task):
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = ? WHERE name = ?",(task.status, task.name))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_db_task(task):
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE name = ?", (task.name,))
        conn.commit()
        conn.close()


    def display_task(self):
        status_text = "Completed" if self.status else "Not Completed"
        print(f"Task: {self.name}\nDescription: {self.description}\nStatus: {status_text}")


