import os
import sys
import socket
import signal
import atexit
import configparser
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, filedialog
from datetime import datetime
import win32api
import win32con
from PIL import Image, ImageTk
from potato import Template as template


class Views:
    """Main application class to initialize and control the GUI."""

    def __init__(self, root):
        """Initialize the main window and setup handlers."""
        self.root = root
        self.window_width = 650
        self.window_height = 600

        # Set up signal handlers and exit cleanup
        atexit.register(self.exit_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        win32api.SetConsoleCtrlHandler(self.console_ctrl_handler, True)

        try:
            # Initialize Template and Logger
            self.template = template()
            self.template.set_window_position(root, root, self.window_width, self.window_height)
            self.template.logging_init("record.log")

            # Load configuration file
            self.config = configparser.ConfigParser()
            self.config.read("config.ini", encoding='utf-8')

            # Set file paths and localization
            self.data_path = self.config.get("URL", "data_path")
            self.renamed_path = self.config.get("URL", "renamed_path")
            self.title = self.config.get("PARAM", "title")

            # Store image references to prevent garbage collection
            self.image_references = self.load_icons()

            # Set up UI and reload initial data
            self.root.title(self.title)
            self.globalid = os.getlogin().upper()
            self.pc_name = socket.gethostname()
            self.selected_item, self.selected_id, self.target_id = [], [], []

            self.create_main_window_item()

        except Exception as error:
            messagebox.showerror("Error", f"An error occurred: {error}")

    def load_icons(self):
        """Load and store icons for the application."""
        icons = [
            "reload", "delete", "master", "csv", "save",
            "register", "add", "send", "preview", "complete"
        ]
        return {icon: self.template.get_icon(icon) for icon in icons}

    def create_main_section(self):
        """Create main section with input fields and action buttons."""
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10)

        # Create Label and Entry for filtering data
        self.boxno_label, self.subject_entry = self.template.create_label_and_entry(
            input_frame, "Lot Number", 1, 0, 15, 12
        )
        self.subject_entry.bind("<KeyRelease>", self.filter_table_data)

        # Create action buttons with icons
        button_data = [
            ("Refresh", self.reload_data, "Reload.TButton", "reload", 1, 2),
            ("Execute", self.process_file, "Delete.TButton", "send", 1, 3),
            ("Execute (All)", self.process_file_all, "Delete.TButton", "send", 1, 4)
        ]
        for text, command, style, icon, row, col in button_data:
            self.template.create_button(
                input_frame, text, command, style, self.image_references[icon], row, col, pady=1, padx=(10, 0)
            )

    def create_main_window_item(self):
        """Create the main window and initialize table."""
        self.create_main_section()
        self.create_data_table()
        self.reload_data()

    def create_data_table(self):
        """Create data table with columns and custom row styles."""
        columns = ("Lot Number", "Status", "Select")
        column_widths = (300, 200, 100)

        self.data_table = self.template.create_table_pack(
            self.root, columns, column_widths, 35, 18, None, None
        )

        # Set row colors and bind row click event
        self.data_table.tag_configure("selected", background="yellow", foreground="red")
        self.data_table.bind("<Button-1>", self.on_row_click)

    def on_row_click(self, event):
        """Handle row click to select/unselect rows."""
        column_index = self.data_table.identify_column(event.x).split('#')[-1]
        item_id = self.data_table.identify_row(event.y)

        if column_index != '0' and item_id:
            item_id = item_id.split("#")[-1]
            values = self.data_table.item(item_id, option="values")
            self.toggle_row_selection(item_id, values)
        else:
            values = self.data_table.item(item_id, option="values")
            self.data_id = -1
            self.set_value_to_show_table(values)

    def toggle_row_selection(self, item_id, values):
        """Toggle selection for a row and update target IDs."""
        if item_id in self.selected_item:
            self.data_table.item(item_id, tags=())
            self.selected_item.remove(item_id)
            self.selected_id.remove((values[0], values[1]))
            self.data_table.item(item_id, values=[values[0], values[1], ""])
        else:
            self.data_table.item(item_id, tags=("selected",))
            self.selected_item.append(item_id)
            self.selected_id.append((values[0], values[1]))
            self.data_table.item(item_id, values=[values[0], values[1], "Selected"])

        self.target_id = ', '.join(f"'{id_}'" for id_ in self.selected_id)

    def process_file_all(self):
        """Process all files by iterating through all items in the table."""
        self.selected_id = []
        for item_id in self.data_table.get_children():
            values = self.data_table.item(item_id, option="values")
            if values:
                self.selected_id.append((values[0], values[1]))
        self.process_file()

    def process_file(self):
        """Process selected files and rename JPEG images."""
        try:
            if messagebox.askyesno("Confirmation", "Do you want to proceed with execution?"):
                if not self.selected_id:
                    messagebox.showinfo("Info", "Please select the target lot.")
                    return

                for values in self.selected_id:
                    if values[1] == "Unprocessed":
                        self.rename_files(values[0])
                        self.record_processed(values[0])
                        self.template.logging_date(f"【{self.pc_name}】【{self.globalid}】Renamed JPEG for {values[0]}")
                self.reload_data()

        except Exception as e:
            messagebox.showerror("ERROR", f"Rename ERROR: {e}")

    def rename_files(self, folder_name):
        """Rename and copy JPEG files to the target folder."""
        folder_path = os.path.join(self.data_path, folder_name)
        subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

        for subfolder in subfolders:
            new_folder_path = os.path.join(self.renamed_path, folder_name, subfolder)
            os.makedirs(new_folder_path, exist_ok=True)

            subfolder_path = os.path.join(folder_path, subfolder, "GoodDieImages", "GoodDiceImages")
            for f in os.listdir(subfolder_path):
                if f.endswith('.jpeg'):
                    prefix = f.split('-')[0]
                    new_filename = f"{prefix}-{folder_name}-{subfolder}-{f.split('-', 1)[-1]}"
                    shutil.copy(os.path.join(subfolder_path, f), os.path.join(new_folder_path, new_filename))

    def record_processed(self, folder_name):
        """Record processed folder name to log."""
        log_file_path = "processed.log"
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(folder_name + "\n")

    def reload_data(self):
        """Reload data and refresh the table."""
        try:
            self.clear_table_data()
            folder_list = os.listdir(self.data_path)
            for index, row in enumerate(folder_list):
                if self.check_record_log(row):
                    continue
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.data_table.insert("", "end", values=(row, "Unprocessed"), tags=(tag, "xfont"))

        except Exception as e:
            messagebox.showerror("ERROR", f"Reload ERROR: {e}")

    def check_record_log(self, folder_path):
        """Check if the folder was already processed."""
        log_file_path = "processed.log"
        with open(log_file_path, "r", encoding="utf-8") as f:
            for line in f:
                if folder_path in line:
                    return True
        return False

    def clear_table_data(self):
        """Clear data from the table."""
        self.data_table.delete(*self.data_table.get_children())

    def exit_handler(self):
        """Handle application exit and update system status."""
        print("Exiting application. Setting update_system_status to 0.")
        Models().update_system_status(0, self.pc_name, self.globalid)

    def signal_handler(self, signal, frame):
        """Handle Ctrl+C signal and update system status."""
        print("Received Ctrl+C. Setting update_system_status to 0.")
        Models().update_system_status(0, self.pc_name, self.globalid)
        sys.exit(0)

    def console_ctrl_handler(self, ctrl_type):
        """Handle console close event."""
        if ctrl_type == win32con.CTRL_CLOSE_EVENT:
            print("Console window is closing. Setting update_system_status to 0.")
            Models().update_system_status(0, self.pc_name, self.globalid)
            return True
        return False


