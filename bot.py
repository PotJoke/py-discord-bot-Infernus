import discord
from discord import Option
from discord.ext import commands #Дискорд

from Cybernator import Paginator as pag #Интерактивные сообщения

import sqlite3 #Таблицы

import random #Оффлайн рандомайзер

from emoji import COIN, PAW_L, PAW_R, REP, EXP, LVL #Кастомные эмодзи дискорд
from config import TOKEN

prefix = ("/")

client = discord.Bot(intents=discord.Intents.all())

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

#Запуск, проверка, таблицы
@client.event
async def on_ready():
	print('Запуск прошёл успешно')

	cursor.execute("""CREATE TABLE IF NOT EXISTS users ( 
		name TEXT, 
		id INT, 
		cash BIGINT, 
		rep INT,
		exp BIGINT, 
		lvl INT,
		server_id INT
	)""")
	connection.commit()

	cursor.execute("""CREATE TABLE IF NOT EXISTS shop ( 
		role_id INT,
		id INT,
		cost BIGINT
	)""")
	connection.commit()

	cursor.execute("""CREATE TABLE IF NOT EXISTS s_guild(
		id BIGINT,
		newbie_id BIGINT,
		help BOOLEAN,
		finance BOOLEAN,
		prediction BOOLEAN,
		profile BOOLEAN,
		VK TEXT,
		YOUTUBE TEXT,
		TIKTOK TEXT,
		TWITTER TEXT
		)""")
	connection.commit()

	for guild in client.guilds:
		for member in guild.members:
			if cursor.execute(f'SELECT id FROM users WHERE id = {member.id}').fetchone() is None:
				cursor.execute(f'INSERT INTO users VALUES ("{member}", {member.id}, 0, 0, 0, 1, {guild.id})')
				connection.commit()
			else:
				pass

@client.event #Операции с новичками
async def on_member_join(member):

	r = cursor.execute("SELECT newbie_id FROM s_guild WHERE id = {}".format(member.guild.id)).fetchone()[0]

	VK = cursor.execute("SELECT VK FROM s_guild WHERE id = {}".format(member.guild.id)).fetchone()[0]
	YT = cursor.execute("SELECT YOUTUBE FROM s_guild WHERE id = {}".format(member.guild.id)).fetchone()[0]
	TT = cursor.execute("SELECT TIKTOK FROM s_guild WHERE id = {}".format(member.guild.id)).fetchone()[0]
	TW = cursor.execute("SELECT TWITTER FROM s_guild WHERE id = {}".format(member.guild.id)).fetchone()[0]

	if cursor.execute('SELECT id FROM users WHERE id = {}'.format(member.id)).fetchone() is None:
		cursor.execute('INSERT INTO users VALUES ("{}", {}, 0, 0, 0, 1, {})'.format(member, member.id, member.guild.id))
		connection.commit()

	else:
		if r == 0:
			pass

		else:
			role = member.guild.get_role(int(r))
			await member.add_roles(role)

	await member.send('Привет, я приветствую тебя на моём сервере uwu.\n Рекомендую ознакомится с правилами и вообще с проектом.\n Также познакомься с кем-нибудь, подружись и веди себя хорошо, если будешь много ругаться плохими словами, то нам придётся зашить тебе ротик на время :(')

	if VK != "off" or YT != "off" or TT != "off" or TW != "off":
		await member.send("Также рекомендую ознакомиться с нашими другими ресурсами")

		if VK != "off":
			await member.send("Вконтакте: " + VK)
		if YT != "off":
			await member.send("Ютуб: " + YT)
		if TT != "off":
			await member.send("Тикток: " + TT)
		if TW != "off":
			await member.send("Твиттер: " + TW)

