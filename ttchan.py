import flask as f
import csv

BOARD_NAME = "ttchan"
POSTS_FILE = "posts.txt"

app = f.Flask(__name__)


@app.route("/")
def index():
    return f.render_template('index.html', boardname=BOARD_NAME, posts=posts)


@app.route("/favicon.ico")
def favicon():
    return f.send_file(os.path.join(app.root_path, 'static', 'logo.ico'))


@app.route("/submit/", methods=['POST', 'GET'])
def submit():
    submission_success = False
    if f.request.method == 'POST':
        submission = [
            f.request.form['tripcode'],
            f.request.form['submission_text']
        ]
        with open(POSTS_FILE, 'a', newline='') as pf:
            pf = csv.writer(pf)
            pf.writerow(submission)
            submission_success = True

    return f.render_template('submit.html', boardname=BOARD_NAME, submission_success=submission_success)


if __name__ == '__main__':
    app.run('0.0.0.0', 80, True)
