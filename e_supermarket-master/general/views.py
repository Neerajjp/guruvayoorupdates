import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from general.models import ShopDetails, Location, BannerImages
from general.forms import ShopForm, LocationForm, BannerImagesForm
from main.functions import get_auto_id, generate_form_errors
from general.functions import get_or_create_location


@login_required
def tax_slabs(request):
    context = {
        "tax_slabs_active" : True,
    }
    return render(request, 'general/tax-slabs.html', context)


@login_required
def shop_settings(request):
    instance = ''
    if ShopDetails.objects.filter(is_deleted=False).exists():
        instance = ShopDetails.objects.filter(is_deleted=False)[0]
    if request.method == 'POST':
        if instance:
            form = ShopForm(request.POST, request.FILES,instance=instance)
            location_form = LocationForm(request.POST, request.FILES,instance=instance.location)
            title = "Updated"
        else:
            form = ShopForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST, request.FILES)
            title = "Created"

        auto_id = get_auto_id(ShopDetails)

        if form.is_valid() and location_form.is_valid():
            location_name = location_form.cleaned_data['location_name']
            latitude = location_form.cleaned_data['latitude']
            longitude = location_form.cleaned_data['longitude']

            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = auto_id
            
            location = get_or_create_location(request,location_name,latitude, longitude)
            data.location = location

            if not data.user:
                data.user = request.user
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully " + title ,
                "message": "Successfully " + title ,
                "redirect": "true",
                "redirect_url": reverse('general:shop_settings')
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')

        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": str(message)
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        if instance:
            form = ShopForm(instance=instance)
            button = "Save Change"
            location_form = LocationForm(instance=instance.location)
        else:
            form = ShopForm()
            button = "Submit"
            location_form = LocationForm()

        context = {
            "form": form,
            'button' : button,
            "location_form" : location_form,
            "settings_active" : True,
            "is_need_popup_box" : True,
        }
        return render(request, 'general/settings.html', context)


@login_required
def banner_images(request):
    pk = request.GET.get("pk")
    instance = ''
    if pk:
        try:
            instance = BannerImages.objects.get(pk=pk)
        except:
            pass
    if request.method == 'POST':
        if instance:
            form = BannerImagesForm(request.POST, request.FILES, instance=instance)
            title = "Updated"
        else:
            form = BannerImagesForm(request.POST, request.FILES)
            title = "Created"

        if form.is_valid():
            auto_id = get_auto_id(ShopDetails)
            data = form.save(commit=False)
            data.creator = request.user
            data.updater = request.user
            data.auto_id = auto_id
            data.save()

            response_data = {
                "status": "true",
                "title": "Successfully " + title,
                "message": "Successfully " + title,
                "redirect": "true",
                "redirect_url": reverse('general:banner_images')
            }
            return HttpResponse(json.dumps(response_data), content_type='application/javascript')

        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false",
                "stable": "true",
                "title": "Form validation error",
                "message": str(message)
            }
        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    else:
        instances = BannerImages.objects.filter(is_deleted=False)
        if instance:
            form = BannerImagesForm(instance=instance)
        else:
            form = BannerImagesForm()

        context = {
            "form": form,
            "instances" : instances,
            "banner_images_active" : True,
            "is_need_popup_box" : True,
        }
        return render(request, 'general/add-banner-images.html', context)


@login_required
def delete_banner_image(request, pk):
    instance = get_object_or_404(BannerImages, pk=pk)
    BannerImages.objects.filter(pk=pk).delete()

    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Banner Images Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('general:banner_images')
    }
    return HttpResponse(json.dumps(response_data), content_type='application/javascript')


@login_required
def pages(request):
    context = {
        "pages_active" : True,
    }
    return render(request, 'general/add-pages.html', context)

    