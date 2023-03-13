import streamlit as st
import numpy as np
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie, Line
from streamlit_echarts import st_pyecharts
from datetime import datetime, timedelta
from database import run_query
from st_settings import main_page_settings

main_page_settings()
wig_twenty_companies = ["Allegro", "Asseco", "Pekao", "CCC", "CD Projekt", "Cyfrowy Polsat", "Dino Polska", "JSW", "Grupa Kęty","KGHM", 
                        "LPP", "mBank", "Orange Polska", "Pepco", "PGE", "KRUK", "PKN Orlen", "PKO BP", "PZU", "Santander"]

fio = ["AGIO Akcji Plus", "Allianz Akcji Małych i Średnich Spółek", "Allianz Selektywny", "BNP Paribas Dynamicznego Inwestowania", "BPS Akcji", "Credit Agricole Akcyjny", "Esaliens Akcji", "Generali Akcje Małych i Średnich Spółek",
       "Generali Akcje Wzrostu", "Generali Korona Akcje", "Pekao Akcji Aktywna Selekcja", "Pekao Dynamicznych Spółek", "PKO Akcji Plus", "PKO Akcji Rynku Polskiego", "Santander Akcji Małych i Średnich Spółek",
       "Santander Akcji Polskich", "Skarbiec Akcja"]  
wibor_values = st.secrets["WIBOR_1Y_url"] 
wibor_query = run_query(f'SELECT * FROM "{wibor_values}"')
wibor_df = pd.DataFrame(wibor_query)
wibor_df = wibor_df.set_index('Date')
beta = {}
alpha = {}
var_assets_share_dict = {key: None for key in wig_twenty_companies}
disable_the_multiselect = False
session = st.session_state

def daily_return(df, start, end):
    df = df.loc[start:end]
    daily_returns = df.pct_change().iloc[1:]
    return daily_returns
  
def calculate_portfolio_value_based_on_investment_sum(investments):
    return sum(investments.values())

def filter_the_dict(dict_to_filter): 
  filtered_dict = {k: v for k, v in dict_to_filter.items() if v}
  return filtered_dict

def calculate_CAPM(rf, rm, beta):
  expected_return = {}
  for i in beta.keys():
    expected_return[i] = (rf + (beta[i] * (rm-rf)))
  return expected_return

def CAPM_calculate_portfolio_ER(capm_dict, weights_dict):
  portfolio_ER = sum(weights_dict[k] * capm_dict[k] for k in weights_dict.keys() & capm_dict.keys())
  return portfolio_ER

def calculate_weights(filtered_dict, portfolio_sum):
  stocks_weights = {key: round(filtered_dict[key] / portfolio_sum, 2) for key in filtered_dict}
  return stocks_weights

def portfolio_beta(beta_dict, weights):
  return sum(weights[k] * beta_dict[k] for k in weights.keys() & beta_dict.keys())

def expected_mean_return(stocks_mean_return, weights):
  return sum(weights[k] * stocks_mean_return[k] for k in weights.keys() & stocks_mean_return.keys())

def latex_sidebar(): #TODO
  with st.sidebar:
    st.title("Formulas used:")
    st.latex(r'''\textbf{Capital Market Line (CML)}''')
    st.latex(r'''\textbf{CML}: E(R_P) = R_f + \frac{(E(R_M) - R_f)}{\sigma_M} \cdot \sigma_P''') #* CML
    st.write("*where:*")
    st.latex(r'''E(R_P) - expected\,return\,of\,the\,efficient\,portfolio\,P''')
    st.latex(r'''R_f - risk-free\,rate\,''')
    st.latex(r'''E(R_M) - expected\,return\,of\,the\,market\,portfolio\,M,''')
    st.latex(r'''σ_M - risk\,of\,the\,market\,portfolio\,M,''')
    st.latex(r'''σ_P - risk\,of\,the\,efficient\,portfolio\,P''')
    st.latex(r'''\textbf{Security Market Line (SML)}''')
    st.latex(r'''\textbf{SML}: E(R_P) = R_f + β_P \cdot (E(R_M) - R_f)''') #* SML
    st.write("*where:*")
    st.latex(r'''E(R_P) - expected\,return\,of\,portfolio\,P,''')
    st.latex(r'''R_f - risk-free\,rate\,''')
    st.latex(r'''β_P - Sharpe's\,beta\,coefficient\,of\,portfolio\,P,''')
    st.latex(r'''E(R_M) - expected\,return\,of\,the\,market\,portfolio\,M.''')
    st.latex(r'''\textbf{Left side of SML and CML:}''')
    st.latex(r'''L_{SML} = L_{CML} = E(R_P)''')
     
