import json
import time
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Running Step: COMBINE")
    
    all_processed_data = []
    
    # Artifacts 会被下载到以它们名字命名的子目录中
    # 我们的 artifact 名字是 processed-chunk-1, processed-chunk-2, ...
    artifact_dirs = list(Path(".").glob("processed-chunk-*"))
    if not artifact_dirs:
        raise FileNotFoundError("No processed chunk directories found! Did the process jobs fail?")
        
    logging.info(f"Found {len(artifact_dirs)} artifact directories.")

    for part_dir in sorted(artifact_dirs, key=lambda p: int(p.name.split('-')[-1])):
        chunk_num = part_dir.name.split('-')[-1]
        json_file = part_dir / f"takeout-part-{chunk_num}.json"
        
        if json_file.exists():
            logging.info(f"Loading data from {json_file}")
            with open(json_file, "r", encoding="u8") as f:
                data = json.load(f)
                all_processed_data.extend(data)
        else:
            logging.warning(f"Warning: {json_file} not found in artifact directory.")

    logging.info(f"Total items combined: {len(all_processed_data)}")

    # 从 base-data artifact 中加载 user 信息
    user_file = Path("base-data/user.json")
    if not user_file.exists():
        raise FileNotFoundError("user.json not found in base-data directory!")
        
    with open(user_file, "r", encoding="u8") as f:
        user_meta = json.load(f)

    if 'id' not in user_meta and 'username' in user_meta:
        logging.warning("User object from API is missing 'id'. Using 'username' as a fallback for 'id'.")
        user_meta['id'] = user_meta['username']
    
    # 构建最终的 takeout.json 结构
    final_takeout = {
        "meta": {
            "generated_at": time.time(),
            "user": user_meta
        },
        "data": all_processed_data
    }

    with open("takeout.json", "w", encoding="u8") as f:
        json.dump(final_takeout, f, ensure_ascii=False, indent=4)

    logging.info("Successfully combined all parts into takeout.json.")
    logging.info("Step COMBINE finished.")

if __name__ == "__main__":
    main()
