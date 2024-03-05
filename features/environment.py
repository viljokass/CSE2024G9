from routes import create_app


def before_feature(context, feature):
    app = create_app()
    app.testing = True
    context.client = app.test_client()