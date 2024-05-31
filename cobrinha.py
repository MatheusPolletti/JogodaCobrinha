from tkinter import *
import random

LINHAS = 25
COLUNAS = 25
TAMANHO_BLOCO = 25

LARGURA_JANELA = TAMANHO_BLOCO * LINHAS
ALTURA_JANELA = TAMANHO_BLOCO * COLUNAS

class Tile:
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

largura_janela = janela.winfo_width()
altura_janela = janela.winfo_height()
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
janela_x = int((largura_tela / 2) - (largura_janela / 2))
janela_y = int((altura_tela / 2) - (altura_janela / 2))
janela.geometry(f'{largura_janela}x{altura_janela}+{janela_x}+{janela_y}')

cobra = Tile(random.randint(2, 16)*TAMANHO_BLOCO, random.randint(2, 16)*TAMANHO_BLOCO)
cobra_corpo = []
comida = Tile(random.randint(2, 16)*TAMANHO_BLOCO, random.randint(2, 16)*TAMANHO_BLOCO)

velocidade_x = 0
velocidade_y = 0

game_over = False
pontuacao = 0

def mudar_direcao(evento):
    global velocidade_x, velocidade_y, pontuacao, cobra_corpo, game_over, cobra, comida
    #print(evento.keysym)

    if (evento.keysym == 'Return' and game_over == True):
        game_over = False
        
        pontuacao = 0
        cobra_corpo = []
    
        cobra = Tile(random.randint(2, 22)*TAMANHO_BLOCO, random.randint(2, 22)*TAMANHO_BLOCO)
        comida = Tile(random.randint(2, 22)*TAMANHO_BLOCO, (random.randint(2, 22)*TAMANHO_BLOCO))

        velocidade_x = 0
        velocidade_y = 0

        return

    if (game_over):
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

    if (game_over):
        return

    if (cobra.x < 0 or cobra.x >= LARGURA_JANELA or cobra.y < 0 or cobra.y >= ALTURA_JANELA):
        game_over = True
        return
    
    for tile in cobra_corpo:
        if (cobra.x == tile.x and cobra.y == tile.y):
            game_over = True
            return

    if (cobra.x == comida.x and cobra.y == comida.y):
        cobra_corpo.append(Tile(comida.x, comida.y))
        comida.x = random.randint(0, COLUNAS - 1) * TAMANHO_BLOCO
        comida.y = random.randint(0, LINHAS-1) * TAMANHO_BLOCO
        pontuacao += 1

    for i in range(len(cobra_corpo) -1, -1, -1):
        tile = cobra_corpo[i]
        if (i == 0):
            tile.x = cobra.x
            tile.y = cobra.y
        else:
            prev_tile = cobra_corpo[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    cobra.x += velocidade_x * TAMANHO_BLOCO
    cobra.y += velocidade_y * TAMANHO_BLOCO


def desenhar():
    global cobra, comida, cobra_corpo, game_over, pontuacao
    
    mover()

    canvas.delete('all')

    canvas.create_rectangle(comida.x, comida.y, comida.x + TAMANHO_BLOCO, comida.y + TAMANHO_BLOCO, fill='#E6471B')

    canvas.create_rectangle(cobra.x, cobra.y, cobra.x + TAMANHO_BLOCO, cobra.y + TAMANHO_BLOCO, fill='#1E89E5')
    
    for tile in cobra_corpo:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TAMANHO_BLOCO, tile.y + TAMANHO_BLOCO, fill='#1E89E5')

    if (game_over):
        canvas.delete('all')    
        canvas.create_text(largura_janela / 2, altura_janela / 2 - 70, font='Arial 20', text=f'               Game Over\n\n          Você comeu {pontuacao} frutas\n\nAperte Enter pra jogar novamente', fill='#F0EADC')
    else:
        canvas.create_text(54, 15, font='Arial 12', text=f'Pontuação: {pontuacao}', fill='#F0EADC')

    janela.after(100 - (pontuacao * 4), desenhar)


desenhar()

janela.bind('<KeyRelease>', mudar_direcao)

janela.mainloop()
