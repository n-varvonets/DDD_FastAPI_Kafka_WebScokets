from punq import Container

from logic.init import init_container

# container = Container()  сначала хотели глобально контейнер создавать и потом его переиспользовать, но решили
# что лучше в самом ините его создовать и там не пичкать его... ЗАкешировать токо его нужно, что б глобальное состояние
# БД не менялось
container = init_container()
