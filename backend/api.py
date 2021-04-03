from flask import Flask, request, send_from_directory, make_response
from flask_cors import CORS
from dotenv import load_dotenv
from utils import get_file_details, validator, extract_time
from mongoengine import connect
from model import Image, ObjectDetected
import os, cv2, io, csv

# Loading local env
load_dotenv()

# Initializing flask instance
app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/api/v1'
# Adding cors
CORS(app)

@app.route("/predict", methods=["POST"])
def predict():
    response = {
        "data": [],
        "error": None,
        "status_code": None
    }
    files = request.files
    
    # Check for bad request 
    isValid = validator(files)
    if not isValid:
        response["error"] = "Files not valid"
        response["status_code"] = 400
        return response, 400
    
    # Fetch details from xml file
    xmlFile = files["xmlFile"]
    xmlData = get_file_details(xmlFile)

    # Check details for image file
    imgFileName = files["imgFile"].filename
    save_path = "{path}/{filename}".format(path=os.environ.get("IMG_SAVE_PATH"), filename=imgFileName)
    files["imgFile"].save(save_path)

    # Image editing
    img = cv2.imread(save_path)
    image = Image(filename=imgFileName, path=save_path, extension=imgFileName.split('.')[1]).save()

    for obj in xmlData["objects"]:

        xmin, ymin, xmax, ymax = obj["dimension"]
        color = (255, 0, 0)

        img = cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, thickness=3)
        img = cv2.putText(img,
            text=obj["name"],
            org=(xmin, ymin-10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=color,
            thickness=2
        )
        ObjectDetected(image=image.id, xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax, type=obj["name"]).save()
    cv2.imwrite(save_path, img)
    return send_from_directory(os.environ.get('IMG_SAVE_PATH'), imgFileName)

@app.route('/export', methods=["GET"])
def fetch_records():
    dataList = [['image_name', 'object_name', 'xmin', 'ymin', 'xmax', 'ymax', 'uploaded_on', 'uploaded_at']]
    for record in Image.objects:
        for object in ObjectDetected.objects(image=record.id):
            row = [record.filename, object.type, object.xmin, object.ymin, object.xmax, object.ymax, record.uploaded_on.date(), extract_time(record.uploaded_on)]
            dataList.append(row)

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows(dataList)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    connection = connect(db=os.environ.get('MONGO_DB'), host=os.environ.get('MONGO_HOST', ''), port=int(os.environ.get('MONGO_PORT')))
    app.run(host="0.0.0.0", port=5000)