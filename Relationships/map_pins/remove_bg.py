from PIL import Image
import os

def remove_background(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        datas = img.getdata()
        
        newData = []
        # Get the color of the top-left pixel to use as the background color
        # Assuming the background is uniform or the corner is representative
        bg_color = datas[0]
        
        # Define a tolerance for color matching
        tolerance = 50 

        for item in datas:
            # Check if the pixel is close to the background color
            if all(abs(item[i] - bg_color[i]) < tolerance for i in range(3)):
                newData.append((255, 255, 255, 0)) # Make it transparent
            else:
                newData.append(item)
        
        img.putdata(newData)
        # Verify if it actually looks transparent (optional check could be added here)
        
        # Save gracefully, maybe backup original
        img.save(image_path, "PNG")
        print(f"Processed: {os.path.basename(image_path)}")
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

folder_path = r"c:\Users\ga-fie\personlig\relationships\map_pins"

for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        file_path = os.path.join(folder_path, filename)
        remove_background(file_path)

print("All done!")
