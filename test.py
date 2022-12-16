import cv2 as cv
import numpy as np

img = cv.imread('source_02_edge.png')
z = np.array([0,0,0]) # np.array.all() ritorna false se c'e' almeno un zero

# Funzione che ritorna l'insieme delle coordinate dei pixel dell'edge
def BuildEdge():
    edges = set()
    # Iterazione su ogni pixel
    i = 0
    for row in img:
        j = 0
        for px in row:
            # Se il pixel è colorato, controlla tutti i suoi adiacenti
            if not (px == z).all():

                # Coordinate dei pixel adiacenti
                coords = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]

                # Per ogni adiacente controlla prima se appartiene al bordo del file
                for adiacentCoord in coords:
                    notBorder = (adiacentCoord[0] in range(0,img.shape[0])) and (adiacentCoord[1] in range(0,img.shape[1]))
                    
                    # Se non appartiene al bordo e il pixel adiacente è [0,0,0] aggiungi agli edges
                    if notBorder and (img[adiacentCoord[0]][adiacentCoord[1]] == z).all():
                        # print("Pixel: ",i,j,"| Empty adiacent: ",adiacentCoord[0],adiacentCoord[1])
                        # Salva come edge
                        edges.add((i,j))

                    # Se il pixel appartiene al bordo aggiungi automaticamente (abbiamo già controllato che il pixel è colorato)
                    elif ((adiacentCoord[0] == -1 or adiacentCoord[1] == -1 ) or (adiacentCoord[0] == img.shape[0] or adiacentCoord[1] == img.shape[1])):
                        edges.add((i,j))
            j+=1
        i+=1
    # Ritorno le coordinate dei pixel dell'edge
    return edges

def BuildMVC(edges, px):
    # Lista contenente tutti i lamda del targetPx
    myLamdas = []
    
    # Per ogni pixel della foto calcola lamda per ogni pixel del bordo
    '''
    for p in edges:
        p_1 = edges[edges.index(p) - 1]
        p1 = edges[edges.index(p) + 1]

        print("P-1: ", p_1, "P1: ", p1)
        '''

        # lamda_edge(px) = w_i/1 (?) dove w_i = tan()
        # a1
        # a_1 = (np.arctan2(px[0] - p[0], px[1] - p[1])) - (np.arctan2(px[0] - ))
    return

Edges = list(BuildEdge())
# Bisogna vedere come ordinare la lista
Edges.sort()

'''
y = 0
for row in img:
    x = 0
    for px in row:
        # Se pixel é colorato
        if not (px == z).all():
            # Se pixel non é nella lista degli edge
            if not (y,x) in Edges:
                # Costruisco l'MVC per ogni pixel dell'area da copiare (interna all'edge)
                BuildMVC(Edges, (y,x))
        x+=1
    y+=1
'''

copyImage = img.copy()
for e in Edges:
    copyImage[e[0]][e[1]] = (102, 255, 102)

cv.imshow("Copy Image", copyImage)
cv.imshow("Image",img)
cv.waitKey(0)