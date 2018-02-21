from django.core.files import File
from django.utils.encoding import smart_str
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import cv2
from .tools.File_Processor.messageProcessor import loadMessage, parseMessage
from .tools.Vigenere.vigenere import encrypt, decrypt
from .tools.BPCS.steganoProcessing import insertMessage, extractMessage, psnr
from .forms import InsertionForm, ExtractionForm
import os 

def index(request):
  response = ""
  response += "<a href='/app/insertion'>Message Insertion</a><br>"
  response += "<a href='/app/extraction'>Message Extraction</a><br>"
  return HttpResponse(response)

def download(request, io, filetype, filename):
  path_to_file = 'file/'+io+'/'+filetype+'/'+filename  
  with open(path_to_file, 'rb') as f:
    myfile = File(f)
    response = HttpResponse(myfile, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + smart_str(filename)
  return response

def image(request, io, filetype, filename):
  path_to_file = 'file/'+io+'/'+filetype+'/'+filename  
  ext = filename.split('.')[-1]
  with open(path_to_file, 'rb') as f:
    myfile = File(f)
    response = HttpResponse(myfile, content_type='image/'+ext)
    response['Content-Disposition'] = 'attachment; filename=' + smart_str(filename)
  return response

def insertion(request):
  if request.method == 'GET':
    form = InsertionForm()
    template = loader.get_template('app/html/form.html')
    context = {'form': form, 'target': 'insertion'}
    return HttpResponse(template.render(context, request))
  elif request.method == 'POST':
    form = InsertionForm(request.POST, request.FILES)
    print(request.FILES)

    if form.is_valid():
      key = request.POST.get('key', '-')
      treshold = float(request.POST.get('treshold', '-'))/100
      medium_name = request.FILES['medium_image'].name
      message_name = request.FILES['message'].name
      
      with open('file/input/medium_image/'+medium_name, 'wb+') as destination:
        for chunk in request.FILES['medium_image'].chunks():
          destination.write(chunk)
      
      with open('file/input/message/'+message_name, 'wb+') as destination:
        for chunk in request.FILES['message'] .chunks():
          destination.write(chunk)



      chiperAoB = encrypt(loadMessage('file/input/message/'+message_name), key) #array of byte yang akan dimasukkan
      #Build stegano image here
      status, payload, messagesize, image = insertMessage('file/input/medium_image/'+medium_name, chiperAoB, key, treshold)
      if status == 1 :
        cv2.imwrite('file/output/stegano_image/stegano_'+medium_name, image)
        psnrScore = psnr('file/input/medium_image/'+medium_name, 'file/output/stegano_image/stegano_'+medium_name)
        template = loader.get_template('app/html/insertion_result.html')
        context = {
            'medium_name': medium_name,
            'payload': payload,
            'medium_src': 'image/input/medium_image/'+medium_name,
            'medium_download': 'download/input/medium_image/'+medium_name,
            'message_name': message_name,
            'messagesize': messagesize,
            'message_download': 'download/input/message/'+message_name,
            #TODO benerin ini setelah berhasil build stegano image
            'stegano_name': 'stegano_'+medium_name,
            'stegano_psnr': str(psnrScore),
            'stegano_src': 'image/output/stegano_image/stegano_'+medium_name,
            'stegano_download': 'download/output/stegano_image/stegano_'+medium_name,
        }
        return HttpResponse(template.render(context, request))
      else :
        return HttpResponse("Message too big. Payload : " + str(payload) + " Bytes. Message : " + str(messagesize) + " Bytes.")
      
  return HttpResponse("error")

def extraction(request):
  if request.method == 'GET':
    form = ExtractionForm()
    template = loader.get_template('app/html/form.html')
    context = {'form': form, 'target': 'extraction'}
    return HttpResponse(template.render(context, request))
  elif request.method == 'POST':
    form = ExtractionForm(request.POST, request.FILES)

    if form.is_valid():
      key = request.POST.get('key', '-')
      treshold = float(request.POST.get('treshold', '-'))/100
      stegano_name = request.FILES['stegano_image'].name
      
      with open('file/input/stegano_image/'+stegano_name, 'wb+') as destination:
        for chunk in request.FILES['stegano_image'].chunks():
          destination.write(chunk)

      #Extract message here
      chiperAoB = extractMessage('file/input/stegano_image/'+stegano_name, key, treshold)  # ntar array of byte yg berhasil diekstrak diassign ke sini
      filename, filecontent = parseMessage(decrypt(chiperAoB,key))
      with open('file/output/message/'+filename, 'wb+') as destination:
        destination.write(filecontent)

      message_name = filename

      template = loader.get_template('app/html/extraction_result.html')
      context = {
        'stegano_name': stegano_name,
        'stegano_src': 'image/input/stegano_image/'+smart_str(stegano_name),
        'stegano_download': 'download/input/stegano_image/'+smart_str(stegano_name),
        'message_name': message_name,
        'message_download': 'download/output/message/'+smart_str(message_name),
      }
      return HttpResponse(template.render(context, request))
  return HttpResponse("error")

    




# Create your views here.
