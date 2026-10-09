from flask import Flask, request, jsonify
from models import db, Snack, User, Order
import os

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'ini_rahasia'

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    user = User(username=data["username"], role=data["role"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registrasi berhasil"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.check_password(data["password"]):
        additional_claims = {"role": user.role}
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Login gagal"}), 401

@app.route("/snack", methods=["POST"])
@jwt_required()
def tambah_snack():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']

    if role != 'Penjual':
        return jsonify({"error": "Hanya penjual yang dapat menambahkan snack"}), 403

    data = request.get_json()
    snack = Snack(
        nama=data["nama"],
        harga=data["harga"],
        id_penjual=current_user_id,
        stok=data.get("stok", 0)
    )
    db.session.add(snack)
    db.session.commit()
    return jsonify({"message": "Snack berhasil ditambahkan"}), 201

@app.route("/snack", methods=["GET"])
def lihat_semua_snack():
    result = Snack.query.all()
    return jsonify([{
        "id": s.id, "nama": s.nama, "harga": s.harga,
        "id_penjual": s.id_penjual, "stok": s.stok
    } for s in result]), 200

@app.route("/snack/<int:snack_id>", methods=["DELETE"])
@jwt_required()
def hapus_snack(snack_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']

    snack = Snack.query.get(snack_id)
    if not snack:
        return jsonify({"error": "Snack tidak ditemukan"}), 404

    if role == 'Admin' or (role == 'Penjual' and snack.id_penjual == current_user_id):
        db.session.delete(snack)
        db.session.commit()
        return jsonify({"message": "Snack berhasil dihapus"}), 200

    return jsonify({"error": "Tidak berhak menghapus snack ini"}), 403

@app.route("/orders", methods=["POST"])
@jwt_required()
def buat_order():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']

    if role != 'Pembeli':
        return jsonify({"error": "Hanya pembeli yang dapat memesan snack"}), 403

    data = request.get_json()
    order = Order(
        snack_id=data["snack_id"],
        buyer_id=current_user_id,
        quantity=data["quantity"],
        status='Pending'
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({"message": "Order berhasil dibuat"}), 201

@app.route("/orders", methods=["GET"])
@jwt_required()
def lihat_order():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims['role']

    if role == 'Admin':
        orders = Order.query.all()
    elif role == 'Penjual':
        orders = Order.query.join(Snack).filter(Snack.id_penjual == current_user_id).all()
    else:
        return jsonify({"error": "Tidak berhak melihat order"}), 403

    result = []
    for o in orders:
        result.append({
            "id": o.id,
            "snack_id": o.snack_id,
            "buyer_id": o.buyer_id,
            "quantity": o.quantity,
            "status": o.status
        })
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)


# kode lab session 12
# from flask import Flask, request, jsonify
# from models import db, Jajanan, User
# import os

# app = Flask(__name__)
# basedir = os.path.abspath(os.path.dirname(__file__))
# db_path = os.path.join(basedir, 'data.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)

# with app.app_context():
#     db.create_all()

# # ========== CRUD Jajanan ==========
# @app.route("/jajanan", methods=["POST"])
# def tambah_jajanan():
#     data = request.get_json()
#     jajanan = Jajanan(
#         nama=data["nama"],
#         harga=data["harga"],
#         id_penjual=data.get("id_penjual", 0),
#         stok=data.get("stok", 0)
#     )
#     db.session.add(jajanan)
#     db.session.commit()
#     return jsonify({"message": "Jajanan ditambahkan", "data": {
#         "id": jajanan.id, "nama": jajanan.nama
#     }}), 201

# @app.route("/jajanan", methods=["GET"])
# def lihat_semua_jajanan():
#     result = Jajanan.query.all()
#     return jsonify([{
#         "id": j.id, "nama": j.nama, "harga": j.harga,
#         "id_penjual": j.id_penjual, "stok": j.stok
#     } for j in result]), 200

# @app.route("/jajanan/<int:jajanan_id>", methods=["GET"])
# def get_jajanan(jajanan_id):
#     jajanan = Jajanan.query.get(jajanan_id)
#     if jajanan:
#         return jsonify({
#             "id": jajanan.id,
#             "nama": jajanan.nama,
#             "harga": jajanan.harga,
#             "id_penjual": jajanan.id_penjual,
#             "stok": jajanan.stok
#         }), 200
#     return jsonify({"error": "Jajanan tidak ditemukan"}), 404

# @app.route("/jajanan/<int:jajanan_id>", methods=["PUT"])
# def ubah_jajanan(jajanan_id):
#     jajanan = Jajanan.query.get(jajanan_id)
#     if not jajanan:
#         return jsonify({"error": "Jajanan tidak ditemukan"}), 404

#     data = request.get_json()
#     jajanan.nama = data.get("nama", jajanan.nama)
#     jajanan.harga = data.get("harga", jajanan.harga)
#     jajanan.id_penjual = data.get("id_penjual", jajanan.id_penjual)
#     jajanan.stok = data.get("stok", jajanan.stok)

#     db.session.commit()
#     return jsonify({"message": "Jajanan berhasil diperbarui"}), 200

# @app.route("/jajanan/<int:jajanan_id>", methods=["DELETE"])
# def hapus_jajanan(jajanan_id):
#     jajanan = Jajanan.query.get(jajanan_id)
#     if not jajanan:
#         return jsonify({"error": "Jajanan tidak ditemukan"}), 404

#     db.session.delete(jajanan)
#     db.session.commit()
#     return jsonify({"message": "Jajanan berhasil dihapus"}), 200



# # ========= Register & CRUD User =========

# @app.route("/register", methods=["POST"])
# def register_user():
#     data = request.get_json()
#     user = User(
#         username=data["username"],
#         password=data["password"],  # *Belum hashing
#         role=data["role"]
#     )
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({"message": "Registrasi berhasil"}), 201

# @app.route("/users", methods=["GET"])
# def lihat_user():
#     users = User.query.all()
#     return jsonify([{
#         "id": u.id, "username": u.username, "role": u.role
#     } for u in users]), 200

# @app.route("/users/<int:user_id>", methods=["PUT"])
# def ubah_user(user_id):
#     data = request.get_json()
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"error": "User tidak ditemukan"}), 404

#     user.username = data.get("username", user.username)
#     user.password = data.get("password", user.password)
#     user.role = data.get("role", user.role)
#     db.session.commit()
#     return jsonify({"message": "User diperbarui"}), 200

# @app.route("/users/<int:user_id>", methods=["DELETE"])
# def hapus_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"error": "User tidak ditemukan"}), 404
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({"message": "User berhasil dihapus"}), 200

# @app.route("/users/<int:user_id>", methods=["GET"])
# def get_user(user_id):
#     user = User.query.get(user_id)
#     if user:
#         return jsonify({
#             "id": user.id,
#             "username": user.username,
#             "role": user.role
#         }), 200
#     return jsonify({"error": "User tidak ditemukan"}), 404


# if __name__ == "__main__":
#     app.run(debug=True)



# #kode lab session 11
# # from flask import Flask, jsonify, request

# # app = Flask(__name__)

# # jajanans = []  # Simpan data sementara di memory
# # counter = 1  # Untuk auto increment ID

# # # Model data jajanan
# # class Jajanan:
# #     def __init__(self, nama, harga, id_penjual=0, stok=0):
# #         global counter
# #         self.id = counter
# #         counter += 1
# #         self.nama = nama
# #         self.harga = harga
# #         self.id_penjual = id_penjual
# #         self.stok = stok

# # # Helper function to find jajanan by id
# # def find_jajanan(jajanan_id):
# #     return next((j for j in jajanans if j.id == jajanan_id), None)

# # # GET /jajanan
# # @app.route("/jajanan", methods=["GET"])
# # def get_all_jajanan():
# #     return jsonify([vars(j) for j in jajanans])

# # # GET /jajanan/<id>
# # @app.route("/jajanan/<int:jajanan_id>", methods=["GET"])
# # def get_jajanan(jajanan_id):
# #     jajanan = find_jajanan(jajanan_id)
# #     if jajanan:
# #         return jsonify(vars(jajanan))
# #     return jsonify({"error": "Jajanan tidak ditemukan"}), 404

# # # POST /jajanan
# # @app.route("/jajanan", methods=["POST"])
# # def add_jajanan():
# #     data = request.json
# #     new_jajanan = Jajanan(data["nama"], data["harga"], data.get("id_penjual", 0), data.get("stok", 0))
# #     jajanans.append(new_jajanan)
# #     return jsonify(vars(new_jajanan)), 201

# # # PUT /jajanan/<id>
# # @app.route("/jajanan/<int:jajanan_id>", methods=["PUT"])
# # def update_jajanan(jajanan_id):
# #     jajanan = find_jajanan(jajanan_id)
# #     if not jajanan:
# #         return jsonify({"error": "Jajanan tidak ditemukan"}), 404
# #     data = request.json
# #     jajanan.nama = data.get("nama", jajanan.nama)
# #     jajanan.harga = data.get("harga", jajanan.harga)
# #     jajanan.id_penjual = data.get("id_penjual", jajanan.id_penjual)
# #     jajanan.stok = data.get("stok", jajanan.stok)
# #     return jsonify(vars(jajanan))

# # # DELETE /jajanan/<id>
# # @app.route("/jajanan/<int:jajanan_id>", methods=["DELETE"])
# # def delete_jajanan(jajanan_id):
# #     jajanan = find_jajanan(jajanan_id)
# #     if not jajanan:
# #         return jsonify({"error": "Jajanan tidak ditemukan"}), 404
# #     jajanans.remove(jajanan)
# #     return jsonify({"message": "Jajanan berhasil dihapus"})

# # if __name__ == "__main__":
# #     app.run(debug=True)
