import sys
import os
import time

from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QSizePolicy

from PyQt5.QtGui import QIcon

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QDir, QEvent, QTimer, Qt

import core.utilities as utils


class Tree(QTreeView):
	def __init__(self):
		QTreeView.__init__(self)
		model = QFileSystemModel()
		model.setRootPath(QDir.homePath())

		self.setModel(model)
		self.setRootIndex(model.index(QDir.homePath()))
		model.setReadOnly(False)

		for i in range(1, model.columnCount()):
			self.hideColumn(i)
		self.setHeaderHidden(True)	
		
		self.setSelectionMode(self.SingleSelection)
		self.setDragDropMode(QAbstractItemView.InternalMove)
		self.setDragEnabled(True)
		self.setAcceptDrops(True)
		self.setDropIndicatorShown(True)

	def dragEnterEvent(self, event):
		m = event.mimeData()
		if m.hasUrls():
			for url in m.urls():
				if url.isLocalFile():
					event.accept()
					return
		event.ignore()

	def dropEvent(self, event):
		if event.source():
			QTreeView.dropEvent(self, event)
		else:
			ix = self.indexAt(event.pos())
			if not self.model().isDir(ix):
				ix = ix.parent()
			pathDir = self.model().filePath(ix)
			m = event.mimeData()
			if m.hasUrls():
				urlLocals = [url for url in m.urls() if url.isLocalFile()]
				accepted = False
				for urlLocal in urlLocals:
					path = urlLocal.toLocalFile()
					info = QFileInfo(path)
					n_path = QDir(pathDir).filePath(info.fileName())
					o_path = info.absoluteFilePath()
					if n_path == o_path:
						continue
					if info.isDir():
						QDir().rename(o_path, n_path)
					else:
						qfile = QFile(o_path)
						if QFile(n_path).exists():
							n_path += "(copy)"
						qfile.rename(n_path)
					accepted = True
				if accepted:
					event.acceptProposedAction()


