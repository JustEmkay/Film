from flask import Flask,request,jsonify
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/',methods=['GET'])
def Connection():
    print("\nConnected to API successful.")
    return True

@app.route('/api/', methods=['POST'])
def get_og_image():
    image_data: dict = request.json
    lut_8u = np.interp(np.arange(0, 256), 
                       image_data["lut_in"], 
                       image_data["lut_out"]).astype(np.uint8)
    image_data_restored = np.array(image_data["image_data"], dtype=np.uint8)
    image_contrasted = cv2.LUT(image_data_restored, lut_8u)
    return_data = {'image_out': image_contrasted.tolist()}

    return jsonify(return_data),200


if __name__ == '__main__':
    app.run()