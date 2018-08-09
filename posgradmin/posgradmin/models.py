# coding: utf-8
import os
from django.db import models
from django.db.models import Q

from django.contrib.auth.models import User

from settings import solicitudes_profesoriles,\
    solicitudes_tutoriles, solicitud_otro,\
    solicitudes_estados, MEDIA_ROOT, MEDIA_URL, \
    APP_PREFIX


class Institucion(models.Model):
    nombre = models.CharField("Institución u Organización", max_length=150)
    suborganizacion = models.CharField(
        "Dependencia, Entidad o Departamento", max_length=150)
    pais = models.CharField("País", max_length=100, blank=True)
    estado = models.CharField(max_length=100, blank=True)
    dependencia_UNAM = models.BooleanField(default=False)
    entidad_PCS = models.BooleanField(default=False)

    def __unicode__(self):
        if self.entidad_PCS:
            pcs = "(entidad del PCS)"
        else:
            pcs = ""
        return u"%s, %s %s" % (self.nombre, self.suborganizacion, pcs)

    class Meta:
        verbose_name_plural = "instituciones"


class CampoConocimiento(models.Model):
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % self.nombre

    class Meta:
        verbose_name_plural = "campos de conocimiento"


class LineaInvestigacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s" % self.nombre

    class Meta:
        verbose_name_plural = "líneas de investigación"


def headshot_path(instance, filename):
    extension = filename.split('.')[-1]
    return 'headshots/%s.%s' % (instance.user.id, extension)


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    titulo = models.CharField("Grado académico (e.g. Dr., Lic.)",
                              max_length=15, blank=True)
    
    curp = models.CharField(max_length=100, blank=True)
    rfc = models.CharField(max_length=100, blank=True)

    telefono = models.CharField(max_length=100)
    telefono_movil = models.CharField(max_length=100, blank=True)

    direccion1 = models.CharField("dirección", max_length=150)

    codigo_postal = models.PositiveSmallIntegerField(default=0)

    website = models.CharField(max_length=200, blank=True)
    pasaporte = models.CharField(max_length=200, blank=True)
    estado_civil = models.CharField(max_length=200, blank=True)

    genero = models.CharField(max_length=1, choices=(('M', 'masculino'),
                                                     ('F', 'femenino')))

    nacionalidad = models.CharField(max_length=100)

    fecha_nacimiento = models.DateField('fecha de nacimiento',
                                        blank=True, null=True)

    headshot = models.ImageField("fotografía",
                                 upload_to=headshot_path,
                                 blank=True, null=True)

    def headshot_url(self):
        return "%s/headshots/%s" % (MEDIA_URL,
                                    os.path.basename(self.headshot.path))

    def __unicode__(self):
        return u"%s" % self.user.get_full_name()

    def __repr__(self):
        return self.__unicode__()

    class Meta:
        verbose_name_plural = "Perfiles"

    def asociado_PCS(self):
        for a in self.adscripcion_set.all():
            if a.institucion.entidad_PCS or a.asociacion_PCS:
                return True
        return False

    def adscripcion_ok(self):
        """
        si tiene adscripciones virtuales, debe tener una real tambien
        """

        if self.adscripcion_set.filter(asociacion_PCS=True).count() > 0:
            # ha registrado virtuales
            if self.adscripcion_set.filter(asociacion_PCS=False).count() > 0:
                # y reales
                return True
            else:
                # pero no reales
                return False
        else:
            # no ha registrado virtuales
            if self.adscripcion_set.count() > 0:
                # pero ha registrado
                return True
            else:
                # no ha registrado ninguna!
                return False


def grado_path(instance, filename):
    return os.path.join(MEDIA_ROOT,
                        'grados/%s/%s' % (instance.user.id,
                                          filename))


class GradoAcademico(models.Model):
    user = models.ForeignKey(User)

    nivel = models.CharField(max_length=15,
                             choices=(('licenciatura', 'licenciatura'),
                                      ('maestria', 'maestria'),
                                      ('doctorado', 'doctorado')))

    grado_obtenido = models.CharField(max_length=100)

    institucion = models.ForeignKey(Institucion)

    fecha_obtencion = models.DateField("Fecha de obtención de grado")

    documento = models.FileField("Copia de documento probatorio",
                                 upload_to=grado_path)

    def documento_url(self):
        return "%s/grados/%s/%s" % (MEDIA_URL,
                                    self.user.id,
                                    os.path.basename(self.documento.path))

    def __unicode__(self):
        return u"%s @ %s" % (self.grado_obtenido, self.institucion)

    class Meta:
        verbose_name_plural = "Grados académicos"


