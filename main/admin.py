from django.contrib import admin

from .models import Profile, ProfileImage, Task, Doc, DocsImage, OtherDoc, ObjectDoc, CustomerDoc, BasicData, \
    BasicDataModel, RentEstimateModel, RentEstimate1, CharacteristicsRE1, RentEstimate2


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'mark_done',
        'is_done',
    )


admin.site.register(Profile)
admin.site.register(ProfileImage)
admin.site.register(Task, TaskAdmin)
admin.site.register(Doc)
admin.site.register(DocsImage)
admin.site.register(ObjectDoc)
admin.site.register(OtherDoc)
admin.site.register(CustomerDoc)
admin.site.register(BasicData)
admin.site.register(BasicDataModel)
admin.site.register(RentEstimateModel)
admin.site.register(RentEstimate1)
admin.site.register(RentEstimate2)
admin.site.register(CharacteristicsRE1)
