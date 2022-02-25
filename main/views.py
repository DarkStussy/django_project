import math
from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from datetime import date

# auth
from django.urls import reverse

from django_project.settings import DEFAULT_FROM_EMAIL
from .forms import UserRegistrationForm, UserForm, ProfileUpdateImageForm, ProfileUpdatePNumberForm, \
    BasicDataForm
from .models import ProfileImage, Profile, Task, Doc, DocsImage, OtherDoc, ObjectDoc, CustomerDoc, BasicDataModel, \
    BasicData, RentEstimateModel, RentEstimate1, CharacteristicsRE1, RentEstimate2


def login_user(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error = 'Login or password is incorrect'

    return render(request, 'main/login_user.html', {'error': error})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile_image = ProfileImage.objects.create(user=new_user)
            profile_image.save()
            profile_user = Profile.objects.create(user=new_user, phone_number='+')
            profile_user.save()
            return render(request, 'main/main.html')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'main/register.html', {'user_form': user_form})


@login_required(login_url='/accounts/loginuser/')
def profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        pi_form = ProfileUpdateImageForm(request.POST, request.FILES, instance=request.user.profileimage)
        pn_form = ProfileUpdatePNumberForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and pn_form.is_valid():
            user_form.save()
            pn_form.save()
            messages.success(request, 'Your profile has been saved successfully!')
        elif pi_form.is_valid():
            pi_form.save()
            messages.success(request, 'Ваша аватарка успешно изменена!')
        else:
            messages.error(request, 'Unable to complete request')
        return redirect("profile")
    user_form = UserForm(instance=request.user)
    pass_form = PasswordChangeForm(user=request.user)
    pi_form = ProfileUpdateImageForm(instance=request.user.profileimage)
    pn_form = ProfileUpdatePNumberForm(instance=request.user.profile)
    return render(request=request, template_name="main/profile.html", context={"user": request.user,
                                                                               "user_form": user_form,
                                                                               "pass_form": pass_form,
                                                                               "pi_form": pi_form,
                                                                               "pn_form": pn_form})


def main(request):
    return render(request, 'main/main.html')


@login_required(login_url='/accounts/loginuser/')
def home(request):
    tasks = Task.objects.all()
    return render(request, 'main/home.html', {'tasks': tasks})


@login_required(login_url='/accounts/loginuser/')
def detail_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        if task.user is None:
            task.user = request.user
            task.save()
            return HttpResponseRedirect(reverse('detail-task', args=(task_id,)))

        if request.user.has_perm('main.view_task'):
            task.is_done = True
            task.save()
            messages.success(request, 'Задача проверена и отмечена выполненной')
            return redirect('home')
        else:
            task.mark_done = True
            task.save()
            messages.success(request, 'Задача отмечена выполненной')
            return redirect('home')

    if task.user != request.user and not request.user.has_perm('main.view_task'):
        messages.error(request, 'Задача уже выполняется кем-то!')
        return redirect('home')

    return render(request, 'main/detail_task.html', {'task': task})


@login_required(login_url='/accounts/loginuser/')
def docs_view(request):
    docs = Doc.objects.all()
    return render(request, 'main/docs.html', {'docs': docs})


