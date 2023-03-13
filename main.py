from PyQt6.QtWidgets import QApplication, QLabel,QWidget,QGridLayout,\
    QLineEdit,QPushButton,QMainWindow,QTableWidget
from PyQt6.QtGui import QAction
import sys
# commit: add table to main window Sec46

#QMainWindow provides menu bar status bar and stuff!!!
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Student Management System')

        # menu items
        file_menu_item=self.menuBar().addMenu('&File')
        help_menu_item=self.menuBar().addMenu('&Help')

        add_student_action=QAction('Add Student',self)
        file_menu_item.addAction(add_student_action)

        about_action=QAction('About',self)
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole) # needed on mac if help menu is not shown!!!

        self.table=QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('Id','Name','Course','Mobile'))
        self.setCentralWidget(self.table)
        

    def load_data(self):
        # self.table
        pass




app=QApplication(sys.argv)
age_calculator=MainWindow()
age_calculator.show()
sys.exit(app.exec())
