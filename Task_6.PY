import time
import threading

class TradingBot:
    def __init__(self, symbol, entry_time, price):
        self.symbol = symbol
        self.entry_time = entry_time
        self.price = price
        
        #ENTRY TIME VALIDATION
        if self.entry_time < time.time():
            raise ValueError("Entry time cannot be in the past.")
        
        self.order_placed = False

    def place_order(self):
        current_time = time.time()
        if current_time > self.entry_time and not self.order_placed:
            self.order_placed = True
            print(f"Order placed for {self.symbol} at {time.ctime(current_time)} for ${self.price}")
        elif current_time > self.entry_time and self.order_placed:
            print(f"Order for {self.symbol} already placed.")
        else:
            print(f"Waiting to place order for {self.symbol} at {time.ctime(self.entry_time)}...")






# INSTANCES OF TRADINGBOT
bot1 = TradingBot("RELIANCE", time.time() + 5, 2222.30)
bot2 = TradingBot("M&M", time.time() + 10, 1105)
bot3 = TradingBot("HDFC", time.time() + 15, 2800.5)
bot4 = TradingBot("TATACHEM", time.time() + 20, 3500)
bot5 = TradingBot("HDFCBANK", time.time() + 25, 2500)






#START RUNING EACH THREAD BOT FOR EACH BOT
threads = []
for bot in [bot1, bot2, bot3, bot4, bot5]:
    thread = threading.Thread(target=bot.place_order)
    thread.start()
    threads.append(thread)






# KEEP  RUNNING LOOP TILL ALL ORDERS ARE PLACED
while not all(bot.order_placed for bot in [bot1, bot2, bot3, bot4, bot5]):
    for bot in [bot1, bot2, bot3, bot4, bot5]:
        if not bot.order_placed:
            bot.place_order()
    time.sleep(5)



    
# FINALLY STOPPING THREADS
for thread in threads:
    thread.join()

print('ALL ORDERS ARE PLACED')