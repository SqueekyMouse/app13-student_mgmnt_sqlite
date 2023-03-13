from PyQt6.QtWidgets import QApplication, QLabel,QWidget,QGridLayout,\
    QLineEdit,QPushButton,QMainWindow,QTableWidget,QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3

# commit: add data to table from sql Sec46

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
        self.table.verticalHeader().setVisible(False) # hide the table id coumn!!!
        self.setCentralWidget(self.table)
        

    def load_data(self):
        connection=sqlite3.connect('database.db')
        result=connection.execute('SELECT * FROM students') # its a cursor obj!!!
        # print(list(result)) # list of tuple [(1, 'John Smith', 'Math', 49111222333), ...
        # for id,name,course,phone in list(result):
        #     print(id,name,course,phone)

        self.table.setRowCount(0) # to reset the table so rows are not duplicated when resizing window etc.!!!
        for row_num,row_data in enumerate(result):
            self.table.insertRow(row_num)
            for colum_num,data in enumerate(row_data):
                print(row_data)
                self.table.setItem(row_num,colum_num,QTableWidgetItem(str(data)))
        connection.close()


        




app=QApplication(sys.argv)
age_calculator=MainWindow()
age_calculator.show()
age_calculator.load_data()
sys.exit(app.exec())
