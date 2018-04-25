# SKIPUNS: CAPTCHA solver in python

* Author: consachapi@gmail.com

This is a solver for a very specific and easy-to-solve CAPTCHAs like the one proposed here.

### The idea
In this example we are going to use the following images.

![alt text](https://github.com/consachapi/skipuns/blob/master/test1.jpeg)

![alt text](https://github.com/consachapi/skipuns/blob/master/test2.jpeg)

### Prerequisites

The only thing you need installed is Python 3.x

```
apt-get install python3
```

You also require to have Scapy and Shodan modules installed
```
pip install pytesseract
```

```
pip install pytesseract
```

Linux

```
apt-get install tesseract-ocr
```

Windows

Link: https://github.com/UB-Mannheim/tesseract/wiki

Configure tesseract-oct on pytesseract

Add the directory where the tesseract-OCR binaries are located to the Path variables, probably C:\Program Files\Tesseract-OCR.

Change in pytesseract.py

```
#tesseract_cmd = "tesseract"
tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```


### Demo skipuns

![](https://github.com/consachapi/skipuns/blob/master/demo.JPG)


### USAGE 
From the shell

```bash
git clone https://github.com/consachapi/skipuns.git
cd skipuns
$ python skipuns.py -u cod_login   

```
