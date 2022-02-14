from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
motdepasse=os.getenv("password")
hote=os.getenv("host")
utilisateur=os.getenv("user")
dialecte=os.getenv("dialect")

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="{0}://{1}:{2}@{3}/bibliotheque".format(dialecte,utilisateur,motdepasse,hote)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

##########################################################################
#                              CREATION DES CLASSES
##########################################################################

#La classe Catégorie
class Categorie(db.Model):
        __tablename__="categories"
        id=db.Column(db.Integer,primary_key=True)
        libelle_categorie=db.Column(db.String(50),nullable=False)
        livres=db.relationship('Livre',backref="categories",lazy=True)
        
        def __init__(self,libelle):
                self.libelle_categorie=libelle;
                
        def inserer(self):
                db.session.add(self)
                db.session.commit()
                
        def modifier(self):
                db.session.commit()

        def supprimer(self):
                db.session.delete(self)
                db.session.commit()
        def afficher(self):
                return{
                        "Identifiant":self.id,
                        "Libelle":self.libelle_categorie
                }
        
        
        
#La classe livre
class Livre(db.Model):
        __tablename__="livres"
        id=db.Column(db.Integer,primary_key=True)
        isbn=db.Column(db.String(30),nullable=False)
        titre=db.Column(db.String(30),nullable=False)
        date_publication=db.Column(db.Date,nullable=False)
        auteur=db.Column(db.String(30),nullable=False)
        editeur=db.Column(db.String(30),nullable=False)
        categorie_id=db.Column(db.Integer,db.ForeignKey('categories.id'),nullable=False)
        
        def __init__(self,isbn,titre,date,auteur,editeur,categorie_id):
                        self.isbn=isbn
                        self.titre=titre
                        self.date_publication=date
                        self.auteur=auteur
                        self.editeur=editeur
                        self.categorie_id=categorie_id
                
        def inserer(self):
                db.session.add(self)
                db.session.commit()
                
        def modifier(self):
                db.session.commit()

        def supprimer(self):
                db.session.delete(self)
                db.session.commit()
        def afficher(self):
                return{
                        
                        "Identifiant":self.id,
                        "Code ISBN":self.isbn,
                        "Titre":self.titre,
                        "Date de la publication ":self.date_publication,
                        "Auteur":self.auteur,
                        "Editeur":self.editeur,
                        "Identifant Categorie":self.categorie_id
                }

db.create_all()


##########################################################################
#                              LES ROUTES CONCERNANTS LES CATEGORIES
##########################################################################        
@app.route("/categories",methods=['GET'])
def liste_categorie():
        cat=Categorie.query.all()
        list_cat=[c.afficher() for c in cat ]
        return jsonify(
                {
                        "Etat":"Success",
                        "Liste des categories":list_cat,
                        "Nombre de catégories":Categorie.query.count()
                }
        )
        
@app.route("/categories/<int:id>",methods=['GET'])
def rechercher_categorie(id):
        cat=Categorie.query.get(id)
        if cat is not None:
                return jsonify(
                        {
                                "Etat de la recherche":"success",
                                "Categorie recherchee":cat.afficher()
                        }
                        
                )
        else:
                abort(404)
        
@app.route("/categories",methods=['POST'])
def ajouter_categorie():
        try:
                body=request.get_json()
                lib=body.get("libelle",None)
                cat=Categorie(libelle=lib)
                cat.inserer()
                return jsonify(
                        {
                                "Etat ajout":"success",
                                "categorie ajoutee":cat.afficher(),
                                "Total des categories":Categorie.query.count()
                        }
                )
        except :
                abort(400)


@app.route("/categories/<int:id>",methods=['DELETE'])
def supprimer_categorie(id):
        catsup=Categorie.query.get(id)
        if(catsup is None):
                abort(404)
        else:
                catsup.supprimer()
                
                listCat=[c.afficher() for c in Categorie.query.all()]
                
                return jsonify(
                        {
                                "Etat de suppression":"success",
                                "Categorie suprimee":catsup.afficher(),
                                "Categories restantes":listCat,
                                "Nombre restant":len(listCat)
                        }
                )
        
@app.route("/categories/<int:id>",methods=['PATCH'])

def modifier_categorie(id):
        cat=Categorie.query.get(id)
        if cat is None:
                abort(404)
                
        b=request.get_json()
        cat.libelle_categorie=b.get("libelle",cat.libelle_categorie)
        if(cat.libelle_categorie is None):
                abort(400)
        else:
                cat.modifier()
                return jsonify(
                        {
                                "Etat de la modification":"succes",
                                "Categorie modifiee":cat.afficher()
                        }
                )
        
