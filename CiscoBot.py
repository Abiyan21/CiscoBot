from ast import Continue
from discord.ext import commands, tasks
import discord
import random
import asyncio
from netmiko import ConnectHandler
import serial.tools.list_ports

ciscoserial = {
    'device_type': 'cisco_ios_serial',
    'serial_settings': {'port': '/dev/cu.usbserial-AO001TXM'},
    'username': 'admin',
    'password': 'cisco',
    'secret': 'Donald4ever$'
}

cisco_SSH = {
    'device_type': 'cisco_ios',
    'host':   '192.168.10.26',
    'username': 'admin',
    'password': 'cisco',
    'port' : 22,          # optional, defaults to 22
    'secret': 'cisco',     # optional, defaults to ''
}
# Verbindungsaufbau
print ("start Verbindung")
net_connect = ConnectHandler(**cisco_SSH)

TOKEN = 'Eigenen Token hinzufügen'

description = '''Die folgende Commands sind ausführbar!'''
bot = commands.Bot(command_prefix='?', description=description)
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    channel = bot.get_channel(919858502921519166)


@bot.command()
async def shutport(ctx, port : str):
    """Gib ein welcher Port du ausschalten willst"""
    turnoffcmd = [f'interface fastEthernet 0/' + port, "shutdown"]
    net_connect.enable()
    net_connect.send_config_set(turnoffcmd)
    output = net_connect.send_command('show interface status')
    await ctx.send(output)

@bot.command()
async def enableport(ctx, port : str):
    """Gib ein welcher Port du anschalten willst"""
    turnoncmd = [f'interface fastEthernet 0/' + port, "no shutdown"]
    net_connect.enable()
    net_connect.send_config_set(turnoncmd)
    output = net_connect.send_command('show interface status')
    await ctx.send(output)

@bot.command()
async def shutallport(ctx):
    """Schaltet alle ports aus"""
    PortList = net_connect.send_command('show interface status')
    ports = PortList.splitlines()
    for port in ports:
        if port.split()[0] == "Port" or "Gi" in port.split()[0]:
            Continue
        else:
            offlist = [f'interface ' + port.split()[0], "shutdown"]
            net_connect.enable
            net_connect.send_config_set(offlist)
            #await ctx.send(port.split()[0])
    await ctx.send(net_connect.send_command('show interface status'))

@bot.command()
async def enableallport(ctx):
    """Schaltet alle Ports an"""
    PortList = net_connect.send_command('show interface status')
    ports = PortList.splitlines()
    for port in ports:
        if port.split()[0] == "Port" or "Gi" in port.split()[0]:
            Continue
        else:
            onlist = [f'interface ' + port.split()[0], "no shutdown"]
            net_connect.enable      
            net_connect.send_config_set(onlist)
            #await ctx.send(port.split()[0])
    await ctx.send(net_connect.send_command('show interface status'))

@bot.command()
async def status(ctx):
    """Gibt den Status von alle Ports aus"""
    await ctx.send(net_connect.send_command("show interface status"))

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
         """Schaltet den Bot aus (NUR OWNER!!!)"""
         await ctx.send('Tschüss!!')
         await bot.close()
         print("Goodbye")

bot.run(TOKEN)