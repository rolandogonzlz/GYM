from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields
from flask import Flask, jsonify, request,make_response

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:change-me@localhost:3306/GYM_final'

db = SQLAlchemy(app)

class Clients(db.Model):
    __tablename__ = 'Clients'
    ID_Client = db.Column(db.Integer, primary_key = True,autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)
    Last_Name = db.Column(db.String(50),nullable=False)
    Phone = db.Column(db.Integer, nullable=True)
    Email = db.Column(db.String(50),unique = True,nullable=False)
    Address = db.Column(db.String(50),nullable=True)
    Birth_Day = db.Column(db.Date, nullable=True)

    def __init__(self, Name,Last_Name, Email, Phone, Address, Birth_Day):
        self.Name = Name
        self.Last_Name = Last_Name
        self.Phone =Phone
        self.Email = Email
        self.Address = Address
        self.Birth_Day = Birth_Day


class Coaches(db.Model):
    __tablename__ = 'Coaches'
    ID_Coach = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Last_Name = db.Column(db.String(100), nullable=False)
    Salary_Coach = db.Column(db.Float, nullable=False)
    Phone = db.Column(db.Integer, nullable=True)
    Email = db.Column(db.String(50), unique=True, nullable=True)
    
    def __init__(self, ID_Coach, Name, Last_Name, Salary_Coach, Phone, Email):
        self.ID_Coach = ID_Coach
        self.Name = Name
        self.Last_Name = Last_Name
        self.Salary_Coach = Salary_Coach
        self.Phone = Phone
        self.Email = Email


        
class Attendance(db.Model):
    __tablename__ = 'Attendance'
    ID_Attendance = db.Column(db.Integer, primary_key=True)
    ID_Client = db.Column(db.Integer, db.ForeignKey('Clients.ID_Client'), nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Last_Name = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.Integer, nullable=True)
    Address = db.Column(db.String(50), nullable=True)
    Visit_date = db.Column(db.Date, nullable=False)
    Entry_Time = db.Column(db.Time, nullable=False)
    Exit_Time = db.Column(db.Time, nullable=True)
    Completed = db.Column(db.Boolean, nullable=False)

    def __init__(self, ID_Attendance, ID_Client, Name, Last_Name, Phone, Address, Visit_date, Entry_Time, Exit_Time, Completed):
        self.ID_Attendance = ID_Attendance
        self.ID_Client = ID_Client
        self.Name = Name
        self.Last_Name = Last_Name
        self.Phone = Phone
        self.Address = Address
        self.Visit_date = Visit_date
        self.Entry_Time = Entry_Time
        self.Exit_Time = Exit_Time
        self.Completed = Completed


class Class(db.Model):
    __tablename__ = 'Class'
    ID_Class = db.Column(db.Integer, primary_key=True)
    ID_Coach = db.Column(db.Integer, db.ForeignKey('Coaches.ID_Coach'), nullable=False)
    Class_Name = db.Column(db.String(50), nullable=False)
    Duration_date = db.Column(db.DateTime, nullable=False)
    Capacity = db.Column(db.Integer, nullable=False)
    Description = db.Column(db.String(50), nullable=True)

    def __init__(self, ID_Class, ID_Coach, Class_Name, Duration_date, Capacity, Description):
        self.ID_Class = ID_Class
        self.ID_Coach = ID_Coach
        self.Class_Name = Class_Name
        self.Duration_date = Duration_date
        self.Capacity = Capacity
        self.Description = Description


class P_Training(db.Model):
    __tablename__ = 'P_Training'
    ID_Training = db.Column(db.Integer, primary_key=True)  # Autoincremental
    ID_Coach = db.Column(db.Integer, db.ForeignKey('Coaches.ID_Coach'), nullable=False)
    ID_Nutrition_Plan = db.Column(db.Integer, db.ForeignKey('Clients.ID_Client'), nullable=False)  # Referencia a 'Clients'
    Description = db.Column(db.String(50), nullable=True)
    Start_date = db.Column(db.Date, nullable=False)
    End_date = db.Column(db.Date, nullable=False)

    # Constructor solo con los atributos que el usuario debe pasar
    def __init__(self, ID_Coach, ID_Nutrition_Plan, Description, Start_date, End_date):
        self.ID_Coach = ID_Coach
        self.ID_Nutrition_Plan = ID_Nutrition_Plan
        self.Description = Description
        self.Start_date = Start_date
        self.End_date = End_date



