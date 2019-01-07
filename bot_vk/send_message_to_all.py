import bot_vk.vkapi as vkapi
import bot_vk.pupular_books_in_genre as pop_book



def send_message_all_members(group_id=169943927, genre_id=22):
    """
    посылает личное сообщение всем подписчикам группы
    """
    member_list = vkapi.get_all_group_members(group_id)
    book_request = pop_book.pupular_books_in_genre(genre_id)
    attachment = book_request[1]
    book = book_request[0]
    message = []
    message.append('Лучшая книга этой недели в жанре фэнтези - ')
    message.append('"' + book.title + '".')
    message.append('Общий рейтинг книги - ')
    message.append(book.rating)
    message.append("Полная информация о книге + возможность ее почитать - https://libs.ru/book/" + str(book.id) + "/")
    message.append("(голосуйте за любимые книги – не забывайте, что ваш голос помогает автору понять, "
                   "хороша книга или автору пора что-то менять). На этом мы прощаемся и на следующей неделе "
                   "сообщим о новой книге, которая наберет наибольшую популярность за следующий 7 дней!")

    res_message = str(" ".join(str(e) for e in message))
    j = member_list["count"]//100

    for i in range(0, j+1):
        if i == j:
            vkapi.send_message_group_members(member_list["items"][i:member_list["count"]], res_message, attachment)
        else:
            vkapi.send_message_group_members(member_list["items"][i*100:i*100+99], res_message, attachment)