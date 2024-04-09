from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

editor_ns = Namespace("editor", description="Editor related operations")

@editor_ns.route("/")
class EditorAPI(Resource):
    @editor_ns.doc("List all editors in the agency")
    def get(self):
        pass
    @editor_ns.doc("Create a new editor")
    def post(self):
        pass