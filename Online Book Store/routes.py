from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp
from werkzeug.security import generate_password_hash, check_password_hash
from db.database import session_scope
from db.models import User, Book, CartItem, Review, Order, OrderItem
from datetime import datetime

main_blueprint = Blueprint("main", __name__)


class LoginForm(FlaskForm):
    identity = StringField(
        "Email / Username / Phone", validators=[InputRequired(), Length(min=3, max=120)]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=36)]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=36)]
    )


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=100)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    phone_number = StringField(
        "Phone number", validators=[InputRequired(), Regexp(r"^\+?[\d\s\-\(\)]{7,15}$")]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=36)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )


@main_blueprint.route("/")
@main_blueprint.route("/home")
def main_route():
    return render_template("home.html", user_auth=current_user.is_authenticated)


@main_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        with session_scope() as session:
            user_email = session.query(User).filter_by(email=form.email.data).first()
            user_phone = (
                session.query(User)
                .filter_by(phone_number=form.phone_number.data)
                .first()
            )
            if user_email:
                flash("User with this email already exist!", category="danger")
                return redirect(url_for("main.register", form=form))
            elif user_phone:
                flash("User with this phone already exist!", category="danger")
                return redirect(url_for("main.register", form=form))
            user = User(
                name=form.username.data,
                email=form.email.data,
                phone_number=form.phone_number.data,
                password_hash=generate_password_hash(form.password.data),
            )
            session.add(user)
            return redirect(url_for("main.login"))
    elif form.errors:
        flash(message=form.errors, category="danger")
    return render_template("register.html", form=form)


@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with session_scope() as session:
            identity = form.identity.data
            if "@" in identity and "." in identity:
                user = session.query(User).filter_by(email=identity).first()
            else:
                user = session.query(User).filter_by(phone_number=identity).first()
            if user is None:
                user = session.query(User).filter_by(name=identity).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                print(user.id)
                return redirect(
                    url_for(
                        "main.verify_code", phone=user.phone_number, user_id=user.id
                    )
                )
        flash("Login failed", "danger")
    return render_template("login.html", form=form)


@main_blueprint.route("/verify_code", methods=["GET", "POST"])
def verify_code():
    phone = request.args.get("phone")
    print(request.form.get("code") == "1234")
    
    if request.form.get("code") == "1234":
        with session_scope() as session:
            user = session.query(User).filter_by(id=request.form.get("user_id")).first()
            login_user(user)
            return redirect(url_for("main.main_route"))
    else:
        if phone == None:
            flash("Неверный код", "danger")  
        user_id = request.args.get("user_id") or request.form.get("user_id")
        return render_template("code.html", phone=phone,user_id=user_id)


@main_blueprint.route("/logout_confirm")
def logout_confirm():
    return render_template("logout_confirm.html")


@main_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("main.main_route"))


@main_blueprint.route("/genre/<genre_name>")
def genre(genre_name):
    with session_scope() as session:
        books = session.query(Book).filter_by(genre=genre_name)
    return render_template(
        "genre.html",
        genre=genre_name,
        books=books,
        user_auth=current_user.is_authenticated,
    )


@main_blueprint.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    if request.method == "POST":
        genre = request.form.get("genre")
        book_id = request.form.get("book_id")
        with session_scope() as session:
            book = session.query(Book).filter_by(id=book_id).first()
            book_title = book.title
            cart_item_exist = session.query(CartItem).filter_by(book_id=book.id).first()
            if cart_item_exist:
                cart_item_exist.count += int(request.form.get("count"))
                session.commit()
            else:
                cart_item = CartItem(user_id=current_user.id, book_id=book_id, count=1)
                session.add(cart_item)
        flash(f"Товар добавлен в корзину", category=f"book_{book_id}")
        if genre:
            return redirect(url_for("main.genre", genre_name=genre))
        else:
            return redirect(url_for("main.book", book_id=request.form.get("book_id")))

    with session_scope() as session:
        cart_items = (
            session.query(CartItem).filter_by(user_id=current_user.id).subquery()
        )
        books = session.query(
            Book.id,
            Book.year,
            Book.title,
            Book.author,
            (Book.price * cart_items.c.count).label("price"),
            cart_items.c.count,
        ).join(cart_items, Book.id == cart_items.c.book_id)
        return render_template(
            "cart.html", books=books, user_auth=current_user.is_authenticated
        )


