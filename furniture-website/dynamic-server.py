from flask import Flask, render_template, request, redirect
import mysql.connector, json

app = Flask(__name__)


with open('secrets.json','r') as secretsFile:
  creds = json.load(secretsFile)['mysqlcredentials']


@app.route('/')
def showtable():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    mycursor.execute('SELECT * FROM Furniture')
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('furniture-project.html', myresult=myresult )

@app.route('/transact.html', methods=['POST'])
def trans():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    id = request.form.get('id')
    mycursor.execute('select LI.ItemID, F.FurnitureType, LI.Quantity, I.DateTime, I.ID, LI.LineNumber from Furniture F JOIN LineItem LI RIGHT JOIN Invoice I on F.ItemID = LI.ItemID and I.ID = LI.InvoiceID where F.ItemID = %s;', (id,))
    myresult=mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('transact.html', myresult=myresult )

@app.route('/delete-t', methods=['GET'])
def delete_t():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    id= request.form.get('LineNumber')
    mycursor.execute("SELECT itemID FROM LineItem WHERE LineNumber= %s", (id,))
    mycursor.fetchall()
    if id is not None:
        mycursor.execute("DELETE FROM LineItem WHERE LineNumber= %s", (id,))
        connection.commit()
    mycursor.close()
    connection.close()
    return redirect('../',)
'''
@app.route('/edit-transact', methods=['GET'])
def edit_t():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    id= request.form.get('itemid')
    if id is not None:
        mycursor.execute("DELETE FROM LineItem WHERE LineNumber= %s", (id,))
        connection.commit()
    mycursor.close()
    connection.close()
    return redirect('../')
'''

@app.route('/edit-furniture.html')
def edit_furn():
    return render_template('edit-furniture.html')

@app.route('/add', methods=['POST'])
def add():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    type = request.form.get('type')
    width = request.form.get('width')
    depth = request.form.get('depth')
    height = request.form.get('height')
    weight = request.form.get('weight')
    dimensions = f'{width} x {depth} x {height}'
    if type is not None:
        mycursor.execute("INSERT into Furniture (FurnitureType, Dimensions, Weight) Values (%s,%s,%s)", (type,dimensions,weight))
        connection.commit()
    mycursor.close()
    connection.close()
    return redirect('../')

@app.route('/delete', methods=['POST'])
def delete_f():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    id= request.form.get('itemid')
    if id is not None:
        mycursor.execute("DELETE FROM Furniture WHERE ItemID=%s", (id,))
        connection.commit()
    mycursor.close()
    connection.close()
    return redirect('../')

@app.route('/update', methods=['POST'])
def update():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    itemid= request.form.get('itemid')
    type = request.form.get('type')
    width = request.form.get('width')
    depth = request.form.get('depth')
    height = request.form.get('height')
    weight = request.form.get('weight')
    dimensions = f'{width} x {depth} x {height}'
    if type is not None:
        mycursor.execute("UPDATE Furniture SET FurnitureType=%s , Dimensions=%s , Weight=%s WHERE ItemID=%s", (type,dimensions,weight,itemid))
        connection.commit()
    mycursor.close()
    connection.close()
    return redirect('../')

@app.route('/edit-transact.html', methods = ['GET'])
def edit_trans():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    ln =  request.args.get('ln')
    mycursor.close()
    connection.close()
    return render_template('edit-transact.html', ln=ln)

@app.route('/update_t')
def update_t():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    mycursor.close()
    connection.close()
    return redirect('../transact.html')

@app.route('/details.html', methods = ['GET'])
def details():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    id = request.args.get('id')
    mycursor.execute("""SELECT F.ItemID,
                GROUP_CONCAT(DISTINCT C.Color ORDER BY C.Color) AS Colors,
                GROUP_CONCAT(DISTINCT M.Material ORDER BY M.Material) AS Materials
                FROM Furniture F
                LEFT JOIN Color C ON F.ItemID = C.ItemID
                LEFT JOIN Material M ON F.ItemID = M.ItemID
                WHERE F.ItemID = %s""", (id,))
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('details.html', myresult=myresult)


@app.route('/edit-details.html', methods=['GET'])
def edit_det():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    id = request.args.get('id')
    return render_template('edit-details.html')
'''
@app.route('/edit-details')
def edit_details():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    itemid= request.form.get('itemid')
    type = request.form.get('type')
    width = request.form.get('width')
    depth = request.form.get('depth')
    height = request.form.get('height')
    weight = request.form.get('weight')
    dimensions = f'{width} x {depth} x {height}'
    if type is not None:
        mycursor.execute("UPDATE Furniture SET FurnitureType=%s , Dimensions=%s , Weight=%s WHERE ItemID=%s", (type,dimensions,weight,itemid))
        connection.commit()
    mycursor.close()
    connection.close()
    return redirect('../')
'''
if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")