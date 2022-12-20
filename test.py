import cv2 as cv
import numpy as np
import math

img = cv.imread('source_02_edge.png')
z = np.array([0,0,0]) # np.array.all() ritorna false se c'e' almeno un zero

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

# Funzione che ritorna un dizionario contenente per ogni px dell'edge, i suoi px adiacenti
def BuildEdgeAdiacent(listEdges):
    Edges = dict()
    for e in listEdges:
        Edges[e] = []
        Y,X = e[0], e[1]
        adiacentCoords = [(Y-1,X), (Y,X-1), (Y+1,X), (Y,X+1)]
        # Per i pixel direttamente adiacenti controlla se fanno parte di listEdges
        for adiacent in adiacentCoords:
            if adiacent in listEdges:
                Edges[e].append(adiacent)
        if len(Edges[e]) < 2:
            exCoords = [(Y-1, X+1), (Y-1, X-1), (Y+1, X-1), (Y+1, X+1)]

            for exC in exCoords:
                if exC in listEdges and len(Edges[e]) < 2:
                    Edges[e].append(adiacent) 

    return Edges

# Funzione che ritorna una lista delle lamda calcolate per px su ogni pixel dell'edge
def BuildMVC(Edges, px):
    # Lista contenente tutti i lamda del targetPx
    myLamdas = []
    
    for edge in Edges:
        # Gli angoli vengono usati tutti 2 volte max, quindi possiamo fare un buffer in cui salviamo gli angoli che devono essere ancora utilizzati per la seconda volta
        # TODO provare ad implementare un "buffer" per gli angoli
        p = edge
        p_1 = Edges[edge][0]
        p1 = Edges[edge][1]

        # Angoli usati nella formula di wi
        a1 = (np.arctan2(px[0] - p1[0], px[1] - p1[1])) - (np.arctan2(px[0] - p[0], px[1] - p[1]))
        a_1 = (np.arctan2(px[0] - p[0], px[1] - p[1])) - (np.arctan2(px[0] - p_1[0], px[1] - p_1[1]))

        # TODO Provare ad usare Numpy per la distanza
        wi = (np.tan(a_1/2) + np.tan(a1/2))/math.dist(p, px)
        myLamdas.append(wi)

    print(p, ":", myLamdas)

    return myLamdas


listEdges = list(BuildEdge())
listEdges.sort()
Px = dict()
dictEdges = BuildEdgeAdiacent(listEdges)

Y = 0
for row in img:
    X = 0
    for px in row:
        # Se pixel é colorato
        if not (px == z).all():
            # Se pixel non é nella negli edge
            if not (Y,X) in dictEdges:
                # Costruisco l'MVC per ogni pixel dell'area da copiare (interna all'edge)
                Px[(Y,X)] = BuildMVC(dictEdges, (Y,X))
        X+=1
    Y+=1

copyImage = img.copy()
for e in listEdges:
    copyImage[e[0]][e[1]] = (102, 255, 102)

cv.imshow("Copy Image", copyImage)
cv.imshow("Image",img)
cv.waitKey(0)