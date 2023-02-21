"""\
This script converts rotation-matrix to euler angles using the pose information 
in rs.xml file as input
Usage: python3 rot2euler.py
"""

# Import the required packages
import xml.etree.ElementTree as ET
from numpy import reshape
from scipy.spatial.transform import Rotation

# Read the cam_imu calibration file as input
tree = ET.parse('rs.xml')

# The parent tag of the xml document
root = tree.getroot()

# Extract camera pose matrix
camera_pose_str = root[0][1][0].text

camera_pose = list(camera_pose_str.split(" "))

# Get rid of extra elements
camera_pose = camera_pose[2:-2]
# Get rid of extra , and ; chars
camera_pose = [camera_pose_elem.replace(',', '') for camera_pose_elem in  camera_pose]
camera_pose = [camera_pose_elem.replace(';', '') for camera_pose_elem in  camera_pose]
rot_matrix = [float(x) for x in camera_pose]

# Remove the translation matrix (3x1), leaving only the rotation matrix
del(rot_matrix[3]);del(rot_matrix[6]);del(rot_matrix[9]);

rot_matrix = reshape(rot_matrix, (3,3))

#print(rot_matrix)

# Transform the rotation matrix to euler angles
r =  Rotation.from_matrix(rot_matrix)
angles = r.as_euler("zyx", degrees=True)

print("Pose angles (YPR): ", angles)

# Write output tot he file
poseFile = open("pose.txt", "w")
poseFile.write(str(angles))
poseFile.close()

