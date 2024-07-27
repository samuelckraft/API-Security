from sqlalchemy.orm import Session
from database import db
from models.employee import Employee
from circuitbreaker import circuit
from sqlalchemy import select
from models.user import User
from utils.util import encode_token
from werkzeug.security import check_password_hash

def fallback_function(employee):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(employee_data):
    try:
        if employee_data['name'] == "Failure":
            raise Exception("Failure condition triggered")
        
        with Session(db.engine) as session:
            with session.begin():
                new_employee = Employee(name=employee_data["name"], position=employee_data['position'])
                session.add(new_employee)
                session.commit
            session.refresh(new_employee)
            return new_employee
    except Exception as e:
        raise e
    

def find_all():
    query = select(Employee)
    employees = db.session.execute(query).scalars().all()
    return employees

def login_employee(username, password):
    user = (db.session.execute(db.select(User).where(User.username == username, User.password == password)).scalar_one_or_none())
    role_names = [role.role_name for role in user.roles]
    if user:
        if check_password_hash(user.password, password):
            auth_token = encode_token(user.id, role_names)

            resp = {
                'status': 'success',
                'message': "Successfully logged in",
                'auth_token': auth_token
            }
            return resp
        
        else:
            return None
    else:
        return None