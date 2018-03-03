from flask import Flask, render_template
app = Flask(__name__)

#  the route() decorator tells flask to trigger this function when this url is called
@app.route('/')
def hello_world():
    return render_template('table.html')

if __name__ == "__main__":
    app.run()
