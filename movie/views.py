from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from django.db.models import Count
from collections import defaultdict

# Create your views here.
def home(request):
    #return HttpResponse('<h1> Welcome to Home Page </h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': 'Jacobo Restrepo'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre')
    movie_counts_by_year = {}
    movie_counts_by_genre = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    movie_counts_by_genre = defaultdict(int)

    for movie in Movie.objects.all():
        first_genre = movie.genre.split(',')[0] if movie.genre else "None"
        movie_counts_by_genre[first_genre] += 1

    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_year))
    bar_positions_genre = range(len(movie_counts_by_genre))

    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png1 = buffer.getvalue()
    buffer.close()

    graphic1 = base64.b64encode(image_png1).decode('utf-8')
    plt.close()

    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=bar_width, align='center')
    plt.title('Movies per first genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=90)

    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png2 = buffer.getvalue()
    buffer.close()

    graphic2 = base64.b64encode(image_png2).decode('utf-8')
    plt.close()

    return render(request, 'statistics.html', {'graphic1': graphic1, 'graphic2': graphic2})
