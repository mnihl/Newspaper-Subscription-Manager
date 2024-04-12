from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
import uuid

from ..model.editor import Editor
from ..model.agency import Agency

editor_ns = Namespace("editor", description="Editor related operations")

editor_model = editor_ns.model('EditorModel', {
    'editor_id': fields.Integer(required=False,
            help='The unique identifier of a editor'),
    'name': fields.String(required=True,
            help='The name of the editor, e.g. John Smith'),
    'address': fields.String(required=False,
            help='The address of the editor, e.g. 1234 Elm St.'),
    'newspapers': fields.List(fields.String(required=True,
            help='A list of newspapers that the editor can care for'))
   })

@editor_ns.route("/")
class EditorAPI(Resource):
    @editor_ns.doc(editor_model, description = "List all editors in the agency")
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def get(self):
        pass
    @editor_ns.doc(editor_model, description ="Create a new editor")
    @editor_ns.expect(editor_model, validate=True)
    def post(self):
        pass

@editor_ns.route('/<int:editor_id>')
class editorID(Resource):

    @editor_ns.doc(editor_model, description="Get an editors information")
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def get(self, editor_id):
        search_result = Agency.get_instance().get_editor(editor_id)
        return search_result

    @editor_ns.doc(parser=editor_model, description="Update an editors information")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self, paper_id):
        # TODO: update editor
        pass

    @editor_ns.doc(editor_model, description="Delete an editor")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_editor(paper_id)
        if not targeted_paper:
            return jsonify(f"editor with ID {paper_id} was not found")
        Agency.get_instance().remove_editor(targeted_paper)
        return jsonify(f"editor with ID {paper_id} was removed")

@editor_ns.route("/<int:editor_id>")
class EditorID(Resource):
    @editor_ns.doc(editor_model, description ="Get an editor's information")
    def get(self, editor_id):
        pass
    @editor_ns.doc(editor_model, description ="Update an editor's information")
    @editor_ns.expect(editor_model, validate=True)
    def post(self, editor_id):
        pass
    @editor_ns.doc(editor_model, description ="Delete an editor")
    def delete(self, editor_id):
        pass

@editor_ns.route("/<int:editor_id>/issues")
class EditorIssues(Resource):
    @editor_ns.doc(editor_model,description = "Return a list of newspaper issues that the editor was responsible for")
    def get(self, editor_id):
        pass

