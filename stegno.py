# watch the video for this project here: https://youtu.be/bZ88gnHzwz8
from tkinter import *
import PIL.Image
from tkinter.filedialog import *
from tkinter import filedialog
import os
from PIL import ImageTk as itk

MAX_COLOR_VALUE = 256
MAX_BIT_VALUE = 8

root =Tk()
root.title('GAMEOPHILE PRODUCTIONS')
root.geometry('900x500')
root.config(bg="black")

dir1=""
dir2=""

class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


def make_image(data, resolution):
    image =PIL.Image.new("RGB", resolution)
    image.putdata(data)

    return image


def remove_n_least_significant_bits(value, n):
    value = value >> n
    return value << n


def get_n_least_significant_bits(value, n):
    value = value << MAX_BIT_VALUE - n
    value = value % MAX_COLOR_VALUE
    return value >> MAX_BIT_VALUE - n


def get_n_most_significant_bits(value, n):
    return value >> MAX_BIT_VALUE - n


def shit_n_bits_to_8(value, n):
    return value << MAX_BIT_VALUE - n


def encode(image_to_hide, image_to_hide_in, n_bits):
    width, height = image_to_hide.size

    hide_image = image_to_hide.load()
    hide_in_image = image_to_hide_in.load()

    data = []

    for y in range(height):
        for x in range(width):
             # (107, 3, 10)
             # most sig bits
            try:
                pixel=hide_image[x, y]
                r_hide, g_hide, b_hide =pixel[0],pixel[1],pixel[2]

                r_hide = get_n_most_significant_bits(r_hide, n_bits)
                g_hide = get_n_most_significant_bits(g_hide, n_bits)
                b_hide = get_n_most_significant_bits(b_hide, n_bits)

              # remove lest n sig bits
                pixel_in=hide_in_image[x, y]
                r_hide_in, g_hide_in, b_hide_in = pixel_in[0],pixel_in[1],pixel_in[2]

                r_hide_in = remove_n_least_significant_bits(r_hide_in, n_bits)
                g_hide_in = remove_n_least_significant_bits(g_hide_in, n_bits)
                b_hide_in = remove_n_least_significant_bits(b_hide_in, n_bits)

                data.append((r_hide + r_hide_in,
                             g_hide + g_hide_in,
                             b_hide + b_hide_in))

            except:
                continue

    return make_image(data, image_to_hide.size)


def decode(image_to_decode, n_bits):
    width, height = image_to_decode.size
    encoded_image = image_to_decode.load()

    data = []

    for y in range(height):
        for x in range(width):
            r_encoded, g_encoded, b_encoded = encoded_image[x, y]

            r_encoded = get_n_least_significant_bits(r_encoded, n_bits)
            g_encoded = get_n_least_significant_bits(g_encoded, n_bits)
            b_encoded = get_n_least_significant_bits(b_encoded, n_bits)

            r_encoded = shit_n_bits_to_8(r_encoded, n_bits)
            g_encoded = shit_n_bits_to_8(g_encoded, n_bits)
            b_encoded = shit_n_bits_to_8(b_encoded, n_bits)

            data.append((r_encoded, g_encoded, b_encoded))

    return make_image(data, image_to_decode.size)




def upload_img_encode():
    global dir1

    directory =str(askopenfile())
    dir1_ins1 = directory.index("name='")
    dir1_ins2 =directory.index("'",dir1_ins1+7)
    dir1=directory[dir1_ins1+6:dir1_ins2]



def upload_img_hidden_encode():
    global dir2

    directory =str(askopenfile())
    dir2_ins1 = directory.index("name='")
    dir2_ins2 =directory.index("'",dir2_ins1+7)
    dir2=directory[dir2_ins1+6:dir2_ins2]
    encode_start()


def encode_start_window():
    newWindow = Toplevel(root)
    newWindow.title("ENCODE")
    newWindow.geometry("400x400")
    newWindow.config(bg="black")
    button_img = Button(newWindow, height=3, width=50, text="Select image inside which you want it done", transition=None, bg="grey", command=upload_img_encode,font=('Helvetica', 12, 'bold'))
    button_img.place(x=20, y=100)


    button_hidden_img = Button(newWindow, height=3, width=50, text="Encode image", transition=None, bg="grey", command=upload_img_hidden_encode,font=('Helvetica', 12, 'bold'))
    button_hidden_img.place(x=20, y=200)


    dat = EntryWithPlaceholder(newWindow,"Or encode a text")
    dat.place(x=20, y=300)

    button_start_encoding = Button(newWindow, height=3, width=50, text="ENCODE THE TEXT INSIDE",transition=None, bg="grey", command=encode_text_start, font=('Helvetica', 12, 'bold'))
    button_start_encoding.place(x=20, y=350)



def upload_img_decode():
    global dir1

    directory =str(askopenfile())
    dir1_ins1 = directory.index("name='")
    dir1_ins2 =directory.index("'",dir1_ins1+7)
    dir1=directory[dir1_ins1+6:dir1_ins2]


def decode_start_window():
    newWindow = Toplevel(root)
    newWindow.title("DECODE")
    newWindow.geometry("400x400")
    newWindow.config(bg="black")
    button_img_decoded = Button(newWindow, height=3, width=50, text="Select image to be decoded", transition=None, bg="grey", command=upload_img_decode,font=('Helvetica', 12, 'bold'))
    button_img_decoded.place(x=20, y=100)
    button_start_decoding = Button(newWindow, height=3, width=50, text="Start Decoding",transition=None, bg="grey", command=decode_start, font=('Helvetica', 12, 'bold'))
    button_start_decoding.place(x=20, y=200)



def encode_start():
    global newWindow
    global dir1
    global dir2
    n_bits = 2

    image_to_hide_path = str(dir2)
    image_to_hide_in_path = str(dir1)
    encoded_image_path = "./encoded.tiff"
    image_to_hide = PIL.Image.open(mode='r', fp=image_to_hide_path)
    image_to_hide_in = PIL.Image.open(mode='r', fp=image_to_hide_in_path)


    encode(image_to_hide, image_to_hide_in, n_bits).save(encoded_image_path)

def decode_start():
    global newWindow
    global dir1
    decoded_image_path = './Decoded.tiff'
    encoded_image_path = str(dir1)
    print((dir1))
    n_bits = 2
    image_to_decode = PIL.Image.open(mode='r',fp=str(dir1))
    decode(image_to_decode, n_bits).save(decoded_image_path)



#########text########
def encode_text_start():
    encode_txt()
def genData(data):

        # list of binary codes
        # of given data
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image
def encode_txt():
    global dat
    global dir1
    global newWindow
    img=dir1
    image = Image.open(img, 'r')
    data=str(dat.get())
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def decode_txt():
    global dat
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')

    data = dat.get()
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data


###################    FRONT END     #####################################
button_encode = Button(root, height=3, width=15,text="ENCODE",transition=None, bg="grey", command=encode_start_window,font=('Helvetica',12,'bold'))
button_encode.place(x=50,y=300)

button_decode = Button(root, height=3, width=15,text="DECODE",transition=None, bg="grey", command=decode_start_window,font=('Helvetica',12,'bold'))
button_decode.place(x=750,y=300)

img =itk.PhotoImage(PIL.Image.open("Logo.png"))
panel =Label(root, image = img,height=300,width=400,bg='black')
panel.place(x=240,y=0)
root.mainloop()

root.mainloop()