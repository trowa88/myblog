from django.core.urlresolvers import reverse_lazy
from django.db.models.query_utils import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView, \
    TodayArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from tagging.views import TaggedObjectList

from blog.forms import PostSearchForm
from blog.models import Post


# --- TemplateView
from mysite.views import LoginRequiredMixin


class TagTV(TemplateView):
    template_name = 'tagging/tagging_cloud.html'


# --- ListView
class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2


class PostTOL(TaggedObjectList):
    model = Post
    template_name = 'tagging/tagging_post_list.html'


# --- DetailView
class PostDV(DetailView):
    model = Post


# --- ArchiveView
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_date'


class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_date'
    make_object_list = True


class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_date'


class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_date'


class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_date'


# --- FormView
class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = "blog/post_search.html"

    def form_valid(self, form):
        sch_word = '%s' % self.request.POST['search_word']
        post_list = Post.objects.filter(Q(title__icontains=sch_word) |
                                        Q(description__icontains=sch_word) |
                                        Q(content__icontains=sch_word)).distinct()
        context = {
            'form': form,
            'search_term': sch_word,
            'object_list': post_list
        }

        return render(self.request, self.template_name, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    initial = {'slug': 'auto-filling-do-not-input'}
    # fields = ['title', 'description', 'content', 'tag']
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostChangeLV(LoginRequiredMixin, ListView):
    template_name = 'blog/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    success_url = reverse_lazy('blog:index')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
