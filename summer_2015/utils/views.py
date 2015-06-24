#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render_to_response,RequestContext

def mp_render(request, template, context={}):
    return render_to_response(template, context, context_instance=RequestContext(request))



