import tkinter as tk

calculator = tk.Tk()
calculator.title('计算器')
calculator.iconbitmap(r'C:\Users\谢培圳\Desktop\calculator\kashuli.ico')
# calculator.geometry('200x200')

tk.Label(calculator, text="金额").grid(row=0)
tk.Label(calculator, text="代理点数").grid(row=1)
tk.Label(calculator, text="代扣点数").grid(row=2)

tk.Label(calculator, text="手续费").grid(row=3)
tk.Label(calculator, text="代扣手续费").grid(row=4)
tk.Label(calculator, text="给代理").grid(row=5)
tk.Label(calculator, text="给客人").grid(row=6)

# input
input_money = tk.StringVar()
agent_counts = tk.StringVar()
withhold_counts = tk.StringVar()

# output
charge = tk.StringVar()
withhold_charge = tk.StringVar()
to_agent = tk.StringVar()
to_guest = tk.StringVar()


def cal(*args):
    if not input_money.get() == '':
        amount = float(input_money.get())
        
    if not agent_counts.get() == '':
        count1 = float(agent_counts.get())
        charge_result = amount * count1 * 0.01
        to_agent_result = amount - amount * count1 * 0.01
        # 显示结果
        charge.set(str(charge_result))
        to_agent.set(str(to_agent_result))
        
    if not withhold_counts.get() == '':
        count2 = float(withhold_counts.get())
        withhold_charge_result = amount * count2 * 0.01
        to_agent_result = amount * (count2 - count1) * 0.01
        to_guest_result = amount - amount * count2 * 0.01
        # 显示结果
        to_agent.set(str(to_agent_result))
        withhold_charge.set(str(withhold_charge_result))
        to_guest.set(str(to_guest_result))
    
def reset():
    input_money.set('')
    agent_counts.set('')
    withhold_counts.set('')
    charge.set('')
    withhold_charge.set('')
    to_agent.set('')
    to_guest.set('')

e1 = tk.Entry(calculator, textvariable = input_money)
e2 = tk.Entry(calculator, textvariable = agent_counts)
e3 = tk.Entry(calculator, textvariable = withhold_counts)

e4 = tk.Entry(calculator, textvariable = charge, state="readonly")
e5 = tk.Entry(calculator, textvariable = withhold_charge, state="readonly")
e6 = tk.Entry(calculator, textvariable = to_agent, state="readonly")
e7 = tk.Entry(calculator, textvariable = to_guest, state="readonly")

b1 = tk.Button(calculator, text="计算", width = 8, command=cal)
b2 = tk.Button(calculator, text="清零", width = 8, command=reset)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)
e6.grid(row=5, column=1)
e7.grid(row=6, column=1)

b1.grid(row=8, column=0)
b2.grid(row=8, column=1)

# 将计算函数与回车键绑定
calculator.bind('<Return>', cal)

calculator.mainloop()
