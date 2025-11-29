# 🧠 Memory Allocation Simulator | شبیه‌ساز تخصیص حافظه

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

[English](#english) | [فارسی](#persian)

---

## <a name="english"></a>🇬🇧 English

### 📖 Description

An interactive educational application that simulates **dynamic memory allocation** in operating systems. This simulator demonstrates four fundamental memory allocation algorithms with real-time visual feedback.

### ✨ Features

- **4 Allocation Algorithms:**
  - 🎯 **First Fit**: Allocates memory in the first available block large enough
  - 🔄 **Next Fit**: Continues search from the last allocation point (circular)
  - 🎪 **Best Fit**: Allocates in the smallest sufficient block (minimizes waste)
  - 📦 **Worst Fit**: Allocates in the largest available block (keeps fragments larger)

- **Visual Interface:**
  - Real-time memory visualization with color-coded blocks
  - Green blocks = Free memory
  - Red blocks = Allocated memory
  - Click-to-deallocate functionality
  - Interactive hover effects

- **Memory Management:**
  - Automatic block splitting during allocation
  - Automatic merging of adjacent free blocks
  - Free list management
  - Fragmentation statistics
    
### 🖥️ Screenshots


<img width="1913" height="1024" alt="image" src="https://github.com/user-attachments/assets/89c13d33-69ec-4c23-9044-03a334273762" />


### 📋 Requirements

```bash
Python 3.8+
PyQt6
```

### 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/memory-allocation-simulator.git
cd memory-allocation-simulator
```

2. Install dependencies:
```bash
pip install PyQt6
```

3. Run the application:
```bash
python memory_allocator.py
```

### 🎮 How to Use

1. **Select Algorithm**: Choose from First Fit, Next Fit, Best Fit, or Worst Fit
2. **Allocate Memory**: Enter size (KB) and click "تخصیص حافظه" (Allocate Memory)
3. **Deallocate Process**: Click on any red (allocated) block to free it
4. **Reset**: Click "بازنشانی حافظه" (Reset Memory) to start fresh
5. **Observe**: Watch the Free List and statistics update in real-time

### 🎯 Educational Goals

- Understand different memory allocation strategies
- Visualize memory fragmentation
- Compare algorithm efficiency
- Learn about free list management
- Observe block splitting and merging

### 🏗️ Architecture

```
MemoryBlock: Represents individual memory blocks
MemoryManager: Implements allocation algorithms
MemoryVisualizer: Handles visual rendering
MemoryAllocatorGUI: Main application interface
```

### 📊 Initial Configuration

The simulator starts with 6 processes (50KB each) separated by gaps:
- 25KB gap
- 40KB gap
- 100KB gap
- 20KB gap
- 10KB gap

Total memory: **1000KB**

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 📝 License

This project is licensed under the MIT License.

---

## <a name="persian"></a>🇮🇷 فارسی

### 📖 توضیحات

یک برنامه آموزشی تعاملی که **تخصیص پویای حافظه** را در سیستم‌عامل‌ها شبیه‌سازی می‌کند. این شبیه‌ساز چهار الگوریتم اصلی تخصیص حافظه را با بازخورد بصری لحظه‌ای نمایش می‌دهد.

### ✨ امکانات

- **4 الگوریتم تخصیص:**
  - 🎯 **First Fit**: تخصیص در اولین بلوک آزاد کافی
  - 🔄 **Next Fit**: ادامه جستجو از آخرین نقطه تخصیص (دایره‌ای)
  - 🎪 **Best Fit**: تخصیص در کوچک‌ترین بلوک مناسب (کمترین اتلاف)
  - 📦 **Worst Fit**: تخصیص در بزرگ‌ترین بلوک آزاد (قطعات باقیمانده بزرگ‌تر)

- **رابط بصری:**
  - نمایش لحظه‌ای حافظه با رنگ‌بندی بلوک‌ها
  - بلوک‌های سبز = حافظه آزاد
  - بلوک‌های قرمز = حافظه تخصیص‌یافته
  - آزادسازی با کلیک روی بلوک
  - جلوه‌های تعاملی hover

- **مدیریت حافظه:**
  - تقسیم خودکار بلوک‌ها هنگام تخصیص
  - ادغام خودکار بلوک‌های آزاد مجاور
  - مدیریت لیست آزاد (Free List)
  - آمار تکه‌تکه‌شدگی

### 📋 پیش‌نیازها

```bash
Python 3.8+
PyQt6
```

### 🚀 نصب

1. کلون کردن مخزن:
```bash
git clone https://github.com/yourusername/memory-allocation-simulator.git
cd memory-allocation-simulator
```

2. نصب وابستگی‌ها:
```bash
pip install PyQt6
```

3. اجرای برنامه:
```bash
python memory_allocator.py
```

### 🎮 نحوه استفاده

1. **انتخاب الگوریتم**: از First Fit، Next Fit، Best Fit یا Worst Fit انتخاب کنید
2. **تخصیص حافظه**: اندازه (KB) را وارد کرده و روی "تخصیص حافظه" کلیک کنید
3. **آزادسازی فرآیند**: روی هر بلوک قرمز (تخصیص‌یافته) کلیک کنید تا آزاد شود
4. **بازنشانی**: روی "بازنشانی حافظه" کلیک کنید تا از نو شروع کنید
5. **مشاهده**: لیست آزاد و آمارها را به صورت لحظه‌ای ببینید

### 🎯 اهداف آموزشی

- درک استراتژی‌های مختلف تخصیص حافظه
- دیدن بصری تکه‌تکه‌شدگی حافظه
- مقایسه کارایی الگوریتم‌ها
- یادگیری مدیریت لیست آزاد
- مشاهده تقسیم و ادغام بلوک‌ها

### 🏗️ معماری

```
MemoryBlock: نمایش بلوک‌های حافظه
MemoryManager: پیاده‌سازی الگوریتم‌های تخصیص
MemoryVisualizer: رندر بصری
MemoryAllocatorGUI: رابط کاربری اصلی
```

### 📊 پیکربندی اولیه

شبیه‌ساز با 6 فرآیند (هر کدام 50KB) که با فاصله‌های زیر جدا شده‌اند، شروع می‌شود:
- فاصله 25KB
- فاصله 40KB
- فاصله 100KB
- فاصله 20KB
- فاصله 10KB

کل حافظه: **1000KB**

### 🎓 مناسب برای

- دانشجویان علوم کامپیوتر
- دوره‌های سیستم‌عامل
- آموزش مدیریت حافظه
- تحقیقات الگوریتم‌ها

### 🤝 مشارکت

مشارکت‌ها خوش‌آمد هستند! لطفاً Pull Request ارسال کنید.

### 📝 مجوز

این پروژه تحت مجوز MIT منتشر شده است.

---

### 👨‍💻 Developer | توسعه‌دهنده

Made with ❤️ for educational purposes

ساخته شده با ❤️ برای اهداف آموزشی

### 🌟 Star this repository if you find it helpful!
### 🌟 اگر این مخزن را مفید یافتید، ستاره دهید!

---

**Keywords**: Memory Management, Operating Systems, First Fit, Best Fit, Worst Fit, Next Fit, Memory Allocation, Fragmentation, Computer Science Education

**کلمات کلیدی**: مدیریت حافظه، سیستم‌عامل، تخصیص حافظه، تکه‌تکه‌شدگی، آموزش علوم کامپیوتر
