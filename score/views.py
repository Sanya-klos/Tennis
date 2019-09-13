from django.shortcuts import render
import getDB
from datetime import datetime
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def index(request):
    DB = getDB.mySqlConnect()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM score2018")
    rows = []
    for data in cursor:
        rows.append(data)
    dict_row = {'rows': [rows]}
    result = {**dict_row, **create_select_box()}
    return render(request, 'score/mainPage.html', result)


def filter_table(request):
    location = request.GET.get('location')
    tournament = request.GET.get('tournament')
    date = request.GET.get('date')
    tier = request.GET.get('tier')
    winner = request.GET.get('winner')
    loser = request.GET.get('loser')
    DB = getDB.mySqlConnect()
    cursor = DB.cursor()
    cursor.execute(create_request(location, tournament, date, tier, winner, loser))
    rows = []
    for data in cursor:
        rows.append(data)
    dict_row = {'rows': [rows]}
    result = {**dict_row, **create_select_box()}
    return render(request, 'score/mainPage.html', result)


def create_schedule(request):
    winner = request.GET.get('winner')
    loser = request.GET.get('loser')
    massage = ""
    if winner != "Все" and loser != "Все":
        DB = getDB.mySqlConnect()
        cursor = DB.cursor()
        cursor.execute("SELECT * FROM score2018 WHERE `Winner`='{}'".format(winner))
        cursor1 = DB.cursor()
        cursor1.execute("SELECT * FROM score2018 WHERE `Winner`='{}'".format(loser))
        Ox_tournament = []
        Ox_tournament1 = []
        Oy_round = [0, 1, 2, 3, 4, 5, 6, 7]
        temp_tournament = ''
        for data in cursor:
            if data[3] != temp_tournament:
                Ox_tournament.append(data[3])
            temp_tournament = data[3]

        temp_tournament = ''
        for data in cursor1:
            if data[3] != temp_tournament:
                Ox_tournament1.append(data[3])
            temp_tournament = data[3]

        player1_rounds = []
        player2_rounds = []
        Ox_finaly = []

        for i in Ox_tournament:
            for j in Ox_tournament1:
                if i == j:
                    Ox_finaly.append(i)

        if len(Ox_finaly) == 0:
            massage = "Players do not have common tournaments"
            return render(request, 'score/schedule.html', {'massage': massage})

        temp_tournament = ''
        temp_round = ''
        cursor_p1 = DB.cursor()
        for k in Ox_finaly:
            cursor_p1.execute("SELECT * FROM score2018 WHERE `Winner`='{}' and `Tournament`='{}'".format(winner, k))
            for m in cursor_p1:
                if k != temp_tournament:
                    player1_rounds.append(index_tournament(temp_round))
                temp_round = m[8]
                temp_tournament = k
        player1_rounds.append(index_tournament(temp_round))
        del player1_rounds[0]

        temp_tournament = ''
        temp_round = ''
        cursor_p2 = DB.cursor()
        for k in Ox_finaly:
            cursor_p2.execute("SELECT * FROM score2018 WHERE `Winner`='{}' and `Tournament`='{}'".format(loser, k))
            for m in cursor_p2:
                if k != temp_tournament:
                    player2_rounds.append(index_tournament(temp_round))
                temp_round = m[8]
                temp_tournament = k
        player2_rounds.append(index_tournament(temp_round))
        del player2_rounds[0]

        dpi = 50
        fig = plt.figure(dpi=dpi, figsize=(600 / dpi, 400 / dpi))
        mpl.rcParams.update({'font.size': 10})

        title = (str(winner) + "  vs  " + str(loser))
        plt.title(title)
        plt.xlabel('Tournament')
        plt.ylabel('Round')
        ax = plt.axes()
        ax.yaxis.grid(True)
        axes = plt.gca()
        axes.set_ylim([Oy_round[0], Oy_round[-1]])

        ys = range(len(Oy_round))
        xs = range(len(Ox_finaly))

        plt.yticks(ys, Oy_round, rotation=10)
        plt.xticks(xs, Ox_finaly, rotation=80)
        # plt.plot(Ox_tournament, data_round, color='red', linestyle='solid', label='tournaments')
        plt.bar([x + 0.05 for x in xs], player1_rounds, width=0.2, color='red', alpha=0.7, label=winner, zorder=2)
        plt.bar([x + 0.3 for x in xs], player2_rounds, width=0.2, color='blue', alpha=0.7, label=loser, zorder=2)
        fig.autofmt_xdate(rotation=25)

        plt.legend(loc='upper right')

        plt.show()
        fig.savefig('score/static/score/images/schedule.png', dpi=60)
        plt.close(fig)

    elif winner != "Все" or loser != "Все":
        DB = getDB.mySqlConnect()
        cursor = DB.cursor()
        if winner != "Все":
            cursor.execute("SELECT * FROM score2018 WHERE `Winner`='{}'".format(winner))
            title = winner
        elif loser != "Все":
            cursor.execute("SELECT * FROM score2018 WHERE `Winner`='{}'".format(loser))
            title = loser
        Ox_tournament = []
        Oy_round = [0, 1, 2, 3, 4, 5, 6, 7]
        data_round = []
        temp_tournament = ''
        temp_round = ''
        for data in cursor:
            if data[3] != temp_tournament:
                Ox_tournament.append(data[3])
                data_round.append(index_tournament(temp_round))
            temp_tournament = data[3]
            temp_round = data[8]
        data_round.append(index_tournament(temp_round))
        del data_round[0]
        dpi = 50
        fig = plt.figure(dpi=dpi, figsize=(600 / dpi, 400 / dpi))
        mpl.rcParams.update({'font.size': 10})

        plt.title(title)
        plt.xlabel('Tournament')
        plt.ylabel('Round')
        ax = plt.axes()
        ax.yaxis.grid(True)
        axes = plt.gca()
        axes.set_ylim([Oy_round[0], Oy_round[-1]])

        ys = range(len(Oy_round))
        xs = range(len(Ox_tournament))

        plt.yticks(ys, Oy_round, rotation=10)
        plt.xticks(xs, Ox_tournament, rotation=80)
        plt.bar(Ox_tournament, data_round, width=0.2, color='red', alpha=0.7, label="Tournaments", zorder=2)
        fig.autofmt_xdate(rotation=25)

        plt.legend(loc='upper right')

        plt.show()
        fig.savefig('score/static/score/images/schedule.png', dpi=60)
        plt.close(fig)

    else:
        return
    return render(request, 'score/schedule.html', {'massage': massage})


