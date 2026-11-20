from invoicer.reminders import due_reminders, schedule

monday = [{"id": "INV-1", "status": "overdue"}]
tuesday = [{"id": "INV-1", "status": "paid"}, {"id": "INV-3", "status": "overdue"}]
print(due_reminders(monday))
print(due_reminders(tuesday))
print([job() for job in schedule(["INV-1", "INV-3"])])
