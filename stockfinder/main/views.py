from django.shortcuts import render
from django.http import HttpResponse

from .forms import EnterMarketCap, EnterDividend, EnterIndustry, EnterPrice, EnterPE

import yfinance as yf
from yahoo_fin import stock_info as si
from yahoofinancials import YahooFinancials
import yahoo_finance
import get_all_tickers
import pandas as pd
import lxml
import html5lib
import datetime
from alpha_vantage import alphavantage as av
import requests_html

key = 'f1a5c022eamsh4ce35ebc089c8eep19e756jsn0073c33e75ea'

# Create your views here.

def index(response):
    form = EnterMarketCap
    form2 = EnterDividend
    form3 = EnterIndustry
    form4 = EnterPrice
    form5 = EnterPE

    form9 = ""
    form10 = ""
    form11 = ""
    bla = ""

    mk = 0
    div = 0
    ind = ""
    price = 0

    if response.method == "GET" and response.GET.get('apply') == 'apply':
        form = EnterMarketCap(response.GET)
        form2 = EnterDividend(response.GET)
        form3 = EnterIndustry(response.GET)
        form4 = EnterPrice(response.GET)
        form5 = EnterPE(response.GET)

        #payload = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        #first_table = payload[0]

        #df = first_table
        #df.head()

        #symbols = df['Symbol'].values.tolist()
        ticker_list = ['FB', 'AAPL', 'FRT', 'AMZN', 'FIS', 'FITB', 'FE', 'FRC', 'FISV', 'FLT', 'FLIR', 'FLS', 'FMC',
                       'F', 'FTNT', 'FTV', 'FBHS', 'FOXA', 'FOX', 'BEN', 'FCX', 'GPS', 'GRMN', 'IT', 'GD', 'GE', 'GIS',
                       'GM', 'L', 'LOW', 'LUMN', 'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA',
                       'MKC', 'MXIM', 'MCD', 'MCK', 'MDT', 'TSLA', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA',
                       'MHK']

        if form.is_valid():
            mk = (form.cleaned_data["marketcap"])
            ck = form.cleaned_data["check"]
            sign = form.cleaned_data["sign"]
        else:
            mk = 0
            ck = False
            sign = ""

        if form2.is_valid():
            div = form2.cleaned_data["dividend"]
            ck2 = form2.cleaned_data["check2"]
            sign2 = form2.cleaned_data["sign2"]
        else:
            div = 0.0
            ck2 = False
            sign2 = ""

        if form3.is_valid():
            ind = form3.cleaned_data["industry"]
            ck3 = form3.cleaned_data["check3"]
        else:
            ind = ""
            ck3 = False

        if form4.is_valid():
            p = form4.cleaned_data["price"]
            ck4 = form4.cleaned_data["check4"]
            sign4 = form4.cleaned_data["sign4"]
        else:
            p = 0
            ck4 = False
            sign4 = ""

        if form5.is_valid():
            pe_ratio = form5.cleaned_data["pe_ratio"]
            ck5 = form5.cleaned_data["check5"]
            sign5 = form5.cleaned_data["sign5"]
        else:
            pe_ratio = 0
            ck5 = False
            sign5 = ""

        if ck is True:
            form10 = mk
        else:
            form10 = ""

        if ck4 is True:
            form9 = p
        else:
            form9 = ""

        resultMK = []
        form11 = ""

        if mk != 0 and ck is True and ck5 is False and ck4 is False and ck2 is False:
            for i in ticker_list:
                ticker = yf.Ticker(i)
                b = ticker.info["marketCap"]
                if sign == "Above":
                    if b > (mk * 1000000000):
                        resultMK.append(i)
                elif sign == "Below":
                    if b < (mk * 1000000000):
                        resultMK.append(i)

        resultDIV = []

        if div != 0 and ck is False and ck5 is False and ck4 is False and ck2 is True:
            for i in ticker_list:
                yahoo_financials = YahooFinancials(i)
                d = yahoo_financials.get_dividend_yield()
                if sign2 == "Above":
                    if d > (div / 100):
                        resultDIV.append(i)
                elif sign2 == "Below":
                    if d < (div / 100):
                        resultDIV.append(i)

        resultP = []

        if p != 0 and ck is False and ck5 is False and ck4 is True and ck2 is False:
            for i in ticker_list:
                price = si.get_live_price(i)
                if sign4 == "Above":
                    if price > p:
                        resultP.append(i)
                elif sign4 == "Below":
                    if price < p:
                        resultP.append(i)

        resultPE = []

        if div != 0 and ck is False and ck5 is True and ck4 is False and ck2 is False:
            for i in ticker_list:
                ticker = yf.Ticker(i)
                pe = ticker.info["forwardPE"]
                if sign5 == "Above":
                    if pe > pe_ratio:
                        resultPE.append(i)
                elif sign5 == "Below":
                    if pe < pe_ratio:
                        resultPE.append(i)



        intermediate = []
        resultP_MK = []

        if ck is True and ck5 is False and ck4 is True and ck2 is False:
            for i in ticker_list:
                price = si.get_live_price(i)
                if sign4 == "Above":
                    if price > p:
                        intermediate.append(i)
                elif sign4 == "Below":
                    if price < p:
                        intermediate.append(i)

            for i in intermediate:
                ticker = yf.Ticker(i)
                b = ticker.info["marketCap"]
                if sign == "Above":
                    if b > (mk * 1000000000):
                        resultP_MK.append(i)
                elif sign == "Below":
                    if b < (mk * 1000000000):
                        resultP_MK.append(i)



        if ck is True and ck5 is False and ck4 is False and ck2 is False:
            if not resultMK:
                form11 = "Your filters match no stock (From my list of 50 stocks :)"
            else:
                form11 = resultMK
        elif ck is False and ck4 is True and ck5 is False and ck2 is False:
            if not resultP:
                form11 = "Your filters match no stock (From my list of 50 stocks :)"
            else:
                form11 = resultP
        elif ck is True and ck5 is False and ck4 is True and ck2 is False:
            if not resultP_MK:
                form11 = "Your filters match no stock (From my list of 50 stocks :)"
            else:
                form11 = resultP_MK
        elif ck is False and ck5 is True and ck4 is False and ck2 is False:
            form11 = resultPE
            #if not resultDIV:
            #    form11 = "Your filters match no stock (From my list of 50 stocks :)"
            #else:
            #    form11 = resultDIV
        elif ck is False and ck5 is False and ck4 is False and ck2 is True:
            form11 = resultDIV
        elif ck is False and ck2 is False and ck4 is False and ck2 is False:
            form11 = "You didn't enter any filter, Click use to use a filter!"



    return render(response, "main/home.html", {"form": form, "form2": form2, "form3": form3, "form4": form4, "form5": form5, "form9": form9, "form10": form10, "form11": form11})


