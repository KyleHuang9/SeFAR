# *SeFAR*: Semi-supervised Fine-grained Action Recognition with Temporal Perturbation and Learning Stabilization (*AAAI'25*🔥)
[Yongle Huang](https://github.com/KyleHuang9)<sup>😎</sup>, [Haodong Chen](https://haroldchen19.github.io/)<sup>😎</sup>, Zhenbang Xu, Zihan Jia, Haozhou Sun, [Dian Shao](https://scholar.google.com/citations?hl=en&user=amxDSLoAAAAJ&view_op=list_works&sortby=pubdate)<sup>🤩</sup>

<sup>😎</sup>Equal Contribution, <sup>🤩</sup>Corresponding Author

<p align="center">
  <a href='https://arxiv.org/abs/2405.07472'>
  <img src='https://img.shields.io/badge/Arxiv-2405.07472-A42C25?style=flat&logo=arXiv&logoColor=A42C25'></a> 
</p>

## Abstract

> Human action understanding is crucial for the advancement of multimodal systems. While recent developments, driven by powerful large language models (LLMs), aim to be *general* enough to cover a wide range of categories, they often overlook the need for more *specific* capabilities. In this work, we address the more challenging task of Fine-grained Action Recognition (FAR), which focuses on detailed semantic labels within shorter temporal duration (*e.g.*, "salto backward tucked with 1 turn"). Given the high costs of annotating fine-grained labels and the substantial data needed for fine-tuning LLMs, we propose to adopt semi-supervised learning (SSL). Our framework, **SeFAR**, incorporates several innovative designs to tackle these challenges. Specifically, to capture sufficient visual details, we construct *Dual-level temporal elements* as more effective representations, based on which we design a new strong augmentation strategy for the Teacher-Student learning paradigm through involving *moderate temporal perturbation*. Furthermore, to handle the high uncertainty within the teacher model's predictions for FAR, we propose the *Adaptive Regulation* to stabilize the learning process. Experiments show that SeFAR achieves state-of-the-art performance on two FAR datasets, FineGym and FineDiving, across various data scopes. It also outperforms other semi-supervised methods on two classical coarse-grained datasets, UCF101 and HMDB51. Further analysis and ablation studies validate the effectiveness of our designs. Additionally, we show that the features extracted by our SeFAR could largely promote the ability of multimodal foundation models to understand fine-grained and domain-specific semantics.

## Installation

First, create a new conda environment and activate it:

```bash
conda create -n sefar python=3.7
conda activate sefar
```

Then, install the runtime environment by running:

~~~
bash env.sh
~~~



## Usage

## Data Preparation

Our data is organized in the following format:
```
<path_1> <label_1>
<path_2> <label_2>
...
<path_n> <label_n>
```
where `<path_i>` points to a video file, and `<label_i>` is an integer between `0` and `num_classes - 1`.

We provide examples in `./dataset`.

__Note:__ We only provide examples of videos lists from Finegym and Finediving. Due to copyright constraints, we are unable to directly disclose the video data we utilize.

## Pretrained Model

We utilize a pre-trained model of [TimeSformer](https://github.com/facebookresearch/TimeSformer), which can be downloaded [here](https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-vitjx/jx_vit_base_p16_224-80ecf9dd.pth).

## Training

You can train on Finegym99 5% by running:

```
bash train.sh
```

If you want to train on more datasets, please modify the parameters in `train.sh` and `./configs/TimeSformer_base_ssl.yaml`



## Main Results in paper 

This is an original-implementation for open-source use.
In the following table we report the accuracy in original paper.

Results of elements across all events:

| Method | Gym99-5% | Gym99-10% | FineDiving-5% | FineDiving-10% |
| ------ | -------- | --------- | ------------- | -------------- |
| SeFAR  | 35.7     | 28.0      | 71.5          | 78.0           |

Results of elements within an event:

| Method | UB-10% | FX-10% | 10m-10% | 10m-20% |
| ------ | ------ | ------ | ------- | ------- |
| SeFAR  | 56.3   | 22.2   | 84.3    | 95.3    |

Results of elements within a set:

| Method | UB-S1-10% | FX-S1-10% | 5253B-10% | 5253B-20% |
| ------ | --------- | --------- | --------- | --------- |
| SeFAR  | 37.8      | 20.0      | 97.8      | 97.0      |

Results on coarse-grained datasets:

| Method | UCF-1% | UCF-5% | UCF-10% | HMDB-40% | HMDB-50% |
| ------ | ------ | ------ | ------- | -------- | -------- |
| SeFAR  | 47.3   | 72.4   | 87.1    | 63.4     | 67.0     |

## Citation
Please consider citing our paper if our code and dataset annotations are useful:
```bib
coming soon~
```



## Acknowledgements

SeFAR is built on top of [TimeSformer](https://github.com/facebookresearch/TimeSformer)and [SVFormer](https://github.com/ChenHsing/SVFormer.git). Thanks for their awesome work!

