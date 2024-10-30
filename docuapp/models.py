from django.db import models
from django.contrib.auth.models import User, Group
import uuid
from django.utils import timezone



# STATIC MODELS --------------------------------------------------------------------
class Condition(models.Model):
    name = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Condition"
        verbose_name = "Estado"
        verbose_name_plural = "Estados"



# DOCTYPE MODELS --------------------------------------------------------------------
class DocType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Nombre de Documento')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "DocType"
        verbose_name = "Tipo de documento"
        verbose_name_plural = "Tipo de documentos"



# OFFICE MODELS --------------------------------------------------------------------
class Office(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nombre de Oficina')
    groups = models.ManyToManyField(Group, related_name='offices', verbose_name="Grupos Asociados")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Office"
        verbose_name = "Oficina"
        verbose_name_plural = "Oficinas"



# EXPEDIENT MODEL --------------------------------------------------------------------
class Expedient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=9, unique=True, editable=False)
    document = models.ForeignKey(DocType, on_delete=models.PROTECT, verbose_name='Tipo Documento')
    doc_number = models.CharField(max_length=50, verbose_name='N° Documento', null=False, blank=False)
    subject = models.TextField(verbose_name='Asunto', null=False, blank=False)
    remitter = models.CharField(max_length=70, verbose_name='Remitente', null=False, blank=False)
    destination = models.ForeignKey(Office, on_delete=models.PROTECT, verbose_name='Oficina Destino')
    folio = models.PositiveIntegerField(verbose_name='Folios',default=0, null=False, blank=False)
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT, default="ASIGNADO", verbose_name='Estado')
    phone = models.CharField(max_length=20, verbose_name='Teléfono', blank=True, null=True)
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    observation = models.TextField(verbose_name='Observación', default="NINGUNO", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = "Expedient"
        verbose_name = "Expediente"
        verbose_name_plural = "Expedientes"

    def save(self, *args, **kwargs):
        if not self.code:
            current_year = str(timezone.now().year)[-2:] 
            
            last_expedient = Expedient.objects.filter(
                code__startswith=f"{current_year}E"
            ).order_by('-code').first()

            if last_expedient:
                last_number = int(last_expedient.code[3:])  
                new_number = last_number + 1
            else:
                new_number = 1

            self.code = f"{current_year}E{new_number:06d}"

        super(Expedient, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.code}'



# RECEIVE EXPEDIENT MODEL --------------------------------------------------------------------
class ReceiveExpedient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expedient = models.ForeignKey(Expedient, on_delete=models.PROTECT)
    office = models.ForeignKey(Office, on_delete=models.PROTECT, verbose_name='Oficina Actual')
    destination = models.ForeignKey(Office, on_delete=models.PROTECT, verbose_name='Oficina Destino',  related_name='destinations', null=True, blank=True)
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT, default="RECIBIDO", verbose_name='Estado')
    observation = models.TextField(verbose_name='Motivo', default="", null=True, blank=True)
    date_attention = models.DateTimeField(auto_now=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    @property
    def exp_code(self):
        return self.expedient.code
    
    @property
    def exp_number(self):
        return self.expedient.doc_number

    @property
    def exp_subject(self):
        return self.expedient.subject
    
    class Meta:
        db_table = "ReceiveExpedient"
        verbose_name = "Expediente Recibido"
        verbose_name_plural = "Expedientes Recibidos"

    def save(self, *args, **kwargs):
        if self.condition.name != 'ASIGNADO' and self.condition.name != 'RECIBIDO' and not self.date_attention:
            self.date_attention = timezone.now()
        super().save(*args, **kwargs)  