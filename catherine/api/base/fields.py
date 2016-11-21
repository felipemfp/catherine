import arrow

from flask_restful import fields


class ArrowField(fields.Raw):
    def format(self, value):
        return arrow.get(value).isoformat()
