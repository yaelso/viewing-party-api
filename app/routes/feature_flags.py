from flask import Blueprint, jsonify, current_app

feature_flags = Blueprint('feature_flags', __name__)

@feature_flags.route('/feature-flags', methods=['GET'])
def get_feature_flags():
    flags = current_app.config['FEATURE_FLAGS']
    return jsonify(flags)
