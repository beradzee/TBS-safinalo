from flask import Flask, render_template, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from os import path

from forms import AddTourForm, RegForm, EditTourForm, LoginForm
from ext import app, db
from models import Tour, TourCategory, User

tours = {}

reg_p = "1"


@app.route("/")
def index():
    tours = Tour.query.all()
    return render_template("index.html", tours=tours)


@app.route("/search/<string:city>")
def search(city):
    tours = Tour.query.filter(Tour.city.ilike(f"%{city}%")).all()
    return render_template("search.html", tours=tours)


@app.route("/sign_in", methods=["POST", "GET"])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():

        existing_user = User.query.filter_by(username=form.username.data).first()


        if existing_user:
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
            return redirect("/")
        else:
            flash('მომსმარებელი არ არსებობს, გთხოვთ შეიყვანეთ სხვა სახელი.', 'error')

    return render_template("sign_in.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/reg", methods=["POST", "GET"])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()

        if existing_user:
            flash('მომსმარებელი უკვე არსებობს, გთხოვთ შეიყვანეთ სხვა სახელი.', 'error')
        else:
            new_user = User(username=form.username.data, password=form.password.data, role="normal")
            new_user.create()
            return redirect("sign_in")

    return render_template("reg.html", form=form, reg_p=reg_p)


@app.route("/tour/<int:tour_id>")
def tour(tour_id):
    chosen_tour = Tour.query.get(tour_id)
    if not chosen_tour:
        return render_template("404.html")

    return render_template("tour.html", tours=chosen_tour)


@app.route("/edit_tour/<int:tour_id>", methods=["POST", "GET"])
@login_required
def edit_tour(tour_id):
    if current_user.role != "admin":
        return redirect("sign_in")

    chosen_tour = Tour.query.get(tour_id)

    if not chosen_tour:
        return render_template("404.html")

    form = EditTourForm(city=chosen_tour.city, country=chosen_tour.country, price=chosen_tour.price,
                        img=chosen_tour.img)
    if form.validate_on_submit():
        chosen_tour.city = form.city.data
        chosen_tour.country = form.country.data
        chosen_tour.price = form.price.data

        if form.img.data and hasattr(form.img.data, 'filename'):
            chosen_tour.img = form.img.data.filename
            file_directory = path.join(app.root_path, "static", form.img.data.filename)
            form.img.data.save(file_directory)
        else:
            if chosen_tour.img:
                chosen_tour.img = chosen_tour.img

        chosen_tour.save()

    return render_template("add_tour.html", form=form, tour=tour)


@app.route("/add_tour", methods=["POST", "GET"])
@login_required
def add_tour():
    if current_user.role != "admin":
        return redirect("sign_in")

    form = AddTourForm()
    if form.validate_on_submit():
        countryy = form.country.data

        category = TourCategory.query.filter_by(
            country="foreign_country" if countryy == "საქართველო" else "georgia").first()

        new_tour = Tour(city=form.city.data, country=countryy, price=form.price.data, img=form.img.data.filename,
                        category_c=category)

        db.session.add(new_tour)
        db.session.commit()

        file_directory = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_directory)

        return redirect("/")

    return render_template("add_tour.html", form=form)

@app.route("/cart")
def cart():
    tours = Tour.query.all()
    return render_template("cart", tours=tours)


@app.route("/delete_tour/<int:tour_id>")
@login_required
def delete_tour(tour_id):
    if current_user.role != "admin":
        return redirect("sign_in")

    chosen_tour = Tour.query.get(tour_id)
    if not chosen_tour:
        return render_template("404.html")

    chosen_tour.delete()

    return redirect("/")


@app.route("/category/<int:category_id>")
def category(category_id):
    category_c = TourCategory.query.get(category_id)
    if not category_c:
        return render_template("404.html")

    tours = Tour.query.filter_by(category_c=category_c).all()
    return render_template("category.html", tours=tours)

# "id": len(tours["foreign_country"]) + len(tours["georgia"])

# tours[countries].append(new_tour)


# "foreign_country": [
#     #     {"country":"ესპანეთი", "city":"ბარსელონა", "price":"500", "img":"image2.jpg", "img2":"image1.jpg", "img3":"image3.jpg", "id": 0},
#
#     #     {"country":"ამსტერდამა და ბრიუსელი", "city":"ბრიუსელი, ამსტერდამი", "price":"800", "img":"image1.jpg", "id": 1},
#
#     #     {"country":"პრაღა", "city":"კარლოვი-ბარი", "price":"1100", "img":"praga1.jpg", "img2":"praga2.jpg", "img3":"praga3.jpg", "id": 2},
#
#     #     {"country":"ამსტერდამა და ბრიუსელი", "city":"ბრიუსელი, ამსტერდამი", "price":"800", "img":"image2.jpg", "id": 3},
#
#     # ],
#
#     # "georgia": [
#     #     {"country":"საქართველო", "city":"ზესტაფონი", "price":"50", "img":"zestafoni.jpg", "id": 4},
#
#     #     {"country":"საქართველო", "city":"ზესტაფონი", "price":"50", "img":"zestafoni.jpg", "id": 5},
#
#     #     {"country":"საქართველო", "city":"ზესტაფონი", "price":"50", "img":"zestafoni.jpg", "id": 6},
#
#     #     {"country":"საქართველო", "city":"ზესტაფონი", "price":"50", "img":"zestafoni.jpg", "id": 7},
#     # ],
