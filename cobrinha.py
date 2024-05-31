from tkinter import *
from random import randint

BLOCOS = 25
TAMANHO_BLOCO = 25

LARGURA_JANELA = TAMANHO_BLOCO * BLOCOS
ALTURA_JANELA = TAMANHO_BLOCO * BLOCOS

class Quadrado:
    def __init__(self, x, y):
        self.x = x
        self.y = y

janela = Tk()

icone = PhotoImage(file='logo.png')
janela.iconphoto(True, icone)

janela.title('Jogo da Cobra')
janela.resizable(False, False)

canvas = Canvas(janela, bg='black', width=LARGURA_JANELA, height=ALTURA_JANELA, borderwidth=0, highlightthickness=0)
canvas.pack()
janela.update()

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
posicao_x = int((largura_tela / 2) - (LARGURA_JANELA / 2))
posicao_y = int((altura_tela / 2) - (ALTURA_JANELA / 2)) - 20
janela.geometry(f'{LARGURA_JANELA}x{ALTURA_JANELA}+{posicao_x}+{posicao_y}')

cobra = Quadrado(randint(2, 16) * TAMANHO_BLOCO, randint(2, 16) * TAMANHO_BLOCO)
cobra_corpo = []
comida = Quadrado(randint(2, 20) * TAMANHO_BLOCO, randint(2, 20) * TAMANHO_BLOCO)

velocidade_x = 0
velocidade_y = 0

game_over = False
pontuacao = 0

def mudar_direcao(evento):
    global velocidade_x, velocidade_y, pontuacao, cobra_corpo, game_over, cobra, comida

    if (evento.keysym == 'Return' and game_over == True):
        game_over = False
        
        pontuacao = 0
        cobra_corpo = []
    
        cobra = Quadrado(randint(2, 16) * TAMANHO_BLOCO, randint(2, 16) * TAMANHO_BLOCO)
        comida = Quadrado(randint(2, 24) * TAMANHO_BLOCO, (randint(2, 24) * TAMANHO_BLOCO))

        velocidade_x = 0
        velocidade_y = 0

        return

    if game_over == True:
        return
    
    if (evento.keysym == 'Up' or evento.keysym == 'w') and velocidade_y != 1:
        velocidade_x = 0
        velocidade_y = -1
    elif (evento.keysym == 'Down' or evento.keysym == 's') and velocidade_y != -1:
        velocidade_x = 0
        velocidade_y = 1
    elif (evento.keysym == 'Left' or evento.keysym == 'a') and velocidade_x != 1:
        velocidade_x = -1
        velocidade_y = 0
    elif (evento.keysym == 'Right' or evento.keysym == 'd') and velocidade_x != -1:
        velocidade_x = 1
        velocidade_y = 0


def mover():
    global cobra, comida, cobra_corpo, game_over, pontuacao

    if game_over == True:
        return

    if (cobra.x < 0 or cobra.x >= LARGURA_JANELA or cobra.y < 0 or cobra.y >= ALTURA_JANELA):
        game_over = True
        return
    
    for parte in cobra_corpo:
        if (cobra.x == parte.x and cobra.y == parte.y):
            game_over = True
            return

    if (cobra.x == comida.x and cobra.y == comida.y):
        cobra_corpo.append(Quadrado(comida.x, comida.y))

        comida.x = randint(0, 24) * TAMANHO_BLOCO
        comida.y = randint(0, 24) * TAMANHO_BLOCO
        
        pontuacao += 1

    for posicao in range(len(cobra_corpo) -1, -1, -1):
        parte_quadrado = cobra_corpo[posicao]

        if (posicao == 0):
            parte_quadrado.x = cobra.x
            parte_quadrado.y = cobra.y
        else:
            anterior_parte_quadrado = cobra_corpo[posicao - 1]
            parte_quadrado.x = anterior_parte_quadrado.x
            parte_quadrado.y = anterior_parte_quadrado.y

    cobra.x += velocidade_x * TAMANHO_BLOCO
    cobra.y += velocidade_y * TAMANHO_BLOCO


def desenhar():
    global cobra, comida, cobra_corpo, game_over, pontuacao
    
    mover()

    canvas.delete('all')

    canvas.create_rectangle(comida.x, comida.y, comida.x + TAMANHO_BLOCO, comida.y + TAMANHO_BLOCO, fill='#E6471B')

    canvas.create_rectangle(cobra.x, cobra.y, cobra.x + TAMANHO_BLOCO, cobra.y + TAMANHO_BLOCO, fill='#1E89E5')
    
    for parte in cobra_corpo:
        canvas.create_rectangle(parte.x, parte.y, parte.x + TAMANHO_BLOCO, parte.y + TAMANHO_BLOCO, fill='#1E89E5')

    if game_over == True:
        canvas.delete('all')
        canvas.create_text(LARGURA_JANELA / 2, ALTURA_JANELA / 2 - 70, font='Arial 20', text=f'               Game Over\n\n          Você comeu {pontuacao} frutas\n\nAperte Enter pra jogar novamente', fill='#F0EADC')
    else:
        canvas.create_text(54, 15, font='Arial 12', text=f'Pontuação: {pontuacao}', fill='#F0EADC')

    janela.after(100 - int((pontuacao * 4.2)), desenhar)


desenhar()

janela.bind('<KeyRelease>', mudar_direcao)

janela.mainloop()
