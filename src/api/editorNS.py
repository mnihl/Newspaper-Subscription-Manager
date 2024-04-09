from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.editor import Editor
from ..model.agency import Agency

editor_ns = Namespace("editor", description="Editor related operations")

@editor_ns.route("/")
class EditorAPI(Resource):
    @editor_ns.doc("List all editors in the agency")
    def get(self):
        pass
    @editor_ns.doc("Create a new editor")
    def post(self):
        pass

@editor_ns.route('/<int:editor_id>')
class editorID(Resource):

    @editor_ns.doc(description="Get an editors information")
    # @editor_ns.marshal_with(paper_model, envelope='editor')
    def get(self, editor_id):
        search_result = Agency.get_instance().get_editor(editor_id)
        return search_result

    # @editor_ns.doc(parser=paper_model, description="Update an editors information")
    # @editor_ns.expect(paper_model, validate=True)
    # @editor_ns.marshal_with(paper_model, envelope='editor')
    def post(self, paper_id):
        # TODO: update editor
        pass

    @editor_ns.doc(description="Delete an editor")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_editor(paper_id)
        if not targeted_paper:
            return jsonify(f"editor with ID {paper_id} was not found")
        Agency.get_instance().remove_editor(targeted_paper)
        return jsonify(f"editor with ID {paper_id} was removed")

@editor_ns.route("/<int:editor_id>")
class EditorID(Resource):
    @editor_ns.doc("Get an editor's information")
    def get(self, editor_id):
        pass
    @editor_ns.doc("Update an editor's information")
    def post(self, editor_id):
        pass
    @editor_ns.doc("Delete an editor")
    def delete(self, editor_id):
        pass

@editor_ns.route("/<int:editor_id>/issues")
class EditorIssues(Resource):
    @editor_ns.doc("Return a list of newspaper issues that the editor was responsible for")
    def get(self, editor_id):
        pass

