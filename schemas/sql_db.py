role = f"""
CREATE TABLE Role (
    name TEXT,
    code TEXT PRIMARY,
)
"""

status = f"""
CREATE TABLE Status (
    name TEXT,
    code TEXT PRIMARY,
)
"""

user = f"""
CREATE TABLE User (
    name TEXT,
    code TEXT PRIMARY,
    gender BOOLEAN,
    role_code TEXT,
    FOREIGN KEY (role_code) REFERENCES Role(code)
)
"""

attendance = f"""
CREATE TABLE Attendance (
    timestamp DATETIME,
    user_code TEXT,
    status_code TEXT,
    FOREIGN KEY (user_code) REFERENCES User(code),
    FOREIGN KEY (status_code) REFERENCES Status(code),
)
"""