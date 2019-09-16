from django.http import HttpResponse
from django.template import loader


# Create your views here

def index(request):
    template = loader.get_template('top.html')
    context = {
        'latest_question_list': "hi",
    }
    return HttpResponse(template.render(context, request))
    # return render(request, 'CurrentRate.html')


def M5(request):
    template = loader.get_template('CurrentRate.html')
    context = {
        'latest_question_list': "hi",
    }
    return HttpResponse(template.render(context, request))
    # return render(request, 'CurrentRate.html')


def m5vsMaComp(request):
    template = loader.get_template('m5vsMaComp.html')
    context = {
        'latest_question_list': "hi",
    }
    return HttpResponse(template.render(context, request))
    # return render(request, 'CurrentRate.html')