#Кастомизация под сервер
@client.command(description="[Только Админы] Настройка бота под сервер.  (Для перелистывания страниц исп. эмодзи)")
@commands.has_permissions(administrator=True)
async def start(ctx):

	await ctx.defer()

	server_id = ctx.guild.id

	if cursor.execute("SELECT id FROM s_guild WHERE id = {}".format(server_id)).fetchone() is None:
		cursor.execute("""INSERT INTO s_guild VALUES ({}, 0, {}, {}, {}, {}, 'off', 'off', 'off', 'off')""".format(server_id, True, True, True, True))
		connection.commit()
	else:
		pass

	embed1 = discord.Embed(title="**Оглавление**", description="Ниже приведены разделы с командами для кастомизации бота под сервер. Чтобы переключаться между страницами используйте эмодзи под сообщением.", color = discord.Color.red())
	embed1.add_field(name="Команды для включения/отключения команд", value="__стр 2__", inline = False)
	embed1.add_field(name="Команды для редактирования контента для новых участников (ссылки на другие ресурсы, роль новичкам)", value="__стр 3__", inline = False)

	embed2 = discord.Embed(title="**Команды для включения/отключения команд**", description="", color=discord.Color.blue())
	embed2.add_field(name= prefix + "s_all (True/False)", value="Отключить все нижеперечисленные команды", inline = False)
	embed2.add_field(name= prefix + "s_help (True/False)", value="Отключить команду **help**", inline = False)
	embed2.add_field(name= prefix + "s_finance (True/False)", value="Отключить команды связанные с финансами **(balance, givemoney, takemoney, newrole, updaterole, delrole, shop, buy, lotery, leaderboard)**", inline = False)
	embed2.add_field(name= prefix + "s_prediction (True/False)", value="Отключить команду **prediction**", inline = False)
	embed2.add_field(name= prefix + "s_profile (True/False)", value="Отключить команду, связанную с профилем **(profile, xp, lvl, lvlup, rep, giverep, takerep)**", inline = False)
	
	embed3 = discord.Embed(title="**Команды для редактирования контента для новых участников**", description="", color=discord.Color.purple())
	embed3.add_field(name= prefix + "newbie_role @роль", value="Настраивает роль, получаемую участниками при присоединении. По умолчанию отключенно", inline = False)
	embed3.add_field(name= prefix + "s_VK ссылка", value= "Добавить ссылку на Вконтакте. Для отключения напишите вместо ссылки **off**", inline= False)
	embed3.add_field(name= prefix + "s_YT ссылка", value= "Добавить ссылку на Ютуб. Для отключения напишите вместо ссылки **off**", inline= False)
	embed3.add_field(name= prefix + "s_TT ссылка", value= "Добавить ссылку на ТикТок. Для отключения напишите вместо ссылки **off**", inline= False)
	embed3.add_field(name= prefix + "s_TW ссылка", value= "Добавить ссылку на Твиттер. Для отключения напишите вместо ссылки **off**", inline= False)

	embeds = [embed1, embed2, embed3]

	message = await ctx.respond(embed = embed1)

	page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer = False, reactions = [PAW_L, PAW_R])
	await page.start()

@client.command(description="[Только Админы] Роль, выдаваемая при присоединении на сервер.")
@commands.has_permissions(administrator=True)
async def newbie_role(
	ctx, 
	role: Option(discord.Role, description='Роль выдаваемая новичкам на сервере', required=True)
	):

	await ctx.defer()

	server_id = ctx.guild.id
	if cursor.execute("SELECT id FROM s_guild WHERE id = {}".format(server_id)).fetchone() is None:
		cursor.execute("INSERT INTO s_guild VALUES ({}, 0, {}, {}, {}, {}, {}, {}, {}, {})".format(server_id, True, True, True, True, "off", "off", "off", "off"))
		connection.commit()
	else:
		cursor.execute("UPDATE s_guild SET newbie_id = {} WHERE id = {}".format(role.id, ctx.guild.id))
		connection.commit()

	await ctx.respond(f"Успешно выполнено. Теперь роль для новичков - @{role.name}")

@client.command(description="[Только Админы] Работа команды help - True/False. (По умолчанию True)")
@commands.has_permissions(administrator=True)
async def s_help(ctx, 
	availability: Option(bool, description="True/False", required=True)):

	await ctx.defer()

	server_id = ctx.guild.id

	if cursor.execute("SELECT id FROM s_guild WHERE id = {}".format(server_id)).fetchone() is None:
		cursor.execute("""INSERT INTO s_guild VALUES ({}, 0, {}, {}, {}, {}, 'off', 'off', 'off', 'off')""".format(server_id, True, True, True, True))
		connection.commit()
	else:
		pass

	if availability == True:
		cursor.execute("UPDATE s_guild SET help = {} WHERE id = {}".format(True, ctx.guild.id))
	elif availability == False:
		cursor.execute("UPDATE s_guild SET help = {} WHERE id = {}".format(False, ctx.guild.id))
	await ctx.respond(f'Успешно выполнено. Состояние по умолчанию - **{availability}**')

@client.command(description="[Только Админы] Работа команд напрвленных на работу с финансами - True/False. (По умолчанию True)")
@commands.has_permissions(administrator=True)
async def s_finance(ctx, 
	availability: Option(bool, description="True/False", required=True)):

	await ctx.defer()

	server_id = ctx.guild.id

	if cursor.execute("SELECT id FROM s_guild WHERE id = {}".format(server_id)).fetchone() is None:
		cursor.execute("""INSERT INTO s_guild VALUES ({}, 0, {}, {}, {}, {}, 'off', 'off', 'off', 'off')""".format(server_id, True, True, True, True))
		connection.commit()
	else:
		pass

	if availability== True:
		cursor.execute("UPDATE s_guild SET finance = {} WHERE id = {}".format(True, ctx.guild.id))
	elif availability == False:
		cursor.execute("UPDATE s_guild SET finance = {} WHERE id = {}".format(False, ctx.guild.id))
	await ctx.respond(f'Успешно выполнено. Состояние по умолчанию - **{availability}**')

@client.command(description="[Только Админы] Работа команды prediction - True/False. (По умолчанию True)")
@commands.has_permissions(administrator=True)
async def s_prediction(ctx, 
	availability: Option(bool, description="True/False", required=True)):

	await ctx.defer()

	server_id = ctx.guild.id

	if cursor.execute("SELECT id FROM s_guild WHERE id = {}".format(server_id)).fetchone() is None:
		cursor.execute("""INSERT INTO s_guild VALUES ({}, 0, {}, {}, {}, {}, 'off', 'off', 'off', 'off')""".format(server_id, True, True, True, True))
		connection.commit()
	else:
		pass

	if availability == True:
		cursor.execute("UPDATE s_guild SET prediction = {} WHERE id = {}".format(True, ctx.guild.id))
	elif availability == False:
		cursor.execute("UPDATE s_guild SET prediction = {} WHERE id = {}".format(False, ctx.guild.id))
	await ctx.respond(f'Успешно выполнено. Состояние по умолчанию - **{availability}**')

