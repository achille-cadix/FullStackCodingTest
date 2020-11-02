Here is the V1 ! with comments on the code and a few adjustments here and there

== Requirements ==

Front end : only npm I think, the rest is installed in the folder
Backend : python 3, flask and peewee (pip install peewee flask flask_cors flask-peewee)

== Run the servers ==

Backend : 
open a console in '/CodingTestAchilleV1/back'
type 'python main.py'
Now the backend server should run, and you'll be able to access the api through your browser
by going to the address 'http://127.0.0.1:5000/api/Volume/2018-W48' for the week 48

Frontend :
open a console in '/CodingTestAchilleV1/front/client'
type 'npm run serve'
Now you should be able to view the name of the products and their volume requiered at 'http://localhost:8080/'

== V1 ==
I've changed a few things since the last version : I added the sku number in the frontend, and also made the frontend a little bit more good looking
Moreover, the table is automatically sorted by name.
Most of the changes are comments, mainly in the backend main.py, in which I explain everystep of my program.
There is also some comments in front/client/src/App.vue and front/client/src/components/stableau.vue


Hope you'll like my work, I found this test very stimulant, I've learned at lot. It also really made me want work as a developper, I know I've barely touched the tip of the iceberg, and I'd like to learn even more.

Anyway thanks for your time, I appreciate it,
Achille