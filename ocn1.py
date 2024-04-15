import io
import qrcode
import sqlite3
from PyQt5 import QtCore
import transliterate
import sys
import datetime
import hashlib
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.Qt import *


class MainWindow(QMainWindow):
    def __init__(self, ap):
        """Графический дизайн окна ввода данных"""
        super().__init__()
        self.ap = ap
        self.name = ''
        self.number = ''
        self.setWindowFlags(Qt.FramelessWindowHint)
        uic.loadUi("Project Qt_1.ui", self)
        self.timer = QTimer(self)
        self.lineEdit_8.setPlaceholderText('Фамилия')
        self.lineEdit_7.setPlaceholderText('Имя')
        self.lineEdit_3.setPlaceholderText('Отчество')
        self.lineEdit_2.setPlaceholderText('Дата рождения')
        self.lineEdit_4.setPlaceholderText('Серия паспорта')
        self.lineEdit_5.setPlaceholderText('Номер паспорта')
        self.lineEdit_6.setPlaceholderText('Кем выдан паспорт')
        self.setWindowIcon(QIcon('Photo_ocn_ocn.ico'))
        self.setWindowTitle('Проверка данных')
        self.setStyleSheet('QMainWindow#MainWindow'
                           '{'
                           'background-image: url(Photo_ocn_ocn1.png); '
                           'background-repeat: no-repeat;'
                           ' background-position: center;'
                           '}'
                           """
                           QPushButton {
                                border: none;
                           }
                           QPushButton#pushButton {
                            max-height: 48px;
                            border-top-right-radius:   20px;
                            border-bottom-left-radius: 20px;
                            background-color:  #15c69a;
                           }
                           #pushButton:hover {
                                background-color: #99f2da;
                           }
                           #pushButton:pressed {
                                background-color: #0fffa7;
                           }
                           QPushButton#pushButton_2 {
                                max-height: 48px;
                                border-top-right-radius:   20px;
                                border-bottom-left-radius: 20px;
                                background-color:  #15c69a;
                           }
                           #pushButton_2:hover {
                                background-color: #99f2da;
                           }
                           #pushButton_2:pressed {
                                background-color: #0fffa7;
                           }
                           QLineEdit {
        border-width: 3px;
        border-style: solid;
        border-color: #15c69a;
    }
    QLineEdit:focus {
        border-color: rgb(255, 156, 0);
    }
                           """)
        self.pushButton_2.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.run)

    def back(self):
        """Реализация кнопки 'назад'"""
        self.f = Necessary_Action()
        self.f.show()
        self.close()

    def run(self):
        """Считывание данных и их проверка"""
        hex_dig = ''
        self.label.setText('')
        n = []
        sname = self.lineEdit_8.text()
        name = self.lineEdit_7.text()
        mname = self.lineEdit_3.text()
        date_of_birth = self.lineEdit_2.text()
        passp_series = self.lineEdit_4.text()
        passp_number = self.lineEdit_5.text()
        w_iss_passp = self.lineEdit_6.text()
        clinic_number = '012345678911'
        if all([self.check_empt(sname, 'Фамилия'),
                self.check_empt(name, 'Имя'),
                self.check_empt(date_of_birth, 'Др')]) \
                and all([self.check_passp(passp_series, 'Серия'),
                         self.check_passp(passp_number, 'Номер')]):
            pal = self.label.palette()
            pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("green"))
            self.label.setPalette(pal)
            list1 = [sname.capitalize(), name.capitalize(),
                     mname.capitalize(), date_of_birth,
                     passp_series, passp_number,
                     w_iss_passp, clinic_number]
            stri = ''
            for i in list1:
                for j in i:
                    stri += str(ord(j))
            hash_object = hashlib.sha384(stri.encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            self.label.setText('Данные верные')
        else:
            pal = self.label.palette()
            pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
            self.label.setPalette(pal)
            if len(self.label.text()) == 0:
                self.label.setText('Ошибка в данных')
                return False
        con = sqlite3.connect('project.db')
        n.append(hex_dig)
        """Проверка на наличие пользователя в базе данных"""
        with con:
            try:
                cur = con.cursor()
                result = cur.execute('''SELECT * FROM Pols
                                        WHERE Hash = ?''', n).fetchall()
                if len(result) == 0:
                    pal = self.label.palette()
                    pal.setColor(QtGui.QPalette.WindowText,
                                 QtGui.QColor("red"))
                    self.label.setPalette(pal)
                    self.label.setText('Данного пользователя нет, обратитесь к администратору')
                else:
                    self.run1(hex_dig)
            except sqlite3.OperationalError:
                pass

    def check_empt(self, arg, arg2):
        """Проверка основных данных на пустоту и содержание"""
        if arg2 == 'Фамилия':
            if len(arg) != 0:
                if not any(map(str.isdigit, arg)):
                    self.lineEdit_8.setStyleSheet("QLineEdit { color: black; background-color: white;}")
                    return True
            self.lineEdit_8.setStyleSheet("QLineEdit { color: black; background-color: red;}")
            return False
        if arg2 == 'Имя':
            if len(arg) != 0:
                if not any(map(str.isdigit, arg)):
                    str(arg)
                    self.lineEdit_7.setStyleSheet("QLineEdit { color: black; background-color: white;}")
                    return True
            self.lineEdit_7.setStyleSheet("QLineEdit { color: black; background-color: red;}")
            return False
        elif arg2 == 'Др':
            try:
                if datetime.datetime.strptime(arg, "%d.%m.%Y"):
                    self.lineEdit_2.setStyleSheet("QLineEdit { color: black; background-color: white;}")
                    return True
            except ValueError:
                self.lineEdit_2.setStyleSheet("QLineEdit { color: black; background-color: red;}")
                return False

    def check_passp(self, arg, arg2):
        """Проверка введенных паспортных данных"""
        if arg2 == "Серия":
            if len(arg) == 4:
                try:
                    int(arg)
                    self.lineEdit_4.setStyleSheet("QLineEdit { color: black; background-color: white;}")
                    return True
                except ValueError:
                    self.lineEdit_4.setStyleSheet("QLineEdit { color: black; background-color: red;}")
                    return False
            self.lineEdit_4.setStyleSheet("QLineEdit { color: black; background-color: red;}")
            return False
        elif arg2 == "Номер":
            if len(arg) == 6:
                try:
                    int(arg)
                    self.lineEdit_5.setStyleSheet("QLineEdit { color: black; background-color: white;}")
                    return True
                except ValueError:
                    self.lineEdit_5.setStyleSheet("QLineEdit { color: black; background-color: red;}")
                    return False
            self.lineEdit_5.setStyleSheet("QLineEdit { color: black; background-color: red;}")
            return False

    def card(self, hash1):
        """Запуск карты пользователя, если данные пользователя прошли проверку"""
        self.close()
        self.cardform = Card(hash1)
        self.cardform.show()

    def record(self, hash1):
        """Запуск записи к врачу, если данные пользователя прошли проверку"""
        self.close()
        self.rec = Record(hash1)
        self.rec.show()

    def run1(self, hex_dig):
        """Выбор необходимого действия по переданным аргументам"""
        if self.ap == 'card':
            self.card(hex_dig)
        elif self.ap == 'record':
            self.record(hex_dig)


class Necessary_Action(QMainWindow):
    def __init__(self):
        """Главное окно для выбора операции"""
        super().__init__()
        uic.loadUi("Project Qt_ocn.ui", self)
        self.setFixedSize(368, 366)
        self.setWindowIcon(QIcon('Photo_ocn_ocn.ico'))
        self.setStyleSheet("""
                           QPushButton {
                                border: none;
                           }
                           QPushButton#pushButton {
                                color: rgb(255, 255, 255);
                                font: bold 20pt "Times New Roman";
                                max-height: 48px;
                                border-top-right-radius:   20px;
                                border-bottom-left-radius: 20px;
                                background-color: #15c69a;
                           }
                           #pushButton:hover {
                                background-color: #ade8ff;
                           }
                           #pushButton:pressed {
                                background-color: #3333ff;
                           }
                           QPushButton#pushButton_3 {
                                color: rgb(255, 255, 255);
                                font: bold 20pt "Times New Roman";
                                max-height: 48px;
                                border-top-right-radius:   20px;
                                border-bottom-left-radius: 20px;
                                background-color: #15c69a;
                           }
                           #pushButton_3:hover {
                                background-color: #ade8ff;
                           }
                           #pushButton_3:pressed {
                                background-color: #3333ff;
                           }
                           QPushButton#pushButton_4 {
                                color: rgb(255, 255, 255);
                                font: bold 20pt "Times New Roman";
                                max-height: 48px;
                                border-top-right-radius:   20px;
                                border-bottom-left-radius: 20px;
                                background-color: #15c69a;
                           }
                           #pushButton_4:hover {
                                background-color: #ade8ff;
                           }
                           #pushButton_4:pressed {
                                background-color: #3333ff;
                           }
                           """)
        self.pushButton_3.clicked.connect(self.run)
        self.pushButton.clicked.connect(self.run1)
        self.pushButton_4.clicked.connect(self.schedule)
        self.setWindowTitle('Основное окно')

    def run(self):
        """Запуск записи к врачу"""
        self.sec = MainWindow('record')
        self.sec.show()
        self.close()

    def run1(self):
        """Запуск карты пользователя"""
        self.sec = MainWindow('card')
        self.close()
        self.sec.show()

    def schedule(self):
        """Запуск расписания"""
        self.sh = Calendr()
        self.sh.show()


class Card(QMainWindow):
    def __init__(self, hash1):
        """По хешу пользователя получение данных о его записи к врачам"""
        super().__init__()
        uic.loadUi("Project Qt_card.ui", self)
        con = sqlite3.connect('project.db')
        self.setWindowTitle("Карта пользователя")
        self.label.setText('Ваши записи')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('Photo_ocn_ocn.ico'))
        self.pushButton.clicked.connect(self.back)
        with con:
            self.cur = con.cursor()
            result = self.cur.execute("""SELECT Name, date1, time1, Status
            FROM Cpns JOIN infDoctors
                ON Cpns.Docinf = infDoctors.id
            WHERE Hash=?""", [hash1]).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            pal = self.label.palette()
            pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
            self.label_2.setPalette(pal)
            self.label_2.setText('Ничего не нашлось')
            return
        else:
            self.tableWidget.setColumnCount(len(result[0]))
            self.titles = ['Doctor', 'Date', 'Time', 'Status']
            self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.modified = {}

    def back(self):
        """Кнопка 'назад'"""
        self.f = Necessary_Action()
        self.f.show()
        self.close()


