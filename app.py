from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from extensions import db, login_manager
from models import Product, User
from forms import ProductForm, LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"   # redirect if not logged in

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ----------------- Home -----------------
@app.route("/")
def home():
    products = Product.query.all()
    return render_template("home.html", products=products)


# ----------------- Register -----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already exists", "danger")
            return redirect(url_for("register"))
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


# ----------------- Login -----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)


# ----------------- Logout -----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


# ----------------- Add Product -----------------
@app.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data
        )
        db.session.add(product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for("home"))
    return render_template("add_product.html", form=form)


# ----------------- Edit Product -----------------
@app.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for("home"))
    return render_template("edit_product.html", form=form, product=product)


# ----------------- Delete Product -----------------
@app.route("/products/delete/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "danger")
    return redirect(url_for("home"))


# ----------------- Run -----------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
