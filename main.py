from flask import Flask
from flask import request
from flask import render_template

from database import User

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    title = 'Shopping Cart Facilito'
    return render_template('index.html', title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['correo']
        password = request.form['pass']
    
        if email and password:
            user = User.create(email=email, password=password)
    
    title = 'Nuevo registro'
    return render_template('register.html', title=title)


@app.route('/products', methods=['GET'])
def products():
    title = 'Listado de productos'
    
    return render_template('products/index.html')



@app.route('/products/create', methods=['GET'])
def create_product():
    title = 'Listado de productos'
    return render_template('products/create.html')




if __name__ == '__main__':
    app.run(debug=True)