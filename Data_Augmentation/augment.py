#!/usr/bin/env python3
"""
augment.py: Perform data augmentation on 68×68 grayscale malware traffic images,
balancing classes via noise, occlusion, temporal shift, random crop, MixUp, and CutMix.

Usage:
    pip install -U albumentations numpy opencv-python-headless torch torchvision

    python augment.py \
      --input_dir ImageDataset \
      --output_dir data/augmented \
      --num_augments 1
"""

import os
import argparse
import random
import cv2
import numpy as np

# Albumentations v1.x imports
import albumentations as A
from torch.utils.data import Dataset, DataLoader

def mixup(image1, label1, image2, label2, alpha=1.0):
    lam = np.random.beta(alpha, alpha)
    mixed = (lam * image1 + (1 - lam) * image2).astype(np.uint8)
    return mixed, (label1, label2, lam)

def cutmix(image1, label1, image2, label2):
    h, w = image1.shape
    cx, cy = np.random.randint(w), np.random.randint(h)
    bw, bh = int(w * np.random.rand()), int(h * np.random.rand())
    x1 = np.clip(cx - bw // 2, 0, w)
    y1 = np.clip(cy - bh // 2, 0, h)
    x2 = np.clip(cx + bw // 2, 0, w)
    y2 = np.clip(cy + bh // 2, 0, h)

    new = image1.copy()
    new[y1:y2, x1:x2] = image2[y1:y2, x1:x2]
    lam = 1 - ((x2 - x1) * (y2 - y1) / float(w * h))
    return new, (label1, label2, lam)

class MalwareDataset(Dataset):
    """Load 68×68 grayscale images organized by class subdirectories."""
    def __init__(self, root_dir):
        self.samples = []
        self.classes = sorted(
            d for d in os.listdir(root_dir)
            if os.path.isdir(os.path.join(root_dir, d))
        )
        self.class_to_idx = {c: i for i, c in enumerate(self.classes)}
        for cls in self.classes:
            cls_path = os.path.join(root_dir, cls)
            for fname in os.listdir(cls_path):
                if fname.lower().endswith('.png'):
                    self.samples.append(
                        (os.path.join(cls_path, fname), self.class_to_idx[cls])
                    )

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        return img, label, path

# ---------------------------------------------------------------------------- #
#                     Albumentations v1.x augmentation pipeline               #
# ---------------------------------------------------------------------------- #
base_transform = A.Compose([
    A.GaussNoise(var_limit=(10.0, 50.0), p=0.5),
    A.ShiftScaleRotate(
        shift_limit=0.1, scale_limit=0.1, rotate_limit=15, p=0.5
    ),
    A.CoarseDropout(max_holes=1, max_height=16, max_width=16, p=0.5),
    A.RandomCrop(height=64, width=64, p=0.5),
])

def save_augmented(img: np.ndarray, out_path: str):
    """Write the augmented image to disk."""
    cv2.imwrite(out_path, img)

def main(args):
    ds = MalwareDataset(args.input_dir)
    dl = DataLoader(ds, batch_size=1, shuffle=True, num_workers=4, pin_memory=True)

    # Prepare output dirs
    os.makedirs(args.output_dir, exist_ok=True)
    for cls in ds.classes:
        os.makedirs(os.path.join(args.output_dir, cls), exist_ok=True)

    # Count originals per class to know how many to generate
    counts = {
        cls: len(os.listdir(os.path.join(args.input_dir, cls)))
        for cls in ds.classes
    }
    max_count = max(counts.values())

    for img_batch, label_batch, path_batch in dl:
        # unwrap batch
        img = img_batch.numpy().squeeze(0).astype(np.uint8)
        label = label_batch.item()
        path = path_batch[0]
        cls = ds.classes[label]
        base_name = os.path.splitext(os.path.basename(path))[0]

        # how many to generate for this sample
        to_gen = max_count - counts[cls]
        for i in range(min(to_gen, args.num_augments)):
            aug = base_transform(image=img)['image']

            # # half the time apply mixup/cutmix
            # if random.random() < 0.5:
            #     idx2 = random.randrange(len(ds))
            #     img2, lbl2, _ = ds[idx2]
            #     if random.random() < 0.5:
            #         aug, _ = mixup(aug, label, img2, lbl2)
            #     else:
            #         aug, _ = cutmix(aug, label, img2, lbl2)

            out_fname = f"{base_name}_aug_{i}.png"
            out_path = os.path.join(args.output_dir, cls, out_fname)
            save_augmented(aug, out_path)

        # update count so that subsequent samples see the new total
        counts[cls] += to_gen

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Augment malware images to balance classes'
    )
    parser.add_argument(
        '--input_dir', type=str, required=True,
        help='Root folder (e.g., ImageDataset) containing class subdirs'
    )
    parser.add_argument(
        '--output_dir', type=str, required=True,
        help='Where to write augmented images (preserves class subdirs)'
    )
    parser.add_argument(
        '--num_augments', type=int, default=50,
        help='Max augments per original sample'
    )
    args = parser.parse_args()
    main(args)