class Can_Receive(db.Model):
    __tablename__ = 'Can_Receive'
    ID_Client = db.Column(db.Integer, db.ForeignKey('Clients.ID_Client'), primary_key=True)
    ID_Nutrition_Plan = db.Column(db.Integer, db.ForeignKey('Clients.ID_Client'), primary_key=True)  # Referencia a 'Clients'

    def __init__(self, ID_Client, ID_Nutrition_Plan):
        self.ID_Client = ID_Client
        self.ID_Nutrition_Plan = ID_Nutrition_Plan


class Reserve(db.Model):
    __tablename__ = 'Reserve'
    ID_Client = db.Column(db.Integer, db.ForeignKey('Clients.ID_Client'), primary_key=True)
    ID_Class = db.Column(db.Integer, db.ForeignKey('Class.ID_Class'), primary_key=True)
    Date_Reserve = db.Column(db.Date, nullable=False)

    def __init__(self, ID_Client, ID_Class, Date_Reserve):
        self.ID_Client = ID_Client
        self.ID_Class = ID_Class
        self.Date_Reserve = Date_Reserve


class Sales(db.Model):
    __tablename__ = 'Sales'
    ID_Purchase = db.Column(db.Integer, primary_key=True)
    ID_Client = db.Column(db.Integer, db.ForeignKey('Clients.ID_Client'), nullable=False)
    Date_Purchase = db.Column(db.Date, nullable=False)
    Total_Purchase = db.Column(db.Float, nullable=False)

    def __init__(self, ID_Purchase, ID_Client, Date_Purchase, Total_Purchase):
        self.ID_Purchase = ID_Purchase
        self.ID_Client = ID_Client
        self.Date_Purchase = Date_Purchase
        self.Total_Purchase = Total_Purchase


class SalesDetail(db.Model):
    __tablename__ = 'SalesDetail'
    ID_Purchase = db.Column(db.Integer, db.ForeignKey('Sales.ID_Purchase'), primary_key=True)
    ID_Client = db.Column(db.Integer, db.ForeignKey('Clients.ID_Client'), primary_key=True)
    ID_Product = db.Column(db.Integer, db.ForeignKey('Products.ID_Product'), primary_key=True)
    Quantity_Purchase = db.Column(db.Integer, nullable=False)
    Unit_Price_and_Value = db.Column(db.Float, nullable=False)

    def __init__(self, ID_Purchase, ID_Client, ID_Product, Quantity_Purchase, Unit_Price_and_Value):
        self.ID_Purchase = ID_Purchase
        self.ID_Client = ID_Client
        self.ID_Product = ID_Product
        self.Quantity_Purchase = Quantity_Purchase
        self.Unit_Price_and_Value = Unit_Price_and_Value


class Products(db.Model):
    __tablename__ = 'Products'
    ID_Product = db.Column(db.Integer, primary_key=True)
    Name_Product = db.Column(db.String(100), nullable=False)
    Price_Product = db.Column(db.Float, nullable=False)
    Description = db.Column(db.String(500), nullable=True)
    Category = db.Column(db.String(100), nullable=False)

    def __init__(self, ID_Product, Name_Product, Price_Product, Description, Category):
        self.ID_Product = ID_Product
        self.Name_Product = Name_Product
        self.Price_Product = Price_Product
        self.Description = Description
        self.Category = Category


class ClientSuscription(db.Model):
    __tablename__ = 'ClientSuscription'
    ID_Client = db.Column(db.Integer, db.ForeignKey('Clients.ID_Client'), primary_key=True)
    ID_Product = db.Column(db.Integer, db.ForeignKey('Products.ID_Product'), primary_key=True)
    ID_Suscription = db.Column(db.Integer, db.ForeignKey('SuscriptionPlan.ID_Suscription'), primary_key=True)

    def __init__(self, ID_Client, ID_Product, ID_Suscription):
        self.ID_Client = ID_Client
        self.ID_Product = ID_Product
        self.ID_Suscription = ID_Suscription



