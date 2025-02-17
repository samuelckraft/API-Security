from flask import request, jsonify
from models.schemas.EmployeeSchema import employee_schema

from services import employeeService
from marshmallow import ValidationError

from caching import cache


def save():
    try:
        employee_data = employee_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    employee_save = employeeService.save(employee_data)
    if employee_save is not None:
        return employee_schema.jsonify(employee_save), 201
    else:
        return jsonify({"message": "Fallback method eror activated", "body":employee_data}), 400


@cache.cached(timeout=60)
def find_all():
    employees = employeeService.find_all()
    return employee_schema.jsonify(employees), 200

def login():
    employee = request.json

    user = employeeService.login_employee(employee['username'], employee['password'])

    if user:
        return jsonify(user), 200
    
    else:
        resp = {
            'status': 'Error',
            'message': "User does not exist"
        }

        return jsonify(resp), 404