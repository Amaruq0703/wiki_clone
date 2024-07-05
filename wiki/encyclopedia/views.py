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


entries = util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        'search_form':  NewSearchForm()
    })

def getentry(request, title):

    if title in entries:
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
                return redirect(reverse('encyclopedia:getentry', args=[query]))
            
            else:
                related = []

                for entry_name in entries:
                    if query.lower() in entry_name.lower() or entry_name.lower() in query.lower():
                        related.append(entry_name)

                return render(request, "encyclopedia/searchpage.html", {
                "query": query,
                "related": related,
                "search_form": NewSearchForm()
                })
            





