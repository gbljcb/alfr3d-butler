#!/usr/bin/python
# -*- coding: utf-8 -*-

###################################
#          versao beta
#              PR1V8
#      https://telegram.me/pr1v8
#      http://pr1v8.co.nf
#
####################################

import time
import telepot
import re
import os
import sys

reload(sys)  
sys.setdefaultencoding('utf8')

def handle(msg):
	#send response func
	def response(id, response):
		bot.sendMessage(id, response, reply_to_message_id=chat_msgid, parse_mode='Markdown')
	
	#chat_var
	chat_id = msg['chat']['id']
	chat_msgid = msg['message_id']
	#user_var
	user_id = msg['from']['id']
	user_username = msg['from']['username']
	user_name = msg['from']['first_name']
	user_cusername = "@" + user_username
	#messages_var
	message = msg['text'].split()
	command = re.sub('\@alfr3d_bot$', '', message[0])
	len_msg = len(message)
	#func var
		#check if user has an @username
	if len(user_username) > 4:
		nick_afk = user_cusername + "\n"
	else:
		nick_afk = user_name

    #cli-output
	print 'Command: {} - from user: {}, id: {}'.format(command, user_username, user_id)

   #allowed commands
	list_commands = ['/id', '/afk', '/back', '/afklist', '/afkclean']


    #command interpretation
	if command in list_commands:
    	#id cmd
		if command == '/id':
			id_response = "_Seu id é: {}_".format(user_id)
			response(chat_id, id_response)
	    
	    #afk cmd
		if command == '/afk':
            #check if @username is already in afklist.txt
			afklist_read = open("afklist.txt",'r')
			afklist_data = afklist_read.read()            
            
			if nick_afk in afklist_data:
				pass
			else: #if not, write @username in afklist.txt
				afklist_open = open("afklist.txt", "a")
				afklist_open.write(nick_afk)
				afklist_open.close()
			afklist_read.close()

			#afk bot response
			if len_msg > 1:
				#set limit to afk_reason
				afk_reason = msg['text'].split(' ', 1)[1]
				if len(afk_reason) > 20:
					afk_response = "User *{}* is *AFK*.".format(user_cusername)
				else:
					afk_response = "User *{}* is *AFK*.\nDoing what: _{}_.".format(user_cusername, afk_reason)
			else:
				afk_response = "User *{}* is *AFK*.".format(user_cusername)

			response(chat_id, afk_response)

		#back cmd
		if command ==  '/back':			
			#open & read afklist.txt 
			afklist_read = open("afklist.txt",'r')
			afklist_data = afklist_read.read()
			
			if not nick_afk in afklist_data:
				pass
				afklist_read.close()
			else:
	            #update afklist.txt
				afklist_newdata = afklist_data.replace(nick_afk, "")
				afklist_open = open("afklist.txt", "w")
				afklist_data = afklist_open.write(afklist_newdata)
				afklist_open.close()

				back_response = "User *{}* is back.".format(user_cusername)
				response(chat_id, back_response)

        #afklist cmd
		if command == '/afklist':
        	#open & filter & prepare for response afklist.txt
			afklist_read = open("afklist.txt", "r")
			afklist_data = afklist_read.read().strip('\n').strip("_")
			afklist_data = os.linesep.join([s for s in afklist_data.splitlines() if s])

            #check if there is @username afk
			if len(afklist_data) > 0:
				afklist_read.close()
				response(chat_id, afklist_data)
			else: 
				afklist_response = "*No user is AFK*"
				response(chat_id, afklist_response)

        #afkclean cmd
		if command == '/afkclean':
			admin_list = ['pr1mus']

			if user_username in admin_list:
        		#delete afklist.txt
				with open("afklist.txt", "w"):
					pass
				afkclean_response = "_afklist.txt_ was deleted."
				response(chat_id, afkclean_response)
	else:
		pass

bot = telepot.Bot('YOUR_APIKEY')
bot.message_loop(handle)
print 'I am listening ...'

while 1:
	time.sleep(5)
