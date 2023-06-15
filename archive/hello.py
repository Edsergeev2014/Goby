# Тестовая программа для проверки запуска Flask:
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return 'This is a Flask'

# Для среды Windows указываем адрес и порт:
app.run('127.0.0.1', port=5000, debug=True)