class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cuenta = models.CharField(max_length=100)
    ingreso = models.PositiveSmallIntegerField("año de ingreso al posgrado",
                                               blank=True, null=True)
    semestre = models.PositiveSmallIntegerField(
        "semestre de ingreso al posgrado",
        choices=((1, 1),
                 (2, 2)),
        blank=True, null=True)

    convenio = models.CharField(max_length=100, blank=True)
    # plan = models.CharField("clave del plan de estudios",
    #                         max_length=100, blank=True)

    plan = models.CharField(
        max_length=20,
        choices=((u"Maestría", u"Maestría"),
                 (u"Doctorado", u"Doctorado"),
                 (u"Doctorado directo", u"Doctorado directo"),
                 (u"Opción a titulación", u"Opción a titulación")))

    estado = models.CharField(max_length=15,
                              default=u"vigente",
                              choices=((u"graduado", u"graduado"),
                                       (u"egresado", u"egresado"),
                                       (u"vigente", u"vigente"),
                                       (u"baja temporal", u"baja temporal"),
                                       (u"baja definitiva", u"baja definitiva")))

    fecha_baja = models.DateField(blank=True, null=True)
    motivo_baja = models.CharField(max_length=200,
                                   blank=True)

    fecha_titulacion = models.DateField(blank=True, null=True)
    folio_titulacion = models.CharField(max_length=200, blank=True)
    mencion_honorifica = models.BooleanField(default=False)
    medalla_alfonso_caso = models.BooleanField(default=False)
    semestre_graduacion = models.PositiveSmallIntegerField(blank=True,
                                                           null=True)

    institucion = models.ForeignKey(Institucion)
    observaciones = models.TextField(blank=True)

    def faltan_documentos(self):
        if self.user.gradoacademico_set.count() == 0:
            return True
        else:
            return False

    def solicitudes(self, estado=None):
        if estado is None or estado is 'todas':
            return Solicitud.objects.filter(
                solicitante=self.user
            )
        else:
            return Solicitud.objects.filter(
                solicitante=self.user).filter(
                    estado=estado)

    def cuantas_solicitudes(self):
        solicitudes = [(estado[0], self.solicitudes(estado=estado[0]).count())
                       for estado in solicitudes_estados]
        solicitudes.append(('todas',
                            self.solicitudes().count()))

        return solicitudes

    def __unicode__(self):
        return u"%s [%s]" % (self.user.get_full_name(),
                             self.cuenta)

    def comite_tutoral(self):
        # comites solicitados
        for c in Comite.objects.filter(
                Q(tipo='tutoral')
                & Q(estudiante=self)).order_by('-id'):
            if c.solicitud:
                if c.solicitud.dictamen_final():
                    if c.solicitud.dictamen_final().resolucion == 'concedida':
                        return c

        # comites importados
        if Comite.objects.filter(tipo='tutoral',
                                 estudiante=self,
                                 solicitud=None).count() > 0:
            return Comite.objects.filter(tipo='tutoral',
                                         estudiante=self,
                                         solicitud=None).last()

        return None

    def get_proyecto(self):
        for p in self.proyecto_set.all():
            p.update_status()

        return self.proyecto_set.filter(
            aprobado=True
        ).order_by('id').last()

    def get_proyecto_no_aprobado(self):
        for p in self.proyecto_set.order_by('-id'):
            if p.id > self.get_proyecto().id \
               and p.solicitud.dictamen_final() is None:
                return p
        return None

    def as_a(self):
        return "<a href='%sinicio/usuario/%s'>%s</a>" % (
            APP_PREFIX,
            self.user.id,
            self.user.get_full_name())


class Beca(models.Model):
    estudiante = models.ForeignKey(Estudiante)

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s %s" % (self.estudiante, self.tipo)


