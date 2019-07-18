import os

from ranker.make_samples import DATASET_DIR


def get_pickle_paths(root_path=DATASET_DIR):
    """
    Return a list of paths to all image files in a directory (does not check subdirectories).
    """
    image_file_paths = []

    for root, dirs, filenames in os.walk(root_path):
        filenames = sorted(filenames)
        for filename in filenames:
            input_path = os.path.abspath(root)
            file_path = os.path.join(input_path, filename)

            file_extension = filename.split(".")[-1]
            if file_extension.lower() in ("pkl",):
                image_file_paths.append(file_path)

        break  # prevent descending into subfolders

    return image_file_paths
