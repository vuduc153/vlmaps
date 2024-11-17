from vlmaps.robot.lang_robot import LangRobot
from vlmaps.navigator.navigator import Navigator
from vlmaps.map.map import Map
from vlmaps.utils.matterport3d_categories import mp3dcat
from omegaconf import DictConfig
from typing import List, Tuple, Dict, Any, Union
import hydra
from pathlib import Path
import cv2
import numpy as np 
from scipy.spatial.transform import Rotation as R
from math import radians
import json


class ApiRobot(LangRobot):

	def __init__(self, config: DictConfig, vis):
		super().__init__(config)
		# update these values based on the transformation between coordinates in ROS map frame and vlmaps
		self.offset_x = 1.865
		self.offset_y = 2.837
		self.cs = self.config["params"]["cs"]
		self.names = []
		self.goals = []
		self.nav = Navigator()
		self.vis = vis

	def setup_scene(self, vlmaps_data_dir: str):
	    self.load_scene_map(vlmaps_data_dir, self.config["map_config"])

	    cropped_obst_map = self.map.get_obstacle_cropped()

	    cropped_obst_map = Map._dilate_map(cropped_obst_map == 0, 3, 1)
	    cropped_obst_map = cropped_obst_map == 0

	    self.nav.build_visgraph(
	        cropped_obst_map,
	        self.map.rmin,
	        self.map.cmin,
	        vis=False,
	    )

	def set_curr_pose(self, pose):
		self.curr_pos_on_map = (pose[0], pose[1])
		self.curr_ang_deg_on_map = pose[2]

	def _set_nav_curr_pose(self):
		# current pose is always immediately updated after move_to & turn 
		pass

	def execute_actions(self, actions_list: List[Any]):
		pass

	def move_to(self, pos: Tuple[float, float]):
		robot_pose = self.get_agent_pose_on_map()  # (row, col, angle_deg) on full map

		goal = self.nav.go_to(
			robot_pose[:2], pos, vis=self.vis
		)  # take (row, col) in full map

		if goal[0] != self.curr_pos_on_map[0] or goal[1] != self.curr_pos_on_map[1]:
			self.goals.append(goal)
		else:
			print("stay in place")
			self.names.pop()
		
		self.set_curr_pose(goal)

	def turn(self, angle_deg: float):
		if angle_deg == 0:
			print("stay in place")
			self.names.pop()
			return

		self.curr_ang_deg_on_map += angle_deg

		if self.curr_ang_deg_on_map < 0:
			self.curr_ang_deg_on_map += 360
		if self.curr_ang_deg_on_map > 360:
			self.curr_ang_deg_on_map -= 360

		robot_pose = self.get_agent_pose_on_map()  # (row, col, angle_deg) on full map

		self.goals.append(robot_pose)

	def get_formatted_goals(self):
		poses = []

		for goal in self.goals:
			poses.append(self.transform_vlmaps_pose_to_ros_pose(goal))

		data = {'movements': [{"actor": "A", "target": {"label": name, "coordinate": pose, "additional_detail": ""}} for (pose, name) in zip(poses, self.names)]}

		self.goals = []
		self.names = []

		return data

	# Override
	def with_object_on_left(self, name: str):
		self.names.append(name)
		super().with_object_on_left(name)

	def with_object_on_right(self, name: str):
		self.names.append(name)
		super().with_object_on_right(name)

	def move_to_left(self, name: str):
		self.names.append(name)
		super().move_to_left(name)

	def move_to_right(self, name: str):
		self.names.append(name)
		super().move_to_right(name)

	def move_north(self, name: str):
		self.names.append(name)
		super().move_north(name)

	def move_south(self, name: str):
		self.names.append(name)
		super().move_south(name)

	def move_west(self, name: str):
		self.names.append(name)
		super().move_west(name)

	def move_east(self, name: str):
		self.names.append(name)
		super().move_east(name)

	def move_to_object(self, name: str):
		self.names.append(name)
		super().move_to_object(name)

	def move_forward(self, meters: float):
		self.names.append(f"move {meters} meters")
		super().move_forward(meters)

	def turn_absolute(self, angle_deg: float):
		self.names.append(f"turn to {angle_deg} degree")
		super().turn_absolute(angle_deg)

	def face(self, name: str):
		self.names.append(name)
		super().face(name)

	def transform_ros_pose_to_vlmaps_pose(self, ros_pose):
		x, y, z, qx, qy, qz, qw = ros_pose
		r = R.from_quat([qx, qy, qz, qw])
		_, _, yaw = r.as_euler('xyz', degrees=True)
		return [(x + self.offset_x) / self.cs, (y + self.offset_y) / self.cs, yaw]

	def transform_vlmaps_pose_to_ros_pose(self, vlmaps_pose):
	    x, y, yaw = vlmaps_pose
	    rotation = R.from_euler('z', yaw, degrees=True)
	    quaternion = rotation.as_quat()
	    qx, qy, qz, qw = quaternion
	    return [x * self.cs - self.offset_x, y * self.cs - self.offset_y, 0, qx, qy, qz, qw]


@hydra.main(
	version_base=None,
	config_path="../../config",
	config_name="map_indexing_cfg.yaml",
)

def main(config: DictConfig) -> None:
	data_dir = Path(config.data_paths.vlmaps_data_dir)
	data_dirs = sorted([x for x in data_dir.iterdir() if x.is_dir()])
	robot = ApiRobot(config, vis=True)
	robot.setup_scene(data_dirs[config.scene_id])

	robot.map._init_clip()
	robot.map.init_categories(mp3dcat[1:-1])

	robot.set_curr_pose((294.254, 123.128, 25))
	robot.move_to_object('laptop next to the white robot')
	robot.move_to_object('couch')
	robot.move_to_object('counter')
	robot.move_to_object('white board')

	print(robot.get_formatted_goals())


if __name__ == "__main__":
	main()