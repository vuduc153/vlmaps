from vlmaps.robot.lang_robot import LangRobot
from vlmaps.navigator.navigator import Navigator
from vlmaps.utils.matterport3d_categories import mp3dcat
from omegaconf import DictConfig
from typing import List, Tuple, Dict, Any, Union
import hydra
from pathlib import Path
import cv2
import numpy as np 
from scipy.spatial.transform import Rotation
from math import radians
import json


class ApiRobot(LangRobot):

	def __init__(self, config: DictConfig):
		super().__init__(config)
		self.cs = self.config["params"]["cs"]
		self.goals = []
		self.nav = Navigator()

	def setup_scene(self, vlmaps_data_dir: str):
	    self.load_scene_map(vlmaps_data_dir, self.config["map_config"])

	    cropped_obst_map = self.map.get_obstacle_cropped()

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
			robot_pose[:2], pos, vis=False
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
		coordinates = []

		for goal in self.goals:
			rotation = Rotation.from_euler('xyz', [0, 0, goal[2]])
			quaternion = rotation.as_quat()
			qx, qy, qz, qw = quaternion
			coordinates.append([goal[0]*self.cs, goal[1]*self.cs, 0, qx, qy, qz, qw])

		data = {
			'movements': [
				{"actor": "A", "target": {"label": "", "coordinate": coordinate, "additional_detail": ""}} for coordinate in coordinates
			]
		}

		return json.dumps(data)


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
	   
	robot.set_curr_pose((284, 94, 0))
	robot.move_to_object('mirror')

	robot.move_to_object('tv_monitor')
	robot.with_object_on_left('table')

	print(robot.get_formatted_goals())


if __name__ == "__main__":
	main()