import csv

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView

from ffooty.forms import LoginForm, AuctionFileUploadForm, PlayerFileUploadForm
from ffooty.functions import (
    get_team_dict, get_week, update_players_json, update_weekly_scores,
    reset_for_new_season, initialise_players
)
from ffooty.models import Player, Team


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class IndexView(LoginRequiredMixin, View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class LoginView(View):
    form_class = LoginForm
    template_name = "login.html"
    initial = {}

    def get(self, request):
        if 'username' in request.COOKIES:
            self.initial['username'] = request.COOKIES['username']
            self.initial['remember_me'] = True
        form = self.form_class(initial=self.initial)  # TODO initial from cookie
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            response = HttpResponseRedirect(reverse('home'))
            if form.cleaned_data['remember_me']:
                response.set_cookie('username', form.cleaned_data['username'])
            else:
                response.delete_cookie('username')
            return response
        else:
            # Return an 'invalid login' error message.
            return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


class AuctionFileUploadView(LoginRequiredMixin, TemplateView):
    template_name = 'auction_file_upload.html'

    def get_context_data(self, **kwargs):
        """
        Add the file upload form to the context.
        """
        context = super(AuctionFileUploadView, self).get_context_data(**kwargs)
        context.update({'file_upload_form': AuctionFileUploadForm})
        return context

    def post(self, request, *args, **kwargs):
        form = AuctionFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            reader = csv.reader(uploaded_file)

            for row in reader:
                # each row is expected to be a list: [<code>, <team_id>, <sale>]
                print(row)
                code = int(row[0])
                team_id = int(row[1])
                sale = float(row[2])

                # get the player and update it
                p = Player.objects.get(code=code)
                p.team_id = team_id
                p.sale = sale
                p.save()

            # update team funds
            for team in Team.objects.all():
                team.update_funds()

            return HttpResponseRedirect('/auction_file_upload/')

        else:
            print("form not valid!")


class PlayerUpdateFileUploadView(LoginRequiredMixin, TemplateView):
    template_name = 'auction_file_upload.html'

    def get_context_data(self, **kwargs):
        """
        Add the file upload form to the context.
        """
        context = super(PlayerUpdateFileUploadView, self).get_context_data(**kwargs)
        context.update({'file_upload_form': PlayerFileUploadForm})
        return context

    def post(self, request, *args, **kwargs):
        form = PlayerFileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES['file']
            week = get_week()
            update_players_json(week, file_object=uploaded_file)
            update_weekly_scores(week)

        else:
            print("form not valid")

        return HttpResponseRedirect('/#/home/')
