import time

from flask import Flask, g

app = Flask(__name__)

# Inicializa o contador global
app.config['REQUEST_COUNTER'] = 0


@app.route('/get-data', methods=['GET'])
def get_data():

    #processing data
    time.sleep(0.1)

    # Incrementa o contador global
    app.config['REQUEST_COUNTER'] += 1

    print(app.config['REQUEST_COUNTER'])

    return {"message": "Data sent successfully", "request_count": app.config['REQUEST_COUNTER']}


if __name__ == '__main__':
    app.run(debug=True)
