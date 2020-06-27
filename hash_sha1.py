import json
import hashlib
import os

import settings as sets
import encoder


folder_path = sets.folder_path
database = sets.database


def hash_directory(path=folder_path):
    digest = hashlib.sha1()

    for root, dirs, files in os.walk(path):
        for names in files:
            file_path = os.path.join(root, names)

            # Hash the path and add to the digest to account for empty files/directories
            digest.update(hashlib.sha1(file_path[len(path):].encode()).digest())

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f_obj:
                    while True:
                        buf = f_obj.read(1024 * 1024)
                        if not buf:
                            break
                        digest.update(buf)

    return digest.hexdigest()


def compare_hashes():
    new_hash = hash_directory()
    with open(database, encoding='utf-8') as db:
        data = json.load(db)
        old_hash = data['sha1']
    if new_hash != old_hash:
        encoder.create_database()
