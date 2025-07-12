from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
from discord import app_commands
import random, json, os, datetime

# ====== FLASK GIỮ SỐNG ======
app = Flask('')
@app.route('/')
def home():
    return "Bot vẫn sống!"
def run():
    app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# ====== CẤU HÌNH ======
TOKEN = "MTM5MzA2MTQwMDI4MDE3MDU0Nw.Gdj3l6.p9pNvH2FH0Kj6U-G4oewkIoLjh8RhI2xD_Gheg"
KÊNH_HỢP_LỆ = "keyshop"
GIÁ_KEY = 100000
ĐIỂM_HÀNG_NGÀY = 500
DỮ_LIỆU_FILE = "users.json"
KEY_FILE = "keys.txt"

# ====== KHỞI TẠO BOT ======
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot đã hoạt động: {client.user}")
    try:
        synced = await client.tree.sync()
        print(f"🔧 Đã sync {len(synced)} lệnh slash.")
    except Exception as e:
        print(f"❌ Lỗi khi sync lệnh: {e}")

# ====== XỬ LÝ ĐIỂM ======
def đọc_dữ_liệu():
    if not os.path.exists(DỮ_LIỆU_FILE):
        return {}
    with open(DỮ_LIỆU_FILE, "r") as f:
        return json.load(f)

def ghi_dữ_liệu(data):
    with open(DỮ_LIỆU_FILE, "w") as f:
        json.dump(data, f, indent=4)

def xem_điểm(user_id):
    data = đọc_dữ_liệu()
    u = str(user_id)
    return data.get(u, {}).get("balance", 0)

def cộng_điểm(user_id, amount):
    data = đọc_dữ_liệu()
    u = str(user_id)
    user = data.get(u, {})
    user["balance"] = user.get("balance", 0) + amount
    data[u] = user
    ghi_dữ_liệu(data)

def trừ_điểm(user_id, amount):
    cộng_điểm(user_id, -amount)

def đặt_điểm(user_id, amount):
    data = đọc_dữ_liệu()
    u = str(user_id)
    user = data.get(u, {})
    user["balance"] = amount
    data[u] = user
    ghi_dữ_liệu(data)

