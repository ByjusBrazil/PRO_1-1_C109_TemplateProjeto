# Numpy é para a conversão numpy-Array
import numpy as np

# Bibliotecas relacionadas com o screenshot da tela
import pyautogui
import imutils

# Bibliotecas relacionadas com a detecção de mão
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# Pontos dos dedos (não o polegar) baseados no sistema de captura da mão feito pelo mp
finger_tips =[8, 12, 16, 20]
# Ponta do dedo (que é o polegar) baseada no sistema de captura da mão feito pelo mp

thumb_tip= 4

# Neste loop, algumas ações são repetidas até o código parar:
# | 1. Detecta as pontas e pontos de referência dos dedos/polegares
# | 2. Usa a distância entre eles para verificar se a mão está fechada
# | 3. Se a mão estiver realmente fechada(de acordo com o mp), a captura de tela será automaticamente ativada pelo código
while True:
    ret,img = cap.read()
    img = cv2.flip(img, 1)
    h,w,c = img.shape
    # Este é o quadro capturado e com as dicas e os landmarks desenhados pelo mp
    results = hands.process(img)

    # Se o mp detectar a mão na câmera, ele vai para um loop for
    if results.multi_hand_landmarks:
        # Acesse todas as posições de referência entre pontos para verificar se elas
        # |estão na posição certa que faz a mão fechar
        for hand_landmark in results.multi_hand_landmarks:
            # Acessando as posições (com base no hand_landmark atual no loop, dentro
            # | resultados.multi_hand_landmarks)

            # Uma lista vazia e um loop para salvar os valores dos landmarks
            lm_list=[]
            for id ,lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)

            # Um array vazio para salvar se os pontos de referência indicarem que a mão está fechada({True}) ou não ({False})  
            finger_fold_status = []
            for tip in finger_tips:
                # Capturando o valor de distância entre os pontos do dedo percorrido na array
                x,y = int(lm_list[tip].x*w), int(lm_list[tip].y*h)
                # Desenhando um círculo para ser visível na pop-up
                cv2.circle(img, (x,y), 15, (255, 0, 0), cv2.FILLED)


                # Verifique se o dedo está dobrado verificando se o valor inicial da ponta do dedo é menor que
                # | a posição inicial do dedo que é o marco interno do dedo indicador
                # A cor do desenho muda para verde se a condição for aprovada, e o array anterior
                # | para verificar se cada ponto de referência está fechado é anexado com o valor {True}
                if lm_list[tip].x < lm_list[tip - 3].x:
                    cv2.circle(img, (x,y), 15, (0, 255, 0), cv2.FILLED)
                    finger_fold_status.append(True)
                # Se a distância entre as pontas do dedo indica que ele não está dobrado, a matriz será
                # | anexada com o valor {False}, o que indica que a mão não deve estar fechada neste momento
 
                else:
                    finger_fold_status.append(False)

            # É possível visualizar os valores de cada landmark se está dobrado ou não no terminal
            print(finger_fold_status)

            # Neste if, é verificado se todos os pontos de referência possuem o valor {True}, o que
            # | indic que a mão está fechada
            if all(finger_fold_status):
                # Local onde o manual de instruções da byju's pede para escrever o código..
                pass # O pass corrige o bug de identação
    
    # Isso desenha as landmarks na tela
    mp_draw.draw_landmarks(
        img,
        hand_landmark,
        mp_hands.HAND_CONNECTIONS,
        mp_draw.DrawingSpec((0, 0, 255), 2, 2),
        mp_draw.DrawingSpec((0, 255, 0), 4, 2)
    )

    
    # Mostrando os Frames
    cv2.imshow("Rastreamento de Maos", img)
    cv2.waitKey(1)

# ATENÇÃO
# Esse código é uma branch editada do template original, que corrige o bug de identação da linha 55 (no código original), basta colocar um pass no if vazio. Além disso, tem alguns comentários e o código é mais organizado em algumas partes, tudo sem alterar o código original. SIGA O MANUAL DE INSTRUÇÕES DA BYJU'S PARA COMPLETAR O PROJETO.
# Branch feito por @RgbCatOficial (ou Daniel Costa Nobre), do curso de informática da byju's.
# Se você se sente bem com isso, delete esses comentários do final e complete seu projeto.