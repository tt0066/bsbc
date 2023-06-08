import lib
import cv2
import numpy as np
import pywt

fontpath = "E:\\App\\back\\runcode\\xiaoxin.ttf"
Hash = "0x3925685356b952817bde2013b8dabf67"
Addr = "0xd8585A6a60D6d293305E1947c231973d19258afc"
key, a, b = 3, 1, 1
a1, a2, a3, a4 = 0.08, 0.08, 0.08, 0.08

# lib.buyer_get_water(fontpath, Addr, Hash, key, a, b, "E:\\App\\back\\runcode")
# lib.buyer_gene_save_key("E:\\App\\back\\runcode")
# lib.buyer_get_J("E:\\App\\back\\runcode\\water.png","E:\\App\\back\\runcode","file1")
# lib.buyer_get_J("E:\\App\\back\\runcode\\watermark.png","E:\\App\\back\\runcode","file2")
# img=cv2.resize(cv2.imread("E:\\App\\back\\runcode\\Lena.jpg",0),(400,400))
# cv2.imwrite("E:\\App\\back\\runcode\\Gray.jpg",img)

# img = cv2.resize(cv2.imread("E:\\App\\back\\runcode\\gray.png", 0), (400, 400))
# water = cv2.resize(cv2.imread(
#     "E:\\App\\back\\runcode\\watermark.png", 0), (101, 101))
# # print(type(img), img.shape)
# # print(type(water), water.shape)
# c = pywt.wavedec2(water, "db2", level=1)
# [cal, (ch1, cv1, cd1)] = c
# d = pywt.wavedec2(img, "db2", level=3)
# [cl, (cH3, cV3, cD3), (cH2, cV2, cD2), (cH1, cV1, cD1)] = d
# # print(cal.shape, cl.shape)

# cl1 = cl+cal*a1
# cH31 = cH3+ch1*a2
# cV31 = cV3+cv1*a3
# cD31 = cD3+cd1*a4
# Arr = pywt.waverec2(
#     [cl1, (cH31, cV31, cD31), (cH2, cV2, cD2), (cH1, cV1, cD1)], "db2")
# newimg = np.array(Arr, np.uint8)
# print(newimg.shape)
# cv2.imshow("1", newimg)
# cv2.waitKey()
# cv2.imwrite("E:\\App\\back\\runcode\\watered.png", newimg)

# new = pywt.wavedec2(newimg, "db2", level=3)
# [c3, (v3, h3, d3), (v2, h2, d2), (v1, h1, d1)] = new
# cal1 = (c3-cl)/a1
# ch11 = (v3-cH3)/a2
# cv11 = (h3-cV3)/a3
# cd11 = (d3-cD3)/a4
# Arr1 = pywt.waverec2([cal1, (ch11, cv11, cd11)], "db2")
# Arrimg = np.array(Arr1, np.uint8)
# print(Arrimg.shape)
# # cv2.imshow("2", Arrimg)
# # cv2.waitKey()
# # cv2.imshow("3", lib.inverse_arnold(Arrimg, key, a, b))
# # cv2.waitKey()
# cv2.imwrite("E:\\App\\back\\runcode\\recover1.png", Arrimg)
# cv2.imwrite("E:\\App\\back\\runcode\\recover2.png",
#             lib.inverse_arnold(Arrimg, key, a, b))


img = cv2.imread("E:\\App1\\OfflineCode\\gray.png", 0)
d = pywt.wavedec2(img, "db2", level=3)
[c3, (cH3, cV3, cD3), (cH2, cV2, cD2), (cH1, cV1, cD1)] = d
arr = []
for i in range(4):
    for j in range(4):
        arr.append(c3[i, j])
        c3[i, j] -= c3[i, j]
np.save("E:\\App1\\OfflineCode\\npy\\c3.npy", c3)
np.save("E:\\App1\\OfflineCode\\npy\\cH3.npy", cH3)
np.save("E:\\App1\\OfflineCode\\npy\\cV3.npy", cV3)
np.save("E:\\App1\\OfflineCode\\npy\\cD3.npy", cD3)
np.save("E:\\App1\\OfflineCode\\npy\\cH2.npy", cH2)
np.save("E:\\App1\\OfflineCode\\npy\\cV2.npy", cV2)
np.save("E:\\App1\\OfflineCode\\npy\\cD2.npy", cD2)
np.save("E:\\App1\\OfflineCode\\npy\\cH1.npy", cH1)
np.save("E:\\App1\\OfflineCode\\npy\\cV1.npy", cV1)
np.save("E:\\App1\\OfflineCode\\npy\\cD1.npy", cD1)
with open("E:\\App1\\OfflineCode\\npy\\arr.txt", "w+") as f:
    f.write(str(arr))
