# import исключений exception для остановок на ограничение скорости
from github import Github, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException
# для сохранения полученных данных
import pandas as pd
# нужны еще запросы к библиотеке - потомучто есть два исключения, которые не обрабатываются
# pi github, такие как повторные попытки и time_out с помощью библиотеки time, чтоб процессор на некоторое время уснул
import requests
import time


# мы получили данные в .csv и теперь нам необходимо преобразовать в код используя попытки и исключения
# для обработки возможных
project_list = ['apache/any23', 'apache/groovy',  'YuriyGamiy/dj_start']

access_token = "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"

def extract_project_info():
    # мы создали пустой фрейм данных
    df_project = pd.DataFrame()
    # с помощью цикла мы берем один
    for project in project_list:
        g = Github(access_token)
        repo = g.get_repo(project)
        PRs = repo.get_pulls(state='all')
        df_project = df_project.append({
            'Project_ID': repo.id,
            'Name': repo.name,
            'Full_name': repo.full_name,
            'Language': repo.language,
            'Forks': repo.forks_count,
            'Stars': repo.stargazers_count,
            'Watchers': repo.subscribers_count,
            'PRs_count': PRs.totalCount
        }, ignore_index=True)
    df_project.to_csv('../Dataset/project_dataset.csv', sep=',', encoding='utf-8', index=True)

# extract_project_info()


def extract_project_info_try_except_2():
    df_project = pd.DataFrame()
    for project in project_list:
        while True:
            try:
                # сначала отправляется запрос на сервер github и он начинает обработку
                # затем извлекается информация о проекте и в переменной PRs метод get_pulls() происходит отправка этой переменной
                # затем данные сохраняются в виде словаря и мы передаем его в фрейм данных
                # что если здесь возникает исключение какое-то, нам доступны эти обработчики исключений
                # чтобы перехватить эти исключения в случае превышения огранияения скорости
                # retry = 15, если 15, то он отправляет 15 раз запрос на сервер, можно увеличить до 20
                # timeout = 15 - по умолчанию я думаю, ждет сервера в течение некоторого времени ичерез 15 секунд
                # завершает работу и выдает исключение
                # Поэтому Вы можете улучшить эти значения, увеличить эти значения, указать собственные, в зависимости от Ваших требований
                # но как только Вы используете эту обработку исключений, Ваш код будет продолжаться
                # до тех пор, пока Вы извлекаете все данные сейчас
                g = Github(access_token, retry=2, timeout=5)
                print(f'Extracting data from {project} repo')
                repo = g.get_repo(project)
                PRs = repo.get_pulls(state='all')
                df_project = df_project.append({
                    'Project_ID': repo.id,
                    'Name': repo.name,
                    'Full_name': repo.full_name,
                    'Language': repo.language,
                    'Forks': repo.forks_count,
                    'Stars': repo.stargazers_count,
                    'Watchers': repo.subscribers_count,
                    'PRs_count': PRs.totalCount
                }, ignore_index=True)
            except RateLimitExceededException as e:
                # e - печатаем исключение как e, это сообщение для этого исключения, можете свое сообщение напечатать
                print(e.status)
                print('Rate limit exceeded')
                # наиболее важным является время, потому-что если оно завершено Вы не можете отправлять запросы серверу
                # в дневное время будет спать процессор около 4 минут, а через 4 минуты снова отправит запрос
                # если 60 секунд, 60 минут завершено, он снова начнет обрабатывать и отправлять запросы
                # и процесс извлечения данных начнется снова. Если снова не начнется, то через исключение будет отображаться превышенный предел скорости сообщений
                time.sleep(300)
                continue
            except BadCredentialsException as e:
                print(e.status)
                print('Bad credentials exception')
                break
            except UnknownObjectException as e:
                print(e.status)
                print('Unknown object exception')
                break
            except GithubException as e:
                print(e.status)
                print('General exception')
                break
                # в случае превышения лимита - укладываем спать систему на 10 секунд, и через 10 секунд снова продолжаем цикл
            except requests.exceptions.ConnectionError as e:
                print('Retries limit exceeded')
                print(str(e))
                time.sleep(10)
                continue
            except requests.exceptions.Timeout as e:
                print(str(e))
                print('Time out exception')
                time.sleep(10)
                continue
            break
    df_project.to_csv('../_2_Dataset/project_dataset_2.csv', sep=',', encoding='utf-8', index=True)


extract_project_info_try_except_2()