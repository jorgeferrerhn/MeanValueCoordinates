import cv2 as cv
import numpy as np
import math

# dictLamda = dict()
# pxSource = dict()
# pxTarget = dict()       # Dict con new coords relativa al target + intensity +
# listEdgesTarget = []    # Lista con le nuove coordinate dell'Edge
# diffsEdges = []    # Dict con i diff per ogni pxEdge

###########
img = cv.imread('source_pixel.png')
z = np.array([0,0,0]) # np.array.all() ritorna false se c'e' almeno un zero
target = cv.imread('target_pixel.png')
dictEdgesSource = dict()
dictSource = dict()
offsetY = 5
offsetX = 5

# Funzione che ritorna l'insieme delle coordinate dei pixel dell'edge
def BuildEdge():
    dictEdgesSource = dict()
    # Iterazione su ogni pixel
    Y = 0
    for row in img:
        X = 0
        for px in row:
            # Se il pixel è colorato, controlla tutti i suoi adiacenti
            if not (px == z).all():

                # Coordinate dei pixel adiacenti
                coords = [(Y-1,X),(Y+1,X),(Y,X-1),(Y,X+1)]

                # Per ogni adiacente controlla prima se appartiene al bordo del file
                for adiacentCoord in coords:
                    adiacentY = adiacentCoord[0]
                    adiacentX = adiacentCoord[1]
                    notBorder = (adiacentY in range(0,img.shape[0])) and (adiacentX in range(0,img.shape[1]))
                    
                    # Se non appartiene al bordo e il pixel adiacente è [0,0,0] aggiungi agli edges
                    if notBorder and (img[adiacentY][adiacentX] == z).all():
                        # print("Pixel: ",Y,X,"| Empty adiacent: ",adiacentCoord[0],adiacentCoord[1])
                        # Salva come edge
                        dictEdgesSource[(Y,X)] = []

                    # Se il pixel appartiene al bordo aggiungi automaticamente (abbiamo già controllato che il pixel è colorato)
                    elif ((adiacentY == -1 or adiacentX == -1 ) or (adiacentY == img.shape[0] or adiacentX == img.shape[1])):
                        dictEdgesSource[(Y,X)] = []
            X+=1
        Y+=1
        
    return dictEdgesSource

def checkCC(px, pred, l, listEdges):
    # Calcolo da differenza delle coordinate tra il px in cui sono e il pixel adiacente che ho appena aggiunto cosí posso sapere in che modo muovermi CC
    Y,X = px[0], px[1]
    pY, pX = pred[0], pred[1]
    nextPx = (0,0)

    start = (pY - Y, pX - X)

    dictEdgesSource[px] = [tuple(img[Y][X])]

    if pred not in dictEdgesSource[px]:
        dictEdgesSource[px].append(pred)

    match start:
        case (-1, 0):
            for adiacent in [(Y-1, X-1), (Y, X-1), (Y+1,X-1), (Y+1, X), (Y+1,X+1), (Y, X+1), (Y-1, X+1)]:
                if adiacent in listEdges:
                    dictEdgesSource[px].append(adiacent)
                    nextPx = adiacent
                    break
        case (-1, -1):
            for adiacent in [(Y, X-1), (Y+1,X-1),(Y+1, X), (Y+1,X+1), (Y, X+1), (Y-1, X+1), (Y-1, X)]:
                if adiacent in listEdges:
                    dictEdgesSource[px].append(adiacent)
                    nextPx = adiacent
                    break
        case (0, -1):
            for adiacent in [(Y+1,X-1),(Y+1, X), (Y+1,X+1), (Y, X+1), (Y-1, X+1), (Y-1, X), (Y-1,X-1)]:
                if adiacent in listEdges:
                    dictEdgesSource[px].append(adiacent)
                    nextPx = adiacent
                    break
        case (1, -1):
            for adiacent in [(Y+1, X), (Y+1,X+1), (Y, X+1), (Y-1, X+1), (Y-1, X), (Y-1,X-1), (Y,X-1)]:
                if adiacent in listEdges:
                    dictEdgesSource[px].append(adiacent)
                    nextPx = adiacent
                    break
        case (1, 0):
            for adiacent in [(Y+1,X+1), (Y, X+1), (Y-1, X+1), (Y-1, X), (Y-1,X-1), (Y,X-1), (Y+1, X-1)]:
                if adiacent in listEdges:
                    dictEdgesSource[px].append(adiacent)
                    nextPx = adiacent
                    break
        case (1, 1):
            for adiacent in [(Y, X+1), (Y-1, X+1), (Y-1, X), (Y-1,X-1), (Y,X-1), (Y+1, X-1), (Y+1,X)]:
                if adiacent in listEdges:
                    dictEdgesSource[px].append(adiacent)
                    nextPx = adiacent
                    break
        case (0, 1):
            for adiacent in [(Y-1, X+1), (Y-1, X), (Y-1,X-1), (Y,X-1), (Y+1, X-1), (Y+1,X), (Y+1,X+1)]:
                if adiacent in listEdges:
                    dictEdgesSource[px].append(adiacent)
                    nextPx = adiacent
                    break
        case (-1, 1):
            for adiacent in [(Y-1, X), (Y-1,X-1), (Y,X-1), (Y+1, X-1), (Y+1,X), (Y+1,X+1), (Y, X+1)]:
                if adiacent in listEdges:
                    dictEdgesSource[px].append(adiacent)
                    nextPx = adiacent
                    break
    
    # print("PX:", px, "pred:", pred, "Start:", start, "Next:", nextPx, "\n")
    l-=1
    pred = px
    if l > 0:
        checkCC(nextPx, pred, l, listEdges)
    else:
        return
    

