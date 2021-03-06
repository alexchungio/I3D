#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------
# @ File       : split_dataset.py
# @ Description:  
# @ Author     : Alex Chung
# @ Contact    : yonganzhong@outlook.com
# @ License    : Copyright (c) 2017-2018
# @ Time       : 2020/4/27 下午3:36
# @ Software   : PyCharm
#-------------------------------------------------------

import os
import pathlib
import shutil

original_dataset_dir = '/home/alex/Documents/dataset/video_binary'
original_dataset_dir = pathlib.Path(original_dataset_dir)

# source dataset
dataset_dir = pathlib.Path(original_dataset_dir / 'bike_raft')
# split_dataset
split_dir = pathlib.Path(original_dataset_dir / 'bike_raft_split')


def train_val_split(src_img_dir, dst_img_dir, split_ratio=0.8, is_balance=False, type='avi'):
    """

    :param img_source_dir:
    :param split_dst_dir:
    :param split_ratio:
    :param is_balance:
    :return:
    """
    # check parameter attribute
    if isinstance(src_img_dir, str) is  False:
        raise AttributeError("{0} must be a string".format(src_img_dir))
    if isinstance(dst_img_dir, str) is  False:
        raise AttributeError("{0} must be a string".format(dst_img_dir))
    if isinstance(split_ratio, float) is False:
        raise AttributeError("{0} must be a float".format(split_ratio))
    if isinstance(is_balance, bool) is False:
        raise AttributeError("{0} must be a boolean".format(is_balance))
    if type not in ['avi', 'mp4']:
        raise AttributeError("{0} must be belong to avi or mp4".format(type))

    src_img_dir = pathlib.Path(src_img_dir)
    if src_img_dir.exists() is False:
        raise OSError("{0} does not exist".format(src_img_dir))

    # create dir
    dst_img_dir = pathlib.Path(dst_img_dir)
    train_dir = pathlib.Path(dst_img_dir / 'train')
    val_dir = pathlib.Path(dst_img_dir / 'val')


    # get category name
    classes_name = [file.name for file in src_img_dir.iterdir() if file.is_dir()]
    print("dataset class name: {0}".format(classes_name))

    for class_name in classes_name:

        class_dir = pathlib.Path(src_img_dir / '{0}'.format(class_name))
        class_video = list(class_dir.glob(pattern='*.{0}'.format(type)))

        # split train and validation samples
        train_img = class_video[:int(len(class_video) * split_ratio)]
        val_img = class_video[int(len(class_video) * split_ratio):]

        # create class dst directory
        train_class_dir = pathlib.Path(train_dir / '{0}'.format(class_name))
        val_class_dir = pathlib.Path(val_dir / '{0}'.format(class_name))

        if train_class_dir.exists() is False:
            train_class_dir.mkdir(parents=True)
        else:
            # use to update split dataset
            # force to remove not-null folder
            shutil.rmtree(train_class_dir, ignore_errors=True)
            train_class_dir.mkdir(parents=True)
        if val_class_dir.exists() is False:
            val_class_dir.mkdir(parents=True)
        else:
            shutil.rmtree(val_class_dir, ignore_errors=True)
            val_class_dir.mkdir(parents=True)

        # execute remove
        for img in train_img:
            img_name = img.name
            shutil.copyfile(str(img.absolute()), pathlib.Path(train_class_dir / '{0}'.format(img_name)).absolute())
        for img in val_img:
            img_name = img.name
            shutil.copyfile(str(img.absolute()), pathlib.Path(val_class_dir / '{0}'.format(img_name)).absolute())

        print("Successful split {0} class: \n {1} train samples and {2} val samples to {3}".
              format(class_name, len(train_img), len(val_img), class_dir.absolute()))

    print('Successful to split dataset')

    return True

if __name__ == "__main__":
    print(dataset_dir.absolute())
    train_val_split(str(dataset_dir), str(split_dir))