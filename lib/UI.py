import math
import sys
from PyQt5 import QtWidgets
import Template as template
import scrape_homebase as lib


class OliveTree(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super(OliveTree, self).__init__(parent=parent)
        self.ui = template.Ui_MainWindow()
        self.ui.setupUi(self)

    def get_employee_hours(self):
        lib.fetchInfo()

    def calculate_tips(self):
        dine_in = self.ui.dinein_text.text()
        togo = self.ui.togo_text.text()

        nacho_tips = dine_in
        connie_tips = math.floor(int(togo) * (2/3))
        my_tips = math.floor(int(togo) * (1/3))

        string = \
            "Nacho's Tips: {}\nConnie's Tips: {}\nMy Tips: {}".format(nacho_tips, connie_tips, my_tips)
        print(string)
        self.ui.tips_output.setText(string)

    def setup_events(self):
        self.ui.getHours.clicked.connect(lambda: self.get_employee_hours())
        self.ui.get_tips.clicked.connect(lambda: self.calculate_tips())


def main():
    print("hello")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = OliveTree()
    MainWindow.setup_events()
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
