import base64

def encode(image):
    string = str(base64.b64encode(image.data.read()))
    return string[2:len(string) - 1]