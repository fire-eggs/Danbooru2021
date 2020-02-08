# determine if 'duplicate' files exist based on the file *name* (not extension)
# needed to identify .GIF and .PNG duplication
#
# For unknown reasons, Gwern's fileset contains a few PNG files which are
# duplicates of other GIF files. The GIF files are the ones in the metadata.
#
import os

root_path="g:\original"
for root, dir, files in os.walk(root_path):
    fname_dict = {}
    for file in files:
        base = os.path.basename(file)
        filen = os.path.splitext(base)
        if (filen[0] in fname_dict):
            print(os.path.join(root,file))
        else:
            fname_dict[filen[0]] = 0
