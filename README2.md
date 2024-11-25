# VLMaps Server for MRP

This repository contains the additional code needed to integrate VLMaps into the mobile telepresence system with the Tiago robot, building on the original VLMaps implementation from the upstream repository. It provides a REST API server that serves the VLMaps data, which can be accessed by the telepresence client via a POST request. The API endpoint accepts the robot's current pose, dialogue history, and the ongoing conversation, and returns the coordinates of potential follow-up navigation points on the map.

## Dependencies

All dependencies for this fork are listed in the `requirements.txt` file, along with the original packages required by the upstream repository.

Since the codebase is optimized for GPU use, additional setup for CUDA/cuDNN may be required on your system.

## Building VLMaps from Real-World Data

The **[README](README.md)** in the upstream repository provides a general overview of the steps for building VLMaps from real-world data. Below are the specific instructions for using **[RTAB-Map](https://github.com/introlab/rtabmap_ros)** with an Azure Kinect mounted on the Tiago robot.

1. **Set up the necessary drivers, packages, and tools** for RTAB-Map and Azure Kinect. The RTAB-Map repository includes detailed instructions for setting up and running simple examples in ROS. Setup guidelines for the Azure Kinect camera can be found in the [official repository](https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md#debian-package), with additional information available in the lab wiki.
   
2. **Mount the Kinect on the Tiago's head**. An STL file is provided in the `mount/` directory for 3D printing the mount. Add the necessary transforms for the Kinect's frame in the ROS launch file.

3. **Build a 3D point cloud using RTAB-Map**. Start the robot, but **do not move it** before running the mapping process. This ensures that the mapping process starts at the origin of the odometry frame, aligning the map frame in RTAB-Map with the VLMaps orientation. However, the x and y coordinates will still need to be adjusted by certain offsets. These can be configured later using the `offset_x` and `offset_y` class variables in `vlmaps/robot/api_robot.py`.

4. **Extract RGB-D frames and optimized poses from RTAB-Map** using the database viewer tool:
    - For poses: `File` -> `Export poses` -> `RGBD-SLAM ID format` -> Select `Map's graph` -> Choose the `camera` frame.
    - For RGB-D frames: `File` -> `Extract images` -> Select `id.png`.

5. **Move the `rgb` and `depth` directories**, as well as the `poses.txt` file, to a subdirectory named `0` under the `vlmaps_data_dir` specified in `config/data_paths/default.yaml`.

6. **Configure relevant parameters** following the instructions in the **[README](README.md)**.

7. **Run the script** located in `rgbd/prepare_data.py` to format the data as required by VLMaps.

8. **Build the map** following the steps in the **README.md**:
    - In `vlmaps.yaml`, set `pose_type` to `camera_base` and update `cam_calib_mat` using the `camera_matrix.data` from the `calib` directory.
    - Update `camera_height` in `params/default.yaml`.

**Important**: The original codebase was written for `mobile_base`, not `camera_base`. As a result, the `h_min` and `h_max` arguments in the `generate_obstacle_map` function (located in `vlmaps/map/map.py`) need to be updated. In general, the default `h_min` and `h_max` values should be increased by the camera height. Once the variables are set, check the generated obstacle map using `application/generate_obstacle_map.py` to ensure it looks correct.

## Usage

Once VLMaps is built, you can launch a REST API server to handle object indexing with the following command:

```
python3 server/api.py
```

After the server starts and loads the CLIP and map models, send a dummy request using a tool like Postman to initialize the necessary objects. This step helps reduce the latency of subsequent requests.

The API endpoint accepts POST requests with the following fields in the body:

- `pose`: The robot's current pose in ROS, using quaternion format.
- `past`: The full dialogue history between speakers. Speakers are represented alphabetically, with the teleoperator’s utterances always labeled as `A`.
- `current`: The current dialogue between speakers.

Here’s an example of a typical request:

```
{ "pose": [10.621, 4.455, 0, 0, 0, -0.5085501, 0.8610324], "past": "B: Let's check out the laptop next to the white robot first.\nA: Okay\nA: I think we are done here. Let's go to the kitchen counter\n", "current": "B: Hey, now I may need you to go back and take a look at the laptop from earlier." }
```

The server will return the coordinates and labels of objects related to potential follow-up actions in the following format:

```
{'movements': [{"actor": "A", "target": {"label": NAME, "coordinate": POSE}}]}
```