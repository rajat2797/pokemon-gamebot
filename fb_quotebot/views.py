#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import re
import random
import pprint
import requests

# Create your views here.

VERIFY_TOKEN = '7thseptember2016'
PAGE_ACCESS_TOKEN = 'EAAP6lh2PEW4BAHZB1M54SRc3bQVyBZAR7qIdMBR57UdvIZAntnk3JyOhzz6TPpIEEVZBIgenCw5vsC16OsyS3LnZCCxlaQjZCRoDRSZBdPNRSnm6FD1mKjrFAfoualmcBMNnMpf8l6He7qZALB9Y53xA5PdcvwZA50LO304GbTVzEPwZDZD'

pokemon_data = {"Bulbasaur":"http://img.pokemondb.net/artwork/bulbasaur.jpg","Ivysaur":"http://img.pokemondb.net/artwork/ivysaur.jpg","Venusaur":"http://img.pokemondb.net/artwork/venusaur.jpg","Charmander":"http://img.pokemondb.net/artwork/charmander.jpg","Charmeleon":"http://img.pokemondb.net/artwork/charmeleon.jpg","Charizard":"http://img.pokemondb.net/artwork/charizard.jpg","Squirtle":"http://img.pokemondb.net/artwork/squirtle.jpg","Wartortle":"http://img.pokemondb.net/artwork/wartortle.jpg","Blastoise":"http://img.pokemondb.net/artwork/blastoise.jpg","Caterpie":"http://img.pokemondb.net/artwork/caterpie.jpg","Metapod":"http://img.pokemondb.net/artwork/metapod.jpg","Butterfree":"http://img.pokemondb.net/artwork/butterfree.jpg","Weedle":"http://img.pokemondb.net/artwork/weedle.jpg","Kakuna":"http://img.pokemondb.net/artwork/kakuna.jpg","Beedrill":"http://img.pokemondb.net/artwork/beedrill.jpg","Pidgey":"http://img.pokemondb.net/artwork/pidgey.jpg","Pidgeotto":"http://img.pokemondb.net/artwork/pidgeotto.jpg","Pidgeot":"http://img.pokemondb.net/artwork/pidgeot.jpg","Rattata":"http://img.pokemondb.net/artwork/rattata.jpg","Raticate":"http://img.pokemondb.net/artwork/raticate.jpg","Spearow":"http://img.pokemondb.net/artwork/spearow.jpg","Fearow":"http://img.pokemondb.net/artwork/fearow.jpg","Ekans":"http://img.pokemondb.net/artwork/ekans.jpg","Arbok":"http://img.pokemondb.net/artwork/arbok.jpg","Pikachu":"http://img.pokemondb.net/artwork/pikachu.jpg","Raichu":"http://img.pokemondb.net/artwork/raichu.jpg","Sandshrew":"http://img.pokemondb.net/artwork/sandshrew.jpg","Sandslash":"http://img.pokemondb.net/artwork/sandslash.jpg","Nidoran":"http://vignette1.wikia.nocookie.net/pokemon/images/2/22/029Nidoran_AG_anime.png/revision/latest?cb=20140914053937","Nidorina":"http://img.pokemondb.net/artwork/nidorina.jpg","Nidoqueen":"http://img.pokemondb.net/artwork/nidoqueen.jpg","Nidorino":"http://img.pokemondb.net/artwork/nidorino.jpg","Nidoking":"http://img.pokemondb.net/artwork/nidoking.jpg","Clefairy":"http://img.pokemondb.net/artwork/clefairy.jpg","Clefable":"http://img.pokemondb.net/artwork/clefable.jpg","Vulpix":"http://img.pokemondb.net/artwork/vulpix.jpg","Ninetales":"http://img.pokemondb.net/artwork/ninetales.jpg","Jigglypuff":"http://img.pokemondb.net/artwork/jigglypuff.jpg","Wigglytuff":"http://img.pokemondb.net/artwork/wigglytuff.jpg","Zubat":"http://img.pokemondb.net/artwork/zubat.jpg","Golbat":"http://img.pokemondb.net/artwork/golbat.jpg","Oddish":"http://img.pokemondb.net/artwork/oddish.jpg","Gloom":"http://img.pokemondb.net/artwork/gloom.jpg","Vileplume":"http://img.pokemondb.net/artwork/vileplume.jpg","Paras":"http://img.pokemondb.net/artwork/paras.jpg","Parasect":"http://img.pokemondb.net/artwork/parasect.jpg","Venonat":"http://img.pokemondb.net/artwork/venonat.jpg","Venomoth":"http://img.pokemondb.net/artwork/venomoth.jpg","Diglett":"http://img.pokemondb.net/artwork/diglett.jpg","Dugtrio":"http://img.pokemondb.net/artwork/dugtrio.jpg","Meowth":"http://img.pokemondb.net/artwork/meowth.jpg","Persian":"http://img.pokemondb.net/artwork/persian.jpg","Psyduck":"http://img.pokemondb.net/artwork/psyduck.jpg","Golduck":"http://img.pokemondb.net/artwork/golduck.jpg","Mankey":"http://img.pokemondb.net/artwork/mankey.jpg","Primeape":"http://img.pokemondb.net/artwork/primeape.jpg","Growlithe":"http://img.pokemondb.net/artwork/growlithe.jpg","Arcanine":"http://img.pokemondb.net/artwork/arcanine.jpg","Poliwag":"http://img.pokemondb.net/artwork/poliwag.jpg","Poliwhirl":"http://img.pokemondb.net/artwork/poliwhirl.jpg","Poliwrath":"http://img.pokemondb.net/artwork/poliwrath.jpg","Abra":"http://img.pokemondb.net/artwork/abra.jpg","Kadabra":"http://img.pokemondb.net/artwork/kadabra.jpg","Alakazam":"http://img.pokemondb.net/artwork/alakazam.jpg","Machop":"http://img.pokemondb.net/artwork/machop.jpg","Machoke":"http://img.pokemondb.net/artwork/machoke.jpg","Machamp":"http://img.pokemondb.net/artwork/machamp.jpg","Bellsprout":"http://img.pokemondb.net/artwork/bellsprout.jpg","Weepinbell":"http://img.pokemondb.net/artwork/weepinbell.jpg","Victreebel":"http://img.pokemondb.net/artwork/victreebel.jpg","Tentacool":"http://img.pokemondb.net/artwork/tentacool.jpg","Tentacruel":"http://img.pokemondb.net/artwork/tentacruel.jpg","Geodude":"http://img.pokemondb.net/artwork/geodude.jpg","Graveler":"http://img.pokemondb.net/artwork/graveler.jpg","Golem":"http://img.pokemondb.net/artwork/golem.jpg","Ponyta":"http://img.pokemondb.net/artwork/ponyta.jpg","Rapidash":"http://img.pokemondb.net/artwork/rapidash.jpg","Slowpoke":"http://img.pokemondb.net/artwork/slowpoke.jpg","Slowbro":"http://img.pokemondb.net/artwork/slowbro.jpg","Magnemite":"http://img.pokemondb.net/artwork/magnemite.jpg","Magneton":"http://img.pokemondb.net/artwork/magneton.jpg","Farfetch'd":"http://vignette3.wikia.nocookie.net/pokemon/images/6/61/083Farfetch'd_AG_anime.png/revision/latest?cb=20140810002805","Doduo":"http://img.pokemondb.net/artwork/doduo.jpg","Dodrio":"http://img.pokemondb.net/artwork/dodrio.jpg","Seel":"http://img.pokemondb.net/artwork/seel.jpg","Dewgong":"http://img.pokemondb.net/artwork/dewgong.jpg","Grimer":"http://img.pokemondb.net/artwork/grimer.jpg","Muk":"http://img.pokemondb.net/artwork/muk.jpg","Shellder":"http://img.pokemondb.net/artwork/shellder.jpg","Cloyster":"http://img.pokemondb.net/artwork/cloyster.jpg","Gastly":"http://img.pokemondb.net/artwork/gastly.jpg","Haunter":"http://img.pokemondb.net/artwork/haunter.jpg","Gengar":"http://img.pokemondb.net/artwork/gengar.jpg","Onix":"http://img.pokemondb.net/artwork/onix.jpg","Drowzee":"http://img.pokemondb.net/artwork/drowzee.jpg","Hypno":"http://img.pokemondb.net/artwork/hypno.jpg","Krabby":"http://img.pokemondb.net/artwork/krabby.jpg","Kingler":"http://img.pokemondb.net/artwork/kingler.jpg","Voltorb":"http://img.pokemondb.net/artwork/voltorb.jpg","Electrode":"http://img.pokemondb.net/artwork/electrode.jpg","Exeggcute":"http://img.pokemondb.net/artwork/exeggcute.jpg","Exeggutor":"http://img.pokemondb.net/artwork/exeggutor.jpg","Cubone":"http://img.pokemondb.net/artwork/cubone.jpg","Marowak":"http://img.pokemondb.net/artwork/marowak.jpg","Hitmonlee":"http://img.pokemondb.net/artwork/hitmonlee.jpg","Hitmonchan":"http://img.pokemondb.net/artwork/hitmonchan.jpg","Lickitung":"http://img.pokemondb.net/artwork/lickitung.jpg","Koffing":"http://img.pokemondb.net/artwork/koffing.jpg","Weezing":"http://img.pokemondb.net/artwork/weezing.jpg","Rhyhorn":"http://img.pokemondb.net/artwork/rhyhorn.jpg","Rhydon":"http://img.pokemondb.net/artwork/rhydon.jpg","Chansey":"http://img.pokemondb.net/artwork/chansey.jpg","Tangela":"http://img.pokemondb.net/artwork/tangela.jpg","Kangaskhan":"http://img.pokemondb.net/artwork/kangaskhan.jpg","Horsea":"http://img.pokemondb.net/artwork/horsea.jpg","Seadra":"http://img.pokemondb.net/artwork/seadra.jpg","Goldeen":"http://img.pokemondb.net/artwork/goldeen.jpg","Seaking":"http://img.pokemondb.net/artwork/seaking.jpg","Staryu":"http://img.pokemondb.net/artwork/staryu.jpg","Starmie":"http://img.pokemondb.net/artwork/starmie.jpg","Mr. Mime":"http://guidesarchive.ign.com/guides/9846/images/mrmime.gif","Scyther":"http://img.pokemondb.net/artwork/scyther.jpg","Jynx":"http://img.pokemondb.net/artwork/jynx.jpg","Electabuzz":"http://img.pokemondb.net/artwork/electabuzz.jpg","Magmar":"http://img.pokemondb.net/artwork/magmar.jpg","Pinsir":"http://img.pokemondb.net/artwork/pinsir.jpg","Tauros":"http://img.pokemondb.net/artwork/tauros.jpg","Magikarp":"http://img.pokemondb.net/artwork/magikarp.jpg","Gyarados":"http://img.pokemondb.net/artwork/gyarados.jpg","Lapras":"http://img.pokemondb.net/artwork/lapras.jpg","Ditto":"http://img.pokemondb.net/artwork/ditto.jpg","Eevee":"http://img.pokemondb.net/artwork/eevee.jpg","Vaporeon":"http://img.pokemondb.net/artwork/vaporeon.jpg","Jolteon":"http://img.pokemondb.net/artwork/jolteon.jpg","Flareon":"http://img.pokemondb.net/artwork/flareon.jpg","Porygon":"http://img.pokemondb.net/artwork/porygon.jpg","Omanyte":"http://img.pokemondb.net/artwork/omanyte.jpg","Omastar":"http://img.pokemondb.net/artwork/omastar.jpg","Kabuto":"http://img.pokemondb.net/artwork/kabuto.jpg","Kabutops":"http://img.pokemondb.net/artwork/kabutops.jpg","Aerodactyl":"http://img.pokemondb.net/artwork/aerodactyl.jpg","Snorlax":"http://img.pokemondb.net/artwork/snorlax.jpg","Articuno":"http://img.pokemondb.net/artwork/articuno.jpg","Zapdos":"http://img.pokemondb.net/artwork/zapdos.jpg","Moltres":"http://img.pokemondb.net/artwork/moltres.jpg","Dratini":"http://img.pokemondb.net/artwork/dratini.jpg","Dragonair":"http://img.pokemondb.net/artwork/dragonair.jpg","Dragonite":"http://img.pokemondb.net/artwork/dragonite.jpg","Mewtwo":"http://img.pokemondb.net/artwork/mewtwo.jpg","Mew":"http://img.pokemondb.net/artwork/mew.jpg"}
score=0

