# -*- coding: UTF-8 -*-
__author__ = 'zhaopan'

'''
https://gist.github.com/jrsmith3/9947838#file-pdfmod-py
http://docs.wand-py.org/en/0.4.4/guide/install.html
http://www.pythonforbeginners.com/gui/how-to-use-pillow
import glob => http://blog.csdn.net/csapr1987/article/details/7469769

import sys
import os
import subprocess
import settings

IMAGE_PATH = os.path.join(settings.MEDIA_ROOT , 'pdf_input' )

def extract_images(pdf):
   output = 'temp.png'
   cmd = 'convert ' + os.path.join(IMAGE_PATH, pdf) + ' ' + os.path.join(IMAGE_PATH, output)
   subprocess.Popen(cmd.split(), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
'''
from PyPDF2 import PdfFileWriter, PdfFileReader


"""
This script was used to create the figures for http://jrsmith3.github.io/sample-logs-the-secret-to-managing-multi-person-projects.html from a PDF file containing some old CMU sample logs.
"""

import PyPDF2
from wand.image import Image
from PIL import Image
import io
import os


def pdf_page_to_png(src_pdf, pagenum = 0, resolution = 72,):
    """
    Returns specified PDF page as wand.image.Image png.

    :param PyPDF2.PdfFileReader src_pdf: PDF from which to take pages.
    :param int pagenum: Page number to take.
    :param int resolution: Resolution for resulting png in DPI.
    """
    dst_pdf = PyPDF2.PdfFileWriter()
    dst_pdf.addPage(src_pdf.getPage(pagenum))

    pdf_bytes = io.BytesIO()
    dst_pdf.write(pdf_bytes)
    pdf_bytes.seek(0)

    img = Image(file = pdf_bytes, resolution = resolution)
    img.convert("png")

    return img


# Main
# ====
src_filename = "babujingang.pdf"

src_pdf = PyPDF2.PdfFileReader(file(src_filename, "rb"))

# What follows is a lookup table of page numbers within sample_log.pdf and the corresponding filenames.
pages = [{"pagenum": 22,  "filename": "samplelog_jrs0019_p1"},
         {"pagenum": 23,  "filename": "samplelog_jrs0019_p2"},
         {"pagenum": 124, "filename": "samplelog_jrs0075_p3_2011-02-05_18-55"},]

# Convert each page to a png image.
for page in pages:
    big_filename = page["filename"] + ".png"
    small_filename = page["filename"] + "_small" + ".png"

    img = pdf_page_to_png(src_pdf, pagenum = page["pagenum"], resolution = 300)
    img.save(filename = big_filename)

    # Ensmallen
    img.transform("", "200")
    img.save(filename = small_filename)


# Deal with the cropping for JRS0070.
jrs0070 = {"pagenum": 109, "filename": "samplelog_jrs0070_p1"}

img = pdf_page_to_png(src_pdf, pagenum = jrs0070["pagenum"], resolution = 300)

big_filename = jrs0070["filename"] + ".png"
small_filename = jrs0070["filename"] + "_small" + ".png"

# Crop
img.crop(bottom = 1000)

# Save
img.save(filename = big_filename)

# Ensmallen
img.transform("", "200")
img.save(filename = small_filename)





