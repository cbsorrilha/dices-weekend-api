from flask import request, render_template, make_response
from flask import current_app as app
from flask_restplus import abort, Api, Resource
from .schemas import ResultSchema, DiceSchema
from .services.dices import DiceService

api = Api(app)


@api.route('/dice')
class DiceController(Resource):
    def get(self):
        """List dices results."""
        schema = ResultSchema(many=True)
        limit = 4
        argLimit = request.args.get('limit')
        if (argLimit):
            limit = argLimit

        return {'results': schema.dump(DiceService.list(limit))}

    def post(self):
        """Create a dice result post."""
        request.get_json(force=True)
        name = request.json.get('name')
        modifier = request.json.get('modifier')
        mode = request.json.get('mode')
        dices = request.json.get('dices')

        schema = ResultSchema()
        dicesSchema = DiceSchema(many=True)

        try:
            new_result, individual_results = DiceService.create(
                name=name, modifier=modifier, mode=mode, dices=dices)
            return {'result': schema.dump(new_result), 'dices': dicesSchema.dump(individual_results)}
        except TypeError as err:
            abort(403, err)
