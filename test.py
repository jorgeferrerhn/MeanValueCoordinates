import cv2 as cv
import numpy as np
import math


# img = cv.imread('source_pixel.png')
# target = cv.imread('target_02_pixel.png')
img = cv.imread('source_02_edge.png')
target = cv.imread('target_02.png')
z = np.array([0,0,0])       # np.array.all() ritorna false se c'e' almeno un zero
# offsetY = 5                # Offset usato per passare al sistema di riferimento giusto
# offsetX = 5               # Offset usato per passare al sistema di riferimento giusto
offsetY = 84               # Offset usato per passare al sistema di riferimento giusto
offsetX = 204              # Offset usato per passare al sistema di riferimento giusto

# TODO: Vengono creati due dizionari diversi per i px degli edge e del source patch. Teoricamente si potrebbe usare un unico dict e in una lista separata vengono mantenute le coordinate dei px dell'edge

# Funzione che costruisce il dict usando ogni pixel dell'edge come key, e lo inizializza a []
def BuildEdge():
    dictEdgesSource = dict()

    # Iterazione su ogni pixel di img
    Y = 0
    for row in img:
        X = 0
        for px in row:
            # Se il pixel è colorato, controlla tutti i suoi adiacenti (N,E,S,W)
            if not (px == z).all():
                # Coordinate dei pixel adiacenti (N,E,S,W)
                coords = [(Y-1,X),(Y+1,X),(Y,X-1),(Y,X+1)]

                # Per ogni adiacente controlla prima se appartiene al bordo del file
                for adiacentCoord in coords:
                    adiacentY = adiacentCoord[0]
                    adiacentX = adiacentCoord[1]
                    notBorder = (adiacentY in range(0,img.shape[0])) and (adiacentX in range(0,img.shape[1]))
                    
                    # Se non appartiene al bordo e il pixel adiacente è [0,0,0] aggiungi agli edges
                    if notBorder and (img[adiacentY][adiacentX] == z).all():
                        # Salva come edge
                        dictEdgesSource[(Y,X)] = []
                        # Aggiungo l'intensitá del pixel dell'edge
                        dictEdgesSource[(Y,X)] = [tuple(img[Y][X])]

                    # Se il pixel appartiene al bordo aggiungi automaticamente (abbiamo già controllato che il pixel è colorato)
                    elif ((adiacentY == -1 or adiacentX == -1 ) or (adiacentY == img.shape[0] or adiacentX == img.shape[1])):
                        dictEdgesSource[(Y,X)] = []
                        # Aggiungo l'intensitá del pixel dell'edge
                        dictEdgesSource[(Y,X)] = [tuple(img[Y][X])]
            X+=1
        Y+=1
    return dictEdgesSource

# Funzione che ritorna un dizionario contenente per ogni px dell'edge, i suoi px adiacenti
def BuildEdgeAdiacent(dictEdges, listEdges):
    Y,X = listEdges[0][0], listEdges[0][1]
    l = len(listEdges)  # Variabile utilizzata per la chiamata ricorsiva di CheckCC()

    # Appena inizio a cercare gli adiacenti devo considerare il caso particolare di quando sto analizzando il primo px in assoluto
    # In questo caso devo controllare in senso ORARIO dove sta il suo adiacente, per poi considerarlo come predecessore
    adiacentCoords = [(Y-1,X), (Y-1,X+1), (Y, X+1), (Y+1, X+1), (Y+1,X), (Y+1,X-1), (Y, X-1), (Y-1, X-1)]
    for A in adiacentCoords:
        if A in listEdges:
            dictEdges[(Y,X)].append(A)
            pred = A    # Imposto il px trovato come predecessore
            break
    # Inizo le chiamate ricorsive per "camminare" lungo l'edge e trovarmi tutti gli adiacenti
    CheckCC((Y,X), pred, l, listEdges)
    return dictEdges

# Funzione ricorsiva che "percorre" in senso antiorario tutti i pixel dell'edge e aggiunge al loro valore nel dict il loro adiacente
def CheckCC(px, pred, l, listEdges):
    # Calcolo da differenza delle coordinate tra il px in cui sono e il pixel adiacente che ho appena aggiunto in questo modo capisco
    # da dove iniziare a camminare in senso antiorario
    Y,X = px[0], px[1]
    pY, pX = pred[0], pred[1]

    # Coordinate del pixel da cui inizio a camminare relative al px che sto analizzando (px)
    start = (pY - Y, pX - X)
    
    # Controllo se il pixel analizzato in precendenza sia stato inserito nel dict(px) come mio primo adiacente
    if pred not in dictEdgesSource[px]:
        dictEdgesSource[px].append(pred)

    # TODO: Non so se é il miglior modo ma per ora funziona :D
    # A secondo di dove sia il mio pixel di inizo, incomincio a camminare in senso antiorario
    # Mi fermo al primo pixel che fa parte dell'edge e lo aggiungo come adiacente
    # Imposto come successivo px da analizzare il mio adiacente appena trovato
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
    l-=1        # Variabile utilizzata per fermare la ricorsivitá
    pred = px   # Imposto il pixel in cui sono come predecessore per la prossima chiamata ricorsiva
    
    # Controllo se devo fare la chiamata ricorsiva: se ho fatto tutto il giro dei px dell'edge mi posso fermare
    if l > 0:
        # Chiamata ricorsiva
        CheckCC(nextPx, pred, l, listEdges)
    else:
        return