class Sesion(models.Model):
    fecha = models.DateField()
    descripcion = models.CharField(max_length=100,
                                   default="sesión ordinaria")
    # guardar markdown
    minuta = models.TextField(blank=True)

    def as_a(self):
        return u"""<a href='%sinicio/sesiones/%s/'>%s %s</a>""" % (
            APP_PREFIX,
            self.id, self.fecha, self.descripcion)

    def __unicode__(self):
        return u'%s, %s' % (self.fecha,
                            self.descripcion)

    class Meta:
        verbose_name_plural = "Sesiones"


class Solicitud(models.Model):
    resumen = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100,
                            choices=solicitudes_profesoriles +
                            solicitudes_tutoriles + solicitud_otro)
    solicitante = models.ForeignKey(User)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    sesion = models.ForeignKey(Sesion, blank=True, null=True)
    descripcion = models.TextField(blank=True)

    estado = models.CharField(max_length=30, default="nueva",
                              choices=solicitudes_estados)

    def agendable(self, user):
        if hasattr(user, 'asistente') or user.is_staff:
            if self.estado == 'nueva':
                return True

    def dictaminable(self, user):

        if self.estado == 'agendada':

            if self.solicitante.id == user.id:
                return False

            if hasattr(user, 'asistente') or user.is_staff \
               or user.academico.acreditado():
                return True
        else:
            return False

    def cancelable(self, user):
        if self.estado == 'nueva':  # sólo nuevas se cancelan
            if self.predictamen():
                return False

            if self.solicitante.id == user.id:   # cancelar las propias
                return True
        else:
            return False

    def dictamen_final(self):
        return self.dictamen_set.filter(autor__is_staff=True).last()

    def predictamen(self):
        if self.dictamen_final():
            return True
        elif self.dictamen_set.count() > 0:
            return True
        else:
            return False

    def __unicode__(self):
        return u"#%s %s [%s]" % (self.id, self.resumen, self.solicitante)

    def as_a(self):
        icon = """<span class='glyphicon glyphicon-{icon}'
                        aria-hidden=true></span>"""
        if self.dictamen_final():
            if self.dictamen_final().resolucion == 'concedida':
                status = '%s' % icon.format(icon='thumbs-up')
            else:
                status = '%s' % icon.format(icon='thumbs-down')
        elif self.predictamen():
            status = '%s' % icon.format(icon='eye-open')
        elif self.estado == 'cancelada':
            return u"""<a href='%sinicio/solicitudes/%s'>
                       <strike>#%s</strike></a>""" % (
                           APP_PREFIX,
                           self.id, self.id)
        elif self.estado == 'agendada':
            status = '%s' % icon.format(icon='calendar')
        else:
            status = self.estado

        return u"""<a href='%sinicio/solicitudes/%s'>#%s %s</a>""" % (
            APP_PREFIX,
            self.id, self.id, status)

    class Meta:
        verbose_name_plural = "Solicitudes"


class Proyecto(models.Model):
    campo_conocimiento = models.ForeignKey(CampoConocimiento)
    nombre = models.CharField(max_length=200)
    estudiante = models.ForeignKey(Estudiante)
    solicitud = models.ForeignKey(Solicitud, blank=True, null=True)
    aprobado = models.BooleanField(default=False)

    def update_status(self):
        if self.solicitud and self.solicitud.dictamen_final():
            if self.solicitud.dictamen_final().resolucion == 'concedida':
                self.aprobado = True
                self.save()

    def __unicode__(self):
        if self.aprobado:
            estado = 'aprobado'
        else:
            estado = 'no aprobado'
        return u'"%s" en %s (%s)' % (self.nombre,
                                     self.campo_conocimiento,
                                     estado)


def anexo_path(instance, filename):
    return os.path.join(MEDIA_ROOT,
                        'solicitudes/%s/%s' % (instance.solicitud.id,
                                               filename))


class Anexo(models.Model):
    solicitud = models.ForeignKey(Solicitud)
    autor = models.ForeignKey(User)
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to=anexo_path)

    def url(self):
        return "%s/solicitudes/%s/%s" % (MEDIA_URL,
                                         self.solicitud.id,
                                         os.path.basename(self.archivo.path))

    def basename(self):
        return os.path.basename(self.archivo.file.name)

    def __unicode__(self):
        return u"[%s anexo a #%s por %s el %s]" % (self.basename(),
                                                   self.solicitud.id,
                                                   self.autor,
                                                   self.fecha)


class Acuerdo(models.Model):
    solicitud = models.ForeignKey(Solicitud)
    archivo = models.FileField()
    fecha = models.DateTimeField(auto_now_add=True)
    # id asamblea


