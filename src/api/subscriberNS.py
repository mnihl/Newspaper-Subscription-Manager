from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

sub_ns = Namespace("subscriber", description="Subscriber related operations")