@login_required(login_url='/accounts/loginuser/')
def detail_docs(request, docs_id):
    doc = get_object_or_404(Doc, pk=docs_id)
    images = DocsImage.objects.filter(doc=doc).all()
    c_docs = CustomerDoc.objects.filter(doc=doc).all()
    other_docs = OtherDoc.objects.filter(doc=doc).all()
    obj_docs = ObjectDoc.objects.filter(doc=doc).all()

    doc.is_filled = all([images, c_docs, other_docs, obj_docs])
    doc.save()

    if request.method == 'POST':
        images_ = request.FILES.getlist('image_field')
        c_docs_ = request.FILES.getlist('customer_docs_field')
        other_docs_ = request.FILES.getlist('other_docs_field')
        obj_docs_ = request.FILES.getlist('objects_field')
        if images_:
            for image in images_:
                image_model = DocsImage.objects.create(doc=doc, image_field=image)
                image_model.save()
            messages.success(request, 'Фотографии загружены!')
        elif c_docs_:
            for c_doc in c_docs_:
                c_doc_model = CustomerDoc.objects.create(doc=doc, file_field=c_doc)
                c_doc_model.save()
            messages.success(request, 'Документы заказчика загружены!')
        elif other_docs_:
            for o_doc in other_docs_:
                o_doc_model = OtherDoc.objects.create(doc=doc, file_field=o_doc)
                o_doc_model.save()
            messages.success(request, 'Иные документы загружены!')
        elif obj_docs_:
            for obj_doc in obj_docs_:
                obj_doc_model = ObjectDoc.objects.create(doc=doc, file_field=obj_doc)
                obj_doc_model.save()
            messages.success(request, 'Объекты-аналоги загружены!')

        return HttpResponseRedirect(reverse('detail-docs', args=(docs_id,)))

    return render(request, 'main/detail_docs.html',
                  {'doc': doc, 'images': images, 'c_docs': c_docs, 'other_docs': other_docs, 'obj_docs': obj_docs})


@login_required(login_url='/accounts/loginuser/')
def delete_docs_images(request, docs_id):
    doc = get_object_or_404(Doc, pk=docs_id)
    if (doc.task.user == request.user) or request.user.has_perm('main.view_task'):
        DocsImage.objects.filter(doc=doc).delete()
        return HttpResponseRedirect(reverse('detail-docs', args=(docs_id,)))
    else:
        raise PermissionError


@login_required(login_url='/accounts/loginuser/')
def delete_docs_customer(request, docs_id):
    doc = get_object_or_404(Doc, pk=docs_id)
    if (doc.task.user == request.user) or request.user.has_perm('main.view_task'):
        CustomerDoc.objects.filter(doc=doc).delete()
        return HttpResponseRedirect(reverse('detail-docs', args=(docs_id,)))
    else:
        raise PermissionError


@login_required(login_url='/accounts/loginuser/')
def delete_docs_other(request, docs_id):
    doc = get_object_or_404(Doc, pk=docs_id)
    if (doc.task.user == request.user) or request.user.has_perm('main.view_task'):
        OtherDoc.objects.filter(doc=doc).delete()
        return HttpResponseRedirect(reverse('detail-docs', args=(docs_id,)))
    else:
        raise PermissionError


def delete_docs_obj(request, docs_id):
    doc = get_object_or_404(Doc, pk=docs_id)
    if (doc.task.user == request.user) or request.user.has_perm('main.view_task'):
        doc = get_object_or_404(Doc, pk=docs_id)
        ObjectDoc.objects.filter(doc=doc).delete()
        return HttpResponseRedirect(reverse('detail-docs', args=(docs_id,)))
    else:
        raise PermissionError


@login_required(login_url='/accounts/loginuser/')
def help_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            send_mail(f'{subject} от {DEFAULT_FROM_EMAIL}', message,
                      DEFAULT_FROM_EMAIL, [f'{request.user.email}'])
        except BadHeaderError:
            messages.error(request, 'Ошибка в теме письма.')

        messages.success(request,
                         'Сообщение успешно отправлено техподдержке. В скором времени поступит ответ на вашу почту.')
        return redirect('home')
    else:
        return render(request, 'main/help.html')


@login_required(login_url='/accounts/loginuser/')
def show_basic_data(request):
    basic_data = BasicDataModel.objects.all()
    return render(request, 'main/basic_data.html', {'basic_data': basic_data})


