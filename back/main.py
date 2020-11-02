from flask import *
from models import forecast_db, recipes_db, Menu, Recipe, Mealkit, MealkitIngredient, Ingredients
from peewee import *
from flask import Flask
from flask_cors import CORS
from flask_peewee.rest import RestAPI
import json
app = Flask(__name__)
CORS(app)

@app.route('/api/Volume/<string:week>', methods=['GET'])#this line lead to the following : if you search to the api with the week, '2018-W48' for instance, you'll enter the function with the same week, in this case, '2018-W48'
def volumes(week):
    SQL_quer_numb='SELECT number from FORECAST WHERE week=='+ str('\'')+week+str('\'') #at first I write sql queries on the forecast database to get the number and the slot of the mealkits for the given week
    SQL_quer_slot='SELECT slot from FORECAST WHERE week=='+ str('\'')+week+str('\'')#the str('\'') was the only way i found to put '' in a string, without messing everything up
    slots=[]
    volume=[]
    SlotVol=[]
    Menu_id_amount=[] #=data21
    Ingredient_amount=[]
    response=[]
    slots_dat=forecast_db.execute_sql(SQL_quer_slot)
    numbers_dat=forecast_db.execute_sql(SQL_quer_numb)
    for value, in slots_dat:
        slots+=[value]
    for value, in numbers_dat:
        volume+=[value]
    for i in range(len(volume)):
        SlotVol+=[(slots[i],volume[i])] #this list is composed of tuples of the slot of the menu, and the amount of it that is forecasted
    SlotVol=SlotVol+SlotVol #there are 20 slots for every week, but there are two versions of every mealkit (I'm not sure I understood that part though), so I had to append this list with itself
    query_idMenu = Menu.select(Menu.id).where(Menu.week == week) #this query returns the menus of the boxes that are planned to be prepared the week of the query
    query_recipies=Mealkit.select(Mealkit.recipe).where((Mealkit.menu<<query_idMenu) & (Mealkit.slot<<slots)) #this query gets the recipes' id of the selected menus, given the corresponding slots
    recipes_id = [i for i, in query_recipies.tuples()]#this line simply gets the data of the query_recipes in a variable
    for i in range (len(recipes_id)):#the idea of the next two lines is to create a list of tuples, in order to multiply the final number of each ingredient by the number of times this recipe needs to be made
        Menu_id_amount+=[(recipes_id[i],SlotVol[i][1])] #the id of the recipes, and the number of menus at this id (0 : recipes id, 1 : number of recipes that needs to be made)
    for i in range(len(recipes_id)):#the next step is to get the sku and the quantity needed from the Mealkitingredient table, given the id of the recipe
        qur_sku=MealkitIngredient.select(MealkitIngredient.sku).where(MealkitIngredient.mealkit==recipes_id[i])#the first request queries the sku of the ingredients needed, given that the mealkit id corresponds
        qur_quant=MealkitIngredient.select(MealkitIngredient.qty_needed).where(MealkitIngredient.mealkit==recipes_id[i])#the second request queries the quantity of ingredient need for one recipe
        data_sku= [i for i, in qur_sku.tuples()]#here I just convert the query into data
        data_quant = [i for i, in qur_quant.tuples()]#same thing here
        for j in range (len(data_sku)):#since recipes can use different ingredients, I need to do a loop for each recipe, in order to get the number of ingredients needed
            Ingredient_amount+=[(data_sku[j],data_quant[j]*Menu_id_amount[i][1])] #0 : id ingredient, 1 : number needed
    for i in range(len(Ingredient_amount)):#now the final part : i just need to get the name of each ingredient
       qur_name=Ingredients.select(Ingredients.name).where(Ingredients.id==Ingredient_amount[i][0]) #query to get the name
       data_name=[i for i, in qur_name.tuples()]#data conversion
       name = {'name':data_name[0]}#I then create dictionnary for each key, I'm not sure if it was necessary but it worked
       sku={'sku':Ingredient_amount[i][0]}
       quantity={'quantity':Ingredient_amount[i][1]}
       name.update(quantity)#here I concatenate the tables
       name.update(sku)
       response+=[name]#here i simply put the dictionnary in the table, once again, not sure if that was necessary but it worked
    return json.dumps(response)

@app.route('/api/weeks/', methods=['GET'])#the second api request is simpler : it just gives the availables week you can see the forecast from
def GiveWeeks():
    weeks=[]
    query='SELECT DISTINCT(week) FROM forecast'#once again, a SQL request, but to get the weeks this time
    results=forecast_db.execute_sql(query)#what's following is the same thing that in the previous query
    for value, in results:
        value2={'text':value}
        weeks+=[value2]
    return json.dumps(weeks)

if __name__=='__main__':
    app.run()
