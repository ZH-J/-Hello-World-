#comic index
'''增加目录文件'''


import os
import sys
from PyQt5.QtWidgets import (QWidget,QHBoxLayout,QVBoxLayout,QLabel,
	  QPushButton,QGridLayout,QLayout,QMessageBox, QLineEdit,QFileDialog,
	  QApplication)
from PyQt5.QtGui import QPixmap


class myLabel(QLabel):
	"""docstring for myLabel"""
	def __init__(self, pic_path=''):
		super().__init__(pic_path)
		self.pic = pic_path
		
	def mousePressEvent(self,e):
		#print('OK, I know the'+self.pic+' was pressed')
		os.startfile(self.pic)
		

class w_comic(QWidget):
	"""docstring for Example"""
	def __init__(self):
		super().__init__()
		#self.fold_path = fold_path
		self.page = 0
		self.cover_path = []
		#QApplication.processEvents()
		self.Openfile(0)
		self.initUI()
		#print(self.cover_path[0])

	def get_path(self, path):
		os.chdir(path)
		
		if os.path.isfile('./comic_index.txt'):
			with open('comic_index.txt','r',encoding='utf-8') as index:
				criterion = index.readline()
				#print(type(criterion))
				fact ='#'+path
				#print(type(fact))
				if fact in criterion:
					#print('!!!')
					for i in index.readlines():
						k = i.strip('\n')
						self.cover_path.append(k)
					#del self.cover_path[0]
		else:
			self.cover_path = []
			with open('comic_index.txt','w',encoding='utf-8') as index:
			#print('???')
				file_cover = []
				pa = os.walk(path)
				for dirpath, dirnames, filenames in pa:
					if dirnames == []:
						if filenames:
							filenames.sort(key=lambda x:x[:-4])
							for name in filenames:
								if name[-3:] in ('jpg','png'):
									file_cover.append(dirpath + os.sep + name)
									break
				index.write('#'+path+'\n')
				for i in file_cover:
					self.cover_path.append(i)
					index.write(i+'\n')	

	def brush(self):
		self.page_text = str(self.page + 1) + '页/' + str(len(self.cover_path)//10) + '页'
		self.label_page.setText('%s' %self.page_text)
		
		
	def Openfile(self, key):
		self.cover_path = []
		self.page = 0
		#fname, ftype = QFileDialog.getOpenFileName(self,'选择文件','./')
		index_path = QFileDialog.getExistingDirectory(self,'选择文件夹')
		path = index_path.replace('/','\\')
		#print(index_path)
		#sys.exit()
		self.get_path(path)
		if key == 1:
			self.Next()
		#self.brush()
		#print(self.cover_path[:10])
		#

		#print(fname)
		#sys.exit()
	

	def Previous(self):
		if self.page <= 0:
			QMessageBox.information(self, 'Message',"第一页了！", 
			QMessageBox.Yes | QMessageBox.No)
		else:
			self.page -=1

			num = self.page
			list_of_pix=self.cover_path[num*10:num*10+10]

			positions = [(i,j) for i in range(2) for j in range(5)]
			for position, cover in zip(positions,list_of_pix):
				pixmap = QPixmap(cover)
				#print(cover)
				name = str(position[0])+str(position[1])
				exec('self.lb%s.pic = cover'%name)
				exec('self.lb%s.setScaledContents (True)'%name)
				exec('self.lb%s.setPixmap(pixmap)'%name)
				#exec('grid.addWidget(self.lb%s,*position)'%name)
			self.brush()

	def Next(self):
		#print(len(cover_path))

		page = int(len(self.cover_path)//10) - 1

		if self.page ==  page:
			QMessageBox.information(self, 'Message',"最后一页了！", 
			QMessageBox.Yes | QMessageBox.No)
			self.page = page
			num = self.page
			list_of_pix = self.cover_path[num*10:num*10+10]

			positions = [(i,j) for i in range(2) for j in range(5)]
			for position, cover in zip(positions,list_of_pix):
				pixmap = QPixmap(cover)
				#print(cover)
				name = str(position[0])+str(position[1])
				exec('self.lb%s.pic = cover'%name)
				exec('self.lb%s.setScaledContents (True)'%name)
				exec('self.lb%s.setPixmap(pixmap)'%name)
			self.brush()
			

		else:
			
			self.page +=1


			num = self.page
			list_of_pix = self.cover_path[num*10:num*10+10]

			positions = [(i,j) for i in range(2) for j in range(5)]
			for position, cover in zip(positions,list_of_pix):
				pixmap = QPixmap(cover)
				#print(cover)
				name = str(position[0])+str(position[1])
				exec('self.lb%s.pic = cover'%name)
				exec('self.lb%s.setScaledContents (True)'%name)
				exec('self.lb%s.setPixmap(pixmap)'%name)
			self.brush()
				
	def change_page(self):
		self.page = int(self.line.text())
		#print(self.page)
		num = self.page
		#print(type(num))
		list_of_pix = self.cover_path[num*10:num*10+10]
		#print('哇哈哈！')

		positions = [(i,j) for i in range(2) for j in range(5)]
		for position, cover in zip(positions,list_of_pix):
			pixmap = QPixmap(cover)
			#print(cover)
			name = str(position[0])+str(position[1])
			exec('self.lb%s.pic = cover'%name)
			exec('self.lb%s.setScaledContents (True)'%name)
			exec('self.lb%s.setPixmap(pixmap)'%name)
		self.brush()

	def initUI(self):

		a = [(i,j) for i in range(2) for j in range(5)]
		for i in range(10):
			name = str(a[i][0])+str(a[i][1])
			exec('self.lb%s = myLabel()'%name)

		self.grid = QGridLayout()

		self.setLayout(self.grid)

		btn1 = QPushButton('Previous',self)
		#btn1.resize(btn1.sizeHint())#默认尺寸
		btn1.clicked.connect(self.Previous)
		btn1.setShortcut('A')  #shortcut key

		btn2 = QPushButton('Next',self)
		#btn2.resize(btn2.sizeHint())#默认尺寸
		btn2.clicked.connect(self.Next)
		btn2.setShortcut('D')  #shortcut key

		btn3 = QPushButton('open',self)
		#btn2.resize(btn2.sizeHint())#默认尺寸
		btn3.clicked.connect(lambda: self.Openfile(1))
		btn3.setShortcut('O')  #shortcut key

		self.line = QLineEdit(self)
		self.line.editingFinished.connect(self.change_page)

		self.label_page = QLabel(self)
		self.page_text = str(self.page + 1) + '页/' + str(len(self.cover_path)//10) + '页'
		self.label_page.setText('%s' %self.page_text)


		num = self.page
		list_of_pix = self.cover_path[num*10:num*10+10]
		#print(list_of_pix)


		self.horizontal_1 = QHBoxLayout()
		self.horizontal_2 = QHBoxLayout()
		self.horizontal_3 = QHBoxLayout()

		positions = [(i,j) for i in range(2) for j in range(5)]
		for position, cover in zip(positions,list_of_pix):
			pixmap = QPixmap(cover)
			#print(cover)
			name = str(position[0])+str(position[1])
			exec('self.lb%s.pic = cover'%name)
			exec('self.lb%s.setPixmap(pixmap)'%name)
			exec('self.lb%s.setScaledContents (True)'%name)  # 让图片自适应label大小
			
			if position[0] == 0:
				exec('self.horizontal_1.addWidget(self.lb%s)'%name)
				if position[1] == 4:
					self.grid.addLayout(self.horizontal_1, 1, 0, 1, 5)
			if position[0] == 1:
				exec('self.horizontal_2.addWidget(self.lb%s)'%name)
				if position[1] == 4:
					self.grid.addLayout(self.horizontal_2, 2, 0, 1, 5)


		
		self.horizontal_3.addWidget(btn3)
		self.horizontal_3.addWidget(self.label_page)
		self.horizontal_3.addWidget(self.line)
		self.horizontal_3.addWidget(btn1)
		self.horizontal_3.addWidget(btn2)
		self.grid.addLayout(self.horizontal_3, 3, 1, 2,5)#行，列，跨行，跨列

		self.setFixedSize(1850,950)
		self.move(35,35)

		self.setWindowTitle('comic')
		self.show()
		






if __name__ == '__main__':


	#cover_path = get_path(path)

	app = QApplication(sys.argv)
	reader = w_comic()
	sys.exit(app.exec_())
