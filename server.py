from flask import Flask,jsonify,request
from flask_cors import CORS
import os
import main
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config["upload"] = "upload/"
CORS(app)
# Route pertama
@app.route('/')
def index():   
     
    return 'Welcome to Api server Dinas Perhubungan'

@app.route('/api/service-image',methods=['POST'])
def service_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image part in the request'})
    
    fileImage = request.files['image']
    if(fileImage.filename == ''):
        return jsonify({'message': 'No image selected for uploading'})
    
    if(fileImage):
        fileImage.save(os.path.join(app.config['upload'], secure_filename(fileImage.filename)))
        result = fileImage.filename
        return jsonify({
            "result":main.main("upload/"+result)
        })
    
if __name__ == '__main__':
    # Menjalankan aplikasi Flask
    app.run(debug=True)
