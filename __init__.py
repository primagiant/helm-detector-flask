from flask import Flask


def create_app():
    app = Flask(__name__)

    from .app.home import home as home_blueprint
    app.register_blueprint(home_blueprint, url_prefix='/')

    from .app.stream import stream as stream_blueprint
    app.register_blueprint(stream_blueprint, url_prefix='/stream')

    from .app.record import record as record_blueprint
    app.register_blueprint(record_blueprint, url_prefix='/record')

    from .app.upload import upload as upload_blueprint
    app.register_blueprint(upload_blueprint, url_prefix='/upload')

    from .app.about import about as about_blueprint
    app.register_blueprint(about_blueprint, url_prefix='/about')

    return app
