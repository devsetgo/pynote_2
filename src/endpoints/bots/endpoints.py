# -*- coding: utf-8 -*-
# import datetime
# import imghdr
# import logging
# import uuid

# from loguru import logger
# from starlette.responses import RedirectResponse
# from starlette_wtf import csrf_protect

# from core import login_required
# from core.crud_ops import execute_one_db
# from core.crud_ops import fetch_all_db
# from core.db_setup import bots
# from core.db_setup import lyrics
# from core.file_functions import open_csv
# from endpoints.bots import crud
# from endpoints.bots import form_validators
# from endpoints.bots import forms
# from endpoints.bots.image_save import save_image
# from resources import templates

# page_url = "/bot"


# @csrf_protect
# @login_required.require_login
# async def bot_index(request):
#     """
#     Index page for twitter bots
#     """
#     query = bots.select()
#     bots_list = await fetch_all_db(query=query)

#     logging.debug(str(bots_list))
#     template = f"{page_url}/bot_index.html"
#     context = {
#         "request": request,
#         "bots": bots_list,
#     }
#     logger.info("page accessed: /bots")
#     return templates.TemplateResponse(template, context)


# @login_required.require_login
# async def bot_info(request):
#     """
#     Not used yet, holder for some type of twitter bot information page if needed
#     """
#     template = f"{page_url}/bot_info.html"
#     context = {"request": request}
#     logger.info("page accessed: /bots/info")
#     return templates.TemplateResponse(template, context)


# @csrf_protect
# @login_required.require_login
# async def bot_activation(request):
#     """
#     activate or deactivate twitter bot form page
#     """
#     twitter_name = request.path_params["page"]
#     logging.debug(twitter_name)
#     bot_data = await form_validators.twittername_check(twitter_name)
#     current_lyric = await crud.get_current_lyric(
#         current_sequence=bot_data["current_lyric_sequence"], twitter_name=twitter_name,
#     )
#     logging.debug(str(current_lyric))

#     form = await forms.BotActivationForm.from_formdata(request)
#     form_data = await request.form()
#     logging.debug(form_data)

#     if form.validate_on_submit():
#         lyrics_list = await crud.get_lyrics_length(twitter_name)
#         logging.debug(str(lyrics_list))

#         if lyrics_list == 0:
#             logger.warning("Twitter Account Name not a match for form entry")
#             form.activate_bot.errors.append(
#                 "You cannot activate a bot with zero lyrics."
#             )
#         else:
#             if "activate_bot" not in form_data:
#                 active_state = False
#             elif form_data["activate_bot"] == "y":
#                 active_state = True

#             values = {
#                 "is_active": active_state,
#             }
#             logging.debug(values)
#             query = bots.update().where(bots.c.twitter_name == twitter_name.lower())
#             db_data = await execute_one_db(query=query, values=values)
#             logging.debug(str(db_data))
#             logger.info("Redirecting user to index page /")
#             return RedirectResponse(url="/bots", status_code=303)

#     template = f"{page_url}/bot_activation.html"
#     context = {
#         "request": request,
#         "form": form,
#         "bot_data": bot_data,
#         "current_lyric": current_lyric,
#     }
#     logger.info(f"page accessed: /bots/bot_activation/{twitter_name}")
#     return templates.TemplateResponse(template, context)


# @csrf_protect
# @login_required.require_login
# async def bot_delete(request):
#     """
#     Delete Bot
#     """
#     twitter_name = request.path_params["page"]
#     logging.debug(twitter_name)
#     bot_data = await form_validators.twittername_check(twitter_name)
#     current_lyric = await crud.get_current_lyric(
#         current_sequence=bot_data["current_lyric_sequence"], twitter_name=twitter_name,
#     )
#     logging.debug(current_lyric)

#     form = await forms.BotDeletionForm.from_formdata(request)
#     form_data = await request.form()
#     logging.debug(form_data)

#     if form.validate_on_submit():

#         logging.debug(form_data)

#         if twitter_name != form_data["twitter_name"]:
#             logger.warning("Twitter Account Name not a match for form entry")
#             form.twitter_name.errors.append("The names must be exact matches")

#         else:
#             user_deleting = request.session["user_name"]
#             logger.warning(
#                 f"{twitter_name} has been deleted by {user_deleting} from {request.client.host}"
#             )
#             await crud.bot_delete(twitter_name)

#             logger.info("Redirecting user to index page /")
#             return RedirectResponse(url="/bots", status_code=303)

#     template = f"{page_url}/bot_delete.html"
#     context = {
#         "request": request,
#         "form": form,
#         "bot_data": bot_data,
#         "current_lyric": current_lyric,
#     }

