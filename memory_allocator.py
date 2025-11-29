import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QSpinBox, 
                             QComboBox, QTableWidget, QTableWidgetItem, 
                             QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QPen

class MemoryBlock:
    def __init__(self, start, size, is_free=True, process_id=None):
        self.start = start
        self.size = size
        self.is_free = is_free
        self.process_id = process_id

class MemoryManager:
    def __init__(self, total_memory=1000):
        self.total_memory = total_memory
        self.blocks = [MemoryBlock(0, total_memory, True)]
        self.allocated_processes = {}
        self.next_process_id = 1
        self.last_allocated_index = 0
        
    def initialize_with_gaps(self):
        gaps = [25, 40, 100, 20, 10]
        initial_process_size = 50
        
        self.blocks = []
        current_pos = 0
        
        for gap_size in gaps:
            self.blocks.append(MemoryBlock(current_pos, initial_process_size, False, self.next_process_id))
            self.allocated_processes[self.next_process_id] = (len(self.blocks) - 1, current_pos, initial_process_size)
            current_pos += initial_process_size
            self.next_process_id += 1
            
            self.blocks.append(MemoryBlock(current_pos, gap_size, True))
            current_pos += gap_size
        
        self.blocks.append(MemoryBlock(current_pos, initial_process_size, False, self.next_process_id))
        self.allocated_processes[self.next_process_id] = (len(self.blocks) - 1, current_pos, initial_process_size)
        current_pos += initial_process_size
        self.next_process_id += 1
        
        if current_pos < self.total_memory:
            self.blocks.append(MemoryBlock(current_pos, self.total_memory - current_pos, True))
        
    def get_free_blocks(self):
        return [block for block in self.blocks if block.is_free]
    
    def first_fit(self, size):
        for i, block in enumerate(self.blocks):
            if block.is_free and block.size >= size:
                return i
        return -1
    
    def next_fit(self, size):
        n = len(self.blocks)
        for i in range(n):
            index = (self.last_allocated_index + i) % n
            block = self.blocks[index]
            if block.is_free and block.size >= size:
                return index
        return -1
    
    def best_fit(self, size):
        best_index = -1
        min_diff = float('inf')
        
        for i, block in enumerate(self.blocks):
            if block.is_free and block.size >= size:
                diff = block.size - size
                if diff < min_diff:
                    min_diff = diff
                    best_index = i
        
        return best_index
    
    def worst_fit(self, size):
        worst_index = -1
        max_diff = -1
        
        for i, block in enumerate(self.blocks):
            if block.is_free and block.size >= size:
                diff = block.size - size
                if diff > max_diff:
                    max_diff = diff
                    worst_index = i
        
        return worst_index
    
    def allocate(self, size, algorithm='first_fit'):
        if algorithm == 'first_fit':
            block_index = self.first_fit(size)
        elif algorithm == 'next_fit':
            block_index = self.next_fit(size)
        elif algorithm == 'best_fit':
            block_index = self.best_fit(size)
        else:
            block_index = self.worst_fit(size)
        
        if block_index == -1:
            return None
        
        if algorithm == 'next_fit':
            self.last_allocated_index = block_index
        
        block = self.blocks[block_index]
        process_id = self.next_process_id
        self.next_process_id += 1
        
        if block.size > size:
            new_allocated = MemoryBlock(block.start, size, False, process_id)
            new_free = MemoryBlock(block.start + size, block.size - size, True)
            
            self.blocks[block_index:block_index+1] = [new_allocated, new_free]
            self.allocated_processes[process_id] = (block_index, new_allocated.start, size)
        else:
            block.is_free = False
            block.process_id = process_id
            self.allocated_processes[process_id] = (block_index, block.start, block.size)
        
        return process_id
    
    def deallocate(self, process_id):
        if process_id not in self.allocated_processes:
            return False
        
        block_to_free = None
        for i, block in enumerate(self.blocks):
            if not block.is_free and block.process_id == process_id:
                block_to_free = i
                break
        
        if block_to_free is None:
            return False
        
        self.blocks[block_to_free].is_free = True
        self.blocks[block_to_free].process_id = None
        del self.allocated_processes[process_id]
        
        self._merge_free_blocks()
        
        return True
    
    def _merge_free_blocks(self):
        i = 0
        while i < len(self.blocks) - 1:
            if self.blocks[i].is_free and self.blocks[i + 1].is_free:
                merged_block = MemoryBlock(
                    self.blocks[i].start,
                    self.blocks[i].size + self.blocks[i + 1].size,
                    True
                )
                self.blocks[i:i+2] = [merged_block]
            else:
                i += 1
    
    def get_fragmentation_stats(self):
        free_blocks = self.get_free_blocks()
        total_free = sum(block.size for block in free_blocks)
        num_free_blocks = len(free_blocks)
        return total_free, num_free_blocks
    
    def get_process_at_position(self, x_pos, widget_width):
        scale = widget_width / self.total_memory
        
        current_x = 0
        for block in self.blocks:
            block_width = block.size * scale
            if current_x <= x_pos <= current_x + block_width:
                if not block.is_free:
                    return block.process_id
                return None
            current_x += block_width
        return None