##########################################################################
#                              LES ROUTES CONCERNANTS LES LIVRES
########################################################################## 
@app.route("/livres",methods=['GET'])
def liste_livre():
        livres=Livre.query.all()
        list_liv=[c.afficher() for c in livres ]
        return jsonify(
                {
                        "Etat":"Succes",
                        "Liste des livres":list_liv,
                        "Nombre de livres":Livre.query.count()
                }
        )
        
@app.route("/livres/<int:id>",methods=['GET'])
def rechercher_livre(id):
        liv=Livre.query.get(id)
        if liv is None:
                abort(404)
        else:
                return jsonify(
                        {
                                "Etat de la recherche":"succes",
                                "Livre recherche":liv.afficher()
                        }
                        
                )
        
@app.route("/livres",methods=['POST'])
def ajouter_livre():
       try:
                body=request.get_json()
                isbn=body.get("Code ISBN")
                title=body.get("Titre")
                dat_list=body.get("Date de la publication").split("-")
                #Le format de la date doit être AAAA-MM-JJ
                dat=datetime(int(dat_list[0])  , int(dat_list[1]),int(dat_list[2])).date()
                autor=body.get("Auteur")
                editor=body.get("Editeur")
                id_cat=body.get("Identifiant Categorie")
                liv=Livre(isbn=isbn,titre=title,date=dat,auteur=autor,editeur=editor,categorie_id=id_cat)
                liv.inserer()
                return jsonify(
                        {
                                "Etat de l'ajout":"success",
                                "Livre ajoute":liv.afficher(),
                                "Total des livres":Livre.query.count()
                        }
                )
       except:
               abort(400)

@app.route("/livres/<int:id>",methods=['DELETE'])
def supprimer_livre(id):
        livsup=Livre.query.get(id)
        if livsup is None:
                abort(404)
        else:
                livsup.supprimer()
                
                listLiv=[c.afficher() for c in Livre.query.all()]
                
                return jsonify(
                        {
                                "Etat de suppression":"success",
                                "Livre suprimee":livsup.afficher(),
                                "Livre restants":listLiv,
                                "Nombre restant":len(listLiv)
                        }
                )

@app.route("/livres/<int:id>",methods=['PATCH'])
def modifier_livre(id):
        liv=Livre.query.get(id)
        if liv is None:
                abort(404)
        else:
                try:
                        body=request.get_json()
                        liv.isbn=body.get("Code ISBN",liv.isbn)
                        liv.titre=body.get("Titre",liv.titre)
                        liv.date_publication=body.get("Date de la publication",liv.date_publication)
                        liv.auteur=body.get("Auteur", liv.auteur)
                        liv.editeur=body.get("Editeur", liv.editeur)
                        liv.categorie_id=body.get("Identifant Categorie",liv.categorie_id)
                        
                        liv.modifier()
                        return jsonify(
                                {
                                        "Etat de la modification":"success",
                                        "Livre modifie":liv.afficher()
                                }
                                )
                except :
                        abort(400)
                
@app.route('/livres/<int:id_cat>/categories',methods=['GET'])
def liste_livre_categorie(id_cat):
        cat=Categorie.query.get(id_cat)
        if cat is None:
                abort(404)
        else:
                livres=Livre.query.filter_by(categorie_id= id_cat)
                
                if livres.count()==0:
                        liste_livre="Aucun"
                else:
                        liste_livre=[l.afficher() for l in livres]
                
                
                return jsonify(
                        {
                                "Etat de la recherche":"success",
                                "Categorie":cat.libelle_categorie,
                                "Nombre de livre":len(liste_livre),
                                "Les livres trouves":liste_livre
                                
                        }
                )
                
##########################################################################
#                                                  LA GESTION DES EXCEPTIONS
##########################################################################

@app.errorhandler(404)
def introuvalbe(error):
        return jsonify(
                {
                        "Etat":"Echec",
                        "Type d'erreur":404,
                        "Cause":"Elément non trouve"
                }
        ),404
        
        
@app.errorhandler(400)
def erreur_client(error):
        return jsonify(
                {
                        "Etat":"Echec",
                        "Type d'erreur":400,
                        "Cause":"Element envoye non valide"
                }
        ),400
        
@app.errorhandler(500)
def erreur_serveur(error):
        return jsonify(
                {
                        "Etat":"Echec",
                        "Type d'erreur":500,
                        "Cause":"L'API a eu un disfonctionnement"
                }
        ),500