class Suscription_Plan(db.Model):
    __tablename__ = 'SuscriptionPlan'
    ID_Suscription = db.Column(db.Integer, primary_key=True)
    Price_Suscription = db.Column(db.Float, nullable=False)
    Name_Suscription = db.Column(db.String(100), nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    Benefit = db.Column(db.String(200), nullable=True)

    def __init__(self, ID_Suscription, Price_Suscription, Name_Suscription, Duration, Benefit):
        self.ID_Suscription = ID_Suscription
        self.Price_Suscription = Price_Suscription
        self.Name_Suscription = Name_Suscription
        self.Duration = Duration
        self.Benefit = Benefit


# Esquemas


class ClientsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Clients
        sqla_session = db.session

    ID_Client = fields.Number(dump_only=True)
    Name = fields.String(required=True)
    Last_Name = fields.String(required=True)
    Address = fields.String(required=True)
    Email = fields.String(required=True)
    Birth_Day = fields.Date(required=True)
    Phone = fields.Integer(required=True)

class AttendanceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Attendance
        sqla_session =db.session

    ID_Attendance = fields.Integer(required=True)
    ID_Client = fields.Integer(required=True)
    Name = fields.String(required=True)
    Last_Name = fields.String(required=True)
    Phone = fields.Integer(required=True)
    Address = fields.String(required=True)
    Visit_date = fields.Date(required=True)
    Entry_Time = fields.Time(required=True)
    Exit_Time = fields.Time(required=True)
    Completed = fields.Boolean(required=True)


class SalesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Sales
        include_fk = True  # Incluir claves foráneas si es necesario
        load_instance = True  # Cargar como instancias del modelo


    ID_Purchase = fields.Integer(required=True)
    ID_Client = fields.Integer(required=True)
    date_purchase = fields.Date(required=True)
    Total_purchase = fields.Float(required=True)

class SalesDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SalesDetail
        sqla_session = db.session

    Quantity_Purchase = fields.Integer(required=True)
    ID_Purchase = fields.Integer(required=True)
    ID_Client = fields.Integer(required=True)
    ID_Product = fields.Integer(required=True)
    unit_price_and_value = fields.Float(required=True)


class CoachesSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Coaches
        sqla_session = db.session

    ID_Coach = fields.Integer(required=True)  # Este campo debe coincidir con el nombre del modelo
    Name = fields.String(required=True)
    Last_Name = fields.String(required=True)
    Salary_Coach = fields.Float(required=True)
    Phone = fields.Integer(required=True)
    Email = fields.String(required=True)


class Suscription_PlanSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Suscription_Plan
        sqla_session = db.session

    ID_Suscription = fields.Integer(required=True)
    Name_Suscription = fields.String(required=True)
    Price_Suscrption = fields.Float(required=True)
    Duration = fields.Date(required=True)
    Benefit = fields.String(required=True)

class ClientSuscriptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ClientSuscription
        sqla_session = db.session

    ID_Client = fields.Integer(required=True)
    ID_Product = fields.Integer(required=True)
    ID_Suscription = fields.Integer(required=True)
    


class ReserveSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reserve
        sqla_session = db.session

    ID_Client = fields.Integer(required=True)
    ID_Class = fields.Integer(required=True)
    ID_Coach = fields.Integer(required=True)

class ProductsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Products
        sqla_session = db.session

    ID_Product = fields.Integer(required=True)
    Name_Product = fields.String(required=True)
    Price_Product = fields.Float(required=True)
    Description = fields.String(required=True)
    Category = fields.String(required=True)
    
class P_TrainingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = P_Training
        sqla_session = db.session

    ID_Nutrition_Plan = fields.Integer(required=True)
    ID_Coach = fields.Integer(required=True)
    Description = fields.String(required=True)
    Start_Date = fields.Date(required=True)
    End_Date = fields.Date(required=True)
    

class Can_ReceiveSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Can_Receive
        sqla_session = db.session

    ID_Nutrition_Plan = fields.Integer(required=True)
    ID_Client = fields.Integer(required=True)

class ClassSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Class
        sqla_session = db.session

    ID_Class = fields.Integer(required=True)
    ID_Coach = fields.Integer(required=True)
    Class_Name = fields.String(required=True)
    Duration_date = fields.DateTime(required=True)
    Capacity = fields.Integer(required=True)
    Description = fields.String(required=True)
    

# Crear la base de datos
with app.app_context():
    db.create_all()


# INSTANCIAS DE ESQUEMAS
# INSTANCIAS DE ESQUEMAS
Reserve_schema = ReserveSchema()
Reserves_schema = ReserveSchema(many=True)
Client_schema = ClientsSchema()
Clients_schema = ClientsSchema(many=True)
Coach_schema = CoachesSchema()
Coaches_schema = CoachesSchema(many=True)

Attendance_schema = AttendanceSchema()
Attendances_schema = AttendanceSchema(many=True)
Sales_schema = SalesSchema()
Sales_many_schema = SalesSchema(many=True)  # Renombrado
Class_Schema = ClassSchema()
Class_schema = ClassSchema(many=True)
Can_Receive_schema = Can_ReceiveSchema()
Can_Receive_many_schema = Can_ReceiveSchema(many=True)  # Renombrado
P_Training_schema = P_TrainingSchema()
P_Training_many_schema = P_TrainingSchema(many=True)  # Renombrado
Products_schema = ProductsSchema()
Products_many_schema = ProductsSchema(many=True)  # Renombrado
SalesDetail_schema = SalesDetailSchema()
SalesDetail_many_schema = SalesDetailSchema(many=True)  # Renombrado
Suscription_Plan_schema = Suscription_PlanSchema()
Suscription_Plan_many_schema = Suscription_PlanSchema(many=True)  # Renombrado
ClientSuscription_schema = ClientSuscriptionSchema()
ClientSuscription_many_schema = ClientSuscriptionSchema(many=True)  # Renombrado


# RUTAS PARA CLIENTS
@app.route('/clients', methods=['GET'])
def get_clients():
    clients = Clients.query.all()
    return jsonify(Clients_schema.dump(clients)), 200


@app.route('/clients/<int:ID_Client>', methods=['GET'])
def get_client(ID_Client):
    client = Clients.query.get(ID_Client)
    if client:
        return Client_schema.jsonify(client), 200
    else:
        return jsonify({'message': 'Client not found'}), 404


@app.route('/clients', methods=['POST'])
def create_client():
    client_data = request.json
    try:
        new_client_data = Client_schema.load(client_data)
        new_client = Clients(**new_client_data)
        db.session.add(new_client)
        db.session.commit()
        return Client_schema.jsonify(new_client), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/clients/<int:ID_Client>', methods=['DELETE'])
def delete_client(ID_Client):
    client = Clients.query.get(ID_Client)
    if client:
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Client deleted successfully'}), 200
    else:
        return jsonify({'error': 'Client not found'}), 404

@app.route('/clients/<int:ID_Client>', methods=['PUT'])
def update_client(ID_Client):
    client = Clients.query.get(ID_Client)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    data = request.json
    try:
        for key, value in data.items():
            setattr(client, key, value)
        db.session.commit()
        return Client_schema.jsonify(client), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400



# RUTAS PARA RESERVE
@app.route('/reserve/<int:ID_Client>/<int:ID_Class>', methods=['GET'])
def get_reserve(ID_Client, ID_Class):
    reserve = Reserve.query.filter_by(ID_Client=ID_Client, ID_Class=ID_Class).first()
    if reserve:
        return Reserve_schema.jsonify(reserve), 200
    else:
        return jsonify({'message': 'Reserve not found'}), 404

@app.route('/clients/<int:ID_Client>/reservations', methods=['GET'])
def get_client_reservations(ID_Client):
    reservations = Reserve.query.filter_by(ID_Client=ID_Client).all()
    if reservations:
        return Reserves_schema.jsonify(reservations), 200
    else:
        return jsonify({'message': 'No reservations found for this client'}), 404


@app.route('/reserve', methods=['POST'])
def create_reserve():
    reserve_data = request.json
    try:
        new_reserve_data = Reserve_schema.load(reserve_data)
        new_reserve = Reserve(**new_reserve_data)
        db.session.add(new_reserve)
        db.session.commit()
        return Reserve_schema.jsonify(new_reserve), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/reserve/<int:ID_Client>/<int:ID_Class>', methods=['DELETE'])
def delete_reserve(ID_Client, ID_Class):
    reserve = Reserve.query.filter_by(ID_Client=ID_Client, ID_Class=ID_Class).first()
    if reserve:
        db.session.delete(reserve)
        db.session.commit()
        return jsonify({'message': 'Reserve deleted successfully'}), 200
    else:
        return jsonify({'error': 'Reserve not found'}), 404



# RUTAS PARA COACHES
@app.route('/coaches', methods=['GET'])
def get_coaches():
    coaches = Coaches.query.all()
    return jsonify(Coaches_schema.dump(coaches)), 200


@app.route('/coaches', methods=['POST'])
def create_coach():
    coach_data = request.json  # Datos que vienen del cuerpo de la solicitud en formato JSON
    try:
        new_coach_data = Coach_schema.load(coach_data)  # `coach_data` debe ser el JSON recibido
        print(new_coach_data)  # Para verificar el contenido

        new_coach = Coaches(**new_coach_data)  # Pasa los datos como diccionario
        db.session.add(new_coach)
        db.session.commit()
        return Coach_schema.jsonify(new_coach), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400





@app.route('/coaches/<int:ID_Coach>', methods=['GET'])
def get_coach(ID_Coach):
    coach = Coaches.query.get(ID_Coach)
    if coach:
        return Coach_schema.jsonify(coach), 200
    else:
        return jsonify({'message': 'Coach not found'}), 404

@app.route('/coaches/<int:ID_Coach>', methods=['DELETE'])
def delete_coach(ID_Coach):
    coach = Coaches.query.get(ID_Coach)
    if coach:
        db.session.delete(coach)
        db.session.commit()
        return jsonify({'message': 'Coach deleted successfully'}), 200
    else:
        return jsonify({'message': 'Coach not found'}), 404


# Ruta para Sales
@app.route('/sales', methods=['GET'])
def get_sales():
    sales = Sales.query.all()
    return jsonify([sale.__dict__ for sale in sales]), 200

@app.route('/sales/total', methods=['GET'])
def get_total_sales():
    total_sales = db.session.query(db.func.sum(Sales.Total_Purchase)).scalar()
    return jsonify({'total_sales': total_sales}), 200


@app.route('/sales', methods=['POST'])
def create_sale():
    try:
        sale_data = request.json
        new_sale = Sales(**sale_data)
        db.session.add(new_sale)
        db.session.commit()
        # Usar esquema para serializar el objeto antes de enviarlo en la respuesta
        return Sales_schema.jsonify(new_sale), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400



# RUTAS PARA ATTENDANCE
@app.route('/attendance', methods=['GET'])
def get_attendances():
    attendances = Attendance.query.all()
    return jsonify(Attendance_schema.dump(attendances, many=True)), 200


@app.route('/attendance/<int:ID_Attendance>', methods=['GET'])
def get_attendance(ID_Attendance):
    attendance = Attendance.query.get(ID_Attendance)
    if attendance:
        return Attendance_schema.jsonify(attendance), 200
    else:
        return jsonify({'message': 'Attendance not found'}), 404


@app.route('/attendance', methods=['POST'])
def create_attendance():
    attendance_data = request.json
    try:
        new_attendance = Attendance(**attendance_data)
        db.session.add(new_attendance)
        db.session.commit()
        return Attendance_schema.jsonify(new_attendance), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/attendance/<int:ID_Attendance>', methods=['DELETE'])
def delete_attendance(ID_Attendance):
    attendance = Attendance.query.get(ID_Attendance)
    if attendance:
        db.session.delete(attendance)
        db.session.commit()
        return jsonify({'message': 'Attendance deleted successfully'}), 200
    else:
        return jsonify({'message': 'Attendance not found'}), 404


# RUTAS PARA CAN_RECEIVE
@app.route('/can_receive', methods=['GET'])
def get_can_receive():
    can_receive = Can_Receive.query.all()
    return jsonify(Can_Receive_schema.dump(can_receive, many=True)), 200


@app.route('/can_receive', methods=['POST'])
def create_can_receive():
    can_receive_data = request.json
    try:
        new_can_receive = Can_Receive(**can_receive_data)
        db.session.add(new_can_receive)
        db.session.commit()
        return Can_Receive_schema.jsonify(new_can_receive), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/can_receive/<int:ID_Client>/<int:ID_Nutrition_Plan>', methods=['DELETE'])
def delete_can_receive(ID_Client, ID_Nutrition_Plan):
    can_receive = Can_Receive.query.filter_by(ID_Client=ID_Client, ID_Nutrition_Plan=ID_Nutrition_Plan).first()
    if can_receive:
        db.session.delete(can_receive)
        db.session.commit()
        return jsonify({'message': 'Can_Receive record deleted successfully'}), 200
    else:
        return jsonify({'message': 'Record not found'}), 404


# RUTAS PARA CLASS
@app.route('/class', methods=['GET'])
def get_classes():
    classes = Class.query.all()
    return jsonify(Class_schema.dump(classes, many=True)), 200


@app.route('/class/<int:ID_Class>', methods=['GET'])
def get_class(ID_Class):
    class_instance = Class.query.get(ID_Class)
    if class_instance:
        return Class_schema.jsonify(class_instance), 200
    else:
        return jsonify({'message': 'Class not found'}), 404

@app.route('/class', methods=['POST'])
def create_class():
    class_data = request.json
    # Se hace la validación de los datos recibidos
    errors = Class_schema.validate(class_data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    try:
        # Se crea una nueva instancia de la clase con los datos recibidos
        new_class = Class(**class_data)
        db.session.add(new_class)
        db.session.commit()
        return Class_schema.jsonify(new_class), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400



@app.route('/class/<int:ID_Class>', methods=['DELETE'])
def delete_class(ID_Class):
    class_instance = Class.query.get(ID_Class)
    if class_instance:
        db.session.delete(class_instance)
        db.session.commit()
        return jsonify({'message': 'Class deleted successfully'}), 200
    else:
        return jsonify({'message': 'Class not found'}), 404



# RUTAS PARA P_TRAINING
@app.route('/p_training', methods=['GET'])
def get_p_training():
    p_training = P_Training.query.all()
    return jsonify(P_Training_schema.dump(p_training, many=True)), 200


@app.route('/p_training', methods=['POST'])
def create_p_training():
    p_training_data = request.json
    try:
        new_p_training = P_Training(**p_training_data)
        db.session.add(new_p_training)
        db.session.commit()
        return P_Training_schema.jsonify(new_p_training), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/p_training/<int:ID_Training>', methods=['DELETE'])
def delete_p_training(ID_Training):
    p_training = P_Training.query.get(ID_Training)
    if p_training:
        db.session.delete(p_training)
        db.session.commit()
        return jsonify({'message': 'P_Training record deleted successfully'}), 200
    else:
        return jsonify({'message': 'Record not found'}), 404
    
# RUTAS PARA PRODUCTS
@app.route('/products', methods=['GET'])
def get_products():
    products = Products.query.all()
    return jsonify(Products_schema.dump(products)), 200


@app.route('/products/<int:ID_Product>', methods=['GET'])
def get_product(ID_Product):
    product = Products.query.get(ID_Product)
    if product:
        return Products_schema.jsonify(product), 200
    else:
        return jsonify({'message': 'Product not found'}), 404


@app.route('/products', methods=['POST'])
def create_product():
    product_data = request.json
    try:
        new_product = Products(**product_data)
        db.session.add(new_product)
        db.session.commit()
        return Products_schema.jsonify(new_product), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/products/<int:ID_Product>', methods=['DELETE'])
def delete_product(ID_Product):
    product = Products.query.get(ID_Product)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    else:
        return jsonify({'message': 'Product not found'}), 404


# Rutas para Sales Detail
@app.route('/sales_detail', methods=['GET'])
def get_sales_details():
    sales_details = SalesDetail.query.all()
    return jsonify(SalesDetail_schema.dump(sales_details, many=True)), 200


@app.route('/sales_detail/<int:ID_Sales_Detail>', methods=['GET'])
def get_sales_detail(ID_Sales_Detail):
    sales_detail = SalesDetail.query.get(ID_Sales_Detail)
    if sales_detail:
        return SalesDetail_schema.jsonify(sales_detail), 200
    else:
        return jsonify({'message': 'SalesDetail not found'}), 404


@app.route('/sales_detail', methods=['POST'])
def create_sales_detail():
    sales_detail_data = request.json
    try:
        new_sales_detail = SalesDetail(**sales_detail_data)
        db.session.add(new_sales_detail)
        db.session.commit()
        return SalesDetail_schema.jsonify(new_sales_detail), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/sales_detail/<int:ID_Sales_Detail>', methods=['DELETE'])
def delete_sales_detail(ID_Sales_Detail):
    sales_detail = SalesDetail.query.get(ID_Sales_Detail)
    if sales_detail:
        db.session.delete(sales_detail)
        db.session.commit()
        return jsonify({'message': 'SalesDetail deleted successfully'}), 200
    else:
        return jsonify({'message': 'SalesDetail not found'}), 404
    

#Rutas para Suscription Plan
@app.route('/suscription_plan', methods=['GET'])
def get_suscription_plans():
    suscription_plans = Suscription_Plan.query.all()
    return jsonify(Suscription_Plan_schema.dump(suscription_plans, many=True)), 200


@app.route('/suscription_plan/<int:ID_Plan>', methods=['GET'])
def get_suscription_plan(ID_Plan):
    suscription_plan = Suscription_Plan.query.get(ID_Plan)
    if suscription_plan:
        return Suscription_Plan_schema.jsonify(suscription_plan), 200
    else:
        return jsonify({'message': 'SuscriptionPlan not found'}), 404


@app.route('/suscription_plan', methods=['POST'])
def create_suscription_plan():
    suscription_plan_data = request.json
    try:
        new_suscription_plan = Suscription_Plan(**suscription_plan_data)
        db.session.add(new_suscription_plan)
        db.session.commit()
        return Suscription_Plan_schema.jsonify(new_suscription_plan), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/suscription_plan/<int:ID_Plan>', methods=['DELETE'])
def delete_suscription_plan(ID_Plan):
    suscription_plan = Suscription_Plan.query.get(ID_Plan)
    if suscription_plan:
        db.session.delete(suscription_plan)
        db.session.commit()
        return jsonify({'message': 'SuscriptionPlan deleted successfully'}), 200
    else:
        return jsonify({'message': 'SuscriptionPlan not found'}), 404




#Rutas para Client Suscrption
@app.route('/client_suscription', methods=['GET'])
def get_client_suscriptions():
    client_suscriptions = ClientSuscription.query.all()
    return jsonify(ClientSuscription_schema.dump(client_suscriptions, many=True)), 200


@app.route('/client_suscription/<int:ID_Client>/<int:ID_Plan>', methods=['GET'])
def get_client_suscription(ID_Client, ID_Plan):
    client_suscription = ClientSuscription.query.filter_by(ID_Client=ID_Client, ID_Plan=ID_Plan).first()
    if client_suscription:
        return ClientSuscription_schema.jsonify(client_suscription), 200
    else:
        return jsonify({'message': 'ClientSuscription not found'}), 404


@app.route('/client_suscription', methods=['POST'])
def create_client_suscription():
    client_suscription_data = request.json
    try:
        new_client_suscription = ClientSuscription(**client_suscription_data)
        db.session.add(new_client_suscription)
        db.session.commit()
        return ClientSuscription_schema.jsonify(new_client_suscription), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/client_suscription/<int:ID_Client>/<int:ID_Plan>', methods=['DELETE'])
def delete_client_suscription(ID_Client, ID_Plan):
    client_suscription = ClientSuscription.query.filter_by(ID_Client=ID_Client, ID_Plan=ID_Plan).first()
    if client_suscription:
        db.session.delete(client_suscription)
        db.session.commit()
        return jsonify({'message': 'ClientSuscription deleted successfully'}), 200
    else:
        return jsonify({'message': 'ClientSuscription not found'}), 404


if __name__ == "__main__":
    app.run(debug=True)