@client.command(description="[Только Админы] Работа команд направленных на работу с профилем - True/False. (По умолчанию True)")
@commands.has_permissions(administrator=True)
async def s_profile(ctx, 
	availability: Option(bool, description="True/False", required=True)):

	await ctx.defer()

	server_id = ctx.guild.id

	if cursor.execute("SELECT id FROM s_guild WHERE id = {}".format(server_id)).fetchone() is None:
		cursor.execute("""INSERT INTO s_guild VALUES ({}, 0, {}, {}, {}, {}, 'off', 'off', 'off', 'off')""".format(server_id, True, True, True, True))
		connection.commit()
	else:
		pass

	if availability == True:
		cursor.execute("UPDATE s_guild SET profile = {} WHERE id = {}".format(True, ctx.guild.id))
	elif availability == False:
		cursor.execute("UPDATE s_guild SET profile = {} WHERE id = {}".format(False, ctx.guild.id))
	await ctx.respond(f'Успешно выполнено. Состояние по умолчанию - **{availability}**')

@client.command(description="[Только Админы] Работа всех пользовательских команд - True/False. (По умолчанию True)")
@commands.has_permissions(administrator=True)
async def s_all(ctx, 
	availability: Option(bool, description="True/False", required=True)):

	await ctx.defer()

	server_id = ctx.guild.id

	if cursor.execute("SELECT id FROM s_guild WHERE id = {}".format(server_id)).fetchone() is None:
		cursor.execute("""INSERT INTO s_guild VALUES ({}, 0, {}, {}, {}, {}, 'off', 'off', 'off', 'off')""".format(server_id, True, True, True, True))
		connection.commit()
	else:
		pass

	cursor.execute("UPDATE s_guild SET help = {} WHERE id = {}".format(availability, ctx.guild.id))
	cursor.execute("UPDATE s_guild SET finance = {} WHERE id = {}".format(availability, ctx.guild.id))
	cursor.execute("UPDATE s_guild SET prediction = {} WHERE id = {}".format(availability, ctx.guild.id))
	cursor.execute("UPDATE s_guild SET profile = {} WHERE id = {}".format(availability, ctx.guild.id))
	await ctx.respond(f'Успешно выполнено. Состояние по умолчанию - **{availability}**')

@client.command(description="[Только Админы] Добавить ссылку на сторонний ресурс (ВК)")
@commands.has_permissions(administrator=True)
async def s_vk(ctx, 
	link: Option(str, description="Ссылка на сторонние ресурсы. (Для отключения напишите off)", required=True)):

	await ctx.defer()

	server_id = ctx.guild.id

	if cursor.execute("SELECT id FROM s_guild WHERE id = {}".format(server_id)).fetchone() is None:
		cursor.execute("""INSERT INTO s_guild VALUES ({}, 0, {}, {}, {}, {}, 'off', 'off', 'off', 'off')""".format(server_id, True, True, True, True))
		connection.commit()
	else:
		pass

	cursor.execute("UPDATE s_guild SET VK = '{}' WHERE id = '{}'".format(link, ctx.guild.id))
	connection.commit()

	await ctx.respond(f'Успешно выполнено. Ссылка на вк - {link}')

@client.command(description="[Только Админы] Добавить ссылку на сторонний ресурс (Ютуб)")
@commands.has_permissions(administrator=True)
async def s_yt(ctx, 
	link: Option(str, description="Ссылка на сторонние ресурсы. (Для отключения напишите off)", required=True)):

	await ctx.defer()

	server_id = ctx.guild.id

	if cursor.execute("SELECT id FROM s_guild WHERE id = {}".format(server_id)).fetchone() is None:
		cursor.execute("""INSERT INTO s_guild VALUES ({}, 0, {}, {}, {}, {}, 'off', 'off', 'off', 'off')""".format(server_id, True, True, True, True))
		connection.commit()
	else:
		pass

	cursor.execute("UPDATE s_guild SET YOUTUBE = '{}' WHERE id = '{}'".format(link, ctx.guild.id))
	connection.commit()

	await ctx.respond(f'Успешно выполнено. Ссылка на ютуб - {link}')

@client.command(description="[Только Админы] Добавить ссылку на сторонний ресурс (ТикТок)")
@commands.has_permissions(administrator=True)
async def s_tt(ctx, 
	link: Option(str, description="Ссылка на сторонние ресурсы. (Для отключения напишите off)", required=True)):

	await ctx.defer()

	server_id = ctx.guild.id

	if cursor.execute("SELECT id FROM s_guild WHERE id = {}".format(server_id)).fetchone() is None:
		cursor.execute("""INSERT INTO s_guild VALUES ({}, 0, {}, {}, {}, {}, 'off', 'off', 'off', 'off')""".format(server_id, True, True, True, True))
		connection.commit()
	else:
		pass

	cursor.execute("UPDATE s_guild SET TIKTOK = '{}' WHERE id = '{}'".format(link, ctx.guild.id))
	connection.commit()
	await ctx.respond(f'Успешно выполнено. Ссылка на ТикТок - {link}')