@main_blueprint.route("/delete/<book_id>")
def delete_item(book_id):
    with session_scope() as session:
        book = session.query(CartItem).filter_by(book_id=book_id).first()
        if book:
            session.delete(book)
            session.commit()
    return redirect(url_for("main.cart"))


@main_blueprint.route("/book/<book_id>")
def book(book_id):
    with session_scope() as session:
        book = session.query(Book).filter_by(id=book_id).first()
        book = book.to_dict()
        reviews_users = (
            session.query(User.id, User.name, Review.review, Review.rating)
            .join(Review, User.id == Review.review_author_id)
            .filter(Review.review_book_id == book_id)
            .all()
        )
        return render_template(
            "book.html",
            user_auth=current_user.is_authenticated,
            book=book,
            reviews=reviews_users,
        )


@main_blueprint.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "POST":
        with session_scope() as session:
            new_review = Review(
                review=request.form.get("review_text"),
                review_author_id=current_user.id,
                review_book_id=request.form.get("book_id"),
                rating=request.form.get("rating"),
            )
            session.add(new_review)
        return redirect(url_for("main.book", book_id=request.form.get("book_id")))


@main_blueprint.route("/new_order", methods=["GET", "POST"])
def new_order():
    selected_books = request.form.getlist("selected_books")
    selected_books_ids = [int(book_id) for book_id in selected_books]
    with session_scope() as session:
        books = (
            session.query(
                Book.id,
                Book.year,
                Book.title,
                Book.author,
                (Book.price * CartItem.count).label("price"),
                CartItem.count,
            )
            .join(CartItem, Book.id == CartItem.book_id)
            .filter(Book.id.in_(selected_books_ids))
            .all()
        )
        total_price = sum(book.price for book in books)
        del_cart = (
            session.query(CartItem)
            .filter(
                CartItem.book_id.in_(selected_books_ids),
                CartItem.user_id == current_user.id,
            )
            .all()
        )
        for item in del_cart:
            session.delete(item)
        return render_template("order.html", books=books, total_price=total_price)


@main_blueprint.route("/create_order", methods=["GET", "POST"])
def create_order():
    selected_books = request.form.getlist("selected_books")
    selected_books_ids = [int(book_id) for book_id in selected_books]
    with session_scope() as session:
        past_orders = (
            session.query(Order)
            .filter(
                Order.user_id == current_user.id,
            )
            .all()
        )
        for order in past_orders:
            order.order_status = "выполнен"

        new_order = Order(
            user_id=current_user.id,
            order_date=datetime.now(),
            order_status="new",
            address=request.form.get("address") or "самовывоз",
        )
        session.add(new_order)
        books = session.query(Book).filter(Book.id.in_(selected_books_ids)).all()
        prices = {book.id: book.price for book in books}

        for book_id in selected_books_ids:
            count = int(request.form.get(f"count_{book_id}", 1))
            order_item = OrderItem(
                order_id=new_order.id,
                book_id=book_id,
                count=count,
                price=prices[book_id] * count,
            )
            session.add(order_item)
    return redirect(url_for("main.main_route"))


@main_blueprint.route("/orders")
def orders():
    with session_scope() as session:
        orders = session.query(Order).filter(Order.user_id == current_user.id)
    return render_template(
        "user_orders.html", orders=orders, user_auth=current_user.is_authenticated
    )


@main_blueprint.route("/search")
def search():
    query = request.args.get("search")
    with session_scope() as session:
        if query:
            book = session.query(Book).filter(Book.title.ilike(f"%{query}%")).first()
            return redirect(url_for("main.book", book_id=book.id))
        else:
            return redirect(url_for("main.main_route"))
