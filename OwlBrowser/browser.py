import os
import json
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class BookmarkManager:
    def __init__(self, filename="bookmarks.json"):
        self.filename = filename
        self.load_bookmarks()

    def load_bookmarks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.bookmarks = json.load(f)
        else:
            self.bookmarks = []

    def save_bookmarks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.bookmarks, f)

    def add_bookmark(self, title, url):
        self.bookmarks.append({'title': title, 'url': url})
        self.save_bookmarks()

    def get_bookmarks(self):
        return self.bookmarks

class MyWebBrowser(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWebBrowser, self).__init__()
        self.showMaximized()

        self.setWindowTitle("Owl Browser")
        self.setWindowIcon(QtGui.QIcon("owl_icon.png"))  # Set the window icon
        self.bookmark_manager = BookmarkManager()

        # Layouts
        self.layout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()

        # URL Bar
        self.urlbar = QLineEdit()
        self.urlbar.setMaximumHeight(30)

        # Navigation Buttons
        self.go_btn = QPushButton("Go")
        self.back_btn = QPushButton("Back")
        self.forward_btn = QPushButton("Forward")
        self.reload_btn = QPushButton("Reload")
        self.stop_btn = QPushButton("Stop")
        self.home_btn = QPushButton("Home")
        self.bookmark_btn = QPushButton("Bookmark")

        # Browser
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://google.com"))

        # Add widgets to the horizontal layout
        self.horizontalLayout.addWidget(self.urlbar)
        self.horizontalLayout.addWidget(self.go_btn)
        self.horizontalLayout.addWidget(self.back_btn)
        self.horizontalLayout.addWidget(self.forward_btn)
        self.horizontalLayout.addWidget(self.reload_btn)
        self.horizontalLayout.addWidget(self.stop_btn)
        self.horizontalLayout.addWidget(self.home_btn)
        self.horizontalLayout.addWidget(self.bookmark_btn)

        # Add layouts to main layout
        self.layout.addLayout(self.horizontalLayout)
        self.layout.addWidget(self.browser)

        # Set the layout in the main window
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Connect buttons to methods
        self.go_btn.clicked.connect(self.navigate)
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)
        self.reload_btn.clicked.connect(self.browser.reload)
        self.stop_btn.clicked.connect(self.browser.stop)
        self.home_btn.clicked.connect(self.go_home)
        self.bookmark_btn.clicked.connect(self.add_bookmark)

        # Connect signals
        self.browser.urlChanged.connect(self.update_urlbar)

    def navigate(self):
        url = self.urlbar.text()
        if not url.startswith('http'):
            url = 'http://' + url
            self.urlbar.setText(url)
        self.browser.setUrl(QUrl(url))

    def go_home(self):
        self.browser.setUrl(QUrl("http://google.com"))

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())

    def add_bookmark(self):
        title = self.browser.title()
        url = self.browser.url().toString()
        self.bookmark_manager.add_bookmark(title, url)
        QMessageBox.information(self, "Bookmark Added", f"'{title}' has been added to bookmarks.")

app = QApplication([])
window = MyWebBrowser()
window.show()
app.exec_()
