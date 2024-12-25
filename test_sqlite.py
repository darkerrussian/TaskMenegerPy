import Task


def test_db_integration():
    Task.Task.initialize_db()
    task = Task.Task.create_task("DB test", "Db des")
    Task.Task.reload_tasks()
    assert len(Task.Task.tasks) > 0
    assert any(t.name == "DB test" for t in Task.Task.tasks)
