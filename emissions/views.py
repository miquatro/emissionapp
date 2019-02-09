from django.shortcuts import render, redirect
from django.views.generic import TemplateView
import os
import zipfile, io
import requests
import xml.etree.ElementTree as ET
from .forms import CountryForm, CompareCountry
import glob

class HomeView(TemplateView):
        template_name = 'emissions/index.html'

        def get(self, request):
                if os.path.isfile('./API_SP.POP.TOTL_DS2_en_xml_v2_10401060.xml') != True:
                        url_population = "http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=xml"
                        r = requests.get(url_population)
                        z = zipfile.ZipFile(io.BytesIO(r.content))
                        z.extractall()
                if os.path.isfile('./API_EN.ATM.CO2E.KT_DS2_en_xml_v2_10401152.xml') != True:
                        url_emission = "http://api.worldbank.org/v2/en/indicator/EN.ATM.CO2E.KT?downloadformat=xml"
                        y = requests.get(url_emission)
                        k = zipfile.ZipFile(io.BytesIO(y.content))
                        k.extractall()
                return render(request, self.template_name)


class SearchView(TemplateView):
        template_name = 'emissions/search.html'

        def get(self, request):
                form = CountryForm()
                return render(request, self.template_name, {'form': form})

        def post(self, request):
                form = CountryForm(request.POST or None)
                if request.method == 'POST':
                        if form.is_valid():
                                country = request.POST.get('country')
                                year = request.POST.get('year')
                                per_capita = request.POST.get('per_capita')
                                print(country)
                                request.session['country'] = country
                                request.session['year'] = year
                                request.session['per_capita'] = per_capita
                else:
                        form = CountryForm()
                # Parsing populations file
                selectedCountry = request.session.get('country')
                selectedYear = request.session.get('year')
                per_capita = request.session.get('per_capita')
                populations = {}
                root_pop = rootPopulation()
                for child in root_pop.findall(".data/record/[field='%s']" % selectedCountry):
                        if int(child[2].text) >= int(selectedYear):
                                populations[child[2].text] = child[3].text

                #Parsing emissions file
                emissions = {}
                root_emis = rootEmission()
                for child in root_emis.findall(".data/record/[field='%s']" % selectedCountry):
                        if int(child[2].text) >= int(selectedYear):
                                emissions[child[2].text] = child[3].text

                emission_values = {k: v for k, v in emissions.items() if v is not None}
                population_values = {k: v for k, v in populations.items() if v is not None}
                emissions_per_capita = {k: round(float(emission_values[k])/float(population_values[k]) * 1000, 4) for k in emission_values}
                print(emissions_per_capita)
                context = {
                        'populations': populations,
                        'emissions': emissions,
                        'per_capita': per_capita,
                        'emissions_per_capita': emissions_per_capita,
                        'form': form,
                }
                return render(request, self.template_name, context)


class CompareView(TemplateView):
        template_name = 'emissions/compare.html'

        def get(self, request):
                form = CompareCountry()
                return render(request, self.template_name, {'form': form})

        def post(self, request):
                form = CompareCountry(request.POST or None)
                if request.method == 'POST':
                        if form.is_valid():
                                country_one = request.POST.get('country_one')
                                country_two = request.POST.get('country_two')
                                request.session['country_one'] = country_one
                                request.session['country_two'] = country_two
                else:
                        form = CompareCountry()
                selectedCountry_one = request.session.get('country_one')
                selectedCountry_two = request.session.get('country_two')
                root_emis = rootEmission()
                emissions_one = {}
                emissions_two = {}
                for child in root_emis.findall(".data/record/[field='%s']" % selectedCountry_one):
                        emissions_one[child[2].text] = child[3].text
                for child in root_emis.findall(".data/record/[field='%s']" % selectedCountry_two):
                        emissions_two[child[2].text] = child[3].text
                data = {'emissions_one': emissions_one,
                        'emissions_two': emissions_two,
                        'country_one': selectedCountry_one,
                        'country_two': selectedCountry_two,
                        'form': form,
                        }
                return render(request, self.template_name, data)

def rootPopulation():
    file_population = glob.glob("API_SP.POP.TOTL_DS2_en_xml_v2*")
    for f in file_population:
        file_population = f
    tree_pop = ET.parse(file_population)
    root_pop = tree_pop.getroot()
    return root_pop

def rootEmission():
    file_emission = glob.glob("API_EN.ATM.CO2E.KT_DS2_en_xml_v2*")
    for f in file_emission:
        file_emission = f
    tree_emis = ET.parse(file_emission)
    root_emis = tree_emis.getroot()
    return root_emis