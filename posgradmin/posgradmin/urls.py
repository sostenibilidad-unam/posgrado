# coding: utf-8

from django.conf.urls import url, include
from django.contrib import admin

from posgradmin.views import PerfilEditar, PerfilDetail, \
    PerfilAcademicoDetail, PerfilProfesorDetail, PerfilProfesorEditar,\
    AcademicoActividadView, AcademicoResumenCVView, AcademicoPerfilView, \
    InicioView, \
    GradoAcademicoAgregar, GradoAcademicoEliminar, InstitucionAgregarView, \
    AdscripcionEliminar, AdscripcionAgregar, AsociacionAgregar, \
    EstudianteSortableView, AcademicoSortableView, \
    UserDetail, PerfilComite, \
    PerfilEstudianteDetail, AcademicoInvitar, AcademicoSearch, \
    TogglePerfilEditar

from posgradmin.views_academico import \
    MisEstudiantesView, EligeAsignatura, SolicitaCurso, \
    AcademicoAutocomplete, CursoView, MisCursos, ProponerAsignatura, CursoConstancia

from posgradmin.views_estudiante import CambiarProyectoView

from posgradmin.views_asistente import SesionesListView, SesionDetail # EstudianteCargar

from posgradmin.views_solicitud import SolicitudCambiarEstado, \
    SolicitudNuevaView, SolicitudDetail, SolicitudDictaminar, \
    SolicitudComment, SolicitudAgendar, \
    SolicitudAnexo, SolicitudSortableView

from django.conf.urls.static import static