class Comentario(models.Model):
    solicitud = models.ForeignKey(Solicitud)
    autor = models.ForeignKey(User)
    fecha = models.DateTimeField(auto_now_add=True)
    comentario = models.CharField(max_length=300)
    # anexo?

    def __unicode__(self):
        return u'%s por %s: "%s"' % (self.fecha, self.autor, self.comentario)


class Academico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nivel_PRIDE = models.CharField(max_length=15,
                                   choices=(('sin PRIDE', 'sin PRIDE'),
                                            ('A', 'A'),
                                            ('B', 'B'),
                                            ('C', 'C'),
                                            ('D', 'D')))
    nivel_SNI = models.CharField(max_length=15,
                                 choices=(('sin SNI', 'sin SNI'),
                                          ('I', 'I'),
                                          ('II', 'II'),
                                          ('III', 'III'),
                                          ('C', 'C'),
                                          ('E', 'E')))
    CVU = models.CharField(max_length=100, blank=True, null=True)
    DGEE = models.CharField(max_length=6, blank=True, null=True)
    numero_trabajador_unam = models.CharField("Número de trabajador (UNAM)",
                                              max_length=100,
                                              blank=True, null=True)

    tutor = models.BooleanField(default=False)

    comite_academico = models.BooleanField(default=False)

    fecha_acreditacion = models.DateField(blank=True, null=True)

    acreditacion = models.CharField(max_length=15,
                                    choices=(('E', 'E'),
                                             ('D', 'D'),
                                             ('PD', 'PD'),
                                             ('NPD', 'NPD'),
                                             ('M', 'M'),
                                             ('NPM', 'NPM'),
                                             ('PM', 'PM')))

    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE,
                                     blank=True, null=True)

    campos_de_conocimiento = models.ManyToManyField(
        CampoConocimiento,
        blank=True)
    lineas_de_investigacion = models.ManyToManyField(
        LineaInvestigacion,
        blank=True)

    # Resumen Curricular
    tesis_licenciatura = models.PositiveSmallIntegerField(
        "Cantidad de tesis dirigidas a nivel Licenciatura",
        null=True, blank=True)
    tesis_licenciatura_5 = models.PositiveSmallIntegerField(
      "Cantidad de tesis dirigidas a nivel Licenciatura en los últimos 5 años",
      null=True, blank=True)

    tesis_maestria = models.PositiveSmallIntegerField(
        "Cantidad de tesis dirigidas a nivel Maestría",
        null=True, blank=True)
    tesis_maestria_5 = models.PositiveSmallIntegerField(
        "Cantidad de tesis dirigidas a nivel Maestría en los últimos 5 años",
        null=True, blank=True)

    tesis_doctorado = models.PositiveSmallIntegerField(
        "Cantidad de tesis dirigidas a nivel Doctorado",
        null=True, blank=True)
    tesis_doctorado_5 = models.PositiveSmallIntegerField(
        "Cantidad de tesis dirigidas a nivel Doctorado en los últimos 5 años",
        null=True, blank=True)

    participacion_comite_maestria = models.PositiveSmallIntegerField(
        "Cantidad de participaciones como miembro de comité tutor en el PCS a nivel maestría",
        null=True, blank=True)
    participacion_comite_doctorado = models.PositiveSmallIntegerField(
       "Cantidad de participaciones como miembro de comité tutor en el PCS a nivel doctorado",
       null=True, blank=True)

    participacion_tutor_maestria = models.PositiveSmallIntegerField(
        "Cantidad de participaciones como tutor principal "
        + "en el PCS a nivel maestría",
        null=True, blank=True)
    participacion_tutor_doctorado = models.PositiveSmallIntegerField(
        "Cantidad de participaciones como tutor principal "
        + "en el PCS a nivel doctorado",
        null=True, blank=True)

    tutor_principal_otros_programas = models.TextField(
        "Otros programas en los que participa como tutor principal",
        blank=True)

    tutor_otros_programas = models.TextField(
        "Otros programas en los que participa como "
        + "miembro de comité tutor",
        blank=True)

    articulos_internacionales = models.PositiveSmallIntegerField(
        "Cantidad de artículos publicados en revistas internacionales",
        null=True, blank=True)

    articulos_internacionales_5 = models.PositiveSmallIntegerField(
        "Cantidad de artículos publicados en revistas internacionales "
        + "durante los últimos 5 años",
        null=True, blank=True)

    articulos_nacionales = models.PositiveSmallIntegerField(
        "Cantidad de artículos publicados en revistas nacionales",
        null=True, blank=True)

    articulos_nacionales_5 = models.PositiveSmallIntegerField(
        "Cantidad de artículos publicados en revistas nacionales "
        + "durante los últimos 5 años",
        null=True, blank=True)

    libros = models.PositiveSmallIntegerField(
        "Cantidad de libros publicados",
        null=True, blank=True)

    libros_5 = models.PositiveSmallIntegerField(
        "Cantidad de libros publicados durante los últimos 5 años",
        null=True, blank=True)

    capitulos = models.PositiveSmallIntegerField(
        "Cantidad de capítulos de libro publicados",
        null=True, blank=True)

    capitulos_5 = models.PositiveSmallIntegerField(
        "Cantidad de capítulos de libro publicados durante los últimos 5 años",
        null=True, blank=True)

    # Actividad profesional y de Investigación
    lineas = models.TextField(
        "Temas de interés y/o experiencia en ciencias de la sostenibilidad",
        blank=True)

    palabras_clave = models.TextField(
        "Palabras clave de temas de interés y/o experiencia"
        + "en ciencias de la sostenibilidad separadas por comas",
        blank=True)
    motivacion = models.TextField("Motivación para participar en el Programa",
                                  blank=True)
    proyectos_sostenibilidad = models.TextField(
        "Principales proyectos relacionados con "
        + "ciencias de la sostenibilidad", blank=True)
    proyectos_vigentes = models.TextField(
        "Proyectos vigentes en los que pueden "
        + "participar alumnos del PCS", blank=True)

    # disponibilidad
    disponible_tutor = models.BooleanField(
        "Disponible como tutor principal (dirección de alumnos)",
        default=False)

    disponible_miembro = models.BooleanField(
        "Disponible como miembro de comité tutor (asesoría de alumnos)",
        default=False)

    # epílogo
    observaciones = models.TextField(blank=True)

    def show_acreditacion(self):
        if self.acreditacion == 'E':
            return u"Comité tutor específico"
        elif (self.acreditacion == 'D'
              or self.acreditacion == 'PD'
              or self.acreditacion == 'NPD'):
            return "Doctorado"
        else:
            return "Maestría"

    def resumen_completo(self):
        if self.tesis_licenciatura == "":
            return False
        elif self.tesis_maestria == "":
            return False
        elif self.tesis_doctorado == "":
            return False
        elif self.tesis_licenciatura_5 == "":
            return False
        elif self.tesis_maestria_5 == "":
            return False
        elif self.tesis_doctorado_5 == "":
            return False
        elif self.participacion_comite_maestria == "":
            return False
        elif self.participacion_tutor_maestria == "":
            return False
        elif self.participacion_comite_doctorado == "":
            return False
        elif self.participacion_tutor_doctorado == "":
            return False
        elif self.articulos_internacionales_5 == "":
            return False
        elif self.articulos_nacionales_5 == "":
            return False
        elif self.articulos_internacionales == "":
            return False
        elif self.articulos_nacionales == "":
            return False
        elif self.capitulos == "":
            return False
        elif self.capitulos_5 == "":
            return False
        elif self.libros == "":
            return False
        elif self.libros_5 == "":
            return False
        else:
            return True

    def actividad_completo(self):
        if self.lineas == "":
            return False
        elif self.palabras_clave == "":
            return False
        elif self.motivacion == "":
            return False
        elif self.proyectos_vigentes == "":
            return False
        else:
            return True

    def as_a(self):
        icon = """<span class='glyphicon glyphicon-{icon}'
                        aria-hidden=true></span>"""
        icon.format(icon='thumbs-up')

        return u"""<a href='%sinicio/usuario/%s'>%s %s</a>""" % (
            APP_PREFIX,
            self.user.id, icon, self.__unicode__())

    def nombre_completo(self):
        return self.user.get_full_name()

    def acreditado(self):
        return self.tutor
        # if self.solicitud.dictamen_final() is None:
        #     return False
        # elif self.solicitud.dictamen_final().resolucion == 'concedida':
        #     self.fecha_acreditacion = self.solicitud.dictamen_final().fecha
        #     self.tutor = True
        #     self.save()
        #     return True

    def solicitudes(self, estado=None):
        solicitudes_de_estudiantes = set()
        for e in self.estudiantes():
            for s in e.solicitudes():
                solicitudes_de_estudiantes.add(s.id)

        if estado is None or estado == 'todas':
            return Solicitud.objects.filter(
                Q(pk__in=solicitudes_de_estudiantes)
                | Q(solicitante=self.user))
        else:
            return Solicitud.objects.filter(
                (Q(pk__in=solicitudes_de_estudiantes)
                 | Q(solicitante=self.user))
                & Q(estado=estado))

    def cuantas_solicitudes(self):
        solicitudes = [(estado[0], self.solicitudes(estado=estado[0]).count())
                       for estado in solicitudes_estados]
        solicitudes.append(('todas', self.solicitudes().count()))

        return solicitudes

    def estudiantes(self):
        estudiantes = set()
        if self.tutor:
            for c in Comite.objects.filter(Q(tipo='tutoral')
                                           & (Q(miembro1=self)
                                              | Q(miembro2=self)
                                              | Q(miembro3=self)
                                              | Q(miembro4=self)
                                              | Q(miembro5=self))):
                if c.solicitud:
                    if c.solicitud.dictamen_final():
                        if c.solicitud.dictamen_final()\
                                      .resolucion == 'concedida':
                            estudiantes.add(c.estudiante)
                        elif c.solicitud.estado != 'cancelada':
                            estudiantes.add(c.estudiante)
                else:
                    if Comite.objects.filter(
                            estudiante=c.estudiante).count() == 1:
                        estudiantes.add(c.estudiante)
            return estudiantes
        else:
            return []

    def comites(self):
        comites = list()

        for c in Comite.objects.filter(
                (Q(tipo='candidatura') | Q(tipo='grado'))
                & (Q(miembro1=self)
                   | Q(miembro2=self)
                   | Q(miembro3=self))):
            if c.solicitud.dictamen_final():
                if c.solicitud.dictamen_final().resolucion == 'concedida':
                    comites.append(c)
        return comites

    def __unicode__(self):
        return u"%s %s %s" % (self.titulo,
                              self.user.first_name,
                              self.user.last_name)

    class Meta:
        verbose_name_plural = "Académicos"


