from flask import Flask, render_template, request, redirect
import mysql.connector, json

app = Flask(__name__)


with open('secrets.json','r') as secretsFile:
  creds = json.load(secretsFile)['mysqlcredentials']

# Main page
@app.route('/')
def showtable():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    mycursor.execute('SELECT * FROM Furniture')
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('furniture.html', myresult=myresult )

# Transactions of on item page
@app.route('/transact.html', methods=['POST'])
def trans():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    id = request.form.get('id')
    mycursor.execute('select LI.ItemID, F.FurnitureType, LI.Quantity, LI.Price, I.DateTime, I.ID, LI.LineNumber from Furniture F JOIN LineItem LI RIGHT JOIN Invoice I on F.ItemID = LI.ItemID and I.ID = LI.InvoiceID where F.ItemID = %s;', (id,))
    myresult=mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('transact.html', myresult=myresult)

# WIll show all transactions
@app.route('/all_transact')
def all_trans():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    mycursor.execute('select LI.ItemID, F.FurnitureType, LI.Quantity, LI.Price, I.DateTime, I.ID, LI.LineNumber from Furniture F JOIN LineItem LI RIGHT JOIN Invoice I on F.ItemID = LI.ItemID and I.ID = LI.InvoiceID')
    myresult=mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('transact.html', myresult=myresult )

# Details on one item page
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

# Delete transaction, deletes frome line item and the coresponding invoice when possible
@app.route('/delete_t', methods=['GET'])
def delete_t():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    ln= request.args.get('ln')
    mycursor.execute("SELECT InvoiceID FROM LineItem WHERE LineNumber= %s", (ln,))
    invoiceID = mycursor.fetchone()
    print(invoiceID)

    if invoiceID is not None:
        # Check if the invoice has any remaining line items
        mycursor.execute("SELECT COUNT(*) FROM LineItem WHERE InvoiceID = %s", (invoiceID[0],))
        count = mycursor.fetchone()[0]
        if count == 1:
            # If there is only one remaining line item, last line item and its invoice
            mycursor.execute("DELETE FROM LineItem WHERE LineNumber = %s", (ln,))
            mycursor.execute("DELETE FROM Invoice WHERE ID = %s", (invoiceID[0],))
        else:
            # If there are more than one remaining line items, delete only the line item
            mycursor.execute("DELETE FROM LineItem WHERE LineNumber = %s", (ln,))

        connection.commit()
    mycursor.close()
    connection.close()
    return redirect('../all_transact')

# Edits the transaction related to the Item ID and Line Number 
@app.route('/edit-transact.html', methods=['GET'])
def edit_tran():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    ln = request.args.get('ln')
    mycursor.execute('SELECT ID, DateTime from Invoice;')
    invoice = mycursor.fetchall()
    mycursor.execute('SELECT ItemID, FurnitureType from Furniture;')
    furniture = mycursor.fetchall()
    mycursor.execute('SELECT max(ItemID) from Furniture;')
    max= mycursor.fetchall()
    info = [invoice,furniture,max,ln]
    mycursor.close()
    connection.close()
    return render_template('edit-transact.html', myresult=info)

# Adds transactions
@app.route('/add-transact.html')
def add_transact():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    mycursor.execute('SELECT ID, DateTime from Invoice;')
    invoice = mycursor.fetchall()
    mycursor.execute('SELECT ItemID, FurnitureType from Furniture;')
    furniture = mycursor.fetchall()
    mycursor.execute('SELECT max(ItemID) from Furniture;')
    max= mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('add-transact.html', myresult=[invoice,furniture,max])

# Renders the page to edit furniture forms
@app.route('/edit-furniture.html')
def edit_furn():
    return render_template('edit-furniture.html')

# Will add to furniture
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

# Will delete from furniture
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

# WIll update a row in Furniture
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


