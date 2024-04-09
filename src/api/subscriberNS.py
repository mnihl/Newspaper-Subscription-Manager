from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

sub_ns = Namespace("subscriber", description="Subscriber related operations")

from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

sub_ns = Namespace("subscriber", description="Subscriber related operations")

@sub_ns.route("/")
class subAPI(Resource):
    @sub_ns.doc("List all subs in the agency")
    def get(self):
        pass
    @sub_ns.doc("Create a new subscriber")
    def post(self):
        pass

@sub_ns.route("/<int:subscriber_id>")
class subAPI(Resource):
    @sub_ns.doc("Get a subscriber's information")
    def get(self):
        pass
    @sub_ns.doc("Update a subscriber's information")
    def post(self):
        pass
    @sub_ns.doc("Delete a subscriber")
    def delete(self):
        pass

@sub_ns.route("/<int:subscriber_id>/subscribe")
class subAPI(Resource):
    @sub_ns.doc("Subscribe a subscriber to a newspaper. (Transmit the newspaper ID as a parameter)")
    def post(self):
        pass

@sub_ns.route("/<int:subscriber_id>/stats")
class subAPI(Resource):
    @sub_ns.doc("Get the number of newspaper subscriptions and the monthly and annual cost, as well as the number of issues that the subscriber received for each paper.")
    def get(self):
        pass

@sub_ns.route("/<int:subscriber_id>/missingissues")
class subAPI(Resource):
    @sub_ns.doc("Check if there are any undelivered issues of the subscribed newspapers.")
    def get(self):
        pass
