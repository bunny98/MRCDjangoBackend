import sys
from os import path
from django.shortcuts import render
from django.http import HttpResponse
import sys
from . import forms
import json
from prepro import convert_to_features, word_tokenize
from config import flags
from main import giveModel
import tensorflow as tf
import threading
from time import sleep
from django.http import JsonResponse
from .models import FileTable
from .serializers import FileNamesSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

import numpy as np
query = []
response = ""


context = """Forests are an intricate ecosystem on earth which contains trees, shrubs, grasses and more. The constituents of forests which are trees and plants form a major part of the forests. Furthermore, they create a healthy environment so that various species of animals can breed and live there happily. Therefore, we see how forests are a habitat for a plethora of wild animals and birds. In addition to being of use to wildlife, forests benefit mankind greatly and hold immense significance.
Forests cover a significant area of the earth. They are a great natural asset to any region and hold immense value. For instance, forests fulfill all our needs of timber, fuel, fodder, bamboos and more. They also give us a variety of products that hold great commercial as well as industrial value."""
config = flags.FLAGS

sys.path.insert(0, '/media/kavyansh/8A9A1B9F9A1B86BB/QANet-master')

def index(request):
    return render(request, "main/demo.html")



def responseFunction(run_event):
        global query, response
        model = giveModel(config)
        with open(config.word_dictionary, "r") as fh:
                word_dictionary = json.load(fh)
        with open(config.char_dictionary, "r") as fh:
            char_dictionary = json.load(fh)

        sess_config = tf.ConfigProto(allow_soft_placement=True)
        sess_config.gpu_options.allow_growth = True

        with model.graph.as_default():

            with tf.Session(config=sess_config) as sess:
                sess.run(tf.global_variables_initializer())
                saver = tf.train.Saver()
                saver.restore(sess, tf.train.latest_checkpoint(config.save_dir))
                sess.run(model.assign_vars)
                while run_event.is_set():
                    sleep(0.1)
                    if query:
                        context = word_tokenize(query[0].replace("''", '" ').replace("``", '" '))
                        c,ch,q,qh = convert_to_features(config, query, word_dictionary, char_dictionary)
                        fd = {'context:0': [c],
                                'question:0': [q],
                                'context_char:0': [ch],
                                'question_char:0': [qh]}
                        yp1,yp2 = sess.run([model.yp1, model.yp2], feed_dict = fd)
                        yp2[0] += 1
                        response = " ".join(context[yp1[0]:yp2[0]])
                        query = []

def FormQAView(request):
    global query, response
    form = forms.FormQA()
    if not myThread.is_alive():
        myThread.start()
    if request.method == 'POST':
        form = forms.FormQA(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            context = form.cleaned_data['context']
            # print('Question: '+form.cleaned_data['question'] +'\nContext: '+form.cleaned_data['context'])
            print("THIS WORKED")
            query = (context, question)
            while not response:
                sleep(0.1)
            response_ = response
            response = []
            return HttpResponse(response_)
    
    return render(request, 'main/form.html', context={"form":form})

run_event = threading.Event()
run_event.set()
myThread = threading.Thread(target=responseFunction, args = [run_event])

def simple_upload(request):
    my_dict = {}
    # # filereq = request.POST['filename']
    # files = FileTable.objects.get(filename='my school')
    # print(files.filename)
    # my_dict = {'files':files}
    # for obj in files:
    #     print(obj.filename)
    #     # if obj.filename == filereq:
    #     #     my_dict = {'files': obj}
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        filename = request.POST['filename']
        fileEntry = FileTable(file = myfile, filename=filename)
        fileEntry.save()
        
        return HttpResponse("Success")
    return render(request, 'main/simple_upload.html', context=my_dict)

@api_view()
def getFileNames(request):
    files = FileTable.objects.all()
    my_dict = {'name': []}
    for obj in files:
        my_dict['name'].append(obj.filename)
    print(my_dict)
    return JsonResponse(my_dict)

@api_view(['POST'])
def getAnswer(request):
    filereq = request.data['filename']
    question = request.data['question']
    f = FileTable.objects.get(filename=filereq).file
    f.open(mode='rb')
    context = str(f.read())
    f.close()
    # print("CONTEXT: "+context)
    # print("QUESTION: "+question)

    global query, response
    if not myThread.is_alive():
        myThread.start()
    query = (context, question)
    while not response:
        sleep(0.1)
    response_ = response
    response = []
    return JsonResponse({'answer':response_})

@api_view(['POST'])
def deleteFile(request):
    fileDel = request.data['filename']
    f = FileTable.objects.get(filename=fileDel)
    f.delete()
    return JsonResponse({'Success':True})