# this is my current code for it:
import os
import numpy as np
import pyvista as pv
import cv2

def stl_to_slices(stl_file, slice_height):
    # Load STL file
    mesh = pv.read(stl_file)

    # Extract vertex coordinates
    vertices = mesh.points
    min_x, min_y, min_z = np.min(vertices, axis=0)
    max_x, max_y, max_z = np.max(vertices, axis=0)

    # Calculate number of slices
    num_slices = int((max_z - min_z) / slice_height)

    # Create directory to save the slice images
    output_dir = 'slice_images'
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over each slice
    for i in range(num_slices):
        # Calculate slice boundaries
        slice_min_z = min_z + i * slice_height
        slice_max_z = min_z + (i + 1) * slice_height

        # Perform slicing to keep only the section between slice_min_z and slice_max_z
        slice_mesh = mesh.clip_box([min_x, max_x, min_y, max_y, min_z, slice_min_z])
        slice_mesh = slice_mesh.clip_box([min_x, max_x, min_y, max_y, slice_max_z, max_z])

        # slice_center = np.array([(min_x + max_x) / 2, (min_y + max_y) / 2, slice_max_z + 0.1])

        camera_position = [0.0, 0.0, slice_max_z]

        # Generate bird's eye view image
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(slice_mesh)
        plotter.camera_position = camera_position
        plotter.show_bounds = False
        plotter.show_grid = False
        plotter.screenshot(os.path.join(output_dir, f'slice_{i}.png'))

    print(f'{num_slices} slice images saved in the "{output_dir}" directory.')


# Example usage
stl_file_path = "/home/pchellia/Desktop/Legoify/legoify/objsrc/toothless.stl"
slice_height = 0.5  # Adjust the slice height as needed

try:
    stl_to_slices(stl_file_path, slice_height)
except FileNotFoundError:
    print(f"File not found: {stl_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
