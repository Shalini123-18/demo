import cv2;

try:
    img = cv2.imread("images/img1.jpg")
    try:
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Gray Image", gray)
            cv2.waitKey(0)
            cv2.imwrite("images/gray_image.jpg", gray)
        except Exception as e:
            print("Error occured while converting to gray scale image: ",e)
    except Exception as e:
        print("Error occured while displaying image: ",e)
    finally:
        cv2.destroyAllWindows()
except Exception as e:
    print("Error occured while reading the image: ",e)
