            local filename = "/home/akalend/projects/myvpn/site/index.htm"
            local file = io.open(filename, "r")
            io.input(file)

            local linesx = ' '
            for line in io.readln(file) do 
               -- line = line:gsub("{id}", id) 
               linesx  =  linesx .. line 
            end


                f = io.popen ("ls -l")
  
                for line in f:lines() do
                    ngx.say(line)
                end 
               
             f:close()



                 for key, val in pairs(args) do
                     if type(val) == "table" then
                         ngx.say(key, ": ", table.concat(val, ", "))
                     else
                         ngx.say(key, ": ", val)
                     end
                 end



                 ngx.req.read_body()
                 local args, err = ngx.req.get_post_args()

                if err == "truncated" then
                    -- one can choose to ignore or reject the current request here
                   ngx.say("error")
                end


                if not args then
                    ngx.say("failed to get post args: ", err)
                    return
                end

                local id = args["id"]
                if not id then
                     ngx.say("failed to get post args: ")
                     return
                end
                ngx.say("id= ", id)

                f = io.popen ("/usr/bin/python /home/akalend/projects/myvpn/master.py > /home/akalend/projects/myvpn/log/app." .. id .. ".log"  )

                for line in f:lines() do
                    ngx.say(line)
                end 
                ngx.say("ok")
                   
                 f:close()
