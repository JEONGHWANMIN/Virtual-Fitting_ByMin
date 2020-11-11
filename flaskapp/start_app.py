from flask import Flask, render_template, request, make_response, redirect, session, Response, g
from werkzeug.utils import secure_filename
from models import db
from models import Users #모델의 클래스 가져오기.
import cv2
import time
import numpy as np
from acgpn import make_clothes_edge, make_keypoints
from humanparse import simple_extractor
import subprocess
from numba import cuda 
import os
from PIL import Image
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm
import shutil

# camera library
from datetime import datetime, timedelta 
import pygame 
from camera import VideoCamera 

# remove background library
import requests
import json 
import urllib.request as down  
import ssl


app = Flask(__name__)

UPLOAD_FOLDER_CLOTHES = './acgpn/Data_preprocessing/test_color/'
UPLOAD_FOLDER_PERSON = './acgpn/Data_preprocessing/test_img/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def sharpening(img_path):
    image = cv2.imread(img_path)
    image = cv2.resize(image,(192,256))

    if image is None:
        print('Image load failed!')

    src_ycrcb1 = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

    src_f1 = src_ycrcb1[:, :, 0].astype(np.float32)
    blr1 = cv2.GaussianBlur(src_f1, (0, 0), 3.0)
    src_ycrcb1[:, :, 0] = np.clip(2. * src_f1 - blr1, 0, 255).astype(np.uint8)

    src_ycrcb2 = cv2.cvtColor(src_ycrcb1, cv2.COLOR_YCrCb2BGR)
    cv2.imwrite('./static/images/sharp_img.jpg', src_ycrcb2)

def remove_background(img_path):
    URL = "https://slazzer.com/api/v1/remove_image_background"
    API_KEY = "63e79f99b44f432db0262d5694b4bb41" # 3번 남음

    image_file = {'source_image_file': open(img_path, 'rb')}
    headers = {'API-KEY': API_KEY}
    response = requests.post(URL, files=image_file, headers=headers)

    data = response.json()

    pre_url = data['output_image_url']
    imgurl1 = f"{pre_url}" 

    context = ssl._create_unverified_context()

    req = down.Request(imgurl1, headers={'User-Agent': 'Mozilla/5.0'})

    close1 = down.urlopen(req , context=context).read()
    savefile1 = open(img_path,'wb')  # w : 쓰기, r : 읽기 , a : 더하기, wb : 바이너리로 쓰기
    savefile1.write(close1)
    savefile1.close()
    print('이미지 배경제거 완료')

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def ecommerce():
    userid = session.get('userid', None)
    return render_template('ecommerce.html', userid=userid)

@app.route('/signup', methods=['GET','POST'])  #겟, 포스트 메소드 둘다 사용
def signup():   #get 요청 단순히 페이지 표시 post요청 회원가입-등록을 눌렀을때 정보 가져오는것
    form = RegisterForm()
    if form.validate_on_submit(): # POST검사의 유효성검사가 정상적으로 되었는지 확인할 수 있다. 입력 안한것들이 있는지 확인됨.
        #비밀번호 = 비밀번호 확인 -> EqulaTo
    
        users = Users()  #models.py에 있는 users
        users.userid = form.data.get('userid')
        users.password = form.data.get('password')
        users.username = form.data.get('username')
        users.birthday_year = form.data.get('birthday_year')
        users.birthday_month = form.data.get('birthday_month')
        users.birthday_day = form.data.get('birthday_day')
        users.sex = form.data.get('sex')
        users.phone = form.data.get('phone')
            
        print(users.userid, users.password)  #회원가입 요청시 콘솔창에 ID만 출력 (확인용, 딱히 필요없음)
        db.session.add(users)  # id, name 변수에 넣은 회원정보 DB에 저장
        db.session.commit()  #커밋
        
        return redirect('/') #post요청일시는 '/'주소로 이동. (회원가입 완료시 화면이동)
            
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():  
    form = LoginForm() #로그인 폼 생성
    if form.validate_on_submit(): #유효성 검사
        session['userid'] = form.data.get('userid') #form에서 가져온 userid를 session에 저장
    
        return redirect('/') #로그인에 성공하면 홈화면으로 redirect
            
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid',None)
    return redirect('/')

@app.route('/takepic', methods=['GET'])
def takepic():
    userid = session.get('userid', None)

    if userid:
        return render_template('takepic.html', userid=userid)
    else:
        return render_template('virtualfitting.html', userid=userid, isLogin="no")