def quiz_gen():
	pokemon_arr=[]
	for k,v in pokemon_data.iteritems():
		pokemon_arr.append([k,v])
	random.shuffle(pokemon_arr)
	answer=pokemon_arr[0]
	options= [i[0] for i in pokemon_arr[1:4]]
	options.append(answer[0])
	random.shuffle(options)
	return dict(answer=answer,options=options)

def index(request):
	# print type(request.GET)
	# t = request.GET.get('text') or 'foo'
	colour=request.GET['text']
	# output_text= quiz_gen()
	# return HttpResponse(output_text['options'],content_type="application/json")
	return HttpResponse(search_colour(colour))

def giphy(search_query):
	url='http://api.giphy.com/v1/gifs/search?q=%s&api_key=dc6zaTOxFJmzC'%(search_query)
	resp=requests.get(url=url).text
	data=json.loads(resp)
	l = len(data['data'])
	i = random.randint(0,l)
	return data['data'][i]['images']['fixed_height']['url']

def scrape_spreadsheet():
	url = 'https://spreadsheets.google.com/feeds/list/1FChO1iS-SnEw9a3JUnUT1ZInLfCaETpvYb7Y_2egOq0/od6/public/values?alt=json'
	resp=requests.get(url=url).text
	data=json.loads(resp)
	arr=[]
	for entry in data['feed']['entry']:	
		# print entry['gsx$name']['$t']
		d=dict(colour_name=entry['gsx$name']['$t'],colour_hex=entry['gsx$colour1']['$t'])
		arr.append(d)
	# although it would be better to create a json object and then return it as it will be fast
	return arr

