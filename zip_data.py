import os
import shutil
rootdir = os.path.join(os.getcwd(), 'Data\ICSBGCs')

os.chdir(rootdir)
for acc in os.listdir(rootdir):
    if acc[0] != ".":
        shutil.make_archive(acc, "zip", os.path.join(rootdir, acc))
        shutil.move(os.path.join(rootdir, acc + ".zip"), os.path.join(rootdir, acc, acc + ".zip"))
        # for cluster in os.listdir(os.path.join(rootdir, acc)):
        #     if cluster[0] != "." and not cluster.endswith("zip"):
        #         # print(cluster)
        #         os.chdir(os.path.join(rootdir, acc, cluster))
        #         shutil.make_archive(cluster, "zip", os.path.join(rootdir, acc, cluster))