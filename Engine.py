"""
DatasetProcessor module handles the processing of the dataset
Dataset may include the following:
- images (jpg, png, jpeg)
- videos (mp4)
- pdfs (pdf)

Developed By : Huzaifa Jawad
"""

import os
import time
from tkinter import *
from PIL import ImageTk, Image

class AppEngine:
    """Main Data processing class"""
    
    def __init__(self, parent, prompt):
        """constructor for Prompt processor class"""
        self.mainEngine(prompt)
        parent.PAlert.destroy()
        parent.notify("Processing Complete!", 1)
        parent._status_ = 1
        
    def mainEngine(self, prompt):
        """Main Engine"""
        time.sleep(1)
        pass

    
