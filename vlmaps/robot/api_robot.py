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

	def __init__(self, config: DictConfig):
		super().__init__(config)
		self.cs = self.config["params"]["cs"]
		self.names = []
		self.goals = []
		self.nav = Navigator()

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
			robot_pose[:2], pos, vis=True
		)  # take (row, col) in full map

		self.goals.append(goal)
		self.set_curr_pose(goal)

	def turn(self, angle_deg: float):
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
		self.names.append(name)
		super().move_forward(name)

	# TODO: get transformation programmatically
	def transform_ros_pose_to_vlmaps_pose(self, ros_pose):
		x, y, z, qx, qy, qz, qw = ros_pose
		r = R.from_quat([qx, qy, qz, qw])
		_, _, yaw = r.as_euler('xyz', degrees=True)
		return [(x + 3.194) / self.cs, (y + 3.943) / self.cs, yaw]

	def transform_vlmaps_pose_to_ros_pose(self, vlmaps_pose):
	    x, y, yaw = vlmaps_pose
	    rotation = R.from_euler('z', yaw, degrees=True)
	    quaternion = rotation.as_quat()
	    qx, qy, qz, qw = quaternion
	    return [x * self.cs - 3.194, y * self.cs - 3.943, 0, qx, qy, qz, qw]


@hydra.main(
	version_base=None,
	config_path="../../config",
	config_name="map_indexing_cfg.yaml",
)

def main(config: DictConfig) -> None:
	data_dir = Path(config.data_paths.vlmaps_data_dir)
	data_dirs = sorted([x for x in data_dir.iterdir() if x.is_dir()])
	robot = ApiRobot(config)
	robot.setup_scene(data_dirs[config.scene_id])

	robot.map._init_clip()
	robot.map.init_categories(mp3dcat[1:-1])
	   
	robot.set_curr_pose((276.3, 79.96, 25))
	# robot.move_to_object('chair')
	robot.move_to_object('white_chair_next_to_the_couch')
	robot.move_to_object('kitchen_counter')
	# robot.with_object_on_left('couch')

	print(robot.get_formatted_goals())


if __name__ == "__main__":
	main()