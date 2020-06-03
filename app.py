import logging
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
import os
import time


app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 5000

app = Flask(__name__, static_url_path="/static", static_folder='/Users/McClain/desktop/anon/Static')

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'Test',# os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": 'Test'#os.environ['EMAIL_PASSWORD']
}

app.config.update(mail_settings)
mail = Mail(app)

@app.route('/')
def home():
    """Return a friendly HTTP greeting."""
    return app.send_static_file("index.html")


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        filename = f.filename
        email = request.form['Email']
        #validate email and filetype
        approved_files = ['jpg', 'jpeg', 'png', 'mp4']
        print(email, filename)
        filetype = filename.split('.')[-1]
        if filetype.lower() not in approved_files:
            print('bad file type')
            return app.send_static_file("index.html") #failure
        #whitelist email/filename
        datafile = open("data.txt", "a")
        datafile.write(email + ',' + filename + '\n')
        datafile.close()
        return render_template("success.html", name = f.filename)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)