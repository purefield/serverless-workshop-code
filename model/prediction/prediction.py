import pickle, boto3, os
from flask import Flask, request, abort, jsonify
from boto3.s3.transfer import TransferConfig

application = Flask(__name__)

# Load the vectorizer and model from S3
# Disable S3 multi threading to prevent gunicorn worker deadlock
bucket_name=os.getenv("BUCKET_NAME")
model_file_name=os.getenv("MODEL_FILE_NAME")

s3 = boto3.resource('s3')
s3.Bucket(bucket_name).download_file(model_file_name, model_file_name, Config=TransferConfig(use_threads=False))
with open(model_file_name, 'rb') as f:
    cv, clf = pickle.load(f)

@application.route('/predict', methods=['POST'])
def predict():
    """Returns a disaster prediction by running the request text through NLP model"""
    if request.method == 'POST':

        if not request.json or not 'text' in request.json:
            abort(400)
        text = request.json['text']

        prediction = clf.predict(cv.transform([text]))[0]      # Do not use .fit_transform() here
        return jsonify({"disaster": True if prediction == 1 else False})