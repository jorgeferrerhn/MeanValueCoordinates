import cv2 as cv
import numpy as np
import math

img = cv.imread('source_02_edge.png')
z = np.array([0,0,0]) # np.array.all() ritorna false se c'e' almeno un zero
dictLamda = dict()
pxSource = dict()
pasteY = 84
pasteX = 204
pxTarget = dict()       # Dict con new coords relativa al target + intensity +
listEdgesTarget = []    # Lista con le nuove coordinate dell'Edge
diffsEdges = dict()     # Dict con i diff per ogni pxEdge

# Funzione che ritorna l'insieme delle coordinate dei pixel dell'edge
def BuildEdge():
    edges = set()
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
                        edges.add((Y,X))

                    # Se il pixel appartiene al bordo aggiungi automaticamente (abbiamo già controllato che il pixel è colorato)
                    elif ((adiacentY == -1 or adiacentX == -1 ) or (adiacentY == img.shape[0] or adiacentX == img.shape[1])):
                        edges.add((Y,X))
            X+=1
        Y+=1
        
    return edges

listEdges = list(BuildEdge())
listEdges.sort()

# Funzione che ritorna un dizionario contenente per ogni px dell'edge, i suoi px adiacenti
def BuildEdgeAdiacent(listEdges):
    Edges = dict()
    for e in listEdges:
        Y,X = e[0], e[1]
        # Intesitá del px Edge
        Edges[e] = [img[Y][X]]  # Intensitá
        adiacentCoords = [(Y-1,X), (Y,X-1), (Y+1,X), (Y,X+1)]
        # Per i pixel direttamente adiacenti controlla se fanno parte di listEdges
        for adiacent in adiacentCoords:
            if adiacent in listEdges:
                Edges[e].append(adiacent)        # Adiacente che appartiene all'Edge
        if len(Edges[e]) < 3:
            exCoords = [(Y-1, X+1), (Y-1, X-1), (Y+1, X-1), (Y+1, X+1)]

            for exC in exCoords:
                if exC in listEdges and len(Edges[e]) < 3:
                    Edges[e].append(adiacent)   # Adiacente che appartiene all'Edge

    # Edges dict con chiave le coordinate dei px dell'edge e con values le coordinate degli adiacenti del relativo pixel
    return Edges

dictEdges = BuildEdgeAdiacent(listEdges)    # Coordinate pxEdge + intesitá + coords px adiacenti che fanno parte dell'edge

# Funzione che ritorna una lista delle lamda calcolate per px su ogni pixel dell'edge
def BuildMVC(Edges, px):
    # Lista contenente tutti i lamda del targetpxSource
    myLamdas = []
    
    for edge in Edges:
        # Gli angoli vengono usati tutti 2 volte max, quindi possiamo fare un buffer in cui salviamo gli angoli che devono essere ancora utilizzati per la seconda volta
        # TODO: provare ad implementare un "buffer" per gli angoli
        p = edge
        p_1 = Edges[edge][1]
        p1 = Edges[edge][2]

        # Angoli usati nella formula di wi
        # TODO: provare ad usare angoli noti per vederne il risultato
        a_1 = (np.arctan2(p[0] - px[0], px[1] - p[1])) - (np.arctan2(p_1[0] - px[0], p_1[1] - px[1]))
        a1 = (np.arctan2(p1[0] - px[0], p1[1] - px[1])) - (np.arctan2(p[0] - px[0], p[1] - px[1]))

        # TODO: Provare ad usare Numpy per la distanza
        wi = (np.tan(a_1/2) + np.tan(a1/2))/math.dist(p, px)
        myLamdas.append(wi)

        dictLamda[(px,p)] = wi
    # print(p, ":", myLamdas)

    return myLamdas




Y = 0
for row in img:
    X = 0
    for px in row:
        # Se pixel é colorato
        if not (px == z).all():
            # Se pixel non é nella negli edge
            if not (Y,X) in dictEdges:
                # Costruisco l'MVC per ogni pixel dell'area da copiare (interna all'edge)
                pxSource[(Y,X)] = [img[Y][X]]
                pxSource[(Y,X)].append(BuildMVC(dictEdges, (Y,X)))
        X+=1
    Y+=1

copyImage = img.copy()
for e in listEdges:
    copyImage[e[0]][e[1]] = (102, 255, 102)

# Clonare foto sopra al target
target = cv.imread('target_01.png')


# Calcola le nuove coordinate dei pxEdge relative al target e calcola diffs
for pxEdge in listEdges:
    listEdgesTarget.append((pxEdge[0] + pasteY, pxEdge[1] + pasteX))

    diff = target[pxEdge[0] + pasteY][pxEdge[1] + pasteX] - img[pxEdge[0]][pxEdge[1]]

    diffsEdges[(pxEdge[0] + pasteY, pxEdge[1] + pasteX)] = diff

# Genera un dict con le nuove coordinate dei pixel interni
for px in pxSource:
    pxTarget[(px[0] + pasteY, px[1] + pasteX)] = pxSource[px]
for px in listEdgesTarget:
    # Salva intensitá
    pxTarget[(px[0], px[1])] = dictEdges[(px[0]- pasteY, px[1] - pasteX)][0]




def interpolant(X, listEges, dictLamda, diffsEdges, offsetY, offsetX):
    # diffsEdges Target
    # dictLamda Source
    R = 0

    for edge in listEdges:
        myLamda = dictLamda[(X,edge)]
        R += myLamda * diffsEdges[edge[0] + offsetY, edge[1] + offsetX]

    return R


for px in pxTarget:
    if not px in listEdgesTarget:
        r = interpolant((px[0] - pasteY, px[1] - pasteX), listEdges, dictLamda, diffsEdges, pasteY, pasteX)
    else:
        r = diffsEdges[px]
    target[px[0]][px[1]] = pxTarget[px][0] + r

# Modifica la foto Target
#for px in pxSource:
#    target[pasteY + px[0]][pasteX + px[1]] = pxSource[px][0]

cv.imshow("Copy Image", copyImage)
cv.imshow("Image",img)
cv.imshow("Target", target)
cv.waitKey(0)