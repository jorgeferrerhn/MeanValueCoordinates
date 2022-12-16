import cv2 as cv
import numpy as np

img = cv.imread('source_02_edge.png')
edges = set()
z = np.array([0,0,0]) # np.array.all() ritorna false se c'e' almeno un zero


print("Image shape: ",str(img.shape))
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
                    print("Pixel: ",i,j,"| Empty adiacent: ",adiacentCoord[0],adiacentCoord[1])
                    # Salva come edge
                    edges.add((i,j))

                # Se il pixel appartiene al bordo aggiungi automaticamente (abbiamo già controllato che il pixel è colorato)
                elif ((adiacentCoord[0] == -1 or adiacentCoord[1] == -1 ) or (adiacentCoord[0] == img.shape[0] or adiacentCoord[1] == img.shape[1])):
                    edges.add((i,j))
        j+=1
    i+=1


# print(edges)
copyImage = img.copy()
for e in edges:
    copyImage[e[0]][e[1]] = (102, 255, 102)

cv.imshow("Copy Image", copyImage)
cv.imshow("Image",img)
cv.waitKey(0)