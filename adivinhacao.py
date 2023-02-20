import random


def jogar():
    print("************************************")
    print("Bem-vindo ao jogo de Adivinhação!")
    print("************************************")

    numero_secreto = random.randrange(1, 101)  # numero entre 0.0 e 1.0
    total_de_tentativas = 0
    pontos = 1000

    print("Está se sentindo sortudo? Escolha sua dificuldade:")
    print("LvL '1' Fácil - LvL '2' Médio  - LvL '3' Difícil")

    nivel = int(input("Defina o nível:"))

    if nivel == 1:
        total_de_tentativas = 20
    elif nivel == 2:
        total_de_tentativas = 10
    else:
        total_de_tentativas = 5

    print(numero_secreto)  # EXCLUIR DEPOIS DE TUDO PRONTO / PARA TESTE

    for rodada in range(1, total_de_tentativas + 1):
        print("Tentativa  {} de {} ".format(rodada, total_de_tentativas))
        chute_str = input("Digite um número entre 1 e 100: ")
        print("Você digitou: ", chute_str)
        chute = int(chute_str)

        if chute < 1 or chute > 100:
            print("!!!Digite um número entre 1 e 100!!!")
            continue

        acertou = numero_secreto == chute
        maior = chute > numero_secreto
        menor = chute < numero_secreto

        if acertou:
            print("Você acertou e fez {} pontos!".format(pontos))
            break
        else:
            if maior:
                print("Você errou! O seu chute foi maior que o número secreto.")
            elif menor:
                print("Você errou! O seu chute foi menor que o número secreto.")
            pontos_perdidos = abs(numero_secreto - chute)
            pontos = pontos - pontos_perdidos

    print("Fim do jogo")


if __name__ == "__main__":
    jogar()
