from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validates_name(self, key, name):
        names = db.seesion.query(Author.name).all()
        if not name:
            raise ValueError('Name field is required')
        elif name in names:
            raise ValueError('Name must be unique')
        return name

    @validates('phone_number')
    def validates_phone_number(self, key, number):
        if len(number) != 10:
            raise ValueError("the phone number is not a 10 digit number")
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validates_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        for phrase in clickbait:
            if phrase in title:
                return title
        raise ValueError('no clickbait found')

    @validates('content', 'summary')
    def validates_content(self, key, content):
        if key == 'content':
            if len(content) <= 250:
                raise ValueError(
                    "The content is less than or = 250 characters")
        if key == "summary":
            if len(content) >= 250:
                raise ValueError("The content is more than 250 characters")
        return content

    @validates('category')
    def validates_category(self, key, category):
        if category.lower() != "fiction" and category.lower() != "non-fiction":
            raise ValueError("The category is invalid")
        else:
            return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
