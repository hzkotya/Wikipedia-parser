import bs4
import requests
from collections import deque


class Parser:
    _BAD_PREFIX_SET = {'Википедия:', 'Портал:'}

    def link_checker(self, link):
        for prefix in self._BAD_PREFIX_SET:
            if link['title'][:len(prefix)] == prefix:
                return False
        return True

    def get_links(self, html):
        soup = bs4.BeautifulSoup(html, features="html.parser")
        css_selector = 'div.mw-parser-output a[href^=\/wiki]:not([class])'
        links = soup.select(css_selector)
        return list(map(lambda link: link['title'], filter(lambda x: self.link_checker(x), links)))

    def get_target_title(self, html):
        soup = bs4.BeautifulSoup(html, features="html.parser")
        return soup.select_one('h1').text

class WebGraph:
    def __init__(self, start, target_link):
        self.start = start
        self.parser = Parser()
        self.target = self.parser.get_target_title(requests.get(target_link).text)
        self.used = {start: 0}

    @staticmethod
    def build_link(title):
        return f'https://ru.wikipedia.org/wiki/{title}'

    def bfs(self):
        deq = deque()
        deq.append(self.start)
        while deq:
            link = deq.popleft()
            for other_link in self.parser.get_links(requests.get(self.build_link(link)).text):
                print(link, other_link)
                if other_link in self.used:
                    continue
                if other_link == self.target:
                    return self.used[link] + 1
                self.used[other_link] = self.used[link] + 1
                if self.used[other_link] > 5:
                    return -1
                deq.append(other_link)


graph = WebGraph(
    input('Введите название страницы, расстояние от которой вы ходите найти'),
    input('Введите ссылку на страницу, расстояние до которой вы ходите найти'),
)
print(graph.bfs())
