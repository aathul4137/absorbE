from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from django.views import generic
from .models import Notes
from youtubesearchpython import VideosSearch
from wikipedia import wikipedia, PageError,DisambiguationError, WikipediaException
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
def base(request):
    return render(request, 'base.html')

@login_required
def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
            try:
                r = requests.get(url)
                r.raise_for_status()
                answer = r.json()
                result_list = []
                items = answer.get('items', [])

                for item in items[:10]:  # Get only the first 10 items
                    volume_info = item.get('volumeInfo', {})
                    image_links = volume_info.get('imageLinks', {})
                    result_dict = {
                        'title': volume_info.get('title', 'N/A'),
                        'subtitle': volume_info.get('subtitle', 'N/A'),
                        'description': volume_info.get('description', 'N/A'),
                        'count': volume_info.get('pageCount', 'N/A'),
                        'categories': volume_info.get('categories', []),
                        'rating': volume_info.get('averageRating', 'N/A'),
                        'thumbnail': image_links.get('thumbnail', 'N/A'),
                        'preview': volume_info.get('previewLink', 'N/A')
                    }
                    result_list.append(result_dict)
                
                context = {
                    'form': form,
                    'results': result_list
                }
                return render(request, 'books.html', context)
            except requests.exceptions.RequestException as e:
                print(f"HTTP Request failed: {e}")
                context = {
                    'form': form,
                    'error': 'Failed to fetch data from Google Books API'
                }
                return render(request, 'books.html', context)
                    
    else:
        form = DashboardForm()
    
    context = {'form': form}
    return render(request, 'books.html', context)

@login_required
def game(request):
    return render(request,'game.html')

@login_required
def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{text}"
            r = requests.get(url)
            answer = r.json()
            try:
                phonetics = answer[0]['phonetics'][0].get('text', 'N/A')
                audio = answer[0]['phonetics'][0].get('audio', '')
                definition = answer[0]['meanings'][0]['definitions'][0].get('definition', 'N/A')
                example = answer[0]['meanings'][0]['definitions'][0].get('example', 'N/A')
                synonyms = answer[0]['meanings'][0]['definitions'][0].get('synonyms', [])

                context = {
                    'form': form,
                    'input': text,
                    'phonetics': phonetics,
                    'audio': audio,
                    'definition': definition,
                    'example': example,
                    'synonyms': synonyms
                }
            except (KeyError, IndexError) as e:
                print(f"Error fetching dictionary data: {e}")
                context = {
                    'form': form,
                    'input': 'No result found'
                }
        else:
            context = {'form': form}
        return render(request, 'dictionary.html', context)

    form = DashboardForm()
    context = {'form': form}
    return render(request, 'dictionary.html', context)

@login_required
def home(request):
    return render(request,'home.html')
@login_required
def homework(request):
    homework = Homework.objects.all()
    # homework = Homework.objects.filter(user=request.user)
    context = {'homeworks':homework}
    return render(request,'homework.html',context)


@login_required
def upload_file(request, homework_id):
    if request.method == 'POST':
        homework = get_object_or_404(Homework, id=homework_id)
        if 'file' in request.FILES:
            homework.file = request.FILES['file']
            homework.status = 'uploaded'  # Update the status to 'uploaded'
            homework.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('homework')
    messages.error(request, 'File upload failed')
    return HttpResponse('File upload failed', status=400)

# @login_required
# def upload_file(request, homework_id):
#     if request.method == 'POST':
#         homework = get_object_or_404(Homework, id=homework_id)
#         if 'file' in request.FILES:
#             homework.file = request.FILES['file']
#             homework.save()
#             messages.success(request, 'File uploaded successfully!')
#             return redirect('homework')  # Change 'homework' to your actual homework list view name
#     messages.error(request, 'File upload failed')
#     return HttpResponse('File upload failed', status=400)

@login_required
def delete_homework(request, homework_id):
    homework = get_object_or_404(Homework, id=homework_id)
    if request.method == 'POST':
        homework.delete()
        return redirect('homework') 
    return HttpResponse('Delete failed', status=400)