#     logger.info(f"page accessed: /bots/bot_activation/{twitter_name}")
#     return templates.TemplateResponse(template, context)


# async def squence(request):
#     twitter_name = request.path_params["page"]
#     logging.debug(f"execute increment for {twitter_name}")
#     data = await crud.squence_one(twitter_name)
#     logging.debug(data)
#     return RedirectResponse(url=f"/bots/lyrics/{twitter_name}", status_code=303)


# @csrf_protect
# @login_required.require_login
# async def bot_lyrics(request, UploadFile=None):

#     twitter_name = request.path_params["page"]
#     logging.debug(twitter_name)
#     bot_data = await crud.bot_information(twitter_name=twitter_name)

#     current_sequence = bot_data["current_lyric_sequence"]
#     lyric_data = await crud.lyrics_for_bot(twitter_name=twitter_name)
#     current_lyric = await crud.get_current_lyric(
#         twitter_name=twitter_name, current_sequence=current_sequence
#     )

#     form = await forms.LyricsForm.from_formdata(request)
#     form_data = await request.form()

#     if form.validate_on_submit():
#         file_name = form_data["lyric_file"].filename
#         logging.debug(type(file_name))

#         is_csv = file_name.endswith(".csv")
#         logging.debug(is_csv)
#         if is_csv == True:

#             logger.info(f"processing lyrics file = {file_name}")
#             contents = await form_data["lyric_file"].read()
#             logging.debug(type(contents))

#             if isinstance(contents, bytes) == True:

#                 with open(f"data/csv/{file_name}", "wb") as w:
#                     w.write(contents)

#                 new_lyrics = open_csv(file_name)
#                 logger.critical(new_lyrics)

#                 for n in new_lyrics:
#                     lyric_length = len(n)
#                     if lyric_length > 140:
#                         form.lyric_file.errors.append(f"Lyric length is too long")
#                         return RedirectResponse(
#                             url=f"/bots/lyrics/{twitter_name}", status_code=303
#                         )
#                 logging.debug(new_lyrics)

#                 exist = await crud.lyrics_for_bot(twitter_name=twitter_name)

#                 if isinstance(exist, list) == True:
#                     logger.info(f"removing exiting lyrics for {twitter_name}")
#                     remove = await crud.lyrics_remove(twitter_name=twitter_name.lower())
#                     logger.info(remove)

#                 try:
#                     count = 1
#                     for l in new_lyrics:

#                         line = l["lyric"]
#                         logging.debug(line)

#                         values = {
#                             "twitter_name": twitter_name.lower(),
#                             "sequence": count,
#                             "lyric_line": line,
#                             "is_active": False,
#                             "date_create": datetime.datetime.now(),
#                             "date_updated": datetime.datetime.now(),
#                         }

#                         logging.debug(values)
#                         query = lyrics.insert()
#                         db_data = await execute_one_db(query=query, values=values)
#                         logging.debug(db_data)
#                         count += 1

#                     return RedirectResponse(
#                         url=f"/bots/lyrics/{twitter_name}", status_code=303
#                     )

#                 except Exception as e:
#                     logger.error(f"Upload error: {e}")
#                     form.lyric_file.errors.append(
#                         "An error occurred while processing. Check file and retry upload."
#                     )

#             else:
#                 logger.error("Not a valid file")
#                 form.lyric_file.errors.append(f"Not a valid file")

#         else:
#             logger.error("Must be a CSV File")
#             form.lyric_file.errors.append("Must be a CSV File")

#     status_code = 200
#     template = f"{page_url}/bot_lyrics.html"
#     context = {
#         "request": request,
#         "bot_data": bot_data,
#         "lyric_data": lyric_data,
#         "current_lyric": current_lyric,
#         "form": form,
#     }
#     return templates.TemplateResponse(template, context, status_code=status_code)


# @csrf_protect
# @login_required.require_login
# async def bot_new(request):

#     form = await forms.NewBotForm.from_formdata(request)
#     form_data = await request.form()

#     if form.validate_on_submit():

#         # check twitter name is unique
#         check_twitter_name = await form_validators.twittername_check(
#             twitter_name=form_data["twitter_name"]
#         )
#         logging.debug(check_twitter_name)

#         image_name = form_data["twitter_name"]

#         image_file_name = form_data["bot_image"].filename
#         contents = await form_data["bot_image"].read()

#         valid_images = ["png", "jpeg", "gif", "jpg"]

#         save_image(file_name=image_file_name.lower(), image_data=contents)
#         image_type = imghdr.what(f"statics/bot_images/{image_file_name}")

#         if image_type not in valid_images:
#             form.twitter_name.errors.append("Only png, jpeg, or gif is allowed")

