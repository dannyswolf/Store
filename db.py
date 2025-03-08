from settings import DB
import traceback
from sqlalchemy import create_engine, Column, Integer, Text, asc, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(f"sqlite:///{DB}")
session = sessionmaker(bind=engine)()
base = declarative_base()
conn = session.bind


def get_spare_parts(table):
    try:
        data = session.query(table).all()
        return data
    except Exception:
        print(traceback.print_exc())
        return


def get_spare_part_to_edit(table, item_id):
    try:
        data = session.query(table).get(item_id)
        return data
    except Exception:
        print(traceback.print_exc())
        return


# Tables
class Brother(base):
    __tablename__ = 'BROTHER'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Brother(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Canon(base):
    __tablename__ = 'CANON'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Canon(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Epson(base):
    __tablename__ = 'EPSON'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Epson(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Konica(base):
    __tablename__ = 'KONICA'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Konica(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Kyocera(base):
    __tablename__ = 'KYOCERA'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Kyocera(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Lexmark(base):
    __tablename__ = 'LEXMARK'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Lexmark(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Oki(base):
    __tablename__ = 'OKI'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Oki(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Ricoh(base):
    __tablename__ = 'RICOH'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Ricoh(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Samsung(base):
    __tablename__ = 'SAMSUNG'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Samsung(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Sharp(base):
    __tablename__ = 'Sharp'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    PARTS_NR = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Sharp(id='%i', PARTS_NR='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s', ΤΕΜΑΧΙΑ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.PARTS_NR, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.PARTS_NR} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Melanakia(base):
    __tablename__ = 'ΜΕΛΑΝΑΚΙΑ'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    ΕΤΑΙΡΕΙΑ = Column(Text)
    ΠΟΙΟΤΗΤΑ = Column(Text)
    ΑΝΑΛΩΣΙΜΟ = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΤΙΜΗ = Column(Text)
    ΣΥΝΟΛΟ = Column(Text)
    ΣΕΛΙΔΕΣ = Column(Text)
    ΠΕΛΑΤΕΣ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Melanakia(id='%i', ΕΤΑΙΡΕΙΑ='%s', ΠΟΙΟΤΗΤΑ='%s', ΑΝΑΛΩΣΙΜΟ='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s' " \
               "ΤΕΜΑΧΙΑ='%s', ΤΙΜΗ='%s', ΣΥΝΟΛΟ='%s', ΣΕΛΙΔΕΣ='%s', ΠΕΛΑΤΕΣ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.ΕΤΑΙΡΕΙΑ, self.ΠΟΙΟΤΗΤΑ, self.ΑΝΑΛΩΣΙΜΟ, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ,
               self.ΤΙΜΗ, self.ΣΥΝΟΛΟ, self.ΣΕΛΙΔΕΣ, self.ΠΕΛΑΤΕΣ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.ΕΤΑΙΡΕΙΑ} {self.ΠΟΙΟΤΗΤΑ} {self.ΑΝΑΛΩΣΙΜΟ} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} " \
               f"{self.ΤΙΜΗ} {self.ΣΥΝΟΛΟ} {self.ΣΕΛΙΔΕΣ} {self.ΠΕΛΑΤΕΣ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Melanotainies(base):
    __tablename__ = 'ΜΕΛΑΝΟΤΑΙΝΙΕΣ'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    ΕΤΑΙΡΕΙΑ = Column(Text)
    ΠΟΙΟΤΗΤΑ = Column(Text)
    ΑΝΑΛΩΣΙΜΟ = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΤΙΜΗ = Column(Text)
    ΣΥΝΟΛΟ = Column(Text)
    ΠΕΛΑΤΕΣ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Melanotainies(id='%i', ΕΤΑΙΡΕΙΑ='%s', ΠΟΙΟΤΗΤΑ='%s', ΑΝΑΛΩΣΙΜΟ='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s' " \
               "ΤΕΜΑΧΙΑ='%s', ΤΙΜΗ='%s', ΣΥΝΟΛΟ='%s', ΠΕΛΑΤΕΣ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.ΕΤΑΙΡΕΙΑ, self.ΠΟΙΟΤΗΤΑ, self.ΑΝΑΛΩΣΙΜΟ, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ,
               self.ΤΙΜΗ, self.ΣΥΝΟΛΟ, self.ΠΕΛΑΤΕΣ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.ΕΤΑΙΡΕΙΑ} {self.ΠΟΙΟΤΗΤΑ} {self.ΑΝΑΛΩΣΙΜΟ} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} " \
               f"{self.ΤΙΜΗ} {self.ΣΥΝΟΛΟ}  {self.ΠΕΛΑΤΕΣ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Toner(base):
    __tablename__ = 'ΤΟΝΕΡ'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    ΕΤΑΙΡΕΙΑ = Column(Text)
    ΠΟΙΟΤΗΤΑ = Column(Text)
    ΑΝΑΛΩΣΙΜΟ = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΤΙΜΗ = Column(Text)
    ΣΥΝΟΛΟ = Column(Text)
    ΣΕΛΙΔΕΣ = Column(Text)
    ΠΕΛΑΤΕΣ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Toner(id='%i', ΕΤΑΙΡΕΙΑ='%s', ΠΟΙΟΤΗΤΑ='%s', ΑΝΑΛΩΣΙΜΟ='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s' " \
               "ΤΕΜΑΧΙΑ='%s', ΤΙΜΗ='%s', ΣΥΝΟΛΟ='%s', ΣΕΛΙΔΕΣ='%s', ΠΕΛΑΤΕΣ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.ΕΤΑΙΡΕΙΑ, self.ΠΟΙΟΤΗΤΑ, self.ΑΝΑΛΩΣΙΜΟ, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ,
               self.ΤΙΜΗ, self.ΣΥΝΟΛΟ, self.ΣΕΛΙΔΕΣ, self.ΠΕΛΑΤΕΣ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.ΕΤΑΙΡΕΙΑ} {self.ΠΟΙΟΤΗΤΑ} {self.ΑΝΑΛΩΣΙΜΟ} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} " \
               f"{self.ΤΙΜΗ} {self.ΣΥΝΟΛΟ} {self.ΣΕΛΙΔΕΣ} {self.ΠΕΛΑΤΕΣ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Copiers(base):
    __tablename__ = 'ΦΩΤΟΤΥΠΙΚΑ'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    ΕΤΑΙΡΕΙΑ = Column(Text)
    ΠΟΙΟΤΗΤΑ = Column(Text)
    ΑΝΑΛΩΣΙΜΟ = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΚΩΔΙΚΟΣ = Column(Text)
    ΤΕΜΑΧΙΑ = Column(Text)
    ΤΙΜΗ = Column(Text)
    ΣΥΝΟΛΟ = Column(Text)
    ΣΕΛΙΔΕΣ = Column(Text)
    ΠΕΛΑΤΕΣ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΗΣ = Column(Text)

    def __repr__(self):
        return "<Copiers(id='%i', ΕΤΑΙΡΕΙΑ='%s', ΠΟΙΟΤΗΤΑ='%s', ΑΝΑΛΩΣΙΜΟ='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΚΩΔΙΚΟΣ='%s' " \
               "ΤΕΜΑΧΙΑ='%s', ΤΙΜΗ='%s', ΣΥΝΟΛΟ='%s', ΣΕΛΙΔΕΣ='%s', ΠΕΛΑΤΕΣ='%s', ΠΑΡΑΤΗΡΗΣΗΣ='%s')>" \
            % (self.ID, self.ΕΤΑΙΡΕΙΑ, self.ΠΟΙΟΤΗΤΑ, self.ΑΝΑΛΩΣΙΜΟ, self.ΠΕΡΙΓΡΑΦΗ, self.ΚΩΔΙΚΟΣ, self.ΤΕΜΑΧΙΑ,
               self.ΤΙΜΗ, self.ΣΥΝΟΛΟ, self.ΣΕΛΙΔΕΣ, self.ΠΕΛΑΤΕΣ, self.ΠΑΡΑΤΗΡΗΣΗΣ)

    def __str__(self):
        return f"{self.ΕΤΑΙΡΕΙΑ} {self.ΠΟΙΟΤΗΤΑ} {self.ΑΝΑΛΩΣΙΜΟ} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΚΩΔΙΚΟΣ} {self.ΤΕΜΑΧΙΑ} " \
               f"{self.ΤΙΜΗ} {self.ΣΥΝΟΛΟ} {self.ΣΕΛΙΔΕΣ} {self.ΠΕΛΑΤΕΣ} {self.ΠΑΡΑΤΗΡΗΣΗΣ}"


class Orders(base):
    __tablename__ = 'ΧΧΧ'

    ID = Column(Integer, primary_key=True, autoincrement=True)

    ΚΩΔΙΚΟΣ = Column(Text)
    ΗΜΕΡΟΜΗΝΙΑ = Column(Text)
    ΠΕΡΙΓΡΑΦΗ = Column(Text)
    ΠΟΙΟΤΗΤΑ = Column(Text)
    ΑΠΟΤΕΛΕΣΜΑ = Column(Text)
    ΠΑΡΑΤΗΡΗΣΕΙΣ = Column(Text)
    images = Column(Text)

    # image = Column(Text)

    def __repr__(self):
        return ("<Orders(id='%i', ΚΩΔΙΚΟΣ='%s', ΗΜΕΡΟΜΗΝΙΑ='%s', ΠΕΡΙΓΡΑΦΗ='%s', ΠΟΙΟΤΗΤΑ='%s', ΑΠΟΤΕΛΕΣΜΑ='%s', "
                "ΠΑΡΑΤΗΡΗΣΕΙΣ='%s'\ images='%s')>") \
            % (
                self.ID, self.ΚΩΔΙΚΟΣ, self.ΗΜΕΡΟΜΗΝΙΑ, self.ΠΕΡΙΓΡΑΦΗ, self.ΠΟΙΟΤΗΤΑ, self.ΑΠΟΤΕΛΕΣΜΑ, self.ΠΑΡΑΤΗΡΗΣΕΙΣ, self.images)

    def __str__(self):
        return f"{self.ΚΩΔΙΚΟΣ} {self.ΗΜΕΡΟΜΗΝΙΑ} {self.ΠΕΡΙΓΡΑΦΗ} {self.ΠΟΙΟΤΗΤΑ} {self.ΑΠΟΤΕΛΕΣΜΑ} {self.ΠΑΡΑΤΗΡΗΣΕΙΣ} {self.images}"


def search_on_spare_parts(table, text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        parts = session.query(table).filter((table.PARTS_NR.ilike(last_like)) |
                                            (table.ΠΕΡΙΓΡΑΦΗ.ilike(last_like)) |
                                            (table.ΚΩΔΙΚΟΣ.ilike(last_like))). \
            order_by(asc(table.ΠΕΡΙΓΡΑΦΗ))

        return parts
    except Exception:
        traceback.print_exc()
        return


def search_on_consumables(table, text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        parts = session.query(table).filter((table.ΠΕΡΙΓΡΑΦΗ.ilike(last_like)) |
                                            (table.ΚΩΔΙΚΟΣ.ilike(last_like)) |
                                            (table.ΠΕΛΑΤΕΣ.ilike(last_like))). \
            order_by(asc(table.ΠΕΡΙΓΡΑΦΗ))

        return parts
    except Exception:
        traceback.print_exc()
        return


def search_on_orders(text_to_search):
    last_like = f"%{text_to_search.upper()}%"  # για να τα κάνει κεφαλαία αν γράψουμε με μικρά
    # στήν βάση είναι ολλα κεφαλαία αρα θελει κεφαλαία για να βρει
    try:
        parts = session.query(Orders).filter((Orders.ΠΕΡΙΓΡΑΦΗ.ilike(last_like)) |
                                             (Orders.ΚΩΔΙΚΟΣ.ilike(last_like))). \
            order_by(asc(Orders.ΠΕΡΙΓΡΑΦΗ))

        return parts
    except Exception:
        traceback.print_exc()
        return
