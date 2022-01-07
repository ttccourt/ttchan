import flask as f
import os
import uuid
import csv

BOARD_NAME = "ttchan"
POSTS_FILE = "posts.txt"

app = f.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1000000
app.config['UPLOAD_FOLDER'] = "images"

posts = []


class Post:
    def __init__(self, image_name, text_content, tripcode):
        self.image_name = image_name
        self.text_content = text_content
        self.tripcode = tripcode


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
        image_name = str(uuid.uuid4())
        image = f.request.files['image']
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name + '.jpg'))
        submission = [
            image_name,
            f.request.form['tripcode'],
            f.request.form['submission_text']
        ]
        with open(POSTS_FILE, 'a', newline='') as pf:
            pf = csv.writer(pf)
            pf.writerow(submission)
            submission_success = True
        posts.append(Post(*submission))

    return f.render_template('submit.html', boardname=BOARD_NAME, submission_success=submission_success)


@app.route("/img/<img_uuid>")
def get_image(img_uuid):
    print("getting image " + img_uuid)
    return f.send_from_directory(app.config['UPLOAD_FOLDER'], img_uuid + '.jpg')


def loadposts():
    try:
        with open(POSTS_FILE, 'r') as pf:
            pf = csv.reader(pf)
            for post in pf:
                posts.append(Post(*post))  # add Post object to posts, using each element in post as a param.
    except FileNotFoundError:
        with open(POSTS_FILE, 'x') as pf:
            pass  # create if doesn't exist


if __name__ == '__main__':
    loadposts()
    app.run('0.0.0.0', 80, True)
