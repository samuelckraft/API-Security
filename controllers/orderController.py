from flask import request, jsonify
from models.schemas.OrderSchema import order_schema

from services import orderService
from marshmallow import ValidationError

from caching import cache

def save():
    try:
        order_data = order_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    order_save = orderService.save(order_data)
    if order_save is not None:
        return order_schema.jsonify(order_save), 201
    else:
        return jsonify({"message": "Fallback method eror activated", "body":order_data}), 400


@cache.cached(timeout=60)
def find_all():
    orders = orderService.find_all()
    return order_schema.jsonify(orders), 200