@client.command(description="[Только Админы] Добавить ссылку на сторонний ресурс (Твиттер)")
@commands.has_permissions(administrator=True)
async def s_tw(ctx, 
	link: Option(str, description="Ссылка на сторонние ресурсы. (Для отключения напишите off)", required=True)):

	await ctx.defer()

	server_id = ctx.guild.id

	if cursor.execute("SELECT id FROM s_guild WHERE id = {}".format(server_id)).fetchone() is None:
		cursor.execute("""INSERT INTO s_guild VALUES ({}, 0, {}, {}, {}, {}, 'off', 'off', 'off', 'off')""".format(server_id, True, True, True, True))
		connection.commit()
	else:
		pass

	cursor.execute("UPDATE s_guild SET TWITTER = '{}' WHERE id = '{}'".format(link, ctx.guild.id))
	connection.commit()
	await ctx.respond(f'Успешно выполнено. Ссылка на Твиттер - {link}')

#Основная часть
@client.command( pass_context = True, description="Информация по боту. (Создатель, версия, сервер поддержки)") #Полезная информация по боту
async def info( ctx ):
	user = client.get_user(472749232252649473)
	await ctx.respond(f"```**INFO** \nМой создатель: {user} \nV2.0 (Global Community) \nМой основной сервер: https://discord.gg/NrN5gSGp9f```")

@client.command(pass_context = True, description="Очистить чат, удалить N последних сообщений") #Очистить чат
@commands.has_permissions( administrator = True)
async def clear( ctx, 
	amount = Option(int, description="Число сообщений которые неоходимо удалить. По умолчанию 999999999999", default=999999999999)):
	await ctx.defer()
	await ctx.channel.purge(limit = amount)

@client.command(description="[A] Помощь админам.")
@commands.has_permissions( administrator = True)
async def admin_help(ctx):
	await ctx.defer()
	embed = discord.Embed(title = '**Админские команды**', description = 'ТОЛЬКО АДМИНАМ!!!')
	embed.add_field( name = prefix + 'start', value = 'кастом бота под сервер', inline = False)
	embed.add_field( name = prefix + 'givemoney/givexp', value = 'Выдать котику деняг или опыта', inline = False)
	embed.add_field( name = prefix + 'take/takerep', value = 'Изьять деньги, репутацию', inline = False)
	embed.add_field( name = prefix + 'giverep', value = 'Выдать респект кому-либо. Неограниченная власть', inline = False)
	embed.add_field( name = prefix + 'newrole @role цена', value = 'Добавить роль в магазин', inline = False)
	embed.add_field( name = prefix + 'updaterole @role цена', value = 'обновить роль в магазине', inline = False)
	embed.add_field( name = prefix + 'delrole @role', value = 'Удалить роль из ассортимента', inline = False)
	embed.add_field( name = prefix + 'clear', value = 'очистить чатик', inline = False)
	embed.add_field( name = prefix + 'admin_help', value = 'Открывает это меню с помощью админам', inline = False)

	await ctx.respond(embed = embed)

