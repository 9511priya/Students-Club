from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from studentsapp import views as sview

urlpatterns = [
                  path('', sview.index_page, name="index_login"),
                  path('register', sview.register, name="register"),
                  path('login', sview.login, name="login"),
                  path('home', sview.home_page, name="home"),
                  # EVENTS
                  path('add_events', sview.add_events, name="add_events"),
                  path('events_update/<str:event_id>', sview.events_update, name="events_update"),
                  path('events_delete/<str:event_id>', sview.events_delete, name="events_delete"),
                  path('events_register/<str:event_id>', sview.register_for_event, name="events_register"),
                  path('events_deregister/<str:event_id>', sview.deregister_for_event, name="events_deregister"),
                  path('event_reg_stu/<str:event_id>', sview.event_registered_students_list, name="event_reg_stu"),
                  # SPORTS
                  path('add_sports', sview.add_sports, name="add_sports"),
                  path('sports_update/<str:sport_id>', sview.sports_update, name="sports_update"),
                  path('sports_delete/<str:sport_id>', sview.sports_delete, name="sports_delete"),
                  path('sports_register/<str:sport_id>', sview.register_for_sport, name="sports_register"),
                  path('sports_deregister/<str:sport_id>', sview.deregister_for_sport, name="sports_deregister"),
                  path('sports_reg_stu/<str:sport_id>', sview.sport_registered_students_list, name="sport_reg_stu"),
                  # ACCOMMODATION
                  path('add_accommodation', sview.accommodation_get_post, name="add_accommodation"),
                  path('acc_update/<str:acc_id>', sview.accommodation_update, name="acc_update"),
                  path('acc_delete/<str:acc_id>', sview.accommodation_delete, name="acc_delete"),
                  path('logout', sview.logout, name="logout"),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
