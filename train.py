import argparse
import functools
import os
import shutil
from datetime import datetime

import paddle
import paddle.distributed as dist
import paddle.nn as nn
from paddle.io import DataLoader
from paddle.metric import accuracy
from paddle.static import InputSpec
from visualdl import LogWriter
from utils.mobilefacenet import MobileFaceNet
from utils.reader import CustomDataset
from utils.utility import add_arguments, print_arguments

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('gpu',              str,    '0,1',                    '训练使用的GPU序号')
add_arg('batch_size',       int,    64,                       '训练的批量大小')
add_arg('num_workers',      int,    16,                       '读取数据的线程数量')
add_arg('num_epoch',        int,    120,                      '训练的轮数')
add_arg('num_classes',      int,    10177,                    '分类的类别数量')
add_arg('learning_rate',    float,  1e-3,                     '初始学习率的大小')
add_arg('train_list_path',  str,    'dataset/train_list.txt', '训练数据的数据列表路径')
add_arg('test_list_path',   str,    'dataset/test_list.txt',  '测试数据的数据列表路径')
add_arg('save_model',       str,    'models/mobilefacenet',   '模型保存的路径')
add_arg('resume',           str,    None,                     '恢复训练，当为None则不使用预训练模型，使用恢复训练模型最好同时也改学习率')
add_arg('pretrained_model', str,    None,                     '预训练模型的路径，当为None则不使用预训练模型')
args = parser.parse_args()


# 评估模型
def test(model, test_loader):
    model.eval()
    accuracies = []
    for batch_id, (img, label) in enumerate(test_loader()):
        label = paddle.reshape(label, shape=(-1, 1))
        out = model(img)
        acc = accuracy(input=out, label=label)
        accuracies.append(acc.numpy()[0])
    model.train()
    return float(sum(accuracies) / len(accuracies))


# 保存模型
def save_model(args, model, model_feature, optimizer):
    if not os.path.exists(os.path.join(args.save_model, 'params')):
        os.makedirs(os.path.join(args.save_model, 'params'))
    if not os.path.exists(os.path.join(args.save_model, 'infer')):
        os.makedirs(os.path.join(args.save_model, 'infer'))
    # 保存模型参数
    paddle.save(model.state_dict(), os.path.join(args.save_model, 'params/model.pdparams'))
    paddle.save(optimizer.state_dict(), os.path.join(args.save_model, 'params/optimizer.pdopt'))
    # 保存预测模型
    paddle.jit.save(layer=model_feature,
                    path=os.path.join(args.save_model, 'infer/model'),
                    input_spec=[InputSpec(shape=[None, 3, 112, 112], dtype='float32')])


def train(args):
    # 设置支持多卡训练
    dist.init_parallel_env()
    if dist.get_rank() == 0:
        shutil.rmtree('log', ignore_errors=True)
        # 日志记录器
        writer = LogWriter(logdir='log')
    # 获取数据
    train_dataset = CustomDataset(args.train_list_path, is_train=True)
    train_loader = DataLoader(dataset=train_dataset, batch_size=args.batch_size, shuffle=True, num_workers=args.num_workers)

    test_dataset = CustomDataset(args.test_list_path, is_train=False)
    test_loader = DataLoader(dataset=test_dataset, batch_size=args.batch_size, num_workers=args.num_workers)

    # 获取模型
    model_feature = MobileFaceNet()
    model = paddle.nn.Sequential(model_feature,
                                 paddle.nn.Linear(in_features=512, out_features=args.num_classes))
    if dist.get_rank() == 0:
        paddle.summary(model, input_size=(None, 3, 112, 112))
    # 设置支持多卡训练
    model = paddle.DataParallel(model)

    # 分段学习率
    boundaries = [10, 30, 70, 100]
    lr = [0.1 ** l * args.learning_rate for l in range(len(boundaries) + 1)]
    scheduler = paddle.optimizer.lr.PiecewiseDecay(boundaries=boundaries, values=lr, verbose=True)
    # 设置优化方法
    optimizer = paddle.optimizer.Adam(parameters=model.parameters(),
                                      learning_rate=scheduler,
                                      weight_decay=paddle.regularizer.L2Decay(1e-4))

    # 加载预训练模型
    if args.pretrained_model is not None:
        model_dict = model.state_dict()
        param_state_dict = paddle.load(os.path.join(args.pretrained_model, 'model.pdparams'))
        for name, weight in model_dict.items():
            if name in param_state_dict.keys():
                if weight.shape != list(param_state_dict[name].shape):
                    print('{} not used, shape {} unmatched with {} in model.'.
                            format(name, list(param_state_dict[name].shape), weight.shape))
                    param_state_dict.pop(name, None)
            else:
                print('Lack weight: {}'.format(name))
        model.set_dict(param_state_dict)

    # 恢复训练
    if args.resume is not None:
        model.set_state_dict(paddle.load(os.path.join(args.resume, 'model.pdparams')))
        optimizer.set_state_dict(paddle.load(os.path.join(args.resume, 'optimizer.pdopt')))

    # 获取损失函数
    loss = nn.CrossEntropyLoss()
    train_step = 0
    test_step = 0
    # 开始训练
    for epoch in range(args.num_epoch):
        loss_sum = []
        for batch_id, (img, label) in enumerate(train_loader()):
            out = model(img)
            # 计算损失值
            los = loss(out, label)
            loss_sum.append(los)
            los.backward()
            optimizer.step()
            optimizer.clear_grad()
            # 多卡训练只使用一个进程打印
            if batch_id % 100 == 0 and dist.get_rank() == 0:
                print('[%s] Train epoch %d, batch_id: %d, loss: %f' % (
                    datetime.now(), epoch, batch_id, sum(loss_sum) / len(loss_sum)))
                writer.add_scalar('Train loss', los, train_step)
                train_step += 1
                loss_sum = []
        # 多卡训练只使用一个进程执行评估和保存模型
        if dist.get_rank() == 0:
            acc = test(model, test_loader)
            print('[%s] Train epoch %d, accuracy: %f' % (datetime.now(), epoch, acc))
            writer.add_scalar('Test acc', acc, test_step)
            # 记录学习率
            writer.add_scalar('Learning rate', scheduler.last_lr, epoch)
            test_step += 1
            save_model(args, model, model_feature, optimizer)
        scheduler.step()


if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
    print_arguments(args)
    dist.spawn(train, args=(args,))
