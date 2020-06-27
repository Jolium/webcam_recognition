"""
Encode and Decode NumPy array to and from JSON file
"""

import face_recognition
import json
import numpy as np
import os

import settings as sets
import hash_sha1


folder_path = sets.folder_path
allowed_formats = sets.allowed_formats
database = sets.database


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


def import_from_database():
    """Import data from database.json"""

    # Deserialization (JSON file into Numpy Array)
    with open(database, 'r', encoding='utf-8') as db:
        data = json.load(db)
        encodings = np.asarray(data["array"])
        names = np.asarray(data["names"])

    return encodings, names


def _export_to_database(names, face_encodings):
    """Export all data to database.json"""

    # Get hash of the folder 'images'
    folder_hash = hash_sha1.hash_directory()

    # Serialization (NumPy Array into JSON file)
    data = {"sha1": folder_hash, "names": names, "array": face_encodings}
    with open(database, 'w', encoding='utf-8') as db:
        json.dump(data, db, cls=NumpyArrayEncoder, ensure_ascii=False, indent=2)


def create_database(path=folder_path):
    """Create lists to be exported to database.json"""

    images = os.listdir(path)
    formats = allowed_formats
    known_face_names = []
    known_face_encodings = []

    for i in images:
        if i.endswith(formats):

            # Creates a list with all names of known faces
            name = os.path.splitext(i)
            known_face_names.append(name[0])

            # Create arrays of known face encodings
            known_image = face_recognition.load_image_file(path + i)
            known_face_encoding = face_recognition.face_encodings(known_image)
            known_face_encodings.extend(known_face_encoding)

    if path == folder_path:
        _export_to_database(known_face_names, known_face_encodings)
    else:
        return known_face_names, known_face_encodings


def update_database(path):
    """
    Import pictures from non standard folders
    Append/update new entries to database.json

    example:

    path = './new_folder/'  # path to non standard folder
    update_database(path)  # Add all pictures in new_folder
    """

    names, face_encodings = create_database(path=path)

    # Add new entries to database.json
    with open(database, 'r', encoding='utf-8') as db:
        data = json.load(db)

        temp_names = data['names']
        temp_names.extend(names)

        temp_face_encodings = data['array']
        temp_face_encodings.extend(face_encodings)

    _export_to_database(temp_names, temp_face_encodings)
