import cv2
import numpy as np
import os

folder_path = "/home/pchellia/Desktop/Legoify/slice_images"
output_folder = "/home/pchellia/Desktop/Legoify/bnw_slices"

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an image
    if filename.endswith(".png") or filename.endswith(".jpg"):
        # Read the image
        file_path = os.path.join(folder_path, filename)
        original_img = cv2.imread(file_path)

        # Convert to grayscale
        gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

        # Resize the image to have an even number of rows and columns
        height, width = gray_img.shape
        gray_img = gray_img[:height - height % 5, :width - width % 5]

        # Reshape the image by dividing each 5x5 square into a single pixel
        condensed_img = gray_img.reshape((gray_img.shape[0] // 5, 5, gray_img.shape[1] // 5, 5)).mean(axis=(1, 3)).astype(np.uint8)

        # Convert to black and white
        _, bnw_img = cv2.threshold(condensed_img, 127, 255, cv2.THRESH_BINARY)

        # Create boolean array
        boolean_array = np.array(bnw_img == 255, dtype=bool)

        # Save the boolean array as a text file
        output_path = os.path.join(output_folder, "boolean_" + filename.replace(".png", ".txt"))
        np.savetxt(output_path, boolean_array, fmt="%d", delimiter="")

        print(f"Processed: {filename}")

print("All files processed.")
