from peewee import *

recipes_db = SqliteDatabase('db/recipes.db')
forecast_db = SqliteDatabase('db/forecast.db')


class Menu(Model):
    id = PrimaryKeyField()
    week = CharField()
    version = CharField()
    comment = CharField()

    class Meta:
        database = recipes_db
    @property
    def serialize(self):
        data = {
            'id': self.id,
            'week': str(self.week).strip(),
            'version': str(self.version).strip(),
            'comment': str(self.comment).strip(),
        }

        return data

    def __repr__(self):
        return "{}, {}, {}, {}".format(
            self.id,
            self.week,
            self.version,
            self.comment,
        )


class Recipe(Model):
    id = PrimaryKeyField()
    name = CharField()

    class Meta:
        database = recipes_db


class Ingredients(Model):
    id = PrimaryKeyField()
    name = CharField()
    price = FloatField()

    class Meta:
        database = recipes_db


class Mealkit(Model):
    id = PrimaryKeyField()
    menu = ForeignKeyField(Menu, backref='mealkits')
    slot = IntegerField()
    recipe = ForeignKeyField(Recipe, backref='mealkits')

    class Meta:
        database = recipes_db


class MealkitIngredient(Model):
    id = PrimaryKeyField()
    mealkit = ForeignKeyField(Mealkit, backref='ingredients')
    sku = ForeignKeyField(Ingredients)
    qty_needed = IntegerField()

    class Meta:
        database = recipes_db


with recipes_db:
    Menu.create_table()
    Recipe.create_table()
    Ingredients.create_table()
    Mealkit.create_table()
    MealkitIngredient.create_table()
