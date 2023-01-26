rm -fr cali_seq
mkdir -p cali_seq/rgb_0

model_str="-models poly3"

init=$1
res=$2
fps=$3
echo "Camera configration:"
echo "Resolution: $res"
echo "FPS: $fps"

if [[ "$init" == "1" ]]
then
    echo "Calibrate with initial value..."
    if [[ "$2" == "1280x720" ]]
    then
      model_str="-model_files init_$res.xml"
    elif [[ "$2" == "848x480" ]]
    then
      model_str="-model_files init_$res.xml"
    elif [[ "$2" ==  "640x480" ]]
    then	    
      model_str="-model_files init_$res.xml"
    else
      echo "Unsupported resolution $res"
      exit 0
    fi   	    
else
    echo "Calibrate without initial value..."	
fi

vicalib -grid-preset small '$model_str' -output rs.xml -accel_sigma 0.1 -gyro_sigma 0.05   -save_poses -remove_outliers -cam realsense2:[id0=134222076632,size=$res,fps=$fps,rgb=1,depth=0,ir0=0,ir1=0,emitter=0.462,exposure=0,gain=64]// -imu rs2imu:[id0=134222076632]// --logtostderr=1 2>&1 | tee log
python3 checker.py $init
