from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
import uuid
from ..model.agency import Agency
from ..model.subscriber import Subscriber
from flask import request

sub_ns = Namespace("subscriber", description="Subscriber related operations")

sub_model = sub_ns.model('SubscriberModel', {
    'subscriber_id': fields.Integer(required=False,
            help='The unique identifier of a subscriber'),
    'name': fields.String(required=True,
            help='The name of the subscriber, e.g. John Smith'),
    'address': fields.String(required=False,
            help='The address of the subscriber, e.g. 1234 Elm St.'),
    'newspapers': fields.List(fields.String(required=True,
            help='A list of the newspapers the subscriber is subscribed to'))
   })

@sub_ns.route("/")
class subAPI(Resource):
    @sub_ns.doc(sub_model, description = "List all subscribers in the agency")
    @sub_ns.marshal_with(sub_model, envelope='subscriber')
    def get(self):
        return Agency.get_instance().get_subscribers()

    @sub_ns.doc(sub_model, description ="Create a new subscriber")
    @sub_ns.expect(sub_model, validate=True)
    @sub_ns.marshal_with(sub_model, envelope='subscriber')
    def post(self):
        new_sub = Subscriber(
            subscriber_id=uuid.uuid4().int % 1000,
            name=sub_ns.payload['name'],
            address=sub_ns.payload['address']
        )
        Agency.get_instance().new_subscriber(new_sub)
        return new_sub

@sub_ns.route("/<int:subscriber_id>")
class subID(Resource):
    @sub_ns.doc(sub_model, description = "Get a subscriber's information")
    @sub_ns.marshal_with(sub_model, envelope='subscriber')
    def get(self, subscriber_id):
        return Agency.get_instance().get_subscriber(subscriber_id)
    @sub_ns.doc(sub_model, description ="Update a subscriber's information")
    @sub_ns.expect(sub_model, validate=True)
    @sub_ns.marshal_with(sub_model, envelope='subscriber')
    def post(self, subscriber_id):
        data = request.get_json()
        updated_sub = Agency.get_instance().subscriber_update(subscriber_id, data["name"], data["address"])
        return updated_sub
    @sub_ns.doc(sub_model, description = "Delete a subscriber")
    def delete(self, subscriber_id):
        target_sub = Agency.get_instance().get_subscriber(subscriber_id)
        if not target_sub:
            return jsonify(f"sub with ID {subscriber_id} was not found")
        Agency.get_instance().delete_subscriber(target_sub)
        return jsonify(f"sub with ID {subscriber_id} was removed")

@sub_ns.route("/<int:subscriber_id>/subscribe")
class subSub(Resource):
    @sub_ns.doc(sub_model, description ="Subscribe a subscriber to a newspaper. (Transmit the newspaper ID as a parameter)")
    @sub_ns.expect(sub_model, validate=True)
    @sub_ns.marshal_with(sub_model, envelope='subscriber')
    def post(self, newspaper_id, subscriber_id):
        return Agency.get_instance().subscribe(newspaper_id, subscriber_id)

@sub_ns.route("/<int:subscriber_id>/stats")
class subStats(Resource):
    @sub_ns.doc(sub_model, description = "Get the number of newspaper subscriptions and the monthly and annual cost, as well as the number of issues that the subscriber received for each paper.")
    @sub_ns.marshal_with(sub_model, envelope='subscriber')
    def get(self, subscriber_id):
        return Agency.get_instance().get_subscriber(subscriber_id).stats()

@sub_ns.route("/<int:subscriber_id>/missingissues")
class subIssues(Resource):
    @sub_ns.doc(sub_model, description = "Check if there are any undelivered issues of the subscribed newspapers.")
    @sub_ns.marshal_with(sub_model, envelope='subscriber')
    def get(self, subscriber_id):
        return Agency.get_instance().get_subscriber(subscriber_id).check_undelivered()
