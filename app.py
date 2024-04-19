from flask import Flask, render_template, request, redirect, url_for, session,g ,send_file
import random
import string
import hashlib
import sqlite3


print("\t____Bienvenue!___")
app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 
app.static_folder =r'C:\Users\ALHASSANE DIALLO\GS\project\sources\videos'
#app.static_folder =r'C:\Users\ALHASSANE DIALLO\GS\project\sources\images'
 
DATABASE = 'database.db'
def get_db():
    db = getattr(g,'_database',None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db 
def create_tables():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                user_id INTEGER,
                password TEXT,
                first_name TEXT,
                last_name TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                payment_method TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        db.commit()      
create_tables()
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g,'_database',None)
    if db is not None:
        db.close()

def add_user(username,password,first_name,last_name):
    cursor = get_db().cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute('INSERT INTO users (username,password,first_name,last_name) VALUES(?,?,?,?)',(username,hashed_password,first_name,last_name))
        user_id = cursor.lastrowid  
        get_db().commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
      

def authenticate_user(username,password):
    cursor = get_db().cursor()
    cursor.execute('SELECT*FROM users WHERE username =? AND password=?',(username,hashlib.sha256(password.encode()).hexdigest()))
    user = cursor.fetchone()
    if user and user[3]==hashlib.sha256(password.encode()).hexdigest():
        return user
    return None

class User:
    def __init__(self, username, password, first_name, last_name):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()
        self.first_name = first_name
        self.last_name = last_name
        self.id = self.generate_id()

    def generate_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    @staticmethod
    def authenticate(username, password):
        cursor = get_db().cursor()
        cursor.execute('SELECT*FROM users WHERE username =? AND password=?',(username,hashlib.sha256(password.encode()).hexdigest()))
        user = cursor.fetchone()
        return user
   
@app.route('/')
def index():
    return render_template('aceuill.html')

@app.route('/index', methods=['POST','GET'])
def index_form():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username and password:
            user = authenticate_user(username, password)
            if user:
                session['username']=username
                return redirect(url_for('cours'))
            else:
                return 'Nom d\'utilisateur ou mot de passe incorrect.'
        else:
            return 'Veuillez remplir tous les champs de conexion.'
    else:
        return render_template('index.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        if first_name and last_name and username and password:
            #if any(user.username == username for user in User):
                #return 'Nom d\'utilisareur dèja utilisé.'
            #else:
            #try :
            user_id = add_user(username,password,first_name,last_name)
            if user_id is not None:
                session['username']= username
                #cursor = get_db().cursor()
                #cursor.execute('SELECT*FROM users WHERE username =?',(username,))
                #existing_user = cursor.fetchone()
                #if existing_user:
                    #return 'Nom d\'utilisateur déjà utlisé.'
                #add_user(username,password,first_name,last_name)
                #cursor.execute('SELECT*FROM users WHERE username =?',(username,))
                #user_record = cursor.fetchone()
                #if user_record :
                    #user_id = user_record[0]
                    #session['username']=username
                return redirect(url_for('success', user_id=user_id,first_name=first_name))
            else:
                return 'Nom d\'utilisateur déjà utlisé.'
                    #return 'Erreur lors de l\'enregistrement de l\'ID. '
            #except Exception as e :
                #return 'Erreur lors de l\'enregistrement {}'.format(e)
        else:
            return 'Veuillez remplir tous les champs.'
    else:
        return render_template('register.html')
@app.route('/success/<int:user_id>/<first_name>')
def success(user_id,first_name):
    return render_template('success.html',user_id=user_id, first_name=first_name)

class Paiements:
    def __init__(self, user_id, amount, payment_method):
        self.user_id = user_id
        self.amount = amount
        self.payment_method = payment_method

    def process_payment(self):
        return "Paiement traité avec succès."
 

@app.route('/process_payment', methods=['POST'])
def process_payment():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    user_id = request.form.get('user_id', '')
    amount = request.form.get('amount', '')
    payment_method = request.form.get('payment_method', '')

    if user_id and amount and payment_method:
        payment = Paiements(user_id, amount, payment_method)
        result = payment.process_payment()
        save_payment_details(user_id,amount,payment_method)
        return result
    else:
        return 'Veuillez remplir tous les champs de paiements.'

class Cours:
    def __init__(self, title, description,video_path,pdf_path):
        self.title = title
        self.description = description
        self.video_path= video_path
        self.pdf_path = pdf_path

class PDF(Cours):
    def __init__(self, title, description, author, pub_date, content,video_path,pdf_path):
        super().__init__(title, description,video_path,pdf_path)
        self.author = author
        self.pub_date = pub_date
        self.content = content

@app.route('/cours')
def cours():
    cours = [
        PDF('Introduction à la programmation informatique', 'Ce cours vous apprend les bases de la programmation', 'Dr. Hassan Gs', '2024-12-15', 'Telechargement : 500ko',r"C:\Users\ALHASSANE DIALLO\GS\project\sources\videos\video_test.mp4",r"C:\Users\ALHASSANE DIALLO\GS\project\sources\pdf\cours_html.pdf"),
        PDF('Python', 'Ce cours vous apprend le langage Python', 'Pr. Diallo Gs', '2024-02-21', 'Téléchargement : 200Ko',r'C:\Users\ALHASSANE DIALLO\GS\project\sources\pdf\cours_html.pdf',r"C:\Users\ALHASSANE DIALLO\GS\project\sources\pdf\cours_html.pdf")
    ]
    return render_template('liste.html', cours=cours)

@app.route('/video1')
def video1():
    video_path = r"C:\Users\ALHASSANE DIALLO\GS\project\sources\videos\video_test.mp4"
    return render_template('video.html',video_path=video_path)

@app.route('/pdf')
def pdf():
    pdf_path = r"C:\Users\ALHASSANE DIALLO\GS\project\sources\pdf\cours_html.pdf"
    return send_file(pdf_path,as_attachment=False)
@app.route('/logo')
def logo():
    return send_file(r'C:\Users\ALHASSANE DIALLO\GS\project\sources\images\logo.png', mimetype='image/png')

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        cursor = get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE username =?',(username,))
        user = cursor.fetchone()
        if user:
            return render_template('profile.html',user=user)
        else:
            return 'Utilisateur non trouvé.'
    else:
        return redirect(url_for('register'))
@app.route('/document')
def document():
    return render_template('document.html')
@app.route('/info')
def info():
    return render_template('info.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
