from PIL import Image
import requests


API_ENDPOINT = "http://127.0.0.1:8000/image/"


class MatrixImage:
    def __init__(self):
        self.data = [[[0, 0, 0] for _ in range(32)] for _ in range(32)]
    
    @classmethod
    def from_file(cls, image_file):
        img = Image.open(image_file)
        px = img.load()
        w, h = img.size
        assert  1 <= w <= 32 and 1 <= h <= 32

        return cls.from_pil(px, w, h, (32-w)//2, (32-h)//2)
        
    def __setitem__(self, key, value):
        self.data[key[1]][key[0]] = value

    @classmethod
    def from_pil(cls, px, w, h, x=0, y=0):
        image = cls()
        for i in range(w):
            for j in range(h):
                image[x+i, y+j] = px[i, j]
        return image

    @staticmethod
    def correct_color(color):
        new_color = []
        for i, value in enumerate(color):
            if value <= 5:
                value = 0

            if i == 1:
                value -= 0.15 * value
            if i == 2:
                value -= 0.40 * value
            
            value += 0.1*value

            new_color.append(max(min(int(value), 255), 0))
        
        return new_color

    def add_color_calibration_pixels(self):
        self[0,0] = [255, 255, 255]
        self[1,0] = [255, 0, 0]
        self[2,0] = [0, 255, 0]
        self[3,0] = [0, 0, 255]
        self[4,0] = [255, 0, 255]
        self[5,0] = [255, 255, 0]
        self[6,0] = [0, 255, 255]

    def get_pixels(self):
        pixels = []
        for line in self.data:
            pixels.append([])
            for pixel in line:
                pixels[-1].append(self.correct_color(pixel))

        return pixels
    
    def send(self):
        requests.post(API_ENDPOINT, json=self.get_pixels())


if __name__ == "__main__":
    image = MatrixImage.from_file(f'test.png')
    image.add_color_calibration_pixels()
    image.send()
