import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd
from config import DARK_RED

class Plot:
    def __init__(self):
        pass
    
    def plot(self, y_data, num_years=5, title=None, xlabel="x-axis", ylabel="y-axis", color1="tab:red", linewidth=3.0, label="None", name='fig'):
        
        start_date = datetime.now() - timedelta(days=len(y_data))
        date_range = pd.date_range(start=start_date, end=datetime.now(), freq='D')[:-1]
        # print(len(date_range), len(y_data))
    
        data = pd.DataFrame({'Date': date_range, 'Y_Data': y_data})        
        
        plt.plot(data['Date'], data['Y_Data'], color=color1, linewidth=linewidth, label=label)

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(title)
        plt.xlabel(xlabel)  
        plt.xticks(rotation=30)
        plt.ylabel(ylabel)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.8), fancybox=True, shadow=True, ncol=1, frameon=False)
        # plt.gca().set_aspect(1.2)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))
        plt.tight_layout()
        plt.savefig(f'{name}.png', bbox_inches='tight')
        # plt.show()
    
    def reset_plot(self):
        plt.clf()
        plt.cla()
        plt.close()
        

        
        


x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
y = [2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10]

# p = Plot()
# p.plot(x,y, title="Test", xlabel="X", ylabel="Y", color1=DARK_RED)