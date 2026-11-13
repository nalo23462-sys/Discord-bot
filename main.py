import discord
from discord.ext import commands, tasks
import random
import os
from flask import Flask
from threading import Thread

# 1. Cấu hình Bot Discord
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Thay ID phòng thoại (Voice Channel ID) và ID kênh chat (Text Channel ID) của bạn vào đây
VOICE_CHANNEL_ID = 123456789012345678 
TEXT_CHANNEL_ID = 123456789012345678

DANH_SACH_NGON = [
    "Hôm nay trời đẹp thế nhờ, chúc mọi người một ngày tốt lành!",
    "Sông sâu tĩnh lặng, lúa chín cúi đầu. Sống ở đời cứ bình tĩnh mà sống.",
    "Cố gắng không phải vì ai khác, mà vì phiên bản tốt hơn của chính mình."
]

@bot.event
async def on_ready():
    print(f"Bot đã online với tên: {bot.user}")
    
    # Tự động vào phòng thoại khi khởi động
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        await channel.connect()
        print(f"Đã tham gia và đang treo tại phòng: {channel.name}")
    else:
        print("Không tìm thấy phòng thoại! Hãy kiểm tra lại ID phòng.")
        
    if not gui_ngon_dinh_ky.is_running():
        gui_ngon_dinh_ky.start()

@tasks.loop(minutes=60)
async def gui_ngon_dinh_ky():
    channel = bot.get_channel(TEXT_CHANNEL_ID)
    if channel:
        cau_noi = random.choice(DANH_SACH_NGON)
        await channel.send(cau_noi)

# Lệnh gọi châm ngôn
@bot.command()
async def ngon(ctx):
    cau_noi = random.choice(DANH_SACH_NGON)
    await ctx.send(f"{ctx.author.mention} {cau_noi}")

# Lệnh gọi bot vào phòng voice
@bot.command()
async def treo(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"Đã vào treo phòng **{channel.name}**!")
    else:
        await ctx.send("Bạn cần phải vào một phòng thoại trước đã!")

# Lệnh cho bot rời phòng voice
@bot.command()
async def roi(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Đã rời khỏi phòng thoại!")
    else:
        await ctx.send("Bot hiện không ở trong phòng thoại nào.")

# --- TÍNH NĂNG PHÁT NHẠC / ÂM THANH (XẢ NHẠC) ---
@bot.command()
async def phat(ctx, url_nhac: str = None):
    """Lệnh phát nhạc cơ bản từ link âm thanh trực tuyến"""
    if not ctx.author.voice:
        await ctx.send("Bạn phải vào phòng thoại trước mới xả nhạc được chứ!")
        return

    channel = ctx.author.voice.channel
    
    # Đưa bot vào phòng nếu chưa vào
    if not ctx.voice_client:
        voice_client = await channel.connect()
    else:
        voice_client = ctx.voice_client
        await voice_client.move_to(channel)

    if not url_nhac:
        await ctx.send("Hãy gửi kèm đường dẫn âm thanh (link file mp3 trực tiếp) nhé! Ví dụ: `!phat <link_nhạc>`")
        return

    try:
        # Dùng FFmpeg để phát nguồn nhạc trực tuyến
        source = discord.FFmpegPCMAudio(url_nhac)
        if voice_client.is_playing():
            voice_client.stop()
            
        voice_client.play(source, after=lambda e: print(f'Lỗi phát nhạc: {e}' if e else 'Phát nhạc xong'))
        await ctx.send("Đang xả nhạc cực căng cho anh em thưởng thức đây! 🎶")
    except Exception as e:
        await ctx.send(f"Không thể phát được link này. Hãy đảm bảo đó là link file âm thanh trực tiếp (định dạng .mp3 hoặc luồng phát trực tiếp). Lỗi: {e}")

@bot.command()
async def dừng(ctx):
    """Lệnh dừng nhạc đang phát"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Đã dừng nhạc!")
    else:
        await ctx.send("Bot có đang phát bài nào đâu!")

# 2. Tạo Web Server giả lập bằng Flask (Giúp bot duy trì 24/7 trên Render)
app = Flask('')

@app.route('/')
def home():
    return "Bot Discord đang hoạt động!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 3. Chạy Server và Bot
if __name__ == "__main__":
    keep_alive()
    # Thay 'TOKEN_BOT_CUA_BAN' bằng Token thật của bot Discord
    bot.run("TOKEN_BOT_CUA_BAN")