# Funzione che ritorna un dizionario contenente per ogni px dell'edge, i suoi px adiacenti
listEdges = list(dictEdgesSource.keys())

def BuildEdgeAdiacent(dictEdges, listEdges):
    Y,X = listEdges[0][0], listEdges[0][1]
    l = len(listEdges)

    # Primo elemento
    adiacentCoords = [(Y-1,X), (Y-1,X+1), (Y, X+1), (Y+1, X+1), (Y+1,X), (Y+1,X-1), (Y, X-1), (Y-1, X-1)]
    for A in adiacentCoords:
        if A in listEdges:
            dictEdges[(Y,X)].append(A)
            pred = A
            break
    checkCC((Y,X), pred, l, listEdges)
    return dictEdges

'''
        # Intesitá del px Edge
        dictEdges[edge] = [img[Y][X]]  # Intensitá
        # adiacentCoords = [(Y-1,X), (Y,X-1), (Y+1,X), (Y,X+1)]
        adiacentCoords = [(Y-1, X), (Y-1, X-1), (Y, X-1), (Y+1,X-1),(Y+1, X), (Y+1,X+1), (Y, X+1), (Y-1, X+1)]
        
        bufferAdiacent = []
        for adiacent in adiacentCoords:
            if adiacent in dictEdges:      
                # dictEdges[edge].append(adiacent)    # Adiacente che appartiene all'Edge
                bufferAdiacent.append(adiacent)

        # Facciamo una selezione dei corretti adiacenti
        for A in bufferAdiacent:
            if A in [(Y-1,X),(Y,X-1),(Y+1,X),(Y, X+1)]:
                dictEdges[edge].append(A)
        
        # Casi
        l = len(dictEdgesp[edge])
        match l:
            # Non ci sta nulla sugli assi
            case 0:
                s
        '''

'''
        if len(dictEdges[edge]) < 3 and len(dictEdges[edge]):
            (startY, startX) = (dictEdges[edge][1][0], dictEdges[edge][1][1])
            i = bufferAdiacent.index((startY,startX))
            dictEdges[edge].append(bufferAdiacent[i+1])
        '''

        # print("\nQUI BUFFER ADIACENT: ",str(bufferAdiacent))
'''        
        if len(bufferAdiacent) == 2:
            dictEdges[edge].append(bufferAdiacent[0])
            dictEdges[edge].append(bufferAdiacent[1])

        if len(bufferAdiacent) > 2:
            contRow,contCol = 0,0
            
            for A in bufferAdiacent:

                if X == A[1]: 
                    contRow += 1

                if Y == A[0]:
                    contCol += 1

            if contRow == 2: #stessa riga
                print("DICT EDGE: ",str(dictEdges[edge]))
                print("DICT EDGE TYPE: ",type(dictEdges[edge]))

                dictEdges[edge].append((Y,X-1))
                dictEdges[edge].append((Y,X+1))

            if contCol == 2: #stessa colonna
                print("DICT EDGE: ",str(dictEdges[edge]))

                dictEdges[edge].append((Y-1,X))
                dictEdges[edge].append((Y+1,X))

        '''
        # print(edge, ":", dictEdges[edge][1:])
        

    # Edges dict con chiave le coordinate dei px dell'edge e con values le coordinate degli adiacenti del relativo pixel
    

# dictEdges = BuildEdgeAdiacent(listEdges)    # Coordinate pxEdge + intesitá + coords px adiacenti che fanno parte dell'edge

