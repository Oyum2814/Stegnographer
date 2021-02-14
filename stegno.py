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

    button_start_encoding = Button(newWindow, height=3, width=10, text="ENCODE",transition=None, bg="grey", font=('Helvetica', 12, 'bold'))
    button_start_encoding.place(x=250, y=290)



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