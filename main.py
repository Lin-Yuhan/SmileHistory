import matplotlib.pyplot as plt
from operator import itemgetter
from json import loads
from PIL import Image

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)

with open('data.json', 'r', encoding='utf-8') as f:
    data = loads(f.read(), encoding='utf-8')

TimePoint, Note = data['Points']['Time'], data['Points']['Note']
TimePeriod, Note2 = data['Period']['Time'], data['Period']['Note']

TimeDot = TimePoint
for period in TimePeriod:
    for time_point in period:
        if not time_point in TimeDot:
            TimeDot.append(time_point)
for time_dot in TimeDot:
    plt.axvline(x=time_dot, ls=":", c="green")

def round_3(a):
    return round(a*1000)/1000

period_start = []
period_y = [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]
plt.plot(TimePoint, [3]*len(TimePoint), linestyle='-', marker='o', color="lightcoral")
for period in TimePeriod:
    plt.plot(period, [period_y[TimePeriod.index(period)%10]]*2, color='cornflowerblue', linestyle='-', marker='o')
    period_start.append(period[0])

texty = 6
for note in Note:
    texty = round_3(texty)
    plt.annotate(
        note,
        xy=(TimePoint[Note.index(note)], 3),
        xytext=(TimePoint[Note.index(note)]-0.5, texty),
        fontsize=7,
        arrowprops=dict(arrowstyle="-", color="navajowhite"),
        bbox=dict(boxstyle="round", fc="w", ec="moccasin")
        )
    texty -= 0.75
    if texty == 3:
        texty -= 0.75
    elif texty == 0:
        texty = 6

for note in Note2:
    texty = round_3(texty)
    plt.annotate(
        note,
        xy=(TimePeriod[Note2.index(note)][0], period_y[Note2.index(note)%10]),
        xytext=(TimePeriod[Note2.index(note)][0], period_y[Note2.index(note)%10]-0.5),
        fontsize=7,
        bbox=dict(boxstyle="round", fc="w", ec="lightgreen")
        )

plt.yticks([])
plt.xticks(range(min(TimeDot)-1, max(TimeDot)+1, 1))
plt.ylim(-12, 8)
plt.subplots_adjust(top = 1, bottom = 0.05, right = 1, left = 0, hspace = 0, wspace = 0)

x_lim = [min(TimeDot)-1, min(TimeDot)+7]
i = 0
img_name = []
while i<=(max(TimeDot)-min(TimeDot))/8+1:
    plt.xlim(x_lim)
    plt.savefig('./img/test_'+str(i)+'.png', dpi=100)
    img_name.append('./img/test_'+str(i)+'.png')
    x_lim[0] += 8
    x_lim[1] += 8
    i += 1

image_file = []
for img in img_name:
    image_file.append(Image.open(img))
target = Image.new('RGB', (len(img_name)*640, 480))
for image in image_file:
    target.paste(image, (image_file.index(image)*640, 0))
target.save('./img/test_all.png', quality=100)

plt.show()
