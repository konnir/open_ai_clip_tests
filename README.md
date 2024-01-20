# A clip implmentaiton of image / text to embeddings 

## General:
* An open ai clip model implmenatation to get vectors from varios clip models.
* Can work with any clip model.
* When running a docker choose your model and it will be downloaded at start (this is a demo to show use of many clip models)

## Uses cases:
Rest API is provided to:
* Embeddings - Send list of images and text, giving back a list of vectors for each input.
* Wearable - send image and get the top 3 wearable in this image (based on clip similarity). 

## Instalation:
General - 
1. Choose clip model from hugging face, reccomanded: "https://huggingface.co/openai/clip-vit-large-patch14 "
2. download the model.
3. Place the model folders in /home/models/clip_models
4. Change the folder names names so you will have: /home/models/clip_models/model-clip and /home/models/clip_models/processor-clip

Docker -
* run - docker run -e CLIP_MODEL=TOUR_CLIP_MODEL -p 8081:8081 clip_syte:TAG_NUMBER
* example - **docker run -e CLIP_MODEL=openai/clip-vit-large-patch14 -p 8081:8081 clip_syte:1.0**
   
## API:
### POST HOST:8081//syte_test/embeddings
* General:
    * You can send multipe imageas and texts descriptions, singel image only, singe text only and any other combination.
    * Response will contain the vectors with the keys given by the user. 
* Input:
    * Headers = request_id, integer (optional)
    * Body = form-data,(key-value pairs of files or texts)
    * KEY = str
    * VALUE = binary_file / text
* Output:
    * Response: 200 OK or Error
    * Json:
      {
           "request_id": STRING_ID,
           "texts_vectors": [[],[],...],
           "images_vectors": [[],[],...]
      }

### POST HOST:8081//syte_test/wearable
* General:
    * You can send image and get the top 3 wearable items inside it from 20 categories (fixed).
* Input:
    * Headers = request_id, integer (optional)
    * Body = form-data,(key-value pairs of files or texts)
    * KEY = str
    * VALUE = binary_file
* Output:
    * Response: 200 OK or Error
    * Json:
      {
           "request_id": STRING_ID,
           "top_categories": [...]
      }

## Demo UI:
* with chrome / other borowser LOCAL_HOST://8081
* upload image
* get the top categories on the image
  
## Limitation:
This is a **demo program** and as so will be workig under those limitatino (might serve more but not tested on other than the below):
* Binary file (png or jpg - clip accept more, let's focus for testing purpose, you can send any size since it will be converted to 224x224 anyway and maybe in production we should limit to save our system)
* Text (english only - max 50 words, clip accept 77 tokens but i'm limiting to focus for testing purposes - for simplicitywe assume 128 ASCII.
* Simple server to concentrate the demo on the functionality asked: no implementation of "feedback" API for now, 1 error fits all, not relating to security and user authentication at all, simple logs, counters in the logs - if some or all are expected, please let me know and I will implement? 

## Examplese API:
### POST HOST:8081//syte_test/embeddings
example, sending image and description with the same ID:

HTTP/1.1 200 OK
POST /syte_test/clip HTTP/1.1
Host: 127.0.0.1:8081
request_id: 1
Content-Length: 385
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="image-1"; filename="Firefly man staring at the moon, moon is made of mechanical parts 74156.jpg"
Content-Type: image/jpeg

(data)
----WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="text-1"

Man staring at the moon, moon is made of mechanical parts
----WebKitFormBoundary7MA4YWxkTrZu0gW

example, response with image and text (with matching id in the keys) - NONE of the fields below the request is mandatory:
Content-Type: application/json
request_id: 1
{
    "image_1_vector": "<Serialized image vector data or a reference to it>",
    "text_1_vector": "<Serialized text vector data or a reference to it>",
    "image_vector_1_similarity_score": 85 
}

HTTP Rest Response:
HTTP/1.1 200 OK (or error)
Content-Type: application/json
request_id: X (if sent, otherwise UUID so we can track responses to logs)
{
    "image_1_vector": "<Serialized image vector data or a reference to it>",
    "text_1_vector": "<Serialized text vector data or a reference to it>",
    "image_vector_1_similarity_score": 85 
}
