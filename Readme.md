# Tourism Management System

The Tourism Management System is a Python application designed to manage various aspects of tourism operations, including booking management, customer interactions, resource allocation, and reporting. It provides a graphical user interface (GUI) built with Tkinter and utilizes a MySQL database for data storage.

## Functionality
The system includes modules for:
- **Booking Management:** Add, update, delete, and search bookings by ID and customer name.
- **Customer Relationship Management (CRM):** Manage customer details, including contact information and interaction history.
- **Reporting:** Generate reports on bookings, customer interactions, and resource utilization.

## System Requirements
### Software Requirements:
- Python 3.x
- Tkinter (usually included with Python installations)
- MySQL 8.3 Server
- MySQL Connector/Python

### Hardware Requirements:
- Standard desktop or laptop with sufficient RAM and CPU for running Python applications.

## Installation Instructions
1. **Install Python:**
   - Download and install Python 3.x from [python.org](https://www.python.org/).

2. **Install MySQL Server:**
   - Download and install MySQL Server from [mysql.com](https://www.mysql.com/) if not already installed.

3. **Install Required Python Libraries:**
   - Open a terminal or command prompt.
   - Install MySQL Connector/Python by running the following command:
     ```
     pip install mysql-connector-python
     ```
   - Tkinter is usually included with Python installations and may not require separate installation.

4. **Clone the Repository:**
   ```
   git clone https://github.com/JalalUrRahman12/DB-Project/blob/main/README.md
   ```

5. **Database Setup:**
   - Import the database schema and initial data from `database/schema.sql` into your MySQL database.

6. **Modify Database Configuration:**
   - Open `config.py` and update the MySQL database configuration settings:
     ```python
     db_config = {
         'host': 'localhost',
         'user': 'root',
         'password': 'your-password',
         'database': 'tourism_db'
     }
     ```

## Usage Instructions
1. **Run the Application:**
   - Navigate to the project directory.
   - Start the application:
     ```
     python main.py
     ```

2. **Use the Application:**
   - Navigate through different modules (searching,adding,updating,deleting) using the GUI.
   - Perform operations like adding, updating, deleting, and searching data.
   - View and manage tourism data efficiently.

## Code Structure Overview
- **`tourism.py`:** Main entry point of the application.

## Credits
- **Team Members:** Munawar Khan, Zunaira Jala ur rehman, Shehzana bibi
- **Third-Party Libraries:**
  - Tkinter: GUI library for Python.
  - MySQL Connector/Python: MySQL database connector for Python.
