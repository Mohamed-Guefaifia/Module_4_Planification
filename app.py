import streamlit as st
import requests
from datetime import datetime
from faker import Faker
import random
from datetime import timedelta

BASE_URL = "http://127.0.0.1:5000/api"  # Mettez à jour avec l'URL de votre serveur


fake = Faker()  # Créez une instance de Faker

def admin_panel():
    st.title("Admin Panel")
    # Entrées de l'administrateur 
    course_title = st.text_input("Course Title")
    course_description = st.text_input("Course Description")
    professor_name = st.text_input("Professor's Name")
    # Sélectionne aléatoirement une salle de classe
    classroom_name = random.choice(["Room A", "Room B", "Room C"])
    
    start_time = generate_random_start_time()

    # Génère l'heure de fin aléatoire
    start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    end_datetime = start_datetime + timedelta(hours=random.randint(2, 4))
    end_time = end_datetime.strftime("%Y-%m-%d %H:%M")

    if st.button('Planify Course'):
        data = {
            "title": course_title,
            "description": course_description,
            "professor_name": professor_name,
            "classroom_name": classroom_name,
            "start_time": start_time,
            "end_time": end_time
        }

        response = requests.post(f"{BASE_URL}/planify_course", json=data)
        if response.status_code == 200:
            st.write("Course planified successfully!")
        else:
            error_message = response.json().get("error")
            if error_message:
                st.write(f"Error: {error_message}")
            else:
                st.write("Error planifying the course.")

def generate_random_start_time():
    while True:
        start_time = fake.date_time_between(start_date="-7d", end_date="+7d", tzinfo=None)
        if 8 <= start_time.hour < 17 and start_time.minute == 0:
            return start_time.strftime("%Y-%m-%d %H:%M")

def professor_panel():
    st.title("Professor Panel")
    professor_name = st.text_input("Enter Professor's Name")
    if st.button('View Schedule'):
        response = requests.get(f"{BASE_URL}/schedule/professor", params={"name": professor_name})
        if response.status_code == 200:
            schedule = response.json()
            if schedule:
                st.write(f"Professor Schedule for {professor_name}:")
                for course in schedule:
                    st.write(f"Title: {course['title']}, Start Time: {course['start_time']}, End Time: {course['end_time']}, Classroom: {course['classroom']}")
            else:
                st.write("Professor not found or has no courses.")
        else:
            st.write("Error fetching professor's schedule.")

def student_panel():
    st.title("Student Panel")
    course_title = st.text_input("Enter Course Title")
    if st.button('Search'):
        response = requests.post(f"{BASE_URL}/search_course", json={"title": course_title})
        if response.status_code == 200:
            course = response.json()
            if isinstance(course, dict):  # Vérifiez si la réponse est un dictionnaire
                st.write(f"Course Title: {course.get('title', 'N/A')}")
                st.write(f"Description: {course.get('description', 'N/A')}")
                st.write(f"Start Time: {course.get('start_time', 'N/A')}")
                st.write(f"End Time: {course.get('end_time', 'N/A')}")
                st.write(f"Classroom: {course.get('classroom', 'N/A')}")
                st.write(f"Professor: {course.get('professor', 'N/A')}")
            else:
                st.write("Course not found.")
        else:
            st.write("Error fetching course information.")


# Set the page title
def main():
    st.title("Course Scheduling System")
    option = st.selectbox("Choose a User Type", ["Admin", "Professor", "Student"])

    if option == "Admin":
        admin_panel()
    elif option == "Professor":
        professor_panel()
    elif option == "Student":
        student_panel()

# Run the main function
if __name__ == '__main__':
    main()
