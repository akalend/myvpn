local stat_dict = ngx.shared.stat

ngx.say("-------- 0 --------")
local keys = stat_dict:get_keys(0)
for _, key in pairs(keys) do
    ngx.say( key .. ":" .. stat_dict:get(key))
end

local last_request = stat_dict["last_request"]
last_request = last_request or 0
ngx.say( "last_request:" .. tostring(last_request) )

local total = stat_dict:get("total.requests")
total = total or 0
ngx.say( "total request:" .. tostring(total) )

local tm = os.time()
local ts = stat_dict["last_time"]
ts = ts or tm

ngx.shared.stat["last_request"] = total
ngx.shared.stat["last_time"] = tm
ngx.say( "last_time:" .. tostring(ts) )
ngx.say( "time:" .. tostring(tm - ts) )
ngx.say( "delta request:" .. tostring( total - last_request )) 
ngx.say( "rps:" .. string.format("%2.2f", (total - last_request) /(tm - ts) )) 
