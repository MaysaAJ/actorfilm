#Importer flask
from flask import Flask,jsonify,abort,request,make_response,url_for
from re import UNICODE
from flask_mysqldb import MySQL
app=Flask(__name__) #mon application lance flask
#import appfilm 
#appel de mysql pour l'utiliser
mysql=MySQL(app)

#configuration a la connection mysql
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='sakila'


#recuperer tache de ma liste de ma bdd
@app.route('/actors/<int:acteur_id>',methods=['GET'])
def get_act_by_id(acteur_id):
    try:
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM actor where actor_id=%s",(str(acteur_id),))
        reponse=cur.fetchone()
        print("I selected the item")
        
        cur.close()
        return jsonify(make_public_acteur(make_acteur(reponse)))

    except Exception as e:
        print(e)
        abort(404)

@app.route('/actors/<int:acteur_id>',methods=['PUT'])
def update_act(acteur_id):
    #PRIX_ACHAT,VOLUME,TITRAGE,ID_MARQUE,ID_Couleur,ID_TYPE
    print("avant get")
    act=get_act_by_id(acteur_id) #j'ai reponse en json
    print("Function update")
    if not request.json:
        abort(400)
    if "first_name" in request.json and type(request.json['first_name'])!=str:
        print("nom")
        abort(400)
    if "last_name" in request.json and type(request.json['last_name']) is not str: 
        print("dans prix")
        abort(400) #descrition pas obligatoire

    if "last_update" in request.json and type(request.json['last_update']) is not str: 
        print("dans last name")
        abort(400)

    try: #parler a bdd

        prenom=request.json.get('first_name',act.json['first_name'])
        nom=request.json.get("last_name",act.json['last_name'])
        dernieremisejour=request.json.get('last_update',act.json['last_update'])
      

        cur=mysql.connection.cursor()
        print("avant update")
        cur.execute("UPDATE actor SET first_name=%s,last_name=%s,last_update=%s where actor_id=%s",(prenom,nom,dernieremisejour,str(acteur_id)))
        print("apres update")
        mysql.connection.commit()
        cur.close()
        return get_act_by_id(acteur_id)
        #TODO CONNECTER A MA BDD
    except Exception as e:
        print(e)
        return jsonify({'is':False})

def delete_film(acteur_id):
    #tache=get_act_by_id(acteur_id) #recuperer une reponse
    try:
        #todo
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM film_actor WHERE actor_id=%s",(str(acteur_id),))
        mysql.connection.commit()
        cur.close()
    
    except Exception as e:
        print(e)
        return jsonify({'is':False})

#route pour supprimer une tache de ma liste dans ma bdd
@app.route('/actors/<int:acteur_id>',methods=['DELETE'])
def delete_act(acteur_id):
    tache=get_act_by_id(acteur_id) #recuperer une reponse
    try:
        #todo
        cur=mysql.connection.cursor()
        delete_film(acteur_id)
        cur.execute("DELETE FROM actor WHERE actor_id=%s",(str(acteur_id),))
        mysql.connection.commit()
        cur.close()
        return tache
    except Exception as e:
        print(e)
        return jsonify({'is':False})


#route pour recuperer la liste des actors
@app.route('/actors',methods=['GET']) #quand tu lances cette route, c'est avec un get
def get_actors():

    try:
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM actor")
        reponse=cur.fetchall()#inverse jsonify #recupere sous forme de tuples et tuples non modifiables
        cur.close()
        actors=[]
        for act in reponse:
            act=make_acteur(act) #je fais ca pour changer format, tache en tuple->tache en objet(tableau)
            actors.append(act)
            
        return jsonify([make_public_acteur(act) for act in actors]) # jsonify conversion of json to response objects.
    except Exception as e:
        print(e)
        abort(404)

#route pour ajouter tache a ma liste dans ma bdd


