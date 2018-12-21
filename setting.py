from flask import Flask, render_template, redirect, url_for, request, g, session, send_from_directory
import sqlite3 as sql,os


app=Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.secret_key = os.urandom(24)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/dashboard")
def dashboard():
	return ("<h1 class='display-1 text-center'>Dashboard</h1><br><a href='/logout'>Logout</a>")

@app.route("/register_server", methods=["POST"])
def register_server():
	if request.method == "POST":
		if request.form['password'] == request.form['repassword']:
			try:
				name = request.form['name']
				emailid = request.form['emailid']
				emailid = emailid.lower()
				password = request.form['password']
				role = request.form['role']
				print(	role)
				con = sql.connect("static/datab.db")
				cur = con.cursor()
				if role == "user":
					cur.execute("select userid from users where email = ?",(emailid,))
					a = cur.fetchone();
					if a != None:
						return render_template("index.html",show_example_modal=True)
					cur.execute("INSERT INTO users (name,password,email)VALUES (?,?,?)",(name,password,emailid))
				elif role == "admin":
					cur.execute("select userid from admin where email = ?",(emailid,))
					a = cur.fetchone();
					if a != None:
						return render_template("index.html",show_example_modal=True)
					cur.execute("INSERT INTO admin (name,password,email)VALUES (?,?,?)",(name,password,emailid))
				con.commit()
				cur.close()
				con.close()
				return redirect("/")
			except:
				cur.close()
				con.close()
				return render_template("index.html",show_example_modal=True)
		else:
			return render_template("index.html",show_example_modal=True)


@app.route("/login_server", methods=["POST"])
def login_server():
  if request.method == "POST":
    emailid = request.form['emailid']
    password = request.form['password']
    role = request.form['role']
    con = sql.connect("static/datab.db")
    cur = con.cursor()
    emailid = emailid.lower()
    if role == "user":
      cur.execute("select password from users where email = ?",(emailid,))
      a = cur.fetchone();
      cur.execute("select name from users where email = ?",(emailid,))
      b = cur.fetchone()
    elif role == "admin":
      cur.execute("select password from admin where email = ?",(emailid,))
      a = cur.fetchone();
      cur.execute("select name from admin where email = ?",(emailid,))
      b = cur.fetchone()
    cur.close()
    con.close()
    ta=str(a)
    output=ta[2:-3]
    tb=str(b)
    name=tb[2:-3]
    session.pop('user', None)
    session.pop('role', None)
    if request.form['password'] == output and output != '':
      session['user'] = name
      session['role'] = role
      session['email'] = emailid
      return redirect('/')
    else:
      return render_template("index.html",login_modal=True)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
      g.user = session['user']


@app.route('/logout')
def logout():
  session.pop('user', None)
  session.pop('role', None)
  session.pop('email', None)
  return redirect('/')

@app.route("/")
def index():
  if 'user' in session:
    if session['role'] == "user":
      return render_template("index1.html",UserName = session['user'])
    elif session['role'] == "admin":
      con = sql.connect("static/datab.db")
      cur = con.cursor()
      cur.execute("select rewards from admin where email = ?",(str(session['email']),))
      print(len(session['email']))
      a = cur.fetchone()
      a = str(a)
      a=a[1:-2]
      con.commit()
      cur.close()
      con.close()
    return render_template("index2.html",UserName = session['user'],re = a)
  return render_template("index.html")

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form['q']
      print(result)
      con=sql.connect("static/datab.db")
      cur=con.cursor()
      cur.execute("select image_name from photos_photo_table where image_tags like '%"+str(result)+"%'")
      inp=cur.fetchall()
      inp = [j for i in inp for j in i]
      new = []
      if len(inp) == 0:
      	result = result.split(" ")
      	for x in result:
      		cur.execute("select image_name from photos_photo_table where image_tags like '%"+str(x)+"%'")
      		temp = cur.fetchall()
      		new.extend([j for i in temp for j in i])
      	for i in new:
      		if i in inp:
      			inp.remove(i)
      			inp.insert(0,i)
      		else:
      			inp.append(i)
      con.commit()
      #return redirect('/')
      #return redirect(url_for('index'))
      cur.close()
      con.close()
      if 'user' in session:
      	if len(inp) == 0:
      		return render_template("index1.html",UserName = session['user'], r = True)
      	return render_template("index1.html", UserName = session['user'], result =inp)
      if len(inp) == 0:
      	return render_template("index.html", r = True)
      return render_template("index.html",result = inp)

@app.route('/result_category',methods = ['POST', 'GET'])
def result_category():
   if request.method == 'POST':
      result = request.form['q']
      print(result)
      con=sql.connect("static/datab.db")
      cur=con.cursor()
      cur.execute("select image_name from photos_photo_table where image_category like '%"+str(result)+"%'")
      inp=cur.fetchall()
      inp = [j for i in inp for j in i]
      print(inp)
      con.commit()
      #return redirect('/')
      #return redirect(url_for('index'))
      cur.close()
      con.close()
      if 'user' in session:
      	if len(inp) == 0:
      		return render_template("index1.html",UserName = session['user'], r = True)
      	return render_template("index1.html", UserName = session['user'], result =inp)
      if len(inp) == 0:
      	return render_template("index.html", r = True)
      return render_template("index.html",result = inp)

@app.route("/upload", methods=["POST"])
def upload():
    '''
    # this is to verify that folder to upload to exists.
    if os.path.isdir(os.path.join(APP_ROOT, 'files/{}'.format(folder_name))):
        print("folder exist")
    '''
    target = os.path.join(APP_ROOT, 'static/photos/upload')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png") or (ext == ".jpeg"):
            print("File supported moving on...")
        else:
            render_template("<h1>File Not Supported</h1>")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        con = sql.connect("static/datab.db")
        cur = con.cursor()
        cur.execute("INSERT INTO upload_photos (image_name,author)VALUES (?,?)",(filename,session['user']))
        cur.execute("UPDATE admin set rewards = (rewards + 50) where name = ?",(session['user'],))
        con.commit()
        cur.close()
        con.close()
    return redirect('/')

@app.route("/redeem",methods=["POST"])
def reedeem():
  if 'user' in session:
    amount = int(request.form['amount'])
    con = sql.connect("static/datab.db")
    cur = con.cursor()
    cur.execute("select rewards from admin where email = ?",(str(session['email']),))
    a = cur.fetchone()
    a = str(a)
    a=int(a[1:-2])
    if a > amount:
      cur.execute("update admin set rewards = ? where email = ?",((a-amount),str(session['email']),))
    con.commit()
    cur.close()
    con.close()
  return redirect("/")


if __name__=="__main__":
	app.run(debug=True,port=4000)
