from flask import Flask, request, jsonify, render_template, url_for, redirect
from database import Database
import math

app = Flask(__name__)
app.config.from_pyfile('server.cfg')

db = Database(app)
operators = ['+', '-', '*', '/', "="]
ip_dic = {}

@app.route('/')
def main_page():
     return render_template("app.html", calculations=db.get())

@app.route('/create', methods=['GET', 'POST'])
def create_calculation():
    if request.method == 'POST':
        user = request.remote_addr
        text = request.form['answer']
        is_valid, message = check_valid_expression(text)
        print(is_valid)
        if is_valid:
            answer = eval(text)
            db.create(user, str(message + "=" + str(answer)))
            return redirect('/')
        return redirect(url_for('.handle_error', message=message))

    return render_template('create_calculation.html', calculation=None)

@app.route('/delete', methods=['GET', 'POST'])
def delete_history():
    db.db.drop_all()
    db.db.create_all()
    return redirect('/')

@app.route('/error')
def handle_error():
    message = request.args['message']
    return render_template("error.html", message=message)

def check_valid_expression(text):
    has_operator = False
    for index in range(len(text)):
        if index == 0 and text[index] in operators:
            return False, "First shouldn't be operator"
        elif index != 0:
            prev = text[index - 1]
            curr = text[index]
            if curr in operators:
                has_operator = True
                if prev in operators:
                    return False, "too many operators"
                elif index == len(text) - 1:
                    return False, "should be a number following an operator"
    if not has_operator:
        return False, "expression should have at least one operator"
    return True, text

if __name__ == '__main__':
    app.run()

