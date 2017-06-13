## 天池医疗AI大赛[第一季]：肺部结节智能诊断
## Pulmonary Nodules AI Diagnosis

### DSB3Tutorial 
> ### mask_segment folder

This code is the companion for the tutorial located at https://www.kaggle.com/c/data-science-bowl-2017#tutorial

### About this repository

This repository is not intended to be an out of the box solution for the DSB challenge. It will not run out-of-the-box
without editing. That was not it's intention. The tutorial was put together rapidly by several people working in tandem
and the code herein is a collection of the code they used to produce the tutorial found on the DSB website. 

The intent behind this tutorial was to presented a series of steps that can be followed as a starting point for competitors. 
Our hope is that this can save competitors time in framing the problem and that they can lift some of this code to speed 
up their own solution generation. We expect that the competitors efforst will supercede this tutorial in short order--which
is, of course, the point of the competition. 

Thanks for participating and helping to advance cancer diagnosis!

### TianChiMedical_AI 天池医疗AI挑战赛 
> ### preprocessing folder
  
这个工程用于托管我分享帖中涉及的代码，有部分病人的文件作为示例。

### 0. 文件说明
##### csv_files
> 存放了那几个csv文件  

##### nodule_cubes
> npy里存放的是提取出来的nodule_cubes  

##### slices_masks
> 存放的是根据annotations.csv文件生成的slices和对应的GroundTruth，可用于训练2D-Unet