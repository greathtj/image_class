import sys
import os
import shutil
import random
from datetime import datetime
import yaml

from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                               QWidget, QDialog, QLabel, QMessageBox)

from widgets.dataset_make_dialog_ui import Ui_Dialog

class make_dataset_dialog(QDialog):
    def __init__(self, 
                 project_data:dict,
                 parent=None):
        super().__init__(parent)

        self.project_data = project_data
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Make Dataset")
        
        self.ui.pushButtonMake.clicked.connect(self.make_dataset)
        self.ui.pushButtonCancel.clicked.connect(self.close)

    def make_dataset(self):
        now = datetime.now()
        timestamp_string = now.strftime("%Y%m%d_%H%M%S")
        source_folder = f"{self.project_data.get('directory')}/data"
        target_folder = f"{self.project_data.get('directory')}/data/dataset/{timestamp_string}"

        # delete the target folder and it's contents if exists
        if os.path.exists(target_folder):
            try:
                shutil.rmtree(target_folder)
                print(f"Folder '{target_folder}' and all its contents have been successfully deleted.")
            except OSError as e:
                print(f"Error: {e.filename} - {e.strerror}.")
        else:
            print(f"The folder '{target_folder}' does not exist, so let's hang on.")

        # make train, valid, test folders
        os.makedirs(f"{target_folder}/train/images")
        os.makedirs(f"{target_folder}/train/labels")
        os.makedirs(f"{target_folder}/val/images")
        os.makedirs(f"{target_folder}/val/labels")
        os.makedirs(f"{target_folder}/test/images")
        os.makedirs(f"{target_folder}/test/labels")

        # get the splitted file list
        annotation_files = self.get_txt_files(source_folder)
        train, valid, test = self.split_files(annotation_files, 7/10, 2/10, 1/10)

        # copy the splitted files
        self.copy_paired_files(train, source_folder, f"{target_folder}/train")
        self.copy_paired_files(valid, source_folder, f"{target_folder}/val")
        self.copy_paired_files(test, source_folder, f"{target_folder}/test")

        # update annotation files by switching class to classID
        classes_path = f"{self.project_data.get("directory")}/data/classes.lst"
        self.convert_classes_in_file(f"{target_folder}/train/labels", classes_path)
        self.convert_classes_in_file(f"{target_folder}/val/labels", classes_path)
        self.convert_classes_in_file(f"{target_folder}/test/labels", classes_path)

        # update coordinate from {x1, y1, w, h} to {cx, cy, w, h}
        self.convert_x1y1wh_to_cxcywh(f"{target_folder}/train/labels")
        self.convert_x1y1wh_to_cxcywh(f"{target_folder}/val/labels")
        self.convert_x1y1wh_to_cxcywh(f"{target_folder}/test/labels")

        # create a data.yaml file
        classes = []
        with open(classes_path, 'r') as file:
            for i, line in enumerate(file):
                class_name = line.strip()
                classes.append(class_name)
        self.create_yolo_yaml_file(target_folder, classes)

        # show message box
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Message")
        msg_box.setText(f"A new Dataset is prepared at {target_folder}.")
        msg_box.exec()

        self.close()

    def get_txt_files(self, folder_path):
        """
        Returns a list of all .txt file names in a specified folder.
        """
        if not os.path.exists(folder_path):
            print(f"Error: Folder '{folder_path}' does not exist.")
            return []
        
        # Get all file names and filter for .txt files
        file_list = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        return file_list
    
    def split_files(self, file_list, train_ratio, valid_ratio, test_ratio):
        """
        Splits a list of files into training, validation, and test sets
        based on the specified ratios.
        """
        total_files = len(file_list)
        
        # Shuffle the list randomly
        random.shuffle(file_list)
        
        # Calculate the number of files for each set
        train_count = int(total_files * train_ratio)
        valid_count = int(total_files * valid_ratio)
        
        # Slice the list to create the new lists
        train_set = file_list[:train_count]
        valid_set = file_list[train_count:train_count + valid_count]
        test_set = file_list[train_count + valid_count:]
        
        return train_set, valid_set, test_set
    
    def copy_paired_files(self, files, source_folder, target_folder):
        """
        Copies .txt and .jpg files with the same base name from a source folder
        to a target folder.
        """
        # Ensure source folder exists
        if not os.path.exists(source_folder):
            print(f"Error: Source folder '{source_folder}' does not exist.")
            return

        # Create the target folder if it doesn't exist
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            print(f"Created target folder '{target_folder}'.")

        # Process each file to find pairs
        for file_name in files:
            # Check if the file is a .txt file
            if file_name.endswith('.txt'):
                base_name = os.path.splitext(file_name)[0]
                jpg_file = base_name + '.jpg'
                
                # Construct full paths for the files
                txt_source_path = os.path.join(source_folder, file_name)
                jpg_source_path = os.path.join(source_folder, jpg_file)

                # Check if the corresponding .jpg file exists
                if os.path.exists(jpg_source_path):
                    # Construct full paths for the destination
                    txt_target_path = os.path.join(f"{target_folder}/labels", file_name)
                    jpg_target_path = os.path.join(f"{target_folder}/images", jpg_file)
                    
                    # Copy the .txt file
                    shutil.copy2(txt_source_path, txt_target_path)
                    print(f"Copied '{file_name}' to '{target_folder}'.")
                    
                    # Copy the .jpg file
                    shutil.copy2(jpg_source_path, jpg_target_path)
                    print(f"Copied '{jpg_file}' to '{target_folder}'.")

    def create_yolo_yaml_file(self, dfolder, classes):
        # current_folder_path = os.getcwd()
        absolute_path = os.path.abspath(dfolder)
        data = {
            'path':f'{absolute_path}',
            'train':'train',
            'test':'test',
            'val':'val',
            'names':classes,
        }

        # File path to save the YAML file
        file_path = f'{dfolder}/data.yaml'

        # Write the data to a YAML file
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

        return file_path
    
    def convert_classes_in_file(self, file_folder, classes_file):
        """
        Reads a .txt file, converts string classes to integer IDs,
        and overwrites the file with the new content.
        """
        class_map = {}

        with open(classes_file, 'r') as file:
            for i, line in enumerate(file):
                class_name = line.strip()
                if class_name:  # Ensure the line is not empty
                    class_map[class_name] = i

        print(class_map)

        annotation_files = [f for f in os.listdir(file_folder) if f.endswith('.txt')]
        for a_file in annotation_files:
            modified_lines = []
            
            # Read the original file
            with open(f"{file_folder}/{a_file}", 'r') as f:
                lines = f.readlines()
                
            # Process each line
            for line in lines:
                parts = line.strip().split()
                
                # Ensure the line has the correct number of parts
                if len(parts) == 5:
                    class_str = parts[0]
                    
                    # Check if the class string exists in our map
                    if class_str in class_map:
                        class_id = class_map[class_str]
                        x, y, w, h = parts[1:]
                        
                        # Format the new line with the integer class ID
                        new_line = f"{class_id} {x} {y} {w} {h}\n"
                        modified_lines.append(new_line)
                    else:
                        # If a class is not found, keep the original line or handle the error
                        print(f"Warning: Class '{class_str}' not found in map. Skipping line in {a_file}")
                        modified_lines.append(line)
                else:
                    # Handle malformed lines
                    print(f"Warning: Malformed line in {a_file}: '{line.strip()}'")
                    modified_lines.append(line)

            # Write the modified lines back to the file
            with open(f"{file_folder}/{a_file}", 'w') as f:
                f.writelines(modified_lines)
            
            print(f"Successfully converted classes in '{a_file}'.")

    def convert_x1y1wh_to_cxcywh(self, file_folder):
        """
        Converts bounding box coordinates in a .txt file from (classid, left, top, w, h)
        to (classid, center_x, center_y, w, h).

        Args:
            file_path (str): The path to the .txt file to be converted.
        """
        annotation_files = [f for f in os.listdir(file_folder) if f.endswith('.txt')]
        for a_file in annotation_files:
            modified_lines = []
            
            # Read the original file
            with open(f"{file_folder}/{a_file}", 'r') as f:
                lines = f.readlines()
                
            # Process each line
            for line in lines:
                parts = line.strip().split()
                
                # Ensure the line has 5 parts
                if len(parts) == 5:
                    # Parse values, converting to float for calculations
                    class_id = parts[0]
                    left, top, w, h = map(float, parts[1:])
                    
                    # Calculate center_x and center_y
                    center_x = left + (w / 2)
                    center_y = top + (h / 2)
                    
                    # Create the new line with the updated format
                    new_line = f"{class_id} {center_x:.6f} {center_y:.6f} {w:.6f} {h:.6f}\n"
                    modified_lines.append(new_line)
                else:
                    # Keep malformed lines as they are
                    modified_lines.append(line)
                    print(f"Warning: Skipping malformed line in {a_file}: '{line.strip()}'")

            # Overwrite the file with the new content
            with open(f"{file_folder}/{a_file}", 'w') as f:
                f.writelines(modified_lines)
            
            print(f"Successfully converted bounding boxes in '{a_file}'.")