import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QMessageBox, QInputDialog,
    QDateEdit, QHBoxLayout, QWidget, QListWidgetItem, QComboBox
)
from PyQt5.QtCore import QDate


class ToDoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('To Do App')
        self.setGeometry(300, 300, 400, 500)

        # Central Widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Button Layout
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        # Task Input
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("write A new task")
        self.layout.addWidget(self.task_input)

        # Date Input
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.layout.addWidget(QLabel('Due Date:'))
        self.layout.addWidget(self.date_input)

        # Priority
        self.priority_combo = QComboBox(self)
        self.priority_combo.addItems(["High", "Medium", "Low"])
        self.layout.addWidget(QLabel('Priority:'))
        self.layout.addWidget(self.priority_combo)

        # Add new task button
        self.addTaskButton = QPushButton("Add Task")
        self.addTaskButton.clicked.connect(self.addTask)
        self.button_layout.addWidget(self.addTaskButton)

        # Task list
        self.task_list = QListWidget(self)
        self.layout.addWidget(self.task_list)

        # Mark As Done Button
        self.markasdonebutton = QPushButton("Mark as Done")
        self.markasdonebutton.clicked.connect(self.markAsDone)
        self.button_layout.addWidget(self.markasdonebutton)

        # Mark As Undone Button
        self.undonbutton = QPushButton("Mark as Undone")
        self.undonbutton.clicked.connect(self.markAsUnDone)
        self.button_layout.addWidget(self.undonbutton)

        # Remove task Button
        self.removeTaskButton = QPushButton("Remove Task")
        self.removeTaskButton.clicked.connect(self.removeTask)
        self.button_layout.addWidget(self.removeTaskButton)

        # Edit task Button
        self.editTaskButton = QPushButton("Edit Task")
        self.editTaskButton.clicked.connect(self.editTask)
        self.layout.addWidget(self.editTaskButton)

        self.loadtasks()

    def addTask(self):
        task = self.task_input.text()
        due_date = self.date_input.date().toString("yyyy-MM-dd")
        priority = self.priority_combo.currentText()
        if task:
            task_with_date = f"{task}     Due: {due_date},    Priority: {priority}"
            self.task_list.addItem(task_with_date)
            self.task_input.clear()
            self.savetasks()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a task")

    def markAsDone(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            for item in selected_items:
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
            self.savetasks()
        else:
            QMessageBox.warning(self, "Warning", "Please select a task")

    def markAsUnDone(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            for item in selected_items:
                font = item.font()
                font.setStrikeOut(False)
                item.setFont(font)
            self.savetasks()
        else:
            QMessageBox.warning(self, "Warning", "Please select a task")

    def removeTask(self):
        selected_items = self.task_list.selectedItems()
        if selected_items:
            for item in selected_items:
                self.task_list.takeItem(self.task_list.row(item))
            self.savetasks()
        else:
            QMessageBox.warning(self, "Warning", "Please select a task")

    def savetasks(self):
        tasks = []
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            task_data = {
                "text": item.text(),
                "strikethrough": item.font().strikeOut(),
            }
            tasks.append(task_data)

        with open('tasks.json', 'w') as file:
            json.dump(tasks, file)

    def loadtasks(self):
        if os.path.exists("tasks.json"):
            with open('tasks.json', 'r') as file:
                tasks = json.load(file)
                for task in tasks:
                    item = QListWidgetItem(task["text"])
                    font = item.font()
                    font.setStrikeOut(task["strikethrough"])
                    item.setFont(font)
                    self.task_list.addItem(item)

    def editTask(self):
        selected_item = self.task_list.selectedItems()
        if selected_item:
            for item in selected_item:
                self.task_list.editItem(item)
        else:
            QMessageBox.warning(self, "Warning", "Please select a task")


def stylesheet(app):
    app.setStyleSheet("""
        QWidget {
            background-color: #E3F2FD;
            color: #0D47A1;
        }
        QPushButton {
            background-color: #009688;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #00796B;
        }
        QListWidget {
            background-color: white;
            color: #0D47A1;
            border: 1px solid #BBDEFB;
            border-radius: 4px;
        }
        QLineEdit {
            background-color: white;
            color: #0D47A1;
            border: 1px solid #BBDEFB;
            border-radius: 4px;
            padding: 5px;
        }
        QDateEdit {
            background-color: white;
            color: #0D47A1;
            border: 1px solid #BBDEFB;
            border-radius: 4px;
            padding: 5px;
        }
        QComboBox{
            background-color: white;
            color: #0D47A1;
            border: 1px solid #BBDEFB;
            border-radius: 4px;
            padding: 5px;
        }
    """)


def main():
    app = QApplication(sys.argv)
    stylesheet(app)
    to_do_app = ToDoApp()
    to_do_app.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
