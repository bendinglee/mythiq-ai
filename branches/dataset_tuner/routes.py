from flask import Blueprint, request, jsonify
from branches.dataset_tuner.dataset_parser import parse_dataset
from branches.dataset_tuner.dataset_validator import validate_schema
from branches.dataset_tuner.embed_dataset import embed_entries
from branches.dataset_tuner.tuning_log import log_tuning_event

dataset_api = Blueprint("dataset_tuner", __name__)

@dataset_api.route("/api/import-dataset", methods=["POST"])
def import_dataset():
    try:
        data = request.get_json()
        if not data:
            return jsonify({ "success": False, "error": "Missing dataset input." }), 400

        is_valid, schema_report = validate_schema(data)
        if not is_valid:
            return jsonify({ "success": False, "error": schema_report }), 422

        entries = parse_dataset(data)
        embedded = embed_entries(entries)
        log_tuning_event(entries)

        return jsonify({ "success": True, "count": len(entries), "embedded": embedded })

    except Exception as e:
        return jsonify({ "success": False, "error": str(e) }), 500