@login_required
def login(request):
    return render(request,'login.html')

@login_required
def logout(request):
    return render(request,'logout.html')

@login_required
def profile(request):
    return render(request,'profile.html')


@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            # Create a new note and save it to the database
            note = Notes(
                user=request.user, 
                title=form.cleaned_data['title'], 
                description=form.cleaned_data['description']
            )
            note.save()
            messages.success(request, 'Notes created successfully by {}'.format(request.user))
            return redirect('notes') 
    else:
        form = NotesForm()
   
    notes= Notes.objects.all()
    # notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'notes.html', context)

def delete_notes(request, notes_id):
    notes = get_object_or_404(Notes, id=notes_id)
    notes.delete()
    messages.success(request, 'Notes deleted successfully')
    return redirect('notes') 

class NotesDetailView(generic.DetailView):
    model = Notes
    
def notes_detail(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    context = {'note': note}
    return render(request, 'notes_detail.html', context)

# def profile(request):
#     todos = Todo.objects.filter(is_finished=False,user=request.user)
# if len(todo) == 0:
#     todos_done = True
# else:
#     todos_done = False
# context = {
#     'todos':todo,
#     'todos_done': todos_done
# }
# return render('profile.html',context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account Created for {username}!!")
            return redirect('login')
        else:
            context = {'form': form}
    else:
        form = UserRegistrationForm()
    
    context = {'form': form} 
    
    return render(request, 'register.html', context)



@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                finished = finished == 'on'
            except KeyError:
                finished = False

            todos = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()
            messages.success(request, 'Todo created successfully by {}'.format(request.user))
        else:
            messages.error(request, 'Invalid form submission.')
            form = TodoForm()
    else:
        form = TodoForm()
    
    todo_list = Todo.objects.all()
    # todo_list = Todo.objects.filter(user=request.user)
    context = {
        'form': form,
        'todo': todo_list
    }
    return render(request, 'todo.html', context)

def update_todo(request, pk=None):
    todo = get_object_or_404(Todo, pk=pk)
    todo.is_finished = not todo.is_finished
    todo.save()
    return redirect('todo')

def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    messages.success(request, 'Todo deleted successfully')
    return redirect('todo')
 

@login_required
def wiki(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            try:
                search = wikipedia.page(text)
                context = {
                    'form': form,
                    'title': search.title,
                    'link': search.url,
                    'info': search.summary
                }
            except PageError:
                context = {
                    'form': form,
                    'error': "The requested page does not exist on Wikipedia."
                }
            except DisambiguationError as e:
                context = {
                    'form': form,
                    'error': f"The term '{text}' is ambiguous. Here are some options: {e.options}"
                }
            except WikipediaException as e:
                context = {
                    'form': form,
                    'error': f"An error occurred: {str(e)}"
                }
            return render(request, 'wiki.html', context)
        else:
            context = {
                'form': form
            }
            return render(request, 'wiki.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form
        }
        return render(request, 'wiki.html', context)
    

@login_required
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            video = VideosSearch(text, limit=10)
            result_list = []
            for i in video.result()['result']:
                result_dict = {
                    'input': text,
                    'title': i.get('title'),
                    'duration': i.get('duration'),
                    'thumbnail': i.get('thumbnails', [{}])[0].get('url', ''),
                    'channel': i.get('channel', {}).get('name', ''),
                    'link': i.get('link'),
                    'views': i.get('viewCount', {}).get('short', ''),
                    'published': i.get('publishedTime')
                }
                desc = ''
                if i.get('descriptionSnippet'):
                    for j in i['descriptionSnippet']:
                        desc += j.get('text', '')
                result_dict['description'] = desc
                result_list.append(result_dict)
            
            context = {
                'form': form,
                'results': result_list
            }
            return render(request, 'youtube.html', context)
                    
    else:
        form = DashboardForm()
    
    context = {'form': form}
    return render(request, 'youtube.html', context)


