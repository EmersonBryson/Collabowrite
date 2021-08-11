from django.shortcuts import render, redirect
from . models import User, Board, Section, Post
from django.contrib import messages
import bcrypt, datetime

# Create your views here.

# Login and Registration

def index(request):
    if 'logged_user' in request.session:
        return redirect('/directory')
    return render(request, 'index.html')

def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        user_name = request.POST['user_name'],
        email = request.POST['email'],
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    )
    request.session['logged_user'] = new_user.id
    return redirect('/directory')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.filter(user_name = request.POST['user_name'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['logged_user'] = logged_user.id
    return redirect('/directory')

def logout(request):
    request.session.clear()
    return redirect('/')

# Directory and Topics

def directory(request):
    if 'logged_user' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id = request.session['logged_user']),
    }
    return render(request, 'directory.html', context)

def topic(request, topic):
    if 'logged_user' not in request.session:
        return redirect('/')
    if topic == "sciencefiction":
        topic_name = "Science Fiction"
    elif topic == "childrensliterature":
        topic_name = "Children's Literature"
    elif topic =='mystery&crime':
        topic_name = "Mystery & Crime"
    elif topic == "youngadult":
        topic_name = "Young Adult"
    elif topic == "biography&memoirs":
        topic_name = "Biography & Memoirs"
    elif topic == "academic&philosophy":
        topic_name = "Academic & Philosophy"
    elif topic == "selfhelp&instruction":
        topic_name = "Self-help & Instruction"
    elif topic == "humor&commentary":
        topic_name = "Humor & Commentary"
    elif topic == "help&questions":
        topic_name = "Help & Questions"
    elif topic == "general&offtopic":
        topic_name = "General & Off-Topic"
    elif topic == "suggestions&bugs":
        topic_name = "Suggestions & Bugs"
    else:
        topic_name = topic
    context = {
        'user': User.objects.get(id = request.session['logged_user']),
        'my_boards': Board.objects.filter(user = request.session['logged_user'], board_topic = topic),
        'all_boards': Board.objects.filter(board_topic = topic).exclude(user = request.session['logged_user']),
        'topic_data': {
            'display_name': topic_name,
            'original_name': topic,
        }
    }
    
    return render(request, 'topics.html', context)

def create_board(request):
    if request.method == 'GET':
        return redirect('/')
    errors = Board.objects.board_validator(request.POST)
    topic = request.POST['board_topic']
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/topic/{topic}')
    else:

        logged_user = User.objects.get(id=request.session['logged_user'])
        new_board = Board.objects.create(
            user = logged_user,
            board_title= request.POST['board_title'],
            board_topic= request.POST['board_topic'],
            board_tags = request.POST['board_tags'],
            board_image = request.POST['board_image'],
        )
    return redirect(f'/topic/{topic}')

# Individual Board View

def display_board(request, board_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    this_board = Board.objects.get(id= board_id)
    context = {
        'user': User.objects.get(id= request.session['logged_user']),
        'this_board': Board.objects.get(id= board_id),
        'sections': Section.objects.filter(board= this_board.id),
        'posts': Post.objects.all(),
    }
    return render(request, 'boards.html', context)
        
def create_section(request):
    if request.method == 'GET':
        return redirect('/')
    logged_user = User.objects.get(id=request.session['logged_user'])
    current_board_id = request.POST['board']
    this_board = Board.objects.get(id=current_board_id)
    new_section = Section.objects.create(
        user = logged_user,
        section_title = request.POST['section_title'],
        section_summary = request.POST['section_summary'],
        board = this_board,
    )
    return redirect(f'/board/{current_board_id}')

def delete_section(request, board_id, section_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    else:
        current_board = Board.objects.get(id= board_id)
        section_to_delete = Section.objects.get(id= section_id)
        section_to_delete.delete()
        return redirect(f'/board/{current_board.id}')

def display_create_post(request, board_id, section_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    else:
        context={
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'current_board': Board.objects.get(id= board_id),
        'current_section': Section.objects.get(id= section_id),
        }
        return render(request, 'createPost.html', context)

def create_post(request):
    if'logged_user' not in request.session:
        return redirect('/')
    else:
        section = request.POST['section']
        board = request.POST['board']
        current_board = Board.objects.get(id = board)
        current_section = Section.objects.get(id = section)
        user = User.objects.get(id=request.session['logged_user'])
        new_post = Post.objects.create(
            user = user,
            section = current_section,
            post_title = request.POST['post_title'],
            post_content = request.POST['post_content'],
        )
        return redirect(f'/board/{current_board.id}')

def delete_board(request, board_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    else:
        board_to_delete = Board.objects.get(id= board_id)
        topic = board_to_delete.board_topic
        board_to_delete.delete()
        return redirect(f'/topic/{topic}')

def display_post(request, board_id, post_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    else:
        context={
            'logged_user': User.objects.get(id=request.session['logged_user']),
            'current_board': Board.objects.get(id= board_id),
            'current_post': Post.objects.get(id= post_id),
        }
        return render(request, 'displayPost.html', context)

def delete_post(request, board_id, post_id):
    if 'logged_user' not in request.session:
        return redirect('/')
    else:
        post_to_delete = Post.objects.get(id= post_id)
        board = Board.objects.get(id= board_id),
        post_to_delete.delete()
        return redirect(f'/board/{board.id}')
