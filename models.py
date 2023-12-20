from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Professor(db.Model):
    __tablename__ = "professors"

    id = db.Column(db.Integer, primary_key=True, index=True)
    first_name = db.Column(db.String, index=True)
    last_name = db.Column(db.String, index=True)
    courses = db.relationship("Course", back_populates="professor")

class Classroom(db.Model):
    __tablename__ = "classrooms"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, index=True)
    capacity = db.Column(db.Integer)
    courses = db.relationship("Course", back_populates="classroom")

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String, index=True)
    description = db.Column(db.String)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professors.id'))
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'))
    professor = db.relationship("Professor", back_populates="courses")
    classroom = db.relationship("Classroom", back_populates="courses")
