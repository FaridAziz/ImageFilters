from tkinter import filedialog
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
import cv2
import numpy as np
import datetime

windo = Tk()
windo.configure(background='white')
windo.title("Image Filters")
width = 1100
height = 500
print(width, height)
windo.geometry(f'{width}x{height}')
windo.resizable(0, 0)

# Size for displaying Image
w = 400
h = 280
size = (w, h)


def upload_im():
    try:
        global im, resized
        imageFrame = tk.Frame(windo)
        imageFrame.place(x=250, y=100)
        path = filedialog.askopenfilename()
        im = Image.open(path)
        resized = im.resize(size, Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        display = tk.Label(imageFrame)
        display.imgtk = tkimage
        display.configure(image=tkimage)
        display.grid()
        dn1 = tk.Label(windo, text='Sebelum ', width=20, height=1, fg="white", bg="maroon1",
                       font=('times', 22, ' bold '))
        dn1.place(x=250, y=70)
    except:
        del im
        noti = tk.Label(windo, text='Please upload an Image File', width=33, height=1, fg="black",
                        bg="dodgerblue2",
                        font=('times', 15, ' bold '))
        noti.place(x=294, y=370)
        windo.after(5000, destroy_widget, noti)


def gray_filter():
    try:
        global op, noti
        # Orignal Image
        op = im.convert('L')
        # Resized Image
        gray = resized.convert('L')
        resi = gray.resize(size, Image.ANTIALIAS)
        tkimage1 = ImageTk.PhotoImage(resi)
        imageFrame1 = tk.Frame(windo)
        imageFrame1.place(x=645, y=100)
        dn1 = tk.Label(windo, text='Sesudah ', width=20, height=1, fg="white", bg="black",
                       font=('times', 22, ' bold '))
        dn1.place(x=674, y=70)
        display1 = tk.Label(imageFrame1)
        display1.imgtk = tkimage1
        display1.configure(image=tkimage1)
        display1.grid()
    except Exception as e:
        print(e)
        noti = tk.Label(windo, text='Please upload an Image', width=33, height=1, fg="black",
                        bg="violet red1",
                        font=('times', 15, ' bold '))
        noti.place(x=244, y=370)
        windo.after(5000, destroy_widget, noti)


def cartoon_filter():
    try:
        global op, noti
        img1 = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray1 = cv2.medianBlur(gray1, 5)
        edges1 = cv2.adaptiveThreshold(gray1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color1 = cv2.bilateralFilter(img1, 9, 300, 300)
        cartoon1 = cv2.bitwise_and(color1, color1, mask=edges1)
        op = Image.fromarray(cv2.cvtColor(cartoon1, cv2.COLOR_BGR2RGB))
        img = cv2.cvtColor(np.asarray(resized), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(img, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        pil_image = Image.fromarray(cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB))
        resi = pil_image.resize(size, Image.ANTIALIAS)
        tkimage2 = ImageTk.PhotoImage(resi)
        imageFrame2 = tk.Frame(windo)
        imageFrame2.place(x=645, y=100)
        dn2 = tk.Label(windo, text='Sesudah ', width=20, height=1, fg="black", bg="deep sky blue",
                       font=('times', 22, ' bold '))
        dn2.place(x=674, y=70)
        display2 = tk.Label(imageFrame2)
        display2.imgtk = tkimage2
        display2.configure(image=tkimage2)
        display2.grid()
    except Exception as e:
        print(e)
        noti = tk.Label(windo, text='Please upload an Image', width=33, height=1, fg="black", bg="gold",
                        font=('times', 15, ' bold '))
        noti.place(x=244, y=370)
        windo.after(5000, destroy_widget, noti)


def sketch_filter():
    try:
        global op
        img = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
        output = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        output = cv2.GaussianBlur(output, (3, 3), 0)
        output = cv2.Laplacian(output, -1, ksize=5)
        output = 255 - output
        ret, output = cv2.threshold(output, 150, 255, cv2.THRESH_BINARY)
        op = Image.fromarray(output)
        resi = op.resize(size, Image.ANTIALIAS)
        tkimage3 = ImageTk.PhotoImage(resi)
        imageFrame3 = tk.Frame(windo)
        imageFrame3.place(x=645, y=100)
        dn3 = tk.Label(windo, text='Sesudah ', width=20, height=1, fg="black", bg="gray80",
                       font=('times', 22, ' bold '))
        dn3.place(x=674, y=70)
        display3 = tk.Label(imageFrame3)
        display3.imgtk = tkimage3
        display3.configure(image=tkimage3)
        display3.grid()
    except:
        noti = tk.Label(windo, text='Please upload an Image', width=33, height=1, fg="white", bg="black",
                        font=('times', 15, ' bold '))
        noti.place(x=244, y=370)
        windo.after(5000, destroy_widget, noti)


def face_eye_det_filter():
    try:
        global op, tkimage4
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        img = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 4)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 4)
            break
        else:
            notip1 = tk.Label(windo, text='Face not found in Image!!', width=33, height=1,
                              fg="white", bg="midnightblue",
                              font=('times', 15, ' bold '))
            notip1.place(x=244, y=370)
            windo.after(5000, destroy_widget, notip1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        op = Image.fromarray(img)
        resi = op.resize(size, Image.ANTIALIAS)
        tkimage4 = ImageTk.PhotoImage(resi)
        imageFrame4 = tk.Frame(windo)
        imageFrame4.place(x=645, y=100)
        dn4 = tk.Label(windo, text='Sesudah ', width=20, height=1, fg="white", bg="navy",
                       font=('times', 22, ' bold '))
        dn4.place(x=674, y=70)
        display4 = tk.Label(imageFrame4)
        display4.imgtk = tkimage4
        display4.configure(image=tkimage4)
        display4.grid()
    except Exception as e:
        notip = tk.Label(windo, text='Face not found in Image!!', width=33, height=1,
                         fg="white", bg="midnightblue",
                         font=('times', 15, ' bold '))
        notip.place(x=244, y=370)
        windo.after(5000, destroy_widget, notip)
        print(e)


def save_img():
    try:
        global noti, dna
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        op.save('./Captures/' + filename)
        dna = tk.Label(windo, text=filename + ' Captured', width=33, height=1, fg="black",
                       bg="spring green",
                       font=('times', 15, ' bold '))
        dna.place(x=844, y=370)
        windo.after(5000, destroy_widget, dna)
    except Exception as e:
        print(e)
        noti = tk.Label(windo, text='Please upload an Image', width=33, height=1, fg="black", bg="cyan2",
                        font=('times', 15, ' bold '))
        noti.place(x=844, y=370)
        windo.after(5000, destroy_widget, noti)


def leave():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        windo.destroy()


windo.protocol("WM_DELETE_WINDOW", leave)


def destroy_widget(widget):
    widget.destroy()


up = tk.Button(windo, text='Upload Gambar', bg="spring green", fg="black", width=15,
               height=1, font=('times', 22, 'italic bold '), command=upload_im, activebackground='yellow')
up.place(x=20, y=20)

hat_f = tk.Button(windo, text="Sketch", borderwidth=0, bg='white', command=sketch_filter,
                  height=1, font=('times', 22, 'italic bold '), activebackground='yellow')
hat_f.place(x=20, y=120)

sg_f = tk.Button(windo, text="Cartoon", borderwidth=0, bg='white', command=cartoon_filter,
                 height=1, font=('times', 22, 'italic bold '), activebackground='yellow')
sg_f.place(x=20, y=170)

dog_f = tk.Button(windo, text="Black & White", borderwidth=0, bg='white', command=gray_filter,
                  height=1, font=('times', 22, 'italic bold '), activebackground='yellow')
dog_f.place(x=20, y=220)

snap = tk.Button(windo, text="Simpan Gambar", borderwidth=0, bg='white', command=save_img,
                 height=1, font=('times', 22, 'italic bold '), activebackground='yellow')
snap.place(x=250, y=20)

fd = tk.Button(windo, text="Face Detection", borderwidth=0, bg='white', command=face_eye_det_filter,
               height=1, font=('times', 22, 'italic bold '), activebackground='yellow')
fd.place(x=20, y=270)

windo.mainloop()
