
def command_start(bot, update):
    global SESSIONS
    chat_id = update.message.chat_id
    if chat_id not in SESSIONS.keys():
        messenger = Messenger(bot, logger)
        SESSIONS[chat_id] = Session(chat_id, config_instance, logger)
        SESSIONS[chat_id].set_messenger(messenger)
        SESSIONS[chat_id].quiz = Quiz(SESSIONS[chat_id])


def command_roll(bot, update, args=''):
    global SESSIONS
    chat_id = update.message.chat_id
    rand_type = args is None and args[0] or None
    SESSIONS[chat_id].messenger.send_msg(chat_id, _("searching_movies"))
    SESSIONS[chat_id].quiz.show(update, rand_type)


def command_leaderboard(bot, update):
    global SESSIONS
    chat_id = update.message.chat_id
    session = SESSIONS[chat_id]
    try:
        session.messenger.send_msg(chat_id, _("leader_board_title"), 'highlights')
        ldb = session.get_leaderboard()
        session.messenger.send_msg(chat_id, ldb)
    except ValueError as e:
        session.messenger.send_msg(chat_id, update.message.from_user.first_name + e.args[0])


def command_action(bot, update):
    global SESSIONS
    group = update.message.chat_id
    try:
        player = Player(update.message.from_user.id)
        player.name = update.message.from_user.first_name + " " + update.message.from_user.last_name
        SESSIONS[group].player_add(player)
        SESSIONS[update.message.chat_id].messenger.send(update, player.name + " entrou na partida!")
    except ValueError as e:
        SESSIONS[update.message.chat_id].messenger.send(update, update.message.from_user.first_name + e.args[0])


def command_repeat(bot, update):
    global SESSIONS
    movie_img = SESSIONS[update.message.chat_id].quiz.get_question()
    SESSIONS[update.message.chat_id].messenger.send(update, "=========REPETINDO=========")
    bot.send_photo(chat_id=update.message.chat_id, photo=movie_img, caption="Qual o nome do filme/série?")
    SESSIONS[update.message.chat_id].messenger.send(update, "===========================")


def command_cut(bot, update):
    global SESSIONS
    group = update.message.chat_id
    try:
        player = Player(update.message.from_user.id)
        SESSIONS[group].player_quit(player)
        SESSIONS[update.message.chat_id].messenger.send(update,
                                                        update.message.from_user.first_name + " saiu da partida!")
    except ValueError as e:
        SESSIONS[update.message.chat_id].messenger.send(update, update.message.from_user.first_name + e.args[0])


def command_stop(bot, update):
    global SESSIONS
    try:
        del (SESSIONS[update.message.chat_id])
        SESSIONS[update.message.chat_id].messenger.send(update, "Encerrando a partida...")
    except ValueError as e:
        SESSIONS[update.message.chat_id].messenger.send(update, "Não foi possível encerrar a partida: %s" % e)


def command_check_resps(bot, update):
    global SESSIONS
    SESSIONS[update.message.chat_id].quiz.check_resps(update)