class Schedule(QMainWindow):
    def __init__(self, date):
        """Создание расписания на основе даты, выбранной в классе Calendr(QMainWindow)"""
        super().__init__()
        uic.loadUi("Project Qt_rasp.ui", self)
        self.label.setText(f'Расписание на {date}')
        self.pushButton.clicked.connect(self.calen_op)
        con = sqlite3.connect('project.db')
        self.setWindowIcon(QIcon('Photo_ocn_ocn.ico'))
        with con:
            self.cur = con.cursor()
            result = self.cur.execute("""SELECT Name, Specialty, Change FROM dspec WHERE Date1=?""", [date]).fetchall()
            self.tableWidget.setRowCount(len(result))
            if not result:
                pal = self.label.palette()
                pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
                self.label.setPalette(pal)
                self.label.setText('Ничего не нашлось')
                return
            else:
                self.tableWidget.setColumnCount(len(result[0]))
                self.titles = ['Name', 'Specialty', 'Change']
                self.tableWidget.setHorizontalHeaderLabels(self.titles)
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            self.modified = {}

    def calen_op(self):
        self.close()
        self.calen = Calendr()
        self.calen.show()


class Calendr(QMainWindow):
    """Выбор даты для расписания"""
    def __init__(self):
        super().__init__()
        uic.loadUi("Project Qt_raspcalen.ui", self)
        self.setWindowIcon(QIcon('Photo_ocn_ocn.ico'))
        self.pushButton.clicked.connect(self.select_date)
        self.alldate = ''

    def select_date(self):
        self.close()
        date = self.calendarWidget.selectedDate()
        alldate = date.toString('dd.MM.yyyy')
        self.sch = Schedule(alldate)
        self.sch.show()


