# -*- coding: utf-8 -*-
# from starlette_wtf import StarletteForm
# from wtforms import BooleanField
# from wtforms import FileField
# from wtforms import TextAreaField
# from wtforms import TextField
# from wtforms.validators import DataRequired
# from wtforms.validators import Length
# from wtforms.widgets import FileInput


# class LyricsForm(StarletteForm):
#     """Lyrics File Upload"""

#     lyric_file = FileField(
#         "Lyrics CSV",
#         widget=FileInput(multiple=False),
#         validators=[DataRequired("File is required"),],
#     )


# class BotActivationForm(StarletteForm):
#     """ Activate or Deactivate Bot """

#     activate_bot = BooleanField()


# class BotDeletionForm(StarletteForm):
#     """ Delete Bot """

#     twitter_name = TextField(
#         "Twiter Name", validators=[DataRequired("Please enter the twitter account"),],
#     )


# class UpdateBotForm(StarletteForm):

#     twitter_name = TextField(
#         "Twiter Name",
#         validators=[
#             DataRequired("Please enter the twitter account"),
#             Length(min=4, max=30, message="length min 4, max 30"),
#         ],
#     )
#     consumer_key = TextField(
#         "Consumer Key",
#         validators=[
#             DataRequired("Please enter the consumer key"),
#             Length(min=4, max=300),
#         ],
#     )
#     consumer_secret = TextField(
#         "Consumer Secret",
#         validators=[
#             DataRequired("Please enter the consumer secret "),
#             Length(min=4, max=300),
#         ],
#     )
#     access_token = TextField(
#         "Access Token",
#         validators=[
#             DataRequired("Please enter the access token"),
#             Length(min=4, max=300),
#         ],
#     )
#     access_token_secret = TextField(
#         "Access Token Secret",
#         validators=[
#             DataRequired("Please enter the access token secret"),
#             Length(min=4, max=300),
#         ],
#     )
#     description = TextAreaField(
#         "Description",
#         validators=[
#             DataRequired("Please enter a description"),
#             Length(min=10, max=500),
#         ],
#     )
#     bot_image = FileField(
#         "Bot Image",
#         widget=FileInput(multiple=False),
#         # validators=[DataRequired("File is required")],
#     )


# class NewBotForm(StarletteForm):

#     twitter_name = TextField(
#         "Twiter Name",
#         validators=[
#             DataRequired("Please enter the twitter account"),
#             Length(min=4, max=30, message="length min 4, max 30"),
#         ],
#     )
#     consumer_key = TextField(
#         "Consumer Key",
#         validators=[
#             DataRequired("Please enter the consumer key"),
#             Length(min=4, max=300),
#         ],
#     )
#     consumer_secret = TextField(
#         "Consumer Secret",
#         validators=[
#             DataRequired("Please enter the consumer secret "),
#             Length(min=4, max=300),
#         ],
#     )
#     access_token = TextField(
#         "Access Token",
#         validators=[
#             DataRequired("Please enter the access token"),
#             Length(min=4, max=300),
#         ],
#     )
#     access_token_secret = TextField(
#         "Access Token Secret",
#         validators=[
#             DataRequired("Please enter the access token secret"),
#             Length(min=4, max=300),
#         ],
#     )
#     description = TextAreaField(
#         "Description",
#         validators=[
#             DataRequired("Please enter a description"),
#             Length(min=10, max=500),
#         ],
#     )
#     bot_image = FileField(
#         "Bot Image",
#         widget=FileInput(multiple=False),
#         validators=[DataRequired("File is required")],
#     )
