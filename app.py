from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
# from werkzeug import secure_filename
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.ownvideo  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('maintemplate.html')


UPLOAD_FOLDER = '/Users/goodjungjun/Desktop/sparta/workoutvideos'
ALLOWED_EXTENSIONS = {'mp4','mov','mkv','avi','wmv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("START upload_file")
    if request.method == 'POST':
        title_receive = request.form['title_give']
        comment_receive = request.form['comment_give']
        type_receive = request.form['type_give']
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_dir = app.config['UPLOAD_FOLDER'] + '/static/storage'
            file.save(os.path.join(file_dir, type_receive + str(file.filename)))
            video_db = {'title': title_receive, 'comment': comment_receive, 'type': type_receive,
                        'videoname': type_receive + str(file.filename)}
            db.videos.insert_one(video_db)
            return redirect("/")
        else:
            print("NOT ALLOWED")
        return jsonify({'result': 'success', 'msg': '성공적으로 저장되었습니다.'})
    return render_template('upload_video_test.html')


@app.route('/showchest')
def homechest():
    return render_template('chest.html')

@app.route('/showback')
def homeback():
    return render_template('back.html')

@app.route('/showabs')
def homeabs():
    return render_template('abs.html')

@app.route('/showleg')
def homeleg():
    return render_template('leg.html')

@app.route('/showshoulder')
def homeshoulder():
    return render_template('shoulder.html')

@app.route('/showdumbbell')
def homedumbbell():
    return render_template('dumbbell.html')



# @app.route('/upload', methods=['POST'])
# def uploadvideo():
#     #1.클라이언트가 준 비디오 정보를 가져오기
#     title_receive = request.form['title_give']
#     comment_receive = request.form['comment_give']
#     category_receive = request.form['category_give']
#     video_receive = request.form['video_give']
#     #2.비디오 정보를 db에 저장하기
#     video = {'title':title_receive, 'comment':comment_receive, 'category':category_receive, 'video':video_receive}
#     db.workout.insert_one(video)
#     #3.성공 여부 알려주기
#     return jsonify({'result':'success','msg':'성공적으로 업로드 되었습니다!'})
#
# @app.route('/video1', methods = ['GET'])
# def showvideo1():
#     #1. db에서 첫번째 카테고리의 비디오를 가져온다
#     chest_videos = list(db.workout.find({'category':'chest'},{'_id':False}))
#     #2. 이를 클라이언트 서버로 쏴준다.
#     return jsonify({'result':'success','chest_video':chest_videos})

@app.route('/view_chest', methods = ['GET'])
def watchvideo1():
    print("START view_chest")
    #1. db에서 chest 카테고리의 비디오를 가져온다.
    chest_videos = list(db.workout.find({'type':'chest'},{'_id':False}))
    #2. 이를 client 서버로 쏴준다.
    print("END view_chest")
    return jsonify({'result':'success','chest':chest_videos})

@app.route('/view_back', methods=['GET'])
def watchvideo2():
    # 1. db에서 back 카테고리의 비디오를 가져온다.
    back_videos = list(db.workout.find({'type':'back'},{'_id':False}))
    # 2. 이를 client 서버로 쏴준다.
    return jsonify({'result':'success','back':back_videos})

@app.route('/view_abs', methods=['GET'])
def watchvideo3():
    # 1. db에서 middle 카테고리의 비디오를 가져온다.
    abs_videos = list(db.workout.find({'type':'abs'},{'_id':False}))
    # 2. 이를 client 서버로 쏴준다.
    return jsonify({'result':'success','abs':abs_videos})

@app.route('/view_leg', methods=['GET'])
def watchvideo4():
    # 1. db에서 bottom 카테고리의 비디오를 가져온다.
    leg_videos = list(db.workout.find({'type':'leg'},{'_id':False}))
    # 2. 이를 client 서버로 쏴준다.
    return jsonify({'result':'success','leg':leg_videos})

@app.route('/view_shoulder', methods=['GET'])
def watchvideo5():
    # 1. db에서 exercise 카테고리의 비디오를 가져온다.
    shoulder_videos = list(db.workout.find({'type':'shoulder'},{'_id':False}))
    # 2. 이를 client 서버로 쏴준다.
    return jsonify({'result':'success','shoulder':shoulder_videos})

@app.route('/view_dumbbell', methods=['GET'])
def watchvideo6():
    # 1. db에서 tool 카테고리의 비디오를 가져온다.
    dumbbell_videos = list(db.workout.find({'type':'dumbbell'},{'_id':False}))
    # 2. 이를 client 서버로 쏴준다.
    return jsonify({'result':'success','dumbbell':dumbbell_videos})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)