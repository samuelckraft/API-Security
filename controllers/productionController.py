from flask import request, jsonify
from models.schemas.ProductionSchema import production_schema

from services import productionService
from marshmallow import ValidationError

from caching import cache

def save():
    try:
        customer_data = production_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    production_save = productionService.save(customer_data)
    if production_save is not None:
        return production_schema.jsonify(production_save), 201
    else:
        return jsonify({"message": "Fallback method eror activated", "body":customer_data}), 400


@cache.cached(timeout=60)
def find_all():
    productions = productionService.find_all()
    return production_schema.jsonify(productions), 200