class AnexoAcademico(models.Model):
    academico = models.ForeignKey(Academico)
    autor = models.ForeignKey(User)
    fecha = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to=anexo_path)

    # def url(self):
    #     return "%s/solicitudes/%s/%s" % (MEDIA_URL,
    #                                      self.solicitud.id,
    #                                      os.path.basename(self.archivo.path))

    # def basename(self):
    #     return os.path.basename(self.archivo.file.name)

    # def __unicode__(self):
    #     return u"[%s anexo a #%s por %s el %s]" % (self.basename(),
    #                                                self.solicitud.id,
    #                                                self.autor,
    #                                                self.fecha)


class Adscripcion(models.Model):
    perfil = models.ForeignKey(Perfil)
    institucion = models.ForeignKey(Institucion)

    asociacion_PCS = models.BooleanField(
        "sólo para asociación con el PCS",
        default=False)

    def __unicode__(self):
        if self.asociacion_PCS:
            asoc = u"(sólo para asociación con el Posgrado)"
        else:
            asoc = ""
        return u"%s %s" % (self.institucion,
                           asoc)


class Comite(models.Model):
    miembro1 = models.ForeignKey(Academico,
                                 related_name="miembro1_comites")
    miembro2 = models.ForeignKey(Academico,
                                 related_name="miembro2_comites")
    miembro3 = models.ForeignKey(Academico,
                                 related_name="miembro3_comites",
                                 null=True, blank=True)
    miembro4 = models.ForeignKey(Academico,
                                 related_name="miembro4_comites",
                                 null=True, blank=True)
    miembro5 = models.ForeignKey(Academico,
                                 related_name="miembro5_comites",
                                 null=True, blank=True)

    solicitud = models.ForeignKey(Solicitud, null=True, blank=True)
    estudiante = models.ForeignKey(Estudiante)
    tipo = models.CharField(max_length=15,
                            choices=(('tutoral', 'tutoral'),
                                     ('candidatura', 'candidatura'),
                                     ('grado', 'grado')))

    def get_tipo(self):
        if self.tipo == 'tutoral':
            return u'Comité tutoral'
        elif self.tipo == 'candidatura':
            return u"Jurado de examen de candidatura"
        elif self.tipo == 'grado':
            return u"Jurado de examen de grado"

    class Meta:
        verbose_name_plural = "Comités"

    def __unicode__(self):
        return u'[%s] %s, %s, %s' \
            % (self.tipo,
               self.miembro1,
               self.miembro2,
               self.miembro3)

    def as_ul(self):
        ul = """
        <ul>
        <li>
            <a href="%sinicio/usuario/%s/">%s</a></li>
        <li>
            <a href="%sinicio/usuario/%s/">%s</a></li>
        """ % (
                APP_PREFIX, self.miembro1.user.id, self.miembro1,
                APP_PREFIX, self.miembro2.user.id, self.miembro2)

        if self.miembro3:
            ul += """<li>
            <a href="%sinicio/usuario/%s/">%s</a></li>""" % (
                APP_PREFIX, self.miembro3.user.id, self.miembro3)

        if self.miembro4:
            ul += """<li>
            <a href="%sinicio/usuario/%s/">%s</a></li>""" % (
                APP_PREFIX, self.miembro4.user.id, self.miembro4)

        if self.miembro5:
            ul += """<li>
            <a href="%sinicio/usuario/%s/">%s</a></li>""" % (
                APP_PREFIX, self.miembro5.user.id, self.miembro5)

        ul += "</ul>"
        return ul


