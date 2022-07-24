import lightbulb as lb
import hikari

client = lb.BotApp(
    token = 'MTAwMDU0NDEyODYwMzU0MTYxNg.GF4ldd.BUAnO5bZwUw2s1kL3Q0tSQlZvO6V7Oq1_yxQ-s',
    default_enabled_guilds=())

@client.listen(hikari.StartedEvent)
async def on_started(event) :
    print('bot online!')

@client.command
@lb.command('ping', 'says pong!') # name, desc
@lb.implements(lb.SlashCommand)
async def ping(ctx) :
    await ctx.respond('pong!')

@client.command
@lb.command('group', 'this is a group') # name, desc
@lb.implements(lb.SlashCommand)
async def group (ctx) :
    pass

@group.child
@lb.command('group', 'this is a group') # name, desc
@lb.implements(lb.SlashSubCommand)
async def subcommand(ctx) :
    await ctx.respond('hi im a')










client.run()