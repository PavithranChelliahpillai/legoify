from PIL import Image, ImageDraw
import os

def load_bricks_array(filename):
    bricks = []
    with open(filename, "r") as file:
        for line in file:
            row = list(map(int, line.strip().split()))
            bricks.append(row)
    return bricks

def draw_bricks(bricks, output_filepath):
    dx = [0, 0, -1, 1]
    dy = [-1, 1, 0, 0]
    image = Image.new("RGBA", (3000, 3000), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Create a 2D array with the same size as the bricks array
    vis = [[False] * len(bricks[0]) for _ in range(len(bricks))]

    for i in range(len(bricks)):
        for j in range(len(bricks[i])):
            val = bricks[i][j]
            if val == 0 or vis[i][j] == 1:
                continue

            tgt = val
            minx = i
            miny = j
            maxx = 0
            maxy = 0
            stack = []
            stack.append((i, j))
            vis[i][j] = 1
            while(len(stack) != 0):
                curr = stack.pop()
                maxx = max(maxx, curr[0])
                maxy = max(maxy, curr[1])
                minx = min(minx, curr[0])
                miny = min(miny, curr[1])

                for k in range(4): 
                    nx = curr[0] + dx[k]
                    ny = curr[1] + dy[k]

                    if (bricks[nx][ny] == tgt and not vis[nx][ny]): 
                        stack.append((nx, ny))
                        vis[nx][ny] = 1

            # dimensioning
            width = maxx - minx + 1
            height = maxy - miny + 1

            if (width == 1 and height == 1): 
                continue

            brick_img = Image.open(f"/home/pchellia/Desktop/Legoify/legoify/brick_images/{width}x{height}.png")
            brick_img = brick_img.resize((width * 10, height * 10))
            image.paste(brick_img, (i * 10, j * 10))
            #print(i * 10, j * 10)

    image.save(output_filepath)

# Path to the bricks files directory
bricks_folder_path = "/home/pchellia/Desktop/Legoify/solutions/solutions"

# Output folder for the generated images
output_folder = "output_images"
os.makedirs(output_folder, exist_ok=True)

# Loop through all brick files
for filename in os.listdir(bricks_folder_path):
    if filename.endswith(".txt"):
        bricks_file_path = os.path.join(bricks_folder_path, filename)

        # Load bricks array from file
        bricks = load_bricks_array(bricks_file_path)
        # print(bricks)

        # Generate output file path
        output_filename = os.path.splitext(filename)[0] + ".png"
        output_filepath = os.path.join(output_folder, output_filename)

        # Draw bricks and save image
        draw_bricks(bricks, output_filepath)
