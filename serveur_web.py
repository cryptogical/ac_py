#!/usr/bin/python3
from bottle import route, run, template, request, response
from scripts import *
import qrcode

@route('/creation', method='POST')
def création_attestation():
    contenu_identité = request.forms.get('identite')
    contenu_intitulé_certification = request.forms.get('intitule_certif')
    print('nom prénom :', contenu_identité, ' intitulé de la certification :',
    contenu_intitulé_certification)
    name = contenu_identité.split(" ")
    if len(name) > 2:
        return "Ton nom est trop long mon cher" 
    img = "fond_attestation.png"
    resize(img)
    texte_ligne = "Attestation de réussite|délivrée à %s" % name
    img_with_text = write_on_img(texte_ligne)
    get_timestamp()
    sig = get_sign()
    make_qr_on_img(texte_ligne)
    #f = open("attestation.png", "r")
    #notended, la signature n'est pas correcte
    
    response.set_header('Content-type', 'text/plain')
    return "ok!"

@route('/verification', method='POST')
def vérification_attestation():
    contenu_image = request.files.get('image')
    contenu_image.save('attestation_a_verifier.png',overwrite=True)
    response.set_header('Content-type', 'text/plain')
    return "ok!"

@route('/fond')
def récupérer_fond():
    response.set_header('Content-type', 'image/png')
    descripteur_fichier = open('fond_attestation.png','rb')
    contenu_fichier = descripteur_fichier.read()
    descripteur_fichier.close()
    return contenu_fichier
    
run(host='127.0.0.1',port=8080,debug=True)