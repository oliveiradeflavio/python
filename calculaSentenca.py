#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#Desenvolvido em Python 3.4.4 e Tkinter
#30/11/2016
#Com o intuito de ajudar a classe de Direito da Faculdade
#Flávio Oliveira Consultoria em T.I (Flávio Dicas)
#www.flaviodeoliveira.com.br

from tkinter import *
from fractions import Fraction
from tkinter import messagebox
import webbrowser

#função quando é chamada, abre o link abaixo
def callback(event):
    webbrowser.open_new(r"http://www.flaviodeoliveira.com.br")

#calcular
def conversao():
    try:
        if int(editmeses.get()) > 11:
            messagebox.showwarning("Atenção","Mês tem que ser igual ou menor que 11, pois 12 meses é igual a 1 ano")
        elif int(editdias.get()) > 31:
            messagebox.showwarning("Atenção", "Dia tem que ser menor ou igual a 31. No mês não existe mais que 31 dias")
        else:
            anosConvertido = int(editanos.get()) * 365
            mesesConvertido = int(editmeses.get()) * 30
            total = anosConvertido + mesesConvertido + int(editdias.get())
        
            #Módulo Fraction para fazer a fração digitada no campo Redução
            x = Fraction(editreducao.get())

            z = x * int(total)
            ano = z / 365
        
            if ano > int(editanos.get()):
        
                messagebox.showinfo("Resultado","Tempo de redução maior que o tempo já proposto")
          
            else:
                mes = (z % 365) / 30
                dia = (z % 365) % 30
                messagebox.showinfo("Resultado","Tempo reduzido para %.0f ano(s) %d mês(es) e %d dia(s)\n" % (ano,mes,dia))
    except ValueError:
        messagebox.showwarning("Atenção", "Campos vazios ou preenchidos incorretamente")
        limparcampos()

#função para limpar os campos
def limparcampos():
    editanos.delete(0,END)
    editmeses.delete(0,END)
    editdias.delete(0,END)
    editreducao.delete(0,END)
    editanos.focus()

#form FormPessoa 
formPessoa = Tk()
formPessoa.title("Calcula Sentença 0.01")
formPessoa.geometry("400x320+300+200")
formPessoa.wm_resizable(0,0) 

#título
titulo = Label(formPessoa,text="Calcula Pena")
titulo.grid(row=0,stick=W+E+N+S,pady=10,padx=10)
separa = Frame(height=2, bd=1, relief=SUNKEN)
separa.grid(row=1, stick=W+E+N+S, columnspan=4, pady=15)

#labels
labelanos = Label(formPessoa,text="Anos: ")
labelmeses = Label(formPessoa,text="Meses: ")
labeldias = Label(formPessoa,text="Dias: ")
labelreducao = Label(formPessoa,text="Redução: ")
labelexemplo = Label(formPessoa,text="*Exemplo: 1/2")
labelexemplo2 = Label(formPessoa,text="*Exemplo: 11")
labelexemplo3 = Label(formPessoa,text="*Exemplo: 31")

#entradas (entry)
editanos = Entry()
editmeses = Entry()
editdias = Entry()
editreducao = Entry()

#posicionamento no formulário dos Labels e Edits
labelanos.grid(row=4, sticky=W,padx=15)
editanos.grid(row=4, column=1, pady=5)
labelmeses.grid(row=5, sticky=W,padx=15)
editmeses.grid(row=5, column=1, pady=5)
labeldias.grid(row=6, sticky=W,padx=15)
editdias.grid(row=6, column=1, pady=5)
labelreducao.grid(row=7,sticky=W,padx=15)
editreducao.grid(row=7,column=1,pady=5)
labelexemplo.grid(row=7,column=2,pady=5)
labelexemplo2.grid(row=5,column=2,pady=5)
labelexemplo3.grid(row=6,column=2,pady=5)

#botões 
botoes = Frame()
botaoCalcular = Button(botoes, text="Calcular", command=conversao)
botaoLimpar = Button(botoes, text="Limpar", command=limparcampos)

botaoCalcular.grid(row=1, column=0, pady=10, padx=4)
botaoLimpar.grid(row=1, column=1, pady=10, padx=4)

#label crédito dentro do form Botões
labelcredito = Label(botoes,text="Flávio Oliveira Consultoria em T.I")
labelcredito2 = Label(botoes,text="www.flaviodeoliveira.com.br", fg="blue", cursor="hand2")
labelcredito2.bind("<Button-1>", callback)
labelcredito.grid(row=2,column=0, columnspan=5)
labelcredito2.grid(row=3,column=0, columnspan=5)

#Risco de separação no form               
separa1 = Frame(height=2, bd=1, relief=SUNKEN)
separa1.grid(row=8, stick=W+E+N+S, columnspan=4,pady=15)

botoes.grid(row=9,column=1)

#posiciona automaticamente o parágrafo no primeiro campo na aplicação
editanos.focus()

mainloop()
