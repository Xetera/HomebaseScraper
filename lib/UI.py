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
        self.ui.chrome_freeze_frame.show()
        lib.fetchInfo()

    def calculate_tips(self):

        if self.ui.dinein_text.text == "" or self.ui.togo_text.text == "":
            return

        dine_in = self.ui.dinein_text.text()
        togo = self.ui.togo_text.text()

        # TODO: automatically add $ before the first number following a +
        # cuz it looks good

        if "+" in dine_in:
            # string converted to int to sum
            split = map(int, dine_in.split('+'))
            dine_in = sum(split)
            # text must be displayed as string to prevent errors
            self.ui.dinein_text.setText(str(dine_in))
            # user knows something happened
        if '+' in togo:
            split = map(int, togo.split('+'))
            togo = sum(split)
            self.ui.togo_text.setText(str(togo))

        nacho_tips = togo
        connie_tips = math.floor(int(dine_in) * (2/3))
        my_tips = math.floor(int(dine_in) * (1/3))

        # this will obviously be created dynamically once program is working
        string = \
            "Nacho's Tips: ${}\nConnie's Tips: ${}\nMy Tips: ${}".format(nacho_tips, connie_tips, my_tips)
        print(string)
        # not append because we want the text to clear when recalculating
        self.ui.tips_output.setText(string)

    def setup_style(self):
        self.ui.chrome_freeze_frame.hide()

    def setup_events(self):

        self.ui.Tab1.autoFillBackground()
        # anonymous functions required to prevent defined functions from running as soon as the program starts
        # sort of like a reverse closure
        self.ui.getHours.clicked.connect(lambda: self.get_employee_hours())
        self.ui.get_tips.clicked.connect(lambda: self.calculate_tips())


def main():
    print("Program is now running.")
    # pass commandline arguments into Qt
    app = QtWidgets.QApplication(sys.argv)
    main_window = OliveTree()
    # we want these to be set up before we show the window
    main_window.setup_style()
    main_window.setup_events()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
