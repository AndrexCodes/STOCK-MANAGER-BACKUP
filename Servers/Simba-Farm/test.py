import os

def change_extension(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print("Folder path does not exist.")
        return
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the item is a file
        if os.path.isfile(os.path.join(folder_path, filename)):
            # Split the file name and extension
            name, ext = os.path.splitext(filename)
            # Rename the file with .jpg extension
            new_filename = name + '.jpg'
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
            print(f"Renamed {filename} to {new_filename}")

# Change the folder path to the directory containing the files you want to rename
folder_path = 'C:/Users/Andrew codes/Desktop/simba images'
change_extension(folder_path)