# Updates the transactions from the edit-transact page
@app.route('/edit_t', methods = ['POST'])
def edit_t():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    ln = request.form.get('ln')
    itemID = request.form.get('itemID')
    invoiceID = request.form.get('invoiceID')
    quant = request.form.get('quant')
    price = request.form.get('price')
    print(1)
    # Checks if a new invoice needs to be created
    mycursor.execute('Select count(*) From Invoice where ID = %s', (invoiceID,))
    if mycursor.fetchone()[0] == 0:
        # Would like to add ClientID as well but might be too complicated for now
        mycursor.execute('Insert into Invoice (ID) values (%s)', (invoiceID,))
        connection.commit()
    mycursor.execute('''UPDATE LineItem SET 
                     ItemID = %s,
                     InvoiceID = %s,
                     Quantity = %s,
                     Price = %s
                     WHERE LineNumber = %s;
                     ''', (itemID,invoiceID,quant,price,ln))
    print(2)
    # Checks if there is a corresponding row in LineItem for THis particular invoice
    mycursor.execute("SELECT COUNT(*) FROM LineItem WHERE InvoiceID = %s", (invoiceID,))
    if mycursor.fetchone()[0] == 0:
        mycursor.execute('DELETE FROM Invoice WHERE ID=%s',(invoiceID,))
    print(3)
    connection.commit()
    mycursor.close()
    connection.close()
    return redirect('../all_transact')

# Adds the transaction from the add-transact page
@app.route('/add_t', methods=['POST'])
def add_t():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    itemID = request.form.get('itemID')
    invoiceID = request.form.get('invoiceID')
    quant = request.form.get('quant')
    price = request.form.get('price')
    mycursor.execute('Select count(*) From Invoice where ID = %s', (invoiceID,))
    if mycursor.fetchone()[0] == 0:
        # Would like to add ClientID as well but might be too complicated for now
        mycursor.execute('Insert into Invoice (ID) values (%s)', (invoiceID,))
    mycursor.execute('Insert INTO LineItem (InvoiceID, ItemID, Quantity, Price) values (%s,%s,%s,%s)',(invoiceID,itemID,quant, price))
    connection.commit()
    mycursor.close()
    connection.close()
    return redirect('../all_transact')

# Will bring up the forms page needed to edit details
@app.route('/edit-details.html', methods=['GET'])
def edit_det():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    itemID = request.args.get('itemID')
    mycursor.execute('''Select DISTINCT Color from Color 
                     WHERE Color NOT IN (
                        SELECT C.Color from Color C 
                        join Furniture F on C.ItemID = F.ItemID 
                        where C.ItemID = %s)''', (itemID,))
    colors = mycursor.fetchall()
    mycursor.execute('''Select DISTINCT Material from Material 
                     WHERE Material NOT IN (
                        SELECT M.Material from Material M 
                        join Furniture F on M.ItemID = F.ItemID 
                        where M.ItemID = %s)''', (itemID,))
    materials = mycursor.fetchall()
    mycursor.execute('SELECT DISTINCT C.Color from Color C join Furniture F on C.ItemID = F.ItemID where C.ItemID = %s', (itemID,))
    cur_col = mycursor.fetchall()
    mycursor.execute('SELECT DISTINCT M.Material from Material M join Furniture F on M.ItemID = F.ItemID where M.ItemID = %s', (itemID,))
    cur_mat = mycursor.fetchall()
    info = [itemID,colors,materials,cur_col,cur_mat]
    mycursor.close()
    connection.close()
    return render_template('edit-details.html',info = info)

@app.route('/add_d', methods=['POST'])
def add_d():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    itemID = request.form.get('itemID')
    colors = request.form.getlist('colors')
    mats = request.form.getlist('materials')
    
    if colors != []:
        for c in colors:
            print(c)
            mycursor.execute('Insert INTO Color (Color, ItemID) values (%s,%s);',(c,itemID))
    if mats != []:
        for m in mats:
            mycursor.execute('Insert INTO Material (Material,ItemID) values (%s,%s)', (m,itemID))
    connection.commit()
    mycursor.close()
    connection.close()
    return redirect(f'../details.html?id={itemID}')

@app.route('/delete_d', methods=['POST'])
def del_d():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    itemID = request.form.get('itemID')
    colors = request.form.getlist('c-colors')
    mats = request.form.getlist('c-materials')
    if colors != []:
        for c in colors:
            print(c)
            mycursor.execute('Delete FROM Color Where Color =%s and ItemID=%s',(c, itemID))
            connection.commit()
    if mats != []:
        for m in mats:
            mycursor.execute('Delete FROM Material Where Material =%s and ItemID=%s',(m, itemID))
            connection.commit()
    mycursor.close()
    connection.close()
    return redirect(f'../details.html?id={itemID}')

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")