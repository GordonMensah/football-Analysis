import os
from roboflow import Roboflow
from dotenv import load_dotenv
from PIL import Image

# Get the current working directory
Home = os.getcwd()
print(f"Current Working Directory: {Home}")

# Load environment variables
load_dotenv('C:/Users/mhizg/OneDrive/Desktop/JOseph/Football/src/data/.env.txt')

# Retrieve API key from environment variables
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found in environment variables. Please check your .env file.")

# Initialize Roboflow
rf = Roboflow(api_key=api_key)

# Load a project
project = rf.workspace("roboflow-jvuqo").project("football-players-detection-3zvbc")
version = project.version(12)
dataset = version.download("yolov8")

# Define the path to the data.yaml file (inside the downloaded dataset)
data_yaml_path = os.path.join(dataset.location, "data.yaml")

# Verify if the data.yaml file exists
if not os.path.exists(data_yaml_path):
    raise FileNotFoundError(f"data.yaml not found at: {data_yaml_path}")

# Read and modify the data.yaml file
with open(data_yaml_path, 'r') as file:
    lines = file.readlines()

with open(data_yaml_path, 'w') as file:
    for line in lines:
        if line.startswith('train:'):
            file.write('train: ../train/images\n')  # Corrected newline character
        elif line.startswith('val:'):
            file.write('val: ../valid/images\n')  # Corrected newline character
        else:
            file.write(line)

print("data.yaml file updated successfully!")

# Example: Display an image from the dataset
image_folder = os.path.join(dataset.location, "train", "images")
if os.path.exists(image_folder):
    # Get the first image in the folder
    first_image = os.listdir(image_folder)[0]
    image_path = os.path.join(image_folder, first_image)

    # Open and display the image
    img = Image.open(image_path)
    img.show()
else:
    print(f"Image folder not found: {image_folder}")