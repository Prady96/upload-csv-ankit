from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.utils.decorators import method_decorator
from django.core.files.storage import default_storage
import pandas as pd
import os
import json
import pdb
from django.conf import settings

# Create your views here.


class File_upload(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(File_upload, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        obj = Csv_file.objects.all()
        return render(request, 'upload.html',locals())

    def post(self, request, *args, **kwargs):
        data_dict = {'data': 'success'}
        ex_file = request.FILES['file_0']
        print(ex_file)
        if not ex_file.name.endswith('.csv'):
            if not ex_file.name.endswith('.CSV'):
                resp = HttpResponse(content_type="application/json", status=400)
        df = pd.read_csv(ex_file)
        if df.isna().any().any():
            resp = HttpResponse(content_type="application/json", status=400)
        obj = Csv_file()
        for i in range(0,len(df)):

            obj.one = df['topic_name'][i]
            obj.two = df['count'][i]
            obj.three = df['marks'][i]
            obj.four = df['subject'][i]
            obj.save()
        path = os.path.join(os.path.join(settings.BASE_DIR, 'media'),ex_file.name)
        default_storage.save(str(path), ex_file)
        obj = Csv_file.objects.all()
        res = []
        for i in obj:
            d = {}
            d['one'] = i.one
            d['two'] = i.two
            d['three'] = i.three
            d['four']  = i.four
            res.append(d)
        dir = path.split('\\')[-1]
        res.append('/media/'+dir)
        resp = HttpResponse(json.dumps(res), content_type='application/json', status=200)
        return resp
