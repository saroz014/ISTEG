from PIL import Image


def get_updated_pixel_value(bit, pix):
    if bit == '0' and pix % 2 != 0:
        return pix - 1
    elif bit == '1' and pix % 2 == 0:
        if pix != 0:
            return pix - 1
        return pix + 1
    return pix


def get_updated_last_pixel_value(current_index, last_index, last_pixel):
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
    last_index = len(binary_message) - 1
    for i, binary_char in enumerate(binary_message):
        pixels = list(next(img_data) + next(img_data) + next(img_data))
        for j, bit in enumerate(binary_char):
            pixels[j] = get_updated_pixel_value(bit, pixels[j])
        pixels[-1] = get_updated_last_pixel_value(i, last_index, pixels[-1])

        yield pixels[:3]
        yield pixels[3:6]
        yield pixels[6:]


def modify_image(new_img, img_width, message):
    (x, y) = (0, 0)
    img_data = iter(new_img.getdata())
    binary_message = [f"{ord(letter):08b}" for letter in message]
    for pixel in modify_pixel(img_data, binary_message):
        new_img.putpixel((x, y), tuple(pixel))
        if x == img_width - 1:
            x = 0
            y += 1
        else:
            x += 1


def encode(img_path):
    message = input('Enter message: ')
    if len(message) == 0:
        print('Message is empty')
        encode(img_path)
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
    modify_image(new_img, width, message)

    new_img_name = input("Enter the name of new image: ")
    new_img.save(f'{new_img_name}.png')


def decode(img_path):
    img = Image.open(img_path, 'r')
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