# Funzione che ritorna una lista delle lamda calcolate per px su ogni pixel dell'edge
def BuildLamda(dictEdges, px):
    # Lista contenente tutti i lamda del targetpxSource
    myLamdas = []
    
    for edge in dictEdges:
        # Gli angoli vengono usati tutti 2 volte max, quindi possiamo fare un buffer in cui salviamo gli angoli che devono essere ancora utilizzati per la seconda volta
        # TODO: Provare ad implementare un "buffer" per gli angoli
        p = edge
        p_1 = dictEdges[edge][1]
        p1 = dictEdges[edge][2]

        # Angoli usati nella formula di wi
        # TODO: Non sono sicuro che vengano calcolati correttamente
        #alpha-1
        angoli = []
        prima = math.atan2(p[0] - px[0], p[1] - px[1])
        seconda = math.atan2(p_1[0] - px[0], p_1[1] - px[1])

        angoli.append(prima)
        angoli.append(seconda)

        for alpha in angoli: 
            if alpha < 0:
                prima += 2*math.pi
                seconda += 2*math.pi
                break

    
         #alpha1
        angoli = []
        terza = math.atan2(p1[0] - px[0], p1[1] - px[1])
        quarta = math.atan2(p[0] - px[0], p[1] - px[1])

        angoli.append(terza)
        angoli.append(quarta)

        for alpha in angoli: 
            if alpha < 0:
                terza += 2*math.pi
                quarta += 2*math.pi
                break

        a_1 = prima - seconda
        a1 = terza - quarta
        # a_1 = math.atan2(px[0] - p[0], px[1] - p[1]) - math.atan2(px[0] - p_1[0], px[1] - p_1[1])
        # a1 = math.atan2(px[0] - p1[0], px[1] - p1[1]) - math.atan2(px[0] - p[0], px[1] - p[1])

        # Possibile modo di correggere gli angoli: secondo il paper l'angolo deve sempre essere 0 < a < π (in radianti)
        # if a1 < 0:
        #     # Togliere a un angolo di 360 a1
        #     a1 += 2*math.pi
        # if a_1 < 0:
        #     # Togliere a un angolo di 360 a1
        #     a_1 += 2*math.pi

        # TODO: Provare ad usare Numpy per la distanza
        wi = (abs(math.tan(a_1*0.5)) + abs(math.tan(a1*0.5)))/math.dist(p, px)
        myLamdas.append(wi)
    return myLamdas

# Funzione che costruisce un dict con tutti i px del source patch (ma non dell'edge) con i valori di intensitá e di lamda
def BuildMVC(dictEdgesSource):
    dictSource = dict()

    # Itera su tutti i px del source patch
    Y = 0
    for row in img:
        X = 0
        for px in row:
            # Se pixel é colorato
            if not (px == z).all():
                # Se pixel non é nella negli edge
                if not (Y,X) in dictEdgesSource:
                    # Costruisco l'MVC per ogni pixel dell'area da copiare (interna all'edge)
                    dictSource[(Y,X)] = [tuple(img[Y][X])]
                    # (Y,X): [intensitá, [mylamdas]]
                    dictSource[(Y,X)].append(BuildLamda(dictEdgesSource, (Y,X)))
                    # print((Y,X),":",dictSource[(Y,X)])
            X+=1
        Y+=1
    return dictSource

# Funzione che aggiunge ad ogni px dell'edge la differenza di intensitá con il px "sotto" del target patch
def BuildDiffs(dictEdgesSource):
    for edge in dictEdgesSource:
        Y,X = edge
        targetY = edge[0] + offsetY
        targetX = edge[1] + offsetX
        targetRGB = tuple(target[targetY][targetX])

        # TODO: Controllare che succede quando la differenza causa un numero negativo
        # Converto in int() per problemi di overflow: i px vengono salvati con valori fino a 255, ma quando vado a fare le differenze potrebbero esserci valori negativi (?)
        # BSource, GSource, RSource = int(dictEdgesSource[edge][0][0]), int(dictEdgesSource[edge][0][1]), int(dictEdgesSource[edge][0][2])
        # BTarget, GTarget, RTarget = int(targetRGB[0]), int(targetRGB[1]), int(targetRGB[2])
        BSource, GSource, RSource = img[Y][X][0], img[Y][X][1], img[Y][X][2]
        BTarget, GTarget, RTarget = target[targetY][targetX][0], target[targetY][targetX][1], target[targetY][targetX][2]

        # Calcolo la differenza di intensitá dei px
        # diff = [BTarget - BSource, GTarget - GSource, RTarget - RSource]
        # diff = cv.absdiff(targetRGB, img[edge[0]][edge[1]])
        diff = cv.add(target[targetY][targetX], -img[Y][X])

        # Inserisco il valore di diff ESATTAMENTE nella seconda posizione della lista
        dictEdgesSource[edge].insert(1, diff) # secondo valore in dictEdgesSource é diff
    return

