""" Provides users with information for the study:
/start-study provides ssh instructions for the bash task interface server
/tellina-urls provides urls to access tellina
"""

from flask import Flask, session, redirect, url_for, escape, request, render_template

import random

app = Flask(__name__)
app.debug = True  # ok to leave debug mode on

# incremented for each user who requests server login credentials
counter = [0]

# ok to be public since no confidential data in the sessions
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

uw_netids = open('data/uw-netids.secret').read().strip().split('\n')
user2pass = open('data/server-credentials.secret').read().strip().split('\n')

@app.route('/start-study')
def start_study():
    if 'username' in session:
        # if logged in
        username = session['username']
        # display server credentials
        return render_template('homepage.html', username=username, password=user2pass[int(username)])

    else:
        # redirect to the login page
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        # already logged in
        return redirect(url_for('start_study'))
    elif request.method == 'POST':
        if request.form['uw_netid'].strip() in uw_netids:
            # checking for a valid participant net id
            session['username'] = counter[0]
            counter[0] += 1

        return redirect(url_for('start_study'))
    else:
        return render_template('login.html')

@app.route('/tellina-urls')
def tellina_urls():
    urls = open('data/tellina-urls.txt').read().strip().split('\n')
    # shuffled for "load balancing"
    random.shuffle(urls)
    return render_template('display-tellina-urls.html', urls=urls)

if __name__ == '__main__':
    # by default this serves a single request at a time
    app.run(host="0.0.0.0", port=8080)