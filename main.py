import bencode
import telebot
import requests
from settings import API_KEY, ADMIN_IDS, TORRENT_FOLDER

bot = telebot.TeleBot(API_KEY)


def is_torrent_content(content):
    try:
        meta_info = bencode.decode(content, 'encoding; default is utf-8')

        info = meta_info['info']
        return info['name']
    except:
        return False


@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    if message.from_user.id not in ADMIN_IDS:
        # print("ID: {} is not admin ID".format(message.from_user.id))
        bot.send_message(message.chat.id, "Your ID {} is not allowed this action".format(message.from_user.id))
        return False

    # print(message)
    # print(message.document)

    file_info = bot.get_file(message.document.file_id)
    # print(file_info)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_KEY, file_info.file_path))
    torrent_name = is_torrent_content(file.content)
    if file and torrent_name:
        with open('{}{}.torrent'.format(TORRENT_FOLDER, torrent_name), 'wb') as f:
            f.write(file.content)


bot.polling(none_stop=True)
