from pathlib import Path
import hydra
from omegaconf import DictConfig
import cv2
import numpy as np
import os
import re


def format_data(data_dir):
	rgb_dir = data_dir / 'rgb'
	depth_dir = data_dir / 'depth'
	pose_path = data_dir / 'poses.txt'

	depth_png_to_npy(depth_dir)

	for frame_dir in [rgb_dir, depth_dir]:
		filter_frames(frame_dir, pose_path)
		format_filenames(frame_dir)

	format_poses(pose_path)


def depth_png_to_npy(data_dir):
	print("Converting depth images...")

	png_files = [f for f in os.listdir(data_dir) if f.endswith('.png')]

	for png_file in png_files:
		img_path = os.path.join(data_dir, png_file)
		img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

		if img.dtype == np.uint16:
			depth_array = np.array(img, dtype=np.float32)
			depth_array /= 1000.0
		else:
			print(f"Skipping {png_file} as it's not in CV_16UC1 format.")
			continue

		npy_file = os.path.splitext(png_file)[0] + '.npy'
		npy_path = os.path.join(data_dir, npy_file)
		np.save(npy_path, depth_array)
		png_path = os.path.join(data_dir, png_file)
		os.remove(png_path)


def format_poses(pose_path):
	print("Formatting pose file...")

	with open(pose_path, 'r') as file:
		lines = file.readlines()

		modified_lines = []
		for line in lines:
			if line.startswith('#'):
				continue
			modified_line = ' '.join(line.split()[1:-1])
			modified_lines.append(modified_line)

	with open(pose_path, 'w') as file:
		for line in modified_lines:
			file.write(line + '\n')


def filter_frames(data_dir, pose_path):
	print(f"Filtering {data_dir} frames without poses...")

	ids = get_frame_ids(pose_path)
	for filename in os.listdir(data_dir):
		base, ext = os.path.splitext(filename)
		if base not in ids:
			file_path = os.path.join(data_dir, filename)
			os.remove(file_path)


def format_filenames(data_dir):
	print(f"Renaming {data_dir} files...")

	for filename in os.listdir(data_dir):
		match = re.match(r'^(\d+)\.(png|npy)$', filename)
		if match:
			number, extension = match.groups()
			new_number = number.zfill(6)
			new_filename = f"{new_number}.{extension}"
			old_path = os.path.join(data_dir, filename)
			new_path = os.path.join(data_dir, new_filename)
			os.rename(old_path, new_path)


def get_frame_ids(pose_path):
	ids = set()
	with open(pose_path, 'r') as file:
		for line in file:
			if line.startswith('#'):
				continue
			parts = line.split()
			id = parts[8]
			ids.add(id)
	return ids


@hydra.main(
    version_base=None,
    config_path="../config",
    config_name="map_creation_cfg.yaml",
)
def main(config: DictConfig) -> None:
    data_dir = Path(config.data_paths.vlmaps_data_dir)
    data_dirs = sorted([x for x in data_dir.iterdir() if x.is_dir()])
    format_data(data_dirs[0])
    

if __name__ == "__main__":
    main()