from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel,QWidget,QGridLayout,\
    QLineEdit,QPushButton,QMainWindow,QTableWidget,QTableWidgetItem,\
    QDialog,QVBoxLayout,QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3

# commit: search-student sub menu impl Sec46

#QMainWindow provides menu bar status bar and stuff!!!
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Student Management System')
        self.setMinimumSize(450,400)

        # menu items
        file_menu_item=self.menuBar().addMenu('&File')
        help_menu_item=self.menuBar().addMenu('&Help')
        edit_menu_item=self.menuBar().addMenu('&Edit')

        add_student_action=QAction('Add Student',self)
        add_student_action.triggered.connect(self.insert) # mention the method to conncet it to 
        file_menu_item.addAction(add_student_action)

        about_action=QAction('About',self)
        help_menu_item.addAction(about_action)
        # about_action.setMenuRole(QAction.MenuRole.NoRole) # needed on mac if help menu is not shown!!!

        search_action=QAction('Search',self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

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
                # print(row_data)
                self.table.setItem(row_num,colum_num,QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog=InsertDialog() # another class we create
        dialog.exec()

    def search(self):
        dialog=SearchDialog()
        dialog.exec()



class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout=QVBoxLayout() # simple vertical layout

        # Add student name widget
        self.student_name=QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)

        # Add courses combobox
        self.course_name=QComboBox()
        courses=['Biology','Math','Astronomy','Physics']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add mobile Widget
        self.mobile=QLineEdit()
        self.mobile.setPlaceholderText('Name')
        layout.addWidget(self.mobile)

        # Add submit button
        button=QPushButton('Register')
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)


    def add_student(self):
        name=self.student_name.text()
        course=self.course_name.itemText(self.course_name.currentIndex())
        mobile=self.mobile.text()
        connection=sqlite3.connect('database.db')
        cursor=connection.cursor()
        cursor.execute('INSERT INTO students (name,course,mobile) VALUES (?,?,?)',
                      (name,course,mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student')
        self.setFixedSize(300,300)

        layout=QVBoxLayout()

        self.search_box=QLineEdit()
        self.search_box.setPlaceholderText('Name')
        layout.addWidget(self.search_box)

        button=QPushButton('Search')
        button.clicked.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name=self.search_box.text()
        # print(f'Search: {name}')
        connection=sqlite3.connect('database.db')
        cursor=connection.cursor()
        result=cursor.execute('SELECT * FROM students WHERE name=?',(name,))
        rows=list(result)
        print(rows)
        items=main_window.table.findItems(name,Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item) # this is a table item object!!!
            # to set the name column as selected
            main_window.table.item(item.row(),1).setSelected(True)

        cursor.close()
        connection.close()


app=QApplication(sys.argv)
main_window=MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
