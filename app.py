from flask import Flask, render_template, request, url_for, redirect, flash
import os
import re
import requests
from flask_wtf import CSRFProtect

app = Flask(__name__)

app.config.update(
    DEBUG=os.environ.get('FLASK_DEBUG') == '1',
    SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key-change-me'),
    AGENTMAIL_API_KEY=os.environ.get('AGENTMAIL_API_KEY'),
    AGENTMAIL_INBOX_ID=os.environ.get('AGENTMAIL_INBOX_ID'),
    MAIL_RECIPIENT=os.environ.get('MAIL_RECIPIENT'),
)

csrf = CSRFProtect(app)

# Submission form limits and format rules
MAX_NAME = 100
MAX_EMAIL = 254
MAX_URL = 2000
MAX_MESSAGE = 5000
# Local part, "@", then a domain containing at least one dot; no whitespace anywhere
EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/benchmark')
def benchmark():
    return render_template('benchmark.html')

@app.route('/submit')
def submit():
    return render_template('submit.html')

@app.route('/sendmail', methods=['POST'])
def send_message():
    name = request.form.get('name', '').strip()
    url = request.form.get('url', '').strip()
    email = request.form.get('email', '').strip()
    mes = request.form.get('message', '').strip()
    typ = request.form.get('type', '').strip()
    data = request.form.get('dataset', '').strip()

    errors = []
    if not name:
        errors.append('Name is required.')
    elif len(name) > MAX_NAME:
        errors.append(f'Name must be {MAX_NAME} characters or fewer.')

    if not email:
        errors.append('Email is required.')
    elif len(email) > MAX_EMAIL:
        errors.append(f'Email must be {MAX_EMAIL} characters or fewer.')
    elif not EMAIL_RE.match(email):
        errors.append('Please enter a valid email address.')

    if not url:
        errors.append('Submission URL is required.')
    elif len(url) > MAX_URL:
        errors.append(f'Submission URL must be {MAX_URL} characters or fewer.')
    elif not url.startswith(('http://', 'https://')):
        errors.append('Submission URL must start with http:// or https://.')

    if not typ:
        errors.append('Type is required.')

    if not data:
        errors.append('Dataset is required.')

    if len(mes) > MAX_MESSAGE:
        errors.append(f'Message must be {MAX_MESSAGE} characters or fewer.')

    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('submit'))

    if not all([app.config['AGENTMAIL_API_KEY'],
                app.config['AGENTMAIL_INBOX_ID'],
                app.config['MAIL_RECIPIENT']]):
        app.logger.error('Email delivery is not configured; skipping notification email.')
        flash('Sorry, something went wrong. Please try again later.', 'error')
        return redirect(url_for('submit'))

    try:
        requests.post(
            f"https://api.agentmail.to/v0/inboxes/{app.config['AGENTMAIL_INBOX_ID']}/messages/send",
            headers={'Authorization': f"Bearer {app.config['AGENTMAIL_API_KEY']}"},
            json={
                'to': [app.config['MAIL_RECIPIENT']],
                'subject': 'Robustness Evaluate[' + name + ']',
                'text': 'Name: '+ name + '\nEmail: '+ email+ '\nModel url: ' + url+ '\nType: ' + typ+ '\nDataset: ' + data + '\nComments: ' + mes,
            },
            timeout=10,
        ).raise_for_status()
    except requests.RequestException as exc:
        app.logger.error('Failed to send notification email: %s', exc)
        flash('Sorry, something went wrong. Please try again later.', 'error')
        return redirect(url_for('submit'))

    # result = Message(
    #    subject='Robustness Evaluate Rusult',
    #    sender='<'+email+'>',
    #    recipients=
    #        [email],
    #    body='Hello ' + name + ':\n\nThis is your model result.\n\nThanks!',
    # )
    # with app.open_resource("resource/model_analyze_result.xlsx") as fp:
    #     result.attach("model_analyze_result.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", fp.read())
    # mail.send(result)
    flash('Thank you! Your submission has been received.', 'success')
    return redirect(url_for('submit'))


if __name__=="__main__":
    print("Server is running on localhost...")
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=app.config['DEBUG'])
