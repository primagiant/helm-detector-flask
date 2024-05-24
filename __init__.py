from flask import Flask


def create_app():
    app = Flask(__name__)

    from .app.stream import stream as stream_blueprint
    app.register_blueprint(stream_blueprint, url_prefix='/')

    from .app.record import record as record_blueprint
    app.register_blueprint(record_blueprint, url_prefix='/record')

    from .app.about import about as about_blueprint
    app.register_blueprint(about_blueprint, url_prefix='/about')

    return app
