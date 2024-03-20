from telegram.ext import Updater, CommandHandler

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    update.message.reply_text("Welcome to the Point Claim Bot! Use /claim to claim your points.")

def claim(update, context):
    user = update.message.from_user
    user_profile = UserProfile.objects.get_or_create(user=user)[0]

    if user_profile.last_claimed is None or (timezone.now() - user_profile.last_claimed).total_seconds() >= 600:
        user_profile.points += 1
        user_profile.last_claimed = timezone.now()
        user_profile.save()
        update.message.reply_text("Points claimed successfully!")
    else:
        update.message.reply_text("You can claim points again in 10 minutes.")

start_handler = CommandHandler('start', start)
claim_handler = CommandHandler('claim', claim)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(claim_handler)

updater.start_polling()