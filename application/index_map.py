from pathlib import Path
import hydra
from omegaconf import DictConfig
from vlmaps.map.vlmap import VLMap
from vlmaps.utils.matterport3d_categories import mp3dcat
from vlmaps.utils.visualize_utils import (
    pool_3d_label_to_2d,
    pool_3d_rgb_to_2d,
    visualize_rgb_map_3d,
    visualize_masked_map_2d,
    visualize_heatmap_2d,
    visualize_heatmap_3d,
    visualize_masked_map_3d,
    get_heatmap_from_mask_2d,
    get_heatmap_from_mask_3d,
    pool_3d_heatmap_to_2d
)

import numpy as np


@hydra.main(
    version_base=None,
    config_path="../config",
    config_name="map_indexing_cfg.yaml",
)
def main(config: DictConfig) -> None:
    data_dir = Path(config.data_paths.vlmaps_data_dir)
    data_dirs = sorted([x for x in data_dir.iterdir() if x.is_dir()])
    print(data_dirs[config.scene_id])
    vlmap = VLMap(config.map_config, data_dir=data_dirs[config.scene_id])
    vlmap.load_map(data_dirs[config.scene_id])
    # visualize_rgb_map_3d(vlmap.grid_pos, vlmap.grid_rgb)
    # cat = input("What is your interested category in this scene?")
    cat = "monitor on the table"

    vlmap._init_clip()
    
    # print("considering categories: ")
    # print(mp3dcat[1:-1])
    # if config.init_categories:
    #     vlmap.init_categories(mp3dcat[1:-1])
    #     mask = vlmap.index_map(cat, with_init_cat=True)
    # else:
    #     mask = vlmap.index_map(cat, with_init_cat=False)

    # if config.index_2d:
    #     mask_2d = pool_3d_label_to_2d(mask, vlmap.grid_pos, config.params.gs)
    #     rgb_2d = pool_3d_rgb_to_2d(vlmap.grid_rgb, vlmap.grid_pos, config.params.gs)
    #     visualize_masked_map_2d(rgb_2d, mask_2d)
    #     heatmap = get_heatmap_from_mask_2d(mask_2d, cell_size=config.params.cs, decay_rate=config.decay_rate)
    #     visualize_heatmap_2d(rgb_2d, heatmap)
    # else:
    #     visualize_masked_map_3d(vlmap.grid_pos, mask, vlmap.grid_rgb)
    #     heatmap = get_heatmap_from_mask_3d(
    #         vlmap.grid_pos, mask, cell_size=config.params.cs, decay_rate=config.decay_rate
    #     )
    #     visualize_heatmap_3d(vlmap.grid_pos, heatmap, vlmap.grid_rgb)

    vlmap.init_categories([cat])

    max_ids = np.argmax(vlmap.scores_mat, axis=1)
    mask = max_ids == 0
    
    cat_sim = vlmap.scores_mat[:, 0]
    cat_sim[~mask] = 0
    cat_sim = np.nan_to_num(cat_sim, nan=0)

    normalized_cat_sim = (cat_sim - np.min(cat_sim)) / (np.max(cat_sim) - np.min(cat_sim))
    normalized_cat_sim[normalized_cat_sim < 0.95] = 0

    non_zero_indices = np.where(normalized_cat_sim > 0)[0]

    result_array = normalized_cat_sim.copy()

    for index in non_zero_indices:
        start = max(index - 10, 0)
        end = min(index + 10 + 1, len(result_array))
        result_array[start:end] = 1

    rgb_2d = pool_3d_rgb_to_2d(vlmap.grid_rgb, vlmap.grid_pos, config.params.gs)
    heat_2d = pool_3d_heatmap_to_2d(result_array, vlmap.grid_pos, config.params.gs)
    visualize_heatmap_2d(rgb_2d, heat_2d)

if __name__ == "__main__":
    main()
