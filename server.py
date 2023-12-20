from flask import Flask, jsonify, request
from models import db, Professor, Classroom, Course
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.cli.command("initdb")
def init_db():
    db.create_all()
    print("Database initialized.")



@app.route("/api/planify_course", methods=["POST"])
def planify_course():
    data = request.get_json()

    course_title = data.get("title")
    course_description = data.get("description")
    professor_name = data.get("professor_name")
    classroom_name = data.get("classroom_name")
    start_time_str = data.get("start_time")
    end_time_str = data.get("end_time")

    # Parse the date and time strings into datetime objects
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")

    professor = Professor.query.filter_by(first_name=professor_name).first()
    if professor is None:
        professor = Professor(first_name=professor_name)
        db.session.add(professor)

    classroom = Classroom.query.filter_by(name=classroom_name).first()
    if classroom is None:
        classroom = Classroom(name=classroom_name, capacity=30)
        db.session.add(classroom)

    # Check for course scheduling conflicts
    course_conflict = Course.query.filter(
        Course.start_time <= end_time,
        Course.end_time >= start_time,
        Course.classroom == classroom,
        Course.professor == professor
    ).first()

    if course_conflict:
        return jsonify({"error": "Course scheduling conflict"}), 400

    course = Course(
        title=course_title,
        description=course_description,
        start_time=start_time,
        end_time=end_time,
        professor=professor,
        classroom=classroom,
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({"message": "Course planning successful"}), 200


@app.route("/api/schedule/professor", methods=["GET"])
def professor_schedule():
    professor_name = request.args.get("name")
    professor = Professor.query.filter_by(first_name=professor_name).first()
    if not professor:
        return jsonify({"error": "Professor not found"}), 404

    schedule = [
        {
            "id": course.id,
            "title": course.title,
            "start_time": course.start_time.strftime("%Y-%m-%d %H:%M"),
            "end_time": course.end_time.strftime("%Y-%m-%d %H:%M"),
            "classroom": course.classroom.name if course.classroom else "Unspecified Room",
        }
        for course in professor.courses
    ]

    return jsonify(schedule)

@app.route("/api/search_course", methods=["POST"])
def search_course():
    data = request.get_json()
    course = Course.query.filter_by(title=data["title"]).first()
    if not course:
        return jsonify({"error": "Course not found"}), 404

    room_name = course.classroom.name if course.classroom else "Unspecified Room"
    professor_name = f"{course.professor.first_name} {course.professor.last_name}" if course.professor else "Unspecified Professor"

    course_details = {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "start_time": course.start_time.strftime("%Y-%m-%d %H:%M"),
        "end_time": course.end_time.strftime("%Y-%m-%d %H:%M"),
        "classroom": room_name,
        "professor": professor_name,
    }
    return jsonify(course_details)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)