from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reports', description='Report operations')

report_model = api.model('Report', {
    'comment': fields.String(required=True, description='Comment of the report')
})

@api.route('/')
class ReportList(Resource):
    @api.expect(report_model)
    @api.response(201, 'Report successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new report"""
        report_data = api.payload or {}
        comment = report_data.get('comment', '').strip()
        
        if not comment:
            return {'error': 'Invalid input data'}, 400
        new_report = facade.create_report({'comment': comment})

        if not new_report:
            return {'error': 'Invalid input data'}, 400
        return new_report.to_dict(), 201

    @api.response(200, 'List of reports retrieved successfully')
    def get(self):
        """Retrieve a list of all reports"""
        reports = facade.get_all_reports()
        return [report.to_dict() for report in reports]

@api.route('/<string:report_id>')
class ReportResource(Resource):
    @api.response(200, 'Report details retrieved successfully')
    @api.response(404, 'Report not found')
    def get(self, report_id):
        """Get report details by ID"""
        report = facade.get_report(report_id)
        if not report:
            return {'error': 'Report not found'}, 404
        return report.to_dict(), 200

    @api.expect(report_model)
    @api.response(200, 'Report updated successfully')
    @api.response(404, 'Report not found')
    @api.response(400, 'Invalid input data')
    def put(self, report_id):
        """Update an report's information"""
        report_data = api.payload or {}
        comment = report_data.get('comment', '').strip()
        
        if not comment:
            return {'error': 'Invalid input data'}, 400

        updated_report = facade.update_report(report_id, {'comment': comment})
        if not updated_report:
            return {'error': 'Report not found'}, 404
        
        return updated_report.to_dict(), 200

    @api.response(200, 'Report deleted successfully')
    @api.response(404, 'Report not found')
    def delete(self, report_id):
        report = facade.delete_report(report_id)
        if not report:
            return {'error': 'Report not found'}, 404
        return {'message': 'Report deleted'}, 200