#help
@client.slash_command(description='Помощь пользователям.') #команда-помощь
async def help(ctx):
	await ctx.defer()
	s = cursor.execute("SELECT help FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:
		embed1 = discord.Embed(title = '**Оглавление**', description = ' ') #Оглавление
		embed1.add_field(name = 'Заработок денег', value = '__страница 2__', inline = False)
		embed1.add_field(name = 'Распоряжение деньгами', value = '__страница 3__', inline = False)
		embed1.add_field(name = 'Опыт', value = '__страница 4__', inline = False)
		embed1.add_field(name = 'Уровень', value = '__страница 5__', inline = False)
		embed1.add_field(name = 'Остальные команды', value = '__страница 6__', inline = False)
		embed1.add_field(name = 'Админские команды', value = prefix + 'admin_help', inline = False)

		embed2 = discord.Embed(title = '**Заработок денег**', description = 'Вы можете заработать деньги самыми разными способами')
		embed2.add_field(name = 'Общее', value = 'Вы получаете деньги за: подьём уровня, а также вы можете попросить деньги у кого-то или заработать', inline = False)
		embed2.add_field(name = 'Конкурсы', value = 'Помимо вышеперечисленных способов, админы могут выдавать деньги, например за победы в конкурсах', inline = False)	

		embed3 = discord.Embed(title = '**Распоряжение деньгами**', description = 'Куда можно потратить заработанные деньги') 
		embed3.add_field(name = prefix + 'shop', value = 'Открыть магазинчик, где можно посмотреть, на что потратить свои монетки на кастомные роли', inline = False)	
		embed3.add_field(name = prefix + 'buy "@роль"', value = 'Купить роль **из списка магазина, доступных для покупки**', inline = False)
		embed3.add_field(name = prefix + 'balance', value = 'Проверьте баланс. Неважно свой, или чужой', inline = False)
		embed3.add_field(name = prefix + 'lotery "сумма"', value = 'Сыграйте в лотерею с шансом на победу в 20 процентов!!!', inline = False)

		embed4 = discord.Embed(title = '**Опыт**', description = 'Что такое опыт, и как это заработать')
		embed4.add_field(name = 'Что такое опыт?', value = 'Опыт - это накапливаемые баллы, которые необходимы для поднятия уровня', inline = False)
		embed4.add_field(name = 'Как получать опыт?', value = 'Получать опыт можно практически за всё: от покупки роли, до выдачи респекта', inline = False)
		embed4.add_field(name = prefix + 'xp', value = 'Проверьте кол-во своего опыта, либо чужого', inline = False)

		embed5 = discord.Embed(title = '**Уровень**', description = 'Зачем нам этот ваш уровень?')
		embed5.add_field(name = 'Что такое уровень?', value = 'Уровень - это показатель вашей активности, изначально он равен 1', inline = False)
		embed5.add_field(name = 'Как его повысить?', value = 'Его можно повышать за опыт, каждый следующий уровень требует на 100 очков опыта больше, чем предыдущий (прокачка с 1 на 2 - 200 очков, с 2 на 3 - 300 очков)', inline = False)
		embed5.add_field(name = prefix + 'lvlup', value = 'Вы можете использовать эту команду для поднятия уровня, если опыта больше 1000', inline = False)

		embed6 = discord.Embed(title = '**Команды, доступные всем**', description = 'Оставшиеся команды')
		embed6.add_field( name = prefix + 'leaderboard', value = 'Топ 10 участников сервера по кол-ву денег', inline = False)
		embed6.add_field( name = prefix + 'profile', value = 'Посмотрите краткую статистику пользователя: Баланс, Уровень, Опыт, Репутацию', inline = False)
		embed6.add_field( name = prefix + 'prediction', value = 'Онлайн гадалка', inline = False)
		embed6.add_field( name = prefix + 'rep', value = 'Выдать респект кому-либо (максимум 3 раза в сутки)', inline = False)
		embed6.add_field( name = prefix + 'help', value = 'Краткий гайд по боту', inline = False)
		embed6.add_field( name = prefix + 'info', value = 'Интересная информация по боту', inline = False)

		embeds = [embed1, embed2, embed3, embed4, embed5, embed6]

		message = await ctx.send(embed = embed1)

		page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer = False, reactions = [PAW_L, PAW_R])
		await page.start()

	elif s == False:
		await ctx.send("Команда **help** отключена на этом сервере")

