from django.db import models
from datetime import date
from datetime import datetime


#раздел информации на wiki, они будут в навигационной панели
class InfoChapter(models.Model):
    ic_name = models.CharField(verbose_name="Название раздела", max_length=300)
    ic_url = models.CharField(verbose_name="Название раздела в url (желательно на EU)", max_length=300)

    def __str__(self) -> str:
        return self.ic_name
    
    class Meta:
        verbose_name = "Раздел на сайте"
        verbose_name_plural = "Раздела на сайте"


#подразделы на сайте, у каждого раздела есть подразделы
#например раздед локации, подразделы (лес, река, шахты)
class InfoSubSection(models.Model):
    infoChapter = models.ForeignKey(InfoChapter, on_delete = models.CASCADE, verbose_name="Раздел информации на wiki")
    iss_name = models.CharField(verbose_name="Название подраздела", max_length=300)
    iss_url = models.CharField(verbose_name="Название подраздела в url (желательно на EU)", max_length=300)
    iss_description = models.TextField(verbose_name="Краткое опсание подраздела", blank=True)


    def __str__(self) -> str:
        return self.iss_name
    
    class Meta:
        verbose_name = "Подраздел на сайте"
        verbose_name_plural = "Подразделы на сайте"


#модель для самих статей о мире или о персонажах 
class Info(models.Model):
    infoSubSection = models.ForeignKey(InfoSubSection, on_delete = models.CASCADE, verbose_name="Подраздел информации на wiki")
    i_name = models.CharField(verbose_name="Название статьи", max_length=300)
    i_img = models.ImageField(verbose_name="Картинка для статьи", upload_to='info_images/', blank=True)
    i_date_creation = models.DateField(verbose_name="Дата создания статьи", default=date.today)
    i_text = models.TextField(verbose_name="Содержание статьи")

    def __str__(self) -> str:
        return self.i_name
    
    class Meta:
        verbose_name = "Статья на сайте"
        verbose_name_plural = "Статьи на сайте"

#материала к статтье, которые будут использоваться в игре (типо спрайта, звуки)
class Material(models.Model):
    info = models.ForeignKey(Info, on_delete = models.CASCADE, verbose_name="Статья на wiki")
    m_name = models.CharField(verbose_name="Название материала (например спрайт, анимаци ходьбы, звук)", max_length=300)
    m_date_add = models.DateField(verbose_name="Дата добавления", default=date.today)
    m_file = models.FileField(verbose_name="Файл материала к статье", upload_to='materials/')

    def __str__(self) -> str:
        return self.m_name
    
    class Meta:
        verbose_name = "Материал к статье на сайте"
        verbose_name_plural = "Материалы к статье на сайте"


#модель для логов дейтсвий с материалами на сайте
class LogMaterials(models.Model):
    m_name  = models.CharField(verbose_name="Название материала (например спрайт, анимаци ходьбы, звук)", max_length=300)
    ml_i_id = models.IntegerField(verbose_name="id статьи к которой идет материал")
    ml_action = models.CharField(verbose_name="Название действия с файлом", max_length=300)
    ml_date_add = models.DateTimeField(verbose_name="Дата", default=datetime.now)
    user_id = models.IntegerField(verbose_name="id пользователя")

