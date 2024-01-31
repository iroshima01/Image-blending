import os
import cv2
import numpy as np

def pyrUp(image, gauss_kernel):

    upsampled = np.zeros((2 * image.shape[0], 2 * image.shape[1], image.shape[2]), dtype=np.uint8)
    upsampled[::2, ::2, :] = image
    upsampled = cv2.filter2D(upsampled, -1, gauss_kernel * 4)

    return upsampled


def pyrDown(image, gauss_kernel):
    image = cv2.filter2D(image, -1, gauss_kernel)
    downsampled = image[::2, ::2, :]

    return downsampled


def laplacian_pyramid(image, levels, gauss_kernel):
    pyramid = []
    current_level = image

    for i in range(levels - 1):
        downsampled = pyrDown(current_level, gauss_kernel).astype(np.float32)
        upsampled = pyrUp(downsampled, gauss_kernel).astype(np.float32)
        upsampled = upsampled[:current_level.shape[0], :current_level.shape[1]]
        current_level = current_level.astype(np.float32)
        upsampled = upsampled.astype(np.float32)
        laplacian = cv2.subtract(current_level, upsampled)
        pyramid.append(laplacian)
        current_level = downsampled

    pyramid.append(current_level.astype(np.uint8))

    return pyramid


def upsample(image):
    new_width, new_height = image.shape[1] * 2, image.shape[0] * 2
    return cv2.resize(image, (new_width, new_height))


def build_gaussian_pyramid(mask, levels, gauss_kernel):
    pyramid = [mask]
    for i in range(levels - 1):
        mask = pyrDown(mask, gauss_kernel)
        pyramid.append(mask)
    return pyramid


def blend_pyramids(laplacian1, laplacian2, mask_pyramid):
    blended_pyramid = []

    num_levels = min(len(laplacian1), len(laplacian2), len(mask_pyramid))

    for i in range(num_levels):
        mask = mask_pyramid[i]

        laplacian1_resized = cv2.resize(laplacian1[i], (mask.shape[1], mask.shape[0]), interpolation=cv2.INTER_NEAREST)
        laplacian2_resized = cv2.resize(laplacian2[i], (mask.shape[1], mask.shape[0]), interpolation=cv2.INTER_NEAREST)

        blended = (laplacian1_resized * mask) + (laplacian2_resized * (1 - mask))

        blended_pyramid.append(blended)

    return blended_pyramid


def collapse_pyramid(pyramid, gauss_kernel):
    result = pyramid[-1]

    for i in range(len(pyramid) - 2, -1, -1):
        result_up = pyrUp(result, gauss_kernel).astype(np.float32)
        result_up = result_up[:pyramid[i].shape[0], :pyramid[i].shape[1], :]
        result = (result_up + pyramid[i]).clip(0, 255).astype(np.uint8)

    return result


def calling(image1, image2, pyramid_level, mask, gauss_kernel, colorful_mask):



    laplacian1 = laplacian_pyramid(image1, pyramid_level, gauss_kernel)
    laplacian2 = laplacian_pyramid(image2, pyramid_level, gauss_kernel)
    mask_pyramid = build_gaussian_pyramid(mask, pyramid_level, gauss_kernel)
    colorful_mask_pyramid = build_gaussian_pyramid(colorful_mask, pyramid_level, gauss_kernel)
    blended_pyramid = blend_pyramids(laplacian1, laplacian2, mask_pyramid)
    result = collapse_pyramid(blended_pyramid, gauss_kernel)

    #to see the level outputs of laplacian pyramid of image 1
    for level, laplacian_img in enumerate(laplacian1):
        laplacian_img_float32 = np.clip(laplacian_img, 0, 255).astype(np.uint8)
        (cv2.imshow(f'Laplacian 1 - Level {level}', laplacian_img_float32))
        (cv2.imwrite(f'Laplacian_1_Level_{level}.jpg', laplacian_img_float32))

        print(f"Laplacian 1 - Level {level} - Shape: {laplacian_img.shape}")



    #to see the level outputs of laplacian pyramid of image 2
    for level, laplacian_img in enumerate(laplacian2):
        laplacian_img_float32 = np.clip(laplacian_img, 0, 255).astype(np.uint8)
        (cv2.imshow(f'Laplacian 2 - Level {level}', laplacian_img_float32))
        (cv2.imwrite(f'Laplacian_2_Level_{level}.jpg', laplacian_img_float32))

        print(f"Laplacian 2 - Level {level} - Shape: {laplacian_img.shape}")

    #to see the level outputs of gaussian pyramid of mask
    for level, laplacian_img in enumerate(colorful_mask_pyramid):
        laplacian_img_float32 = np.clip(laplacian_img, 0, 255).astype(np.uint8)
        cv2.imshow(f'Gaussian - Level {level}', laplacian_img_float32)
        (cv2.imwrite(f'gaussian_1_Level_{level}.jpg', laplacian_img_float32))
        print(f"Gaussian - Level {level} - Shape: {laplacian_img.shape}")

    #to see the level outputs of blended pyramid
    for level, blended_img in enumerate(blended_pyramid):
        blended_img_float32 = np.clip(blended_img, 0, 255).astype(np.uint8)
        (cv2.imshow(f'Laplacian 1 - Level {level}', blended_img_float32))
        (cv2.imwrite(f'Laplacian_1_Level_{level}.jpg', blended_img_float32))

        print(f"Laplacian 1 - Level {level} - Shape: {blended_img.shape}")


    cv2.imshow('Blended Result', result)
    cv2.imwrite("blended output.jpg", result)

    '''combined_laplacian1 = collapse_pyramid(laplacian1, gausskernel)
    cv2.imshow('Combined Laplacian 1', combined_laplacian1)'''

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    global gausskernel
    image1 = cv2.imread("source image here")
    image2 = cv2.imread("target image path here")


    cv2.namedWindow("Select ROI", cv2.WINDOW_NORMAL)

    roi = cv2.selectROI("Select ROI", image1)
    cv2.destroyWindow("Select ROI")
    mask = np.zeros_like(image1)
    mask[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]] = 1

    colorful_mask = np.zeros_like(image1)
    colorful_mask[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]] = image1[roi[1]:roi[1] + roi[3],
                                                                    roi[0]:roi[0] + roi[2]]


    gauss_kernel = np.array([[0.00390625, 0.015625, 0.0234375, 0.015625, 0.00390625],
                             [0.015625, 0.0625, 0.09375, 0.0625, 0.015625],
                             [0.0234375, 0.09375, 0.140625, 0.09375, 0.0234375],
                             [0.015625, 0.0625, 0.09375, 0.0625, 0.015625],
                             [0.00390625, 0.015625, 0.0234375, 0.015625, 0.00390625]])

    print(gauss_kernel)

    calling(image1, image2, 13, mask, gauss_kernel, colorful_mask)

    cv2.imshow('Selected Mask', colorful_mask)
    cv2.imwrite("selected mask.jpg", colorful_mask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
