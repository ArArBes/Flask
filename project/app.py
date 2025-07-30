from flask import Flask

app = Flask(__name__)

from apps import routes
print(app.url_map)

@app.route('/')
def hello():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
