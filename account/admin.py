from django.contrib import admin
from account.models import CustomUser , CardRequest , CardDetails ,AccountTransaction


admin.site.register(CustomUser)
admin.site.register(CardRequest)
admin.site.register(CardDetails)
admin.site.register(AccountTransaction)



