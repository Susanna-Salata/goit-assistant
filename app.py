import os.path

from flask import Flask, render_template, request, redirect
from models import Contact, Phone, Email, db_session

app = Flask(__name__, template_folder='templates')
app.debug = True
app.env = "development"


@app.route("/", strict_slashes=False)
def index():
    contacts = db_session.query(Contact).all()
    return render_template("index.html", contacts=contacts)


@app.route("/detail/<id>", strict_slashes=False)
def detail(id):
    contact = db_session.query(Contact).filter(Contact.id == id).first()
    return render_template("detail.html", contact=contact)


@app.route("/contact/", methods=["GET", "POST"], strict_slashes=False)
def add_contact():
    if request.method == "POST":
        name = request.form.get("name")
        birthday = request.form.get("birthday")
        phones = request.form.getlist("phones")
        emails = request.form.getlist("emails")
        phones_obj = []
        for phone in phones:
            phones_obj.append(db_session.query(Phone).filter(Phone.phone == phone).first())
        emails_obj = []
        for email in emails:
            emails_obj.append(db_session.query(Email).filter(Email.email == email).first())
        contact = Contact(name=name, birthday=birthday, phones=phones_obj, emails=emails_obj)
        db_session.add(contact)
        db_session.commit()
        return redirect("/")
    else:
        tags = db_session.query(Phone).all()

    return render_template("note.html", tags=tags)


@app.route("/phone/", methods=["GET", "POST"], strict_slashes=False)
def add_phone():
    if request.method == "POST":
        name = request.form.get("name")
        phone = Phone(phone=name)
        db_session.add(phone)
        db_session.commit()
        return redirect("/")

    return render_template("phone.html")


@app.route("/email/", methods=["GET", "POST"], strict_slashes=False)
def add_email():
    if request.method == "POST":
        name = request.form.get("name")
        email = Email(email=name)
        db_session.add(email)
        db_session.commit()
        return redirect("/")

    return render_template("email.html")

@app.route("/delete/<id>", strict_slashes=False)
def delete(id):
    db_session.query(Contact).filter(Contact.id == id).delete()
    db_session.commit()

    return redirect("/")


@app.route("/done/<id>", strict_slashes=False)
def done(id):
    db_session.query(Contact).filter(Contact.id == id).first().done = True
    db_session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run()
