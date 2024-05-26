from django.shortcuts import render
from .models import Chapter

# Create your views here.

def index(request):
    """View function for home page of site."""
    updated_chapters = Chapter.objects.all().order_by('-published_date')[:5]
    context = {
        'updated_chapters': updated_chapters,
    }
    return render(request, 'index.html', context=context)
