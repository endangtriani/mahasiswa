from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mahasiswa'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM siswa")
    data = cur.fetchall()
    cur.close()
    return render_template('data_siswa.html', value=data )

@app.route('/new_users')
def template_add():
    return render_template('input.html')

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        nim = request.form['nim']
        nama = request.form['nama']
        jurusan = request.form['jurusan']
        alamat = request.form['alamat']
        tlpn = request.form['tlp']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO siswa (nim, nama_siswa, jurusan_siswa, alamat_siswa, tlp_siswa) VALUES (%s, %s, %s, %s, %s)", (nim, nama, jurusan, alamat, tlpn))
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/edit/<string:id_data>')
def edit(id_data):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM siswa WHERE nim=%s", [id_data])
    mysql.connection.commit()
    row = cur.fetchall()
    if row:
        return render_template('update.html', value=row)
    else:
        return 'Error loading #{id}'.format(nim=id_data)

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        data = ['IT','SI','Management', 'Akuntasi']
        nim = request.form['nim']
        nama = request.form['nama']
        jurusan = request.form['jurusan']
        alamat = request.form['alamat']
        tlpn = request.form['tlp']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE siswa SET nim=%s, nama_siswa=%s, jurusan_siswa=%s, alamat_siswa=%s, tlp_siswa=%s WHERE nim=%s", (nim, nama, jurusan, alamat, tlpn, nim))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM siswa WHERE nim=%s", [id_data])
    mysql.connection.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)