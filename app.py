from flask import Flask, render_template, request, redirect
from models import Note, Tag, db_session, Contact, Phone, Email
from validate import convert_to_date, valid_phone_number, valid_email

from datetime import datetime

app = Flask(__name__)
app.debug = True
# app.env = "development"


@app.route("/", strict_slashes=False)
def index():
    notes = db_session.query(Note).all()
    contacts = db_session.query(Contact).all()
    return render_template("index.html", notes=notes, contacts=contacts)


@app.route("/detail/<id>", strict_slashes=False)
def detail(id):
    note = db_session.query(Note).filter(Note.id == id).first()
    return render_template("detail.html", note=note)


@app.route("/contact_detail/<id>", strict_slashes=False)
def contact_detail(id):
    contact = db_session.query(Contact).filter(Contact.id == id).first()
    date_of_birth = contact.date_of_birth.strftime('%B %d') if contact.date_of_birth else "unknown"
    phone_numbers = db_session.query(Phone).filter(Phone.contact_id == id)
    phone_numbers = [x.number for x in phone_numbers] if phone_numbers else None
    phone_number = phone_numbers[0] if phone_numbers else "unknown"
    emails = db_session.query(Email).filter(Email.contact_id == id)
    emails = [x.mail for x in emails] if emails else None
    email_address = emails[0] if emails else "unknown"
    return render_template("contact_detail.html", contact=contact, date_of_birth=date_of_birth,
                           phone_number=phone_number, email_address=email_address)


@app.route("/note/", methods=["GET", "POST"], strict_slashes=False)
def add_note():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        tags = request.form.getlist("tags")
        tags_obj = []
        for tag in tags:
            tags_obj.append(db_session.query(Tag).filter(Tag.name == tag).first())
        note = Note(name=name, description=description, tags=tags_obj)
        db_session.add(note)
        db_session.commit()
        return redirect("/")
    else:
        tags = db_session.query(Tag).all()

    return render_template("note.html", tags=tags)


@app.route("/tag/", methods=["GET", "POST"], strict_slashes=False)
def add_tag():
    if request.method == "POST":
        name = request.form.get("name")
        tags = db_session.query(Tag).all()
        known_tags = [x.name for x in tags]
        if name not in known_tags:
            tag = Tag(name=name)
            db_session.add(tag)
            db_session.commit()
            return redirect("/")
    return render_template("tag.html")


@app.route("/contact/", methods=["GET", "POST"], strict_slashes=False)
def add_contact():
    if request.method == "POST":
        contacts = db_session.query(Contact).all()
        known_names = [x.fullname for x in contacts]
        name = request.form.get("name")
        birthday = request.form.get("birthday")
        birthday = convert_to_date(birthday)

        phone = request.form.get("number")
        phone = valid_phone_number(phone)
        email = request.form.get("email")
        email = valid_email(email)

        if name not in known_names:
            contact = Contact(fullname=name)
            if birthday is not None:
                contact.date_of_birth = birthday
            db_session.add(contact)
            db_session.commit()
            print(f"contact.id = {contact.id}")
            if phone is not None:
                new_phone = Phone(number=phone, contact_id=contact.id)
                db_session.add(new_phone)
            if email is not None:
                new_email = Email(mail=email, contact_id=contact.id)
                db_session.add(new_email)
            db_session.commit()

            return redirect("/")
    return render_template("contact.html")


@app.route("/delete/<id>", strict_slashes=False)
def delete(id):
    db_session.query(Note).filter(Note.id == id).delete()
    db_session.commit()
    return redirect("/")


@app.route("/delete_contact/<id>", strict_slashes=False)
def delete_contact(id):
    db_session.query(Contact).filter(Contact.id == id).delete()
    db_session.query(Phone).filter(Phone.contact_id == id).delete()
    db_session.query(Email).filter(Email.contact_id == id).delete()
    db_session.commit()
    return redirect("/")


@app.route("/edit_contact/<id>", methods=["GET", "POST"], strict_slashes=False)
def edit_contact(id):
    if request.method == "POST":
        name = request.form.get("name")
        contacts = db_session.query(Contact).all()
        # known_names = [x.fullname for x in contacts]
        name = request.form.get("name")
        birthday = request.form.get("birthday")
        birthday = convert_to_date(birthday)

        phone = request.form.get("number")
        phone = valid_phone_number(phone)
        email = request.form.get("email")
        email = valid_email(email)
        print("hi1")
        for x in contacts:
            if (int(x.id) != int(id)) and (str(x.fullname) == str(name)):
                print("name exists")
                return redirect("/")
        print("hi2")
        contact = db_session.query(Contact).filter(Contact.id == id).first()
        contact.fullname = name
        db_session.commit()
        if birthday is not None:
            contact.date_of_birth = birthday
            db_session.commit()
        if phone is not None:
            print("phone")
            old_phone = db_session.query(Phone).filter(Phone.contact_id == id).first()
            print(old_phone.number)
            old_phone.number = phone
            db_session.commit()
        if email is not None:
            old_email = db_session.query(Email).filter(Email.contact_id == id).first()
            print("hi")
            print(old_email, old_email.mail)
            old_email.mail = email
            db_session.commit()
        return redirect("/")
    contact = db_session.query(Contact).filter(Contact.id == id).first()
    date_of_birth = contact.date_of_birth.strftime('%B %d') if contact.date_of_birth else ""
    phone_numbers = db_session.query(Phone).filter(Phone.contact_id == id)
    phone_numbers = [x.number for x in phone_numbers] if phone_numbers else None
    phone_number = phone_numbers[0] if phone_numbers else ""
    emails = db_session.query(Email).filter(Email.contact_id == id)
    emails = [x.mail for x in emails] if emails else None
    email_address = emails[0] if emails else ""
    return render_template("edit_contact.html", contact=contact, date_of_birth=date_of_birth,
                           phone_number=phone_number, email_address=email_address)


@app.route("/done/<id>", strict_slashes=False)
def done(id):
    db_session.query(Note).filter(Note.id == id).first().done = True
    db_session.commit()
    return redirect("/")


if __name__ == "__main__":
    # app.run()
    app.run(host="localhost", port=8000, debug=True)
