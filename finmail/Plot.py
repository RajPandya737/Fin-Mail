import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
from config import DARK_RED

class Plot:
    def __init__(self):
        pass
    
    def plot(self, y_data, num_years=5, title=None, xlabel="x-axis", ylabel="y-axis", color1="tab:red", linewidth=3.0, label="None"):
        
        start_date = datetime.now() - timedelta(days=len(y_data))
        date_range = pd.date_range(start=start_date, end=datetime.now(), freq='D')[:-1]
        # print(len(date_range), len(y_data))
    
        data = pd.DataFrame({'Date': date_range, 'Y_Data': y_data})        
        
        plt.plot(data['Date'], data['Y_Data'], color=color1, linewidth=linewidth, label=label)

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(title)
        plt.xlabel(xlabel)  # Corrected line
        plt.ylabel(ylabel)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), fancybox=True, shadow=True, ncol=1, frameon=False)
        plt.gca().set_aspect(0.8)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.tight_layout()
        plt.savefig('fig.png', bbox_inches='tight')
        plt.show()
    
        

        
        


x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
y = [2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10, 2, 4, 6, 8, 10]

# p = Plot()
# p.plot(x,y, title="Test", xlabel="X", ylabel="Y", color1=DARK_RED)