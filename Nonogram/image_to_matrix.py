import cv2
'''
This class is created with the objective of transforming an image into an image made up with ascii characters instead of
pixels.
'''
ASCII_TRANSLATION = {
    7 : ".",
    6 : ":",
    5 : "-",
    4 : "=",
    3 : "%",
    2 : "&",
    1 : "#",
    0 : "@",
}

class ImageToAscii:

    def __init__(self, image_path, resize=10):
        self.image_path = image_path
        self.image = None
        self.resize = resize
        self.ascii_image = None
        self.original_height = None
        self.original_width = None

    # This function takes an image and resize it to a new format
    # This has to be do to make the image on the correct size so a terminal can show the ascii image with no problem
    # the image is just an opencv image, the default rescaling means a 1//rescaling

    def __resize_image__(self, image, rescaling=10):
        new_height = image.shape[0] // rescaling
        new_width = image.shape[1] // rescaling
        resolution = (new_width, new_height)
        return cv2.resize(image, resolution, interpolation=cv2.INTER_AREA)

        # This function handles the main focus of this class that is the translation of the image into ascii
        # It takes 1 single opencv image and it return an string with the frame alreade translate it

    def __image_to_ascii__(self, image, resize):
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_gray = self.__resize_image__(img_gray, resize)
        shape_img = img_gray.shape[:2]
        ascii_transformation = ""

        for i in range(shape_img[0]):
            for j in range(shape_img[1]):
                luminosity_tier = img_gray[i][j] // 32
                ascii_transformation += ASCII_TRANSLATION[luminosity_tier] * 3
            ascii_transformation += "\n"
        return ascii_transformation

    #This function tries to generate the ascii image using the path on the constructor
    #If the program couldn't find the image it will return false
    def generate_image(self):
        image = cv2.imread(self.image_path, 0)

        if image == None:
            print("WARNING!!!\nCouldn't find the image to transform, please verify the path of the image.")
            return False

        self.ascii_image = self.__image_to_ascii__(self.image, self.resize)
        self.original_height = image.shape[0]
        self.original_width = image.shape[1]

        return True

    def show_ascii_image(self):
        if self.ascii_image == None:
            return "Coudn't find any ascii image, please try to generate one"

        else:
            return self.ascii_image