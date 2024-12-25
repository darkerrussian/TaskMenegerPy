from gui import TaskApp
import Task
from tkinter import Tk

def test_add_task():
    root = Tk()
    app = TaskApp(root)
    app.name_entry.insert(0, "GUI Task")
    app.description_entry.insert(0, "GUI Description")
    app.add_task()
    assert any(task.name == "GUI Task" for task in Task.Task.tasks)
    root.destroy()

def test_refresh_task_table():
    root = Tk()
    app = TaskApp(root)

    # Добавляем тестовую задачу
    Task.Task.create_task("Test Task", "Description")
    app.refresh_task_table()

    # Проверяем, что задача появилась в таблице
    table_items = app.task_table.get_children()
    task_names = [app.task_table.item(item, "text") for item in table_items]
    assert "Test Task" in task_names

    root.destroy()
