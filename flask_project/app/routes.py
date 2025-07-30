from app import app

@app.route('/')
def hello():
    return "Hello, Flask!"

@app.route('/hello')
def hello_world():
    return "Hello, World!"

@app.route('/info')
def info():
    return "This is an informational page."

@app.route('/calc/<num1>/<num2>')
def calc(num1, num2):
    try:
        n1 = int(num1)
        n2 = int(num2)
    except ValueError:
        return "Incorrect data", 400
    sum_ = n1 + n2
    return f'The sum of {n1} and {n2} is {sum_}'

@app.route('/reverse/<string:str>')
def reverse(str):
    if str == '':
        return 'Incorrect data', 400
    return f'{str[::-1]}'

@app.route('/user/<name>/<age>')
def user(name, age):
    try:
        age_int = int(age)
        if age_int < 0:
            return "Incorrect data", 400
    except ValueError:
        return "Incorrect data", 400
    return f'Hello, {name}. You are {age_int} years old.'