from posgradmin.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    url(r'^admin/posgradmin/toggle_perfil_editar/', TogglePerfilEditar.as_view(),
        name="toggle_perfil_editar"),

    url(r'^admin/posgradmin/academico/invitar/', AcademicoInvitar.as_view(),
        name="academico_invitar"),

    url(r'^admin/', admin.site.urls),

    url('^accounts/', include('allauth.urls')),

    url(r'^export_action/', include(("export_action.urls", 'export_action'),
                                     namespace="export_action")),

    url(r'^institucion/agregar/(?P<devolver>[\w-]+)/',
        InstitucionAgregarView.as_view(),
        name="agregar_institucion"),

    url(r'^inicio/academico/perfil',
        AcademicoPerfilView.as_view(),
        name="academico_perfil"),

    url(r'^inicio/academico/resumen',
        AcademicoResumenCVView.as_view(),
        name="academico_resumen"),

    url(r'^inicio/academico/actividad',
        AcademicoActividadView.as_view(),
        name="academico_actividad"),

    url(r'^inicio/perfil/editar$',
        PerfilEditar.as_view(),
        name="editar_perfil"),

    url(r'^inicio/perfil/eliminar-grado/(?P<pk>[0-9]+)$',
        GradoAcademicoEliminar.as_view(),
        name="eliminar_grado"),

    url(r'^inicio/perfil/eliminar-adscripcion/(?P<pk>[0-9]+)$',
        AdscripcionEliminar.as_view(),
        name="eliminar_adscripcion"),

    url(r'^inicio/perfil/agregar-grado$',
        GradoAcademicoAgregar.as_view(),
        name="agregar_grado"),

    url(r'^inicio/perfil/agregar-adscripcion$',
        AdscripcionAgregar.as_view(),
        name="agregar_adscripcion"),

    url(r'^inicio/perfil/agregar-asociacion$',
        AsociacionAgregar.as_view(),
        name="agregar_asociacion"),

    url(r'^inicio/perfil/comite/(?P<username>.+)$',
        PerfilComite.as_view(),
        name="perfilcomite"),

    url(r'^inicio/perfil/$',
        PerfilDetail.as_view(),
        name='perfil'),

    url(r'^inicio/perfil-estudiante/$',
        PerfilEstudianteDetail.as_view(),
        name='perfil_estudiante'),

    url(r'^inicio/perfil-academico/$',
        PerfilAcademicoDetail.as_view(),
        name='perfil_academico'),

    url(r'^inicio/perfil-profesor/$',
        PerfilProfesorDetail.as_view(),
        name='perfil_profesor'),

    url(r'^inicio/perfil-profesor/editar',
        PerfilProfesorEditar.as_view(),
        name="perfil_profesor_editar"),

    url(r'^inicio/estudiantes/mis$',
        MisEstudiantesView.as_view(),
        name="mis_estudiantes"),

    # url(r'^inicio/estudiantes/cargar$',
    #     EstudianteCargar.as_view(),
    #     name="cargar_estudiantes"),

    url(r'^inicio/estudiantes/$',
        EstudianteSortableView.as_view(),
        name="lista_estudiantes"),

    url(r'^inicio/academicos/$',
        AcademicoSortableView.as_view(),
        name="lista_academicos"),

    url(r'^inicio/academicos/search/$',
        AcademicoSearch.as_view(),
        name="academicos_search"),

    # url(r'^inicio/catedras/$',
    #     CatedraSortableView.as_view(),
    #     name="lista_catedras"),

    url(r'^inicio/solicitudes/$',
        SolicitudSortableView.as_view(),
        name="solicitudes"),

    url(r'^inicio/solicitudes/(?P<pk>[0-9]+)/dictaminar$',
        SolicitudDictaminar.as_view(),
        name="dictaminar"),

    url(r'^inicio/solicitudes/(?P<pk>[0-9]+)/comentar$',
        SolicitudComment.as_view()),

    url(r'^inicio/solicitudes/(?P<pk>[0-9]+)/agendar$',
        SolicitudAgendar.as_view()),

    url(r'^inicio/solicitudes/(?P<pk>[0-9]+)/estado/(?P<estado>[\w-]+)$',
        SolicitudCambiarEstado.as_view()),

    url(r'^inicio/solicitudes/(?P<pk>[0-9]+)/anexar$',
        SolicitudAnexo.as_view()),

    url(r'^inicio/solicitudes/(?P<pk>[0-9]+)/cambiar-proyecto$',
        CambiarProyectoView.as_view(),
        name="cambiar_proyecto"),

    url(r'^inicio/solicitudes/(?P<pk>[0-9]+)/$',
        SolicitudDetail.as_view(),
        name="solicitud_detail"),

    url(r'^inicio/solicitudes/e/([\w-]+)/$',
        SolicitudSortableView.as_view(),
        name="solicitudes_estado"),

    url(r'^inicio/solicitudes/nueva',
        SolicitudNuevaView.as_view(),
        name='solicitud_nueva'),

    url(r'^inicio/$',
        InicioView.as_view(),
        name="inicio"),

    url(r'^inicio/sesiones/(?P<pk>[0-9]+)/$',
        SesionDetail.as_view(),
        name="sesion_detail"),

    url(r'^inicio/sesiones/$',
        SesionesListView.as_view(),
        name='lista_sesiones'),

    url(r'^inicio/usuario/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(),
        name="user_detail"),

    url('^inicio/', InicioView.as_view()),

    url(
        r'^academico-autocomplete/$',
        AcademicoAutocomplete.as_view(),
        name='academico-autocomplete',
        ),

    url('^convocatoria-cursos/(?P<pk>[0-9]+)/asignatura/(?P<as_id>[0-9]+)/',
        SolicitaCurso.as_view(),
        name="solicita_curso"),

    url('^convocatoria-cursos/(?P<pk>[0-9]+)/',
        EligeAsignatura.as_view(),
        name="elige_asignatura"),

    url('^cursos/mis/',
        MisCursos.as_view(),
        name="mis_cursos"),

    url('^cursos/(?P<pk>[0-9]+)/constancia/',
        CursoConstancia.as_view(),
        name="curso_constancia"),

    url('^cursos/(?P<pk>[0-9]+)/',
        CursoView.as_view(),
        name="curso"),

    url('^proponer-asignatura/',
        ProponerAsignatura.as_view(),
        name="proponer_asignatura"),


] + static(MEDIA_URL, document_root=MEDIA_ROOT)


# ./coordinacion/alimentar_saep.md
# ./coordinacion/oficios_para_firma_de_los_miembros_del_Jurado.md
