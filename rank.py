import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# 페이지 설정 (초기 페이지를 더 넓게 설정)
st.set_page_config(layout="centered", page_title="Team Rank", page_icon="🔢")

# 타이틀 추가
st.title('BetterJin309')
st.subheader('Team Rank')

# 스포츠 나열
sports = ['축구','농구','야구']

# 리그 나열
league = {
    '축구' : ['EPL','EFL','라리가','분데스리가','세리에A','리그1','K리그 1','K리그 2','A리그','에레디비시에'],
    '농구' : ['KBL','W-KBL','NBA'],
    '야구' : ['KBO']
}

selected_sport = st.selectbox('종목 선택', sports)

if selected_sport:
    selected_league = st.selectbox('리그 선택', league[selected_sport])
    

url_mapping = {
    'EPL': 'https://www.zentoto.com/sports/soccer/epl',
    'EFL': 'https://www.zentoto.com/sports/soccer/championship',
    '라리가': 'https://www.zentoto.com/sports/soccer/laliga',
    '분데스리가': 'https://www.zentoto.com/sports/soccer/bundesliga',
    '세리에A': 'https://www.zentoto.com/sports/soccer/serie-a',
    '리그1': 'https://www.zentoto.com/sports/soccer/ligue1',
    'K리그 1': 'https://www.zentoto.com/sports/soccer/k-classic',
    'K리그 2': 'https://www.zentoto.com/sports/soccer/k-challenge',
    'A리그': 'https://www.zentoto.com/sports/soccer/australia-league',
    '에레디비시에': 'https://www.zentoto.com/sports/soccer/eredivisie',
    'NBA': 'https://www.zentoto.com/sports/basketball/nba',
    'KBL': 'https://www.zentoto.com/sports/basketball/kbl',
    'W-KBL': 'https://www.zentoto.com/sports/basketball/wkbl',
    'KBO': 'https://www.zentoto.com/sports/baseball/kbo'
}

url = url_mapping.get(selected_league, '')




if st.button('순위 조회'):
    result = []

    if selected_sport == '농구' : # 농구 일 경우
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 나무 태그 : 팀
        teams = soup.select('div.container.league-main > div > div.col-8 > div > div.content-bdy.mt-10 > div > table > tbody > tr')

        result = []

        for team in teams : 
            name = team.select_one('td:nth-of-type(2) > a').text
            rank = team.select_one('td').text
            total = team.select_one('td:nth-of-type(3)').text
            wins = team.select_one('td:nth-of-type(4)').text
            loses = team.select_one('td:nth-of-type(5)').text
            score = team.select_one('td:nth-of-type(6)').text
            conceded = team.select_one('td:nth-of-type(7)').text
            odds = team.select_one('td:nth-of-type(8)').text
            last5 = team.select_one('li:nth-of-type(2) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(3) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(4) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(5) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(6) > span').text.replace('W','승').replace('D','무').replace('L','패')
            link = 'https://www.zentoto.com/' + team.select_one('a').attrs['href']
            result.append([rank, name, odds, last5, total, wins, loses, score, conceded, link])

        df = pd.DataFrame(result, columns=['순위','팀','승률', '최근경기', '경기수','승', '패','득점','실점', '일정'])

        # 일정 열을 "링크"로 표시하며 하이퍼링크로 변환
        def make_clickable(link):
            return f'<a href="{link}" target="_blank">링크</a>'
        df['일정'] = df['일정'].apply(make_clickable)

        # Streamlit에서 HTML로 데이터프레임 표시
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)


    elif selected_sport == '축구' : # 축구일 경우
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 나무 태그 : 팀
        teams = soup.select('div.container.league-main > div > div.col-8 > div > div.content-bdy.mt-10 > div > table > tbody > tr')

        result = []
        for team in teams : 
            name = team.select_one('td:nth-of-type(2) > a').text
            rank = team.select_one('td').text
            total = team.select_one('td:nth-of-type(3)').text
            points = team.select_one('td:nth-of-type(4)').text
            wins = team.select_one('td:nth-of-type(5)').text
            draws = team.select_one('td:nth-of-type(6)').text
            loses = team.select_one('td:nth-of-type(7)').text
            goal_differ = team.select_one('td:nth-of-type(8)').text
            last5 = team.select_one('li:nth-of-type(2) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(3) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(4) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(5) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(6) > span').text.replace('W','승').replace('D','무').replace('L','패')
            link = 'https://www.zentoto.com/' + team.select_one('a').attrs['href']
            result.append([rank, name, points, last5, total, wins, draws, loses, goal_differ, link])

        df = pd.DataFrame(result, columns=['순위','팀','승점', '최근경기' ,'경기수','승','무','패','득실차','일정'])

        # 일정 열을 "링크"로 표시하며 하이퍼링크로 변환
        def make_clickable(link):
            return f'<a href="{link}" target="_blank">링크</a>'
        df['일정'] = df['일정'].apply(make_clickable)

        # Streamlit에서 HTML로 데이터프레임 표시
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)


    elif selected_sport == '야구' : # 야구일 경우
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 리그 명
        League = soup.select_one('div.container.league-main > div > div.col-8 > div > div.content-tit > h2 > span:nth-of-type(2)').text

        # 나무 태그 : 팀
        teams = soup.select('div.container.league-main > div > div.col-8 > div > div.content-bdy.mt-10 > div > table > tbody > tr')

        result = []

        for team in teams : 
            name = team.select_one('td:nth-of-type(2) > a').text
            rank = team.select_one('td').text
            total = team.select_one('td:nth-of-type(3)').text
            wins = team.select_one('td:nth-of-type(4)').text
            draws = team.select_one('td:nth-of-type(5)').text
            loses = team.select_one('td:nth-of-type(6)').text
            score = team.select_one('td:nth-of-type(7)').text
            conceded = team.select_one('td:nth-of-type(8)').text
            odds = team.select_one('td:nth-of-type(9)').text
            last5 = team.select_one('li:nth-of-type(2) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(3) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(4) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(5) > span').text.replace('W','승').replace('D','무').replace('L','패') + team.select_one('li:nth-of-type(6) > span').text.replace('W','승').replace('D','무').replace('L','패')
            link = 'https://www.zentoto.com/' + team.select_one('a').attrs['href']
            result.append([rank, name, odds, last5, total, wins, draws, loses, score, conceded, link])

        df = pd.DataFrame(result, columns=['순위','팀','승률', '최근경기', '경기수','승','무','패','득점','실점', '일정'])

        # 일정 열을 "링크"로 표시하며 하이퍼링크로 변환
        def make_clickable(link):
            return f'<a href="{link}" target="_blank">링크</a>'
        df['일정'] = df['일정'].apply(make_clickable)

        # Streamlit에서 HTML로 데이터프레임 표시
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    
    else:
        pass

if not url:
    st.error("URL을 확인하세요. 선택한 리그에 대한 데이터가 없습니다.")
else:
    response = requests.get(url)
