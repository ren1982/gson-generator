# from datetime import datetime
# import secrets
#
# from app import db
#
#
# class Lyrics(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     lyrics = db.Column(db.Text, nullable=False)
#     url = db.Column(db.String(10), unique=True)
#     visits = db.Column(db.Integer, default=0)
#     date_created = db.Column(db.DateTime, default=datetime.now)
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.url = self.generate_url()
#
#     def generate_url(self):
#         url = secrets.token_hex(10)
#         item = self.query.filter_by(url=url).first()
#         if item:
#             return self.generate_url()
#         return url