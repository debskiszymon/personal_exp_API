import json

class Expenses:
    def __init__(self):
        try:
            with open("expenses.json", "r") as f:
                self.expenses = json.load(f)
        except FileNotFoundError:
            self.expenses = []

    def get_all(self):
        return self.expenses

    def get(self, id):
        return self.expenses[id]

    def create(self, data):
        self.expenses.append(data)
        self.save_all()

    def save_all(self):
        with open("expenses.json", "w") as f:
            json.dump(self.expenses, f)

    def update(self, id, data):
        # data.pop('csrf_token')
        self.expenses[id] = data
        self.save_all()

    def delete(self, id):
        self.expenses.pop(id)
        self.save_all() 

    def sort(self):
        self.expenses = sorted(self.get_all(), key=lambda x: x["amount"], reverse=True)
        self.save_all()

    def total(self):
        total = sum([expense['amount'] for expense in self.expenses])
        return total

expenses = Expenses()