class Models:
    """Database connection and status handling class."""

    def __init__(self):
        """Initialize database connection parameters."""
        self.template = template()
        self.db_params_system = {
            'database': 'system',
            'host': 'localhost',  
            'user': 'system',
            'password': 'system',
            'port': '5432',
            'query': None,
            'values': None
        }

    def update_system_status(self, onoff, pc_name, globalid):
        """Update system status in the database."""
        try:
            update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = """
                UPDATE vos.website_system
                SET update_date=%s, status=%s, pc_user=%s
                WHERE system_name = 'qc_jpeg'
            """
            self.execute_query(query, (update_time, onoff, f"{pc_name}_{globalid}"))
        except Exception as e:
            print(f"PostgreSQL ERROR: {e}")
            self.record_log('', f"PostgreSQL ERROR: {e}")

    def record_log(self, log, error):
        """Log errors to the database."""
        try:
            update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = """
                INSERT INTO vos.website_log
                (system_name, system_type, update_date, log, error)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.execute_query(query, ('qc_jpeg', 'main', update_time, log, error))
        except Exception as e:
            print(f"PostgreSQL ERROR: {e}")

    def execute_query(self, query, values):
        """Execute the query with provided values."""
        query_params = {'query': query}
        values_params = {'values': values}
        self.db_params_system.update(query_params)
        self.db_params_system.update(values_params)
        self.template.db_commit_values(self.db_params_system)


if __name__ == "__main__":
    root = tk.Tk()
    app = Views(root)
    root.mainloop()
