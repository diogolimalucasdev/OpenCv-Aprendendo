import random
import sys

import cv2

print(cv2.__version__)

(major_ver , minor_ver , subminor_ver) = cv2.__version__.split('.')

tracker_types = ['BOOSTING' , 'MIl' , 'KCF' , 'TLD' , 'MEDIANFLOW' , 'MOSSE' , 'CSRT']  # algoritmos rastreadores
tracker_type = tracker_types[1]  # mil
# print(tracker_type)


# verificar as versoes
if int(minor_ver) < 3:
    tracker = tracker_type
else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting.create()
    if tracker_type == 'MIl':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIAFLOW':
        tracker = cv2.TrackerMediaFlow_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    if tracker_type == 'CSRT':
        tracker = cv2.TrackerCSRT_create()
# print(tracker)
video = cv2.VideoCapture('race.mp4')

# verificando se consegui abrir o video
if not video.isOpened():
    print("nao foi possivel carregar o video")
    sys.exit()
ok , frame = video.read()  # esse comando faz a leitura do video que retorna dois parametros, o primeiro frame e se ele consegui abrir

if not ok:  # se nao retornar um ok
    print('nao foi possivel ler o arquivo de video')
    sys.exit()  # sair da leitura se der alguma coisa errado
print(ok)  # se sair um true é pq conseguiu

# agora selecionamos o que queremos rastrear
bbox = cv2.selectROI(frame , False)  ##baldem box é onde selecionamos o que queremos selecionar

# agora preciso iniciar o algoritmo
ok = tracker.init(frame , bbox)  # passou o primeiro frame e a caixa onde eu selecionei
print(bbox)  # (x, y, largura e altura = tamanho da caixa)

# criar cores aleatorias

colors = (random.randint(0 , 255) , random.randint(0 , 255) , random.randint(0 , 255))  # crio uam cor rgb
print(colors)

# pecorrer todos os frames do video

while True:
    ok , frame = video.read()
    if not ok:  # faço essa verificação para quando ele receber um false do meu ok(quie é quando acaba o video)
        # ai eu saio do loop
        break
    timer = cv2.getTickCount()  # quanto ciclos de clok o processador esat gerando (processador de frames)
    ok, bbox = tracker.update(frame)
    #print(ok, bbox)

    #calcular fps
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    #desenhar o bbox
    if ok:
        (x, y, w, h) = [int(v) for v in bbox] #pecorrendo o bbox e jogador o valor desse em v
        cv2.rectangle(frame, (x, y), (x+ w, y + h), colors, 2, 1)

    else:
        cv2.putText(frame, 'Falaha no rastreamento', (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 255), 2) #se algo der errados eu escrevo no video



    cv2.putText(frame, tracker_type  + 'Tracker', (100, 20),
                cv2.FONT_HERSHEY_SIMPLEX, .75, (50, 170, 50), 2)

    cv2.putText(frame, str(int(fps)), (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, .75, (50, 170, 50), 2)

    cv2.imshow('Rastreando', frame)

    #vai esperar uma tecla do usuario
    if cv2.waitKey(1) & 0xff == 27:
        break
