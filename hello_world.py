from flask import Flask, render_template, request, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
from io import BytesIO

app = Flask(__name__)

# the route() decorator tells flask to trigger this function when this url is called
@app.route('/')
def hello_world():
    return 'Hello, World!'

# putting information in the url
@app.route('/name/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/table')
def table():
    return render_template('table.html')


@app.route('/input')
def student():
   return render_template('take_input.html')

@app.route('/output',methods = ['POST', 'GET'])
def output():
    if request.method == 'POST':
        result = request.form
        return render_template("produce_output.html", result = result)

@app.route('/calculator',methods = ['POST', 'GET'])
def calculator():
    return render_template("calculator.html")

@app.route('/result',methods = ['POST', 'GET'])
def result():
    print(request.form['action'])
    if request.method == 'POST':
        if request.form['action'] == 'add':
            result = request.form
            return str(int(result['a']) + int(result['b']))
        if request.form['action'] == 'multiply':
            result = request.form
            return str(int(result['a']) * int(result['b']))
        if request.form['action'] == 'subtract':
            result = request.form
            return str(int(result['a']) - int(result['b']))
        if request.form['action'] == 'divide':
            result = request.form
            return str(float(result['a']) / float(result['b']))


@app.route('/image')
def root():
    return """<form action='/plot.png' method='post'>
    <p><input type='text' name='x'></p>
    <p><input type='text' name='y'></p>
    <input type='submit' value='submit'>"""

@app.route('/plot.png', methods=['GET', 'POST'])
def plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    if request.method == 'GET':
        xs = range(100)
        ys = [random.randint(1, 50) for x in xs]

    if request.method == 'POST':
        # assuming posted data looks like '3.3,5.3,6.13,33.4'
        ys = request.form['y'].strip().split(',')
        xs = request.form['x'].strip().split(',')
        if len(xs) != len(ys):
            return "Incorrect Input"

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

if __name__ == "__main__":
    app.run(debug=True)
