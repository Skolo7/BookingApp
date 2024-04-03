# from django.shortcuts import render, redirect
# from django.utils import timezone
#
# from django.views import View
#
# from ..models.products import Room
# from ..models.reservations import Reservation
# from ..forms import FilterAvailabilityForm, ReserveForm
# from django.contrib.auth.mixins import LoginRequiredMixin
#
#
# class FilterRoomView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         form = FilterAvailabilityForm(request.POST)
#         print(form)
#         print(form.is_valid())
#         start_date, end_date = form.cleaned_data['start_date'], form.cleaned_data['end_date']
#         request.session['start_date'] = start_date.strftime("%Y-%m-%d")
#         request.session['end_date'] = end_date.strftime("%Y-%m-%d")
#         return redirect('parking')
#
#
# class ReserveParkingView(LoginRequiredMixin, View):
#     template_name = 'reserve_parking.html'
#
#     def get(self, request, *args, **kwargs):
#         today = timezone.now().date()
#         reservation_form = ReserveForm()
#
#         start_date_str = request.session.get('start_date')
#         end_date_str = request.session.get('end_date')
#
#         if start_date_str and end_date_str:
#             start_date = timezone.datetime.strptime(start_date_str, "%Y-%m-%d").date()
#             end_date = timezone.datetime.strptime(end_date_str, "%Y-%m-%d").date()
#             available_parkings = self.get_available_parkings(start_date, end_date)
#         else:
#             available_parkings = self.get_default_parkings(today)
#         return self.render_with_form_and_default_parkings(request, reservation_form, available_parkings, today)
#
#     def post(self, request, *args, **kwargs):
#         form = ReserveForm(request.POST)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.person = self.request.user
#             parking_number = form.data['parking_number']
#             reservation.parking = Parking.objects.get(number=parking_number)
#             reservation.save()
#             self.get(request)
#         else:
#             print(form.errors)
#         return self.get(request)
#
#     def get_filtered_parkings(self, form):
#         start_date = form.cleaned_data['start_date']
#         end_date = form.cleaned_data['end_date']
#         return self.get_available_parkings(start_date=start_date, end_date=end_date)
#
#     @staticmethod
#     def get_default_parkings(today):
#         reservations_today = Reservation.objects.filter(start_date__range=(today, today)).select_related('parking')
#         reserved_parkings_today = {reserv.parking for reserv in reservations_today}
#         all_parkings = set(Parking.objects.all())
#         return all_parkings - reserved_parkings_today
#
#     def render_with_form_and_default_parkings(self, request, form, parkings, today):
#         context = {
#             'all_parkings': parkings,
#             'today': today,
#             'form': form,
#             'date_form': ReserveForm()
#         }
#         return render(request, self.template_name, context=context)
#
#     def get_available_parkings(self, start_date, end_date):
#         available_parkings = set(Parking.objects.all()) - {reserv.parking for reserv in
#                                                            Reservation.objects.filter(
#                                                                start_date__range=(start_date, end_date),
#                                                                end_date__range=(start_date, end_date)).select_related(
#                                                                'parking')}
#         return available_parkings
