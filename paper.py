from tkinter import *
from tkinter import ttk, messagebox

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import os
import locale

#definindo a localização para a conversão da moeda
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

#importando as funções que estão em main.py
from main import *

# cores 
black = "#000000" #letra
silver = "#C0C0C0" #fundo
darkgray = "#A9A9A9" # fundo
gray = "#808080" #letra principal
dimgray = "#696969"


#criando janela
janela = Tk()
janela.title("") 
janela.geometry("490x610")
janela.config(background=darkgray)
janela.resizable(width=False, height=False)

# Frame (São widgets para organizar os espaços de cada item na tela)
frame_cima = Frame(janela, width=500, height=70, backgroun=darkgray, relief="flat")
frame_cima.grid (row=0, column=0, columnspan=2, sticky=NSEW)

frame_meio = Frame(janela, width=500, height=340, background=darkgray, relief="solid")
frame_meio.grid (row=1, column=0, sticky=NSEW)
frame_meioH = Frame(frame_meio, width=500, height=50, background=darkgray, relief="solid")
frame_meioH.grid (row=0, column=0, sticky=NSEW)
frame_meioB = Frame(frame_meio, width=500, height=200, background=darkgray, relief="solid")
frame_meioB.grid (row=2, column=0, sticky=NSEW)


frame_baixo = Frame(janela, width=500, height=200, background=silver, relief="raised")
frame_baixo.grid (row=2, column=0, pady=10, sticky=NSEW)
frame_baixo_P = Frame(frame_baixo, width=500, height=100, background=darkgray, relief="raised")
frame_baixo_P.grid (row=0, column=0, sticky=NSEW)
frame_baixo_D = Frame(frame_baixo, width=500, height=100, background=darkgray, relief="raised")
frame_baixo_D.grid (row=1, column=0, sticky=NSEW)


frame_baixo_S = Frame(frame_baixo, width=500, height=100, background=darkgray, relief="raised")
frame_baixo_S.grid (row=2, column=0, sticky=NSEW)

frame_menu = Frame(janela, width=500, height=50, background=darkgray, relief="raised")
frame_menu.grid (row=3, column=0, sticky=NSEW)

# Frame Cima
logo = Label(frame_cima, text="Folha de Pagamento", compound=LEFT , padx= 5, anchor= NW, font = "arial 22", background=darkgray, fg=dimgray)
logo.place(x = 10, y = 20)


#funções 


#função gerar pdf
def gerar_pdf():
    if e_salario_bruto.get() == "" or e_horas_extras.get()== "" or e_nome.get() =="" or e_cargo.get()=="" or e_cpf.get()=="":
        messagebox.showerror("Erro!", "Preencha todos os campos")
        return
 
    #Obtendo Informações   
    salario_bruto = float(e_salario_bruto.get())
    horas_extras_trabalhadas = int(e_horas_extras.get())
    nome=e_nome.get()
    cpf=e_cpf.get()
    cargo=e_cargo.get()    
    
    #Criando um novo arquivo pdf
    c=canvas.Canvas("first.pdf", pagesize=letter)
    
    c.setFillColorRGB(0.7,0.3,0.2)
    c.rect(0,720,612,100, fill=1)
    
    #Adcionando a logo
    c.drawImage("icons8-visão-da-página-96.png", 50, 725, width=50, height=60)
    
    #Adcionando Nome e Informação da empresa
    nome_empresa="Nome Empresa"
    endereco_empresa="Brasil - Rio de Janeiro"
    
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(1,1,1) #Branco
    c.drawString(220, 760, nome_empresa) #Posição: X, Y
    
    c.setFont("Helvetica", 12)
    c.drawString(220, 740, endereco_empresa)
    
    #linha Decorativa
    c.setStrokeColorRGB(0,0,0)
    c.setLineWidth(1)
    c.line(50,720,562,720)
    
    
    #Dados Pessoais do Trabalhador
    dados_pessoais = {
        "Nome": nome,
        "CPF": cpf,
        "Cargo": cargo
    }
    
    
    c.setFillColorRGB(0,0,0) #Preto
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 670, "Dados Pessoais Do Trabalhador") #Posição: X, Y
    c.setFont("Helvetica", 12)
    
    vertical_posicao = 650
    for chave, valor in dados_pessoais.items():
        c.drawString(70, vertical_posicao, f"{chave}:{valor}")
        vertical_posicao -=20
    
    #calculando as horas extras como provento
    salario_bruto = salario_bruto
    horas_extras_trabalhadas = horas_extras_trabalhadas
    provento_horas_extras = calcular_hora_extra(salario_bruto, horas_extras_trabalhadas) #Chamei a função
    
    
    #proventos
    proventos = {
        "Salário Bruto": salario_bruto,
        "Horas Extras": provento_horas_extras,
    }
    
    #Descontos
    descontos={
        "INSS": calcular_inss(salario_bruto),
        "IRRF": calcular_irrf(salario_bruto)
    }
    
    c.setFillColorRGB(0,0,0) #Preto
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 570, "Proventos: ") #Posição: X, Y
    c.setFont("Helvetica", 12)
    
    vertical_posicao = 550
    for chave, valor in proventos.items():
        c.drawString(70, vertical_posicao, f"{chave}:{valor:.2f}")
        vertical_posicao -=20
    
    #linha Decorativa embaixo do cabeçalho
    c.setStrokeColorRGB(0,0,0)
    c.setLineWidth(1)
    c.line(50,510,562,510)
    
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 490, "Descontos: ") #Posição: X, Y
    c.setFont("Helvetica", 12)
    
    vertical_posicao = 470
    for chave, valor in descontos.items():
        c.drawString(70, vertical_posicao, f"{chave}:{valor:.2f}")
        vertical_posicao -=20
    
    
    
    #Calculando e exibindo o valor liquido a receber
    liquido_receber=sum(proventos.values()) - sum(descontos.values())
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 420, f"Liquido a Receber: R$ {liquido_receber:.2f}") #Posição: X, Y
    
    #linha Decorativa 
    c.setStrokeColorRGB(0,0,0)
    c.setLineWidth(1)
    c.line(50,400,562,400)
    
    #Mensagem de Agradecimento
    mensagem_agradecimento = "Agradecemos por toda sua dedicação!"
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(50, 370, mensagem_agradecimento) #Posição: X, Y
    
    #Assinatura Empresa
    assinatura_empresa = "Nome do Responsável / Cargo"
    c.setFont("Helvetica-Bold", 12)
    c.drawString(380, 340, assinatura_empresa) #Posição: X, Y
    
    
    #Salvando e finalizando o PDF
    c.save()
    
    
    #Mostrando mensagem de sucesso
    messagebox.showinfo("Sucesso!", "Fatura salva com sucesso")





