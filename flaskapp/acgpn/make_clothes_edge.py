import cv2

def generate_clothes_edge(file_path):
    file_name = file_path.split('/')[-1]
    print(file_name)
    img_source = cv2.imread(file_path , 0)

    # ret,img_result1 = cv2.threshold(img_source , 127 , 255 , cv2.THRESH_BINARY)
    ret,img_result2 = cv2.threshold(img_source , 220 , 255 , cv2.THRESH_BINARY_INV)

    # cv2.imshow("SOURCE" , img_source)
    # cv2.imshow("THRESH_BINARY" , img_result1)
    # cv2.imshow("THRESH_BINARY_INV" , img_result2)
    cv2.imwrite(f"./acgpn/Data_preprocessing/test_edge/{file_name}", img_result2);
    cv2.waitKey(0)
    cv2.destroyAllWindows()