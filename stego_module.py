 # PIL module is used to extract 
# pixels of image and modify it 
from PIL import Image 
import base64
import numpy as np
import os
import stepic

# Embed data into image 
def encode(img,data_filename): 

    image = Image.open(img, 'r')   
    with open(data_filename[:-4] + ".enc",'rb') as fo:
        data = fo.read()
    
    if (len(data) == 0): 
        raise ValueError('Data is empty') 
    
    filename = os.path.basename(img)
    newimg = image.copy() 
    newimg = stepic.encode(newimg,base64.b64encode(data))
    new_img_name = filename[:-4] +'_stego_image.png'
    newimg.save(new_img_name, str(filename.split(".")[1].upper())) 
    
    imgs = [filename, new_img_name]
    concatenated = Image.fromarray(
        np.concatenate(
            [np.array(Image.open(x)) for x in imgs],
            axis=1
        )
    )
    concatenated.save("difference_"+filename, str(filename.split(".")[1].upper()))
    concatenated.show();
  
# Extract the data from the image 
def decode(img): 
    image = Image.open(img, 'r') 
    data = stepic.decode(image)
 
    with open("extracted_text.enc",'wb') as fo:
            fo.write(bytes(base64.b64decode(bytes(data,encoding='utf-8'))))

            
