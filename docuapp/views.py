from django.shortcuts import render, redirect, get_object_or_404
from .models import Expedient, ReceiveExpedient, Condition, DocType, Office, User
from .forms import ExpedientForm, ReceiveExpedientForm, DocTypeForm, OfficeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from babel.dates import format_datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import pytz



# ************************************ GENERAL VIEWS ************************************

# HOME ---------------------------------------------------------------->
def home_view(request):
    return render(request, 'index.html')

# LOGIN --------------------------------------------------------------->
def login_view(request):
    if request.user.is_authenticated:
        return redirect('tramitec:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tramitec:home')
            else:
                form.add_error(None, 'Usuario o contraseña incorrecto')
    else:
        form = AuthenticationForm(
            initial={'username': request.POST.get('username', '')})

    return render(request, 'login.html', {'form': form})

# LOGOUT --------------------------------------------------------------->
@login_required
def logout_view(request):
    logout(request)
    return redirect('tramitec:home')



# ************************************ DOCTYPE VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
def doctype_create_view(request):
    if request.method == 'POST':
        form = DocTypeForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, '¡Registro exitoso!')
            return redirect('tramitec:doctype_create')  
    else:
        results = DocType.objects.all()
        form = DocTypeForm()
    
    return render(request, 'doctypes/doctype_create.html', {'form': form, 'doctypes': results,})

# UPDATE ----------------------------------------------------------------->
@login_required
def doctype_update_view(request, id):
    doctype = get_object_or_404(DocType, pk=id)

    if request.method == 'POST':
        form = DocTypeForm(request.POST, instance=doctype)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect('tramitec:doctype_create')
    else:
        form = DocTypeForm(instance=doctype)

    return render(request, 'doctypes/doctype_update.html', {'form': form})

# DELETE ------------------------------------------------------------------>
@login_required
def doctype_delete_view(request, id):
    doctype = get_object_or_404(DocType, pk=id)

    if Expedient.objects.filter(document=doctype.pk).exists():
        messages.warning(request, 'Tipo de documento está en uso')
        return redirect('tramitec:doctype_create')  

    doctype.delete()
    messages.success(request, '¡Registro eliminado!')

    return redirect('tramitec:doctype_create')  



# ************************************ OFFICE VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
def office_create_view(request):
    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, '¡Registro exitoso!')
            return redirect('tramitec:office_create')  
    else:
        results = Office.objects.all()
        form = OfficeForm()
    
    return render(request, 'offices/office_create.html', {'form': form, 'offices': results,})

# UPDATE ----------------------------------------------------------------->
@login_required
def office_update_view(request, id):
    office = get_object_or_404(Office, pk=id)

    if request.method == 'POST':
        form = OfficeForm(request.POST, instance=office)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect('tramitec:office_create')
    else:
        form = OfficeForm(instance=office)

    return render(request, 'offices/office_update.html', {'form': form})

# DELETE ------------------------------------------------------------------>
@login_required
def office_delete_view(request, id):
    office = get_object_or_404(Office, pk=id)

    if Expedient.objects.filter(document=office.pk).exists():
        messages.warning(request, 'Tipo de documento está en uso')
        return redirect('tramitec:office_create')  

    office.delete()
    messages.success(request, '¡Registro eliminado!')

    return redirect('tramitec:office_create')  



# ************************************ EXPEDIENT VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
def expedient_create_view(request):
    if request.method == 'POST':
        form = ExpedientForm(request.POST, user=request.user)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, '¡Registro exitoso!')
            return redirect('tramitec:expedient_list')  
    else:
        form = ExpedientForm(user=request.user)
    
    return render(request, 'expedients/expedient_create.html', {'form': form})

