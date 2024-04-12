from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
import uuid

sub_ns = Namespace("subscriber", description="Subscriber related operations")

sub_model = sub_ns.model('SubscriberModel', {
    'sub_id': fields.Integer(required=False,
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
    @sub_ns.marshal_with(sub_model, envelope='editor')
    def get(self):
        pass

    @sub_ns.doc(sub_model, description ="Create a new subscriber")
    @sub_ns.expect(sub_model, validate=True)
    def post(self):
        pass

@sub_ns.route("/<int:subscriber_id>")
class subAPI(Resource):
    @sub_ns.doc(sub_model, description = "Get a subscriber's information")
    @sub_ns.marshal_with(sub_model, envelope='editor')
    def get(self):
        pass
    @sub_ns.doc(sub_model, description ="Update a subscriber's information")
    @sub_ns.expect(sub_model, validate=True)
    def post(self):
        pass
    @sub_ns.doc(sub_model, description = "Delete a subscriber")
    def delete(self):
        pass

@sub_ns.route("/<int:subscriber_id>/subscribe")
class subAPI(Resource):
    @sub_ns.doc(sub_model, description ="Subscribe a subscriber to a newspaper. (Transmit the newspaper ID as a parameter)")
    @sub_ns.expect(sub_model, validate=True)
    def post(self):
        pass

@sub_ns.route("/<int:subscriber_id>/stats")
class subAPI(Resource):
    @sub_ns.doc(sub_model, description = "Get the number of newspaper subscriptions and the monthly and annual cost, as well as the number of issues that the subscriber received for each paper.")
    @sub_ns.marshal_with(sub_model, envelope='editor')
    def get(self):
        pass

@sub_ns.route("/<int:subscriber_id>/missingissues")
class subAPI(Resource):
    @sub_ns.doc(sub_model, description = "Check if there are any undelivered issues of the subscribed newspapers.")
    @sub_ns.marshal_with(sub_model, envelope='editor')
    def get(self):
        pass
