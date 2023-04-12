import os
rootdir = 'Data\ICSBGCs'

with open("bgc_filenames.json", "w+") as f:

    f.write("{")
    for acc in os.listdir(rootdir):
        if acc[0] != ".":
            f.write('"' + acc + '": {')
            for cluster in os.listdir(os.path.join(rootdir, acc)):
                if cluster[0] != ".":
                    f.write('"' + cluster + '": [')
                    for file in os.listdir(os.path.join(rootdir, acc, cluster)):
                        if file[0] != ".":
                            # do the printing
                            f.write('"' + file + '",')
                    f.write("],")
            f.write("},")
    f.write("}")