# TODO: Potrebbe essere sbagliato il modo in cui viene calcolato
# Funzione che calcola il valore dell'interpolatore per un px dato
def Interpolant(px, dictEdgesSource, dictSource, listEdges):
    # R = [0,0,0] # Valore dell'interpolatore per tutti e 3 i canali (R,G,B)
    R = np.array([0,0,0], dtype=np.uint8)

    # Interpolatore va calcolato considerando tutti i px dell'edge
    for edge in dictEdgesSource:
        # Dato che le lamda sono state inserite e calcolate considerando l'ordine dei px dell'edge nel loro dict
        # Posso semplicemente trovare il valore della lamda corretto controllando l'indice
        i = listEdges.index(edge)    # Indice della chiave dell'edge
        lamdaEdge = dictSource[px][1][i]
        edgeDiff = dictEdgesSource[edge][1]

        # Calcola il valore dell'interpolatore per i 3 canali
        R[0] += lamdaEdge * edgeDiff[0]
        R[1] += lamdaEdge * edgeDiff[1]
        R[2] += lamdaEdge * edgeDiff[2]
    return R

# Funzione che calcola il valore della nuova intensitá del px
def Clone(dictSource, listEdges, dictEdgesSource):
    # Loop su ogni px del source patch
    for px in dictSource:
        Y = px[0]
        X = px[1]
        # TODO: Questo if non ha senso, sto facendo un loop sui px interni
        # Controlla se il px appartiene all'edge perché i px dell'edge vengono calcolati in modo diverso
        if not px in listEdges:
            # Viene calcola il valore dell'interpolatore
            R = Interpolant(px, dictEdgesSource, dictSource, listEdges)
            # n0, n1, n2 = False, False, False
            # if R[0] < 0:
            #     n0 = True
            # if R[1] <0:
            #     n1 = True
            # if R[2] <0:
            #     n2 = True

            # R = [R[0]%255,R[1]%255,R[1]%255]
            # if n0:
            #     R[0] = R[0] * (-1)
            # if n1:
            #     R[1] = R[1] * (-1)
            # if n2:
            #     R[2] = R[2] * (-1)

            # if px == (2,2):
            #     print(R[0], R[1], R[2])
        # Valore della nuova intensitá
        # newInt = [(dictSource[px][0][0] + R[0])%255, (dictSource[px][0][1] + R[1])%255, (dictSource[px][0][2] + R[2])%255]
        newInt = cv.add(img[Y][X], R)
        # newInt = [cv.add(dictSource[px][0][0], R[0]). cv.add(dictSource[px][0][1], R[1]), cv.add(dictSource[px][0][2] , R[2])]
        # Sostituisce l'intensitá del px target con il nuovo valore calcolato
        # target[px[0] + offsetY][px[1] + offsetX] = newInt
        target.itemset((px[0] + offsetY, px[1] + offsetX, 0), newInt[0])
        target.itemset((px[0] + offsetY, px[1] + offsetX, 1), newInt[1])
        target.itemset((px[0] + offsetY, px[1] + offsetX, 2), newInt[2])
    
    # Loop per modificare gli edge
    for edge in listEdges:
        edgeDiff = dictEdgesSource[edge][1]
        newInt = [dictEdgesSource[edge][0][0] + edgeDiff[0], dictEdgesSource[edge][0][1] + edgeDiff[1], dictEdgesSource[edge][0][2] + edgeDiff[2]]
        target.itemset((edge[0] + offsetY, edge[1] + offsetX, 0), newInt[0])
        target.itemset((edge[0] + offsetY, edge[1] + offsetX, 1), newInt[1])
        target.itemset((edge[0] + offsetY, edge[1] + offsetX, 2), newInt[2])

# Crea il dict con tutti i px edge
dictEdgesSource = BuildEdge()

# Lista (ordinata come il dict) delle coordinate dei px dell'edge
listEdges = list(dictEdgesSource.keys())

# Aggiunge al dict gli adiacenti per ogni px edge
dictEdgesSource = BuildEdgeAdiacent(dictEdgesSource, listEdges)

# Costruisce dict con pixel del source con intensitá e mylamdas
dictSource = BuildMVC(dictEdgesSource)
# Calcola le diff sull'edge
BuildDiffs(dictEdgesSource)

# Clona il source patch sul target
Clone(dictSource, listEdges, dictEdgesSource)
# print(dictSource[(2,2)])

# for e in listEdges:
#     img[e[0]][e[1]] = (123,123,-64)

cv.imshow("Image",img)
cv.resizeWindow("Image", 150,150)
cv.imshow("Target", target)
cv.waitKey(0)
