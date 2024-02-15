import cv2
import numpy as np

# Loading images
im1 = cv2.imread("D:\CVIP\Assignment1\image1.jfif")
im2 = cv2.imread("D:\CVIP\Assignment1\image2.jfif")
im3 = cv2.imread("D:\CVIP\Assignment1\image3.jfif")
im4 = cv2.imread("D:\CVIP\Assignment1\image1.jfif")

# Check if images were successfully loaded or not
if im1 is None or im2 is None or im3 is None or im4 is None:
    print("Error! Unable to read one or more images.")
else:
    # Resize images to have the same height
    target_height = 180
    im1_resized = cv2.resize(im1, (int(im1.shape[1] * target_height / im1.shape[0]), target_height))
    im2_resized = cv2.resize(im2, (int(im2.shape[1] * target_height / im2.shape[0]), target_height))
    im3_resized = cv2.resize(im3, (int(im3.shape[1] * target_height / im3.shape[0]), target_height))
    im4_resized = cv2.resize(im4, (int(im4.shape[1] * target_height / im4.shape[0]), target_height))

    # Create a blank collage image
    collage_width = im1_resized.shape[1] + im2_resized.shape[1] + im3_resized.shape[1] + im4_resized.shape[1]
    collage_image = np.zeros((target_height, collage_width, 3), dtype=np.uint8)

    # Concatenate resized images horizontally
    collage_image[:, :im1_resized.shape[1], :] = im1_resized
    collage_image[:, im1_resized.shape[1]:im1_resized.shape[1] + im2_resized.shape[1], :] = im2_resized
    collage_image[:, im1_resized.shape[1] + im2_resized.shape[1]:im1_resized.shape[1] + im2_resized.shape[1] + im3_resized.shape[1], :] = im3_resized
    collage_image[:, im1_resized.shape[1] + im2_resized.shape[1] + im3_resized.shape[1]:, :] = im4_resized

    # Display the collage image
    cv2.imshow("Collage Image", collage_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