#finance
@client.command(description="Проверить баланс. (Чтобы проверить чужой баланс укажите пользователя через @)") #проверка баланса
async def balance(ctx, 
	member: Option(discord.Member, description="@Пользователь", default=None)):
	await ctx.defer()
	s = cursor.execute("SELECT finance FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:
		if member is None:
			await ctx.respond(embed = discord.Embed(
				description = f'''Баланс пользователя **{ctx.author}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} {COIN} **'''
				))

		else:
			await ctx.respond(embed = discord.Embed(
				description = f'''Баланс пользователя **{member}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} {COIN} **'''
				))

	elif s == False:
		await ctx.respond("Команда **balance** отключена на этом сервере")

@client.command(description="[A] Выдать деньги.")
@commands.has_permissions( administrator = True) #Выдать "премию"
async def givemoney(ctx, 
	member: Option(discord.Member, description="@Пользователь", required=True), 
	amount: Option(int, description="Сумма денег. (больше или равно 1)", required=True, min_value=1)):
	await ctx.defer()
	s = cursor.execute("SELECT finance FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:
		cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
		connection.commit()

		await ctx.respond('Успешно выполнено')

	elif s == False:
		await ctx.respond("Команда **givemoney** отключена на этом сервере")

@client.command(description="[A] Забрать деньги.") #Команда, которую используют гаишнки по отношению к деньгам водителей
@commands.has_permissions( administrator = True)
async def takemoney(ctx, 
	member: Option(discord.Member, description="@Пользователь"), 
	amount: Option(int, description="Сумма денег. (Больше или равно 1)", required=True, min_value=1)):
	await ctx.defer()
	s = cursor.execute("SELECT finance FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:
		cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
		connection.commit()

		await ctx.respond('Успешно выполнено')

	elif s == False:
		await ctx.respond("Команда **takemoney** отключена на этом сервере")

@client.command(description="[A] Добавить роль в магазин.") #Добавить роль в магазин
@commands.has_permissions( administrator = True)
async def newrole(ctx, 
	role: Option(discord.Role, description="@Роль", required=True), 
	cost: Option(int, description="Стоимость", required=True, min_value=1)):
	
	await ctx.defer()
	member = ctx.guild.get_member(901125980234592266)
	top_r = member.top_role
	bot_r = top_r.position
	role_p = role.position

	s = cursor.execute("SELECT finance FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

			if bot_r <= role_p:
				await ctx.respond("Данная роль не может быть размещена на продажу")
			else:			
				cursor.execute("INSERT INTO shop VALUES ({},{},{})".format(role.id, ctx.guild.id, cost))
				connection.commit()

				await ctx.respond('Успешно выполнено')

	elif s == False:
		await ctx.respond("Команда **newrole** отключена на этом сервере")

@client.command(description="[A] Обновить стоимость роли в магазине.")
@commands.has_permissions(administrator=True)
async def updaterole(ctx, 
	role: Option(discord.Role, description="@Роль", required=True), 
	cost: Option(int, description="Новая стоимость", required=True, min_value=0)):
	await ctx.defer()
	s = cursor.execute("SELECT finance FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:
		cursor.execute('UPDATE shop SET cost = {} WHERE role_id = {}'.format(cost, role.id))
		connection.commit()

		await ctx.respond('Успешно выполнено')

	elif s == False:
		await ctx.respond("Команда **updaterole** отключена на этом сервере")

@client.command(description="[A] Удалить роль из магазина.") #Удалить роль из магазина
@commands.has_permissions( administrator = True)
async def delrole(ctx, 
	role: Option(discord.Role, description="@Роль", required=True)):
	await ctx.defer()
	s = cursor.execute("SELECT finance FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:
		cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
		connection.commit()

	await ctx.respond('Успешно выполнено')

	if s == False:
		await ctx.respond("Команда **delrole** отключена на этом сервере")

@client.command(description="Магазин") #Посмотреть ассортимент пятёрочки
async def shop(ctx):
	await ctx.defer()
	s = cursor.execute("SELECT finance FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		embed = discord.Embed(title = 'Мой магазинчик')

		for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
			if ctx.guild.get_role(row[0]) != None:
				embed.add_field(
					name = f'Стоимость **{row[1]} {COIN}**',
					value = f'Роль {ctx.guild.get_role(row[0]).mention}',
					inline = False
					)
			else:
				pass

		await ctx.respond(embed = embed)

	elif s == False:
		await ctx.respond("Команда **shop** отключена на этом сервере")

@client.command(description="Купить роль в магазине.") #Купить хлебцы
async def buy(ctx, 
	role: Option(discord.Role, description="@Роль", required=True)):
	await ctx.defer()
	s = cursor.execute("SELECT finance FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		if role in ctx.author.roles:
			await ctx.respond(f'**{ctx.author}**, данная роль у вас уже имеется')

		elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor.execute('SELECT cash FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0]:
			await ctx.respond(f'У вас недостаточно {COIN}')

		else:
			await ctx.author.add_roles(role)
			cursor.execute('UPDATE users SET cash = cash - {0} WHERE id = {1}'.format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
			cursor.execute("UPDATE users SET exp = exp + {} WHERE id = {}".format(15, ctx.author.id))
			await ctx.respond('Успешно выполнено')

	elif s == False:
		await ctx.respond("Команда **buy** отключена на этом сервере")

@client.command(description="Лотерея") #Лохотрон
async def lotery(ctx, 
	amount: Option(int, description="Сумма поставленная на лотерею. (В случае победы вернётся в 2 раза больше)", required=True)):
	await ctx.defer()
	s = cursor.execute("SELECT finance FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		if int(amount) > cursor.execute('SELECT cash FROM users WHERE id = {}'.format(ctx.author.id)).fetchone()[0]:
			await ctx.send(f'У вас недостаточно {COIN}')

		else:
			randomizer = random.randint(1, 2)

			if randomizer == 1:
				await ctx.respond(f'**{ctx.author}**, вы победили :partying_face:')
				cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(int(amount), ctx.author.id))
				connection.commit()

			else:
				await ctx.respond(f'**{ctx.author}**, к сожалению вы проиграли :cry:')
				cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), ctx.author.id))
				connection.commit()

	elif s == False:
		await ctx.respond("Команда **lotery** отключена на этом сервере")

@client.command(description="Таблица лидеров")
async def leaderboard(ctx):
	await ctx.defer()
	s = cursor.execute("SELECT finance FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		embed = discord.Embed(title = "Топ 10 сервера")
		counter = 0

		for row in cursor.execute("SELECT name, cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 10".format(ctx.guild.id)):
			counter += 1

			embed.add_field(
				name = f'#{counter} | `{row[0]}`',
				value = f'Баланс: {row[1]}',
				inline = False
			)

		await ctx.respond(embed = embed)

	elif s == False:
		await ctx.respond("Команда **leaderboard** отключена на этом сервере")

@newrole.error
async def newrole_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send("Данная роль не существует или не может быть размещена на продажу")
 
@updaterole.error
async def updaterole_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send("Данная роль не существует или не может быть обновлена")	
 
@delrole.error
async def dekrole_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send("Данная роль и так не продаётся")

#prediction
@client.command(description="Предсказание. (1 в день)") #Гадалка
@commands.cooldown(1, 86400, commands.BucketType.user)  #
async def prediction(ctx):
	await ctx.defer()
	s = cursor.execute("SELECT prediction FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		randomizer = random.randint(1, 15)

		if randomizer == 1:
			await ctx.send(f'```"Стремитесь к успеху и выглядите так, словно вы его уже достигли."```')

		elif randomizer == 2:
			await ctx.send(f'```"Лучшее всегда является врагом хорошего."```')

		elif randomizer == 3:
			await ctx.send(f'```"Ничего не может быть смешнее, чем нравиться всем и каждому."```')

		elif randomizer == 4:
			await ctx.send(f'```"Чем мы наполняем наши молитвы, то нам и причитается."```')

		elif randomizer == 5:
			await ctx.send(f'```"Разница между победителем и побежденным только в том, что первый поднялся больше раз, чем упал."```')

		elif randomizer == 6:
			await ctx.send(f'```"Пока ты сам не сдашься, никто тебя не победит."```')

		elif randomizer == 7:
			await ctx.send(f'```"Любая борьба имеет смысл, если ты видишь цель."```')

		elif randomizer == 8:
			await ctx.send(f'```"Не забывай о главном!"```')

		elif randomizer == 9:
			await ctx.send(f'```"Не стоит рвать в герои, пока тебя туда не позвали."```')

		elif randomizer == 10:
			await ctx.send(f'``"Все, что происходит с нами, мы приводим в свою жизнь сами."```')

		elif randomizer == 11:
			await ctx.send(f'```"Тупиковых ситуаций не бывает – выход есть всегда."```')

		elif randomizer == 12:
			await ctx.send(f'```"Вот и пришел завтрашний день, который так беспокоил вас вчера."```')

		elif randomizer == 13:
			await ctx.send(f'```"У собак друзей больше, ведь они метут хвостами, а не языками."```')

		elif randomizer == 14:
			await ctx.send(f'```"Действуйте, даже если для этого нужен прыжок в неизвестность."```')

		elif randomizer == 15:
			await ctx.send(f'```"P.S. от автора: всё это бред)))"```')

	elif s == False:
		await ctx.send("Команда **prediction** отключена на этом сервере")

@prediction.error
async def prediction_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Притормози, эту команду можно использовать раз в 24 часа")

#profile
@client.command(description="Профиль пользователя")
async def profile(ctx, 
	member: Option(discord.Member, description="Пользователь, профиль которого вы хотите посмотреть. (Необязательно)")):
	await ctx.defer()
	s = cursor.execute("SELECT profile FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		if member is None:

			embed = discord.Embed(title = f'Профиль **{ctx.author}**')
			embed.add_field(name = f'Баланс пользователя', value = f'**{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} {COIN}**', inline = False) #balance
			embed.add_field(name = f'Уровень пользователя', value = f'**{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} {LVL}**', inline = False) #xp
			embed.add_field(name = f'Опыт пользователя', value = f'**{cursor.execute("SELECT exp FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} {EXP}**', inline = False) #lvl		
			embed.add_field(name = f'Репутация пользователя', value = f'**{cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} {REP}**', inline = False) #rep
			embed.set_thumbnail(url = ctx.author.avatar)

			await ctx.respond(embed = embed)

		else:
			embed = discord.Embed(title = f'Профиль **{member}**')
			embed.add_field(name = f'Баланс пользователя', value = f'**{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} {COIN}**', inline = False) #balance
			embed.add_field(name = f'Уровень пользователя', value = f'**{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]} {LVL}**', inline = False) #lvl
			embed.add_field(name = f'Опыт пользователя', value = f'**{cursor.execute("SELECT exp FROM users WHERE id = {}".format(member.id)).fetchone()[0]} {EXP}**', inline = False) #xp
			embed.add_field(name = f'Репутация пользователя', value = f'**{cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]} {REP}**', inline = False) #rep
			embed.set_thumbnail(url = member.avatar)


			await ctx.respond(embed = embed)

	elif s == False:
		await ctx.respond("Команда **profile** отключена на этом сервере")

@client.command(description="Посмотреть опыт") #проверка xp
async def xp(ctx, 
	member: Option(discord.Member, description="Пользователь(необязательно)")):
	await ctx.defer()
	s = cursor.execute("SELECT profile FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		if member is None:
			nxp = (f'{cursor.execute("SELECT exp FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}')
			clvl = int(cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0])
			rnum = int((clvl+1)*100)
			if  int(nxp) >= int(rnum):

				await ctx.respond(embed = discord.Embed(
					description = f'''**Опыт** пользователя **{ctx.author}** составляет **{cursor.execute("SELECT exp FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} {EXP}**. (Доступно поднятие уровня {LVL})'''
					))

			else:
				await ctx.respond(embed = discord.Embed(
					description = f'''**Опыт** пользователя **{ctx.author}** составляет **{cursor.execute("SELECT exp FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} {EXP}**.'''
					))


		else:
			xp_bal = (f'{cursor.execute("SELECT exp FROM users WHERE id = {}".format(member.id)).fetchone()[0]}')
			if  int(xp_bal) > int(needxp):

				await ctx.respond(embed = discord.Embed(
					description = f'''**Опыт** пользователя **{member}** составляет **{cursor.execute("SELECT exp FROM users WHERE id = {}".format(member.id)).fetchone()[0]} {EXP}**. (Доступно поднятие уровня {LVL})'''
					))

			else:
				await ctx.respond(embed = discord.Embed(
					description = f'''**Опыт** пользователя **{member}** составляет **{cursor.execute("SELECT exp FROM users WHERE id = {}".format(member.id)).fetchone()[0]} {EXP}**.'''
					))

	elif s == False:
		await ctx.respond("Команда **xp** отключена на этом сервере")

@client.command(description="[A] Выдать опыт.")
@commands.has_permissions( administrator = True) #Выдать "премию" xp
async def givexp(ctx, 
	member: Option(discord.Member, description="@Пользователь", required=True), 
	amount: Option(int, description="Кол-во", required=True, min_value=1)):
	await ctx.defer()
	s = cursor.execute("SELECT profile FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:
		cursor.execute("UPDATE users SET exp = exp + {} WHERE id = {}".format(amount, member.id))
		connection.commit()

		await ctx.respond('Успешно выполнено')

	elif s == False:
		await ctx.respond("Команда **givexp** отключена на этом сервере")

@client.command(description="Проверка уровня") #проверка lvl
async def lvl(ctx, 
	member: Option(discord.Member, description="Пользователь (необязательно)")):
	await ctx.defer()
	s = cursor.execute("SELECT profile FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		if member is None:
			await ctx.respond(embed = discord.Embed(
				description = f'''**Уровень** пользователя **{ctx.author}** составляет **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} {LVL}**.'''
				))

		else:
			await ctx.respond(embed = discord.Embed(
				description = f'''**Уровень** пользователя **{member}** составляет **{cursor.execute("SELECT lvl FROM users WHERE id = {}".format(member.id)).fetchone()[0]} {LVL}**.'''
				))

	elif s == False:
		await ctx.respond("Команда **lvl** отключена на этом сервере")

@client.command(description="Поднять уровень") #Поднять лвл
async def lvlup(ctx):

	s = cursor.execute("SELECT profile FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		nxp = (f'{cursor.execute("SELECT exp FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]}')
		clvl = int(cursor.execute("SELECT lvl FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0])
		rnum = int((clvl+1)*100)

		if  int(nxp) < int(rnum):
			await ctx.respond(f'**{ctx.author}**, у вас не хватает опыта')

		else:

			cursor.execute('UPDATE users SET exp = exp - {} WHERE id = {}'.format(rnum, ctx.author.id))
			cursor.execute('UPDATE users SET lvl = lvl + 1 WHERE id = {}'.format(ctx.author.id))
			cursor.execute('UPDATE users SET cash = cash + 1000 WHERE id = {}'.format(ctx.author.id))

			connection.commit()

			await ctx.message.add_reaction('✅')

	elif s == False:
		await ctx.respond("Команда **lvlup** отключена на этом сервере")

@client.command(description="Поднять репутацию (Макс. 3 раза в день)") #Респектануть
@commands.cooldown(3, 86400, commands.BucketType.user) 
async def rep(ctx, 
	member: Option(discord.Member, description="Пользователь", required=True)):
	await ctx.defer()
	s = cursor.execute("SELECT profile FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		if member is None:
			await ctx.respond(f"**{ctx.author}**, вы забыли указать участника сервера")

		else:
			if member.id == ctx.author.id:
				await ctx.respond(f"**{ctx.author}**, вы не можете выдать репутацию себе")

			else:
				cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(1, member.id))
				cursor.execute("UPDATE users SET exp = exp + {} WHERE id = {}".format(25, ctx.author.id))
				connection.commit()		

				await ctx.message.add_reaction('✅')

	elif s == False:
		await ctx.respond("Команда **rep** отключена на этом сервере")			

@client.command(description="[A] Выдать огромное количество репутации.") #Респектануть
@commands.has_permissions(administrator = True)
async def giverep(ctx, 
	member: Option(discord.Member, description="Пользователь", required=True), 
	amount: Option(int, description="Пользователь", required=True, min_value=1)):
	await ctx.defer()
	s = cursor.execute("SELECT profile FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(amount, member.id))
		connection.commit()		

		await ctx.respond('Успешно выполнено')

	elif s == False:
		await ctx.respond("Команда **giverep** отключена на этом сервере")	

@client.command(description="[A] Забрать неограниченное количество репутации.") #xДизРеспектануть
@commands.has_permissions( administrator = True)
async def takerep(ctx, 
	member: Option(discord.Member, description="Пользователь", required=True), 
	amount: Option(int, description="Кол-во", required=True, min_value=1)):
	await ctx.defer()
	s = cursor.execute("SELECT profile FROM s_guild WHERE id = {}".format(ctx.guild.id)).fetchone()[0]
	if s == True:

		nrep = ("SELECT rep FROM users WHERE id = {}".format(ctx.author.id))

		if nrep<amount:
			await ctx.respond(f"У пользователя нет такого количества репутации {REP}")
		else:
			cursor.execute("UPDATE users SET rep = rep - {} WHERE id = {}".format(amount, member.id))
			connection.commit()		

			await ctx.respond("Успешно выполнено")

	elif s == False:
		await ctx.respond("Команда **takerep** отключена на этом сервере")

@rep.error
async def rep_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Я понимаю, вокруг так много крутых бро которым хочется кинуть респект, но ты можешь выдавать респект только 3 раза за сутки.")

@client.command(description="[A] Выдать предупреждение.")
@commands.has_permissions(administrator=True)
async def pred(ctx,
	member: Option(discord.Member, description="Нарушитель", required=True),
	time: Option(int, description="Время на исправление (в минутах)", required=True),
	reason: Option(str, description="Нарушение", required=True)):
	await ctx.defer()
	guild = ctx.guild.name
	await member.send(f"Вам выдано предупреждение на сервере **{guild}** по причине {reason}. У вас есть {time} минут на исправление.")
	await ctx.send(f"{member}, вам выдано предупреждение по причине '{reason}'. У вас есть {time} минут на исправление.")
	await ctx.respond("Успешно выполнено")

#Подключение
client.run(TOKEN)