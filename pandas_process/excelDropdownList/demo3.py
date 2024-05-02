from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grades', methods=['POST'])
def grades():
    junior_high = request.form['juniorHigh']
    if junior_high == '初中':
        grades = ['初一', '初二', '初三']
    elif junior_high == '高中':
        grades = ['高一', '高二', '高三']
    else:
        grades = []
    return {'grades': grades}

if __name__ == '__main__':
    app.run(debug=True)