class Record(QMainWindow):
    def __init__(self, hash1):
        """Выбор Специализации врача"""
        super().__init__()
        self.hash = hash1
        self.setWindowFlags(QtCore.Qt.Window | Qt.WindowStaysOnTopHint)
        con = sqlite3.connect('project.db')
        self.setWindowIcon(QIcon('Photo_ocn_ocn.ico'))
        with con:
            cur = con.cursor()
            result = cur.execute('''SELECT * FROM Spesial''').fetchall()
        uic.loadUi("Project Qt_12.ui", self)
        self.setWindowTitle('Выберите специальность')
        self.setGeometry(650, 300, 841, 606)
        self.setFixedSize(841, 700)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Отделение"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.back)

        for x in range(len(result)):
            self.button = QPushButton(str(result[x][0]), self)
            self.tableWidget.setCellWidget(x, 0, self.button)
            self.button.clicked.connect(lambda state, numButton=result[x][0]: self.button_pushed(numButton))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.modified = {}

    def back(self):
        self.f = Necessary_Action()
        self.f.show()
        self.close()

    def button_pushed(self, numButton):
        self.hide()
        self.s = Second(numButton, self.hash)
        self.s.show()


class Second(QMainWindow):
    def __init__(self, numButton, hash1):
        """Выбор фамилии врача"""
        QMainWindow.__init__(self)
        n = []
        self.numButton = numButton
        self.hash = hash1
        uic.loadUi("Project Qt_doct.ui", self)
        self.setWindowIcon(QIcon('Photo_ocn_ocn.ico'))
        self.setWindowFlags(Qt.FramelessWindowHint)
        n.append(numButton)
        self.setWindowTitle('Выберите фамилию')
        con = sqlite3.connect('project.db')
        self.setGeometry(500, 300, 500, 500)
        with con:
            cur = con.cursor()
            result = cur.execute('''SELECT Name FROM infDoctors
                                                   WHERE Specialty = ?''', n).fetchall()
        self.setWindowFlags(QtCore.Qt.Window | Qt.WindowStaysOnTopHint)
        self.setGeometry(650, 300, 500, 500)
        self.setFixedSize(796, 500)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Фамилия"])
        self.pushButton.clicked.connect(self.back)

        for x in range(len(result)):
            self.button = QPushButton(str(result[x][0]), self)
            self.tableWidget.setCellWidget(x, 0, self.button)
            self.button.clicked.connect(lambda state, numButton=result[x][0]: self.button_pushed(numButton))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def button_pushed(self, numButton):
        self.hide()
        self.s = Third(numButton, self.numButton, self.hash)
        self.s.show()

    def back(self):
        self.firs = Record(self.hash)
        self.firs.show()
        self.hide()


