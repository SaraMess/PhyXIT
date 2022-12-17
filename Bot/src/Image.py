#**************************************************#
#             Imager Class File                    #
#**************************************************#
#   Authors : Sara MESSARA - Clément PAGES         #
#**************************************************#


#========================================#
#       Modules used in this file        #
#========================================#


import logging
from PIL import Image as img, ImageFont as font, ImageDraw, UnidentifiedImageError


#===============================#
#       Class Declaration       #
#===============================#

class Image() :
    """This class provides methods to generate an image. An image is composed of a background image
    and elements added on top of it, such as other images, or text elements"""

    def __init__(self, backgroundImagePath : str, width : int = 1050, height : int = 700) -> None:
        """Create an image from the image pointed by the specified path. Loaded image is resized
        according to optional width and height arguments. If these parameters is not set, image
        is not resized and keep its original dimensions.
        ## Parameters :
        * `backgroundImagePath` : string representing path to the image
        * `width` : optional. If specified, new width for the loaded image
        * `height` : optional. If specified, new height for the loaded image

        ## Return : not applicable
        
        ##Exceptions:
        * `ValueError` : if specified width or height have negative value"""

        if width < 0 or height < 0 :
            raise ValueError(f"Width or height must have positive value. Given value w = {width}, h = {height}")
        #Try to load the specified image. If it doesn't exist, create a new image with black background and default size:
        try:
            logging.info(f"Loading image from {backgroundImagePath}...")
            self.backgroundImage = img.open(backgroundImagePath)
            self.backgroundImage = self.backgroundImage.resize((width, height))
        except (FileNotFoundError, UnidentifiedImageError):
            logging.error(f"Image at {backgroundImagePath} cannot be found. Please check the path")
            logging.info(f"Creating an image with black background")
            self.backgroundImage = img.new("RGBA", (width, height))

        self.drawTool = ImageDraw.ImageDraw(self.backgroundImage)
        self.height = self.backgroundImage.height
        self.width = self.backgroundImage.width


    #Getters and setters:
    def getImageSize(self) -> tuple:
        """Return size of this image as tuple
        ## Parameters:
        not applicable
        ## Return value:
        Image dimensions, as a tuple (`width`, `height`)"""

        return  self.backgroundImage.size


    def resizeImage(self, width : int, height : int) -> None:
        """Resize image according to specified width and height
        ## Parameters:
        * `width` : new width for this image
        * `height` : new height for this image

        ## Return value: not applicable"""

        self.backgroundImage.resize((width, height))
        logging(f"Image {self.backgroundImage.__str__}")


    def addMask(self, maskColor : str, alpha : int, size : tuple, position : tuple, rotationAngle : float = 0.) -> None:
        """Add a new mask to the image, with specified `maskColor` and `alpha` value.
        ## Parameters :
        * `maskColor` : color of the mask to be generated
        * `alpha` : alpha value for the mask to be generated
        * `size` :  size of the mask to be generated as a tuple, with first width and then height
        * `position` : coordinates where place the mask to be generated as a tuple
        * `rotationAngle` : angle rotation for the mask, if specified
        ## Return value: 
        not applicable
        ## Exceptions:
        * `ValueError` : if one of the specified argument has an incorrect value"""

        #Arguments checks :
        if alpha < 0 or alpha > 255 :
            logging.error(f"Specified value for the argument 'alpha' ({alpha}) is not correct")
            raise ValueError(f"Alpha argument must be in 0-255 range. Given value : {alpha}")
        if len(size) != 2 or size[0] < 0 or size[1] < 0:
            logging.error(f"Tuple size must have a len of 2 : (width, height). Current size: {len(size)}")
            raise ValueError("addMask : tuple specified for mask size is incorrect.")
        if len(position) != 2 or position[0] < 0 or position[1] < 0:
            logging.error(f"Specified value for width and height must be positive")
            raise ValueError("addMask : tuple specified for mask position is incorrect.")

        #Creation of the mask :
        mask = img.new("RGBA", size, maskColor)
        mask.putalpha(alpha)
        mask = mask.rotate(rotationAngle)

        #Add mask to this image :
        self.backgroundImage.paste(mask, position, mask)


    def addIcon(self, iconPath : str, size : tuple, position : tuple, rotationAngle : float = 0.) -> None:
        """Add the icon pointed by the specified path to this image, with the given size, position and
        rotation angle.
        ## Parameters :
        * `iconPath` : path to the icon to add on the image as string
        * `size` : icon size on the image as a tuple (width, height)
        * `position` : position where placed icon on this image, as a tuple (x, y)
        * `rotationAngle` : rotation angle for the icon on this image
        ## Return value: 
        not applicable
        ## Exceptions:
        * `ValueError` : if one of the specified argument has an incorrect value"""

        #Arguments checks :
        if len(size) != 2 or size[0] < 0 or size[1] < 0:
            logging.error(f"Tuple size for icon size must have a len of 2 : (width, height). Current size: {len(size)}")
            raise ValueError("addIcon : tuple specified for icon size is incorrect.")
        if len(position) != 2 or position[0] < 0 or position[1] < 0:
            logging.error(f"Tuple size for icon position must have a len of 2 : (width, height). Current size: {len(position)}")
            raise ValueError("addIcon : tuple specified for icon position is incorrect.")
        #Try to load and resize specified icon:
        try:
            icon = img.open(iconPath).convert("RGBA")
            icon = icon.resize(size).rotate(rotationAngle)
        except (FileNotFoundError, UnidentifiedImageError):
            logging.error(f"Specified icon at {iconPath} doesn't exist. Please check the icon path. Icon can't be added to this image")
        else:
            #Add icon to this background image :
            self.backgroundImage.paste(icon, position, icon)


    def drawText(self, text : str, textFont : font.ImageFont, position : tuple, color = "WHITE") -> None:
        """Write specified text on this image, with the given font and color and at the specified
        position
        ## Parameters:
        * `text` : text to write on this image
        * `textFont` : font used to write the text on this image
        * `position` : position where write the text on this image, as a tuple (x, y)
        * `color` : color of the text to write, default color is white

        ## Return value: 
        not applicable
        ## Exceptions:
        * ValueError : if one of the specified argument has an incorrect value"""
        #Arguments checks :

        if len(position) != 2 or position[0] < 0 or position[1] < 0:
            logging.error(f"Tuple size for icon position must have a len of 2 : (width, height). Current size: {len(position)}")
            raise ValueError("addMask : tuple specified for mask position is incorrect.")
        if textFont is None :
            raise ValueError("drawText : Font must be defined")

        #Write text on this image :
        self.drawTool.text(position, text, color, font=textFont)


    def saveImage(self, saveLocationPath : str, format : str = "png") -> None :
        """Save this image at the specified location and format
        ## Parameters:
        * `saveLocationPath` : path where save this image, as a string
        * `format` : save format for this image, default is png
        ## Return value: 
        not applicable
        ##Exceptions:
        * ValueError : if specified `format` could not be determined
        * IOError : if the file where save this image cannot be created"""

        self.backgroundImage.save(saveLocationPath, format)