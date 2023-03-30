import sys
import os.path
import csv
from datetime import datetime, timedelta
from PyQt6.QtCore import Qt, QTimer, QDateTime
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QTreeView, QWidget, QMessageBox, QDialog, QSystemTrayIcon
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon


class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Tracker App")
        self.setFixedSize(600, 600)
        self.setStyleSheet("QMainWindow { background-color: #D3D3D3; }")

        # Task times dictionary
        self.task_times = {}

        # Widgets
        self.task_entry = QLineEdit(self)
        self.task_entry.setPlaceholderText("Enter Task Name")
        self.task_details_entry = QTextEdit(self)
        self.task_details_entry.setPlaceholderText("Enter Task Details")

        self.add_task_button = QPushButton("Add Task", self)
        self.add_task_button.clicked.connect(self.add_task)

        # Treeview for tasks
        self.todo_treeview = QTreeView(self)
        self.todo_treeview.setModel(self.create_treeview_model())

        # Buttons
        self.complete_task_button = QPushButton("Complete Task", self)
        self.complete_task_button.clicked.connect(self.complete_task)

        self.delete_task_button = QPushButton("Delete Task", self)
        self.delete_task_button.clicked.connect(self.delete_task)

        self.edit_task_button = QPushButton("Edit Task", self)
        self.edit_task_button.clicked.connect(self.edit_task)

        # Layouts
        main_layout = QVBoxLayout()
        top_layout = QGridLayout()
        button_layout = QHBoxLayout()

        top_layout.addWidget(QLabel("Enter Task Name:"), 0, 0)
        top_layout.addWidget(self.task_entry, 0, 1)
        top_layout.addWidget(self.add_task_button, 0, 2)
        top_layout.addWidget(QLabel("Task Details:"), 1, 0)
        top_layout.addWidget(self.task_details_entry, 1, 1, 1, 2)

        button_layout.addWidget(self.complete_task_button)
        button_layout.addWidget(self.delete_task_button)
        button_layout.addWidget(self.edit_task_button)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.todo_treeview)
        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.initialize_completed_tasks_csv()
        self.load_tasks_from_file()

        # Add the timer to check for overdue tasks
        self.check_overdue_tasks_timer = QTimer()
        self.check_overdue_tasks_timer.timeout.connect(self.check_overdue_tasks)
        self.check_overdue_tasks_timer.start(60 * 60 * 1000)  # Check every 1 hour

    def create_treeview_model(self):
        self.treeview_model = QStandardItemModel()
        self.treeview_model.setHorizontalHeaderLabels(['Task', 'Details'])
        self.todo_treeview.header().setStretchLastSection(True)
        self.todo_treeview.setModel(self.treeview_model)
        return self.treeview_model  # Add this line

    def add_treeview_item(self, task, details):
        model = self.todo_treeview.model()
        item_task = QStandardItem(task)
        item_details = QStandardItem(details)
        model.appendRow([item_task, item_details])

    def initialize_completed_tasks_csv(self):
        if not os.path.exists('completed_tasks.csv'):
            with open('completed_tasks.csv', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Task', 'Details', 'Date Completed'])

    def add_task_to_view(self, task, details):
        item = QStandardItem(f"{task}: {details}")
        self.treeview_model.appendRow(item)

    def load_tasks_from_file(self):
        if os.path.exists("tasks.csv"):
            with open("tasks.csv", "r") as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip the header row
                for row in csv_reader:
                    task, details, timestamp = row
                    self.add_treeview_item(task, details)  # Change this line
                    self.task_times[task] = datetime.fromisoformat(timestamp)

    def check_overdue_tasks(self):
        now = datetime.now()
        for task, created_at in self.task_times.items():
            delta = now - created_at
            if delta > timedelta(hours=24):
                QMessageBox.warning(self, "Task Reminder",
                                    f"The task '{task}' has not been completed, edited, or deleted in the last 24 hours.")
                break

    def save_tasks_to_file(self):
        with open("tasks.csv", "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Task", "Details", "Timestamp"])
            for i in range(self.todo_treeview.model().rowCount()):
                task = self.todo_treeview.model().item(i, 0).text()
                details = self.todo_treeview.model().item(i, 1).text()
                timestamp = self.task_times[task].isoformat()
                csv_writer.writerow([task, details, timestamp])

    def add_task(self):
        task = self.task_entry.text().strip()
        details = self.task_details_entry.toPlainText().strip()
        if task:
            self.add_treeview_item(task, details)
            self.task_times[task] = datetime.now()
            self.save_tasks_to_file()
            self.task_entry.clear()
            self.task_details_entry.clear()

    def delete_task(self):
        selected_item = self.todo_treeview.selectedIndexes()
        if selected_item:
            row = selected_item[0].row()
            task = self.todo_treeview.model().item(row, 0).text()
            del self.task_times[task]
            self.todo_treeview.model().removeRow(row)
            self.save_tasks_to_file()

    def complete_task(self):
        selected_item = self.todo_treeview.selectedIndexes()
        if selected_item:
            row = selected_item[0].row()
            task = self.todo_treeview.model().item(row, 0).text()
            details = self.todo_treeview.model().item(row, 1).text()
            completion_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open("completed_tasks.csv", "a", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([task, details, completion_date])

            del self.task_times[task]
            self.todo_treeview.model().removeRow(row)
            self.save_tasks_to_file()

    def edit_task(self):
        selected_item = self.todo_treeview.selectedIndexes()
        if selected_item:
            row = selected_item[0].row()
            old_task = self.todo_treeview.model().item(row, 0).text()
            old_details = self.todo_treeview.model().item(row, 1).text()

            edit_window = QDialog(self)
            edit_window.setWindowTitle("Edit Task")
            edit_window.setFixedSize(400, 200)

            layout = QVBoxLayout(edit_window)

            edit_task_entry = QLineEdit(edit_window)
            edit_task_entry.setText(old_task)
            layout.addWidget(edit_task_entry)

            edit_details_entry = QTextEdit(edit_window)
            edit_details_entry.setPlainText(old_details)
            layout.addWidget(edit_details_entry)

            def save_edited_task():
                new_task = edit_task_entry.text().strip()
                new_details = edit_details_entry.toPlainText().strip()
                if new_task:
                    self.todo_treeview.model().item(row, 0).setText(new_task)
                    self.todo_treeview.model().item(row, 1).setText(new_details)
                    del self.task_times[old_task]
                    self.task_times[new_task] = datetime.now()
                    self.save_tasks_to_file()
                edit_window.accept()

            save_button = QPushButton("Save", edit_window)
            save_button.clicked.connect(save_edited_task)
            layout.addWidget(save_button)

            edit_window.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_icon = QIcon('icons8-check-64.png')
    app.setWindowIcon(app_icon)
    tray_icon = QSystemTrayIcon(app_icon, app)
    tray_icon.show()
    window = TodoApp()
    window.show()
    sys.exit(app.exec())
