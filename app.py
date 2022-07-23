import sys
from PyQt5.QtWidgets import QApplication
from viewer import ImageViewer


if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_dir_path = input("Enter Image dir path: ")
    win = ImageViewer(image_dir_path)
    win.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        print("Exiting error: ", e)
