
from app import app
from views import views

app.register_blueprint(views)

if __name__ == '__main__':
	app.run()