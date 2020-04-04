import telebot
from django.core.management import BaseCommand
from django.utils.text import Truncator
from telebot import types

from microlearning.models import Article

TOKEN = ""
bot = telebot.TeleBot(TOKEN)


class Task():
    is_running = False
    names = [
        'Last new articles from medscape',
        'Last articles by category'
    ]


start_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
start_markup.add(
    types.KeyboardButton('/start')
)

source_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
source_markup.add(
    types.KeyboardButton(Task.names[0]),
    types.KeyboardButton(Task.names[1])
)

category_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
category_markup.add(*[types.KeyboardButton(name) for _, name in Article.ARTICLE_TYPES])


@bot.message_handler(commands=['start'])
def start_message(message):
    if not Task.is_running:
        msg = bot.send_message(
            message.chat.id,
            'Hi! What do you want to read?',
            reply_markup=source_markup
        )
        bot.register_next_step_handler(msg, ask_source)
        Task.is_running = True


def ask_source(message):
    text = message.text
    if text == Task.names[0]:
        articles = Article.objects.all().order_by('-publish')[:10]

        output = "\n".join(generate_output(articles))
        msg = bot.send_message(message.chat.id, output, reply_markup=start_markup)
        Task.is_running = False
    elif text == Task.names[1]:
        msg = bot.send_message(message.chat.id, 'What category are you interested in?', reply_markup=category_markup)
        bot.register_next_step_handler(msg, ask_category)
    else:
        msg = bot.send_message(message.chat.id, 'You need to choose what do you want to read')
        bot.register_next_step_handler(msg, ask_source)


def ask_category(message):
    Task.is_running = False

    def get_category_by_name(category_name: str):
        for category, name in Article.ARTICLE_TYPES:
            if name == category_name:
                return category

        return None

    category = get_category_by_name(message.text)
    if category:
        articles = Article.objects.all().filter(type=category).order_by('-publish')[:10]
        output = "\n".join(generate_output(articles))
        msg = bot.send_message(message.chat.id, output, reply_markup=start_markup)
    else:
        msg = bot.send_message(message.chat.id, 'What category are you interested in?', reply_markup=category_markup)
        bot.register_next_step_handler(msg, ask_category)


def generate_output(articles: list) -> list:
    output = []
    for article in articles:
        output.append("{}, {}\n {}\n".format(
            article.title,
            article.publish,
            Truncator(article.body).words(15, truncate=' …')
        ))

    return output


class Command(BaseCommand):
    help = 'Using telebot'

    def handle(self, *args, **kwargs):
        bot.polling(none_stop=True)
