from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def input():
    return render_template('input.html')

@app.route('/furniture.html', methods=['POST'])
def index():
    itemID = request.form.get('ItemID') # retrieve a POST variable 
    type = request.form.get('Type')
    dimensions = request.form.get('Dimensions')
    weight = request.form.get('Weight')
    return render_template('furniture.html',itemID=itemID, type=type, dimensions=dimensions, weight=weight)

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")