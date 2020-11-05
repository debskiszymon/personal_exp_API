from flask import Flask, jsonify
from models import expenses
from flask import abort
from flask import make_response
from flask import request
from forms import PersonalExpenses
from flask import render_template
from flask import url_for
from flask import redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"
app.url_map.strict_slashes = False

@app.route("/api/v1/expenses/", methods=["GET"])
def expenses_list_api_v1():
    form = PersonalExpenses()
    error = ""
    total = expenses.total()
    expenses.sort()
    if request.method == "GET":
        return render_template("expenses.html", form=form, expenses=expenses.all(), error=error, total=total)

@app.route("/api/v1/expenses/<int:expense_id>", methods=["GET"])
def get_expense(expense_id):
    expense = expenses.get(expense_id-1)
    form = PersonalExpenses(data=expense)
    if not expense:
        abort(404)
    if request.method == "GET":
        return render_template("expense.html", form=form, expense_id=expense_id)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/v1/expenses/", methods=["POST"])
def create_expense():
    error = ""
    total = expenses.total()
    form = PersonalExpenses()
    if request.method == "POST":
        if form.validate_on_submit():
            expense = {
                'id': expenses.all()[-1]['id'] + 1,
                'title': form.title.data,
                'description': form.description.data,
                'amount': form.amount.data
            }
            expenses.create(expense)
        return redirect(url_for("expenses_list_api_v1"))
    return render_template("expenses.html", form=form, expenses=expenses.all(), error=error, total=total)

#DELETE method not working from what I understand forms only accepte POST or GET
# @app.route("/api/v1/expenses/<int:expense_id>/", methods=["POST"])
# def delete_expense(expense_id):
#     expense = expenses.get(expense_id-1)
#     form = PersonalExpenses(data=expense)
#     if request.method == "POST":
#         if form.validate_on_submit():
#             expenses.delete(expense_id-1)
#         return redirect(url_for("expenses_list_api_v1"))
#     return render_template("expense.html", form=form, expense_id=expense_id)

#I used POST method for changeing entries instead of PUT because PUT method is not accepted by form field
@app.route("/api/v1/expenses/<int:expense_id>", methods=["POST"])
def update_expense(expense_id):
    expense = expenses.get(expense_id-1)
    form = PersonalExpenses(data=expense)
    if request.method == "POST":
        if form.validate_on_submit():
            expense = {
                'id': expense_id,
                'title': form.title.data,
                'description': form.description.data,
                'amount': form.amount.data
            }
            expenses.update(expense_id-1, expense)
        return redirect(url_for("expenses_list_api_v1"))
    return render_template("expense.html", form=form, expense_id=expense_id)
    # return jsonify({'expense': expense})

if __name__ == "__main__":
    app.run(debug=True)