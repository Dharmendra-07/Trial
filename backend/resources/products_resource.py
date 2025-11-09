from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with, reqparse, marshal
from services import ProductService

section_field = {
    'name' : fields.String,
}

product_fields = {
    'name': fields.String,
    'price': fields.Float,
    'stock': fields.Float,
    'expiry': fields.DateTime,
    'mfd': fields.DateTime,
    'unit_of_sale': fields.String,
    'section_id': fields.Integer,
    'section': fields.Nested(section_field),
}

parser = reqparse.RequestParser()
parser.add_argument('name',type=str, required=True)
parser.add_argument('price',required=True)
parser.add_argument('stock')
parser.add_argument('expiry')
parser.add_argument('mfd')
parser.add_argument('unit_of_sale')
parser.add_argument('section_id')

'''/api/product/:id'''
class ProductResource(Resource):
    @marshal_with(product_fields)
    def get(self, id):
        item = ProductService.get_by_id(id)
        if not item:
          return {'message': 'Product not found'}, 404
        return item, 200
    
    def put(self, id):
        item = ProductService.get_by_id(id)
        if not item :
          return {'message': 'not found'}, 404
        args = parser.parse_args()
        args['id'] = id
        ProductService.update(args)
        
    def patch(self, id):
      item = ProductService.get_by_id(id)
      if not item:
        return {'message': 'not found'}, 404
      data  = request.get_json()
      ProductService.update(data)
    
    def delete(self, id):
        item = ProductService.get_by_id(id)
        if not item :
          return {'message': 'not found'}, 404
        item = ProductService.delete(id)
        return marshal(item, marshal_fields), 200


'''/api/product -> get, post'''
class ProductListResource(Resource):
  def get(self):
    items = ProductService.get_all()
    return marshal(items, marshal_fields)
  
  def post(self):
    args = parser.parse_args()
    item = ProductService.create(args)
    return marshal(items, marshal_fields)