from django.shortcuts import render, redirect
from django.views import generic

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages

from django.contrib.auth import authenticate

from bases.views import SinPrivilegios

from .models import Solicitud
from .forms import SolicitudForm

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, inch, elevenSeventeen
from reportlab.platypus import Table
from io import BytesIO
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

from becas import settings


class SolicitudView(generic.ListView):
    model = Solicitud
    template_name = "solicitudes/becas_list.html"
    context_object_name = "bec"
    permission_required = "solicitud.view_solicitud"


def entregados(request):
    en = Solicitud.objects.filter(entrega='ENTREGADO')
    return render(request, 'solicitudes/entregasi_list.html', {'en': en})


def no_entregados(request):
    en = Solicitud.objects.filter(entrega='NO ENTREGADO')
    return render(request, 'solicitudes/entregano_list.html', {'en': en})


class SolicitudNew(SinPrivilegios, SuccessMessageMixin, generic.CreateView):
    model = Solicitud
    template_name = "solicitudes/becas_form.html"
    form_class = SolicitudForm
    success_url = reverse_lazy("solicitudes:beca_list")
    permission_required = "solicitud.add_solicitud"
    context_object_name = 'obj'
    success_message = "Registro Agregado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class SolicitudEdit(generic.UpdateView):
    model = Solicitud
    template_name = "solicitudes/becas_form.html"
    context_object_name = 'obj'
    form_class = SolicitudForm
    success_url = reverse_lazy("solicitudes:beca_list")
    success_message = "Solicitud Editada"
    permission_required = "solicitud.change_solicitud"


def delete(request, solicitud_id):
    # Recuperamos la instancia de la persona y la borramos
    instancia = Solicitud.objects.get(id=solicitud_id)
    instancia.delete()

    # Después redireccionamos de nuevo a la lista
    return redirect('/solicitudes/solicitud')


def reporte(request, pk):

    response = HttpResponse(content_type='application/pdf')
    report = generarPDF(pk)
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=30,
                            bottomMargin=18,
                            )
    doc.build(report)
    response.write(buff.getvalue())
    buff.close()
    return response


def texto(texto, tamanio):
    styles = getSampleStyleSheet()
    style = 'Heading{}'.format(tamanio)
    return Paragraph(texto, styles[style])


def generarPDF(pk):
    title1 = ParagraphStyle('parrafos',
                            alignment=TA_CENTER,
                            fontSize=20,
                            fontName="Times-Bold",
                            spaceAfter=30,
                            spaceBefore=0
                            )

    body = ParagraphStyle('parrafos',
                          alignment=TA_JUSTIFY,
                          fontSize=12,
                          fontName="Courier",
                          leftIndent=36,
                          spaceAfter=20,
                          spaceBefore=20
                          )
    # header_bold = ParagraphStyle('parrafos',
    # alignment=TA_CENTER,
    # fontSize=15,
    # fontName="Times-Bold",
    # spaceAfter=5,
    # spaceBefore=15
    # )

    info = []
    I = Image(settings.PATH_MEDIA+'ljr.jpg')
    I.drawHeight = 1.0*inch
    I.drawWidth = 1.0*inch
    I.hAlign = 'LEFT'

    info.append(I)

    e = Solicitud.objects.get(pk=pk)

    title_ = Paragraph("SOLICITUD DE BECA 2020 ", title1)
    info.append(title_)
    info.append(Paragraph("NOMBRE: {}".format(e.nombre), body))
    info.append(Paragraph("APELLIDO PATERNO: {}".format(e.ap), body))
    info.append(Paragraph("APELLIDO MATERNO: {}".format(e.am), body))
    info.append(Paragraph("DOMICILIO: {}".format(e.domicilio), body))
    info.append(Paragraph("COLONIA: {}".format(e.colonia), body))
    info.append(Paragraph("TELEFONO: {}".format(e.telefono), body))
    info.append(Paragraph("FECHA DE NACIMIENTO: {}".format(e.fn), body))
    info.append(Paragraph("GRADO ACADEMICO: {}".format(e.ga), body))
    info.append(Paragraph("MATRICULA: {}".format(e.matricula), body))
    info.append(Paragraph("FORMACIÓN ARTISTICA: {}".format(
        e.formacion_artistica), body))
    info.append(Paragraph("MODALIDAD: {}".format(e.modalidad), body))
    info.append(Paragraph("GENERO: {}".format(e.genero), body))
    info.append(Paragraph("CORREO: {}".format(e.correo), body))
    return info