def calcular():
    salario_bruto = float(e_salario_bruto.get())
    horas_extras_trabalhadas = int(e_horas_extras.get())
    
    if e_salario_bruto.get() == "" or e_horas_extras.get()== "":
        messagebox.showerror("Erro! Preencha todos os campos")
        
    #obtendo valores
    
    desconto_inss = calcular_inss(salario_bruto)

    salario_liquido = salario_bruto - desconto_inss

    desconto_irrf = calcular_irrf(salario_liquido)

    aproveito_horas_adicionais = calcular_hora_extra(salario_bruto, horas_extras_trabalhadas)

    salario_final = salario_liquido + aproveito_horas_adicionais - desconto_irrf
    
    #Jogando no front (Para aparecer em proventos (segunda divisão))
    app_salario["text"] = locale.currency(salario_bruto, grouping=True)
    app_horas["text"] = locale.currency(horas_extras_trabalhadas, grouping=True)
    app_inss["text"] = locale.currency(desconto_inss, grouping=True)
    app_irrf["text"] = locale.currency(desconto_irrf, grouping=True)
    
    app_liquido_receber["text"] = locale.currency(salario_final, grouping=True)
    
    
    
    




# Frame Meio
meio1 = Label(frame_meioH, text="Dados do Trabalhador", compound=LEFT , padx= 5, anchor= NW, font = "Arial 13", background=darkgray, fg=dimgray)
meio1.place(x = 9, y = 8)

linha = Label(frame_meioH, width=270 , anchor= NW, font = "Verdana 1", background=gray)
linha.place(x = 190, y = 17)
linha = Label(frame_meioH, width=270 , anchor= NW, font = "Verdana 1", background=darkgray)
linha.place(x = 190, y = 20)

nome = Label(frame_meioB, text="Nome*", anchor= NW, font = "Ivy 10", background=darkgray, fg=black)
nome.grid(row=0, column=0, padx=20, pady=5 , sticky=NSEW)
e_nome=Entry(frame_meioB, width=25, justify="left", relief=SOLID)
e_nome.grid(row=0, column=1, pady=5 , sticky=NSEW)

cpf = Label(frame_meioB, text="CPF*", anchor= NW, font = "Ivy 10", background=darkgray, fg=black)
cpf.grid(row=1, column=0, padx=20, pady=5 , sticky=NSEW)
e_cpf=Entry(frame_meioB, width=25, justify="left", relief=SOLID)
e_cpf.grid(row=1, column=1, pady=5 , sticky=NSEW)

cargo = Label(frame_meioB, text="Cargo*", anchor= NW, font = "Ivy 10", background=darkgray, fg=black)
cargo.grid(row=2, column=0, padx=20, pady=5 , sticky=NSEW)
e_cargo=Entry(frame_meioB, width=25, justify="left", relief=SOLID)
e_cargo.grid(row=2, column=1, pady=5 , sticky=NSEW)

