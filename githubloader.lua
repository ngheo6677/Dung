-- Tải script từ GitHub (tự động thêm ?v để tránh cache)
local url = "https://raw.githubusercontent.com/ngheo6677/Dung/refs/heads/main/framboss.txt?v=" .. math.random(100000,999999)

-- Hàm giải mã Base64
local function decodeBase64(data)
	local b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
	data = data:gsub('[^'..b..'=]', '')
	return (data:gsub('.', function(x)
		if x == '=' then return '' end
		local r, f = '', (b:find(x) - 1)
		for i = 6, 1, -1 do
			r = r .. (f % 2^i - f % 2^(i - 1) > 0 and '1' or '0')
		end
		return r
	end):gsub('%d%d%d?%d?%d?%d?%d?%d?', function(x)
		if #x ~= 8 then return '' end
		local c = 0
		for i = 1, 8 do
			c = c + (x:sub(i, i) == '1' and 2^(8 - i) or 0)
		end
		return string.char(c)
	end))
end

-- Kiểm tra có phải base64 không
local function isLikelyBase64(str)
	return #str > 16 and str:match("^[A-Za-z0-9+/=\n\r]+$") ~= nil
end

-- Tải nội dung từ URL
local success, response = pcall(function()
	return game:HttpGet(url)
end)

if not success then
	warn("[LOADER][ERROR] Không thể tải script:", response)
	return
end

-- Giải mã nếu cần và chạy
local function runScript(raw)
	local decoded = isLikelyBase64(raw) and decodeBase64(raw) or raw
	local func, err = loadstring(decoded)
	if func then
		func()
	else
		warn("[LOADER][ERROR] Script lỗi:", err)
	end
end

runScript(response)