class FormDialog(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Python")
		self.setGeometry(100, 100, 500, 200)
		self.form = QFormLayout()
		self.email = QLineEdit()
		self.form.addRow('Email:', self.email)
		self.password = QLineEdit()
		self.password.setEchoMode(QLineEdit.Password)
		self.form.addRow('Password:', self.password)
		self.formWidget = QWidget()
		self.formWidget.setLayout(self.form)
		self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.buttonBox.accepted.connect(self.getInfo)
		self.buttonBox.rejected.connect(self.reject)
		self.val = ''
		mainLayout = QVBoxLayout()
		mainLayout.addWidget(self.formWidget)
		mainLayout.addWidget(self.buttonBox)
		self.setLayout(mainLayout)
		self.exec_()

	def getInfo(self):
		self.val = 'success'
		self.close()


class FileDialog(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 file dialogs - pythonspot.com'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
	
	def openFileNameDialog(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "",
				"All Files (*);;Python Files(*.py)", options = options)
		if fileName:
			return fileName

	def openFileNamesDialog(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		files, _ = QFileDialog.getOpenFileNames(self, "Open Files", "",
				"All Files (*);;Python Files(*.py)", options = options)
		if files:
			return files

	def saveFileDialog(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "",
				"All Files (*);;Python Files(*.py)", options = options)
		if fileName:
			return fileName
	
class List(QListWidget):
	itemDropped = pyqtSignal()
	def __init__(self, parent = None):
		super().__init__(parent)
		QListWidgetItem("Test Item", self)
		self.setAcceptDrops(True)
		self.setDragEnabled(True)
		self.setSelectionMode(self.ExtendedSelection)
		self.droppedUrls = []

	def _addEntry(self, item, icon=None):
		listWidgetItem = QListWidgetItem(item)
		if icon:
			listWidgetItem.setIcon(icon)
		self.addItem(listWidgetItem)


	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()
	

	def dragMoveEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()


	def dropEvent(self, event):
		if event.mimeData().hasUrls():
			for url in event.mimeData().urls():
				self.droppedUrls.append(str(url.toLocalFile()))
		self.itemDropped.emit()

				
class Window(QMainWindow):
	def __init__(self, CentralWidget, parent=None):
		super().__init__(parent)
		self.setCentralWidget(CentralWidget)
		self._createMenu()
		self._createToolBar()
		self._createStatusBar()

	def _createMenu(self):
		self.menu = self.menuBar().addMenu("&Menu")
		self.menu.addAction('&Exit', self.close)

	def _createToolBar(self):
		self.tools = QToolBar()
		self.addToolBar(self.tools)
		#self.tools.addAction('Exit', self.close)

	def _createStatusBar(self):
		self.status = QStatusBar()
		self.status.showMessage("I'm the Status Bar")
		self.setStatusBar(self.status)

	def notify(self, message, timeout = 0):
		print("Notification: " + message)
		self.status.showMessage(message, timeout)
	
class AppWindow(Window):
	def __init__(self, parent=None):
		self.currEmail = ''
		self.loggedIn = False

		self.fileList = List()
		self.file_icon = QIcon(QApplication.style().standardIcon(QStyle.SP_FileIcon))

		### This is how new entries are added:
		self.fileList._addEntry("Additional list entry", self.file_icon)

		self.mainWidget = QWidget()
		self.splitter = QSplitter()
		self.splitter.addWidget(self.fileList)

		self.treeView = Tree()
		self.treeView.hide()
		self.splitter.insertWidget(0, self.treeView)
		self.treeInserted = False
		self.splitter.setStretchFactor(0, 10)
		self.splitter.setStretchFactor(1, 25)

		super().__init__(self.splitter)
		self.setWindowTitle('Main App Window')
		self.setGeometry(100, 100, 800, 500)

		self.selectedItems = []

		self.tools.addAction('Download', self.downloadAction)
		self.tools.addAction('Upload', self.uploadAction)
		self.tools.addAction('Login', self.loginAction)
		self.tools.addAction('Tree View', self.treeviewAction)

		self.fileList.itemSelectionChanged.connect(self.selectionChanged)
		self.fileList.itemDropped.connect(self.dropHandle)


	def showEvent(self, event):
		QTimer.singleShot(50, self.functionAfterShown)

	def functionAfterShown(self):
		self.notify("Attempting automatic login...")
		#time.sleep(5)
		res, email = utils.try_easy_login()
		if res:
			self.notify("Successfully logged in")
			self.currEmail = email
			self.loggedIn = True
			self.updateFileList()
		else:
			self.notify("Automatic login unsuccessful")

	def selectionChanged(self):
		self.selectedItems = self.fileList.selectedItems()

	def treeviewAction(self):
		if not self.treeInserted:
			self.treeView.show()
			self.treeInserted = True

		else:
			self.treeView.hide()
			self.treeInserted = False
		
	def loginAction(self):
		if self.loggedIn:
			self.notify("Already logged in")
			return

		formdiag = FormDialog()
		if formdiag.val == 'success':
			self.notify("Attempting to log in...")
			res = utils.login(formdiag.email.text(), formdiag.password.text())
			if res:
				self.notify("Login successful")
				self.currEmail = formdiag.email.text()
			else:
				self.notify("Login unsuccessful")

	def downloadAction(self):
		if self.selectedItems:
			for selectedItem in self.selectedItems:
				selectedFile = selectedItem.text()
				self.notify("Downloading: " + selectedFile)
				if not utils.send_file(selectedFile, self.currEmail):
					self.notify("Failed to download file: " + selectedFile)
					continue
			self.notify("Download completed", 10000)

	def uploadAction(self):
		mydiag = FileDialog()
		if mydiag:
			filesToUpload = mydiag.openFileNamesDialog()
			self.uploadFileList(filesToUpload)

	def dropHandle(self):
		if self.fileList.droppedUrls:
			self.uploadFileList(self.fileList.droppedUrls)
			self.fileList.droppedUrls = []

	def uploadFileList(self, fileList):
		for fileToUpload in fileList:
			self.notify("Uploading: " + fileToUpload)
			if not utils.send_file(fileToUpload, self.currEmail):
				self.notify("Failed to upload file: " + fileToUpload)
				continue
		self.notify("Upload completed", 10000)
		self.updateFileList()

	def updateFileList(self):
		self.notify("Updating file list...")
		fileList = utils.list_available()
		for singleFile in fileList:
			if not self.fileList.findItems(singleFile, Qt.MatchExactly):
				self.fileList._addEntry(singleFile, self.file_icon)
		self.notify("File list updated", 10000)
		

					


#if __name__ == '__main__':
#	app = QApplication(sys.argv)
#
#	win = AppWindow()
#	win.show()
#
#	sys.exit(app.exec_())

def run():
	app = QApplication(sys.argv)

	win = AppWindow()
	win.show()

	sys.exit(app.exec_())

