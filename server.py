from flask import Flask, request, jsonify, render_template, url_for, redirect
from database import Database

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
        ip = request.remote_addr
        text = request.form['answer']
        user = find_user(ip)
        is_valid, message = check_valid_expression(text)
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
    ip_dic.clear()
    return redirect('/')

@app.route('/error')
def handle_error():
    message = request.args['message']
    return render_template("error.html", message=message)


def find_user(ip):
    if ip in ip_dic:
        return ip_dic[ip]
    user_id = len(ip_dic) + 1
    ip_dic[ip] = "User " + str(user_id)
    return ip_dic[ip]

def check_valid_expression(text):
    has_operator = False
    for index in range(len(text)):
        if index == 0 and text[index] in operators:
            return False, "The first element shouldn't be an operator"
        elif index != 0:
            prev = text[index - 1]
            curr = text[index]
            if curr in operators:
                has_operator = True
                if prev in operators:
                    return False, "There are too many operators"
                elif index == len(text) - 1:
                    return False, "An operator can't follow another operator"
    if not has_operator:
        return False, "The expression should have at least one operator"
    return True, text

if __name__ == '__main__':
    app.run()

