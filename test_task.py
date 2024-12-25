import Task


def test_create_task():
    Task.Task.tasks = []
    task = Task.Task.create_task("Test task", "This is a test task")
    assert len(Task.Task.tasks) == 1
    assert Task.Task.tasks[0].name == "Test task"
    assert Task.Task.tasks[0].description == "This is a test task"
    assert not Task.Task.tasks[0].status

def test_delete_task():
    Task.Task.tasks = []
    task = Task.Task.create_task("Delete task", "Deleting task")
    Task.Task.delete_task("Delete task")
    assert len(Task.Task.tasks) == 0

def test_update_status():
    Task.Task.tasks = []
    task = Task.Task.create_task("Update task", "Updating task")
    Task.Task.update_status("Update task")
    assert Task.Task.tasks[0].status