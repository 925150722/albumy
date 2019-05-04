from flask import Blueprint


ajax_bp = Blueprint('ajax', __name__)


@ajax_bp.route('/notifications_count')
def notifications_count():
    return 'notifications_count'
