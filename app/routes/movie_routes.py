from flask import Blueprint, jsonify, make_response, request
from app.models.movie import Movie
from app import db

movies_bp = Blueprint("movies", __name__, url_prefix="/movies")
