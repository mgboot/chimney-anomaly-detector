from math import ceil

def resize(width, height):
    if width > 1024 or height > 1024:
        if width > height:
            height = int(height * 1024 / width)
            width = 1024
        else:
            width = int(width * 1024 / height)
            height = 1024
    return width, height

def count_image_tokens(width: int, height: int):
    width, height = resize(width, height)
    h = ceil(height / 512)
    w = ceil(width / 512)
    total = 85 + 170 * h * w
    return total

if __name__ == "__main__":
    height = input("image height in pixels:")
    width = input("image width in pixels:")

    print("Confirming the image size: ", width, "x", height, "pixels")

    print("Total tokens used: ", count_image_tokens(int(width), int(height)))