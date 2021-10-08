
#* Library Imports
import json
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, response
from django.shortcuts import redirect

#* Relative Imports
from .utils.test import get_answer


class ParseQuery(APIView):
    
    def post(self,request,format=None):
        try:
            #? Converting Json request from frontend into python dictionary
            request_data = json.loads(request.body)
            
            #? Fatching parameters
            sent = request_data['sentence']
            
            #? Finding output
            result = get_answer(sent)
            
            return Response({"status_code":200,"response_msg":"Successful Retrival","message":result})
                
        except Exception as e:
            print(str(e))
            return Response({"status_code":500,"response_msg":"Something went wrong, please try again!"})
