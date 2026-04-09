# lvgl8_img_convert
This code will convert an image file ( i.e bmp,jpg,png ) to a RGB565 bin file that can be used for embedded devices using LVGL version 8. ( Such as the ESP32)

The code also resizes the image to 156 x 156 ( Change this is you have different requirements)
I wrrote this app for use with Python 3.11.0

> install the following python library : 'pip install pillow'

So this application will do the following : 
 - Loads the image file
 - resizes it to 156 x 156 pixels
 - converts it to RGB565   ( If you want Swapped bytes, Change line 71 in the code swapped =  f.write(bytes([low, high])) normal =  f.write(bytes([high, low]))  )
 - saves the file as <filename.bin>

### To use 
Type the below command in the project folder. you must also save the image file in the same folder that you want to convert.

Below is an example of a file named *myimage.png* that i want to convert.

`python lvgl_convert.py myimage.png`

This will output a file in the same directory as: *myimage.bin*

---



