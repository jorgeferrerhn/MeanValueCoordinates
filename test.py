import cv2 as cv
import numpy as np

img = cv.imread('source_03_edge.png')
edges = set()
z = np.array([0,0,0]) # np.array.all() ritorna false se c'e' almeno un zero


print("Image shape: ",str(img.shape))
# Ciclo sulle righe, cerca primo pixel colorato e lo salva come edge.
# Quando finisce "zona colorata" trovando primo pixel (0,0,0), salva il pixel precendete come edge.
i = 0
for row in img:
    j = 0
    for px in row:
        # Se pixel e' colorato salvare come edge => inizia "zona colorata"
        if not (px == z).all():
            # print("Pixel: ",i,j)
            coords = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]

            for coord in coords:
                valid = (coord[0] in range(1,img.shape[0])) and (coord[1] in range(1,img.shape[1]))
                
                if valid:
                    if (img[coord[0]][coord[1]] == z).all(): #vicino è non-colorato --> boundary
                        print(coord[0],coord[1], px)
                        # Salva come edge
                        edges.add((i,j))
                elif ((coord[0] == 0 or coord[1] == 0 ) or (coord[0] == img.shape[0] or coord[1] == img.shape[1])):
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