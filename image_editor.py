import shutil
from PIL import Image 

class ImageEditor():

    def __init__(self):
        self.imagePath='/Users/mattnaranjo/documents/fannotated/images/'
    
    def isJPG(self, filename):
        if filename.lower().endswith(".jpg"):
            return True
        return False

    def copyPhoto(self, filepath):
        if self.isJPG(filepath):
            image_name = filepath.split("/")[-1]
            new_filepath = self.imagePath + image_name
            shutil.copyfile(filepath, new_filepath)

        else:
            image_name = filepath.split("/")[-1]
            image_name_no_ext = image_name.split(".")[0]
            print(image_name, image_name_no_ext)
            new_filepath = self.imagePath + image_name_no_ext + '.jpg'

            im = Image.open(filepath)

            # Make a background, same size filled with solid white
            result = Image.new('RGB', (im.width,im.height), color=(255,255,255))

            # Paste original image over white background and save
            result.paste(im,im)
            result.save(new_filepath)

        return new_filepath

    def addMainPhoto(self, filepath, article_name):
        image_name = article_name.split('/')[-1]
        image_name= image_name.split('.')[0]
        if self.isJPG(filepath):
            new_filepath = self.imagePath + image_name + '.jpg'
            im = Image.open(filepath)
            im.putalpha(255)
            w, h = im.size
            # Make a background, same size filled with solid white
            result = Image.new('RGB', (w,h), color=(255,255,255))

            # Paste original image over white background and save
            result.paste(im,im)
            while w/2 >= 1200 and h/2 >= 600:
                result = result.resize((w//2,h//2), Image.ANTIALIAS)
                w, h = result.size

            #adjusted size
            y = (h-600)/2
            x = (w-1200)/2
            resized = (x,y,w-x,h-y)
            result = result.crop(resized)
            result.save(new_filepath)

        else:
            new_filepath = self.imagePath + image_name + '.jpg'

            im = Image.open(filepath)
            im.putalpha(255)

            # Make a background, same size filled with solid white
            result = Image.new('RGB', (im.width,im.height), color=(255,255,255))

            # Paste original image over white background and save
            result.paste(im,im)
            result = result.resize((1200,600), Image.ANTIALIAS)
            result.save(new_filepath)

        return new_filepath