@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/shutter', methods=['POST'])
def shutter():
    userid = session.get('userid', None)

    period = timedelta(seconds=6)
    next_time = datetime.now() + period
    
    pygame.mixer.init()
    pygame.mixer.music.load('./static/audio/sound.mp3')
    count = pygame.mixer.Sound('./static/audio/4second.wav')
    count.set_volume(0.3)
    
    while True:       
        delta = next_time-datetime.now()
        if(delta.seconds<=6):
            count.play()
            print(delta.seconds+1)
        if(delta.seconds==0):
            count.stop()
            pygame.mixer.music.play()
            image_path = './static/images/users/' + userid + '.jpg'
            cv2.imwrite(image_path, VideoCamera().capture_frame())
            # remove_background(image_path)
            # sharpening(image_path)
            image_exists = True
            return render_template('virtualfitting.html', userid=userid, image_exists=image_exists, image_path='.'+image_path)


@app.route('/virtualfitting', methods=['GET','POST'])
def virtualfitting():
    userid = session.get('userid', None)

    image_exists = False
    image_path = ''
    if userid:
        image_path = './static/images/users/' + userid + '.jpg'

    if os.path.isfile(image_path):
        image_exists = True
        
    return render_template('virtualfitting.html', userid=userid, image_exists=image_exists, image_path='.'+image_path)

@app.route('/filesave', methods=['POST'])
def filesave():
    userid = session.get('userid', None)
    print(userid)

    if userid:
        if request.method == 'POST':
            person_file = request.files['person_file']

            if person_file:
                with Image.open(person_file) as person_image:
                        resize_person_image = person_image.resize((192, 256), Image.ANTIALIAS).convert("RGB")
                        resize_person_image.save('./static/images/users/' + userid + '.jpg', quality=96)
                return redirect('/')
            return render_template('virtualfitting.html', userid=userid, nothing='nothing')
    return render_template('virtualfitting.html', userid=userid, isLogin="no")


@app.route('/photomontage', methods=['POST'])
def photomontage():
    userid = session.get('userid', None)

    if userid != None and request.method == 'POST':
        person_image_path = './static/images/users/' + userid + '.jpg'

        if os.path.isfile(person_image_path):
            clothes_image_path = './static/images/' + request.values["filename"]

            shutil.copy(person_image_path, UPLOAD_FOLDER_PERSON + secure_filename('person.jpg'))

            with Image.open(clothes_image_path) as clothes_image:
                resize_clothes_image = clothes_image.resize((192, 256), Image.ANTIALIAS).convert("RGB")
                resize_clothes_image.save(UPLOAD_FOLDER_CLOTHES + secure_filename('clothes.jpg'))

            time.sleep(1)

            print(cuda.current_context().get_memory_info(), '===== 전처리 전 memory')

            # 전처리
            make_clothes_edge.generate_clothes_edge(UPLOAD_FOLDER_CLOTHES + secure_filename('clothes.jpg'))
            make_keypoints.generate_pose_keypoints(UPLOAD_FOLDER_PERSON + secure_filename('person.jpg'))
            simple_extractor.main()

            # 모든 GPU 메모리 해제
            # 첫 번째 숫자는 여유 메모리, 두 번째는 총 메모리
            print(cuda.current_context().get_memory_info(), '===== 전처리 후 memory')
            device = cuda.get_current_device()
            device.reset()
            print(cuda.current_context().get_memory_info(), '===== reset 후 memory')

            # ACGPN 모델 수행
            subprocess.call(['run_model.sh'], shell=True)

            img_name = "images/results/person.png"
            person_img = person_image_path[9:]
            clothes_img = clothes_image_path[9:] 
            print(cuda.current_context().get_memory_info(), '===== ACGPN 처리 후 memory =====')


            return make_response(render_template("result.html", image_file=img_name, person_img=person_img, clothes_img=clothes_img))

        return '본인의 사진을 등록해주세요!'

    return 'Login 후 이용해주세요!'

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__)) #db파일을 절대경로로 생성
    dbfile = os.path.join(basedir, 'db.sqlite')#db파일을 절대경로로 생성

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile   
    #sqlite를 사용함. (만약 mysql을 사용한다면, id password 등... 더 필요한게많다.)
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True 
    #사용자 요청의 끝마다 커밋(데이터베이스에 저장,수정,삭제등의 동작을 쌓아놨던 것들의 실행명령)을 한다.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    #수정사항에 대한 track을 하지 않는다. True로 한다면 warning 메시지유발
    app.config['SECRET_KEY'] = 'wcsfeufhwiquehfdx'

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all()  #db 생성

    app.run(host='127.0.0.1', port=80, debug=True) 