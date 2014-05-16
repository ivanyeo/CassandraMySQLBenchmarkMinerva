from django.contrib import admin

# Register your models here.

from post.models import Post, Tag, PostTag



class PostAdmin(admin.ModelAdmin):
    #fields = ['text', 'time_created']
    list_display = ('id', 'text', 'time_created')

admin.site.register(Post, PostAdmin)



class TagAdmin(admin.ModelAdmin):
    #fields = ['value', 'time_created']
    list_display = ('value', 'time_created')

admin.site.register(Tag, TagAdmin)



class PostTagAdmin(admin.ModelAdmin):
    #fields = ['pid', 'tid']
    list_display = ('get_pid', 'get_tid')

    def get_pid(self, obj):
        return "(ID: {0}): {1}".format(obj.pid.id, obj.pid.text)

    def get_tid(self, obj):
        return "(ID: {0}): {1}".format(obj.tid.id, obj.tid.value)


admin.site.register(PostTag, PostTagAdmin)

