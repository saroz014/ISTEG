import onetimepad
from PIL import Image


def get_updated_pixel_value(bit, pix):
    """
    Updates LSB of the pixel with the bit value from the message
    :param bit: bit value from the message
    :param pix: pixel to be updated
    """

    if bit == '0' and pix % 2 != 0:
        return pix - 1
    elif bit == '1' and pix % 2 == 0:
        if pix != 0:
            return pix - 1
        return pix + 1
    return pix


def get_updated_last_pixel_value(current_index, last_index, last_pixel):
    """
    Updates LSB of the last pixel in a batch by comparing the current index with the last index of the message.
    0 LSB means keep reading, 1 LSB means the message is over
    :param current_index: current index of a bit while looping the binary message
    :param last_index: index of the last bit of the binary message
    :param last_pixel: pixel to be updated.
    """

    if current_index == last_index:
        if last_pixel % 2 == 0:
            if last_pixel != 0:
                return last_pixel - 1
            return last_pixel + 1
        return last_pixel
    else:
        if last_pixel % 2 != 0:
            return last_pixel - 1
        return last_pixel


def modify_pixel(img_data, binary_message):
    """
    Modifies the LSB of the image based on the bits of the binary message. A batch of 9 consecutive pixels is formed.
    8 consecutive pixels will contain the message while the last pixel will contain the information to whether to stop
    or read further
    :param img_data: pixel values of the image
    :param binary_message: message to be hidden in the image in its binary representation
    """

    last_index = len(binary_message) - 1
    for i, binary_char in enumerate(binary_message):
        pixels = list(next(img_data) + next(img_data) + next(img_data))
        for j, bit in enumerate(binary_char):
            pixels[j] = get_updated_pixel_value(bit, pixels[j])
        pixels[-1] = get_updated_last_pixel_value(i, last_index, pixels[-1])

        yield pixels[:3]
        yield pixels[3:6]
        yield pixels[6:]


def modify_image(img, img_width, message):
    """
    Modifies the image with the updated pixel value
    :param img: image object
    :param img_width: width of the image
    :param message: message to be hidden in the image
    """

    (x, y) = (0, 0)
    img_data = iter(img.getdata())
    binary_message = [f"{ord(letter):08b}" for letter in message]
    for pixel in modify_pixel(img_data, binary_message):
        img.putpixel((x, y), tuple(pixel))
        if x == img_width - 1:
            x = 0
            y += 1
        else:
            x += 1


def encode(img_path):
    """
    Performs some checks, calls necessary functions to encode the message into the image and saves the updated image
    :param img_path: image path
    """

    message = input('Enter message: ')
    if len(message) == 0:
        print('Message is empty')
        encode(img_path)

    password = input('Enter password: ')
    cipher = onetimepad.encrypt(message, password)

    img = Image.open(img_path, 'r')
    if img.mode.lower() != 'rgb':
        print('Image is not in RBG format.')
        return

    width, height = img.size
    img_bytes = width * height * 3 // 9

    if len(message) > img_bytes:
        print('Image size is small for the message. Either provide a bigger image or a shorter message.')
        return
    new_img = img.copy()
    modify_image(new_img, width, cipher)

    new_img_name = input("Enter the name of new image: ")
    new_img.save(f'{new_img_name}.png')


def decode(img_path):
    """
    Decodes the message hidden within the image
    :param img_path: image path
    """
    img = Image.open(img_path, 'r')
    password = input('Enter password: ')
    img_data = iter(img.getdata())
    message = ''

    while True:
        pixels = next(img_data) + next(img_data) + next(img_data)
        bin_str = ''
        for i in pixels[:8]:
            if i % 2 == 0:
                bin_str += '0'
            else:
                bin_str += '1'

        message += chr(int(bin_str, 2))
        if pixels[-1] % 2 != 0:
            message = onetimepad.decrypt(message, password)
            return message


def main():
    a = int(input("Enter 1 to Encode. 2 to Decode: "))
    if a == 1:
        img_path = input('Enter image path: ')
        encode(img_path)
    elif a == 2:
        img_path = input('Enter image path: ')
        print("Decoded Word : " + decode(img_path))
    else:
        print('Invalid input!!!')
        main()


if __name__ == '__main__':
    main()