class Asistente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def cuantas_solicitudes(self):
        solicitudes = [(estado[0], self.solicitudes(estado=estado[0]).count())
                       for estado in solicitudes_estados]
        solicitudes.append(('todas', self.solicitudes().count()))

        return solicitudes

    def solicitudes(self, estado=None):
        if estado is None or estado is 'todas':
            return Solicitud.objects.all()
        else:
            return Solicitud.objects.filter(estado=estado)

    class Meta:
        verbose_name_plural = "Asistentes de Proceso"

    def __unicode__(self):
        return "%s (asistente de proceso)" % self.user


class Dictamen(models.Model):
    resolucion = models.CharField(max_length=15,
                                  choices=(('concedida', 'concedida'),
                                           ('denegada', 'denegada')))
    solicitud = models.ForeignKey(Solicitud)
    autor = models.ForeignKey(User, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Dictámenes"

    def __unicode__(self):
        return u'#%s %s por %s' \
            % (self.solicitud.id,
               self.resolucion,
               self.autor)


def curso_path(instance, filename):
    return os.path.join(MEDIA_ROOT,
                        'cursos/%s/%s' % (instance.id,
                                          filename))


class Curso(models.Model):
    asignatura = models.CharField(max_length=100)
    clave = models.CharField(max_length=100, blank=True, null=True)

    creditos = models.PositiveSmallIntegerField()
    horas_semestre = models.PositiveSmallIntegerField("Horas por semestre")
    tipo = models.CharField(max_length=40,
                            choices=(("Obligatoria", "Obligatoria"),
                                     (u"Obligatorias de elección",
                                      u"Obligatorias de elección"),
                                     ("Optativa", "Optativa"),
                                     ("Optativa, intersemestral",
                                      "Optativa, intersemestral")))

    programa = models.FileField("Documento con descripción extensa.",
                                upload_to=curso_path)

    def programa_url(self):
        return "%s/cursos/%s/%s" % (MEDIA_URL,
                                    self.id,
                                    os.path.basename(self.programa.path))

    def __unicode__(self):
        return u'%s: %s' % (self.clave,
                            self.asignatura)


class Catedra(models.Model):
    curso = models.ForeignKey(Curso)
    semestre = models.PositiveSmallIntegerField(
        choices=((1, 1), (2, 2)))
    year = models.PositiveSmallIntegerField("Año")
    profesor = models.ForeignKey(Academico, blank=True, null=True)
    sede = models.CharField(max_length=80, blank=True)

    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Cátedras"

    def __unicode__(self):
        return u'%s, %s %s, por %s' % (self.curso,
                                       self.semestre,
                                       self.year,
                                       self.profesor)


class Acta(models.Model):
    acuerdos = models.TextField(blank=True)
    sesion = models.ForeignKey(Sesion)
