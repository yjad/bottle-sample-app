import bottle
import routes
from icecream import install


# https://github.com/kurocode25/bottle-sample-app.git

app = routes.app
install()

if __name__ == '__main__':
    # this setting is running for development.
    # bottle.run(app=app, host='0.0.0.0',port=8080, reloader=True, debug=True)
    bottle.run(app=app, host='localhost',port=8080, reloader=True, debug=True)
