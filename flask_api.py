import json
from flask import Flask, request, jsonify
from flask_restx import Resource, Api
from flask_jwt_extended import JWTManager, create_access_token
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "bfaa900b6ca9a5140706f2df9c3613ff"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://arunsingh:emppassword@localhost/dummydb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
ms = Marshmallow(app)
api = Api(app)
jwt = JWTManager(app)


class Employee(db.Model):
    """Here i am creating a table which name is employee
    in which all the details of an employee is stored
    """

    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zipcode = db.Column(db.String(100))


# here is schema
# using the concepts of serialization with marshmallow
class EmployeeSchema(ms.Schema):
    class Meta:
        fields = (
            "id",
            "first_name",
            "last_name",
            "role",
            "city",
            "country",
            "state",
            "zipcode",
        )


# this one is for an employee
emp_schema = EmployeeSchema()

# this one is for list of employees
emps_schema = EmployeeSchema(many=True)


@app.route("/login/", methods=["POST"])
def login():
    try:
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user_file = open("D:\\Week_One_Task\\task2\\users.json", "r")
        user_data = user_file.read()
        user_details = json.loads(user_data)
        user_file.close()
        for user in user_details:
            if user["username"] != username or user["password"] != password:
                return jsonify({"msg": "Bad username or password"}, 401)

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    except Exception:
        return False


@api.route("/employees/")
class EmployeesListResource(Resource):
    def get(self):
        """this function is used to get all employee details"""
        try:
            employees = Employee.query.all()
            serialize_data = emps_schema.dump(employees)
            return jsonify({"emps": serialize_data})
        except Exception:
            return False

    def post(self):
        """this function is used to create a employee details"""
        try:
            new_employee = Employee(
                id=request.json["id"],
                first_name=request.json["first_name"],
                last_name=request.json["last_name"],
                role=request.json["role"],
                city=request.json["city"],
                country=request.json["country"],
                state=request.json["state"],
                zipcode=request.json["zipcode"],
            )

            db.session.add(new_employee)
            db.session.commit()
            return emp_schema.dump(new_employee)
        except Exception:
            return False


@api.route("/employee/<int:id>")
class EmployeeResource(Resource):
    def get(self, id):
        """this function is used to get an employee details"""
        try:
            employee = Employee.query.get_or_404(id)
            serialize_data = emp_schema.dump(employee)
            return jsonify({"emp": serialize_data})
        except Exception:
            return False

    def delete(self, id):
        """this function is used to delete a single employee details"""
        try:
            employee = Employee.query.get_or_404(id)
            db.session.delete(employee)
            db.session.commit()
            return "employee deleted"
        except Exception:
            return False

    def patch(self, id):
        """this function is used to update an employee details"""
        try:
            employee = Employee.query.get_or_404(id)
            if "id" in request.json:
                employee.id = request.json["id"]
            if "first_name" in request.json:
                employee.first_name = request.json["first_name"]
            if "last_name" in request.json:
                employee.last_name = request.json["last_name"]
            if "role" in request.json:
                employee.role = request.json["role"]
            if "city" in request.json:
                employee.city = request.json["city"]
            if "country" in request.json:
                employee.country = request.json["country"]
            if "state" in request.json:
                employee.state = request.json["state"]
            if "zipcode" in request.json:
                employee.zipcode = request.json["zipcode"]

            db.session.commit()
            return emp_schema.dump(employee)
        except Exception:
            return False


if __name__ == "__main__":
    app.run(debug=True)
