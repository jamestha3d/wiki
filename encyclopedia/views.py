from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util
import requests
from django.urls import reverse
from django import forms
import markdown2
import random

class NewEntryForm(forms.Form):
    title = forms.CharField(label= "Entry Title", widget=forms.TextInput(attrs={"class": 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":6, "cols":30, "class": 'form-control'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def edit(request, title):    
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            content = f"# {title} \n {content}"

            #do something with info:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": title}))
            
        else:
            return render(request, "encyclopedia/edit.html", {"form": form})

    else:
        form_content2 = util.get_entry(title)
        n = len(title) + 3
        form_content = form_content2[n:]
        return render(request, "encyclopedia/edit.html", {"form": NewEntryForm(initial={"title": title, "content": form_content})})


def entry(request, title):
    entry = util.get_entry(title)
    if entry:
    #markdown2.markdown(entry)
        return render(request, "encyclopedia/title.html", {
        "entry": markdown2.markdown(entry),
        "title": title
        })
    #else if method == post:
    else:
        return render(request, "encyclopedia/error.html", {"error": "Entry does not exist!"})

def haphazard(request):
    #pick an entry by random.
    #go to entry
    entries = util.list_entries()
    select = random.sample(entries, 1)
    return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": select[0]}))
    

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            content = f"# {title} \n\n {content}"
            #do something with info:
            if title.lower() not in (entry.lower() for entry in entries):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": title}))
            else:
                return render(request, "encyclopedia/error.html", {"error": "Entry already exists!"})

                #check if entry does not exist
                #add entry to list of entries
            #take user to the page of this entry
            #return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": title}))
        else:
            return render(request, "encyclopedia/create.html", {"form": form})
    else:
        return render(request, "encyclopedia/create.html", {"form": NewEntryForm()})

def search(request):
    query = request.GET['q']
    entries = util.list_entries()
    if query.lower() in (entry.lower() for entry in entries):
        return HttpResponseRedirect(reverse("wiki:entry", kwargs={"title": query}))
    else:
        #show all the results that look like query
        results = [result for result in entries if query.lower() in result.lower()]
        return render(request, "encyclopedia/results.html", {
        "results": results
        })
    
   


def error(request, message):
    #message = message
    return render(request, "encyclopedia/error.html", {"error": message})