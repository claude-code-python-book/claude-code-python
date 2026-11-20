from invoicer.reminders import iter_due

due = iter_due([{"id": "INV-1"}])  # nothing has been read yet
print("created", type(due).__name__)
next(due)
