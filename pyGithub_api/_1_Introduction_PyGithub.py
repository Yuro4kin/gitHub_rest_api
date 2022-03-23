from github import Github

access_token = "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"

g = Github(access_token)

print(type(g))

current_user = g.get_user()

print(current_user.name)
print(current_user.bio)
print(current_user.company)
print(current_user.location)

# repos = g.get_user().get_repos()
# for repo in repos:
#     print(repo.name)
#     print(repo)


# Поиск в github
# java_repos = g.search_repositories(query="language:java")
# for repo in java_repos:
#     print(repo.name)
#     print(repo)

# Поиск в репозиториях по количеству проблем с хорошей первой проблемой
# Search repositories based on number of issues with good-first-issue
# repositories = g.search_repositories(query='good-first-issues:>3')
# for repo in repositories:
#     print(repo)

# https://docs.github.com/en/search-github/searching-on-github/searching-code
# Search by file size
# сопоставляет код со словом «функция», написанный на Python, в файлах размером более 10 КБ.
# repositories = g.search_repositories(query='function size:>10000 language:python')
# for repo in repositories:
#     print(repo)


# Search by filename
# repositories = g.search_repositories(query='filename:re_3_1_csv.py')
# for repo in repositories:
#     print(repo)


# https://docs.github.com/en/search-github/getting-started-with-searching-on-github/sorting-search-results
# Сортировать по дате фиксации соответствует коммитам, содержащим слово «feature» в репозиториях,
# принадлежащих GitHub, отсортированных по убыванию даты фиксации
# Sort by committer date
repositories = g.search_repositories(query='function org:github sort:committer-date-desc')
for repo in repositories:
     print(repo)

# ??????????????????
# Поиск в своем репозитории по языку программирования
# repos = g.get_user().get_repos()
# for repo in repos:
#     repo = g.search_repositories(query="language:python")
#     for py in repo:
#         print(py.name)

