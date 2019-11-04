from django.http import HttpResponse
from django.template import loader


# Create your views here

def index(request):
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': "hi",
    }
    return HttpResponse(template.render(context, request))


def test(request):
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': "hi",
    }
    return HttpResponse(template.render(context, request))
    # return render(request, 'CurrentRate.html')
