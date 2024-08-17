from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect #шорткат, чтобы не использовать HttpResponse и loader
from django.http import Http404 #для обработки ошибки 404
from .models import InfoChapter, InfoSubSection, Info, Material, LogMaterials
from datetime import datetime
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import MaterialForm

#для пагинации
from django.core.paginator import Paginator

#для сохранения файла
from django.core.files.storage import default_storage

#имопртируем доумент для поиска 
from .documents import InfoDocument
from elasticsearch_dsl.query import MultiMatch

#для авторизации 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#для отдачи файла 
from django.http import FileResponse

#логи django взаимодейтсиве пользователей
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User


#Create your views here.


#получение всех разделов и подразделов wiki
def getAllInfoChapterWithSubSection() -> list:
    result = []
    InfoChapters = InfoChapter.objects.all()


    for ic in InfoChapters:
        subs = InfoSubSection.objects.filter(infoChapter__id = ic.id)
        subs_res = []

        for s in subs:
            subs_res.append(
                {
                    "iss_name": s.iss_name,
                    "iss_url": s.iss_url
                }
            )

        result.append(
            {
                "ic_name": ic.ic_name,
                "ic_url": ic.ic_url,
                "ic_subs": subs_res
            }
        )
    return result


#главная страница
@login_required
def index(request):
    #получение разделов сайта
    allInfoChapters = getAllInfoChapterWithSubSection()

    #получаем логи с админ панели
    logs = LogEntry.objects.all() 
    log_res = []

    for l in logs:

        if l.action_flag == 1:
            action = "добавлен"
        elif l.action_flag == 2:
            action = "изменён"
        elif l.action_flag == 3:
            action = "удалён"


        #тип объекта
        type="отсутсвует"
        if l.content_type_id == 4:
            type = "пользователь"
        elif l.content_type_id == 7:
            type = "материал"
        elif l.content_type_id == 8:
            type = "подраздел"
        elif l.content_type_id == 9:
            type = "раздел"
        elif l.content_type_id == 10:
            type = "статьи"
        
        #получаем пользователя, который сделал дейтсвие на сайте
        user = User.objects.filter(pk=l.user_id).first()


        log_res.append({
            "action_flag": action,
            "object_repr": l.object_repr,
            "type" : type,
            "date": l.action_time.strftime("%d.%m.%Y в %H:%M:%S"),
            "user_id": user
        })

    #получаем логи, которые связаны с материалами к статье
    logMaterials = LogMaterials.objects.order_by("-ml_date_add")
    logMres = []

    for lm in logMaterials:
        user = User.objects.filter(pk=lm.user_id).first()
        logMres.append(
            {
                "m_name": lm.m_name,
                "ml_i_id": int(lm.ml_i_id),
                "ml_action": lm.ml_action,
                "ml_date": lm.ml_date_add.strftime("%d.%m.%Y в %H:%M:%S"),
                "user": user
            }
        )

    #пагинация
    paginator = Paginator (log_res, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    #пагинация для материал логов
    paginator_material_log = Paginator(logMres, 5)
    page_number_material_log = request.GET.get("page_material_log")
    page_obj_material_log = paginator_material_log.get_page(page_number_material_log)


    #подсчет сколько статей на сайте
    info_count = len(Info.objects.all())
    #подсчет сколько материалов на сайте
    materials_count = len(Material.objects.all())

    return render(
        request=request, 
        template_name='wiki/index.html',
        context={
            "allInfoChapters": allInfoChapters,
            "logs": log_res,
            "logs_count": len(log_res),
            "page_obj": page_obj,
            "logMres": logMres,
            "logM_count": len(logMres),
            "page_obj_material_log": page_obj_material_log,
            "info_count": info_count,
            "materials_count": materials_count
        }
        )




#получить подразделы нашего раздела
@login_required
def InfoChapterDetails(request, ic_url: str) -> HttpResponse:


    #получение разделов сайта
    allInfoChapters = getAllInfoChapterWithSubSection()

    #информация конкретно о нашем разделе
    infoChapter : dict = {}

    #ищем наш раздел
    for ic in allInfoChapters:
        if ic['ic_url'] == ic_url:
            infoChapter = ic

    #определяем контекст
    context = {
        "allInfoChapters": allInfoChapters,
        "infoChapter": infoChapter
    }

    #воззвращаем HttpResponse
    return render(request=request, context=context, template_name="wiki/infoChapter.html")


#получить информацию о подразделе
@login_required
def InfoSubSectionDetails(request, ic_url: str, iss_url: str) -> HttpResponse:

    #получение разделов сайта
    allInfoChapters = getAllInfoChapterWithSubSection()


    
    #находим информацию о подразделе
    infoSubSection = get_object_or_404(InfoSubSection, iss_url=iss_url)

    #находим все статьи данного раздела
    infos = Info.objects.filter(infoSubSection__id=infoSubSection.id)

    #структурируем информацию о всех статьях данного подраздела
    result_infos : list = []


    for i in infos:
        try:
            img_url = i.i_img.url
        except:
            img_url = False

        result_infos.append({
            "i_id": i.id,
            "i_name": i.i_name,
            "i_img": img_url,
        })

    #воззвращаем HttpResponse
    return render(
        request=request, 
        context={
            "allInfoChapters": allInfoChapters,
            "iss_name": infoSubSection.iss_name,
            "iss_url": infoSubSection.iss_url,
            "iss_description": infoSubSection.iss_description,
            "ic_name": infoSubSection.infoChapter.ic_name,
            "ic_url": ic_url,
            "result_infos": result_infos
        },
        template_name="wiki/InfoSubSection.html"
        )


#получить статью
@login_required
def InfoDetails(request, ic_url: str, iss_url: str, i_id: int) -> HttpResponse:
    #получение разделов сайта
    allInfoChapters = getAllInfoChapterWithSubSection()

    #получаем статью на сайте по её индентификатору
    info = Info.objects.filter(id=i_id).first()

    #получаем все материалы к нашей статье
    materials = Material.objects.filter(info__id=i_id).order_by('-m_date_add')

    #пагинатор
    paginator = Paginator (materials, 5) #будет показывтьа 5 объектов на одной странице 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    #структурируем информацию о всех материалах статьи
    result_materials : list = []
    for m in materials:
        result_materials.append({
            "m_name": m.m_name,
            "m_date_add": m.m_date_add.strftime("%d.%m.%Y"),
            "m_file": m.m_file.url
        })

    try:
        main_img = info.i_img.url
    except:
        main_img = False


    #теперь проверяем какой метод в запросе
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        post = form.save(commit=False)
        post.info = info
        if form.is_valid():

            #добавляем лог о том, что мы добавили материал к статье
            LogMaterials.objects.create(
                m_name=post.m_name, 
                ml_i_id=i_id, 
                ml_action="загружен",
                user_id = request.user.id
            )

            post.save()
            return redirect(request.META['HTTP_REFERER'])
    
    else:
        form = MaterialForm()
    
    #воззвращаем HttpResponse
    return render(
        request=request,
        context={
            "allInfoChapters": allInfoChapters,
            "i_id": i_id,
            "i_name": info.i_name,
            "i_img": main_img,
            "i_date_creation": info.i_date_creation.strftime("%d.%m.%Y"),
            "i_text": info.i_text,
            "materials": result_materials,
            "iss_url": iss_url,
            "ic_url": ic_url,
            "form": form,
            "page_obj": page_obj
        },
        template_name="wiki/Info.html"
    )


#удаление материала к записи
@login_required
def deleteMaterial(request,ic_url, iss_url, i_id, m_id):
    #получение разделов сайта
    allInfoChapters = getAllInfoChapterWithSubSection()

    material = get_object_or_404(Material, pk=m_id)

    info = get_object_or_404(Info, pk=i_id)

    if request.method == 'POST':
        Material.objects.get(pk=m_id).delete()

        #добавляем лог о том, что мы добавили материал к статье
        LogMaterials.objects.create(
            m_name=material.m_name, 
            ml_i_id=i_id, 
            ml_action="удалён",
            user_id = request.user.id
        )

        return HttpResponseRedirect(reverse("wiki:InfoDetails", args=(ic_url, iss_url, i_id)))

    return render(
        request=request,
        context={
            "allInfoChapters": allInfoChapters,
            "ic_url": ic_url,
            "iss_url": iss_url,
            "i_id": i_id,
            "m_id": m_id,
            "m_name": material.m_name,
            "m_date_add": material.m_date_add.strftime("%d.%m.%Y"),
            "m_file": material.m_file.url,
            "i_name": info.i_name
        },
        template_name="wiki/deleteMaterial.html"
    )

#функция предсталвения рещультатов поиска 
@login_required
def searh(request) -> HttpResponse:
    #получение разделов сайта
    allInfoChapters = getAllInfoChapterWithSubSection()

    results_info = []

    if request.method == 'GET' and request.GET['q']:
        searh_query = request.GET['q']

        #multimatch query
        query = MultiMatch(query=searh_query, fields=["i_name", "i_text", ], fuzziness="AUTO")
        results_elastic = InfoDocument.search().query(query)

        for re in results_elastic:
            results_info.append(
                {
                    "id": re.meta.id,
                    "i_name": re.i_name,
                    "i_text": re.i_text
                }
            )

    else:
        infos = Info.objects.order_by("i_name")

        searh_query = "Ты бля нихуя не ввел, поэтому лови все статьти"
        
        for i in infos:
            results_info.append({
              "id": i.pk,
              "i_name": i.i_name,
              "i_text": i.i_text
            })


    return render(
        request=request,
        context={
            "allInfoChapters": allInfoChapters,
            "searh_query": searh_query,
            "results_info": results_info
        },
        template_name="wiki/search_result.html"
    )

#результаты поиска
@login_required
def result_search(request, i_id: int):
    #получаем статью на сайте по её индентификатору
    info = get_object_or_404(Info, pk=i_id)

    #получаем подраздел
    infoSubSection = info.infoSubSection
    iss_url = infoSubSection.iss_url

    #получаем раздел 
    InfoChapter = infoSubSection.infoChapter
    ic_url = InfoChapter.ic_url

    return HttpResponseRedirect(reverse("wiki:InfoDetails", args=(ic_url, iss_url, i_id)))

#представление для авторизации пользователя
def login_wiki(request):

    if request.method == "POST":
        username = request.POST['login']
        password = request.POST['password']

        user = authenticate(request=request,username=username, password=password)
        #проверка на существование пользователя
        if user is not None:
            #входим
            login(request, user=user)
            #делаем редирект на гланую страницу
            return HttpResponseRedirect(reverse("wiki:index"))

    return render(
        request=request,
        context={

        },
        template_name='wiki/login.html'
    )

#представление для выхода
def logout_wiki(request):
        logout(request)
        return render(
        request=request,
        context={

        },
        template_name='wiki/login.html'
    )

#доступ к файлам, только для авторизированных пользователей
@login_required
def secure_file(request, filename):
    #получили файл
    obj = Material.objects.filter(m_file=f'materials/{filename}').first()
    #отдача файла
    if obj:
        return FileResponse(obj.m_file)