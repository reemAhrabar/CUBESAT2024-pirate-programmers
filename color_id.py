import cv2
import numpy as np

def get_mask(image, lower_bound, upper_bound):
    return cv2.inRange(image, lower_bound, upper_bound)

def analyze_image(image):
    color_range = {
        "blue": [(50, 0, 0), (255, 100, 100)],
        "green": [(0, 40, 0), (100, 255, 100)],
        "red": [(0, 0, 40), (100, 100, 255)]
    }
    color_amount = {"blue": 0, "green": 0, "red": 0}
    
    for color, (lower, upper) in color_range.items():
        lower_bound = np.array(lower, dtype="uint8")
        upper_bound = np.array(upper, dtype="uint8")
        mask = get_mask(image, lower_bound, upper_bound)
        color_amount[color] = cv2.countNonZero(mask)
    
    total_pixels = image.shape[0] * image.shape[1]
    perc_blue = color_amount["blue"] / total_pixels
    perc_green = color_amount["green"] / total_pixels
    perc_red = color_amount["red"] / total_pixels
    
    return color_range, perc_blue, perc_green, perc_red

def color_id(image_file):
    image = cv2.imread(image_file)
    if image is None:
        print(f"Error: Unable to load image {image_file}")
        return
    
    color_range, perc_blue, perc_green, perc_red = analyze_image(image)
    print(f"The percentage of red is {round(100 * perc_red, 2)}%")
    print(f"The percentage of green is {round(100 * perc_green, 2)}%")
    print(f"The percentage of blue is {round(100 * perc_blue, 2)}%")
    
    blue_mask = get_mask(image, *color_range['blue'])
    green_mask = get_mask(image, *color_range['green'])
    red_mask = get_mask(image, *color_range['red'])
    
    cv2.imwrite('blue_mask.jpg', blue_mask)
    cv2.imwrite('green_mask.jpg', green_mask)
    cv2.imwrite('red_mask.jpg', red_mask)
    print('Image masks saved')

def compare_images(image_file1, image_file2):
    image1 = cv2.imread(image_file1)
    image2 = cv2.imread(image_file2)
    
    if image1 is None or image2 is None:
        print("Error: Unable to load one or both images.")
        return
    
    _, blue1, green1, _ = analyze_image(image1)
    _, blue2, green2, _ = analyze_image(image2)
    
    print(f"Image 1 - Blue: {round(100 * blue1, 2)}%, Green: {round(100 * green1, 2)}%")
    print(f"Image 2 - Blue: {round(100 * blue2, 2)}%, Green: {round(100 * green2, 2)}%")
    
    blue_ratio_change = (blue2 / (green2 + 1e-6)) / (blue1 / (green1 + 1e-6))
    
    if blue_ratio_change > 1.5:
        print("Tsunami detected: Significant increase in blue relative to green.")
    else:
        print("No tsunami detected.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        color_id(sys.argv[1])
    elif len(sys.argv) == 3:
        compare_images(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python script.py <image> or python color_id.py <image1> <image2>")
