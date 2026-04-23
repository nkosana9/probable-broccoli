from flask import Blueprint
from ingestion import views

blueprint = Blueprint("main", __name__)

blueprint.add_url_rule("/accounts/bulk-ingestion", view_func=views.bulk_account_ingestion, methods=["POST"])
blueprint.add_url_rule("/accounts/<string:account_id>/summary", view_func=views.account_summary, methods=["GET"])
