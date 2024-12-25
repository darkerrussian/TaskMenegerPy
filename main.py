import Task
from Task import display_all_tasks






def menu():
    while True:
        Task.Task.load_from_db()
        tasks = Task.Task.tasks
        print("\nМеню:")
        print("1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Обновить статус задачи")
        print("4. Удалить задачу")
        print("5. Выйти")

        choice = input("Выберите действие: ")
        if choice == "1":
            Task.Task.create_task()
        elif choice == "2":
            display_all_tasks(Task.Task)
        elif choice == "3":
            Task.Task.update_status(tasks)
        elif choice == "4":
            Task.Task.delete_task(tasks)
        elif choice == "5":
            print("Выход.")
            break
        else:
            print("Некорректный выбор, попробуйте снова.")