# Funzione che ritorna una lista delle lamda calcolate per px su ogni pixel dell'edge
def BuildLamda(dictEdges, px):
    # Lista contenente tutti i lamda del targetpxSource
    myLamdas = []
    
    for edge in dictEdges:
        # Gli angoli vengono usati tutti 2 volte max, quindi possiamo fare un buffer in cui salviamo gli angoli che devono essere ancora utilizzati per la seconda volta
        # TODO: provare ad implementare un "buffer" per gli angoli
        # print("\nQUI: ",str(dictEdges[edge][1]))
        p = edge
        p_1 = dictEdges[edge][1]
        p1 = dictEdges[edge][2]

        # Angoli usati nella formula di wi
        # TODO: provare ad usare angoli noti per vederne il risultato
        a_1 = (math.atan2(p[0] - px[0], p[1] - px[1])) - (math.atan2(p_1[0] - px[0], p_1[1] - px[1]))
        a1 = (math.atan2(p1[0] - px[0], p1[1] - px[1])) - (math.atan2(p[0] - px[0], p[1] - px[1]))

        # if a1 < 0:
        #     # Togliere a un angolo di 360 a1
        #     a1 = (2*math.pi) + a1
        # if a_1 < 0:
        #     # Togliere a un angolo di 360 a1
        #     a_1 = (2*math.pi) + a_1

        # TODO: Provare ad usare Numpy per la distanza
        wi = (math.tan(a_1/2) + math.tan(a1/2))/math.dist(p, px)
        # print(a1,a_1)
        # print(wi,":",math.tan(a_1/2), math.tan(a1/2))
        # print("\t",a_1, a1, "\n")
        myLamdas.append(wi)

        # dictLamda[(px,p)] = wi
    return myLamdas


def BuildMVC(dictEdgesSource):
    dictSource = dict()
    Y = 0

    for row in img:
        X = 0
        for px in row:
            # Se pixel é colorato
            if not (px == z).all():
                # Se pixel non é nella negli edge
                if not (Y,X) in dictEdgesSource:
                    # Costruisco l'MVC per ogni pixel dell'area da copiare (interna all'edge)
                    dictSource[(Y,X)] = [img[Y][X]]
                    # (Y,X): [intensitá, [mylamdas]]
                    dictSource[(Y,X)].append(BuildLamda(dictEdgesSource, (Y,X)))
            X+=1
        Y+=1

    return dictSource

# Crea il dict con tutti i px edge
dictEdgesSource = BuildEdge()
listKeys = list(dictEdgesSource.keys())
# Aggiunge al dict gli adiacenti per ogni px edge
dictEdgesSource = BuildEdgeAdiacent(dictEdgesSource, listKeys)

# for el in dictEdgesSource:
#     print(el,":", dictEdgesSource[el])
# Costruisce dict con pixel del source con intensitá e mylamdas
dictSource = BuildMVC(dictEdgesSource)


# Clonare foto sopra al target
# Calcola le nuove coordinate dei pxEdge relative al target e calcola diffs
for edge in dictEdgesSource:
    targetY = edge[0] + offsetY
    targetX = edge[1] + offsetX
    targetRGB = target[targetY][targetX]

    # diff = tuple(target[targetY][targetX]) - dictEdgesSource[edge][0]
    RSource, GSource, BSource = int(dictEdgesSource[edge][0][0]), int(dictEdgesSource[edge][0][1]), int(dictEdgesSource[edge][0][2])
    RTarget, GTarget, BTarget = int(targetRGB[0]), int(targetRGB[1]), int(targetRGB[2])

    diff = [RTarget - RSource, BTarget - BSource, GTarget - GSource]

    dictEdgesSource[edge].insert(1, diff) # secondo valore in dictEdgesSource é diff

# Genera un dict con le nuove coordinate dei pixel interni
# for px in pxSource:
    #pxTarget[(px[0] + pasteY, px[1] + pasteX)] = pxSource[px]
#for px in listEdgesTarget:
    # Salva intensitá
    #pxTarget[(px[0], px[1])] = dictEdges[(px[0]- pasteY, px[1] - pasteX)][0]

def Interpolant(px, dictEdgesSource, dictSource, listKeys):
    # R = 0
    R = [0,0,0]
    for edge in dictEdgesSource:
        # Indice della chiave dell'edge
        # La lista lamda, nel pxSource, confronti lo stesso indice
        i = listKeys.index(edge)
        lamdaEdge = dictSource[px][1][i]
        edgeDiff = dictEdgesSource[edge][1]

        # R += lamdaEdge * edgeDiff
        R[0] += lamdaEdge * edgeDiff[0]
        R[1] += lamdaEdge * edgeDiff[1]
        R[2] += lamdaEdge * edgeDiff[2]
        
    return R

for px in dictSource:
    if not px in dictEdgesSource:
        R = Interpolant(px, dictEdgesSource, dictSource, listKeys)
    else:
        # TODO: Per edges basta sommare tutti i diff degli edge
        # R = 0
        R = [0,0,0]
        for edge in dictEdgesSource:
            # R += dictEdgesSource[edge][1]
            R[0] += dictEdgesSource[edge][1][0]
            R[1] += dictEdgesSource[edge][1][1]
            R[2] += dictEdgesSource[edge][1][2]

    newInt = [(dictSource[px][0][0] + R[0])%255, (dictSource[px][0][1] + R[1])%255, (dictSource[px][0][2] + R[2])%255]
    target[px[0] + offsetY][px[1] + offsetX] = newInt

# Modifica la foto Target
#for px in pxSource:
#    target[pasteY + px[0]][pasteX + px[1]] = pxSource[px][0]

cv.imshow("Image",img)
cv.imshow("Target", target)
cv.waitKey(0)
