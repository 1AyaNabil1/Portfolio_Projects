"""This project to change any photo by blurring it
or changing its effect into black and white and
Another effects that we call it as cartooning the image"""

# Created by Aya Nabil on 26/9/2022

# Importing packages

# For image processing
import cv2

# To open the filebox
import easygui
import sys

# To plot the image
import matplotlib.pyplot as plt

# To read the path and save images to that path
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox


# create main window
top = tk.Tk()
top.geometry('400x400')
top.title('Cartooning Your Image!')
top.configure(background='white')
label = Label(top, background='#CDCDCD', font=('calibri', 20, 'bold'))


def upload():
    ImagePath = easygui.fileopenbox()
    cartooning(ImagePath)


def cartooning(ImagePath):

    # read the image and scale the color to grayscale
    originalImage = cv2.imread(ImagePath)
    originalImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2RGB)

    # plt.imshow(ReSized1, cmap ='gray')
    ReSized1 = cv2.resize(originalImage, (960, 540))

    if (originalImage is not None):
        grayScaleImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        ReSized2 = cv2.resize(grayScaleImage, (960, 540))
        # plt.imshow(ReSized2, cmap='gray')

    elif originalImage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    # Smoothening a grayscale image

    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    # plt.imshow(ReSized3, cmap='gray')\

    # Retrieving the edges of an image
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255,
                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                    # or
                                    # cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 9, 9)
    ReSized4 = cv2.resize(getEdge, (960, 540))
    # plt.imshow(ReSized4, cmap='gray')

    # Preparing a Mask Image
    colorImage = cv2.bilateralFilter(originalImage, 8, 300, 300)
    ReSized5 = cv2.resize(colorImage, (960, 540))
    # plt.imshow(ReSized5, cmap='gray')

    # Giving a Cartoon Effect
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSized6 = cv2.resize(cartoonImage, (960, 540))
    # plt.imshow(ReSized6, cmap='gray')

    # Plotting the whole transition
    images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]
    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []},
                             gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    save1 = Button(top, text="Save cartoon image", command=lambda: save(ReSized6, ImagePath), padx=30, pady=5)
    save1.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    save1.pack(side=TOP, pady=50)

    plt.show()


def save(ReSized6, ImagePath):
    # saving an image using imwrite()
    newName = "Cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName + extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + newName + " at " + path
    messagebox.showinfo(title=None, message=I)


# Making the cartooning button in the main window
upload = Button(top, text="Cartooning an Image", command=upload, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
upload.pack(side=TOP, pady=50)
top.mainloop()
