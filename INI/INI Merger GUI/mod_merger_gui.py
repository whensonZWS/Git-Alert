import sys
from PyQt5.QtWidgets import QMenu, QSplitter, QLabel, QTreeWidget, QLineEdit, QListWidget, QAction, QStatusBar, QHBoxLayout, QFileDialog, QPushButton, QMessageBox, QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QListView, QTableView, QAbstractItemView
from PyQt5.QtCore import QDir,Qt

class DropListWidget(QListWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		self.setAcceptDrops(True)
		
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.setDragEnabled(True)
		self.setDropIndicatorShown(True)
		self.setDragDropMode(QAbstractItemView.InternalMove)
		self.setDefaultDropAction(Qt.MoveAction)
		self.viewport().setAcceptDrops(True)
		self.files = []
		
	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			pass
			#event.ignore()
			
	def dragMoveEvent(self, event):
		if event.mimeData().hasUrls():
			event.setDropAction(Qt.CopyAction)
			event.accept()
		else:
			pass
			#event.ignore()
			
			
	def dropEvent(self, event):
		if event.mimeData().hasUrls():
			event.setDropAction(Qt.CopyAction)
			event.accept()
			for url in event.mimeData().urls():
				if url.isLocalFile():
					temp = url.toLocalFile()
					if temp.endswith('.ini') or temp.endswith('.txt') or temp.endswith('.map'):
						if temp not in self.files:
							self.addItems([temp])
							self.files.append(temp)
		
		
		else:
			pass
			#event.ignore()
			
	# def mousePressEvent(self,event):
		# if event.button() == Qt.LeftButton:
			# self.dragStartPosition = event.pos()
			
	# def mouseMoveEvent(self,event):
		# if not (event.buttons() & Qt.LeftButton):
			# return
		# if (event.pos() - self.dragStartPosition).manhattanLength() < QApplication.startDragDistance() :
			# return
		
		# print('drag')
		# #drag = QDrag(self)
		# #mimeData = QmimeData()
		
		# #mimeData.setData()
		# #drag.setMimeData(mimeData)
	
		

class App(QWidget):
	
	def __init__(self):
		super().__init__()
		self.title = 'Whenson\'s Custom INI Merger'
		self.geo = (200,200,800,600)
		self.initGUI()
		
		
	def initGUI(self):
		# windows title and geometry
		self.setGeometry(*(self.geo))
		self.setWindowTitle(self.title)
		self.show()
		
		# master layout and widget definition
		self.layout = QHBoxLayout()
		
		self.file_box = QVBoxLayout()
		
		self.list_box = QVBoxLayout()
		self.btn_group = QVBoxLayout()

		# deploy layout
		self.setLayout(self.layout)
		self.layout.addLayout(self.file_box)
		
		

		self.layout.addLayout(self.list_box)
		self.layout.addLayout(self.btn_group)
		
		# file box
		self.file_box.addWidget(QLabel('File Browser'))
		self.folder_tree = QTreeView()
		self.file_box.addWidget(self.folder_tree)
		self.file_list = QTreeView()
		self.file_box.addWidget(self.file_list)
		

		# list box
		
		self.normal_list = DropListWidget()
		self.demo_list = DropListWidget()
		
		self.list_box.addWidget(QLabel('Output File'))
		self.list_box.addWidget(QLineEdit())
		
		self.list_box.addWidget(QLabel('Module List'))
		self.list_box.addWidget(self.normal_list)
		
		temp = QHBoxLayout()
		self.up_btn = QPushButton()
		self.up_btn.setText('ᐱ')
		self.down_btn = QPushButton()
		self.down_btn.setText('ᐯ')
		self.list_box.addLayout(temp)
		temp.addWidget(self.up_btn)
		temp.addWidget(self.down_btn)
		
		self.list_box.addWidget(QLabel('With Demostration'))
		self.list_box.addWidget(self.demo_list)
		
		
		# button group 
		self.merge_btn = QPushButton('Merge')
		self.btn_group.addWidget(self.merge_btn)
		
		self.load_btn = QPushButton('Load')
		self.btn_group.addWidget(self.load_btn)
		
		self.init_file_tree()
		self.init_drag()
		
	def init_file_tree(self):
		self.dir_model = QFileSystemModel()
		self.dir_model.setRootPath('C:/')
		self.dir_model.setFilter(QDir.AllDirs|QDir.NoDotAndDotDot)
		self.folder_tree.setModel(self.dir_model)
		self.folder_tree.hideColumn(1)
		self.folder_tree.hideColumn(2)
		self.folder_tree.hideColumn(3)
		
		
		self.file_model = QFileSystemModel()
		self.file_model.setFilter(QDir.NoDotAndDotDot|QDir.Files)
		self.file_list.setModel(self.file_model)
		self.file_list.setRootIndex(self.file_model.setRootPath('C:/'))
		self.file_model.setNameFilters(['*.txt','*.ini','*.map'])
		self.file_model.setNameFilterDisables(False)
		self.folder_tree.clicked.connect(self.tree_on_clicked)
		self.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
		
	def init_drag(self):
		self.file_list.setDragEnabled(True)
		self.file_list.setDropIndicatorShown(True)
		# self.file_list.setDefaultDropAction(Qt.MoveAction)
		
		
	def tree_on_clicked(self,index):
		path = self.dir_model.fileInfo(index).absoluteFilePath()
		self.file_list.setRootIndex(self.file_model.setRootPath(path))
	

		
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	
	mm = App()
	
	sys.exit(app.exec_())