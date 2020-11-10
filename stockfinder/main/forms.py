from django import forms

class EnterMarketCap(forms.Form):
    check = forms.BooleanField(label="Use", required=False, initial=False)
    sign = forms.ChoiceField(label="Market Cap ", choices=[("Above", "Above"), ("Below", "Below")], required=False)
    marketcap = forms.IntegerField(label="", required=False, min_value=0, max_value=5000)

class EnterDividend(forms.Form):
    check2 = forms.BooleanField(label="Use", required=False, initial=False)
    sign2 = forms.ChoiceField(label="Dividend Yield ", choices=[("Above", "Above"), ("Below", "Below")], required=False)
    dividend = forms.DecimalField(label="", required=False, min_value=0, max_value=20,)

class EnterIndustry(forms.Form):
    check3 = forms.BooleanField(label="Use", required=False, initial=False)
    sign3 = forms.ChoiceField(label="Industry ", choices=[("Including", "Including"), ("Excluding", "Excluding")],
                              required=False)
    industry = forms.ChoiceField(label="", choices=[("Technology", "Technology"), ("Consumer Cyclical",
                "Consumer Cyclical"), ("Healthcare", "Healthcare "), ("Basic Materials", "Basic Materials ")],
                                 required=False)

class EnterPrice(forms.Form):
    check4 = forms.BooleanField(label="Use", required=False, initial=False)
    sign4 = forms.ChoiceField(label="Stock Price ", choices=[("Above", "Above"), ("Below", "Below")], required=False)
    price = forms.IntegerField(label="", required=False, min_value=0, max_value=5000)

class EnterPE(forms.Form):
    check5 = forms.BooleanField(label="Use", required=False, initial=False)
    sign5 = forms.ChoiceField(label="Forward PE ", choices=[("Above", "Above"), ("Below", "Below")], required=False)
    pe_ratio = forms.IntegerField(label="", required=False, min_value=0, max_value=1000)



