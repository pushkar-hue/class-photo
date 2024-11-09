import os
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image

def crop(imgs):
    try:
        os.mkdir("img/cropped")
        print("Created cropped directory!")
    except FileExistsError:
        print("cropped directory already exists! Overwriting existing photos.")

    print("Cropping...")
    img_filenames = []
    for index, img in enumerate(imgs):
        with open(f"img/discord/{index}.jpg", 'rb') as image:
            faces = detect_face(image)
            output_filename = f"img/cropped/{index}.jpg"
            img_filenames.append(output_filename)
            image.seek(0)
            try:
                crop_faces(image, faces, output_filename)
            except:
                im = Image.open(image)
                im.save(output_filename)

def detect_face(face_file, max_results=1):
    client = vision.ImageAnnotatorClient()
    content = face_file.read()
    image = types.Image(content=content)
    return client.face_detection(
        image=image, max_results=max_results).face_annotations

def crop_faces(image, faces, output_filename):
    im = Image.open(image)
    im_width, im_height = im.size

    left = right = top = bottom = 0
    max_area = 0  

    for face in faces:
        box = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
        width = abs(box[1][0] - box[0][0])
        height = abs(box[2][1] - box[0][1])
        area = width * height

        if area > max_area:
            max_area = area
            largest_box = box  

    
    centre = int((largest_box[0][0] + largest_box[1][0]) / 2)
    middle = int((largest_box[0][1] + largest_box[2][1]) / 2)
    width = abs(largest_box[1][0] - largest_box[0][0]) + (0.1 * im_width)
    height = abs(largest_box[2][1] - largest_box[0][1]) + (0.1 * im_height)

    if max(width, height) < min(im_width, im_height):
        distance = int(max(width, height) / 2)
    else:
        distance = int(min(im_width, im_height) / 2)
    
    left = max(0, centre - distance)
    right = min(im_width, centre + distance)
    top = max(0, middle - distance)
    bottom = min(im_height, middle + distance)

   
    new_im = im.crop((left, top, right, bottom))
    new_im = new_im.resize((200, 200), Image.ANTIALIAS)
    new_im.save(output_filename)

