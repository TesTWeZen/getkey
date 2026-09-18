local SECRET = "IRISH_HUB_2024_X9K2"
local CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
local charsetLen = #CHARSET

local charsetPos = {}
for i = 1, charsetLen do
	charsetPos[string.sub(CHARSET, i, i)] = i - 1
end

local function crc32Compute(str)
	local crc = 4294967295 -- 0xFFFFFFFF using math only
	for i = 1, #str do
		local byte = string.byte(str, i)
		crc = bit32.bxor(crc, byte)
		for _ = 1, 8 do
			if bit32.band(crc, 1) == 1 then
				crc = bit32.bxor(bit32.rshift(crc, 1), 3735928559) -- 0xEDB88320
			else
				crc = bit32.rshift(crc, 1)
			end
		end
	end
	return bit32.bxor(crc, 4294967295) -- 0xFFFFFFFF
end

local function makeChecksum(payload)
	local h = crc32Compute(SECRET .. payload)
	local s = ""
	for _ = 1, 4 do
		local idx = h % charsetLen
		s = string.sub(CHARSET, idx + 1, idx + 1) .. s
		h = math.floor(h / charsetLen)
	end
	return s
end

local function irishValidateKey(key)
	if type(key) ~= "string" then return false end
	if #key ~= 20 then return false end
	if string.sub(key, 1, 6) ~= "IRISH-" then return false end

	local parts = {}
	for p in string.gmatch(key, "[^-]+") do
		table.insert(parts, p)
	end
	if #parts ~= 4 then return false end

	for i = 1, 4 do
		if #parts[i] ~= (i == 1 and 5 or 4) then return false end
		local checkStr = (i == 1 and string.sub(parts[i], 2) or parts[i])
		for j = 1, #checkStr do
			local c = string.sub(checkStr, j, j)
			if not charsetPos[c] and charsetPos[c] ~= 0 then
				return false
			end
		end
	end

	local payload = parts[2] .. parts[3]
	local expected = makeChecksum(payload)
	return parts[4] == expected
end

return irishValidateKey