@app.route('/actors',methods=['POST'])
def create_acteur():
    if not request.json and not "first_name" in request.json:
        abort(400)
    try:


        prenom=request.json['first_name']
        nom=request.json.get('last_name',"") # ""attr par defaut
        misejour=request.json.get('last_update',"")

        #creer ma connection et l'envoyer a la bdd
        cur=mysql.connection.cursor()
      
        cur.execute("INSERT INTO actor(first_name,last_name,last_update) VALUES(%s,%s,%s)",(prenom,nom,misejour))
        mysql.connection.commit()
        cur.close()
        return jsonify({'is':True})
    except Exception as e:
        print(e)
        return jsonify({'is':False})



#annotations app.route('URL')
@app.route('/') #quand je me connecte a cet url, je recupere quoi?  si je dis rien il fait un get
def index():
    return "Hello Maysa"

#fonction pour creer une url d facon dynamique a pactir d'une tache
def make_public_acteur(act): #je veux pas que mes utilisateurs voient id, a la place de l'id je donne url
    public_act={}
    for argument in act:
        if argument=='actor_id':
            #pour que la fonction prenne en parametre id dans app:route on ajoute id en param de url-for
            public_act['url']=url_for('get_act_by_id',acteur_id=act['actor_id'],_external=True) 
        else:
            public_act[argument]=act[argument]

    return public_act

#if ce que je cherche est nul

#fonction pour creer une tache a pactir d'une tache bdd
def make_acteur(acteur_bdd): #recupere en tuple et transformer en liste
    list_acteur=list(acteur_bdd)
    new_acteur={}
    new_acteur['actor_id']=str(list_acteur[0])
    new_acteur['first_name']=str(list_acteur[1])
    new_acteur['last_name']=str(list_acteur[2])
    new_acteur['last_update']=str(list_acteur[3])
    
    return new_acteur

'''@app.route('/films',methods=['GET'])
def afficherfilmes():
    get_films()
'''

@app.route('/films/<int:filme_id>',methods=['GET'])
def get_film_by_id(filme_id):
    try:
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM film where film_id=%s",(str(filme_id),))
        reponse=cur.fetchone()
        print("I selected the item")
        
        cur.close()
        return jsonify(make_public_film(make_film(reponse)))

    except Exception as e:
        print(e)
        abort(404)

@app.route('/films',methods=['GET'])
def get_films():

    try:
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM film")
        reponse=cur.fetchall()#inverse jsonify #recupere sous forme de tuples et tuples non modifiables
        cur.close()
        films=[]
        for unfilm in reponse:
            unfilm=make_film(unfilm) #je fais ca pour changer format, tache en tuple->tache en objet(tableau)
            films.append(unfilm)
            
        return jsonify([make_film(unfilm) for unfilm in films]) # jsonify conversion of json to response objects.
    except Exception as e:
        print(e)
        abort(404)

def make_public_film(unfilm): #je veux pas que mes utilisateurs voient id, a la place de l'id je donne url
    public_unfilm={}
    for argument in unfilm:
        if argument=='film_id':
            #pour que la fonction prenne en parametre id dans app:route on ajoute id en param de url-for
            public_unfilm['url']=url_for('get_unfilm_by_id',film_id=unfilm['film_id'],_external=True) 
        else:
            public_unfilm[argument]=unfilm[argument]

    return public_unfilm

def make_film(film_bdd): #recupere en tuple et transformer en liste
    list_film=list(film_bdd)
    new_film={}
    new_film['film_id']=str(list_film[0])
    new_film['title']=str(list_film[0])
    new_film['description']=str(list_film[2])
    new_film['release_year']=str(list_film[3])
    new_film['language_id']=str(list_film[4])
    new_film['original_language_id']=str(list_film[5])
    new_film['rental_duration']=str(list_film[6])
    new_film['rental_rate']=str(list_film[7])
    new_film['length']=str(list_film[8])
    new_film['replacement_cost']=str(list_film[9])
    new_film['rating']=str(list_film[10])
    new_film['special_features']=str(list_film[11])
    new_film['last_update']=str(list_film[12])
    
    return new_film



#lancer mon application
if __name__=='__main__': 
    app.run(debug=True)