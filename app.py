#!/usr/bin/python
import os
from flask import Flask, request, render_template,jsonify,redirect,session
import face_recognition


UNKNOWN_FOLDER = './unknown'
KNOWN_FOLDER = './known'


app = Flask(__name__)
app.config['UNKNOWN_FOLDER'] = UNKNOWN_FOLDER
app.config['KNOWN_FOLDER'] = KNOWN_FOLDER
app.secret_key = "fr"

@app.route('/getLost')
def getLost():
        return render_template('error.html',message=session['message'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        user = request.form['user']
        session['name']=user
        if 'file1' not in request.files:
                session['message']="chehra to dikhao"
                return redirect('/getLost',code=302)

        file = request.files['file1']
        unknownPath = os.path.join(app.config['UNKNOWN_FOLDER'], user+'.jpg')
        knownPath =os.path.join(app.config['KNOWN_FOLDER'], user+'.jpg')

        file.save(unknownPath)

        if(os.path.exists(knownPath)==False):
                session['message']="tumhara to naam hi itna kharab hai"
                return redirect('/getLost',code=302)

        results=matchFace(knownPath,unknownPath)
        matchStatus=results[0]

        if results[0] == True:
            return redirect('/welcome',code=302)
        else:
            session['message']="naam to thik hai, lekin mujhe shakal pasand nahi tumhari"
            return redirect('/getLost',code=302)

        return
    return render_template('index.html')

@app.route('/welcome')
def welcome():
        return render_template('welcome.html',name=session['name'])

def matchFace(path1,path2):
        try:
            picture_of_me = face_recognition.load_image_file(path1)
            my_face_encoding =face_recognition.face_encodings(picture_of_me)[0]

            unknown_picture = face_recognition.load_image_file(path2)
            unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

            results = face_recognition.compare_faces([my_face_encoding],unknown_face_encoding)
            return results
        except:
            return [False]



if __name__ == '__main__':
    app.run()
