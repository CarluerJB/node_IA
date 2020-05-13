from annotation_graphic_point import Graphic_point

# point data for actual image
class point():
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.grPoint = Graphic_point(self)
        self.coordinates = (0,0)
        self.scene.get_actual_image().addPoint(self)
        self.show()

    @property
    def pos(self):
        return self.grPoint.pos()        # QPointF

    def setPos(self, x, y):

        self.grPoint.setPos(x, y)
        self.coordinates = (x,y)

    def x(self):
        return self.coordinates[0]

    def y(self):
        return self.coordinates[1]

    def show(self):
        self.scene.grScene.addItem(self.grPoint)

    def hide(self):
        self.scene.grScene.removeItem(self.grPoint)
