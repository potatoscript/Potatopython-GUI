# 📧 JPEG Processing Application

This project is a **JPEG Processing Application** built using Python and Tkinter. It allows users to process, rename, and manage image files within specified folders. The application provides a user-friendly GUI and logs actions while interacting with a PostgreSQL database to manage system status and logs.

---

## 📚 **Table of Contents**

- [📧 JPEG Processing Application](#-qc-jpeg-processing-application)
- [📚 Table of Contents](#-table-of-contents)
- [✨ Features](#-features)
- [🚀 Getting Started](#-getting-started)
- [⚙️ Configuration](#️-configuration)
- [🏗️ Project Structure](#️-project-structure)
- [📝 Usage](#-usage)
- [🔌 Database Configuration](#-database-configuration)
- [🐛 Error Handling](#-error-handling)
- [📄 Logs](#-logs)
- [🤝 Contribution](#-contribution)
- [📧 Contact](#-contact)

---

## ✨ **Features**

✅ GUI with Tkinter for easy user interaction.  
✅ Dynamically renames JPEG files and moves them to a target folder.  
✅ Supports batch processing for multiple folders.  
✅ Logs activity and errors into log files.  
✅ Database integration with PostgreSQL for system status updates.  
✅ Handles unexpected termination with signal handlers (`Ctrl + C` and window close).  
✅ Supports Japanese localization for interface text.

---

## 🚀 **Getting Started**

### 📥 Prerequisites

Make sure you have the following installed:

- Python 3.8 or above
- PostgreSQL
- Required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

### 📂 Clone the Repository

```bash
git clone https://github.com/potatoscript/Potatopython-GUI.git
cd Potatopython-GUI
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ **Configuration**

### 🔧 `config.ini` File

Create a `config.ini` file in the root directory with the following content:

```ini
[URL]
data_path = ./data
renamed_path = ./renamed

[PARAM]
title = Internal Email ( VERSION: Ver 1.0.0 )
```

---

## 🏗️ **Project Structure**

```
Potatopython-GUI/
├── data/                     # Source folder containing files to process
├── renamed/                  # Destination folder for renamed files
├── icons/                    # Icons for buttons
├── config.ini                # Configuration file
├── record.log                # Log file for application activity
├── Template.py               # Template class for GUI operations
├── views.py                  # Main application GUI logic
├── models.py                 # Database model logic
└── main.py                   # Entry point of the application
```

---

## 📝 **Usage**

### ▶️ Run the Application

```bash
python main.py
```

### 🔁 Update Data

- Click **Reload** to update the data list.
- Select a target folder and click **Process** to rename and move files.

### 🗂️ Process All Data

- Click **Process All** to process all available folders automatically.

### 🔍 Filter Data

- Use the search bar labeled **Subject Search** to filter the list of folders.

---

## 🔌 **Database Configuration**

### ⚙️ PostgreSQL Setup

Update the `Models` class in `models.py` with your database connection details:

```python
self.db_params_system = {
    'database': 'system',
    'host': 'localhost',
    'user': 'system',
    'password': 'system',
    'port': '5432',
    'query': None,
    'values': None
}
```

### 📡 Update System Status

The application automatically updates the system status (`1` for running, `0` for stopped) in the PostgreSQL database.

---

## 🐛 **Error Handling**

### 🚨 Common Errors

1. **Database Connection Error**

   - Verify the database credentials in `models.py`.
   - Ensure the PostgreSQL server is running.

2. **File Not Found Error**

   - Confirm that the `data/` folder and subfolders are correctly set up.

3. **Permissions Error**
   - Ensure that the application has the necessary permissions to read and write files.

---

## 📄 **Logs**

### 📝 `record.log`

Logs all major actions performed in the application.

### 🗂️ `complete.log`

Logs all successfully processed folders.

---

## 🤝 **Contribution**

Contributions are welcome! Feel free to submit a pull request or open an issue to improve the application.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## 📧 **Contact**

📧 Email: [your.email@example.com](mailto:your.email@example.com)  
🔗 GitHub: [https://github.com/potatoscript](https://github.com/potatoscript)

---
