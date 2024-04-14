from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
import uuid
from flask import request


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

issue_model = editor_ns.model('IssueModel', {
    'pubdate': fields.DateTime(required=True,
            help='The date of the issue'),
    'pages': fields.Integer(required=True,
            help='The pages of the issue'),
    'issue_id': fields.Integer(required=False,
            help='The unique identifier of an issue'),
   })

@editor_ns.route("/")
class EditorAPI(Resource):
    @editor_ns.doc(editor_model, description = "List all editors in the agency")
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def get(self):
        return Agency.get_instance().all_editors()
    @editor_ns.doc(editor_model, description ="Create a new editor")
    @editor_ns.expect(editor_model, validate=True)
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def post(self):
        editor_id = uuid.uuid4().int % 1000
        new_editor = Editor(editor_id=editor_id,
                            name=editor_ns.payload['name'],
                            address=editor_ns.payload['address'])
        Agency.get_instance().new_editor(new_editor)
        return new_editor

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
    def post(self, editor_id):
        data = request.get_json()
        updated_editor = Agency.get_instance().update_editor(editor_id, data["name"], data["address"])
        return updated_editor

    @editor_ns.doc(editor_model, description="Delete an editor")
    def delete(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f"editor with ID {editor_id} was not found")
        Agency.get_instance().delete_editor(targeted_editor)
        return jsonify(f"editor with ID {editor_id} was removed")

@editor_ns.route("/<int:editor_id>/issues")
class EditorIssue(Resource):
    @editor_ns.doc(editor_model, description ="Get an editor's information")
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def get(self, editor_id):
        return Agency.get_instance().editor_issues(editor_id)

