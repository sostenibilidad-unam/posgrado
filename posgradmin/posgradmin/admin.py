# coding: utf-8
from django.contrib import admin
from .models import Perfil, Academico, Estudiante, \
    GradoAcademico, Institucion, CampoConocimiento, \
    Solicitud, Proyecto, Dictamen, \
    Comite, Curso, Catedra, Sesion, Adscripcion, \
    LineaInvestigacion

admin.site.site_header = \
                "Administración de Posgrado en Ciencias de la Sostenibilidad"
admin.site.site_title = "Posgrado en Ciencias de la Sostenibilidad"
admin.site.site_url = "/"


class EstudianteAdmin(admin.ModelAdmin):
    search_fields = ['cuenta', 'user__first_name', 'user__last_name']
    list_display = ['user', 'cuenta',
                    'plan', 'ingreso', 'unificado']

    def unificado(self, estudiante):
        return estudiante.as_a()

    unificado.allow_tags = True
    unificado.short_description = 'Vista unificada'


admin.site.register(Estudiante, EstudianteAdmin)


class AcademicoAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name']
    list_display = ['fullname',
                    'acreditacion',
                    'perfil_personal_completo',
                    'perfil_academico_completo',
                    'unificado']
    list_filter = ['acreditacion', 'disponible_tutor', 'disponible_miembro', ]

    fieldsets = (
        (None,
         {'fields': ('user',
                     'observaciones',)}),
        ('Participación en el Programa',
         {'fields': ('tutor',
                     'comite_academico',
                     'fecha_acreditacion',
                     'acreditacion',
                     'estimulo_UNAM',
                     'nivel_SNI',
                     'CVU',
                     'DGEE',
                     'anexo_CV',
                     'anexo_solicitud'
         )}),
        ('Líneas de investigación, Campos de Conocimiento',
         {'fields': ('lineas_de_investigacion',
                     'campos_de_conocimiento')}),
        ('Resumen Curricular',
         {'fields': ('tesis_licenciatura',
                     'tesis_maestria',
                     'tesis_doctorado',
                     'tesis_licenciatura_5',
                     'tesis_maestria_5',
                     'tesis_doctorado_5',
                     'participacion_comite_maestria',
                     'participacion_tutor_maestria',
                     'participacion_comite_doctorado',
                     'participacion_tutor_doctorado',
                     'tutor_otros_programas',
                     'tutor_principal_otros_programas',
                     'articulos_internacionales_5',
                     'articulos_nacionales_5',
                     'articulos_internacionales',
                     'articulos_nacionales',
                     'capitulos',
                     'capitulos_5',
                     'libros',
                     'libros_5',)}),
        ("Actividad profesional y de Investigación",
         {"fields": ("lineas",
                     'palabras_clave',
                     'motivacion',
                     'proyectos_vigentes',)}),
        ("Disponibilidad",
         {"fields": ("disponible_miembro",
                     'disponible_tutor',)}),
    )

    def perfil_academico_completo(self, obj):
        return obj.resumen_completo()

    perfil_academico_completo.boolean = True

    def perfil_personal_completo(self, obj):
        ok = False
        if hasattr(obj.user, 'perfil'):
            if obj.user.gradoacademico_set.count > 0:
                if obj.user.perfil.adscripcion_ok():
                    ok = True
        return ok

    perfil_personal_completo.boolean = True

    def fullname(self, obj):
        name = obj.user.get_full_name()
        if name:
            return name
        else:
            return obj.user.username

    def unificado(self, academico):
        return academico.as_a()

    unificado.allow_tags = True
    unificado.short_description = 'Vista unificada'


admin.site.register(Academico, AcademicoAdmin)


class AdscripcionAdmin(admin.ModelAdmin):
    search_fields = ['perfil__user__first_name',
                     'perfil__user__last_name']
    list_display = ['perfil',
                    'institucion',
                    'nombramiento',
                    'anno_nombramiento']
    list_filter = ['catedra_conacyt', 'asociacion_PCS', ]


admin.site.register(Adscripcion, AdscripcionAdmin)


class ComiteAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'tipo', 'miembro1', 'miembro2', 'miembro3']
    search_fields = ['estudiante__user__first_name',
                     'estudiante__user__last_name']


admin.site.register(Comite, ComiteAdmin)


class CursoAdmin(admin.ModelAdmin):
    list_display = ['clave', 'asignatura',
                    'tipo', 'creditos', 'horas_semestre']


admin.site.register(Curso, CursoAdmin)


class CatedraAdmin(admin.ModelAdmin):
    list_display = ['curso', 'profesor', 'semestre', 'year']


admin.site.register(Catedra, CatedraAdmin)


class GradoAcademicoAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ['grado_obtenido', 'nivel', 'user',
                    'institucion', 'fecha_obtencion']


admin.site.register(GradoAcademico, GradoAcademicoAdmin)


class InstitucionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'suborganizacion', 'dependencia_UNAM']


admin.site.register(Institucion, InstitucionAdmin)


class SesionAdmin(admin.ModelAdmin):
    search_fields = ['descripcion', 'fecha']
    list_display = ['fecha', 'descripcion',
                    'unificado']

    def unificado(self, sesion):
        return sesion.as_a()

    unificado.allow_tags = True
    unificado.short_description = 'Ver'


admin.site.register(Sesion, SesionAdmin)


class SolicitudAdmin(admin.ModelAdmin):
    search_fields = ['resumen', 'fecha_creacion',
                     'solicitante__first_name',
                     'solicitante__last_name']
    list_display = ['resumen', 'user', 'fecha_creacion',
                    'unificado', 'estado', 'tipo']

    def unificado(self, solicitud):
        return solicitud.as_a()

    def user(self, solicitud):
        return solicitud.solicitante.perfil

    unificado.allow_tags = True
    unificado.short_description = 'Ver'


admin.site.register(Solicitud, SolicitudAdmin)


class PerfilAdmin(admin.ModelAdmin):
    list_display = [
        'fullname',
        'telefono',
        'email',
        'academico_unificado'
       ]
    search_fields = ['user__first_name', 'user__last_name']

    def email(self, obj):
        return obj.user.email

    def fullname(self, obj):
        name = obj.user.get_full_name()
        if name:
            return name
        else:
            return obj.user.username

    def academico_unificado(self, perfil):
        if hasattr(perfil.user, 'academico'):
            return perfil.user.academico.as_a()
        else:
            return ""
    academico_unificado.allow_tags = True


admin.site.register(Perfil, PerfilAdmin)


admin.site.register(CampoConocimiento)
admin.site.register(LineaInvestigacion)
# admin.site.register(Comentario)
admin.site.register(Proyecto)
admin.site.register(Dictamen)
