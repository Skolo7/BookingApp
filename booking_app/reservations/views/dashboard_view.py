from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count
from django.db.models.functions import TruncDate
from reservations.models.reservations import Reservation
from reservations.models.products import Desk, Room, Parking
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta


class CustomDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservations = Reservation.objects.all()
        types_data = []

        desk_count = Reservation.objects.filter(type='DESK').count()
        room_count = Reservation.objects.filter(type='ROOM').count()
        parking_count = Reservation.objects.filter(type='PARKING').count()

        types_data = [
            {'type': 'Desk', 'count': desk_count},
            {'type': 'Room', 'count': room_count},
            {'type': 'Parking', 'count': parking_count}
        ]

        df_types = pd.DataFrame(types_data)

        fig1 = px.bar(
            df_types,
            x='type',
            y='count',
            title='Reservations by Type',
            labels={'type': 'Type', 'count': 'Number of Reservations'},
            color='type',
            color_discrete_map={
                'Desk': '#3498db',
                'Room': '#2ecc71',
                'Parking': '#9b59b6'
            },
            template='plotly_white'
        )

        fig1.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12),
            height=300
        )

        total_desks = Desk.objects.count()
        reserved_desks = Reservation.objects.filter(type='DESK', end_date__gte=datetime.now().date()).count()
        total_rooms = Parking.objects.count()
        reserved_rooms = Reservation.objects.filter(type='ROOM', end_date__gte=datetime.now().date()).count()
        availability_data_desks = [
            {'resource': 'Desks Available', 'count': total_desks - reserved_desks},
            {'resource': 'Desks Reserved', 'count': reserved_desks},

        ]
        availability_data_rooms = [
            {'resource': 'Rooms Available', 'count': total_rooms - reserved_rooms},
            {'resource': 'Rooms Reserved', 'count': reserved_rooms},
        ]
        #
        # fig2 = make_subplots(rows=1, cols=2, subplot_titles=('Desks Availability', 'Parking places Availability'), specs=[[{'type': 'domain'}, {'type': 'domain'}]])
        # fig2.add_trace(go.Pie(labels=['Rooms Available', 'Rooms Reserved', 'Desks Available', 'Desks Reserved'], values=[availability_data_rooms[0]['count'],
        #                                                                                                                  availability_data_rooms[1]['count'],
        #                                                                                                                  availability_data_desks[0]['count'],
        #                                                                                                                  availability_data_desks[1]['count']], name="Desks"),
        #               1, 1)
        # fig2.add_trace(go.Pie(labels=['Rooms Available', 'Rooms Reserved', 'Desks Available', 'Desks Reserved'],
        #                       values=[availability_data_rooms[0]['count'],
        #                               availability_data_rooms[1]['count'],
        #                               availability_data_desks[0]['count'],
        #                               availability_data_desks[1]['count']], name="Parkings"),
        #                1, 2)
        #
        # fig2.update_traces(hole=.4, hoverinfo="label+percent+name")
        # fig2.update_layout(
        #     title_text="Global Emissions 1990-2011",
        #     annotations=[dict(text='Desk', x=sum(fig2.get_subplot(1, 1).x) / 2, y=0.5,
        #                       font_size=20, showarrow=False, xanchor="center"),
        #                  dict(text='Parking', x=sum(fig2.get_subplot(1, 2).x) / 2, y=0.5,
        #                       font_size=20, showarrow=False, xanchor="center")])
        #
        today = datetime.now().date()
        thirty_days_ago = today - timedelta(days=30)

        date_range = pd.date_range(start=thirty_days_ago, end=today)
        base_df = pd.DataFrame({'date': date_range})
        reservations_by_date = (
            Reservation.objects
            .filter(start_date__gte=thirty_days_ago)
            .annotate(date=TruncDate('start_date'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        trend_data = list(reservations_by_date)
        trend_df = pd.DataFrame(trend_data) if trend_data else pd.DataFrame({'date': [], 'count': []})

        if not trend_df.empty:
            trend_df['date'] = pd.to_datetime(trend_df['date'])
            merged_df = base_df.merge(trend_df, on='date', how='left').fillna(0)
        else:
            merged_df = base_df.copy()
            merged_df['count'] = 0

        fig3 = px.line(
            merged_df,
            x='date',
            y='count',
            title='Reservation Trend (Last 30 Days)',
            labels={'date': 'Date', 'count': 'Number of Reservations'},
            markers=True,
            template='plotly_white',
            line_shape='spline'
        )

        fig3.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(tickformat="%d %b"),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12),
            height=300
        )


        plot_div1 = plot(fig1, output_type='div', include_plotlyjs=True)
        # plot_div2 = plot(fig2, output_type='div', include_plotlyjs=True)
        plot_div3 = plot(fig3, output_type='div', include_plotlyjs=True)

        today = datetime.now().date()
        active_reservations = Reservation.objects.filter(end_date__gte=today).count()
        total_reservations = Reservation.objects.count()
        total_resources = Desk.objects.count() + Room.objects.count() + Parking.objects.count()
        utilization_rate = (active_reservations / total_resources * 100) if total_resources > 0 else 0


        if self.request.user.is_authenticated:
            recent_reservations = Reservation.objects.filter(
                person=self.request.user
            ).order_by('-start_date')[:5]
            context['recent_reservations'] = recent_reservations

        context.update({
            'plot_div1': plot_div1,
            # 'plot_div2': plot_div2,
            'plot_div3': plot_div3,
            'total_reservations': total_reservations,
            'active_reservations': active_reservations,
            'total_resources': total_resources,
            'utilization_rate': round(utilization_rate, 1)
        })

        return context