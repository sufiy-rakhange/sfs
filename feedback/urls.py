from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # Students Urls
    path('', views.index, name="index"),
    path('login', views.student_login, name="student_login"),
    path('takemeout', views.student_logout, name="student_logout"),
    path('student/feedback/<teacher_id>/<subject_id>', views.student_feedback, name="student_feedback"),

    # Teacher Urls
    path('teacher/', views.teacher_index, name="teacher_index"),
    path('teacher/login', views.teacher_login, name="teacher_login"),
    path('teacher/logout', views.teacher_logout, name="teacher_logout"),
    path('teacher/register', views.register, name="register"),
    path('teacher/regular/suggestions/<id>', views.regular_suggestions, name="regular_suggestions"),
    path('teacher/defaulter/suggestions/<id>', views.defaulter_suggestions, name="defaulter_suggestions"),
    path('teacher/all/suggestions', views.all_suggestions, name="all_suggestions"),
    path('teacher/suggestions/<id>/<t_id>', views.hod_suggestions, name="hod_suggestions"),

    # Subject Urls
    path('teacher/add/subject', views.add_subject, name="add_subject"),
        # Thoery
    path('teacher/subject/theory/details/<id>', views.subject_details, name="subject_details"),
    path('teacher/subject/theory/edit', views.subject_edit, name="subject_edit"),
    path('teacher/subject/theory/delete/<id>', views.subject_delete, name="subject_delete"),
    path('teacher/subject/theory/deletion', views.subject_deletion, name="subject_deletion"),
        # Practical
    path('teacher/subject/practical/details/<id>', views.practical_details, name="practical_details"),
    path('teacher/subject/practical/edit', views.practical_edit, name="practical_edit"),
    path('teacher/subject/practical/delete/<id>', views.practical_delete, name="practical_delete"),
    path('teacher/subject/practical/deletion', views.practical_deletion, name="practical_deletion"),

    # Admin Urls
    path('admin/', views.sfsadmin_index, name="sfsadmin_index"),
    path('admin/login', views.sfsadmin_login, name="sfsadmin_login"),
    path('admin/logout', views.sfsadmin_logout, name="sfsadmin_logout"),
    path('admin/upload', views.student_upload, name="student_upload"),

    # Teacher Verification
    path('admin/moderate', views.moderate, name="moderate"),
    path('admin/moderate/<id>', views.moderate_details, name="moderate_details"),
    path('admin/approve', views.approve, name="approve"),
    path('admin/decline', views.decline, name="decline"),
    path('admin/details', views.details, name="details"),

    # CRUD of Students
    path('admin/student/list', views.student_list, name="student_list"),
    path('admin/student/details/<id>', views.student_details, name="student_details"),
    path('admin/student/edit', views.student_edit, name="student_edit"),
    path('admin/student/delete/<id>', views.student_delete, name="student_delete"),
    path('admin/student/deletion', views.student_deletion, name="student_deletion"),

    # CRUD of Teachers
    path('admin/teacher/list', views.teacher_list, name="teacher_list"),
    path('admin/teacher/details/<id>', views.teacher_details, name="teacher_details"),
    path('admin/teacher/edit', views.teacher_edit, name="teacher_edit"),
    path('admin/teacher/delete/<id>', views.teacher_delete, name="teacher_delete"),
    path('admin/teacher/deletion', views.teacher_deletion, name="teacher_deletion"),
    # path('admin/teacher/search', views.teacher_search, name="teacher_search"),

    # Password reset for teacher
    path('password_reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='feedback/password/password_reset_done.html'),
        name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='feedback/password/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password_reset/',
        auth_views.PasswordResetView.as_view(template_name='feedback/password/password_reset_form.html'),
        name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='feedback/password/password_reset_complete.html'),
         name='password_reset_complete'),
    # Change password for teacher
    path('password_change/',
        auth_views.PasswordChangeView.as_view(template_name='feedback/password/password_change_form.html'),
        name='password_change',
    ),
    path('password_change/done',
        auth_views.PasswordChangeDoneView.as_view(template_name='feedback/password/password_change_done.html'),
        name='password_change_done'
    ),

    # Password reset for admin
    path('admin/password_reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='feedback/admin/password_reset_done.html'),
        name='admin_password_reset_done'),
    path('admin/password_reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='feedback/admin/password_reset_confirm.html'),
        name='admin_password_reset_confirm'),
    path('admin/password_reset/',
        auth_views.PasswordResetView.as_view(template_name='feedback/admin/password_reset_form.html'),
        name='admin_password_reset'),
    path('admin/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='feedback/admin/password_reset_complete.html'),
         name='admin_password_reset_complete'),
    # Change password for admin
    path('admin/password_change/',
        auth_views.PasswordChangeView.as_view(template_name='feedback/admin/password_change_form.html'),
        name='password_change',
    ),
    path('admin/password_change/done',
        auth_views.PasswordChangeDoneView.as_view(template_name='feedback/admin/password_change_done.html'),
        name='password_change_done'
    ),
]