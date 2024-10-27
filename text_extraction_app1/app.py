from flask import Flask, render_template, request, redirect, url_for, session, send_file
import os
from PIL import Image
import pytesseract
import mysql.connector



app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Path to the Tesseract executable (change this if necessary)
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract OCR\tesseract.exe'

# Directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
def firstpage():
    return render_template('firstpage.html')


'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username exists in the users dictionary and if the provided password matches
        if username in users and users[username]['password'] == password:
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. <a href='/'>Try again</a>."

    return render_template('login.html')
'''


'''@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists in the users dictionary
        if email in users:
            return "Email already exists. <a href='/signup'>Try again</a>."
        else:
            # Add new user to the users dictionary
            users[email] = {
                'fname': fname,
                'lname': lname,
                'password': password
            }
            return redirect(url_for('login'))

    return render_template('signup.html')
'''

# Create a connection to the database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='text_extraction_app1'
)

# Check the connection
if conn.is_connected():
    cursor = conn.cursor()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match in the database
        cursor.execute("SELECT * FROM userdb WHERE email = %s AND passwd = %s", (username, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. <a href='/'>Try again</a>."

    return render_template('login.html')
'''
@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()

    # Redirect to the first page
    return '<script>var db=confirm("You have loged out");if(db){window.location.href="/"}</script>'
    # return redirect(url_for('firstpage'))
'''
@app.route('/download_text', methods=['POST'])
def download_text():
    if request.method == 'POST':
        text_content = request.form['text_content']

        # Create a temporary text file
        temp_file_path = 'temp_extracted_text.txt'
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write(text_content)

        # Send the file for download
        return send_file(temp_file_path, as_attachment=True, download_name='extracted_text.txt')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists in the database
        cursor.execute("SELECT * FROM userdb WHERE email = %s", (email,))
        if cursor.fetchone():
            return "Email already exists. <a href='/signup'>Try again</a>."
        else:
            # Add new user to the database
            sql = "INSERT INTO userdb (fname, lname, email, passwd) VALUES (%s, %s, %s, %s)"
            values = (fname, lname, email, password)

            try:
                cursor.execute(sql, values)
                conn.commit()
                return '<script>var db=confirm("Registered Successfully");if(db){window.location.href="/login"}</script>'
            except Exception as e:
                return f"Error: {e}"

    return render_template('signup.html')

@app.route('/adminfeedback', methods=['GET', 'POST'])
def adminfeedback():
    # Create a new connection to the database for each request
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='text_extraction_app1'
    )

    if conn.is_connected():
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True here
        cursor.execute("SELECT * FROM feedback")
        result = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        return render_template('adminfeedback.html', result=result)
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match in the database
        cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()

        if admin:
            return redirect(url_for('adminfeedback'))

        else:
            return "Invalid credentials. <a href='/'>Try again</a>."

    return render_template('adminlogin.html')

@app.route('/feedback.html', methods=['GET','POST'])
def feedback():
    return render_template('feedback.html')

@app.route('/process.php', methods=['POST'])
def process_feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['msg']  # Assuming the form field is named 'msg'

        # Create a connection to the database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='text_extraction_app1'
        )

        # Check the connection
        if conn.is_connected():
            cursor = conn.cursor()

            # Insert data into the database
            sql = "INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)"
            values = (name, email, message)

            try:
                cursor.execute(sql, values)
                conn.commit()
                return '<script>var db=confirm("Feedback Send Successfully");if(db){window.location.href="/index"}</script>'
            except Exception as e:
                return f"Error: {e}"

            finally:
                cursor.close()
                conn.close()

    return "Invalid request"
    

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', extracted_text='No file uploaded')

        image = request.files['image']

        if image.filename == '':
            return render_template('index.html', extracted_text='No selected file')

        if image:
            # Save the uploaded image
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)

            # Perform text extraction using Tesseract OCR
            extracted_text = perform_ocr(image_path)

            # Delete the uploaded image after processing
            os.remove(image_path)

            return render_template('index.html', extracted_text=extracted_text)

    return render_template('index.html', extracted_text='')

def perform_ocr(image_path):
    image = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

if __name__ == '__main__':
    app.run(debug=True)
