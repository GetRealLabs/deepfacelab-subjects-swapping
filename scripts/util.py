from pathlib import Path
from typing import List
from tqdm import tqdm
from scripts.Subject import Subject


def cp_aligned_frames(subjects: List[Subject], dst_dir: Path) -> None:
    import shutil
    hard_clean_dir(dst_dir)
    for subject in tqdm(subjects, total=len(subjects), desc="copying subject's aligned frames", unit="subject", miniters=1.0):
        
        # Debug Information
        print(f"Processing subject with ID: {subject.id()}")
        print(f"Root directory of subject: {subject.root_dir().name}")
        try:
            aligned_frames_list = list(subject.aligned_frames().glob('*'))
            print(f"Number of aligned frames for the subject: {len(aligned_frames_list)}")
        except AttributeError as e:
            print(f"Error: {e}")
            continue

        for src_file in aligned_frames_list:
            tmp = dst_dir / f"{subject.root_dir().name}_{subject.id()}_{src_file.stem}{src_file.suffix}"
            shutil.copy(src_file, tmp)


def hard_clean_dir(dst_dir: Path) -> None:
    import shutil
    if dst_dir.exists():
        shutil.rmtree(dst_dir)
    dst_dir.mkdir(exist_ok=True)


def smooth_clean_dir(dst_dir: Path, pak_ok: bool = False) -> None:
    for img in dst_dir.glob('*'):
        if (pak_ok and img.suffix == ".pak") or not img.exists():
            continue
        img.unlink()
