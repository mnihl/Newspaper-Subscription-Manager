from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
import uuid
from flask import request


from ..model.agency import Agency
from ..model.newspaper import Newspaper

newspaper_ns = Namespace("newspaper", description="Newspaper related operations")

paper_model = newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')
   })


@newspaper_ns.route('/')
class NewspaperAPI(Resource):
    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        paper_id = uuid.uuid4().int % 1000

        # create a new paper object and add it
        new_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        Agency.get_instance().add_newspaper(new_paper)

        # return the new paper
        return new_paper

    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()


@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):

    @newspaper_ns.doc(description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        return search_result

    @newspaper_ns.doc(parser=paper_model, description="Update a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        data = request.get_json()
        updated_paper = Agency.get_instance().update_newspaper(paper_id, data)
        return updated_paper

    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")

@newspaper_ns.route("/<int:paper_id>/issue")
class NewspaperIssue(Resource):
    @newspaper_ns.doc("List all issues of a specific newspaper")
    def get(self, paper_id):
        return Agency.get_instance().get_newspaper(paper_id).list_all_issues(paper_id)
    @newspaper_ns.doc("Create a new issue")
    def post(self, paper_id):
        Agency.get_instance().get_newspaper(paper_id).create_new_issue()
        return "New issue created"

@newspaper_ns.route("/<int:paper_id>/issue/<int:issue_id>")
class NewspaperIssueID(Resource):
    @newspaper_ns.doc("Get information of a newspaper issue")
    def get(self, paper_id, issue_id):
        return Agency.get_instance().get_newspaper(paper_id).get_issue(issue_id)

@newspaper_ns.route("/<int:paper_id>/issue/<int:issue_id>/release")
class NewspaperIssueRelease(Resource):
    @newspaper_ns.doc("Release an issue")
    def post(self, paper_id, issue_id):
        return Agency.get_instance().get_newspaper(paper_id).publish(issue_id)

@newspaper_ns.route("/<int:paper_id>/issue/<int:issue_id>/editor")
class NewspaperIssueEditor(Resource):
    @newspaper_ns.doc("Specify an editor for an issue (Transmit the editor ID as parameter)")
    def post(self, paper_id, issue_id, editor_id):
        for editor in Agency.get_instance().all_editors():
            if editor.editor_id == editor_id:
                Agency.get_instance().get_newspaper(paper_id).get_issue(issue_id).set_editor(editor)
                return True


@newspaper_ns.route("/<int:paper_id>/issue/<int:issue_id>/deliver")
class NewspaperIssueDeliver(Resource):
    @newspaper_ns.doc("'Send' an issue to a subscriber. This means there should be a record of the subscriber receiving")
    def post(self, issue_id, subscriber_id):
        return Agency.get_instance().deliver_issue(issue_id, subscriber_id)

@newspaper_ns.route("/<int:paper_id>/stats")
class NewspaperIssueStats(Resource):
    @newspaper_ns.doc("Return information about the specific newspaper (number of subscribers, monthly and annual revenue)")
    def get(self, paper_id):
        return Agency.get_instance().get_newspaper(paper_id).stats()


