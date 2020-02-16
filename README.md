# MRCDjangoBackend
A Django backend for tensorflow implementation of Google's [QANet](https://openreview.net/pdf?id=B14TlG-RW), being used with the [MRC mobile application] (https://github.com/bunny98/MRC-Android-Application)

## Dataset
The dataset used for this task is [Stanford Question Answering Dataset](https://rajpurkar.github.io/SQuAD-explorer/).
Pretrained [GloVe embeddings](https://nlp.stanford.edu/projects/glove/) obtained from common crawl with 840B tokens used for words.

## Requirements
  * Python3.6
  * NumPy
  * tqdm
  * TensorFlow=1.15
  * spacy==2.0.9
  * Django
  * Djangorestframework

## Usage
To download and preprocess the data, run

```bash
# download SQuAD and Glove
sh download.sh
# preprocess the data
python config.py --mode prepro
```
To debug/train/test
```bash
python config.py --mode debug/train/test
```

To evaluate the model with the official code, run
```bash
python evaluate-v1.1.py ~/data/squad/dev-v1.1.json train/{model_name}/answer/answer.json
```

The default directory for the tensorboard log file is `train/{model_name}/event`

### Pretrained Model
Pretrained model weights can be downloaded from the below link
```bash
https://drive.google.com/open?id=1mS-981dpppGzfTHgQ1HmlgcBCOD9llqk
```

### Demo Server
To start the django server, run
```bash
python manage.py runsever
```
Note: Information regarding various APIs can be found in mainApp/urls.py

## Detailed Implementaion

  * The model adopts character level convolution - max pooling - highway network for input representations similar to [this paper by Yoon Kim](https://arxiv.org/pdf/1508.06615.pdf).
  * The encoder consists of positional encoding - depthwise separable convolution - self attention - feed forward structure with layer norm in between.
  * Despite the original paper using 200, we observe that using a smaller character dimension leads to better generalization.
  * For regularization, a dropout of 0.1 is used every 2 sub-layers and 2 blocks.
  * Stochastic depth dropout is used to drop the residual connection with respect to increasing depth of the network as this model heavily relies on residual connections.
  * Query-to-Context attention is used along with Context-to-Query attention, which seems to improve the performance more than what the paper reported. This may be due to the lack of diversity in self attention due to 1 head (as opposed to 8 heads) which may have repetitive information that the query-to-context attention contains.
  * Learning rate increases from 0.0 to 0.001 in the first 1000 steps in inverse exponential scale and fixed to 0.001 from 1000 steps.
  * At inference, this model uses shadow variables maintained by the exponential moving average of all global variables.
  * This model uses a training / testing / preprocessing pipeline from [R-Net](https://github.com/HKUST-KnowComp/R-Net) for improved efficiency.

## TODO's
- [x] Training and testing the model
- [x] Add trilinear function to Context-to-Query attention
- [x] Apply dropouts + stochastic depth dropout
- [x] Query-to-context attention
- [x] Realtime Demo
- [ ] Data augmentation by paraphrasing
- [ ] Train with full hyperparameters (Augmented data, 8 heads, hidden units = 128)

## Tensorboard
Run tensorboard for visualisation.
```shell
$ tensorboard --logdir=./
```
