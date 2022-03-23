from github import Github
import pandas as pd

# pandas - для обработки файлов

project_list = ['apache/any23', 'apache/groovy',  'YuriyGamiy/dj_start']

access_token = "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"

# create function
def extract_project_info():
    # создадим пустой фрейм данных df_project - это как пустой лист excel
    df_project = pd.DataFrame()
    print(type(df_project))

    for project in project_list:
        # создадим объект класса github, которому передадим token
        g = Github(access_token)
        # при появлении исключений, превышения лимитов, далее мы можем рассмотреть обработку исключений github
        # извлекаем информацию о каждом проекте
        repo = g.get_repo(project)
        # для суммарного получения запросов создадим переменную, состояние all
        pl_rq = repo.get_pulls(state='all')

        # сохраним наши данные во фрейме данных, добавляем словарь и вторым параметром флаг True в ignore_index
        # в словаре указываем, что мы хотим извлечь
        df_project = df_project.append({
             'Project_ID': repo.id,
              'Name': repo.name,
             'Full_name': repo.full_name,
             'Language': repo.language,
             'Forks': repo.forks_count,
             'Stars': repo.stargazers_count,
             'Watchers': repo.subscribers_count,
             'Pul_req.count': pl_rq.totalCount,

        }, ignore_index=True)

        # Данные будут извлечены и сохранены в этом файле .csv
        # df_project.to_csv('../_2_Dataset/project_dataset.csv', sep=',', encoding='utf-8', index=True)
        df_project.to_csv('project_dataset.json', sep=',', encoding='utf-8', index=True)
        # index=True - каждая строка в файле будет иметь числовой индекс
        # в этом примере мы получили представление о том как извлекать данные из конкретных проектов

# вызов function
extract_project_info()