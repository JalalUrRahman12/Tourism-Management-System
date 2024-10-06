import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connect to the MySQL database
def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jalal@21",
            database="Tourism_Management_System"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return None

class TourismManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tourism Management System")
        self.root.geometry("1000x800")
        self.root.config(bg="#2e3f4f")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", font=("Helvetica", 12), foreground="white", background="#2e3f4f")
        style.configure("TButton", font=("Helvetica", 12), background="#4a8fe7", foreground="white")
        style.map("TButton", background=[("active", "#366ac3")])
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("TCombobox", font=("Helvetica", 12))
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#4a8fe7", foreground="white")
        style.configure("Treeview", font=("Helvetica", 12), foreground="#ffffff", background="#3a4b5c", fieldbackground="#3a4b5c")

        self.create_widgets()
        self.treeview = None

    def create_widgets(self):
        self.create_menu()
        self.create_title_label()
        self.create_table_selection_frame()

    def create_title_label(self):
        title_label = tk.Label(self.root, text="Tourism Management System", font=("Helvetica", 24, "bold"), bg="#2e3f4f", fg="#4a8fe7")
        title_label.pack(pady=20)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def show_about(self):
        messagebox.showinfo("About", "Tourism Management System\nVersion 1.0")

    def create_table_selection_frame(self):
        self.selection_frame = ttk.LabelFrame(self.root, text="Table Selection", padding=10)
        self.selection_frame.place(x=5, y=75, width=1355, height=575)

        ttk.Label(self.selection_frame, text="Select Table:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.table_combobox = ttk.Combobox(self.selection_frame, values=[
            "Tourist", "Transportation", "Journey", "Destination", "VisitRecord", 
            "Route", "Accomodation", "Stay", "PaymentTransaction", 
            "PackagePrice", "TourPackages", "Booking"], state="readonly")
        self.table_combobox.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(self.selection_frame, text="Select", command=self.show_data_entry_frame).grid(row=0, column=2, padx=10, pady=5)

    def show_data_entry_frame(self):
        table = self.table_combobox.get()
        if not table:
            messagebox.showerror("Error", "Please select a table.")
            return

        self.current_table = table

        # Hide the selection frame
        self.selection_frame.place_forget()

        if hasattr(self, 'display_frame') and self.display_frame.winfo_exists():
            self.display_frame.place_forget()
        if not hasattr(self, 'data_entry_frame') or not self.data_entry_frame.winfo_exists():
            self.data_entry_frame = ttk.LabelFrame(self.root, text=f"Data Entry for {table}", padding=10)
        
        self.data_entry_frame.place(x=5, y=75, width=1355, height=575)
        for widget in self.data_entry_frame.winfo_children():
            widget.destroy()

        ttk.Button(self.data_entry_frame, text="Back", command=self.show_table_selection_frame).grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)

        columns = self.get_fields_for_table(table)

        self.field_labels = []
        self.field_entries = []

        for i, field in enumerate(columns):
            label = ttk.Label(self.data_entry_frame, text=field + ":")
            entry = ttk.Entry(self.data_entry_frame, width=30)
            self.field_labels.append(label)
            self.field_entries.append(entry)

            label.grid(row=i + 1, column=0, sticky=tk.W, pady=5)
            entry.grid(row=i + 1, column=1, pady=5)

        ttk.Button(self.data_entry_frame, text="Add", command=self.add_data).grid(row=len(columns) + 1, column=0, pady=10)
        ttk.Button(self.data_entry_frame, text="Modify", command=self.modify_data).grid(row=len(columns) + 1, column=1, pady=10)
        ttk.Button(self.data_entry_frame, text="Delete", command=self.delete_data).grid(row=len(columns) + 2, column=0, pady=10)
        ttk.Button(self.data_entry_frame, text="Search", command=self.search_data).grid(row=len(columns) + 2, column=1, pady=10)
        ttk.Button(self.data_entry_frame, text="Show All", command=self.show_all_data).grid(row=len(columns) + 3, column=0, pady=10, columnspan=2)

    def show_all_data(self):
        if hasattr(self, 'data_entry_frame') and self.data_entry_frame.winfo_exists():
            self.data_entry_frame.place_forget()
        if not hasattr(self, 'display_frame') or not self.display_frame.winfo_exists():
            self.display_frame = ttk.LabelFrame(self.root, text=f"Data Display for {self.current_table}", padding=10)

        self.display_frame.place(x=5, y=75, width=1355, height=575)

        ttk.Button(self.display_frame, text="Back", command=self.show_data_entry_frame_from_display).grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        
        columns = self.get_fields_for_table(self.current_table)

        self.treeview = ttk.Treeview(self.display_frame, columns=columns, show="headings")

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100)

        self.treeview.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Adding Vertical Scrollbar
        self.scrollbar = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.display_frame.grid_rowconfigure(1, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)

        self.load_data()

    def show_data_entry_frame_from_display(self):
        self.display_frame.place_forget()
        self.data_entry_frame.place(x=5, y=75, width=1355, height=575)

    def show_table_selection_frame(self):
        if hasattr(self, 'data_entry_frame'):
            self.data_entry_frame.place_forget()
        if hasattr(self, 'display_frame'):
            self.display_frame.place_forget()
        self.create_table_selection_frame()

    def get_fields_for_table(self, table):
        if table == "Tourist":
            return ["T_ID", "Name", "Gender", "Age", "Phone_No", "Email", "CNIC"]
        elif table == "Transportation":
            return ["Trans_ID", "Type", "Depar_Time", "Arriv_Time"]
        elif table == "Journey":
            return ["T_ID", "Trans_ID", "Depar_Date"]
        elif table == "Destination":
            return ["Dest_ID", "Name", "Depar_Location", "Dest_Location"]
        elif table == "VisitRecord":
            return ["Dest_ID", "T_ID", "Visit_Date"]
        elif table == "Route":
            return ["Dest_ID", "Trans_ID"]
        elif table == "Accomodation":
            return ["Acc_ID", "Dest_ID", "Hotel_Name"]
        elif table == "Stay":
            return ["T_ID", "Acc_ID", "Check_In", "Check_Out", "Room_Type"]
        elif table == "PaymentTransaction":
            return ["Pay_ID", "Payment_Date", "Payment_Method", "Payment_Status"]
        elif table == "PackagePrice":
            return ["Type", "Price"]
        elif table == "TourPackages":
            return ["TP_ID", "Package_Name", "Type"]
        elif table == "Booking":
            return ["B_ID", "T_ID", "TP_ID", "Pay_ID", "Duration_Ofpackage"]

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_data(self):
        table = self.current_table
        if table:
            self.treeview.delete(*self.treeview.get_children())
            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table}")
                for row in cursor.fetchall():
                    self.treeview.insert("", tk.END, values=row)
                cursor.close()
                conn.close()

    def add_data(self):
        table = self.current_table
        fields = self.get_fields_for_table(table)
        values = [entry.get() for entry in self.field_entries]

        if all(values):
            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                placeholders = ", ".join(["%s"] * len(fields))
                try:
                    cursor.execute(f"INSERT INTO {table} VALUES ({placeholders})", values)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.show_all_data()
                    self.clear_entries()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error: {err}")
                    cursor.close()
                    conn.close()
        else:
            messagebox.showerror("Error", "All fields are required")

    def modify_data(self):
        if self.treeview is None:
            messagebox.showerror("Error", "No data to modify")
            return

        table = self.current_table
        fields = self.get_fields_for_table(table)
        values = [entry.get() for entry in self.field_entries]

        if all(values):
            selected_item = self.treeview.selection()
            if selected_item:
                item = self.treeview.item(selected_item)
                id_field = fields[0]
                id_value = item['values'][0]
                conn = connect_to_db()
                if conn:
                    cursor = conn.cursor()
                    set_clause = ", ".join([f"{field}=%s" for field in fields[1:]])
                    cursor.execute(f"UPDATE {table} SET {set_clause} WHERE {id_field}=%s", values[1:] + [id_value])
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.show_all_data()
                    self.clear_entries()
            else:
                messagebox.showerror("Error", "No item selected for modification")
        else:
            messagebox.showerror("Error", "All fields are required")

    def delete_data(self):
        if self.treeview is None:
            messagebox.showerror("Error", "No data to delete")
            return

        table = self.current_table
        fields = self.get_fields_for_table(table)

        selected_item = self.treeview.selection()
        if selected_item:
            item = self.treeview.item(selected_item)
            id_field = fields[0]
            id_value = item['values'][0]
            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(f"DELETE FROM {table} WHERE {id_field}=%s", (id_value,))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    self.show_all_data()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error: {err}")
                    cursor.close()
                    conn.close()
        else:
            messagebox.showerror("Error", "No item selected for deletion")

    def search_data(self):
        table = self.current_table
        fields = self.get_fields_for_table(table)
        id_search = self.field_entries[0].get()

        if id_search:
            conn = connect_to_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table} WHERE {fields[0]} = %s", (id_search,))
                row = cursor.fetchone()
                cursor.close()
                conn.close()

                if row:
                    for i, value in enumerate(row):
                        self.field_entries[i].delete(0, tk.END)
                        self.field_entries[i].insert(0, value)
                else:
                    messagebox.showinfo("No Results", f"No entry found with {fields[0]} = {id_search}")
        else:
            messagebox.showerror("Error", "ID field is required for search")

    def clear_entries(self):
        for entry in self.field_entries:
            entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TourismManagementApp(root)
    root.mainloop()
