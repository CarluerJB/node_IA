from PyQt5.QtWidgets import QGraphicsPixmapItem
from annotation_graphic_scene import QDMGraphicsScene
from annotation_image import Image

class ImageScene():
    def __init__(self):
        super().__init__()

        self.scene_width = 64000
        self.scene_height = 64000
        self.image_annotation = []
        self.image = QGraphicsPixmapItem()
        self.actual_image=0
        self.initUI()
        self.init_images()
        self.set_image(0)

    def init_images(self):
        # TO REMOVE IN FUTURE
        self.image_annotation.append(Image("le_parrain.jpg"))
        self.image_annotation.append(Image("DiagVS1Dresult_support_10_0.6_100.png"))



    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def set_image(self, index=0):
        if len(self.image_annotation)>index:
            self.actual_image = index
            self.image.setPixmap(self.image_annotation[index].pixmap)
            self.load_points()


    def set_next_image(self):
        # TO REMOVE IN FUTURE
        for point in self.image_annotation[self.actual_image].points:
            point.hide()
        self.actual_image+=1
        if((self.actual_image)>=len(self.image_annotation)):
            self.actual_image=0

        self.set_image(self.actual_image)


    def get_actual_image(self):
        return self.image_annotation[self.actual_image]

    def load_points(self):
        for point in self.image_annotation[self.actual_image].points:
            point.show()
