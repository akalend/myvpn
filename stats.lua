local stat_dict = ngx.shared.stat
local status = tonumber(ngx.status) --ответ сервера
local consume = tonumber(ngx.var.upstream_response_time)  --количество секунд которые были потрачены в обработке запросов 
local bandwidth = tonumber(ngx.var.bytes_sent)  --количество байт отправленных  с сервера


local function incr(dict, key, increment)
    increment = increment or 1
    local newval, err = dict:incr(key, increment)
    if not newval or err then
      dict:add(key, increment)
      newval = increment
    end
end

local function get_status_code_class(code)
  local  status_code = tostring(code)
  if     status_code:sub(1,1) == '1' then return '1xx'
  elseif status_code:sub(1,1) == '2' then return '2xx'
  elseif status_code:sub(1,1) == '3' then return '3xx'
  elseif status_code:sub(1,1) == '4' then return '4xx'
  else                                    return 'xxx'
  end
end
------------------------------------------------------------------------------------------


if not consume then --may be nil
  consume = 0
end

-- stat_dict['last_time'] = os.time()
-- incr(stat_dict, 'last_request')
incr(stat_dict, 'total.consume', consume)
incr(stat_dict, 'total.requests')
incr(stat_dict, 'total.bandwidth', bandwidth)
if (status >= 500) and (status < 600) then
  incr(stat_dict, 'total.errors.' .. tostring(status))
else
  incr(stat_dict, 'total.codes.' .. get_status_code_class(status))
end