def get_prices_data(prices_url: str):
    close_prices = st.secrets[prices_url]
    close_query = run_query(f'SELECT * FROM "{close_prices}"')
    stocks_df = pd.DataFrame(close_query)
    stocks_df = stocks_df.set_index('Date')
    stocks_df = stocks_df.rename(lambda x: x.replace('_', ' '), axis=1)
    stocks_daily_range_returns = daily_return(stocks_df, start_date, end_date)
    stocks_mean_er = stocks_daily_range_returns.mean()
    market_daily_range_returns = stocks_daily_range_returns["WIG20"]
    market_mean = market_daily_range_returns.mean()
    return stocks_df, stocks_daily_range_returns, stocks_mean_er, market_daily_range_returns, market_mean

def create_date_input(col, label, start_value):
    if funds_checkbox:
        min_date_value = datetime(2018, 1, 3)
        max_date_value = datetime(2022, 11, 24)
    else:
        min_date_value = datetime(2021, 5, 26)
        max_date_value = datetime(2022, 12, 30)

    date_value = col.date_input(label, value=start_value, min_value=min_date_value, max_value=max_date_value)

    if date_value.isoweekday() == 6:
        date_value -= timedelta(days=1)
    elif date_value.isoweekday() == 7:
        date_value -= timedelta(days=2)

    return date_value



funds_checkbox = st.checkbox("Switch from stocks to funds.")
col1, col2 = st.columns(2)
if 'assets_share_dict' not in session:
    session["assets_share_dict"] = {key: 1000 for key in wig_twenty_companies}
    
start_date = create_date_input(col1, "Start date", datetime(2022, 1, 1))
end_date = create_date_input(col2, "End date", datetime(2022, 7, 1))

if start_date > end_date:
    st.error("Start date is higher than the end date!")
    disable_the_multiselect = True
    st.stop()
elif start_date == end_date:
    st.error("Time period is equal to 0. Same dates chosen.")
    disable_the_multiselect = True
    st.stop()
    
assets_dict = {
    True: {"assets": fio, "url": "Funds_url"},
    False: {"assets": wig_twenty_companies, "url": "Stocks_url"}
}

if 'assets_share_dict' not in session:
    session["assets_share_dict"] = {key: 1000 for key in assets_dict[funds_checkbox]["assets"]}

try:
    stocks_df, stocks_daily_range_returns, stocks_mean_er, market_daily_range_returns, market_mean = get_prices_data(assets_dict[funds_checkbox]["url"])
except IndexError:
    st.error("There were no trading sessions in the chosen time period. Choose a different period.")
    st.stop()

assets_multiselect = st.multiselect(
    f"Select {'funds' if funds_checkbox else 'companies that are part of the WIG20 index'} that you want to include in your investment portfolio.",
    assets_dict[funds_checkbox]["assets"],
    disabled=disable_the_multiselect
)
  
