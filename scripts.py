#!/usr/bin/python3
import subprocess,sys,re
from typing import Text
import qrcode
def use_creation(n1, n2):
    commande = subprocess.Popen("curl -d %s -d %s -X POST http://localhost:8080/creation 2>/dev/stdout" %n1 %n2, shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    if not resultat:
        return "Erreur lors du lancement du script pour la création !"
    else:
        return "Création OK!"

def use_verif(link):
    commande = subprocess.Popen("curl -v -F image=@ %s http://localghost:8080/verification 2>/dev/stdout" %link, shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    if not resultat:
        return "Erreur lors du lancement du script pour la vérification !"
    else:
        return "Vérification OK!"

def get_img_on_server(name):
    commande = subprocess.Popen("curl -v -o %s http://localghost:8080/fond 2>/dev/stdout" %name, shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    if not resultat:
        return "Impossible de récupérer %s" %name
    else:
        return "OK!"
    
def write_on_img(text):
    commande = subprocess.Popen("curl -o texte.png 'http://chart.apis.google.com/chart' --data-urlencode 'chst=d_text_outline' --data-urlencode 'chld=000000|56|h|FFFFFF|b|${%s}' 2>/dev/stdout" %text, shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    if not resultat:
        return "Erreur sur l'écriture de l'image!"
    else:
        return "OK!"

def resize(mon_img):
    commande = subprocess.Popen("mogrify -resize 1000x600 %s 2>/dev/stdout" %mon_img, shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    if not resultat:
        return "Erreur sur le resize"
    else:
        return "OK!"

def make_qr_on_img(data):
    nom_fichier = "qrcode.png"
    qr = qrcode.make(data)
    qr.save(nom_fichier, scale=2)
    
    commande = subprocess.Popen("composite -gravity center texte.png fond_attestation.png combinaison.png 2>/dev/stdout", shell=True,stdout=subprocess.PIPE)
    commande2 = subprocess.Popen("composite -geometry +1418+934 qrcode.png combinaison.png attestation.png 2>/dev/stdout", shell=True,stdout=subprocess.PIPE)

    (resultat1, ignorer) = commande.communicate()
    (resultat2, ignorer) = commande2.communicate()
    if not resultat2 or not resultat1:
        return "Erreur sur la création du QR sur l'image"
    else:
        return "OK!"
    
def get_timestamp():
    commande = subprocess.Popen("openssl ts -query -data texte.png -no_nonce -sha512 -cert -out texte.tsq", shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    if not resultat:
        return "Erreur sur le timestamp"
    else:
        return resultat
    
def get_sign():
    commande = subprocess.Popen("openssl dgst -sha256 texte.png > texte_sign.png", shell=True,stdout=subprocess.PIPE)
    (resultat, ignorer) = commande.communicate()
    if not resultat:
        return "Erreur sur le hashage"
    else:
        return "Ok!"