def search_colour(text):
	colour_arr=scrape_spreadsheet()
	for colour in colour_arr:
		if text in colour['colour_name']:
			return colour
	random.shuffle(colour_arr)
	return colour_arr[0]

def set_greeting():
	post_message_url = "https://graph.facebook.com/v2.6/me/thread_settings?access_token%s"%PAGE_ACCESS_TOKEN
	response_msg = {
				"setting_type":"greeting",
				  "greeting":{
				    "text":"Pokemon Quiz Bot"
				  }
	}
	response_msg = json.dumps(response_msg)
	status=requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	logg(status.text,'---GR---')

def post_facebook_message(fbid,message_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	matching_colour = search_colour(message_text)
	image_url = 'https://dummyimage.com/100x100/%s/%s.png'%(matching_colour['colour_hex'],matching_colour['colour_hex'])
	output_text = '%s : %s'%(matching_colour['colour_name'],matching_colour['colour_hex'])
	response_msg_image = {
				"recipient":{
				    "id":fbid
				  },
				  "message":{
				    "attachment":{
				      "type":"image",
				      "payload":{
				        "url":image_url
				      }
				    }
				  }

	}
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":output_text}})
	requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg_image)

def post_facebook_message_old(fbid,message_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	# output_text = wikisearch(message_text)
	# output_text,output_url,output_image=jokes()
	# output_image='http://thecatapi.com/api/images/get?format=src&type=png'
	output_text=quiz_gen()
	# output_text_with_button = {
	# 		  "recipient":{
	# 		    "id":fbid
	# 		  },
	# 		  "message":{
	# 		    "attachment":{
	# 		      "type":"template",
	# 		      "payload":{
	# 		        "template_type":"button",
	# 		        "text":output_text,
	# 		        "buttons":[
	# 		          {
	# 		            "type":"web_url",
	# 		            "url": output_url,
	# 		            "title":"Show Website"
	# 		          },
	# 		          {
	# 		            "type":"postback",
	# 		            "title":"Another Joke",
	# 		            "payload":"USER_DEFINED_PAYLOAD"
	# 		          }
	# 		        ]
	# 		      }
	# 		    }
	# 		  }
	# 		}

	# response_msg_generic = {
	# 			  "recipient":{
	# 			    "id":fbid
	# 			  },
	# 			  "message":{
	# 			    "attachment":{
	# 			      "type":"template",
	# 			      "payload":{
	# 			        "template_type":"generic",
	# 			        "elements":[
	# 			          {
	# 			            "title":output_text,
	# 			            "item_url":output_url,
	# 			            "image_url":output_image,
	# 			            "subtitle":output_text,
	# 			            "buttons":[
	# 			              {
	# 			                "type":"web_url",
	# 			                "url":output_url,
	# 			                "title":"View Website"
	# 			              },
	# 			              {
	# 			                "type":"postback",
	# 			                "title":"Another Joke",
	# 			                "payload":"DEVELOPER_DEFINED_PAYLOAD"
	# 			              }              
	# 			            ]
	# 			          },
	# 			          {
	# 			            "title":output_text,
	# 			            "item_url":output_url,
	# 			            "image_url":output_image,
	# 			            "subtitle":output_text,
	# 			            "buttons":[
	# 			              {
	# 			                "type":"web_url",
	# 			                "url":output_url,
	# 			                "title":"View Website"
	# 			              },
	# 			              {
	# 			                "type":"postback",
	# 			                "title":"Another Joke",
	# 			                "payload":"DEVELOPER_DEFINED_PAYLOAD"
	# 			              }              
	# 			            ]
	# 			          }
	# 			        ]
	# 			      }
	# 			    }
	# 			  }
	# 			}
	response_msg_score = {
				"recipient":{
				    "id":fbid
				  },
				  "message":{
				    "attachment":{
				      "type":"template",
				      "payload":{
				        "template_type":"generic",
				        "elements":[
				          {
				            "title":"SCORE : %d"%(score),
				            "buttons":[
				              {
				                "type":"element_share"
				              }              
				            ]
				          }
				        ]
				      }
				    }
				  }
	}

	response_msg_image = {
				"recipient":{
				    "id":fbid
				  },
				  "message":{
				    "attachment":{
				      "type":"image",
				      "payload":{
				        "url":output_text['answer'][1]
				      }
				    }
				  }

	}

	response_msg_quickreply = {
				"recipient":{
				    "id":fbid
				  },
				  "message":{
				    "text":"Who is this Pokemon?",
				    "quick_replies":[
				      {
				        "content_type":"text",
				        "title":output_text['options'][3],
				        "payload":"%s:%s"%(output_text['options'][3],output_text['answer'][0])
				      },
				      {
				        "content_type":"text",
				        "title":output_text['options'][1],
				        "payload":"%s:%s"%(output_text['options'][1],output_text['answer'][0])
				      },
				      {
				        "content_type":"text",
				        "title":output_text['options'][2],
				        "payload":"%s:%s"%(output_text['options'][2],output_text['answer'][0])
				      },
				      {
				        "content_type":"text",
				        "title":output_text['options'][0],
				        "payload":"%s:%s"%(output_text['options'][0],output_text['answer'][0])
				      }
				    ]
				  }
	}

	# response_msg = json.dumps(output_text_with_button)
	# response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":output_text}})
	# response_msg = json.dumps(response_msg_generic)
	response_msg = json.dumps(response_msg_quickreply)
	response_msg_img=json.dumps(response_msg_image)
	response_msg_scoreit=json.dumps(response_msg_score)
	
	# output_text = search_colour(message_text)
	
	# response_msg = json.dumps(output_text)
	requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg_img)
	requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg_scoreit)
	requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	