class MemoryVisualizer(QWidget):
    process_clicked = pyqtSignal(int)
    
    def __init__(self, memory_manager):
        super().__init__()
        self.memory_manager = memory_manager
        self.setMinimumHeight(100)
        self.setMouseTracking(True)
        self.hovered_process = None
        
    def mousePressEvent(self, event):
        process_id = self.memory_manager.get_process_at_position(
            event.position().x(), self.width()
        )
        if process_id is not None:
            self.process_clicked.emit(process_id)
    
    def mouseMoveEvent(self, event):
        process_id = self.memory_manager.get_process_at_position(
            event.position().x(), self.width()
        )
        if process_id is not None:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.hovered_process = process_id
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.hovered_process = None
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        width = self.width()
        height = self.height()
        
        scale = width / self.memory_manager.total_memory
        
        x = 0
        for block in self.memory_manager.blocks:
            block_width = int(block.size * scale)
            
            if block.is_free:
                color = QColor(100, 200, 100)
            else:
                if block.process_id == self.hovered_process:
                    color = QColor(220, 80, 80)
                else:
                    color = QColor(200, 100, 100)
            
            painter.fillRect(x, 0, block_width, height, color)
            
            painter.setPen(QPen(QColor(0, 0, 0), 2))
            painter.drawRect(x, 0, block_width, height)
            
            painter.setPen(QColor(255, 255, 255))
            font = QFont('Arial', 9, QFont.Weight.Bold)
            painter.setFont(font)
            
            if block.is_free:
                text = f"آزاد\n{block.size}KB"
            else:
                text = f"P{block.process_id}\n{block.size}KB"
            
            painter.drawText(x, 0, block_width, height, 
                           Qt.AlignmentFlag.AlignCenter, text)
            
            x += block_width

class MemoryAllocatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.memory_manager = MemoryManager(1000)
        self.current_algorithm = 'first_fit'
        
        self.memory_manager.initialize_with_gaps()
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('شبیه‌ساز تخصیص حافظه')
        self.setGeometry(100, 100, 1200, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        title = QLabel('شبیه‌ساز تخصیص حافظه پویا')
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        instruction = QLabel('برای آزادسازی فرآیند، روی آن کلیک کنید')
        instruction.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        instruction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction.setStyleSheet('color: blue;')
        main_layout.addWidget(instruction)
        
        memory_group = QGroupBox('نمایش حافظه')
        memory_layout = QVBoxLayout()
        
        self.memory_visualizer = MemoryVisualizer(self.memory_manager)
        self.memory_visualizer.process_clicked.connect(self.on_process_clicked)
        memory_layout.addWidget(self.memory_visualizer)
        
        legend_layout = QHBoxLayout()
        legend_layout.addStretch()
        
        free_label = QLabel('■ آزاد')
        free_label.setStyleSheet('color: rgb(100, 200, 100); font-weight: bold; font-size: 12pt;')
        legend_layout.addWidget(free_label)
        
        allocated_label = QLabel('■ تخصیص‌یافته')
        allocated_label.setStyleSheet('color: rgb(200, 100, 100); font-weight: bold; font-size: 12pt;')
        legend_layout.addWidget(allocated_label)
        
        legend_layout.addStretch()
        memory_layout.addLayout(legend_layout)
        
        memory_group.setLayout(memory_layout)
        main_layout.addWidget(memory_group)
        
        control_table_layout = QHBoxLayout()
        
        control_group = QGroupBox('کنترل‌ها')
        control_layout = QVBoxLayout()
        
        algo_layout = QHBoxLayout()
        algo_label = QLabel('الگوریتم:')
        algo_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(['First Fit', 'Next Fit', 'Best Fit', 'Worst Fit'])
        self.algorithm_combo.currentTextChanged.connect(self.change_algorithm)
        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.algorithm_combo)
        control_layout.addLayout(algo_layout)
        
        size_layout = QHBoxLayout()
        size_label = QLabel('اندازه (KB):')
        size_label.setFont(QFont('Arial', 10, QFont.Weight.Bold))
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(1, 500)
        self.size_spinbox.setValue(50)
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_spinbox)
        control_layout.addLayout(size_layout)
        
        self.allocate_button = QPushButton('تخصیص حافظه')
        self.allocate_button.setStyleSheet('QPushButton { background-color: #4CAF50; color: white; padding: 10px; font-weight: bold; }')
        self.allocate_button.clicked.connect(self.allocate_memory)
        control_layout.addWidget(self.allocate_button)
        
        self.reset_button = QPushButton('بازنشانی حافظه')
        self.reset_button.setStyleSheet('QPushButton { background-color: #f44336; color: white; padding: 10px; font-weight: bold; }')
        self.reset_button.clicked.connect(self.reset_memory)
        control_layout.addWidget(self.reset_button)
        
        control_layout.addStretch()
        control_group.setLayout(control_layout)
        control_table_layout.addWidget(control_group)
        
        free_list_group = QGroupBox('لیست بلوک‌های آزاد (Free List)')
        free_list_layout = QVBoxLayout()
        
        self.free_list_table = QTableWidget()
        self.free_list_table.setColumnCount(3)
        self.free_list_table.setHorizontalHeaderLabels(['آدرس شروع', 'اندازه (KB)', 'وضعیت'])
        self.free_list_table.horizontalHeader().setStretchLastSection(True)
        free_list_layout.addWidget(self.free_list_table)
        
        free_list_group.setLayout(free_list_layout)
        control_table_layout.addWidget(free_list_group)
        
        allocated_group = QGroupBox('فرآیندهای تخصیص‌یافته (کلیک برای آزادسازی)')
        allocated_layout = QVBoxLayout()
        
        self.allocated_table = QTableWidget()
        self.allocated_table.setColumnCount(3)
        self.allocated_table.setHorizontalHeaderLabels(['شناسه فرآیند', 'آدرس شروع', 'اندازه (KB)'])
        self.allocated_table.horizontalHeader().setStretchLastSection(True)
        allocated_layout.addWidget(self.allocated_table)
        
        allocated_group.setLayout(allocated_layout)
        control_table_layout.addWidget(allocated_group)
        
        main_layout.addLayout(control_table_layout)
        
        stats_group = QGroupBox('آمار حافظه')
        stats_layout = QHBoxLayout()
        
        self.stats_label = QLabel()
        self.stats_label.setFont(QFont('Arial', 11, QFont.Weight.Bold))
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_layout.addWidget(self.stats_label)
        
        stats_group.setLayout(stats_layout)
        main_layout.addWidget(stats_group)
        
        self.update_display()
        
    def change_algorithm(self, text):
        if text == 'First Fit':
            self.current_algorithm = 'first_fit'
        elif text == 'Next Fit':
            self.current_algorithm = 'next_fit'
        elif text == 'Best Fit':
            self.current_algorithm = 'best_fit'
        else:
            self.current_algorithm = 'worst_fit'
    
    def allocate_memory(self):
        size = self.size_spinbox.value()
        process_id = self.memory_manager.allocate(size, self.current_algorithm)
        
        if process_id is None:
            QMessageBox.warning(self, 'خطا', 
                              f'حافظه کافی برای تخصیص {size}KB وجود ندارد!\n\n'
                              f'الگوریتم: {self.current_algorithm}')
        else:
            self.update_display()
    
    def on_process_clicked(self, process_id):
        reply = QMessageBox.question(
            self, 
            'تایید آزادسازی',
            f'آیا می‌خواهید فرآیند P{process_id} را آزاد کنید؟',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.memory_manager.deallocate(process_id)
            if success:
                self.update_display()
                QMessageBox.information(self, 'موفقیت', 
                                      f'فرآیند P{process_id} با موفقیت آزاد شد!')
            else:
                QMessageBox.warning(self, 'خطا', 'خطا در آزادسازی فرآیند!')
    
    def reset_memory(self):
        reply = QMessageBox.question(
            self, 
            'تایید بازنشانی',
            'آیا می‌خواهید حافظه را بازنشانی کنید؟',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.memory_manager = MemoryManager(1000)
            self.memory_manager.initialize_with_gaps()
            self.memory_visualizer.memory_manager = self.memory_manager
            self.update_display()
    
    def update_display(self):
        self.memory_visualizer.update()
        
        free_blocks = self.memory_manager.get_free_blocks()
        self.free_list_table.setRowCount(len(free_blocks))
        
        for i, block in enumerate(free_blocks):
            self.free_list_table.setItem(i, 0, 
                QTableWidgetItem(str(block.start)))
            self.free_list_table.setItem(i, 1, 
                QTableWidgetItem(str(block.size)))
            self.free_list_table.setItem(i, 2, 
                QTableWidgetItem('آزاد'))
        
        allocated_blocks = [b for b in self.memory_manager.blocks if not b.is_free]
        self.allocated_table.setRowCount(len(allocated_blocks))
        
        for i, block in enumerate(allocated_blocks):
            self.allocated_table.setItem(i, 0, 
                QTableWidgetItem(f'P{block.process_id}'))
            self.allocated_table.setItem(i, 1, 
                QTableWidgetItem(str(block.start)))
            self.allocated_table.setItem(i, 2, 
                QTableWidgetItem(str(block.size)))
        
        total_free, num_free_blocks = self.memory_manager.get_fragmentation_stats()
        total_allocated = self.memory_manager.total_memory - total_free
        stats_text = (f'کل حافظه: {self.memory_manager.total_memory}KB | '
                     f'تخصیص‌یافته: {total_allocated}KB | '
                     f'آزاد: {total_free}KB | '
                     f'تعداد بلوک‌های آزاد: {num_free_blocks}')
        self.stats_label.setText(stats_text)

def main():
    app = QApplication(sys.argv)
    
    font = QFont('Arial', 10)
    app.setFont(font)
    
    window = MemoryAllocatorGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()