import json
import subprocess
import sys
import os
from PySide6.QtWidgets import QWidget, QFileDialog, QTableWidgetItem, QTableWidget, QMessageBox
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtGui import QPixmap
import time
import datetime
import random
import shutil

from ultralytics import YOLO

from widgets.project_manager_ui import Ui_FormProjectManager
from widgets.annotation_manager import AnnotationWidget
from widgets.annotate_dialog import AnnotateDialog
from widgets.video_stream_manager import VideoStreamer

class image_classifier():
    
    def __init__(
            self, 
            parentui: Ui_FormProjectManager,
            projec_data, 
            my_annotator: AnnotationWidget,
            my_video: VideoStreamer,
            parent=None
        ):

        self.project_data = projec_data
        self.my_annotator = my_annotator
        self.my_video = my_video
        self.my_parent = parent

        self.capture_timer = QTimer(self.my_parent)
        self.capture_timer.setInterval(200)  # 0.2 seconds
        self.capture_timer.timeout.connect(self.take_shot)

        self.ui = parentui
        self.ui.pushButtonTakeShots.pressed.connect(self.start_taking_shots)
        self.ui.pushButtonTakeShots.released.connect(self.stop_taking_shots)
        self.ui.pushButtonTakeShots.clicked.connect(self.take_shot)
        self.ui.pushButtonAnnotate.clicked.connect(self.start_annotation)
        self.ui.pushButtonMakeDataset.clicked.connect(self.make_dataset)

        self.ui.pushButtonDeleteFiles.clicked.connect(self.delete_files)

        self.ui.pushButtonUpdateDatasets.clicked.connect(self.update_datasets)
        self.ui.pushButtonStartTrain.clicked.connect(self.start_train)

        self.ui.pushButtonRefreshTrainedModels.clicked.connect(self.update_trained_models)
        self.ui.pushButtonToggleInference.clicked.connect(self.toggle_inference)


    def toggle_inference(self):
        if self.my_video and self.my_video.is_detecting:
            self.my_video.is_detecting = False
        elif self.my_video and not self.my_video.is_detecting:
            sel_model = self.ui.comboBoxTrainedModels.currentText()
            if sel_model:
                model_path = f"{self.project_data.get('directory')}/trained_models/{sel_model}/weights/best.pt"
                self.my_video.set_model(model_path)
                self.my_video.is_detecting = True


    def update_trained_models(self):
        trained_model_list = self.get_subfolders_scandir(f"{self.project_data.get('directory')}/trained_models")
        self.ui.comboBoxTrainedModels.clear()
        self.ui.comboBoxTrainedModels.addItems(trained_model_list)

    def start_train(self):
        # check the selection
        this_dataset = self.ui.comboBoxSelectedDataset.currentText()
        if this_dataset:
            dataset_folder = f"{self.project_data.get('directory')}/dataset/{this_dataset}"
            if not os.path.exists(dataset_folder):
                QMessageBox.information(self.my_parent, "No dataset folder", "Dataset folder is not prepared.")
                return
            
            if os.path.exists(f"{dataset_folder}/train_dataset"):
                shutil.rmtree(f"{dataset_folder}/train_dataset")
            
            # copy files to train_dataset
            with open(f"{dataset_folder}/train.json", 'r') as f:
                dict_train = json.load(f)
                self.organize_files_by_annotation(
                    dict_train, 
                    f"{self.project_data.get('directory')}/dataset", 
                    f"{dataset_folder}/train_dataset/train"
                )
            with open(f"{dataset_folder}/test.json", 'r') as f:
                dict_test = json.load(f)
                self.organize_files_by_annotation(
                    dict_test, 
                    f"{self.project_data.get('directory')}/dataset", 
                    f"{dataset_folder}/train_dataset/test"
                )
            with open(f"{dataset_folder}/val.json", 'r') as f:
                dict_val = json.load(f)
                self.organize_files_by_annotation(
                    dict_val, 
                    f"{self.project_data.get('directory')}/dataset", 
                    f"{dataset_folder}/train_dataset/val"
                )

            # run yolo train
            pretrained_model = self.ui.comboBoxPreTrainedModel.currentText()
            # model = YOLO(pretrained_model)
            # results = model.train(
            #     data=f"{dataset_folder}/train_dataset",
            #     epochs = int(self.ui.lineEditEpochs.text()),
            #     imgsz = int(self.ui.comboBoxImageSize.currentText()),
            #     project = f"{self.project_data.get('directory')}/trained_models",
            #     name = self.ui.lineEditTrainTitle.text()
            # )

            python_executable = sys.executable
            script_path = os.path.join(os.path.dirname(__file__), 'trainer_gui.py')
            command = [
                python_executable, 
                script_path,
                "--data", f"{dataset_folder}/train_dataset",
                "--epochs", self.ui.lineEditEpochs.text(),
                "--model", pretrained_model,
                "--imgsz", self.ui.comboBoxImageSize.currentText(),
                "--project", f"{self.project_data.get('directory')}/trained_models",
                "--name", self.ui.lineEditTrainTitle.text()
            ]
            result = subprocess.run(command, text=True, check=True)

    def organize_files_by_annotation(
        self,
        annotation_dict: dict,
        source_base_folder: str,
        destination_base_folder: str
    ) -> tuple[list[str], list[str]]:
        """
        Copies image files to subfolders named after their annotated class.

        Args:
            annotation_dict (dict): A dictionary where keys are filenames (e.g., "image.jpg")
                                    and values are their corresponding class names (e.g., "cat").
            source_base_folder (str): The path to the folder containing the original image files.
            destination_base_folder (str): The path to the base folder where class subfolders
                                        (e.g., 'destination_base_folder/cat/',
                                        'destination_base_folder/dog/') will be created.

        Returns:
            tuple[list[str], list[str]]: A tuple containing two lists:
                                        - The first list contains paths of successfully copied files.
                                        - The second list contains paths of files that failed to copy,
                                            along with the error message.
        """
        successfully_copied = []
        failed_copies = []

        # 1. Validate source base folder existence
        if not os.path.isdir(source_base_folder):
            error_msg = f"Error: Source base folder '{source_base_folder}' does not exist or is not a directory."
            print(error_msg)
            return [], [error_msg]

        # 2. Ensure destination base folder exists (create if not)
        if not os.path.exists(destination_base_folder):
            try:
                os.makedirs(destination_base_folder)
                print(f"Created destination base folder: '{destination_base_folder}'")
            except OSError as e:
                error_msg = f"Failed to create destination base folder '{destination_base_folder}': {e}"
                print(f"Error: {error_msg}")
                return [], [error_msg]
        else:
            print(f"Destination base folder '{destination_base_folder}' already exists.")

        if not annotation_dict:
            print("Annotation dictionary is empty. No files to organize.")
            return [], []

        print(f"\nStarting file organization from '{source_base_folder}' to '{destination_base_folder}':")

        # 3. Iterate through each item in the annotation dictionary
        for filename, class_name in annotation_dict.items():
            source_file_path = os.path.join(source_base_folder, filename)
            
            # 4. Construct the path for the class-specific subfolder
            target_class_folder = os.path.join(destination_base_folder, class_name)
            
            # 5. Create the class-specific subfolder if it doesn't exist
            if not os.path.exists(target_class_folder):
                try:
                    os.makedirs(target_class_folder)
                    print(f"  Created class folder: '{target_class_folder}'")
                except OSError as e:
                    failed_copies.append(f"'{filename}': Failed to create class folder '{target_class_folder}': {e}")
                    print(f"  Error creating folder for '{filename}': {e}")
                    continue # Skip copying this file if folder creation failed

            destination_file_path = os.path.join(target_class_folder, filename)

            # 6. Copy the file
            if os.path.exists(source_file_path):
                try:
                    # shutil.copy2 preserves metadata (timestamps, permissions)
                    shutil.copy2(source_file_path, destination_file_path)
                    successfully_copied.append(destination_file_path)
                    print(f"  Copied '{filename}' to '{class_name}/'")
                except Exception as e:
                    failed_copies.append(f"'{filename}': Failed to copy to '{class_name}': {e}")
                    print(f"  Error copying '{filename}': {e}")
            else:
                failed_copies.append(f"'{filename}': Source file not found at '{source_file_path}'")
                print(f"  Warning: Source file not found: '{filename}' at '{source_file_path}'")

        return successfully_copied, failed_copies

    def update_datasets(self):
        dataset_list = self.get_subfolders_scandir(f"{self.project_data.get('directory')}/dataset")
        self.ui.comboBoxSelectedDataset.clear()
        self.ui.comboBoxSelectedDataset.addItems(dataset_list)

    def get_subfolders_scandir(self, folder_path: str) -> list[str]:
        """
        Gets a list of immediate subfolder names within a given folder using os.scandir().

        Args:
            folder_path (str): The path to the parent folder.

        Returns:
            list[str]: A list of names of the immediate subfolders.
                    Returns an empty list if the folder does not exist,
                    is not a directory, or has no subfolders.
        """
        subfolders = []
        if not os.path.isdir(folder_path):
            print(f"Error: Folder '{folder_path}' does not exist or is not a directory.")
            return []
        
        try:
            with os.scandir(folder_path) as entries:
                for entry in entries:
                    if entry.is_dir():
                        subfolders.append(entry.name)
        except OSError as e:
            print(f"Error accessing folder '{folder_path}': {e}")
            return []
            
        return sorted(subfolders)

    def make_dataset(self):
        # get the annotation inforamtion
        annotation_info_path = self.project_data.get("directory") + "/data/annotation_info.json"
        if not os.path.exists(annotation_info_path):
            QMessageBox.information(self.my_parent, "No annotation file", "No annotation file, check your annotation.")
            return
        
        with open(annotation_info_path, 'r') as f:
            annotation_info = json.load(f)
            print("Annotation info file opens successfully.")

        # split data into train, test, and val
        train_dict, test_dict, val_dict = self.split_dict_randomly(annotation_info)

        # copy files to the destination folder
        self.copy_files_from_dict_keys(
            annotation_info, 
            self.project_data.get("directory") + "/data", 
            self.project_data.get("directory") + "/dataset")

        # save the dataset inforamtion
        if self.project_data:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            dataset_dir = f"{self.project_data.get('directory')}/dataset/{timestamp}"
            try:
                os.makedirs(dataset_dir, exist_ok=True)
                print(f"Folder '{dataset_dir}' ensured to exist.")

                self.save_dict_as_json(train_dict, f"{dataset_dir}/train.json")
                self.save_dict_as_json(test_dict, f"{dataset_dir}/test.json")
                self.save_dict_as_json(val_dict, f"{dataset_dir}/val.json")

                self.update_datasets()
            except OSError as e:
                print(f"Error creating folder '{dataset_dir}': {e}")

    def copy_files_from_dict_keys(
        self,
        annotation_dict: dict,
        source_folder: str,
        destination_folder: str
    ) -> tuple[list[str], list[str]]:
        """
        Copies files specified by keys in a dictionary from a source folder to a destination folder.

        Args:
            annotation_dict (dict): A dictionary where keys are the filenames of the images.
            source_folder (str): The path to the directory where the original image files are located.
            destination_folder (str): The path to the directory where the files should be copied.

        Returns:
            tuple[list[str], list[str]]: A tuple containing two lists:
                                        - The first list contains paths of successfully copied files.
                                        - The second list contains paths of files that failed to copy,
                                            along with the error message.
        """
        successfully_copied = []
        failed_copies = []

        # 1. Validate source folder existence
        if not os.path.isdir(source_folder):
            error_msg = f"Source folder '{source_folder}' does not exist or is not a directory."
            print(f"Error: {error_msg}")
            return [], [error_msg]

        # 2. Ensure destination folder exists (create if not)
        if not os.path.exists(destination_folder):
            try:
                os.makedirs(destination_folder)
                print(f"Created destination folder: '{destination_folder}'")
            except OSError as e:
                error_msg = f"Failed to create destination folder '{destination_folder}': {e}"
                print(f"Error: {error_msg}")
                return [], [error_msg]
        else:
            print(f"Destination folder '{destination_folder}' already exists.")

        if not annotation_dict:
            print("Annotation dictionary is empty. No files to copy.")
            return [], []

        print(f"\nAttempting to copy files from '{source_folder}' to '{destination_folder}':")

        # 3. Iterate through the filenames (keys) and copy each file
        for filename_key in annotation_dict.keys():
            source_path = os.path.join(source_folder, filename_key)
            destination_path = os.path.join(destination_folder, filename_key)

            if os.path.exists(source_path):
                try:
                    # shutil.copy2 preserves metadata (timestamps, permissions)
                    shutil.copy2(source_path, destination_path)
                    successfully_copied.append(destination_path)
                    print(f"  Copied: '{filename_key}'")
                except Exception as e:
                    failed_copies.append(f"'{filename_key}': {e}")
                    print(f"  Error copying '{filename_key}': {e}")
            else:
                failed_copies.append(f"'{filename_key}': Source file not found at '{source_path}'")
                print(f"  Warning: Source file not found: '{filename_key}' at '{source_path}'")

        return successfully_copied, failed_copies


    def save_dict_as_json(self, data_dict: dict, file_path: str, indent: int = 4) -> bool:
        """
        Saves a Python dictionary to a JSON file.

        Args:
            data_dict (dict): The dictionary to be saved.
            file_path (str): The path where the JSON file will be created/overwritten.
            indent (int, optional): The number of spaces to use for indentation in the JSON file.
                                    Defaults to 4 for readability. Use None for no indentation (compact output).

        Returns:
            bool: True if the dictionary was successfully saved, False otherwise.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=indent)
            print(f"Successfully saved dictionary to '{file_path}'")
            return True
        except TypeError as e:
            print(f"Error: Cannot serialize dictionary to JSON. Check data types: {e}")
            return False
        except OSError as e: # Catches file-related errors like permission denied, disk full
            print(f"Error: Could not write to file '{file_path}': {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while saving to '{file_path}': {e}")
            return False


    def split_dict_randomly(
        self,
        original_dict: dict,
        train_ratio: float = 0.7,
        test_ratio: float = 0.20,
        val_ratio: float = 0.10
    ) -> tuple[dict, dict, dict]:
        """
        Randomly splits a dictionary into three dictionaries for training, testing, and validation.

        Args:
            original_dict (dict): The input dictionary where keys are filenames and values are class names.
            train_ratio (float): The proportion of data for the training set (e.g., 0.7).
            test_ratio (float): The proportion of data for the test set (e.g., 0.15).
            val_ratio (float): The proportion of data for the validation set (e.g., 0.15).

        Returns:
            tuple[dict, dict, dict]: A tuple containing (dict_train, dict_test, dict_val).
                                    Returns empty dictionaries if original_dict is empty.

        Raises:
            ValueError: If the sum of ratios is not approximately 1.0.
        """
        # Validate ratios
        if not (0 <= train_ratio <= 1 and 0 <= test_ratio <= 1 and 0 <= val_ratio <= 1):
            raise ValueError("Ratios must be between 0 and 1.")
        if abs(train_ratio + test_ratio + val_ratio - 1.0) > 1e-6: # Using a small epsilon for float comparison
            raise ValueError("The sum of train, test, and validation ratios must be approximately 1.0.")

        if not original_dict:
            print("Input dictionary is empty. Returning empty splits.")
            return {}, {}, {}

        # Get all items (key-value pairs) and shuffle them
        all_items = list(original_dict.items())
        random.shuffle(all_items)

        total_items = len(all_items)

        # Calculate split sizes
        train_size = int(total_items * train_ratio)
        test_size = int(total_items * test_ratio)
        # Validation size takes the remainder to ensure all items are used
        val_size = total_items - train_size - test_size

        # Slice the shuffled list
        train_items = all_items[:train_size]
        test_items = all_items[train_size : train_size + test_size]
        val_items = all_items[train_size + test_size :]

        # Convert sliced lists back to dictionaries
        dict_train = dict(train_items)
        dict_test = dict(test_items)
        dict_val = dict(val_items)

        print(f"Original items: {total_items}")
        print(f"Train split: {len(dict_train)} items ({train_ratio*100:.1f}%)")
        print(f"Test split:  {len(dict_test)} items ({test_ratio*100:.1f}%)")
        print(f"Val split:   {len(dict_val)} items ({val_ratio*100:.1f}%)")

        return dict_train, dict_test, dict_val

    def delete_files(self):
        # get the list of files from the tablewidget
        file_list = self.get_selected_first_column_texts(self.ui.tableWidgetFilesIC)
        if not file_list:
            QMessageBox.information(self.my_parent, "No Selection", "Please select at least one row to delete.")
            return
        
        # --- ASK USER FOR CONFIRMATION HERE ---
        confirm_msg = (
            f"You are about to permanently delete {len(file_list)} file(s).\n\n"
            "This action cannot be undone. Are you sure you want to proceed?"
        )
        reply = QMessageBox.question(
            self.my_parent,
            "Confirm Deletion",              # Window title
            confirm_msg,                     # Message to display
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, # Buttons
            QMessageBox.StandardButton.No    # Default button to highlight
        )        
        
        # delete a list of files
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_files_from_folder(f"{self.project_data.get('directory')}/data", file_list)

            # update annotation_info.json
            self.remove_items_from_json_by_keys(self.project_data.get("directory") + "/data/annotation_info.json", file_list)

            # update file list
            self.update_file_list()

    def remove_items_from_json_by_keys(self, file_path: str, keys_to_remove: list[str]) -> bool:
        """
        Removes items from a JSON file whose keys are present in the given list.

        Args:
            file_path (str): The path to the JSON file.
            keys_to_remove (list[str]): A list of keys to be removed from the JSON data.

        Returns:
            bool: True if the operation was successful, False otherwise.
                Returns True even if none of the keys were found in the file,
                as the desired state (keys absent) is maintained.
        """
        data = {}
        changes_made = False

        # 1. Read the JSON file (or handle its absence/invalidity)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"Successfully loaded JSON from '{file_path}'.")
            except json.JSONDecodeError:
                print(f"Error: '{file_path}' contains invalid JSON. Cannot process file.")
                return False
            except Exception as e:
                print(f"Error reading '{file_path}': {e}.")
                return False
        else:
            print(f"File '{file_path}' does not exist. No items to remove.")
            return True # Considered successful as there's nothing to remove

        # Ensure the loaded data is a dictionary
        if not isinstance(data, dict):
            print(f"Error: JSON content of '{file_path}' is not a dictionary. Cannot remove items.")
            return False

        # 2. Iterate through the keys_to_remove and delete matching items
        print(f"Attempting to remove keys: {keys_to_remove}")
        for key in keys_to_remove:
            if key in data:
                del data[key]
                print(f"  Removed key: '{key}'")
                changes_made = True
            else:
                print(f"  Key '{key}' not found in file. Skipping.")

        # 3. Write the modified dictionary back to the JSON file (only if changes were made or file was empty)
        if changes_made or not data: # Write back if something was deleted or if data became empty
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4) # Use indent for pretty-printing
                print(f"Successfully wrote updated JSON to '{file_path}'.")
                return True
            except Exception as e:
                print(f"Error writing to '{file_path}': {e}")
                return False
        else:
            print("No matching keys found and no changes made to the file.")
            return True # Considered successful as no action was needed

    def delete_files_from_folder(self, folder_path: str, files_to_delete: list[str]) -> tuple[list[str], list[str]]:
        """
        Deletes a list of files from a specified folder.

        Args:
            folder_path (str): The path to the folder where the files are located.
            files_to_delete (list[str]): A list of filenames (not full paths)
                                        to be deleted from the folder.

        Returns:
            tuple[list[str], list[str]]: A tuple containing two lists:
                                        - The first list contains paths of successfully deleted files.
                                        - The second list contains paths of files that failed to delete,
                                            along with the error message.
        """
        successfully_deleted = []
        failed_to_delete = []

        if not os.path.isdir(folder_path):
            print(f"Error: Folder '{folder_path}' does not exist or is not a directory.")
            return [], [f"Folder '{folder_path}' not found."]

        if not files_to_delete:
            print("No files specified for deletion.")
            return [], []

        print(f"Attempting to delete files from: '{folder_path}'")

        for file_name in files_to_delete:
            full_file_path = os.path.join(folder_path, file_name)
            
            if os.path.exists(full_file_path):
                try:
                    os.remove(full_file_path)
                    successfully_deleted.append(full_file_path)
                    print(f"  Deleted: {full_file_path}")
                except OSError as e:
                    failed_to_delete.append(f"'{full_file_path}': {e}")
                    print(f"  Error deleting '{full_file_path}': {e}")
            else:
                failed_to_delete.append(f"'{full_file_path}': File not found")
                print(f"  Warning: File not found: {full_file_path}")

        return successfully_deleted, failed_to_delete

    def get_selected_first_column_texts(self, this_table_widget:QTableWidget):
        """
        Retrieves the text from the first column (index 0)
        of all currently selected rows.
        """
        selected_names = []
        
        # Get unique row indices from all selected cells
        # We use a set to ensure unique row numbers, then convert to list for iteration
        # No need to sort if we just iterate and get items.
        unique_selected_rows = {index.row() for index in this_table_widget.selectedIndexes()}
        if not unique_selected_rows:
            QMessageBox.information(self.my_parent, "No Selection", "Please select at least one row to delete.")
            return

        if not unique_selected_rows:
            self.result_label.setText("Names: No rows selected.")
            print("No rows selected.")
            return None

        for row_index in sorted(list(unique_selected_rows)): # Sort for consistent order in output
            # Get the QTableWidgetItem from the first column (index 0) of the current row
            item = this_table_widget.item(row_index, 0)
            if item is not None:
                selected_names.append(item.text())
            else:
                # This case typically indicates an empty cell or an issue, but defensively handle it
                print(f"Warning: No item found at row {row_index}, column 0.")

        print(f"Selected names from first column: {selected_names}")
        return selected_names

    def start_annotation(self):
        my_annotate_dialog = AnnotateDialog(
            project_data=self.project_data,
            parent=self.my_parent
        )
        my_annotate_dialog.exec()

    def start_taking_shots(self):
        self.capture_timer.start()

    def stop_taking_shots(self):
        self.capture_timer.stop()

    def take_shot(self):
        if self.project_data and self.my_annotator:
            data_dir = f"{self.project_data.get('directory')}/data"
            try:
                os.makedirs(data_dir, exist_ok=True)
                print(f"Folder '{data_dir}' ensured to exist.")
            except OSError as e:
                print(f"Error creating folder '{data_dir}': {e}")

            if data_dir and os.path.exists(data_dir):
                pixmap = self.my_annotator.current_pixmap
                # timestamp = int(time.time() * 1000)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                file_path = os.path.join(data_dir, f"shot_{timestamp}.jpg")
                pixmap.save(file_path, "JPG")
                print(f"Image saved to {file_path}")
                self.update_file_list()

    def update_file_list(self):
        if self.project_data:
            data_dir = f"{self.project_data.get('directory')}/data"
            try:
                os.makedirs(data_dir, exist_ok=True)
                print(f"Folder '{data_dir}' ensured to exist.")
            except OSError as e:
                print(f"Error creating folder '{data_dir}': {e}")

            if data_dir and os.path.exists(data_dir):
                files = sorted([f for f in os.listdir(data_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
                self.ui.tableWidgetFilesIC.setRowCount(len(files))
                self.ui.tableWidgetFilesIC.setColumnCount(2)
                self.ui.tableWidgetFilesIC.setHorizontalHeaderLabels(["File Name", "Class"])
                self.ui.tableWidgetFilesIC.setColumnWidth(0, 250)
                self.ui.tableWidgetFilesIC.setColumnWidth(1, 60)
                for row, file_name in enumerate(files):
                    self.ui.tableWidgetFilesIC.setItem(row, 0, QTableWidgetItem(file_name))
                    self.ui.tableWidgetFilesIC.setItem(row, 1, QTableWidgetItem(""))

