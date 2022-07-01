import uuid as uuid
import os
from website import app
from .. import db,basedir
from ..database.models import Image,User
from werkzeug.utils import secure_filename

# the createimage is used to save image location information on the database and save the image locally on the machine.
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

# Deletes image information from the database and locally from the machine.
def deleteimage(postid):
    images=Image.query.filter(Image.post_id==postid).all()
    if images:
        for image in images:
            os.remove(os.path.join(basedir,app.config['UPLOAD_FOLDER'],image.image))
            db.session.delete(image)
            db.session.commit()

# create user profile image and sace location to database.
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

# deletes user's profile image
def deleteuserimage(userid):
    user=User.query.filter_by(id=userid).first()
    if user.userimage:
        os.remove(os.path.join(basedir,app.config['UPLOAD_FOLDER'],'User/',user.userimage))
        user.userimage=None
        db.session.commit()