# UPDATE ----------------------------------------------------------------->
@login_required
def expedient_update_view(request, id):
    expedient = get_object_or_404(Expedient, pk=id)

    if request.method == 'POST':
        form = ExpedientForm(request.POST, instance=expedient, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Actualización exitosa!')
            return redirect('tramitec:expedient_list')
    else:
        
        form = ExpedientForm(instance=expedient, user=request.user)

    return render(request, 'expedients/expedient_update.html', {'form': form, })

# LIST ------------------------------------------------------------------->
@login_required
def expedient_list_view(request):
    user_groups = request.user.groups.all()
    users_in_same_groups = User.objects.filter(groups__in=user_groups).distinct()
    results = Expedient.objects.filter(user__in=users_in_same_groups)

    return render(request, 'expedients/expedient_list.html', 
                {
                    'expedients': results,
                })

# GENEREATE PDF ------------------------------------------------------------------>
@login_required
def generate_expedient_pdf(request, id):
    expedient = get_object_or_404(Expedient, pk=id)
    user = expedient.user 

    base_url = 'file:///C:/tramitec/'

    current_date = timezone.localtime(timezone.now(), timezone=pytz.timezone('America/Lima'))
    date_print = format_datetime(current_date, format="d'/'MM'/'yyyy HH:mm", locale='es')

    data = {
        'date': date_print,
        'expedient': expedient,
        'current_date': current_date,
        'img_drta': f"{base_url}static/images/drta.png",
        'img_tramitec': f"{base_url}static/images/logo_tramitec.png",
        'user':user,
    }

    html_string = render_to_string('expedients/expedient_pdf.html', data)

    filename = current_date.strftime('%d-%m-%Y %H.%M') + "_hoja de ruta.pdf"
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

# DELETE ------------------------------------------------------------------>
@login_required
def expedient_delete_view(request, id):
    expedient = get_object_or_404(Expedient, pk=id)

    if ReceiveExpedient.objects.filter(expedient=expedient.pk).exists():
        messages.warning(request, 'Documento ya tiene recepción en otra Oficina')
        return redirect('tramitec:expedient_list')  

    expedient.delete()
    messages.success(request, '¡Registro eliminado!')

    return redirect('tramitec:expedient_list')  



# ************************************ RECEIVE EXPEDIENT VIEWS ************************************

# CREATE --------------------------------------------------------------->
@login_required
def receive_expedient_create_view(request):
    expedient = None

    if 'code' in request.GET:
        code = request.GET.get('code')
        expedient = Expedient.objects.filter(code=code).first()

        if not expedient:
            return render(request, 'receive_expedients/receive_expedient_create.html', {
                'form': None,
                'error': f"Expediente {code} no existe",
            })
        
        first_reception = not ReceiveExpedient.objects.filter(expedient=expedient).exists()
        user_groups = request.user.groups.all()

        if expedient.condition.name == 'FINALIZADO':
            return render(request, 'receive_expedients/receive_expedient_create.html', {
                'form': None,
                'error': f"Expediente {code} ya terminó su ciclo",
            })

        if first_reception:
            if not expedient.destination.groups.filter(id__in=user_groups).exists():
                return render(request, 'receive_expedients/receive_expedient_create.html', {
                    'form': None,
                    'error': f"Expediente {code} está asignado a otra oficina",
                })
        else:
            last_receive = ReceiveExpedient.objects.filter(expedient=expedient).order_by('-created_at').first()

            if last_receive.destination:

                if last_receive and not last_receive.destination.groups.filter(id__in=user_groups).exists():
                    return render(request, 'receive_expedients/receive_expedient_create.html', {
                        'form': None,
                        'error': f"Expediente {code} está asignado a otra oficina",
                    })
            else:
                return render(request, 'receive_expedients/receive_expedient_create.html', {
                'form': None,
                'error': f"Expediente {code} está en proceso de atención",
                })

    if request.method == 'POST' and expedient:
        form = ReceiveExpedientForm(request.POST, expedient=expedient, user=request.user, is_edit=False)
        if form.is_valid():
            receive_expedient = form.save(commit=False)
            receive_expedient.expedient = expedient  # Asociar el expediente
            receive_expedient.user = request.user
            receive_expedient.save()

            last_record = ReceiveExpedient.objects.filter(expedient=expedient).order_by('-created_at').first()
            if last_record and last_record.condition.name == 'FINALIZADO':
                expedient.condition = Condition.objects.get(name='FINALIZADO')
                expedient.save()

            return redirect('tramitec:receive_expedient_list')  
    else:
        form = ReceiveExpedientForm(expedient=expedient, user=request.user, is_edit=False) if expedient else None

    return render(request, 'receive_expedients/receive_expedient_create.html', {
        'expedient': expedient,
        'form': form,
    })

# UPDATE ----------------------------------------------------------------->
@login_required
def receive_expedient_update_view(request, id):
    receive_expedient = get_object_or_404(ReceiveExpedient, pk=id)

    if request.method == 'POST':
        form = ReceiveExpedientForm(request.POST, instance=receive_expedient, is_edit=True)
        if form.is_valid():
            updated_expedient = form.save(commit=False) 
            updated_expedient.save() 

            last_record = ReceiveExpedient.objects.filter(expedient=receive_expedient.expedient).order_by('-created_at').first()
            if last_record and last_record.condition.name == 'FINALIZADO':
                expedient = receive_expedient.expedient
                expedient.condition = Condition.objects.get(name='FINALIZADO')
                expedient.save()

            messages.success(request, '¡Actualización exitosa!')
            return redirect('tramitec:receive_expedient_list')
    else:
        form = ReceiveExpedientForm(instance=receive_expedient, is_edit=True)

    return render(request, 'receive_expedients/receive_expedient_update.html', {'form': form, })

# LIST ------------------------------------------------------------------->
@login_required
def receive_expedient_list_view(request):
    user_groups = request.user.groups.all()
    users_in_same_groups = User.objects.filter(groups__in=user_groups).distinct()
    results = ReceiveExpedient.objects.filter(user__in=users_in_same_groups)

    return render(request, 'receive_expedients/receive_expedient_list.html', 
                {
                    'receive_expedients': results,
                })

# ROUTE ------------------------------------------------------------------->
@login_required
def receive_expedient_route_view(request):
    expedient = None
    related_records = None

    if 'code' in request.GET:
        code = request.GET.get('code').strip()
        expedient = Expedient.objects.filter(code=code).first()

        if not expedient:
            return render(request, 'receive_expedients/receive_expedient_create.html', {
                'form': None,
                'error': f"El expediente con código {code} no existe",
            })
        
        if expedient:
            related_records = ReceiveExpedient.objects.filter(expedient=expedient)

    return render(request, 'receive_expedients/receive_expedient_route.html', {
        'expedient': expedient,
        'related_records': related_records,
    })

# DELETE ------------------------------------------------------------------>
@login_required
def receive_expedient_delete_view(request, id):
    receive_expedient = get_object_or_404(ReceiveExpedient, pk=id)

    receive_expedient.delete()
    messages.success(request, '¡Registro eliminado!')

    return redirect('tramitec:receive_expedient_list')  



# ************************************ ERROR VIEWS ************************************
@login_required
def error_404(request, exception):
    return render(request, '404.html', {})

@login_required
def error_403(request, exception):
    return render(request, '403.html', status=403)
