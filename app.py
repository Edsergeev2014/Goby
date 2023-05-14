from flask import Flask, render_template, url_for
# from goby import Goby

from datetime import time

app = Flask(__name__)
# goby = Goby()


@app.route('/')
def index():
    return render_template("index.html")

#
# @app.route('/info')
# def info():
#     ''' Текущее время и день '''
#     current_time = goby.get_msc(goby.current_datetime(), is_datetime='date')
#
#     ''' Список активных аккаунтов '''
#     accounts = goby.get_accounts(content='list_dict')
#     # print(accounts[0])
#     account_id = accounts[0]['id']
#
#     ''' Статьи портфеля '''
#     portfolio_articles = goby.get_portfolio_articles(account_id)
#
#     ''' Баланс портфеля '''
#     balance_in_currencies = goby.get_balance(account_id)
#
#     ''' Содержание портфеля '''
#     portfolio_positions = goby.get_portfolio_positions(request=goby.request_blank(account_id=account_id), content='list_dict')
#
#     ''' Проверка активных заявок-ордеров: '''
#     orders = goby.get_orders(request=goby.request_blank(account_id=account_id), content='list_dict')
#
#     ''' Список операций в портфеле за выбранный период: '''
#     # operations = goby.get_operations(request=goby.request_blank(account_id=account_id), content='list_dict')
#
#     ''' Режим и расписание торгов на биржах '''
#     exchanges_schedules = goby.get_exchanges_activity(content='list_dict', exchanges=['MOEX',
#                                                                                       'MOEX_INVESTBOX',
#                                                                                       'MOEX_MORNING',
#                                                                                       'MOEX_PLUS',
#                                                                                       'SPB',
#                                                                                       'SPB_DE',
#                                                                                       'SPB_DE_MORNING',
#                                                                                       'SPB_EUROBONDS',
#                                                                                       'SPB_MORNING',
#                                                                                       'SPB_MORNING_WEEKEND',
#                                                                                       'SPB_RU_MORNING',
#                                                                                       'SPB_WEEKEND',
#                                                                                       ])
#
#     return render_template("info.html",
#                            current_time=current_time,
#                            accounts=accounts,
#                            account_active=account_id,
#                            portfolio_articles=portfolio_articles,
#                            balance_in_currencies=balance_in_currencies,
#                            portfolio_positions=portfolio_positions,
#                            orders=orders,
#                            # operations=operations,
#                            exchanges_schedules=exchanges_schedules
#                            )
#
#
# @app.route('/portfolio')
# def portfolio():
#     return render_template("portfolio.html")
#
#
# @app.route('/instruments')
# def instruments():
#     ''' Текущее время и день '''
#     current_time = goby.get_msc(goby.current_datetime(), is_datetime='date')
#     shares = ['FNKO', 'HSC', 'OII', 'PUMP', 'AAPL', 'GOOGL', 'MXL', 'GRMN', 'KLAC', 'ONTO']
#     instruments_info = goby.get_instruments_info(shares)
#
#     # Временные переменные для тестирования отображения графика:
#     # legend = ''
#     # labels = ["", "", "", "", "", "", ""]
#     # values = [6, 8, 7, 6, 4, 7, 8]
#     # green = "rgba(50,205,50,1)"
#     # red = "rgba(220,20,60,1)"
#     # green_or_red = green if values[-1]>values[0] else red
#
#     return render_template("instruments.html",
#                            current_time=current_time,
#                            instruments_info=instruments_info,
#                            # values=values,
#                            # green_or_red=green_or_red,
#                            # legend=legend,
#                            # labels=labels
#                            )
#
#
# @app.route('/instruments/<string:name>/<int:id>')
# def instruments_details(name, id):
#     return "Instrument: " + name + " - " + str(id)
#
#
# @app.route('/operations')
# def operations():
#     ''' Список активных аккаунтов '''
#     accounts = goby.get_snb_accounts()
#     account_id = accounts[0].id
#
#     ''' Список операций в портфеле за выбранный период: '''
#     operations = goby.get_operations(request=goby.request_blank(account_id=account_id), content='list_dict')
#
#     return render_template("operations.html", operations=operations)
#
#
# @app.route("/chart")
# def chart():
#     legend = 'Monthly Data'
#     labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
#     values = [10, 9, 8, 7, 6, 4, 7, 8]
#     return render_template('chart.html', values=values, labels=labels, legend=legend)
#
#
# @app.route("/chart_free")
# def chart_free():
#     legend = 'Chart'
#     labels = ["", "", "", "", "", "", "", ""]
#     values = [6, 8, 7, 6, 4, 7, 8]
#     green = "rgba(50,205,50,1)"
#     red = "rgba(220,20,60,1)"
#     green_or_red = green if values[-1]>values[0] else red
#     return render_template('chart_free.html', values=values, labels=labels, legend=legend, green_or_red=green_or_red)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run('127.0.0.1', port=5000, debug=True)