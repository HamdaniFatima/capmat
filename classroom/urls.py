from django.urls import include, path

from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.home, name='home'),

    path('CapMat/', include(([
        path('Accueil/', students.HomeView.as_view(), name='lanceur_projet_home'),
        path('profile/', students.profile, name='profile'),
        path('visualiser', students.profile_view, name='visualiser_profile'),



        path('projet/add/', students.QuizCreateView.as_view(), name='projet_add'),
        path('projet/<int:pk>/', students.QuizUpdateView.as_view(), name='projet_change'),
        path('projet/<int:pk>/delete/', students.QuizDeleteView.as_view(), name='projet_delete'),
        path('projet/detail/<slug:slug>', students.display_detail, name='projet_detail'),



        path('forum', students.ForumListView, name='forum_list'),
        path('forum/par/<username>/', students.ForumUserListView.as_view(), name='forum-by'),
        path('forum/par/profile/<username>/', students.ProfilUserListView.as_view(), name='forum_by_profile'),
        path('forum/projet/detail/<slug:slug>', students.forum_projet_detail, name='forum_detail'),

        
        path('Capteurs/', students.CapteursView.as_view(), name='capteur_home'),
        path('capteur/add/', students.CapteurCreateView.as_view(), name='capteur_add'),
        path('capteur/<int:pk>/', students.CapteurUpdateView.as_view(), name='capteur_change'),

        path('Potentielles/collaborations', students.CollobarationListView.as_view(), name='collaborations'),
        path('Expert', students.ExpertsListView, name='experts_list'),
        
        
        
        
        
        
        
        
        
        
        path('partager/<int:pk>/', students.Publi_projet, name='publi_projet'),




        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
       
       
        path('', students.QuizListView.as_view(), name='quiz_list'),
    
      
        path('Mes_projet/', students.QuizMesView.as_view(), name='projet_list'),
        path('subject/add/', students.SubjectCreateView.as_view(), name='subject_add'),
      
  
        
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
