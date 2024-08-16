from django.contrib import admin
from django import forms #для CKEditor
from .models import InfoChapter, InfoSubSection, Info, Material
from ckeditor_uploader.widgets import CKEditorUploadingWidget #для CKEditor


@admin.register(InfoChapter)
class InfoChapterAdmin(admin.ModelAdmin):
    list_display = ("ic_name", "ic_url",)
    search_fields = ("ic_name", "ic_url",)
    save_on_top = True
    save_as = True


@admin.register(InfoSubSection)
class InfoSubSectionAdmin(admin.ModelAdmin):
    list_display = ("iss_name", "iss_url",)
    search_fields = ("iss_name", "iss_url",)
    list_filter = ("infoChapter",)
    save_on_top = True
    save_as = True  


#подключение CKEditor для того, чтобы интегрировать его в форму
class IndfoTextForm(forms.ModelForm):
    i_text = forms.CharField(label="Содержание статьи", widget=CKEditorUploadingWidget())

    class Meta:
        model = Info
        fields = '__all__'


@admin.register(Info) 
class InfoAdmin(admin.ModelAdmin):
    list_display = ("i_name", "i_date_creation",)
    search_fields = ("i_name", "i_date_creation",)
    list_filter = ("infoSubSection",)
    form = IndfoTextForm
    save_on_top = True
    save_as = True


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("m_name", "m_date_add",)
    search_fields = ("m_name", "m_date_add",)
    save_on_top = True
    save_as = True
    