def create_request(location, tournament, date, tier, winner, loser):
    sql_request = "SELECT * FROM score2018 "
    if location != "Все":
        sql_request += "WHERE `Location`='{}' ".format(location)
    if tournament != "Все" and location == "Все":
        sql_request += "WHERE `Tournament`='{}' ".format(tournament)
    else:
        if tournament != "Все":
            sql_request += "and `Tournament`='{}' ".format(tournament)
    if date != "Все" and tournament == "Все" and location == "Все":
        sql_request += "WHERE `Date`='{}' ".format(date)
    else:
        if date != "Все":
            sql_request += "and `Date`='{}' ".format(date)
    if tier != "Все" and date == "Все" and tournament == "Все" and location == "Все":
        sql_request += "WHERE `Tier`='{}'".format(tier)
    else:
        if tier != "Все":
            sql_request += "and `Tier`='{}' ".format(tier)
    if winner != "Все" and date == "Все" and tournament == "Все" and location == "Все" and tier == "Все":
        sql_request += "WHERE `Winner`='{}'".format(winner)
    else:
        if winner != "Все":
            sql_request += "and `Winner`='{}' ".format(winner)
    if loser != "Все" and winner == "Все" and date == "Все" and tournament == "Все" and location == "Все" and tier == "Все":
        sql_request += "WHERE `Loser`='{}'".format(loser)
    else:
        if loser != "Все":
            sql_request += "and `Loser`='{}' ".format(loser)
    return sql_request


def create_select_box():
    DB = getDB.mySqlConnect()
    cursor = DB.cursor()
    cursor.execute('select * FROM score2018 ')
    rows1 = []
    for data in cursor:
        rows1.append(data)
    location_list = []
    tournament_list = []
    date_list = []
    tier_list = []
    winner_list = []
    loser_list = []
    temp1 = ""
    temp2 = ""
    temp3 = ""
    temp4 = ""
    temp5 = ""
    temp6 = ""
    for row in rows1:
        if row[2] != temp1:
            location_list.append(row[2])
            temp1 = row[2]
        if row[3] != temp2:
            tournament_list.append(row[3])
            temp2 = row[3]
        if row[4] != temp3:
            date_list.append(row[4])
            temp3 = row[4]
        if row[5] != temp4:
            tier_list.append(row[5])
            temp4 = row[5]
        if row[10] != temp5:
            winner_list.append(row[10])
            temp5 = row[10]
        if row[11] != temp6:
            loser_list.append(row[11])
            temp6 = row[11]
    tier_list = list(set(tier_list))
    winner_list = list(set(winner_list))
    winner_list = sorted(winner_list)
    loser_list = list(set(loser_list))
    loser_list = sorted(loser_list)
    sorted(date_list, key=lambda x: datetime.strptime(x, "%d.%m.%Y").strftime("%Y.%m.%d"))
    context = {'location': [location_list], 'tournament': [tournament_list], 'date': [date_list], 'tier': [tier_list],
               'winner': [winner_list], 'loser': [loser_list]}
    return context


def index_tournament(round):
    if round == "Round Robin":
        return 0
    elif round == "1st Round":
        return 1
    elif round == "2nd Round":
        return 2
    elif round == "3rd Round":
        return 3
    elif round == "4th Round":
        return 4
    elif round == "Quarterfinals":
        return 5
    elif round == "Semifinals":
        return 6
    elif round == "The Final":
        return 7
    else:
        return 99
