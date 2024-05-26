from flask import Flask, jsonify, request 
from flask_marshmallow import Marshmallow 
from marshmallow import fields, ValidationError 
import mysql.connector
from mysql.connector import Error
# Install commands
# python3 -m venv venv
# source venv/bin/activate
# pip install Flask Flask-Marshmallow marshmallow mysql-connector-python



# These lines set up the basic structure for a Flask application with Marshmallow support
app = Flask(__name__) #creates instance of Flask class. 
ma = Marshmallow(app) #initializes the Marshmallow library - used for coverting objects to json and json back to objects. Here we pass app instance to Marshmallow
#                      this integrates Marshmallow with your Flask application.
# Marshmallow is ready to be used for defining schemas that will help serialize and deserialize the data handled by the Flask application.

# Database configuration
db_name = "fitness_tracker"
user = "root"
password = "sqlpass#4"
host = "localhost"

def get_db_connection():
    try:
        # attempt to make a connection
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )

        # check for a connection
        if conn.is_connected():
            print("Connected to database successfully.")
            return conn
        
    except Error as e:
        # handling any errors specific to our Database
        print(f"Error: {e}")
        return None

db = get_db_connection()
# database should connect at this point



# Implementing CRUD Operations for Members
# -add - retrieve -update -delete
# define routes and implement corresponding logic

class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)




@app.route("/members", methods=["POST"])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        name = member_data['name']
        age = member_data['age']
        gender = member_data['gender']

        query = "INSERT INTO Members (name, age, gender) VALUES (%s, %s, %s)"
        new_member = (name, age, gender)
        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({"message": "Member added successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/members/<int:id>", methods=["GET"])
def get_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        query = "SELECT * FROM Members WHERE member_id = %s"
        cursor.execute(query, (id,))
        member = cursor.fetchone()

        if member:
            member_dict = {
                "id": member[0],
                "name": member[1],
                "age": member[2],
                "gender": member[3]
            }
            return jsonify(member_dict), 200
        else:
            return jsonify({"message": "Member not found"}), 404

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    try: 
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        name = member_data['name']
        age = member_data['age']
        gender = member_data['gender']

        query = "UPDATE Members SET name = %s, age = %s, gender = %s WHERE member_id = %s"
        updated_member = (name, age, gender, id)
        cursor.execute(query, updated_member)
        conn.commit()

        return jsonify({"message": "Member details updated successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        query = "DELETE FROM Members WHERE member_id = %s"
        cursor.execute(query, (id,))
        conn.commit()

        return jsonify({"message": "Member deleted successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()



#Managing Workout Sessions
# Develop routes for schedule, update, and view workout sessions            

# WorkoutSession schema using Marshmallow
class WorkoutSessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'member_id', 'date', 'duration')

workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)



@app.route("/workout_sessions", methods=["POST"])
def schedule_workout_session():
    try:
        session_data = workout_session_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        member_id = session_data['member_id']
        date = session_data['date']
        duration = session_data['duration']
        calories_burned = session_data['calories_burned']

        query = "INSERT INTO WorkoutSessions (member_id, date, duration, calories_burned) VALUES (%s, %s, %s, %s)"
        new_session = (member_id, date, duration, calories_burned)
        cursor.execute(query, new_session)
        conn.commit()

        return jsonify({"message": "Workout session scheduled successfully"}), 201

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/workout_sessions/<int:id>", methods=["PUT"])
def update_workout_session(id):
    try: 
        session_data = workout_session_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        member_id = session_data['member_id']
        date = session_data['date']
        duration = session_data['duration']
        calories_burned = session_data['calories_burned']

        query = "UPDATE WorkoutSessions SET member_id = %s, date = %s, duration = %s, calories_burned = %s WHERE session_id = %s"
        updated_session = (member_id, date, duration, calories_burned, id)
        cursor.execute(query, updated_session)
        conn.commit()

        return jsonify({"message": "Workout session details updated successfully"}), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/workout_sessions/<int:id>", methods=["GET"])
def get_workout_session(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        query = "SELECT * FROM WorkoutSessions WHERE session_id = %s"
        cursor.execute(query, (id,))
        session = cursor.fetchone()

        if session:
            session_dict = {
                "id": session[0],
                "member_id": session[1],
                "date": session[2].isoformat(),
                "duration": session[3]
            }
            return jsonify(session_dict), 200
        else:
            return jsonify({"message": "Workout session not found"}), 404

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/workout_sessions/members/<int:member_id>", methods=["GET"])
def get_workout_sessions_for_member(member_id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        query = "SELECT * FROM WorkoutSessions WHERE member_id = %s"
        cursor.execute(query, (member_id,))
        sessions = cursor.fetchall()

        session_list = []
        for session in sessions:
            session_dict = {
                "id": session[0],
                "member_id": session[1],
                "date": session[2].isoformat(),
                "duration": session[3]
            }
            session_list.append(session_dict)

        return jsonify(session_list), 200

    except Error as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
