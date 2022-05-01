from django.contrib import admin
from .models import (
                    User,
                    Doctor,
                    Patient,
                    MedicalHistory,
                    Education,
                    WorkExperience
)

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('id','doctor')


admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(MedicalHistory)
admin.site.register(Education)
admin.site.register(WorkExperience,WorkExperienceAdmin)