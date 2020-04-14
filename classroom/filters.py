import django_filters
from classroom.models import Quiz, Profile

class CasesFilter (django_filters.FilterSet):
    class Meta:
        model = Quiz
        fields = [ 'subject',]



class ExpertsFilter (django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = [ 'interests',]