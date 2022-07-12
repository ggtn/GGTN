# -*- coding: utf-8 -*-
"""
    This module is intended to join all the pipeline in separated tasks
    to be executed individually or in a flow by using command-line options

    Example:
    Dataset embedding and processing:
        $ python taskflows.py -e -pS
"""

import argparse
import gc
import shutil
from argparse import ArgumentParser

from gensim.models.word2vec import Word2Vec

import configs
import src.data as data
import src.prepare as prepare
import src.process as process
import src.utils.functions.cpg as cpg
from torch_geometric.data import Data
from pandas import Series,DataFrame
from os import listdir
from os.path import isfile, join

PATHS = configs.Paths()
FILES = configs.Files()
DEVICE = FILES.get_device()


def select(dataset):
    #result = dataset.loc[dataset['project'] == "NVD"]
    result=dataset
    len_filter = result.func.str.len() < 5000  #back-up:1200
    result = result.loc[len_filter]
    #print(len(result))
    #result = result.iloc[11001:]
    result = result.head(900)

    return result



def process_task(stopping):
    context = configs.Process()
    GGTN = configs.GGTN()
    model_path = PATHS.model + FILES.model
    model = process.GGTN(path=model_path, device=DEVICE, model=GGTN.model, learning_rate=GGTN.learning_rate,
                           weight_decay=GGTN.weight_decay,
                           loss_lambda=GGTN.loss_lambda)
    train = process.Train(model, context.epochs)

    dataset=DataFrame(columns=['input','target'])
    data_sets_files = sorted([f for f in listdir("dataset/") if isfile(join("dataset/", f))])

    for file in data_sets_files:

        dataset_sub = data.load("dataset/",file)
        dataset=dataset.append(dataset_sub)


    #dataset=DataFrame({'input':data_input,'target':data_target})

  # split the dataset and pass to DataLoader with batch size
    train_loader, val_loader, test_loader = list(
        map(lambda x: x.get_loader(context.batch_size, shuffle=context.shuffle),
            data.train_val_test_split(dataset, shuffle=context.shuffle)))
    train_loader_step = process.LoaderStep("Train", train_loader, DEVICE)
    val_loader_step = process.LoaderStep("Validation", val_loader, DEVICE)
    test_loader_step = process.LoaderStep("Test", test_loader, DEVICE)

    if stopping:
        early_stopping = process.EarlyStopping(model, patience=context.patience)
        train(train_loader_step, val_loader_step, early_stopping)
        model.load()
    else:
        train(train_loader_step, val_loader_step)
        model.save()

    process.predict(model, test_loader_step)


def main():
    """
    main function that executes tasks based on command-line options
    """
    parser: ArgumentParser = argparse.ArgumentParser()
    #parser.add_argument('-p', '--prepare', help='Prepare task', required=False)

    parser.add_argument('-p', '--process', action='store_true')
    parser.add_argument('-pS', '--process_stopping', action='store_true')

    args = parser.parse_args()


    if args.process:
        process_task(False)
    if args.process_stopping:
        process_task(True)



if __name__ == "__main__":
    main()