#         elif check_twitter_name != None:
#             if check_twitter_name["twitter_name"] == form_data["twitter_name"].lower():
#                 logger.error(f'{form_data["twitter_name"]} exists in database')
#                 form.twitter_name.errors.append(
#                     "the twitter name exists within database"
#                 )

#         else:

#             query = bots.insert()
#             values = {
#                 "bot_id": str(uuid.uuid4()),
#                 "bot_type": "lyric",
#                 "bot_group": "a",
#                 "created_by": request.session["user_name"],
#                 "image_name": image_file_name.lower(),
#                 "twitter_name": form_data["twitter_name"].lower(),
#                 "consumer_key": form_data["consumer_key"],
#                 "consumer_secret": form_data["consumer_secret"],
#                 "access_token": form_data["access_token"],
#                 "access_token_secret": form_data["access_token_secret"],
#                 "description": form_data["description"],
#                 "is_active": False,
#                 "date_create": datetime.datetime.now(),
#                 "current_lyric_sequence": 1,
#             }
#             logging.debug(values)
#             db_result = await execute_one_db(query=query, values=values)
#             logger.info("Redirecting user to index page /")
#             return RedirectResponse(url="/", status_code=303)

#     status_code = 200
#     template = f"{page_url}/bot_new.html"
#     context = {"request": request, "form": form}
#     logger.info("page accessed: /bots/new-bot")
#     return templates.TemplateResponse(template, context, status_code=status_code)


# @csrf_protect
# @login_required.require_login
# async def bot_update(request):

#     twitter_name = request.path_params["page"]
#     form = await forms.UpdateBotForm.from_formdata(request)
#     form_data = await request.form()
#     bot_data = await crud.bot_information(twitter_name=twitter_name)
#     logging.debug(str(bot_data))

#     if form.validate_on_submit():

#         # check twitter name is unique
#         check_twitter_name = await form_validators.twittername_check(
#             twitter_name=form_data["twitter_name"]
#         )
#         logging.debug(check_twitter_name)

#         # image_name = form_data["twitter_name"]

#         image_file_name = form_data["bot_image"].filename
#         logger.critical(image_file_name)
#         contents = await form_data["bot_image"].read()
#         logger.critical(type(contents))
#         valid_images = ["png", "jpeg", "gif", "jpg"]

#         if len(image_file_name) == 0:
#             image_name = bot_data["image_name"]
#             logging.debug(f"using form_data for bot_image: {image_name}")
#         else:
#             image_name = image_file_name.lower()

#             save_image(file_name=image_file_name.lower(), image_data=contents)
#             image_type = imghdr.what(f"statics/bot_images/{image_file_name}")

#             if image_type not in valid_images:
#                 form.bot_image.errors.append("Only png, jpeg, or gif is allowed")

#         twitter_name = bot_data["twitter_name"].lower()

#         if form_data["consumer_key"] != bot_data["consumer_key"]:
#             consumer_key = form_data["consumer_key"]
#         else:
#             consumer_key = bot_data["consumer_key"]

#         if form_data["consumer_secret"] != bot_data["consumer_secret"]:
#             consumer_secret = form_data["consumer_secret"]
#         else:
#             consumer_secret = bot_data["consumer_secret"]

#         if form_data["access_token"] != bot_data["access_token"]:
#             access_token = form_data["access_token"]
#         else:
#             access_token = bot_data["access_token"]

#         if form_data["access_token_secret"] != bot_data["access_token_secret"]:
#             access_token_secret = form_data["access_token_secret"]
#         else:
#             access_token_secret = bot_data["access_token_secret"]

#         if form_data["description"] != bot_data["description"]:
#             description = form_data["description"]
#         else:
#             description = bot_data["description"]

#         query = bots.update().where(bots.c.twitter_name == twitter_name)
#         values = {
#             # "bot_id": "uuid",
#             "image_name": image_name,
#             "twitter_name": twitter_name,
#             "consumer_key": consumer_key,
#             "consumer_secret": consumer_secret,
#             "access_token": access_token,
#             "access_token_secret": access_token_secret,
#             "description": description,
#             "date_updated": datetime.datetime.now(),
#         }
#         logging.debug(values)
#         db_result = await execute_one_db(query=query, values=values)
#         logger.info("Redirecting user to index page /")
#         return RedirectResponse(url="/", status_code=303)

#     status_code = 200
#     template = f"{page_url}/bot_update.html"
#     context = {
#         "request": request,
#         "form": form,
#         "bot_data": bot_data,
#     }
#     logger.info(f"page accessed: /bots/update/{twitter_name}")
#     return templates.TemplateResponse(template, context, status_code=status_code)
