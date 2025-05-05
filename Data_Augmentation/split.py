#!/usr/bin/env python3
import os
import shutil
import argparse
from sklearn.model_selection import train_test_split
from collections import Counter

def parse_args():
    p = argparse.ArgumentParser(
        description="Stratified train/val/test split of a folder-based dataset."
    )
    p.add_argument(
        "--root_dir", "-i", required=True,
        help="Path to input data. Should contain one subdirectory per class."
    )
    p.add_argument(
        "--output_dir", "-o", required=True,
        help="Where to write the splits. Creates train/, val/, test/ under this."
    )
    p.add_argument(
        "--train_ratio", type=float, default=0.8,
        help="Fraction for the training set (default: 0.8)"
    )
    p.add_argument(
        "--val_ratio", type=float, default=0.1,
        help="Fraction for the validation set (default: 0.1)"
    )
    p.add_argument(
        "--test_ratio", type=float, default=0.1,
        help="Fraction for the test set (default: 0.1)"
    )
    p.add_argument(
        "--exts", nargs="+",
        default=[".jpg", ".jpeg", ".png", ".bmp"],
        help="Allowed image extensions (default: common ones)"
    )
    p.add_argument(
        "--random_state", type=int, default=42,
        help="Random seed (default: 42)"
    )
    return p.parse_args()

def gather_files(root_dir, exts):
    filepaths, labels = [], []
    for cls in os.listdir(root_dir):
        cls_dir = os.path.join(root_dir, cls)
        if not os.path.isdir(cls_dir):
            continue
        for fname in os.listdir(cls_dir):
            if os.path.splitext(fname.lower())[1] in exts:
                filepaths.append(os.path.join(cls_dir, fname))
                labels.append(cls)
    return filepaths, labels

def stratified_split(filepaths, labels, train_ratio, val_ratio, test_ratio, rnd):
    # First split: train vs temp
    train_files, temp_files, train_labels, temp_labels = train_test_split(
        filepaths, labels,
        train_size=train_ratio,
        stratify=labels,
        random_state=rnd
    )
    # Then split temp into val and test
    temp_ratio = val_ratio + test_ratio
    val_frac_of_temp = val_ratio / temp_ratio
    val_files, test_files, val_labels, test_labels = train_test_split(
        temp_files, temp_labels,
        train_size=val_frac_of_temp,
        stratify=temp_labels,
        random_state=rnd
    )
    return (train_files, train_labels), (val_files, val_labels), (test_files, test_labels)

def copy_split(split, output_dir, split_name):
    files, labels = split
    for fp, cls in zip(files, labels):
        dst_dir = os.path.join(output_dir, split_name, cls)
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy(fp, os.path.join(dst_dir, os.path.basename(fp)))

def main():
    args = parse_args()
    # sanity check ratios
    total = args.train_ratio + args.val_ratio + args.test_ratio
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"train+val+test ratios must sum to 1.0 (got {total})")
    # gather
    filepaths, labels = gather_files(args.root_dir, args.exts)
    if not filepaths:
        raise RuntimeError("No files found. Check your --root_dir and --exts.")
    # split
    train, val, test = stratified_split(
        filepaths, labels,
        args.train_ratio, args.val_ratio, args.test_ratio,
        args.random_state
    )
    # optional: print class counts
    for name, split in zip(["train", "val", "test"], [train, val, test]):
        cnt = Counter(split[1])
        print(f"{name}:", {cls: cnt[cls] for cls in sorted(cnt)})
    # copy
    for name, split in zip(["train", "val", "test"], [train, val, test]):
        copy_split(split, args.output_dir, name)
    print(f"\nDone! Splits written to `{args.output_dir}`")

if __name__ == "__main__":
    main()
    