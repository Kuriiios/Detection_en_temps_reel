import cv2

def convert_to_binary(image_array):
    # Encode the image into a buffer (memory) instead of saving to disk
    success, encoded_image = cv2.imencode('.jpg', image_array)
    if success:
        return encoded_image.tobytes() # This is the BLOB format
    return None