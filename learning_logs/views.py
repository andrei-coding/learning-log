from django.shortcuts import render, redirect
from .models import Topic, Entry
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from .forms import TopicForm, EntryForm
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    """PAGINA PRINCIPAL DO LEARNING_LOGS"""
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    """ TOPICOS DO LEARNING LOGS"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_Added')
    context = {'topics' : topics}
    return render(request, 'learning_logs/topics.html', context)
@login_required
def topic(request, topic_id):
    """ Unico um unico assunto e todas suas entradas"""
    try:
        # Tenta buscar o tópico pelo ID
        topic = Topic.objects.get(id=topic_id)
        if topic.owner != request.user:
            raise Http404
        
        entries = topic.entry_set.order_by('-date_Added')
        context = {'topic' : topic, 'entries': entries, 'error_message':'Sem Registro'}
    except Topic.DoesNotExist:
        # Se não encontrar, envia mensagem de erro para o template
        context = {'topic': 'Sem Registro', 'error_message': "Tópico não existe."}
    return render(request, 'learning_logs/topic.html', context)
@login_required
def new_topic(request):
    """Adiciona um novo assunto."""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
@login_required
def new_entry(request, topic_id):
    """Acrescenta uma nova entrada para um assunto em especifico."""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
            raise Http404
    if request.method != 'POST':
        #nenhum dado submetido cria um formulario em branco 
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_ent = form.save(commit=False)
            new_ent.topic = topic 
            new_ent.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
        
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edita uma entrada existente."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        #Requisição Inicial:Preenche previamente com a entrada atual.
        form = EntryForm(instance=entry)
    else:
        #Após inserçao dos dados:processa os dados
        form= EntryForm(instance=entry, data=request.POST)

        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    
    context = {'entry': entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)