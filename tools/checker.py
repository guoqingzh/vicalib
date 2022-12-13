from os import listdir
from os.path import isfile,join, exists
import numpy as np 
import xml
import xml.etree.ElementTree as ET
import csv
import sys


has_init_value = sys.argv[1]
mypath="./cali_seq/rgb_0"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath,f))]
num_frames = len(onlyfiles);
print("Totally frames:{}".format(num_frames))
timestamps = []
for f in onlyfiles:
    _,_,n = f.split("_")
    timestamps.append(float(n[:-4]))

timestamps = np.array(timestamps)
timestamps = np.sort(timestamps)
delta = timestamps[1:] - timestamps[:-1]

max_fps = (1/delta).max()
min_fps = (1/delta).min()
std_fps = (1/delta).std()
avg_fps = (1/delta).mean()

print("MAX FPS:", (1/delta).max())
print("MIN FPS", (1/delta).min())
print("STD FPS", (1/delta).std())
print("AVG FPS", (1/delta).mean())

tree = ET.parse('rs.xml')
root = tree.getroot()
camera_model = root[0][0]

camera_intrinsic = eval(camera_model[5].text.replace(';', ','))
pose = root[0][1]
camera_imu_extrinsic = eval(pose[0].text.replace(';',','))


result_file = "./results.csv"

result_file_exists = exists(result_file)


rmse = -1;
with open('rmse_and_imu.txt') as f:
    rmse = float(f.readline().strip('\n'))

with open(result_file, 'a', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=",")
    if not result_file_exists:
        csv_writer.writerow(['init','num_frames', 'std_fps', 'avg_fps', 'rmse','ext_x', 'ext_y', 'ext_z', 'fx', 'fy', 'cx', 'cy'])
    csv_writer.writerow([has_init_value, num_frames, std_fps, avg_fps, rmse, camera_imu_extrinsic[3], camera_imu_extrinsic[7], camera_imu_extrinsic[11], camera_intrinsic[0], camera_intrinsic[1], camera_intrinsic[2], camera_intrinsic[3]])







