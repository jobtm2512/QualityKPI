# Quality Management System

A web-based application built with Flask and MySQL for managing quality indicators, divisions, departments, and sub-departments in a healthcare organization. The system allows users to add quality indicators, divisions, departments, sub-departments, and tag quality indicators to departments or sub-departments. The goal is to streamline the management of key performance indicators (KPIs) within the organization.

## Features

- Add new quality indicators with unique IDs.
- Manage divisions, departments, and sub-departments.
- Tag quality indicators to specific departments and sub-departments.
- Display success or error messages using Flask's flash messaging system.
- Simple, user-friendly interface.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- MySQL
- MySQL Connector for Python

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/quality-management-system.git
    ```

2. Navigate to the project directory:

    ```bash
    cd quality-management-system
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the MySQL database:

    - Create a MySQL database named `quality_management`.
    - Run the following SQL commands to create the necessary tables:

    ```sql
    CREATE TABLE Division (
      id INT AUTO_INCREMENT PRIMARY KEY,
      division_name VARCHAR(255) NOT NULL
    );

    CREATE TABLE Department (
      id INT AUTO_INCREMENT PRIMARY KEY,
      department_name VARCHAR(255) NOT NULL,
      division_id INT,
      FOREIGN KEY (division_id) REFERENCES Division(id)
    );

    CREATE TABLE Sub_department (
      id INT AUTO_INCREMENT PRIMARY KEY,
      sub_department_name VARCHAR(255) NOT NULL,
      department_id INT,
      FOREIGN KEY (department_id) REFERENCES Department(id)
    );

    CREATE TABLE quality_indicators (
      id INT AUTO_INCREMENT PRIMARY KEY,
      indicator_id VARCHAR(50) NOT NULL,
      indicator_name VARCHAR(255) NOT NULL,
      numerator VARCHAR(255),
      denominator VARCHAR(255),
      factor INT,
      frequency VARCHAR(255),
      benchmark INT
    );

    CREATE TABLE quality_indicator_tags (
      id INT AUTO_INCREMENT PRIMARY KEY,
      quality_indicator_id VARCHAR(50),
      department_id INT,
      sub_department_id INT,
      FOREIGN KEY (quality_indicator_id) REFERENCES quality_indicators(indicator_id),
      FOREIGN KEY (department_id) REFERENCES Department(id),
      FOREIGN KEY (sub_department_id) REFERENCES Sub_department(id)
    );
    ```

5. Update the MySQL connection settings in `app.py`:

    ```python
    db = mysql.connector.connect(host="localhost", user="root", passwd="your_mysql_password", db="quality_management")
    ```

6. Run the Flask application:

    ```bash
    python app.py
    ```

7. Open your web browser and navigate to:

    ```
    http://localhost:5000
    ```

## Usage

- **Add Quality Indicator**: Navigate to `/add_quality_indicator` to add a new quality indicator.
- **Add Division, Department, and Sub-department**: Navigate to `/add_division_dept` to add a new division, department, and sub-department.
- **Tag Quality Indicator**: Navigate to `/tag_quality_indicator` to tag a quality indicator to a department and sub-department.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
