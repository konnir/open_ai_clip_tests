# A clip implmentaiton or image / text to embeddings 

My understanding is to build a simple HTTP server application that receives a:
Binary file (png or jpg - clip accept more, let's focus for testing purpose, you can send any size since it will be converted to 224x224 anyway and maybe in production we should limit to save our system) 
Text (english only - max 50 words, clip accept 77 tokens but i'm limiting to focus for testing purposes - for simplicity i will also remove anything that is not 128 ASCII).
I'm going to keep the server simple to concentrate the demo on the functionality asked: no implementation of "feedback" API for now, 1 error fits all, not relating to security and user authentication at all, simple logs, counters in the logs - if some or all are expected, please let me know and I will implement? 

input:
1. path (to image)
2. text (describing text)
*. you can send 1 or 2 or 1 & 2
HTTP Rest 
Type - POST
Headers = request_id, integer (optional)
Body = form-data,(key-value pairs of files or text, start with 'text-' or 'image-', if value after the '-' match between image and text they will be compared)
KEY=imax-X / text-X
VALUE= binary_file / text) 

Output:
1. image_vector: torch.Tensor [1, 512], embeddings for (1) image 
2. text_vector: torch.Tensor [1, 512], embeddings for (1) text description provided 
3. similarity_score: int, (0-100) between the image and the text (if both sent) - let's make it interesting :)
HTTP Rest Response:
HTTP/1.1 200 OK (or error)
Content-Type: application/json
request_id: X (if sent, otherwise UUID so we can track responses to logs)
{
    "image_1_vector": "<Serialized image vector data or a reference to it>",
    "text_1_vector": "<Serialized text vector data or a reference to it>",
    "image_vector_1_similarity_score": 85 
}

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

Delivery:
- git project 
- docker 

Models:
- using model "clip-vit-large-patch14"

deploy:
- from the shared folder take "clip-vit-large-patch14.zip" and deploy it in a folder on your machine. point to the directory in the docker run below. 

Running Docker:
docker run -v /path/to/host/model:/model -p 8081:8081 your_image_name
