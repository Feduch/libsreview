import bot_vk.command_system as command_system
import bot_vk.vkapi as vkapi

def hello():
   message = 'Привет, друг!\n Я тут сижу, считаю, кому что нравится, чтобы выслать в четверг лучшую свежую книгу. Если тебе грустно напиши "котэ".'
   return message, ''

hello_command = command_system.Command()

hello_command.keys = ['привет', 'hi', 'hello', 'дратути', 'здравствуй', 'здравствуйте']
hello_command.description = 'Поприветствую тебя'
hello_command.process = hello


def cat():
   # Получаем случайную картинку из паблика
   attachment = vkapi.get_random_wall_picture(-32015300)
   message = 'Вот тебе котэ.\nУ меня их еще много :)'
   return message, attachment

cat_command = command_system.Command()

cat_command.keys = ['котэ', 'котик', 'кошка', 'кот', 'котенок', 'котяра', 'cat']
cat_command.description = 'Пришлю котэ'
cat_command.process = cat


def info():
   message = 'Я мега бот, сижу, никого не трогаю, считаю популярность книг, рассылаю по четвергам лучшую книгу в жанре фэнтези. А еще по запросу могу кой-чего.\n'
   for c in command_system.command_list:
        message += c.keys[0] + ' - ' + c.description + '\n'
   return message, ''

info_command = command_system.Command()

info_command.keys = ['помощь', 'помоги', 'help']
info_command.description = 'Покажу список команд'
info_command.process = info
