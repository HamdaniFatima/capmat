from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django import forms
from ..decorators import student_required
from ..forms import StudentSignUpForm, TakeQuizForm, UserUpdateForm, ProfileUpdateForm , SubjectForm, StudentInterestsForm, CommentForm
from ..models import Capteur, Quiz,Forum, Student, TakenQuiz, User, Subject, Profile,Comment
from  classroom.filters import CasesFilter, ExpertsFilter


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:lanceur_projet_home')



@method_decorator([login_required, student_required], name='dispatch')
class HomeView(ListView):
    model = Quiz
    ordering = ('created_at', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/home_page.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes  \
            .select_related() 
        return queryset




@method_decorator([login_required, student_required], name='dispatch')
class CapteurCreateView(CreateView):
    model = Capteur
    fields =('nom_capteur', 'description_projet','type_capteur','subject', 'type_evt', 'nature_evt', 'grandeur_evt', 'envirennoment_evt','type_capteur','domaine_utilisation','technologie_utilisee', 'etendue','sensibilite','resolution', 'precision', 'rapidite', 'justesse','reproductibilite', 'temps_de_reponse','bande_passante','hysteresis', 'gamme_temperature','file_1', 'file_2', 'file_3','confidentalite',)
    template_name = 'classroom/students/capteurs/capteur_add.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'The projet was created with success!' )
        return redirect('students:capteur_home')




@method_decorator([login_required, student_required], name='dispatch')
class CapteurUpdateView(UpdateView):
    model = Capteur
    fields =('nom_capteur','description_projet', 'type_capteur','subject', 'type_evt', 'nature_evt', 'grandeur_evt', 'envirennoment_evt','type_capteur','domaine_utilisation','technologie_utilisee', 'etendue','sensibilite','resolution', 'precision', 'rapidite', 'justesse','reproductibilite', 'temps_de_reponse','bande_passante','hysteresis', 'gamme_temperature','file_1', 'file_2', 'file_3','confidentalite',)
    context_object_name = 'quiz'
    template_name = 'classroom/students/capteurs/capteur_change_form.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.capteurs.all()

    def get_success_url(self):
        return reverse('students:capteur_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, student_required], name='dispatch')
class CapteursView(ListView):
    model = Capteur
    context_object_name = 'quizzes'
    template_name = 'classroom/students/capteurs/home_page.html'


    def get_queryset(self):
        queryset = self.request.user.capteurs  \
            .select_related() 
        return queryset





@method_decorator([login_required, student_required], name='dispatch')
class CollobarationListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/collaboration/home_page.html'

    def get_queryset(self):
        student = self.request.user.profile
        student_interests = student.interests.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) 
        return queryset



def ExpertsListView(request):
    case_list = Profile.objects.all()
    case_filter = ExpertsFilter(request.GET, queryset = case_list)
    template_name = 'classroom/students/collaboration/experts_list.html'
    return render(request, template_name, {'filter' : case_filter})




@method_decorator([login_required, student_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    fields =('titre_projet', 'description_projet','subject', 'type_evt', 'nature_evt', 'grandeur_evt', 'envirennoment_evt','type_capteur', 'etendue','sensibilite','resolution', 'precision', 'rapidite', 'dimensions','finance','file_1', 'file_2', 'file_3','confidentalite',)
    template_name = 'classroom/students/quiz_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'The projet was created with success!')
        return redirect('students:lanceur_projet_home')





@method_decorator([login_required, student_required], name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    fields =('titre_projet', 'description_projet','subject', 'type_evt', 'nature_evt', 'grandeur_evt', 'envirennoment_evt','type_capteur', 'etendue','sensibilite','resolution', 'precision', 'rapidite', 'dimensions','finance','file_1', 'file_2', 'file_3','confidentalite',)
    context_object_name = 'quiz'
    template_name = 'classroom/students/quiz_change_form.html'


    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('students:projet_change', kwargs={'pk': self.object.pk})




@login_required
def display_detail(request, slug):
    template_name = 'classroom/students/display_projet.html'
    post = get_object_or_404(Quiz, slug=slug)
    comments = post.comments.all()
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})


@method_decorator([login_required, student_required], name='dispatch')
class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'classroom/students/quiz_delete_confirm.html'
    success_url = reverse_lazy('students:lanceur_projet_home')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Profile
    form_class = StudentInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:lanceur_projet_home')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.profile
        student_interests = student.interests.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(subject__in=student_interests) 
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Profile
    form_class = StudentInterestsForm
    template_name = 'classroom/students/interests_form.html'
    success_url = reverse_lazy('students:quiz_list')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizMesView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/students/projet_list.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('subject') 
        return queryset








@method_decorator([login_required, student_required], name='dispatch')
class SubjectCreateView(CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'classroom/students/subject_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.save()
        return redirect('students:subject_add')











@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'classroom/students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__subject') \
            .order_by('quiz__name')
        return queryset




@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 50.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! You completed the quiz %s with success! You scored %s points.' % (quiz.name, score))
                    return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'classroom/students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })




@login_required
def profile(request):


    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('students:profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'classroom/students/user/profile.html', context)





@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.domaine_profile.add(*self.cleaned_data.get('domaine_profile'))
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
     
    }

    return render(request, 'classroom/students/user/display_profile.html', context)














class ForumUserListView(ListView):
    template_name = 'classroom/students/forums/forum_by_user.html'
    def get_queryset(self):
        self.user = get_object_or_404(User, username = self.kwargs['username'])
        return Quiz.objects.filter(owner = self.user)



class ProfilUserListView(ListView):
    model = Quiz
    template_name = 'classroom/students/forums/profile_by_user.html'
    context_object_name  = "objForums"
    def get_queryset(self):
        self.user = get_object_or_404(User, username = self.kwargs['username'])
        return Profile.objects.filter(user = self.user)






def ForumListView(request):
    case_list = Quiz.objects.filter(confidentalite=False).order_by('-created_at')
    case_filter = CasesFilter(request.GET, queryset = case_list)
    template_name = 'classroom/students/forums/forum_list.html'
    return render(request, template_name, {'filter' : case_filter})







def forum_projet_detail(request, slug):
    template_name = 'classroom/students/forums/forum_post.html'
    post = get_object_or_404(Quiz, slug=slug)
    comments = post.comments.all()
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})





















@login_required
@student_required
def Publi_projet(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    
    try:
           newSummary = Forum(post=quiz)

           newSummary.save()
    except quiz.DoesNotExist:
            raise Http404('Le projet does not exist')

    return render(request, 'classroom/students/home_page.html' )




