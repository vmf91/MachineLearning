import os
import re
import glob
import time
import sys
import warnings
def create_image_list(image_dir, valid_image_formats, max_num_images_per_class):
    """Builds a list of training images from the file system.

    Analyzes the sub folders in the image directory, splits them into stable
    training, testing, and validation sets, and returns a data structure
    describing the lists of images for each label and their paths.

    # Arguments
        image_dir: string path to a folder containing subfolders of images.
        validation_pct: integer percentage of images reserved for validation.

    # Returns
        dictionary of label subfolder, with images split into training
        and validation sets within each label.
    """
    if not os.path.isdir(image_dir):
        raise ValueError("Image directory {} not found.".format(image_dir))
    image_lists = {}
    sub_dirs = [x[0] for x in os.walk(image_dir)]
    sub_dirs_without_root = sub_dirs[1:]  # first element is root directory
    dirs = []
    filenames = []
    for sub_dir in sub_dirs_without_root:
        file_list = []
        dir_name = os.path.basename(sub_dir)
        if dir_name == image_dir:
            continue

        if dir_name not in dirs:
            dirs.append(dir_name)

        print("Looking for images in '{}'".format(dir_name))
        for extension in valid_image_formats:
            file_glob = os.path.join(image_dir, dir_name, '*.' + extension)
            file_list.extend(glob.glob(file_glob))
        if not file_list:
            warnings.warn('No files found')
            continue
        if len(file_list) < 20:
            warnings.warn('Folder has less than 20 images, which may cause '
                            'issues.')
        elif len(file_list) > max_num_images_per_class:
            warnings.warn('WARNING: Folder {} has more than {} images. Some '
                            'images will never be selected.'
                            .format(dir_name, MAX_NUM_IMAGES_PER_CLASS))
        label_name = re.sub(r'[^a-z0-9]+', ' ', dir_name.lower())
        for file_name in file_list:
            base_name = os.path.basename(file_name)
            current_file = (dir_name + '/' + base_name, dirs.index(dir_name))
            filenames.append(current_file)

    return filenames

def progress(itr, iterations, cost, acc, epoch_cost, epoch_acc, new_line=False):

    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'

    l = 10
    p = int((itr/iterations)*l)

    progress_done_str = "=" * p

    if p > 0 and p < l:
        progress_done_str = progress_done_str + ">"
        progress_left_str = "." * (l - p - 1)
    elif p == l:
        progress_left_str = ""
    else:
        progress_left_str = "." * (l - p)

    progress = progress_done_str + progress_left_str

    if not new_line:
        sys.stdout.write("\r" + "[{}] {}/{} [{}] acc: {:.4f} loss: {:.4f} total acc: {:.4f} total loss: {:.4f}".format(time.strftime("%Y-%m-%d %H:%M:%S"), itr, iterations, progress, acc, cost, epoch_acc, epoch_cost))
        sys.stdout.flush()
 