salario_bruto = Label(frame_meioB, text="Salário Bruto*", anchor= NW, font = "Ivy 10", background=darkgray, fg=black)
salario_bruto.grid(row=3, column=0, padx=20, pady=5 , sticky=NSEW)
e_salario_bruto=Entry(frame_meioB, width=25, justify="center", relief=SOLID)
e_salario_bruto.grid(row=3, column=1, pady=5 , sticky=NSEW)

horas_extras = Label(frame_meioB, text="Horas Extras*", anchor= NW, font = "Ivy 10", background=darkgray, fg=black)
horas_extras.grid(row=3, column=2, padx=20, pady=5 , sticky=NSEW)
e_horas_extras=Entry(frame_meioB, width=8, justify="center", relief=SOLID)
e_horas_extras.grid(row=3, column=3, pady=5 , sticky=NSEW)


# Frame Baixo
meio1 = Label(frame_baixo_P, text="Proventos", compound=LEFT , padx= 5, anchor= NW, font = "Arial 13", background=darkgray, fg=dimgray)
meio1.place(x = 9, y = 8)

linha = Label(frame_baixo_P, width=361, anchor= NW, font = "Verdana 1", background=gray)
linha.place(x = 100, y = 17)
linha = Label(frame_baixo_P, width=361 , anchor= NW, font = "Verdana 1", background=darkgray)
linha.place(x = 100, y = 20)

l_salario = Label(frame_baixo_P, text="Salário Bruto", compound=LEFT, padx=5, anchor= NW, font = "Arial 10", background=darkgray, fg=black)
l_salario.place(x = 20, y = 40)
app_salario = Label(frame_baixo_P, compound=LEFT, padx=5, anchor= NW, font = "Arial 10 bold", background=darkgray, fg=black)
app_salario.place(x = 152, y = 40)

l_horas = Label(frame_baixo_P, text="Horas Extras", compound=LEFT, padx=5, anchor= NW, font = "Arial 10", background=darkgray, fg=black)
l_horas.place(x = 20, y = 70)
app_horas = Label(frame_baixo_P, compound=LEFT, padx=5, anchor= NW, font = "Arial 10 bold", background=darkgray, fg=black)
app_horas.place(x = 152, y = 70)



meio2 = Label(frame_baixo_D, text="Descontos", compound=LEFT , padx= 5, anchor= NW, font = "Arial 13", background=darkgray, fg=dimgray)
meio2.place(x = 9, y = 8)

linha = Label(frame_baixo_D, width=361, anchor= NW, font = "Verdana 1", background=gray)
linha.place(x = 100, y = 17)
linha = Label(frame_baixo_D, width=361 , anchor= NW, font = "Verdana 1", background=darkgray)
linha.place(x = 100, y = 20)

l_inss = Label(frame_baixo_D, text="INSS", compound=LEFT, padx=5, anchor= NW, font = "Arial 10", background=darkgray, fg=black)
l_inss.place(x = 20, y = 40)
app_inss = Label(frame_baixo_D, compound=LEFT, padx=5, anchor= NW, font = "Arial 10 bold", background=darkgray, fg=black)
app_inss.place(x = 152, y = 40)

l_irrf = Label(frame_baixo_D, text="IRRF", compound=LEFT, padx=5, anchor= NW, font = "Arial 10", background=darkgray, fg=black)
l_irrf.place(x = 20, y = 70)
app_irrf = Label(frame_baixo_D, compound=LEFT, padx=5, anchor= NW, font = "Arial 10 bold", background=darkgray, fg=black)
app_irrf.place(x = 152, y = 70)


meio3 = Label(frame_baixo_S, text="Liquído a receber", compound=LEFT , padx= 5, anchor= NW, font = "Arial 13", background=darkgray, fg=dimgray)
meio3.place(x = 9, y = 8)

linha = Label(frame_baixo_S, width=300, anchor= NW, font = "Verdana 1", background=gray)
linha.place(x = 161, y = 17)
linha = Label(frame_baixo_S, width=300 , anchor= NW, font = "Verdana 1", background=darkgray)
linha.place(x = 161, y = 20)


app_liquido_receber = Label(frame_baixo_S, width=18 , compound=LEFT, padx=5, anchor= E, font = "Arial 20 bold", background=darkgray, fg=black)
app_liquido_receber.place(x = 152, y = 40)

#Menu
b_folha_pagamento = Button(frame_menu, command=calcular, anchor=NW, text="Calcular Pagamento", bg=black, fg=silver, font = "Ivy 10", overrelief=RIDGE, relief=GROOVE)
b_folha_pagamento.grid(row=0, column=0, sticky=NSEW, padx=10, pady=6)

b_gerar_pdf = Button(frame_menu, command=gerar_pdf,anchor=NW, text="Gerar documento PDF", bg=black, fg=silver, font = "Ivy 10", overrelief=RIDGE, relief=GROOVE)
b_gerar_pdf.grid(row=0, column=2, sticky=NSEW, padx=10, pady=6)



janela.mainloop()