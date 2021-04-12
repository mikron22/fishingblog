from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from blog.models import Post, UserProfile
from blog.forms import RegisterForm, CommentForm
from blog.utils import ErrorMessageMixin

#region Auth

class InteractiveLoginView(SuccessMessageMixin, ErrorMessageMixin, LoginView):
    success_message = "Logowanie zakończone pomyślnie"
    error_message = "Logowanie nie udało się, sprawdź poprawność wpisanych danych i spróbuj ponownie."


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            image = form.cleaned_data.get('image')
            print(image)
            if image:
                print("saving image")
                user.refresh_from_db()
                user.userprofile.image = image
            print("saved picture")
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Rejestracja przebiegła pomyślnie!')
            return redirect('post-list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

#endregion

#region Profile

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile

    def get_object(self, queryset=None):
        try:
            user = User.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg)).first()
            return user.userprofile
        except:
            return self.request.user.userprofile
    
#endregion

#region Post

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-created_at'
    paginate_by = 10

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, ErrorMessageMixin, CreateView):
    model = Post
    fields = ['title', 'text', 'image']
    success_message = "Udało się dodać nowy wpis!"
    error_message = "Nie udało się stworzyć wpisu, sprawdź poprawność wprowadzonych danych."
    success_url="/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser

class PostDisplayView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDisplayView, self).get_context_data(**kwargs)
        context['form'] = CommentForm
        return context

class CommentCreateView(SingleObjectMixin, SuccessMessageMixin, ErrorMessageMixin, FormView):
    template_name = "blog/post_detail.html"
    form_class = CommentForm
    model = Post

    success_message = "Pomyślnie dodano nowy komentarz!"
    error_message = "Nie udało się dodać komentarza, spróbuj ponownie później."

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CommentCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        print("saving")
        comment = form.save(commit=False)
        comment.created_by = self.request.user
        comment.post = self.object
        comment.save()
        return super(CommentCreateView, self).form_valid(form)


class PostDetailView(LoginRequiredMixin, DetailView):

    def get(self, request, *args, **kwargs):
        view = PostDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentCreateView.as_view()
        return view(request, *args, **kwargs)
    

#endregion