@login_required(login_url='/accounts/loginuser/')
def detail_basic_data(request, d_id):
    bd_model = get_object_or_404(BasicDataModel, pk=d_id)
    if (bd_model.task.user == request.user) or request.user.has_perm('main.view_task'):
        if not bd_model.is_filled:
            if request.method == 'POST':
                bd_form = BasicDataForm(request.POST, request.FILES)
                if bd_form.is_valid():
                    bd_form.save()
                    bd_model = get_object_or_404(BasicDataModel, pk=d_id)
                    bd_model.is_filled = True
                    bd_model.save()
                    messages.success(request, 'Форма успешно заполнена!')
                    return redirect('show-basic-data')
                else:
                    messages.error(request, 'Форма неверно заполнена!')
                    return redirect('show-basic-data')

            bd_form = BasicDataForm(initial={'bd_model': bd_model})
            return render(request, 'main/detail_basic_data.html',
                          {'bd_form': bd_form})
        else:
            basic_data = BasicData.objects.filter(bd_model=bd_model).last()
            return render(request, 'main/detail_bd_filled.html', {'basic_data': basic_data})
    else:
        raise PermissionError


def main_rent_estimates(request):
    re_model = RentEstimateModel.objects.all()
    return render(request, 'main/main_rent_estimates.html', {'re_model': re_model})


def show_rent_estimate1(request, re_id):
    re_model = get_object_or_404(RentEstimateModel, pk=re_id)
    characteristics_t1 = CharacteristicsRE1.objects.filter(re_model=re_model).last()
    tables1 = RentEstimate1.objects.filter(re_model=re_model).all()

    if request.method == 'POST':
        location = request.POST.get('location')
        area = request.POST.get('area')
        price = request.POST.get('price')
        info_resource = request.POST.get('info_resource')
        if location and area and price and info_resource:
            offer_price = round(float(price) / float(area), 2)
            rent_estimate1 = RentEstimate1.objects.create(re_model=re_model, location=location, area=area, price=price,
                                                          offer_price=offer_price, info_resource=info_resource,
                                                          date=date.today(), ad_number=randint(0, 1000))
            rent_estimate1.save()
            rent_estimate2 = RentEstimate2.objects.filter(re_model=re_model).all()
            rent_estimate2.delete()
            re_model.is_filled = False
            re_model.save()

            calculate_characteristics(tables1, characteristics_t1)

            messages.success(request, 'Таблица заполнена!')
            return HttpResponseRedirect(reverse('show-rent-estimate1', args=(re_id,)))
        else:
            messages.error(request, 'Поля неверно заполнены!')
            return HttpResponseRedirect(reverse('show-rent-estimate1', args=(re_id,)))

    return render(request, 'main/rent_estimate1.html',
                  {'re_model': re_model, 'tables1': tables1, 'characteristics_t1': characteristics_t1})


