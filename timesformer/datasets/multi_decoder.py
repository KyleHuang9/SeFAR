# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.

import math
import numpy as np
import random
import torch
import torchvision.io as io
import cv2
import time

def get_start_end_idx(video_size, clip_size, clip_idx, num_clips):
    """
    Sample a clip of size clip_size from a video of size video_size and
    return the indices of the first and last frame of the clip. If clip_idx is
    -1, the clip is randomly sampled, otherwise uniformly split the video to
    num_clips clips, and select the start and end index of clip_idx-th video
    clip.
    Args:
        video_size (int): number of overall frames.
        clip_size (int): size of the clip to sample from the frames.
        clip_idx (int): if clip_idx is -1, perform random jitter sampling. If
            clip_idx is larger than -1, uniformly split the video to num_clips
            clips, and select the start and end index of the clip_idx-th video
            clip.
        num_clips (int): overall number of clips to uniformly sample from the
            given video for testing.
    Returns:
        start_idx (int): the start frame index.
        end_idx (int): the end frame index.
    """
    delta = max(video_size - clip_size, 0)
    if clip_idx == -1:
        # Random temporal sampling.
        start_idx = random.uniform(0, delta)
    else:
        # Uniformly sample the clip with the given index.
        start_idx = delta * clip_idx / num_clips
    end_idx = start_idx + clip_size - 1
    return int(start_idx), int(end_idx)

# def decode(
#     video_path,
#     sampling_rate,
#     num_frames,
#     clip_idx=-1,
#     num_clips=10,
#     whole=False,
# ):
#     """
#     Decode the video and perform temporal sampling.
#     Args:
#         video_path (str): video path.
#         sampling_rate (int): frame sampling rate (interval between two sampled
#             frames).
#         num_frames (int): number of frames to sample.
#         clip_idx (int): if clip_idx is -1, perform random temporal
#             sampling. If clip_idx is larger than -1, uniformly split the
#             video to num_clips clips, and select the
#             clip_idx-th video clip.
#         num_clips (int): overall number of clips to uniformly
#             sample from the given video.
#         whole (bool): Whether sample from whole video.
#     """
#     assert clip_idx >= -1, "Not valied clip_idx {}".format(clip_idx)
#     try:
#         cap = cv2.VideoCapture(video_path)
#         if not cap.isOpened():
#             return None
#         frame_length = cap.get(7)
#         # print("frame_length: ", frame_length)
#         clip_sz = min(sampling_rate * num_frames, frame_length)
#         # print("clip_sz: ", clip_sz)
        
#         if whole:
#             # print("whole video")
#             start_pt, end_pt = 0, frame_length - 1
#             new_sampling_rate = max(int(frame_length // num_frames), 1)
#         else:
#             # print("random sampling")
#             start_pt, end_pt = get_start_end_idx(
#                 frame_length - 1,
#                 clip_sz,
#                 clip_idx,
#                 num_clips,
#             )
#             new_sampling_rate = int(clip_sz // num_frames)
#         # print("new_sampling_rate: ", new_sampling_rate)
            
#         # Get frame index.
#         index = []
#         for i in range(num_frames):
#             start = start_pt + i * new_sampling_rate
#             end = start_pt + (i + 1) * new_sampling_rate
#             select_id = random.randint(start, end - 1)
#             index.append(select_id)
        
#         # print("index: ", index)
    
#         frames = []
#         for id in index:
#             cap.set(cv2.CAP_PROP_POS_FRAMES, id)
#             ret, frame = cap.read()
#             if ret:
#                 h, w, _ = frame.shape
#                 ratio =  min(h * 1.0 / 480, w * 1.0 / 480)
#                 frame = cv2.resize(frame, (int(w / ratio), int(h / ratio)))
#                 frames.append(frame)
#             else:
#                 # print("id: ", id)
#                 # print("frame_length: ", frame_length)
#                 # print("clip_sz: ", clip_sz)
#                 # print("new_sampling_rate: ", new_sampling_rate)
#                 # print("index: ", index)
#                 # print("path: ", video_path)
#                 break
#     except Exception as e:
#         print("Failed to decode by {} with exception: {}".format("cv2", e))
#         return None

#     # print("frames: ", len(frames), "\n")
    
#     if len(frames) == num_frames:
#         output_frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in frames]
#         output_frames = torch.as_tensor(np.stack(output_frames))
#         return output_frames
#     else:
#         return None

def decode(
    video_path,
    sample_list,
):
    """
    Decode the video and perform temporal sampling.
    Args:
        video_path (str): video path.
        sampling_rate (int): frame sampling rate (interval between two sampled
            frames).
        num_frames (int): number of frames to sample.
        clip_idx (int): if clip_idx is -1, perform random temporal
            sampling. If clip_idx is larger than -1, uniformly split the
            video to num_clips clips, and select the
            clip_idx-th video clip.
        num_clips (int): overall number of clips to uniformly
            sample from the given video.
        whole (bool): Whether sample from whole video.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    frame_length = int(cap.get(7))
    
    start_pt, end_pt = 0, frame_length - 1
    
    total_frames = 0
    for nframe in sample_list:
        total_frames += nframe
    if total_frames > frame_length:
        total_frames = max(sample_list[-1], frame_length)
    
    if total_frames > frame_length:
        return None
    
    sampling_rate = frame_length / total_frames
    selected_list = [0 for _ in range(total_frames)]
    
    
    sample_clip_id = []
    for i in range(len(sample_list)):
        num_clips = sample_list[-(i + 1)]
        interval = total_frames / num_clips
        
        clip_id = []
        for j in range(total_frames):
            if j >= len(clip_id) * interval and selected_list[j] == 0:
                clip_id.append(j)
                selected_list[j] = 1
        if len(clip_id) < num_clips:
            clip_id.clear()
            for j in range(num_clips):
                t_id = random.randint(round(j * interval), round((j + 1) * interval - 1))
                clip_id.append(t_id)
        # clip_id.sort()
        sample_clip_id.append(clip_id)
    sample_clip_id.reverse()
    
        
    # Get frame index.
    selected_frames_list = []
    for i in range(len(sample_list)):
        t_frames_list = []
        for id in sample_clip_id[i]:
            start = start_pt + round(id * sampling_rate)
            end = start_pt + round((id + 1) * sampling_rate)
            if start == end:
                end += 1
            select_id = random.randint(start, end - 1)
            t_frames_list.append(select_id)
        selected_frames_list.append(t_frames_list)
    

    frames_list = []
    for i in range(len(sample_list)):
        t_frames_list = []
        for id in selected_frames_list[i]:
            cap.set(cv2.CAP_PROP_POS_FRAMES, id)
            ret, frame = cap.read()
            if ret:
                h, w, _ = frame.shape
                ratio =  min(h * 1.0 / 480, w * 1.0 / 480)
                frame = cv2.resize(frame, (int(w / ratio), int(h / ratio)))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                t_frames_list.append(frame)
            else:
                return None
            t_frames = torch.as_tensor(np.stack(t_frames_list))
        frames_list.append(t_frames)
    cap.release()
    return frames_list