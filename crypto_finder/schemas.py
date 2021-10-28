"""
Schemas for request validation
"""
from marshmallow import fields, Schema, validate


class HistoryRequestSchema(Schema):
    page = fields.Int(
        validate=validate.Range(min=1),
        required=False,
    )