if assets_multiselect:
    line_chart = (
        Line()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Prices"),
            xaxis_opts=opts.AxisOpts(name="Date", axislabel_opts=opts.LabelOpts(color="black")),
            yaxis_opts=opts.AxisOpts(name="Price", axislabel_opts=opts.LabelOpts(color="black"), is_scale=True),
            legend_opts=opts.LegendOpts(pos_top=True, padding=10, type_="scroll"),
            datazoom_opts=opts.DataZoomOpts(is_show=True, type_="inside"),
        )
        .add_xaxis(stocks_df[start_date:end_date].index.tolist())
        .add_yaxis("WIG20", stocks_df["WIG20"].loc[start_date:end_date], is_selected=False, is_symbol_show=False)
    )
    for stock in assets_multiselect:
        prices = [f"{value:.2f}" for value in stocks_df[stock].loc[start_date:end_date]]
        line_chart.add_yaxis(stock, prices, is_symbol_show=False).set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b}: {c}")
        )
    st_pyecharts(line_chart)
    expander =  st.expander("Enter the amount that you want to allocate to each asset.", expanded=True)
    with expander:
      for i in assets_multiselect:
        b, a = np.polyfit(stocks_daily_range_returns['WIG20'], stocks_daily_range_returns[i], 1)
        beta[i] = b
        alpha[i] = round(a, 4)
        var_assets_share_dict[i] = st.number_input("Asset: {} | Alpha: {} | Beta: {:.2f} | Price: {:.2f} PLN".format(i, alpha[i], beta[i], stocks_df[i].loc[end_date]), min_value=0, step=100, value=session.assets_share_dict[i])
        session.assets_share_dict[i] = var_assets_share_dict[i]
    #filter the dictionary to get only values picked by user
    var_assets_share_dict = filter_the_dict(var_assets_share_dict)
    weights = calculate_weights(var_assets_share_dict, calculate_portfolio_value_based_on_investment_sum(var_assets_share_dict))
    risk_free_rate = (wibor_df["Close"].loc[end_date])/(365)
    capm_values = calculate_CAPM(risk_free_rate, market_mean, beta)
    portfolio_beta_ = portfolio_beta(beta, weights)
    if expander.button("Go to the next step"):
      dict_pandas_df = {'Przeznaczona suma (PLN)': var_assets_share_dict.values(), 'Weight in the portfolio': weights.values(), 'Beta': beta.values(), 'Alpha': alpha.values()}#, 'Expected daily return CAPM:': capm_values.values()}
      pand_df = pd.DataFrame(dict_pandas_df, index=assets_multiselect)
      p = (
        Pie()
        .set_global_opts(
          title_opts=opts.TitleOpts("Portfolio composition with a value of: {} PLN".format(calculate_portfolio_value_based_on_investment_sum(var_assets_share_dict))),
          legend_opts=opts.LegendOpts(is_show=False)
        )
        .add("", [list(item) for item in weights.items()], is_clockwise=True)
      )
      st_pyecharts(p)
      SML, CML = st.columns(2)
      expec_mean_return = expected_mean_return(stocks_mean_er, weights)
      with SML:
        st.latex(r'\textbf{SML:}')
        st.latex(r'''Question,\,whether\,L_{SML}≈R_{SML}?''')
        st.latex("R_f = {:.2f}".format(risk_free_rate))
        st.latex("E(R_m) = {:.4f}".format(market_mean))
        st.latex("β_P = {:.2f}".format((portfolio_beta_)))
        st.latex("Left\,side\,of\,SML = {}".format(round(expec_mean_return, 4)))
        st.latex("Right\,side\,of\,SML = {}".format(round(CAPM_calculate_portfolio_ER(capm_values, weights), 4)))
        st.latex(r'\footnotesize{How\,to\,interpret\,the\,question?}')
        st.markdown('If **YES**, then we can say that portfolio P was **well-valued** during the analyzed period.')
        st.markdown('If **NO**, then we consider two possible cases:')
        st.markdown('If $L_{SML}$ < $P_{SML}$ then portfolio P was **overvalued** (unattractive)')
        st.markdown('If $L_{SML}$ > $P_{SML}$ then portfolio P was **undervalued** (attractive)')
      with CML:
        st.latex(r'\textbf{CML:}')
        st.latex(r'''Question,\,whether\,L_{CML}≈R_{CML}?''')
        # Calculating the covariance matrix of selected assets' daily returns
        covariance = np.cov(stocks_daily_range_returns[assets_multiselect].fillna(0).T)
        # Getting the portfolio weights
        portfolio_ = weights.values()
        portfolio_numpy_data = list(portfolio_)
        portfolio_numpy = np.array(portfolio_numpy_data)
        # Calculating portfolio volatility
        portfolio_volatility = np.sqrt(np.dot(np.dot(portfolio_numpy, covariance), portfolio_numpy.T))
        # Getting the standard deviation of market daily returns
        market_standard_deviation = np.std(market_daily_range_returns)
        # Calculating the expected return of the portfolio using the Capital Market Line (CML) formula
        r_CML = risk_free_rate+((market_mean-risk_free_rate)/market_standard_deviation)*portfolio_volatility
        # Displaying the risk-free rate, expected market return, portfolio volatility and expected return
        st.latex("R_f = {:.2f}".format(risk_free_rate))
        st.latex("E(R_m) = {:.4f}".format(market_mean))
        st.latex("σ_P = {}, σ_M = {}".format(round(portfolio_volatility, 4), round(market_standard_deviation, 4)))
        st.latex("Left\,side\,of\,CML = {}".format(round(expec_mean_return, 4))) 
        st.latex("Right\,side\,of\,CML = {}".format(round(r_CML, 4)))
        st.latex(r'\footnotesize{How\,to\,interpret\,the\,question?}')
        # Displaying the interpretation of the question based on the calculated values
        st.markdown('If **YES**, we can conclude that portfolio P was efficient during the analyzed period.')
        st.markdown('If **NO**, we can conclude that portfolio P was not efficient during the analyzed period.')

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

latex_sidebar()