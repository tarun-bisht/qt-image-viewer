import os
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QImage, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QLabel, QShortcut

import viewer


class LabelImage(QLabel):
    def __init__(self):
        super(LabelImage, self).__init__()
        self.setScaledContents(True)

    def load(self, image_path):
        pixmap = QPixmap.fromImage(QImage(image_path))
        self.setPixmap(pixmap)
        self.adjustSize()


# noinspection PyUnresolvedReferences
class ImageViewerGUI(QMainWindow):
    def __init__(self, image_dir):
        super(ImageViewerGUI, self).__init__()
        self.images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if
                       (f.endswith(".jpeg") or f.endswith(".jpg") or f.endswith(".png"))]
        self.num_images = len(self.images)
        self.img_index = 0
        self.scale_factor = 1.0
        # load UI
        self.setup_ui()
        self.shortcut_previous = QShortcut(QKeySequence("Left"), self)
        self.shortcut_next = QShortcut(QKeySequence("Right"), self)

        self.image_holder = LabelImage()
        self.scroll_area.setWidget(self.image_holder)

        if self.num_images > 0:
            self.update_image_status()
            self.image_holder.load(self.images[self.img_index])
        else:
            self.image_holder.setText("No images to preview")
            self.statusBar().showMessage(f"No images in the directory")

        self.connect_gui_buttons()
        self.connect_menu_actions()
        self.connect_window_shortcuts()

    def setup_ui(self):
        ui_file = os.path.join(os.path.dirname(viewer.__file__), "viewer.ui")
        loadUi(ui_file, self)

    def connect_gui_buttons(self):
        self.previous_btn.clicked.connect(lambda: self.change_image(-1))
        self.next_btn.clicked.connect(lambda: self.change_image(1))

    def connect_menu_actions(self):
        self.action_zoom_in.triggered.connect(self.zoom_in)
        self.action_zoom_out.triggered.connect(self.zoom_out)
        self.action_normal.triggered.connect(self.normal_size)

    def connect_window_shortcuts(self):
        self.shortcut_previous.activated.connect(lambda: self.change_image(-1))
        self.shortcut_next.activated.connect(lambda: self.change_image(1))

    def change_image(self, factor):
        self.img_index += factor
        if self.img_index < 0:
            self.img_index = 0
        if self.img_index >= self.num_images:
            self.img_index = self.num_images - 1
        self.image_holder.load(self.images[self.img_index])
        self.update_image_status()

    def zoom_in(self):
        self.scale_image(1.25)

    def zoom_out(self):
        self.scale_image(0.8)

    def normal_size(self):
        self.image_holder.adjustSize()
        self.scale_factor = 1.0

    def scale_image(self, factor):
        self.scale_factor *= factor
        self.image_holder.resize(self.scale_factor * self.image_holder.pixmap().size())

        self.adjust_scrollbar(self.scroll_area.horizontalScrollBar(), factor)
        self.adjust_scrollbar(self.scroll_area.verticalScrollBar(), factor)

        self.action_zoom_in.setEnabled(self.scale_factor < 3.0)
        self.action_zoom_out.setEnabled(self.scale_factor > 0.333)

    def update_image_status(self):
        self.statusBar().showMessage(f"showing image {self.img_index + 1} out of {self.num_images} images")

    @staticmethod
    def adjust_scrollbar(scrollbar, factor):
        scrollbar.setValue(int(factor * scrollbar.value() + ((factor - 1) * scrollbar.pageStep() / 2)))