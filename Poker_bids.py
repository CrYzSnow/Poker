##########################################################
#   Programme permettant de gérer une partie de poker    #
#   sans mise physiques. Permet de simplifier            #
#   l'attribution de joueurs, leurs mises et le joueur   #
#   ayant gagné.                                         #
##########################################################

from functools import partial

import tkinter
from tkinter import ttk
import tkinter.font as tkfont

class Joueur:

    def __init__(self,banque,numJoueur) :
        self.numJoueur = numJoueur
        self.banque = banque
        self.__Banque = banque
        self.miseJoueur = 0

    def mise(self,montant) :
        if montant > self.banque or montant <= 0:
            return 0
        self.banque -= montant
        self.miseJoueur += montant

    def ajout(self,montant) :
        if montant <= 0:
            return self.banque
        self.banque += montant
        return self.banque

    def ReInit(self):
        self.banque = self.__Banque
        self.miseJoueur = 0

    def __str__(self) :
        return "Banque : "+str(self.banque)

def unset_intro():
    titre.grid_forget()
    choixJoueur.grid_forget()
    bque.grid_forget()
    banque_montant.grid_forget()
    Start.grid_forget()

def intro():
    global val,titre,choixJoueur,bque,banque_montant,Start

    val = tkinter.IntVar()
    banque_mt = tkinter.IntVar()

    titre = tkinter.Label(fenetre, text="Choisissez le nombre de joueur",height=3,font=font)
    choixJoueur = tkinter.Spinbox(fenetre,from_=1,to=50,justify='center',state='readonly',textvariable=val,width=4)
    bque = tkinter.Label(fenetre, text="Choisissez le montant",height=3,font=font)
    banque_montant = tkinter.Entry(fenetre, textvariable=banque_mt,width=8,justify='center')
    Start = tkinter.Button(fenetre,text = "Start",command=lambda:start(val.get(),banque_mt.get()),height=1,width=6)

    titre.grid(column=0,row=0,padx=5)
    choixJoueur.grid(column=0,row=1,pady=5)
    bque.grid(column=0,row=2)
    banque_montant.grid(column=0,row=3,pady=10)
    Start.grid(column=0,row=4,pady=10)  

def start(nb_joueur,banque_joueur):
    unset_intro()
    global listJoueur,listBanque,labelMise,listValMontant, boxJoueur, nb_j
    nb_j = nb_joueur
    listJoueur = [Joueur(banque_joueur,i) for i in range(nb_joueur)]
    listTitre = [tkinter.Label(fenetre,height=3,font=font,text="Joueur "+str(i+1)) for i in range(nb_joueur)]
    listBanque = [tkinter.Label(fenetre,height=2,text="Banque : "+str(listJoueur[i].banque)) for i in range(nb_joueur)]
    labelMise = [tkinter.Label(fenetre,height=3,text='Mise : 0')for i in range(nb_joueur)]
    listValMontant = [tkinter.IntVar() for i in range(nb_joueur)]
    listEntreeMontantMise = [tkinter.Entry(fenetre,textvariable=listValMontant[i],width=8,justify='center')for i in range(nb_joueur)]
    listButtonMise = [tkinter.Button(fenetre,text='Mise',command=partial(incrementMise,i),height=1,width=6)for i in range(nb_joueur)]
    gagnant = tkinter.Label(fenetre,height=2,text="Choisissez un gagnant :")
    boxJoueur = ttk.Combobox(fenetre,state="readonly",justify='center',width=13,values=[("Joueur "+str(listJoueur[i].numJoueur+1)) for i in range(nb_joueur)])
    boxJoueur.bind("<<ComboboxSelected>>",ChoixGagnant)
    buttonGagnant = tkinter.Button(fenetre,text='Fin de tour',command=fin_de_tour,height=1,width=13)
    buttonReinit = tkinter.Button(fenetre,text='Réinitialiser',command=ReInit,height=1,width=16)
    
    for i in range(len(listJoueur)):
        listTitre[i].grid(column=i,row=0)
        listBanque[i].grid(column=i,row=1,padx=10)
        labelMise[i].grid(column=i,row=2,padx=10,pady=5)
        listEntreeMontantMise[i].grid(column=i,row=3,padx=10)
        listButtonMise[i].grid(column=i,row=4,padx=10)
    gagnant.grid(column=0,row=5,columnspan=nb_joueur,pady=5)
    boxJoueur.grid(column=0,row=6,columnspan=nb_joueur,pady=5)
    buttonGagnant.grid(column=0,row=7,columnspan=nb_joueur,padx=10,pady=5)
    buttonReinit.grid(column=0,row=8,columnspan=nb_joueur,pady=5,padx=10)

def ReInit():
    for i in range(nb_j):
        listJoueur[i].ReInit()
        labelMise[i].config(text="Mise : "+str(listJoueur[i].miseJoueur))
        listBanque[i].config(text="Banque : "+str(listJoueur[i].banque))

def ChoixGagnant(event):
    global gagnant
    gagnant = boxJoueur.get()

def fin_de_tour():
    for i in range(nb_j):
        listJoueur[int(gagnant[-1])-1].ajout(listJoueur[i].miseJoueur)
        listJoueur[i].miseJoueur = 0
    for i in range(nb_j):
        labelMise[i].config(text="Mise : "+str(listJoueur[i].miseJoueur))
        listBanque[i].config(text="Banque : "+str(listJoueur[i].banque))

def incrementMise(joueur):
    mise = listValMontant[joueur].get()
    listJoueur[joueur].mise(mise)
    labelMise[joueur].config(text="Mise : "+str(listJoueur[joueur].miseJoueur))
    listBanque[joueur].config(text="Banque : "+str(listJoueur[joueur].banque))    

fenetre = tkinter.Tk()
fenetre.title('Poker bids')

font = tkfont.Font(size=12,weight="bold")

intro()

fenetre.mainloop()