# ====== KEY ======
def đọc_key_chưa_dùng():
    if not os.path.exists(KEY_FILE):
        return []
    with open(KEY_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def xoá_key_đã_dùng(key):
    keys = đọc_key_chưa_dùng()
    if key in keys:
        keys.remove(key)
        with open(KEY_FILE, "w") as f:
            for k in keys:
                f.write(k + "\n")

def chỉ_kênh_hợp_lệ(interaction):
    return interaction.channel.name == KÊNH_HỢP_LỆ

# ====== SLASH COMMAND ======
@client.tree.command(name="daily")
async def daily(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = đọc_dữ_liệu()
    now = datetime.datetime.utcnow()
    user = data.get(user_id, {})
    last = user.get("last_daily")
    if last:
        try:
            last_time = datetime.datetime.fromisoformat(last)
            if (now - last_time).total_seconds() < 86400:
                await interaction.response.send_message("⛔ Bạn đã nhận điểm hôm nay rồi.", ephemeral=True)
                return
        except:
            pass
    user["balance"] = user.get("balance", 0) + ĐIỂM_HÀNG_NGÀY
    user["last_daily"] = now.isoformat()
    data[user_id] = user
    ghi_dữ_liệu(data)
    await interaction.response.send_message(f"✅ Nhận {ĐIỂM_HÀNG_NGÀY} điểm!", ephemeral=True)

@client.tree.command(name="bal")
async def bal(interaction: discord.Interaction):
    bal = xem_điểm(interaction.user.id)
    await interaction.response.send_message(f"💰 Bạn có {bal} điểm.", ephemeral=True)

@client.tree.command(name="shop")
async def shop(interaction: discord.Interaction):
    if not chỉ_kênh_hợp_lệ(interaction):
        await interaction.response.send_message("⛔ Dùng trong #keyshop", ephemeral=True)
        return
    keys = đọc_key_chưa_dùng()
    if keys:
        await interaction.response.send_message(f"🛒 Shop có {len(keys)} key. Dùng /buy để mua!", ephemeral=True)
    else:
        await interaction.response.send_message("🚫 Shop đã hết key!", ephemeral=True)

@client.tree.command(name="buy")
async def buy(interaction: discord.Interaction):
    if not chỉ_kênh_hợp_lệ(interaction):
        await interaction.response.send_message("⛔ Dùng trong #keyshop", ephemeral=True)
        return
    uid = interaction.user.id
    bal = xem_điểm(uid)
    if bal < GIÁ_KEY:
        await interaction.response.send_message("❌ Không đủ điểm để mua key!", ephemeral=True)
        return
    keys = đọc_key_chưa_dùng()
    if not keys:
        await interaction.response.send_message("🚫 Shop hết key!", ephemeral=True)
        return
    key = keys[0]
    trừ_điểm(uid, GIÁ_KEY)
    xoá_key_đã_dùng(key)
    await interaction.user.send(f"🔑 Key của bạn: `{key}`")
    await interaction.response.send_message("✅ Đã gửi key qua DM!", ephemeral=True)

@client.tree.command(name="setpoint")
@app_commands.describe(user="Người nhận", amount="Số điểm")
async def setpoint(interaction: discord.Interaction, user: discord.User, amount: int):
    if interaction.user.id != interaction.guild.owner_id:
        await interaction.response.send_message("⛔ Lệnh này chỉ chủ server được dùng.", ephemeral=True)
        return
    đặt_điểm(user.id, amount)
    await interaction.response.send_message(f"✅ Đã đặt {amount} điểm cho {user.name}.", ephemeral=True)

@client.tree.command(name="top")
async def top(interaction: discord.Interaction):
    data = đọc_dữ_liệu()
    sorted_users = sorted(data.items(), key=lambda x: x[1].get("balance", 0), reverse=True)
    msg = "**🏆 Top người có nhiều điểm:**\n"
    for i, (uid, info) in enumerate(sorted_users[:10]):
        user = await client.fetch_user(int(uid))
        msg += f"{i+1}. {user.name}: {info.get('balance', 0)} điểm\n"
    await interaction.response.send_message(msg, ephemeral=True)

@client.tree.command(name="taixiu")
@app_commands.describe(cuoc="Điểm cược", chon="Chọn tài hoặc xỉu")
async def taixiu(interaction: discord.Interaction, cuoc: int, chon: str):
    if chon.lower() not in ["tài", "xỉu"]:
        await interaction.response.send_message("❌ Chỉ được chọn tài hoặc xỉu", ephemeral=True)
        return
    bal = xem_điểm(interaction.user.id)
    if cuoc > bal:
        await interaction.response.send_message("❌ Không đủ điểm để cược!", ephemeral=True)
        return
    tong = sum(random.randint(1, 6) for _ in range(3))
    kq = "tài" if tong >= 11 else "xỉu"
    if chon == kq:
        cộng_điểm(interaction.user.id, cuoc)
        msg = f"🎲 Tổng {tong} là **{kq.upper()}** — bạn thắng {cuoc} điểm!"
    else:
        trừ_điểm(interaction.user.id, cuoc)
        msg = f"🎲 Tổng {tong} là **{kq.upper()}** — bạn thua {cuoc} điểm!"
    await interaction.response.send_message(msg, ephemeral=True)

@client.tree.command(name="doanso")
async def doanso(interaction: discord.Interaction, so: int):
    if so < 1 or so > 10:
        await interaction.response.send_message("❌ Chỉ đoán số từ 1 đến 10!", ephemeral=True)
        return
    ran = random.randint(1, 10)
    if so == ran:
        cộng_điểm(interaction.user.id, 1000)
        await interaction.response.send_message("🎯 Chính xác! Bạn nhận 1000 điểm!", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ Sai! Số đúng là {ran}", ephemeral=True)

@client.tree.command(name="coinflip")
async def coinflip(interaction: discord.Interaction, chọn: str):
    if chọn.lower() not in ["ngửa", "sấp"]:
        await interaction.response.send_message("❌ Chỉ được chọn ngửa hoặc sấp", ephemeral=True)
        return
    kq = random.choice(["ngửa", "sấp"])
    if chọn == kq:
        cộng_điểm(interaction.user.id, 500)
        await interaction.response.send_message(f"🪙 Kết quả: {kq.upper()} — bạn thắng 500 điểm!", ephemeral=True)
    else:
        trừ_điểm(interaction.user.id, 500)
        await interaction.response.send_message(f"🪙 Kết quả: {kq.upper()} — bạn thua 500 điểm!", ephemeral=True)

client.run(TOKEN)
