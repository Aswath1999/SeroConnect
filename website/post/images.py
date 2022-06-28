import uuid as uuid
import os
from website import app
from .. import db,basedir
from ..database.models import Image,User
from werkzeug.utils import secure_filename


def createimage(files,postid):
    if files:
        for file in files:
            filename=secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return f'Invalid image{filename}', 400
            else:
                filename=str(uuid.uuid1())+"_"+filename
                file.save(os.path.join(basedir,app.config['UPLOAD_FOLDER'],filename))
                image=Image(image=filename,post_id=postid)
                db.session.add(image)
                db.session.commit()


def deleteimage(postid):
    images=Image.query.filter(Image.post_id==postid).all()
    if images:
        for image in images:
            os.remove(os.path.join(basedir,app.config['UPLOAD_FOLDER'],image.image))
            db.session.delete(image)
            db.session.commit()


def createuserimage(file,userid):
    user=User.query.filter_by(id=userid).first()
    if file:
        filename=secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return f'Invalid image{filename}', 400
        else:
            filename=str(uuid.uuid1())+"_"+filename
            file.save(os.path.join(basedir,app.config['UPLOAD_FOLDER'],'User/',filename))
            user.userimage=filename
            db.session.commit()
            return filename


def deleteuserimage(userid):
    user=User.query.filter_by(id=userid).first()
    if user.userimage:
        os.remove(os.path.join(basedir,app.config['UPLOAD_FOLDER'],'User/',user.userimage))
        user.userimage=None
        db.session.commit()