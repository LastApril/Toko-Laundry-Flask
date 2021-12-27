from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'laundry'
mysql = MySQL(app)

@app.route('/')
def index():
    con = mysql.connection.cursor()
    con.execute("select * from harga")
    harga = con.fetchall()
    con.close()
    return render_template('index.html',data=harga)

@app.route('/formubahtransaksi/<id>')
def formubahtransaksi(id):
    con = mysql.connection.cursor()
    con.execute("select * from harga")
    harga = con.fetchall()
    con.execute("select * from transaksi where id=%s",id)
    transaksi = con.fetchall()
    con.close()
    return render_template('formubahtransaksi.html',data=transaksi,data2=harga)

@app.post('/ubahtransaksi')
def ubahtransaksi():
    id = request.form['id']
    nama = request.form['nama']
    id_paket = request.form['id_paket']
    berat = request.form['berat']
    harga = request.form['total']
    con = mysql.connection.cursor()
    con.execute(
        "update transaksi set nama=%s, id_paket=%s, berat=%s, harga=%s where id=%s",(nama,id_paket, berat, harga,id)
    )
    mysql.connection.commit()
    con.close()
    return redirect(url_for('transaksi'))

@app.post('/tambahtransaksi')
def tambahtransaksi():
    nama = request.form['nama']
    id = request.form['id']
    berat = request.form['berat']
    harga = request.form['total']
    con = mysql.connection.cursor()
    con.execute(
        "insert into transaksi(nama,id_paket,berat,harga) values(%s,%s,%s,%s)",(nama,id,berat,harga)
    )
    mysql.connection.commit()
    con.close()
    return redirect(url_for('transaksi'))

@app.route('/transaksi')
def transaksi():
    con = mysql.connection.cursor()
    con.execute("select * from transaksi")
    transaksi = con.fetchall()
    con.execute("select * from harga")
    harga = con.fetchall()
    con.close()
    return render_template('transaksi.html',data=transaksi,data2=harga)

@app.route('/harga')
def harga():
    con = mysql.connection.cursor()
    con.execute("select * from harga")
    harga = con.fetchall()
    con.close()
    return render_template('harga.html',data=harga)

@app.route('/formtambahharga')
def formtambahharga():
    return render_template('formtambahharga.html')

@app.post('/tambahharga')
def tambahharga():
    nama = request.form['nama']
    harga = request.form['harga']
    con = mysql.connection.cursor()
    con.execute(
        "insert into harga(nama,harga) values(%s,%s)",(nama,harga)
    )
    mysql.connection.commit()
    con.close()
    return redirect(url_for('harga'))

@app.route('/formubahharga/<id>')
def formubahharga(id):
    con = mysql.connection.cursor()
    con.execute("select * from harga where id=%s",id)
    harga = con.fetchall()
    con.close()
    return render_template('formubahharga.html',data=harga)

@app.post('/ubahharga')
def ubahharga():
    id = request.form['id']
    nama = request.form['nama']
    harga = request.form['harga']
    con = mysql.connection.cursor()
    con.execute(
        "update harga set nama=%s, harga=%s where id=%s",(nama,harga,id)
    )
    mysql.connection.commit()
    con.close()
    return redirect(url_for('harga'))

@app.route('/hapusharga/<id>', methods=['POST','GET'])
def hapusharga(id):
    con = mysql.connection.cursor()
    con.execute("delete from harga where id=%s",id)
    mysql.connection.commit()
    con.close()
    return redirect(url_for('harga'))

if __name__ == "__main__":
    app.run(debug = True)