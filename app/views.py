from django.utils.encoding import smart_str
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import InsertionForm, ExtractionForm

def index(request):
  response = ""
  response += "<a href='/app/insertion'>Message Insertion</a><br>"
  response += "<a href='/app/extraction'>Message Extraction</a><br>"
  return HttpResponse(response)

def download(request, io, filetype, filename):
  path_to_file = 'file/input/'+io+'/'+filetype+'/'+filename
  response = HttpResponse()
  response['mimetype']='application/force-download'
  response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
  response['X-Sendfile'] = smart_str(path_to_file)
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
      medium_name = request.FILES['medium_image'].name
      with open('file/input/medium_image/'+medium_name, 'wb+') as destination:
        for chunk in request.FILES['medium_image'].chunks():
          destination.write(chunk)

      message_name = request.FILES['message'].name
      with open('file/input/message/'+message_name, 'wb+') as destination:
        for chunk in request.FILES['message'] .chunks():
          destination.write(chunk)

      #Build stegano image here

      template = loader.get_template('app/html/insertion_result.html')
      context = {
          'medium_name': medium_name,
          'medium_src': 'file/input/medium_image/'+medium_name,
          'medium_download': 'download/input/medium_image/'+medium_name,
          'message_name': message_name,
          'message_download': 'download/input/message/'+message_name,
          #TODO benerin ini setelah berhasil build stegano image
          'stegano_name': medium_name,
          'stegano_psnr': '100',
          'stegano_src': 'file/input/medium_image/'+medium_name,
          'stegano_download': 'download/input/medium_image/'+medium_name,
        }
      return HttpResponse(template.render(context, request))
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
      stegano_name = request.FILES['stegano_image'].name
      with open('file/input/stegano_image/'+stegano_name, 'wb+') as destination:
        for chunk in request.FILES['stegano_image'].chunks():
          destination.write(chunk)

    #Extract message here

      template = loader.get_template('app/html/extraction_result.html')
      context = {
        'stegano_name': stegano_name,
        'stegano_src': 'input/stegano_image/'+smart_str(stegano_name),
        'stegano_download': 'download/input/stegano_image/'+smart_str(stegano_name),
        #TODO benerin ini setelah berhasil extract message
        'message_name': smart_str(stegano_name),
        'message_download': 'download/input/message/'+smart_str(stegano_name),
      }
      return HttpResponse(template.render(context, request))
  return HttpResponse("error")

    




# Create your views here.