def show_rent_estimate2(request, re_id):
    re_model = get_object_or_404(RentEstimateModel, pk=re_id)
    tables1 = RentEstimate1.objects.filter(re_model=re_model).all()
    tables2 = RentEstimate2.objects.filter(re_model=re_model).all()
    amount_tables1 = tables1.all().count() + 1

    if request.method == 'POST':
        for counter in range(1, tables1.count() + 1):
            transferable_property_rights = request.POST.get(f't_p_rights{counter}')
            financing_conditions = request.POST.get(f'financing_conditions{counter}')
            terms_of_sale = request.POST.get(f'terms_of_sale{counter}')
            price_change = request.POST.get(f'price_change{counter}')
            bargain_discount = request.POST.get(f'bargain_discount{counter}')
            type_of_use = request.POST.get(f'type_of_use{counter}')
            locality_status = request.POST.get(f'locality_status{counter}')
            location_within_city = request.POST.get(f'location_within_city{counter}')
            location_relative_to_red_line = request.POST.get(f'location_relative_to_red_line{counter}')
            proximity_public_transport = request.POST.get(f'proximity_public_transport{counter}')
            parking_type = request.POST.get(f'parking_type{counter}')
            object_access = request.POST.get(f'object_access{counter}')
            area_category = request.POST.get(f'area_category{counter}')
            object_type = request.POST.get(f'object_type{counter}')
            level = request.POST.get(f'level{counter}')
            separate_entrance = request.POST.get(f'separate_entrance{counter}')
            object_quality_class = request.POST.get(f'object_quality_class{counter}')
            object_state = request.POST.get(f'object_state{counter}')
            finish_condition = request.POST.get(f'finish_condition{counter}')
            economic_characteristics = request.POST.get(f'economic_characteristics{counter}')
            movable_property = request.POST.get(f'movable_property{counter}')
            other_characteristics = request.POST.get(f'other_characteristics{counter}')

            rent_estimate2 = RentEstimate2.objects.create(re_model=re_model,
                                                          rent_estimate1=tables1[counter - 1],
                                                          transferable_property_rights=transferable_property_rights,
                                                          financing_conditions=financing_conditions,
                                                          terms_of_sale=terms_of_sale,
                                                          price_change=price_change,
                                                          bargain_discount=bargain_discount,
                                                          type_of_use=type_of_use,
                                                          locality_status=locality_status,
                                                          location_within_city=location_within_city,
                                                          location_relative_to_red_line=location_relative_to_red_line,
                                                          proximity_public_transport=proximity_public_transport,
                                                          parking_type=parking_type,
                                                          object_access=object_access,
                                                          area_category=area_category,
                                                          object_type=object_type,
                                                          level=level,
                                                          separate_entrance=separate_entrance,
                                                          object_quality_class=object_quality_class,
                                                          object_state=object_state,
                                                          finish_condition=finish_condition,
                                                          economic_characteristics=economic_characteristics,
                                                          movable_property=movable_property,
                                                          other_characteristics=other_characteristics
                                                          )
            rent_estimate2.save()
        re_model.is_filled = True
        re_model.save()
        messages.success(request, 'Таблица заполнена!')
        return HttpResponseRedirect(reverse('show-rent-estimate2', args=(re_id,)))

    return render(request, 'main/rent_estimate2.html',
                  {'re_model': re_model, 'tables1': tables1, 'tables2': tables2, 'amount_tables1': amount_tables1})


def delete_tables(request, re_id, table_id):
    re_model = get_object_or_404(RentEstimateModel, pk=re_id)
    characteristics_t1 = CharacteristicsRE1.objects.filter(re_model=re_model).last()
    tables1 = RentEstimate1.objects.filter(re_model=re_model).all()

    if request.method == 'POST':
        table = get_object_or_404(RentEstimate1, pk=table_id)
        table.delete()
        rent_estimate2 = RentEstimate2.objects.filter(re_model=re_model).all()
        rent_estimate2.delete()
        re_model.is_filled = False
        re_model.save()
        calculate_characteristics(tables1, characteristics_t1)
        return HttpResponseRedirect(reverse('show-rent-estimate1', args=(re_id,)))

    return render(request, 'main/delete_tables.html', {'re_model': re_model})


def calculate_characteristics(tables, characteristics_t):
    offer_prices = [el.offer_price for el in tables]
    if len(offer_prices) == 0:
        characteristics_t.least_offer_price = 0
        characteristics_t.greatest_offer_price = 0
        characteristics_t.mid_range = 0
        characteristics_t.average = 0
        characteristics_t.median = 0
        characteristics_t.standard_deviation = 0
        characteristics_t.coefficient_variation = 0
        characteristics_t.save()
    else:
        characteristics_t.least_offer_price = min(offer_prices)
        characteristics_t.greatest_offer_price = max(offer_prices)
        characteristics_t.mid_range = (min(offer_prices) + max(offer_prices)) / 2.0
        characteristics_t.average = sum(offer_prices) / len(offer_prices)

        n = len(offer_prices)
        index = n // 2
        if n % 2:
            characteristics_t.median = sorted(offer_prices)[index]
        else:
            characteristics_t.median = sum(sorted(offer_prices)[index - 1:index + 1]) / 2

        st_dev = 0
        if len(offer_prices) > 1:
            mean = sum(offer_prices) / len(offer_prices)
            var = sum((i - mean) ** 2 for i in offer_prices) / (len(offer_prices) - 1)
            st_dev = math.sqrt(var)

        characteristics_t.standard_deviation = round(st_dev, 2)
        characteristics_t.coefficient_variation = round(st_dev / (sum(offer_prices) / len(offer_prices)), 2)
        characteristics_t.save()
