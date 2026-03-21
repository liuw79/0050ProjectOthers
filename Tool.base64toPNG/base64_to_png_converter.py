import os
import base64
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget

class Base64ToPngConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Base64转PNG转换器')
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()
        
        self.label = QLabel('请选择要转换的base64文件')
        layout.addWidget(self.label)
        
        self.select_button = QPushButton('选择文件')
        self.select_button.clicked.connect(self.select_files)
        layout.addWidget(self.select_button)
        
        self.convert_button = QPushButton('转换')
        self.convert_button.clicked.connect(self.convert_files)
        self.convert_button.setEnabled(False)
        layout.addWidget(self.convert_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.selected_files = []
    
    def select_files(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择Base64文件", "", 
            "所有文件 (*.*)", 
            options=options
        )
        
        if files:
            self.selected_files = files
            self.label.setText(f'已选择 {len(files)} 个文件')
            self.convert_button.setEnabled(True)
    
    def convert_files(self):
        for file_path in self.selected_files:
            try:
                with open(file_path, 'r') as f:
                    base64_data = f.read()
                
                # 移除可能的base64前缀
                if 'base64,' in base64_data:
                    base64_data = base64_data.split('base64,')[1]
                
                # 解码base64数据
                image_data = base64.b64decode(base64_data)
                
                # 创建输出路径
                dir_name = os.path.dirname(file_path)
                file_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path = os.path.join(dir_name, f"{file_name}.png")
                
                # 保存PNG文件
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                
            except Exception as e:
                self.label.setText(f"转换 {file_path} 失败: {str(e)}")
                return
        
        self.label.setText(f"成功转换 {len(self.selected_files)} 个文件")
        self.selected_files = []
        self.convert_button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication([])
    window = Base64ToPngConverter()
    window.show()
    app.exec_()