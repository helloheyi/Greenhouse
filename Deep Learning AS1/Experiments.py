#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 20:30:25 2024

@author: hy
"""

import argparse
import yaml
import copy
import matplotlib.pyplot as plt
from models import TwoLayerNet, SoftmaxRegression
from optimizer import SGD
from utils import load_mnist_trainval, load_mnist_test, generate_batched_data, train, evaluate, plot_curves
import os 
current_dir = os.getcwd()

parser = argparse.ArgumentParser(description='CS7643 Assignment-1')

# parser.add_argument('--config', default='./config_softmax.yaml')
parser.add_argument('--config', default=current_dir + '/configs/config_twolayer.yaml')

global args
args = parser.parse_args()
with open(args.config) as f:
    config = yaml.load(f)

for key in config:
    for k, v in config[key].items():
        setattr(args, k, v)


def Baseline(train_data, train_label,val_data,val_label,test_data,test_label,model): 
    
    optimizer = SGD(learning_rate=args.learning_rate, reg=args.reg)
    for epoch in range(args.epochs):
        batched_train_data, batched_train_label = generate_batched_data(train_data, train_label,
                                                                                batch_size=args.batch_size, shuffle=True)
        train_loss, train_acc = train(epoch, batched_train_data, batched_train_label, model, optimizer, args.debug)
        
        
        batched_val_data, batched_val_label = generate_batched_data(val_data,val_label,
                                                                                batch_size=args.batch_size)
        val_loss, val_acc = evaluate( batched_train_data, batched_train_label, model, args.debug)
        
        
    batched_test_data, batched_test_label = generate_batched_data(test_data, test_label,
                                                                  batch_size=args.batch_size)
    test_loss, test_acc = evaluate(batched_test_data, batched_test_label,model)
        
    
    return train_acc,val_acc, test_acc


def LR(train_data, train_label,test_data, test_label,model): 
    LR_list = [3,1,0.1,0.05,0.01]   
    train_acc_list = []
    test_acc_list = []
    for LR_val in LR_list:
        model = TwoLayerNet(hidden_size=args.hidden_size)
        optimizer = SGD(learning_rate=LR_val, reg=args.reg)
        for epoch in range(args.epochs):
            batched_train_data, batched_train_label = generate_batched_data(train_data, train_label,
                                                                                    batch_size=args.batch_size, shuffle=True)
            train_loss, train_acc = train(epoch, batched_train_data, batched_train_label, model, optimizer, args.debug)
            print('LR Train Dataset')
            
        
        # batched_train_data, batched_train_label = generate_batched_data(train_data, train_label,
        #                                                                           batch_size=args.batch_size, shuffle=True)
        # train_loss, train_acc = train(args.epochs, batched_train_data, batched_train_label, model, optimizer, args.debug)
        batched_test_data, batched_test_label = generate_batched_data(test_data, test_label,
                                                                                    batch_size=args.batch_size)
        val_loss, val_acc = evaluate(batched_test_data, batched_test_label,model, args.debug)
        print('LR Test Dataset')

        train_acc_list.append(train_acc)

        test_acc_list.append(val_acc)
     
    x = LR_list
    plt.plot(x,train_acc_list, label="Train", linestyle="-",marker='^')
    plt.plot(x,test_acc_list, label="Test", linestyle="-",marker='^')
    plt.xlabel("Learning Rate")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)    

     # plt.show()
    plt.title("Accuracy Curve")
    plt.savefig('Accuracy Curve to Learning Curve.png')
    plt.close()
    return train_acc_list,test_acc_list


def RC(train_data, train_label,val_data,val_label,test_data,test_label,model): 
    RC_list = [1,0.1,0.01,0.001,0.0001]   
    train_acc_list = []
    val_acc_list = []
    test_acc_list = []
    
    
    for RC_val in RC_list:
        model = TwoLayerNet(hidden_size=args.hidden_size)
        optimizer = SGD(learning_rate=args.learning_rate, reg=RC_val)
        for epoch in range(args.epochs):
            batched_train_data, batched_train_label = generate_batched_data(train_data, train_label,
                                                                                    batch_size=args.batch_size, shuffle=True)
            train_loss, train_acc = train(epoch, batched_train_data, batched_train_label, model, optimizer, args.debug)
            print('RC Train Dataset')
            
            
            batched_val_data, batched_val_label = generate_batched_data(val_data,val_label,
                                                                                    batch_size=args.batch_size)
            val_loss, val_acc = evaluate( batched_train_data, batched_train_label, model, args.debug)
            print('RC Val Dataset')
            
        train_acc_list.append(train_acc)
        val_acc_list.append(val_acc)

        batched_test_data, batched_test_label = generate_batched_data(test_data, test_label,
                                                                      batch_size=args.batch_size)
        test_loss, test_acc = evaluate(batched_test_data, batched_test_label,model)
        test_acc_list.append(test_acc)
        print('RC Test Dataset')
        
     
    x = RC_list
    plt.plot(x,train_acc_list, label="Train", linestyle="-",marker='^')
    plt.plot(x,val_acc_list, label="Validation", linestyle="-",marker='^')
    plt.plot(x,test_acc_list, label="Test", linestyle="-",marker='^')
    plt.xlabel("Regularization Coefficient")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)    

     # plt.show()
    plt.title("Accuracy Curve")
    plt.savefig('Accuracy Curve to Regularization.png')
    plt.close()
    return train_acc_list,val_acc_list, test_acc_list


def TuneParameter(train_data, train_label,val_data,val_label,test_data,test_label,model): 
    RC_list = [1,0.1,0.01,0.001,0.0001]   
    train_acc_list = []
    val_acc_list = []
    test_acc_list = []
    ## tune: learning rate, regulation coff, hidden size 
    
    for RC_val in RC_list:
        optimizer = SGD(learning_rate=args.learning_rate, reg=RC_val)
        best_acc = 0.0
        for epoch in range(args.epochs):
            batched_train_data, batched_train_label = generate_batched_data(train_data, train_label,
                                                                                    batch_size=args.batch_size, shuffle=True)
            train_loss, train_acc = train(epoch, batched_train_data, batched_train_label, model, optimizer, args.debug)
            train_acc_list.append(train_acc)
            print('RC Train Dataset')
            
            
            batched_val_data, batched_val_label = generate_batched_data(val_data,val_label,
                                                                                    batch_size=args.batch_size)
            val_loss, val_acc = evaluate( batched_train_data, batched_train_label, model, args.debug)
            val_acc_list.append(val_acc)
            print('RC Val Dataset')
            
            if val_acc > best_acc:
               best_acc = val_acc
               best_model = copy.deepcopy(model)
        batched_test_data, batched_test_label = generate_batched_data(test_data, test_label,
                                                                      batch_size=args.batch_size)
        epoch_loss, epoch_acc = evaluate(batched_test_data, batched_test_label,model, args.debug)
        test_acc_list.append(epoch_acc)
        print('RC Test Dataset')
        
        
        
     
    x = RC_list
    plt.plot(x,train_acc, label="Train", linestyle="-")
    plt.plot(x,val_acc, label="Validation", linestyle="-")
    plt.plot(x,test_acc, label="Test", linestyle="-")
    plt.xlabel("Regularization Coefficient")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)    

     # plt.show()
    plt.title("Accuracy Curve")
    plt.savefig('Accuracy Curve to Regularization.png')
    plt.close()
    return train_acc,val_acc, test_acc











if __name__ == '__main__':        
    
    ## The number of epochs is a hyperparameter that defines the number times that the learning algorithm will work through the entire training dataset. 
    ## For instance, if you set the number of epochs to 10, the model will go through the entire dataset 10 times
    model = TwoLayerNet(hidden_size=args.hidden_size)
    train_data, train_label, val_data, val_label = load_mnist_trainval()
    test_data, test_label = load_mnist_test()
    # LR_train_acc,LR_test_acc = LR(train_data, train_label,test_data, test_label,model)
    
    RC_train_acc,RC_val_acc,RC_test_acc = RC(train_data, train_label,val_data,val_label,test_data,test_label,model)
    
    # baseline_Train,baseline_val, baseline_Test = Baseline(train_data, train_label,val_data,val_label,test_data,test_label,model)
    
    # optimizer = SGD(learning_rate=args.learning_rate, reg=args.reg)
    # batched_train_data, batched_train_label = generate_batched_data(train_data, train_label,
    #                                                                         batch_size=args.batch_size, shuffle=True, seed=1028)
    # epoch_loss, Train_acc = train(args.epochs, batched_train_data, batched_train_label, model, optimizer, args.debug)