def logg(message,symbol='-'):
	print '%s\n %s\n %s\n'%(symbol*10,message,symbol*10)

def handle_postback(fbid,payload):
	# post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	# response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":"output_text"}})
	# status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	logg(payload,symbol='*')
	post_facebook_message(fbid,payload)

def handle_quickreply(fbid,payload):
	if not payload:
		return
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	# response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":"output_text"}})
	# status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	logg(payload,symbol='-------QR----')
	a,b=payload.split(':')
	if a==b:
		logg('CORRECT','-YES-')
		# global score
		# score+=1
		output_text='Correct Answer'
		giphy_image_url = giphy('YES,correct,good')
	else:
		logg('WRONG','-NO-')
		output_text='Wrong Answer'
		giphy_image_url = giphy('NO,wrong,bad')

	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":output_text}})
	response_image_msg = {
				"recipient":{
				    "id":fbid
				  },
				  "message":{
				    "attachment":{
				      "type":"image",
				      "payload":{
				        "url": giphy_image_url
				      }
				    }
				  }
	}

	response_image_msg = json.dumps(response_image_msg)
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_image_msg)
	# return

class MyChatBotView(generic.View):
	def get (self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Oops invalid token')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message= json.loads(self.request.body.decode('utf-8'))
		# print incoming_message
		logg(incoming_message)

		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				print message
				try:
					if 'postback' in message:
						handle_postback(message['sender']['id'],message['postback']['payload'])
						return HttpResponse()
					else:
						pass
				except Exception, e:
					logg(e,symbol='-140-')

				try:
					if 'quick_reply' in message['message']:
						# logg(message['message']['quick_reply']['payload'],symbol='--------------avnaua------------')
						handle_quickreply(message['sender']['id'],message['message']['quick_reply']['payload'])
						# return HttpResponse()
					else:
						pass
				except Exception, e:
					logg(e,symbol='-140-')


				try:
					sender_id = message['sender']['id']
					message_text = message['message']['text']
					post_facebook_message(sender_id,message_text) 
					# jokes(sender_id)
				except Exception as e:
					print e
					pass

		return HttpResponse()  

