import numpy as np
import os
import cv2
from PIL import Image


def merge_image(path_image, path_seg, ratio=0.5, color=(0, 255, 0)):
    with open(path_image) as fi:
        image = np.array(Image.open(fi)).astype(np.float32)
    with open(path_seg) as fs:
        seg = np.array(Image.open(fs)).astype(np.float32)
    color = np.array(color, dtype=np.float32)
    print('open image {} and segmentatino {}'.format(path_image, path_seg))
    print('image size:', image.shape)
    print('seg size:', seg.shape)
    cover = np.where(seg > 0)
    image[cover] = image[cover] * ratio + (1 - ratio) * color
    return image.astype(np.uint8)


def merge_images(image_dir, seg_dir, result_dir):
    list_dir = os.listdir(seg_dir)
    while len(list_dir) > 0:
        dir = list_dir.pop(0)
        image_paths = os.path.join(image_dir, dir)
        seg_paths = os.path.join(seg_dir, dir)
        result_paths = os.path.join(result_dir, dir)
        if not os.path.isdir(result_paths):
            os.makedirs(result_paths)
        list_image = os.listdir(image_paths)
        for image_id in range(len(list_image)):
            image_path = os.path.join(image_paths, '{:05}.jpg'.format(image_id))
            seg_path = os.path.join(seg_paths, '{:05}.png'.format(image_id))
            result = merge_image(image_path, seg_path)
            result_path = os.path.join(result_paths, '{:05}.jpg'.format(image_id))
            result_image = Image.fromarray(result)
            result_image.save(result_path)


def vis_video(result_dir):
    list_dir = os.listdir(result_dir)
    while len(list_dir) > 0:
        dir = list_dir.pop(0)
        image_paths = os.path.join(result_dir, dir)
        list_image = os.listdir(image_paths)
        video_path = os.path.join(image_paths, dir + '.avi')
        images = []
        for image_id in range(len(list_image)):
            with open(os.path.join(image_paths, '{:05}.jpg'.format(image_id)), 'rb') as fi:
                image = np.array(Image.open(fi)).astype(np.uint8)
            images.append(image)
        h = images[0].shape[0]
        w = images[0].shape[1]
        video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc('M','J','P','G'), 25, (w, h), True)
        for image in images:
            video.write(image[..., ::-1])
        video.release()
        print('succeed to generate video', video_path)


image_dir = '/home/linguangchen/codes/vos/research/feelvos/datasets/davis17/DAVIS/JPEGImages/480p'
seg_dir = '/home/linguangchen/codes/vos/research/feelvos/datasets/davis17/exp_davis_only\
/eval_on_val_set/eval/segmentation'
result_dir = '/home/linguangchen/vis_feelvos'
merge_images(image_dir, seg_dir, result_dir)
vis_video(result_dir)

