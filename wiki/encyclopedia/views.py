from django.shortcuts import render, redirect
import markdown2
from django.urls import reverse
from django import forms
from . import util


class NewSearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'search',
        'placeholder' : 'Search Encyclopedia'
    }))

class NewEntryForm(forms.Form):

    topic = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Enter Topic Name',
    }), label='')

    content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder' : 'Enter Markdown Content Here',
    }), label='')


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'search_form':  NewSearchForm()
    })

def getentry(request, title):

    if title in util.list_entries():
        mdfile = util.get_entry(title)
        htmlfile = markdown2.markdown(mdfile)
        
        return render(request, 'encyclopedia/wikipage.html', {   
            'htmlfile' : htmlfile,
            'title' : title,
            'search_form' : NewSearchForm()
        })
    
    else:
        return render(request, 'encyclopedia/errorpage.html', {
            'title' : title,
            'search_form' : NewSearchForm()
        })
    


def search(request):

    if request.method == 'POST':
        form = NewSearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data['query']
            searchentries = util.get_entry(query)

            if searchentries:
                return redirect(reverse('encyclopedia/wikipage.html', args=[query]))
            
            else:
                related = []

                for entry_name in util.list_entries():
                    if query.lower() in entry_name.lower() or entry_name.lower() in query.lower():
                        related.append(entry_name)

                return render(request, "encyclopedia/searchpage.html", {
                "query": query,
                "related": related,
                "search_form": NewSearchForm()
                })

def createentry(request):

    if request.method == 'POST':
        createform = NewEntryForm(request.POST)

        if createform.is_valid():
        
            topic = createform.cleaned_data['topic']
            content = createform.cleaned_data['content']

            if topic in util.list_entries():
                return render(request, 'encyclopedia/createerror.html', {
                    'topic' : topic,
                    'search_form' : NewSearchForm()
                })
                
            util.save_entry(topic, content)
            return redirect(reverse('encyclopedia:getentry', args=[topic]))
            
    return render(request, 'encyclopedia/newtask.html', {
        'createform' : NewEntryForm()
    })







