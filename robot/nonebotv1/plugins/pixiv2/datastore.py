'''
@Date: 2020-04-04 18:01:40
@LastEditors: code
@Author: code
@LastEditTime: 2020-04-07 21:26:03
'''

from peewee import IntegerField, TimestampField, Model, CharField, SqliteDatabase, AutoField, chunked, ForeignKeyField, BooleanField, fn
from typing import Dict, List, Tuple

db = SqliteDatabase('./db/app_storage_v1.db')


class BaseModel(Model):
    class Meta:
        database = db


class ArtWork(BaseModel):
    illust_id = IntegerField(unique=True, index=True)
    illust_type = IntegerField(index=True)
    page_count = IntegerField()
    timestamp = TimestampField()
    upload_time = CharField()
    is_full_upload = BooleanField(default=False)


# class SingleImage(BaseModel):
#     page_index = IntegerField()
#     url = CharField(unique=True, index=True)
#     delay = IntegerField(default=0)
#     object_id = CharField()
#     art_work = ForeignKeyField(ArtWork, backref='single_images')

class SingleImage2(BaseModel):
    illust_id = IntegerField(index=True)
    page_index = IntegerField()
    url = CharField(unique=True, index=True)
    delay = IntegerField(default=0)
    object_id = CharField()
    # art_work = ForeignKeyField(ArtWork, backref='single_image2s')


def add_datastore(book_marks: List[Tuple]):
    with db.atomic():
        for batch in chunked(book_marks, 100):
            insert = ArtWork.insert_many(
                batch,
                fields=(
                    ArtWork.illust_id, ArtWork.illust_type,
                    ArtWork.page_count, ArtWork.upload_time,
                    ArtWork.timestamp
                )
            )
            insert.on_conflict_ignore().execute(db)


# db.connect()
# db.create_tables([ArtWork, SingleImage2])