class Third(QMainWindow):
    def __init__(self, doc, spec, hash1):
        super().__init__()
        self.hash = hash1
        self.name_doctor = doc
        self.setWindowTitle('Талон')
        self.specialty_doctor = spec
        uic.loadUi("Ui_tablecalen.ui", self)
        self.setWindowIcon(QIcon('Photo_ocn_ocn.ico'))
        self.setWindowFlags(QtCore.Qt.Window | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(650, 300, 500, 500)
        self.setFixedSize(800, 500)
        self.calendarWidget.clicked.connect(self.data_process_db)
        self.pushButton.clicked.connect(self.back)

    def data_process_db(self):
        """Выдача талонов по дате, выбранной специализации и имени врача"""
        self.n = ''
        date = self.calendarWidget.selectedDate()
        s_date = date.toPyDate()
        self.alldate = date.toString('dd.MM.yyyy')
        now = datetime.datetime.now()
        now_date = now.strftime("%d.%m.%Y")
        if now.date() < s_date:
            self.con = sqlite3.connect('project.db')
            with self.con:
                cur = self.con.cursor()
                result = cur.execute("""SELECT * FROM dspec
        WHERE Date1 = ? and Specialty = ? and Name = ? and Change != ''""",
                                     (self.alldate, self.specialty_doctor, self.name_doctor)).fetchall()
            self.doctorid = cur.execute('''SELECT id FROM infDoctors
            WHERE Name = ?''', [self.name_doctor]).fetchall()[0][0]
            for i in result:
                self.n = i[3].split(', ')
            self.data_visualizatoin()
        else:
            print(1)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)

    def data_visualizatoin(self):
        """Добавление кнопок в Tablewidget"""
        self.tableWidget.setRowCount(len(self.n))
        self.tableWidget.setColumnCount(1)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        for x in range(len(self.n)):
            self.button = QPushButton(str(self.n[x]), self)
            self.tableWidget.setCellWidget(x, 0, self.button)
            self.button.clicked.connect(lambda state, numButton=self.n[x]: self.button_pushed(numButton))
        self.tableWidget.setHorizontalHeaderLabels([""])

    def back(self):
        self.firs = Record(self.hash)
        self.firs.show()
        self.hide()

    def button_pushed(self, time):
        """Группировка данных, которые необходимо закодировать в qr-код и добавления талона пользователю"""
        valid = QMessageBox.question(
            self, '', f'''Взять талон:
Специальность: {self.specialty_doctor}
Фамилия: {self.name_doctor}
Время: {time}?''',
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            del self.n[self.n.index(time)]
            cur = self.con.cursor()
            cur.execute('''UPDATE Schedule
SET Change = ?
WHERE Doctor = ? and Date = ?''', (', '.join(self.n), self.doctorid, self.alldate))
            cur.execute(''' INSERT INTO Cpns VALUES(?, ?, ?, ?, ?)''',
                        (self.hash, self.doctorid, self.alldate, time, '-'))
            self.con.commit()
            text = f"""{self.hash}
{transliterate.translit(self.name_doctor, reversed=True)}
{transliterate.translit(self.specialty_doctor, reversed=True)}
{self.alldate}
{time}"""
            img = qrcode.make(text)
            io_data = io.BytesIO()
            img.save(io_data, 'png')
            img.save('qr_code_1.png')
            self.qr = Qrcode()
            self.qr.show()
            self.close()


class Qrcode(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        """Создание qr-кода, и его вывод"""
        hbox = QtWidgets.QVBoxLayout()
        self.setWindowFlags(Qt.FramelessWindowHint)
        pixmap = QPixmap('qr_code_1.png')
        self.setWindowIcon(QIcon('Photo_ocn_ocn.ico'))
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        hbox.addWidget(lbl)
        self.move(600, 300)
        self.setWindowTitle('Qr')
        self.time_left_int = 30
        self.widget_counter_int = 0
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(hbox)
        self.time_passed_qll = QtWidgets.QLabel()
        self.pages_qsw = QtWidgets.QStackedWidget()
        hbox.addWidget(self.pages_qsw)
        hbox.addWidget(self.time_passed_qll)
        self.timer_start()
        self.update_gui()

    def timer_start(self):
        self.time_left_int = 30
        self.my_qtimer = QtCore.QTimer(self)
        self.my_qtimer.timeout.connect(self.timer_timeout)
        self.my_qtimer.start(1000)
        self.update_gui()

    def timer_timeout(self):
        self.time_left_int -= 1
        if self.time_left_int == 0:
            self.back = Necessary_Action()
            self.back.show()
            self.close()
        self.update_gui()

    def update_gui(self):
        self.time_passed_qll.setText(f'Окно закроется через {str(self.time_left_int)}')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Necessary_Action()
    w.show()
    sys.exit(app.exec_())
