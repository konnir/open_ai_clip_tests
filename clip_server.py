import uuid
from io import BytesIO
from PIL import Image
from flask import Flask, request, abort, jsonify, render_template
from flask_cors import CORS

from clip_embedder import ClipEmbeder
from clip_similarity import ClipSimilarity

app = Flask(__name__)

# For running the testing web page at http://127.0.0.1:8081
CORS(app)

# Handlers, common for all parallel requests
embeddings_handler = ClipEmbeder()
similarity_handler = ClipSimilarity()

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/syte_test/embeddings", methods=['POST'])
def process_embeddings():
    """
    Create embeddings for the given texts and images.
    image_id - if found on the request headers the response will contain it, otherwise a uuid will be generated
    image_files - expected as raw in Body, 'form-data' with key to each file,
                    embedding will be in response with key to each file
    text_descriptions - expected as String in Body, 'form-data' with key to each file, embedding will be in response
                            with key to each file
    """
    try:
        # Parameters
        request_id = request.headers.get('request_id', str(uuid.uuid4()))

        # Process image files
        images = []
        images_keys = []
        for key in request.files:
            file = request.files[key]
            images.append(Image.open(BytesIO(file.read())))
            images_keys.append(key)

        # Process text fields
        texts = []
        texts_keys = []
        for key in request.form:
            text = request.form[key].strip()
            texts.append(text)
            texts_keys.append(key)

        # Get embeddings
        text_embeddings_list, image_embeddings_list = embeddings_handler.embed_texts_and_image(images, texts)

        # Build response
        response = { "request_id": request_id }
        text_vector = {key: text_embeddings_list[i] for i, key in enumerate(texts_keys)} if text_embeddings_list else []
        response["texts_vectors"] = text_vector
        image_vector = {key: image_embeddings_list[i] for i, key in enumerate(images_keys)} if image_embeddings_list else []
        response["images_vectors"] = image_vector
        return response
    except Exception as e:
        return jsonify({"error": e}), 500


@app.route("/syte_test/wearable", methods=['POST'])
def process_wearable():
    """ Find the top 3 fashion categories in the image. """
    try:
        # Parameters
        request_id = request.headers.get('request_id', str(uuid.uuid4()))

        # Process image files
        images = []
        images_keys = []
        for key in request.files:
            file = request.files[key]
            images.append(Image.open(BytesIO(file.read())))
            images_keys.append(key)

        # Get embeddings
        top_categories = similarity_handler.fashion_in_the_image(images[0])
        # Build response
        response = { "request_id": request_id }
        response["top_categories"] = top_categories
        return response
    except Exception as e:
        return jsonify({"error": e}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
