from __future__ import annotations

import sys
import json
import threading
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QHeaderView, QFrame, QStatusBar, QSizePolicy, QDialog,
    QDialogButtonBox, QComboBox, QMessageBox, QTextEdit,
    QStackedWidget, QScrollArea, QSlider, QCheckBox, QGroupBox, QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QPointF, QRectF, pyqtSlot
from PyQt6.QtGui import (
    QFont, QColor, QPalette, QIcon, QPainter, QPainterPath,
    QLinearGradient, QBrush, QPen, QPixmap, QFontDatabase
)
from PyQt6.QtWidgets import QStyleFactory, QStyleOption
from PyQt6.QtCore import QRect

_BUILTIN_CURSORS = {
    'roblox_2015': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAACS0lEQVR4nO3VT2saQRgG8GfendF2SQutSHKQLEZvPQkBDwuRBY0WAsZSz36C3s2t0MvCBoIk+QB+geZUb6VtIIemn6D0UGppq41U/LeajOv0khQbJJW4xz4whz3M/N55DrOwLOtJoVB4BuDh1taWDp/DTdN8wTkPA+BHR0cvS6VSs1qtngNQvgj7+/sqEokox3E6uVyuDMAoFot3fTkcAA4PDz0AXjQaVbZttzc3N8sAVkul0h1fgIODAyWEUAC8tbU1Zdt2O5PJ7EwhbGGAiBTn/C8km83uAFhduK4rgDGmNE1TALxYLOZfXdMAgD+Ib3VdB2YhC9U1C5iF3LquWQARKU3TVCAQUAC8eDyuHMdpb29v7wCIFIvFwK0BIrqCJgC8yyWXl5cn5XL5Vz6ffx4MBuOGYcx1Ez79oWkaPM9TiUSCGYbBRqMRIyIQEV1cXKDRaDxYX19/WqvV6s1m8zWAbwDGcwGcc0gp1cbGBkun0yPG2E8iGnDOPQBKCMH6/f654zhvpZSQUt4H8GOuG2iaBimlsiyLmabp7u7unna73Q8A6gDOr+1hAL4DGMzREDgRTaSUsCyLTNMcViqVk16vVwuHw6dCiK9CCDm9odVqqcFgIAEM8Y96AIAPh0NKJpNIpVLu3t7eSa/Xe6Xr+vHZ2dlHAO48U94Uqtfr7yzLalcqlTedTqem6/qx67qfLidkN6y5wlZWVh6Px+NUq9X6ouv6e9d1ryb35YfDADwCsCSEcKWUnwH0/Th4OkuhUOgegMXf/v+5TX4Dh28jM6QBlYYAAAAASUVORK5CYII=',
    'normal_select': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAADdElEQVR4nK1Vz2sjVRz/vPc6mZpMfkA2GthgQ2ACOYiHiPkDAioIhTamLc1FXD1Ke/NWdA8Sz/YkpfVWQgk9KEFhocW6UPCQjfZQLEG3LRihUF3BIZ2Z99mD02W27mZT1w8M83gz3+/n8/m+931P4HFIACIYM/T8L0gAkFJKCCHC8xKAukI+Ni4DUgDWA5IflFLfT01N/ZTNZs/39/f/0lqHY1QQRwD+OCQSwASAXcuyaNs2DcNwAPwG4C6Az5RStXQ6/VqxWLwhpby2AyWl9LXWn9q2/dHa2pp/dnY20ev1xOHhIbrdLvr9PrTWDwD0ANwDcATgZwB7AP4OOXoilBACSqm3TdN0tre3SdInqT3P8/v9vrezs+Otrq5ycXGRpVKJSikC+BNAJVS2kSVCoVB4GcBgZWWFJLXjOLwCTdJrtVrO5OQkhRB70Wg0G6gfufgCAOr1ugXg7tzcHF3X9UjS9336vs+LiwuSZLvd9tPpNIUQdyzLyoTjnwVJUgBo2rbNfr//iMB1XWqtubm56ScSCR/AV5lMJht2Pw4UAEQikZqUkru7ux5JDofDR+Wp1+sagJPNZt8JYoxx1D+mIB6P39daPzg4OFBaa0YiEbRaLTYaDUxPT7NarZqDweALy7LeF0K4AcFYLgQAFIvFGwC+azQaJOm1220/Ho8TwLBarfLo6MhfWFggAM8wjE/K5bIRrsAz3QRN9HmpVNJbW1tOKpUigK8zmUwdwPn8/Dwdx3GXlpZ8AFRKbRQKheS4JBPB+0MpJU3TJIA7sVjsJQCIRqO3AAyXl5d9kn6z2fSCfvgml8vdvJLjibhU8Bb+aaK9WCz2YjBnCCFgmubHANhsNj2Sen193bUsi0KIe/l8/tUQycjFfwHA66F9fnmKynK5bCilvlRKcWNjwyXJTqfj5vN5Avg1kUi8GRI7Vn+Ef5IARKFQSAohvrUsi51OxyXJXq/nVioVAvhDSvneOImfdvYrAMjlcjellD/m83l2u12PJE9PT72ZmRmapukqpW4DMMd18TSSVwD8UqlUeHJy4pPkYDC4sG2bAH5PpVJT/yX5JSYAIBqNvgHgfHZ2Vh8fH1/UajUKIRzDMD7ANZpwJImU8paU0g2UOwDeDb4/V3IguKwAQAhxG8D9QDlwjV00DgkAqGQymQ/Gz618FNG/kj8E95eD0rPZU0YAAAAASUVORK5CYII=',
    'red_hand': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABCGlDQ1BJQ0MgUHJvZmlsZQAAeJxjYGA8wQAELAYMDLl5JUVB7k4KEZFRCuwPGBiBEAwSk4sLGHADoKpv1yBqL+viUYcLcKakFicD6Q9ArFIEtBxopAiQLZIOYWuA2EkQtg2IXV5SUAJkB4DYRSFBzkB2CpCtkY7ETkJiJxcUgdT3ANk2uTmlyQh3M/Ck5oUGA2kOIJZhKGYIYnBncAL5H6IkfxEDg8VXBgbmCQixpJkMDNtbGRgkbiHEVBYwMPC3MDBsO48QQ4RJQWJRIliIBYiZ0tIYGD4tZ2DgjWRgEL7AwMAVDQsIHG5TALvNnSEfCNMZchhSgSKeDHkMyQx6QJYRgwGDIYMZAKbWPz9HbOBQAAAEV0lEQVR4nO2WS2hcVRjHf+ece+f9yMzk3YlN2yBW3Cg+kT6E4qKbujAoKLhzJ7hxHbJVd3VjV+4Uu2qhpQiu7KJCQUGpNJa2tKZJbZxHZjIz93HO5yKTGrRNMzYVRD84cC+Xc77f9/qfC9sz1V//UStDYdPrjmZCb/FNARyB4oGpqWsHpqbPAMl/DOBd8AA1nsm8f7g4Wt7v5Y6UIAW4nYS4H4A6ARGQqyRz740IUmm12hWQnXL8IAAAZkBVykXfSKxce9WMg2GHJ2JLAADlGzEGPI2ch1XWs+Dm1vc+NMyDAYzGOotK6tSxROLoDBRKe0vFeXBqHUYeBsa7l8/+khqQ0lop54iJU09MjJ/ea6OGXxi1348n3/5qefnc7mJxaL7ZbAzqeCuAjUZTAK4TuNhZPKNlCKX2pctDjVsNCsnCl5NT6YvRWOHZXUuLb/66uHL+ynqJNvZuq2E3l0ABHDp0F0qGIdHptjO5fAblhObSMpV2RxJ3FuWxMMgfHBl+ZTLo5sc74ZnXp/bdfKc8fhpIzg1QirsAs+vPfmeh8sXLk8NfPzeZryzASqfXOu90TFKsa4UBqW5LVY1W12qLUli749I3bshMN5aDuZFCFf8okJofQCs2olUnQarVqjed86sVzAtr7fCnak59JjZ4Mo4insoPa9eKmfA1NuXxYtBTudWaavRiWqFyQ8srTPXsarnfO9u1zT3gUp2OPz0980yl2UEHbmR4ZPcHl5Yuo1pd9rfSaiI5SlBfxtMhh7OGerdLKpulEVk1sRqoBdcyA/gG/iiBzIK5Uqu1frhy9bXf6vW1x/1s7N9ajjwbScUJY1GPRHeFkhbyWqNaMcVOzEQYskdrRj2fIZWgvHHggACcBDsH5tzyytlbje6HzXrdKwVrPC+oQruOdnWM62CsQzsPXAIJNYVewERSCOIGPde9CzBoBgCYBzsL5rt27ZPrvUYtn8mbPcmcjAv4LkAQnItRsUNpD2N8jBXEBoRZj1ZS2436b3cM/qyEUgJ9CWrXveD4Ykb0kJ+Jx8IExgquL1FChJUQPIeXStAwisWcB9PVwnSpNJAa/kWKT0A8C+ZsFH10sVP/pmFj38ZY5xRagdbr5yuxiHVEoSX20u52Ssvl+u2z1+v1Xl+a//7NObt+63EMDnyeL/ZupofitpeRWBlxWotVSiKlxOqkROTcz+mS+7iUWwWy9wts2xkAONkXklPw7Y9xGN0wRvdM2jnxiZzBikHEB/FxJNGZEt180ZXLbIzhtqO/110A/bEE7FIYvrWQzZ6aSRacb1MREoBSoFFOPBM6Ffnl0cTYnpwvVzqKWn27vrcE2BhLPW/t6YpRpyZTiWO7jGci8RFPiHCETuGbdOJqtNa+sNRs1pvaDeSdB0+LmgMzD/EbycyrecVLa8450eiuc03BXE145ulfOvr4BVYjoM0j+G17pLbtmZ0FU9rUtBMgl/q68SnE/YP+XdH/b/8bwO9e/92jeL0keAAAAABJRU5ErkJggg==',
    'purple_dot': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABCGlDQ1BJQ0MgUHJvZmlsZQAAeJxjYGA8wQAELAYMDLl5JUVB7k4KEZFRCuwPGBiBEAwSk4sLGHADoKpv1yBqL+viUYcLcKakFicD6Q9ArFIEtBxopAiQLZIOYWuA2EkQtg2IXV5SUAJkB4DYRSFBzkB2CpCtkY7ETkJiJxcUgdT3ANk2uTmlyQh3M/Ck5oUGA2kOIJZhKGYIYnBncAL5H6IkfxEDg8VXBgbmCQixpJkMDNtbGRgkbiHEVBYwMPC3MDBsO48QQ4RJQWJRIliIBYiZ0tIYGD4tZ2DgjWRgEL7AwMAVDQsIHG5TALvNnSEfCNMZchhSgSKeDHkMyQx6QJYRgwGDIYMZAKbWPz9HbOBQAAACMElEQVR4nO2VzWsTQRiHn9ndbNxNNt2maWnNoYgFe1PIQfHSiwfRol6CN70F716F0v9CetOTUi89RFEQFBEvRkHw4EeLlGLaVNM2SbfZ3dldD239QCFJrfWyz2WGmXdefvObd2YgJiYm5j8j9rquQEn7eaDCjASiv5fUkSllb3N/plcHBBBlyGQtJq4lsRIS8Gn6VV7fhKX6bsw/EFBUYTbIcWlyQBy7NZIaz6aMfvywzaZX48vWu/q6XLi6woMyFBWYDfZTwE6clR3jyuIR87I5ZI94quYKGcgoVNvUnff6x/pjZyF8NAhVB1CAsFPirs6sQEEDolFOlw4bx41+c8TdaL7R55dvJxZqZb25WdXtdJ8cNI8aw5y8A2NJmOpqZ10WTQEAnVzSTudFUhei7rySVe/e5KL/bK7e/oRpGNjmgFDRJyE8BNMhXTjcU9V6hMjIBcUnUFKqy3gpYPCElDqehyIUNRKwDBsdrd9F6xwClZ3WoeGue0uRZQ4LOz0maOsXVNWmT8/juJ5stZu6QnQXvrYKlBIVZvx9EcD2IyNWmZ/p33p7w9L7zLRl+bncuKIn0pHr+mFtfVGrtT7IFo0yEFVY68qFnq9hnnPnU2p+LpcaVTOGjaJoNJw1VlrzQSP4fHGF++Xd2H0WANsv3XSYZeKMwdB1FeNUhPs8JHzpsPpijScPYUKDp7K3vD1RVH/0z2Z+F3ggFFWIdtyLRIFS4ldhB8def9OYmJiY73wDLx3FVNjEKyMAAAAASUVORK5CYII=',
    'crosshair': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAeElEQVR4nO2XQQrAIAwETelj4lva59q/5Dfbk0UqBWmEIOycvOxmEBFNifgpocMBwCOxTZShAAUoQIE1BcQThiqeIrNfXe/Q8J0O1aMrM7sG42dd7O1wAF3pJzn3UoN5ESlVInwHws+AF74HKEABCqwvMIPQr9n63C6vJvh5UWEvAAAAAElFTkSuQmCC',
    'arrow_neon': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAA1ElEQVR4nO3WvQ3CMBCG4TdRKhqapDUFjMEcTMAQZgIYgiLjZAhTQGsKmMDpkJX/Ij5LyF8XO5KfO+ekoJw2REwO0DhTRwUAxOrED/Dkuo+ByP2HGIi8uyCN6AGkEYMAScQoQAoxCZBAzAJCIxYBQiIWA0IhirkXdlwe3TXltHllt4MIAGCtw4bSu4JuxaJTMNTu4FFOm8aZ2q9SOW2cl7IsP0HH8MT9OHXP1tptiMOB8R8RqS4Uc194VVVfgI09v9c+HCCb2vQrDjmKiwApKSkpf5sWlfF9r5gfCRcAAAAASUVORK5CYII=',
    'sword': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAA1UlEQVR4nO3WrQ7CMBAH8H8JCoOpQWOmMRj0DIg+AqIGngCFQKPBTOwREMVMI/YQaDDTtYdqAwnQkJR14s61a3O/pdcPgAMAUWnopuhqMmIEIzqPOGgZFdX79EGI5QIjdR5PMjiESx4TIUIDiEqD+2l+3F5837pogvOiAYDXP46ZHPiyBO+Sr3YzJClMh+j07mAEIxjRCYTZy3qTS9LTYZ0MAQCMYMQviKh3ewjRwPp2UVkBAP22AA0sVC6fe6iorAg+SP4dyQGt1QAA6Hzgj2lXA8njATLPx/gOFYDcAAAAAElFTkSuQmCC',
    'plus_crosshair': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAA4klEQVR4nO3SPWoDMRAF4DejBAwBwRbbqVKXO/gcOUZUqfUhfIxtVW0jfIW9QcBFylSuwvLcrMFlJPJDYL5mkBg9xDCAMcaY/4ykI+n++h+/j6SQ1JzzMed8JKkkpSfroeeRiBAA53l+2c6vPTkAoC3N0zQ5AEgpHUoppxjjLsa4K6WcUkqH+56vaprAOI4CAN775xDCfhiGFQBCCHvv/ft9z097AjDUWs+11jOAYbtr1rUDzrkLycuyLG8AoKofIoJ1XZuzesd1e/e41c+tsjOvj6pCtWmPv52gf4rGGGMAAFeBEkHrw9wlUAAAAABJRU5ErkJggg==',
    'dash_crosshair': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAApUlEQVR4nO3TPQ7CMAwF4GeZDYmpHXIDll4JjpA1Z8qS5CwdeoJeAImxMWuLitRawFJ/U2Q9R1Z+AGOMMUdHX+yVvw1ARGDmRW2aJoioZlCjD+vfiTEyAHjvbymloZTS55z7lNIQQrjPM1ud9oTbtiUAcM41Xddda60iImBmGsexmWe20h7dGcDlrfYA8Ny7kfruiJat2geoHYBWegXKr2iMMebYXrhxLGKPNy5LAAAAAElFTkSuQmCC',
    'himitsu': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAaklEQVR4nO3RsQnAMAxEUSNnoJtDdVR6Fq2i1byIlTaENMFgQ7hXufI/UClEREQTzKyaWd0Wf3svjQM4AdjSEe4umSmq2iKiR0RX1ZaZ4u7y9b9jZswYY+/9AdjyEzxHbInfw9viRET0Gxfu4iOhNG7CUAAAAABJRU5ErkJggg==',
    'sinaways': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAJoWlDQ1BJQ0MgUHJvZmlsZQAAeJztmWdQVFkWgO97r3OgobtpMjQ5SZTQgOScJEdRge4m00KTwYgMjsAIIiJJEUQUcMDRIcgoKqIYEAUFzNPIIKCMg6OIisoC/pit2q3d2qqt/bN9frz31bmn3jn31a16X9UDQIaQwE5MgfUBSOSl8n2d7ZjBIaFM7H2AA2RAAlSAiWCnJHn6OfmD5VipBf8Q70cBtHK/p/PP1/9lkDiJPA4AEH2Z4zjcFPYy71zmGE4iZyU/vcIZqUmpAMDey0znLw+4zJwVjvzGmSsc/Y2LVmv8fe2X+SgAOFL0KhNOrXDkKlO7Vpgdw08EQLpvuV6FncRffr70Si/FbzOshujKfpjRXB6XH5HK5TD/w639+/i7XuiU5Zf/X2/wP+6zcna+0VvL1TMBMSr+ym0pA4D1GgCk5K+cymEAKLsB6Oj5Kxd5HIDOEgAkn7HT+OnfcqjV2QEBUAAdSAF5oAw0gA4wBKbAAtgAR+AGvIA/CAGbABvEgETABxlgK9gF8kEhKAEHQRWoBQ2gCbSCM6ATnAeXwTVwC9wFI+AxEIBJ8ArMgfdgEYIgLESGaJAUpACpQtqQIcSCrCBHyAPyhUKgcCga4kFp0FZoN1QIlUJVUB3UBP0EnYMuQzegIeghNA7NQH9Cn2AEJsF0WA5Wg/VgFmwLu8P+8EY4Gk6Gs+E8eB9cAdfDp+AO+DJ8Cx6BBfAreB4BCBFhIIqIDsJC7BEvJBSJQvjIdqQAKUfqkVakG+lH7iECZBb5iMKgaCgmSgdlgXJBBaDYqGTUdlQRqgp1EtWB6kPdQ42j5lBf0WS0LFobbY52RQejo9EZ6Hx0OboR3Y6+ih5BT6LfYzAYBkYdY4pxwYRg4jA5mCLMYUwb5hJmCDOBmcdisVJYbawl1gsbgU3F5mMrsaewF7HD2EnsBxwRp4AzxDnhQnE8XC6uHNeM68EN46Zwi3hRvCreHO+F5+Cz8MX4Bnw3/g5+Er9IECOoEywJ/oQ4wi5CBaGVcJXwhPCWSCQqEc2IPsRY4k5iBfE08TpxnPiRRCVpkexJYaQ00j7SCdIl0kPSWzKZrEa2IYeSU8n7yE3kK+Rn5A8iNBFdEVcRjsgOkWqRDpFhkdcUPEWVYkvZRMmmlFPOUu5QZkXxomqi9qIRottFq0XPiY6JzovRxAzEvMQSxYrEmsVuiE1TsVQ1qiOVQ82jHqNeoU7QEJoyzZ7Gpu2mNdCu0ibpGLo63ZUeRy+k/0gfpM+JU8WNxAPFM8WrxS+ICxgIQ43hykhgFDPOMEYZnyTkJGwluBJ7JVolhiUWJGUkbSS5kgWSbZIjkp+kmFKOUvFS+6U6pZ5Ko6S1pH2kM6SPSF+VnpWhy1jIsGUKZM7IPJKFZbVkfWVzZI/JDsjOy8nLOcslyVXKXZGblWfI28jHyZfJ98jPKNAUrBRiFcoULiq8ZIozbZkJzApmH3NOUVbRRTFNsU5xUHFRSV0pQClXqU3pqTJBmaUcpVym3Ks8p6Kg4qmyVaVF5ZEqXpWlGqN6SLVfdUFNXS1IbY9ap9q0uqS6q3q2eov6Ew2yhrVGska9xn1NjCZLM17zsOZdLVjLWCtGq1rrjjasbaIdq31Ye2gNeo3ZGt6a+jVjOiQdW510nRadcV2Grodurm6n7ms9Fb1Qvf16/Xpf9Y31E/Qb9B8bUA3cDHINug3+NNQyZBtWG95fS17rtHbH2q61b4y0jbhGR4weGNOMPY33GPcafzExNeGbtJrMmKqYhpvWmI6x6CxvVhHruhnazM5sh9l5s4/mJuap5mfM/7DQsYi3aLaYXqe+jruuYd2EpZJlhGWdpcCKaRVuddRKYK1oHWFdb/3cRtmGY9NoM2WraRtne8r2tZ2+Hd+u3W7B3tx+m/0lB8TB2aHAYdCR6hjgWOX4zEnJKdqpxWnO2dg5x/mSC9rF3WW/y5irnCvbtcl1zs3UbZtbnzvJ3c+9yv25h5YH36PbE/Z08zzg+WS96nre+k4v4OXqdcDrqbe6d7L3Lz4YH2+fap8Xvga+W337/Wh+m/2a/d772/kX+z8O0AhIC+gNpASGBTYFLgQ5BJUGCYL1grcF3wqRDokN6QrFhgaGNobOb3DccHDDZJhxWH7Y6Eb1jZkbb2yS3pSw6cJmyuaIzWfD0eFB4c3hnyO8Iuoj5iNdI2si59j27EPsVxwbThlnhmvJLeVORVlGlUZNR1tGH4ieibGOKY+ZjbWPrYp9E+cSVxu3EO8VfyJ+KSEooS0RlxieeI5H5cXz+rbIb8ncMpSknZSfJEg2Tz6YPMd35zemQCkbU7pS6csf6YE0jbTv0sbTrdKr0z9kBGaczRTL5GUOZGll7c2aynbKPp6DymHn9G5V3Lpr6/g2221126Htkdt7dyjvyNsxudN558ldhF3xu27n6ueW5r7bHbS7O08ub2fexHfO37Xki+Tz88f2WOyp/R71fez3g3vX7q3c+7WAU3CzUL+wvPBzEbvo5g8GP1T8sLQvat9gsUnxkRJMCa9kdL/1/pOlYqXZpRMHPA90lDHLCsreHdx88Ea5UXntIcKhtEOCCo+KrkqVypLKz1UxVSPVdtVtNbI1e2sWDnMODx+xOdJaK1dbWPvpaOzRB3XOdR31avXlxzDH0o+9aAhs6D/OOt7UKN1Y2PjlBO+E4KTvyb4m06amZtnm4ha4Ja1l5lTYqbs/OvzY1arTWtfGaCs8DU6nnX75U/hPo2fcz/SeZZ1t/Vn155p2WntBB9SR1THXGdMp6ArpGjrndq6326K7/RfdX06cVzxffUH8QnEPoSevZ+li9sX5S0mXZi9HX57o3dz7+Erwlft9Pn2DV92vXr/mdO1Kv23/xeuW18/fML9x7ibrZuctk1sdA8YD7beNb7cPmgx23DG903XX7G730LqhnmHr4cv3HO5du+96/9bI+pGh0YDRB2NhY4IHnAfTDxMevnmU/mjx8c4n6CcFT0Wflj+TfVb/q+avbQITwYVxh/GB537PH0+wJ179lvLb58m8F+QX5VMKU03ThtPnZ5xm7r7c8HLyVdKrxdn838V+r3mt8frnP2z+GJgLnpt8w3+z9GfRW6m3J94Zveud955/9j7x/eJCwQepDyc/sj72fwr6NLWY8Rn7ueKL5pfur+5fnywlLi0JXUDoAkIXELqA0AWELiB0AaELCF1A6AJCFxC6gNAFhC4gdIH/YxdY/Y+zHMjK5dgYAP45AHjcBqCyCgC1KAAoYanczNSVVd4WJntLUhY/NjomdQ0zLYXLjOJzuQlZgPA3Dn8KHV7zVqUAAADySURBVHic7dYxSgNBFAbgL5uEgBAbPZOIFnoKb+ApPIcgigrewFaCBwhWglUgYmNY3c2zSFa2SLAwziLsD1P/H8PMm6FNmzZt2rT57wk6TRsEWWPFJ2wlR1TbfsrwgZd7jmBEPylgh+Ezs1fKcw6SISrAPttjpkFM+LxNhagDnngL5kE5oUiCWAGIgiIZYhWgXO5CEsQ6wJwI8iCfMrthDy7ppgCUsQB8r3fijmN0Yg2itylTRjaheOSsy0dGsUtvQI642lDRom3NNbzmcJM9PwLqg+hieejGDEb0q/UnI7rxUVyDNPMYrYI0Wd78h+Q3+QJyx4eaY9k8QAAAAABJRU5ErkJggg==',
    'x_crosshair': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAb0lEQVR4nO3TwQnAIAwF0N/WU6lzOEZWERfx0FkcwP2U9OKh57QUiv9BLoGEQBKAiIjomWXEpFJKPoTgc87O2mO1FKnqBgAxxrOUUgE4VTWtwjQAAB2D9NZav+W/vQcROQDsImJewe9N/oZERPSGC0A6GAMC5mM9AAAAAElFTkSuQmCC',
    'shiftlock_traingle': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAA70lEQVR4nO3SPYqDQBQA4PeewcrSrU0hQiCnmMZqiq22NhewzsLy9gDbioiFxQpbyF7BQ3iIXEBSRfLSGEixjcKwBN5XDTMD7xdAKaWUemYiQiJC/xUc/zovtVkbHBGlqqqj53kXRPwSEULEq/MEmJkAQNI03UZR9DlN08UY8wMAJwAgAFiUxOLW3Stt2/Z7HMcNEZHv++csyw5rurBogZiZEPHKzPsgCF77vn8fhuEjDMO3PM9385u7pZw3Hsuy/K3rur3fN03TFUXRPfxxiqy1JkmSUERQRDCO4xdrrYEVI31O85wfq0Wns1dKKZdu33lebWp/Oq0AAAAASUVORK5CYII=',
    'white_dot': 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABBElEQVR4nO3TIW7EMBAF0D+OacJzBaNVT5ALWIvMTbsHCDVMcEDVXsHcOCDhC/cIyQXaovUUNJWCqmykVKrkJw2xx5qRxwaSJEmS/8o5J5hZMrN0zok/Lc7MtGVtC/noAeecIKJYluVTXdfPMUZ0XfdCRFdmJiLiPY1sLs7MpJQ6DcPwwYtxHN+VUidmpkPH0fe9BIC2bd+W2p9LcNM0r+ucrR5KrqoKAJDneQ7gHmMUACCEuBdFUaxzDmGMyYgIWuvzPM8/E+BpmlhrfSYiGGOy4zrA9zsAAGvtJYRwCyHcrLWX9d7hVl9OLLH7G+7mvc+klJBSwnt/7LX/gpZIkiRJdvsClZiATh0n+JwAAAAASUVORK5CYII=',
}
_BUILTIN_CURSOR_NAMES = {
    'roblox_2015': 'Roblox 2015',
    'normal_select': 'Normal Select',
    'red_hand': 'Red Hand',
    'purple_dot': 'Purple Dot',
    'crosshair': 'Crosshair',
    'arrow_neon': 'Neon Arrow',
    'sword': 'Sword',
    'plus_crosshair': '+ crosshair',
    'dash_crosshair': 'Dash crosshair',
    'himitsu': 'Himitsu',
    'sinaways': 'Sinaways',
    'x_crosshair': 'X crosshair',
    'shiftlock_traingle': 'shiftlock traingle',
    'white_dot': 'white dot',
}

BUILTIN_PRESETS = [{'name': "Taehi's Main FFlags", 'desc': '12 flags · Main optimized config', 'flags': {'DebugLimitMinTextureResolutionWhenSkipMips': '2147483647', 'DoNotSkipMipsBasedOnSystemMemoryPS': 'True', 'TM2SkipMipsForUnstreamable2': 'True', 'RenderUseTextureManager224': 'False', 'DebugTextureManagerSkipMips': '3', 'EnablePowerTraceModule': 'True', 'IncludePowerSaverMode': 'True', 'DebugFRMQualityLevelOverride': '1', 'FFlagDebugSkyGray': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4000', 'DFIntTouchSenderMaxBandwidthBps': '-9999', 'DFIntRemoteEventSingleInvocationSizeLimit': '2900'}, 'tag': 'MAIN'}, {'name': 'Potato Low Graphics', 'desc': '117 flags · Max performance, low gfx', 'flags': {'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'DFIntTaskSchedulerTargetFps': '2147483647', 'FFlagDebugDisplayFPS': 'True', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagDisableDPIScale': 'True', 'FFlagDebugGraphicsPreferD3D11': 'False', 'FIntDebugForceMSAASamples': '1', 'FFlagDebugGraphicsPreferVulkan': 'True', 'DFIntTextureCompositorActiveJobs': '0', 'FIntRenderShadowmapBias': '0', 'FIntTerrainArraySliceSize': '0', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'FFlagRenderUseTextureManager224': 'False', 'FFlagIncludePowerSaverMode': 'True', 'FFlagEnablePowerTraceModule': 'True', 'FFlagDebugForceFSMCPULightCulling': 'True', 'DFFlagDoNotSkipMipsBasedOnSystemMemoryPS': 'True', 'DFIntDebugLimitMinTextureResolutionWhenSkipMips': '9999999999999999', 'TM2SkipMipsForUnstreamable2': 'True', 'FIntDebugTextureManagerSkipMips': '10', 'DFIntTextureQualityOverride': '12', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagAcceleratorUpdateOnPropsAndValueTimeChange': 'True', 'DFFlagTeleportClientAssetPreloadingDoingExperiment2': 'True', 'FIntRuntimeMaxNumOfSchedulers': '1000000', 'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '25', 'DFFlagReplicatorSeparateVarThresholds': 'True', 'DFIntClientPacketMaxFrameMicroseconds': '200', 'DFIntRakNetNakResendDelayMsMax': '1', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntReplicationDataCacheNumParallelTasks': '20', 'DFIntGraphicsOptimizationModeFRMFrameRateTarget': '144', 'DFIntRakNetLoopMs': '1', 'FIntRuntimeMaxNumOfSemaphores': '1000000', 'DFIntTimestepArbiterAccelerationModelFactorThou': '50000', 'DFIntMaxFrameBufferSize': '4', 'DFFlagDebugLargeReplicatorForceFullSend': 'True', 'DFFlagTeleportClientAssetPreloadingEnabledIXP2': 'True', 'FFlagEnableZstdForClientSettings': 'False', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'FIntSmoothMouseSpringFrequencyTenths': '100', 'DFIntTouchSenderMaxBandwidthBpsScaling': '2', 'DFIntTaskSchedulerJobInitThreads': '6', 'FIntRobloxGuiBlurIntensity': '0', 'DFFlagRakNetEnablePoll': 'True', 'DFIntSendItemLimit': '5', 'DFIntDataSenderRate': '20000', 'DFIntClusterSenderMaxJoinBandwidthBps': '2100000000', 'DFIntPhysicsReceiveNumParallelTasks': '5', 'DFIntNetworkClusterPacketCacheNumParallelTasks': '5', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntRuntimeConcurrency': '12', 'DFIntClusterCompressionLevel': '0', 'DFFlagAnimatorEnableNewAdornments': 'False', 'DFFlagJointIrregularityOptimization': 'True', 'DFFlagTeleportClientAssetPreloadingEnabled9': 'True', 'FIntInterpolationMaxDelayMSec': '100', 'DFIntNumAssetsMaxToPreload': '9999999', 'DFFlagDebugLargeReplicatorDisableDelta': 'True', 'FIntFRMMaxGrassDistance': '0', 'FIntTaskSchedulerAutoThreadLimit': '6', 'FIntRuntimeMaxNumOfConditions': '1000000', 'DFIntTaskSchedulerJobInGameThreads': '6', 'DFFlagRakNetDetectRecvThreadOverload': 'True', 'DFIntBatchThumbnailResultsSizeCap': '200', 'DFIntNetworkQualityResponderUnit': '10', 'DFIntBufferCompressionThreshold': '100', 'DFFlagReplicatorCheckReadTableCollisions': 'True', 'FIntGrassMovementReducedMotionFactor': '0', 'DFFlagReplicateCreateToPlayer': 'True', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'FFlagQuaternionPoseCorrection': 'True', 'DFFlagAnimatorAnywhere': 'True', 'FIntSimSolverResponsiveness': '2147483647', 'FIntRuntimeMaxNumOfThreads': '12', 'DFIntServerBandwidthPlayerSampleRate': '10', 'DFIntRakNetApplicationFeedbackScaleUpThresholdPercent': '0', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntNetworkSchemaCompressionRatio': '0', 'FIntRakNetResendBufferArrayLength': '128', 'DFIntMaxDataPacketPerSend': '2147483647', 'DFIntMegaReplicatorNumParallelTasks': '5', 'FIntActivatedCountTimerMSMouse': '0', 'DFIntPerformanceControlFrameTimeMax': '1', 'FIntRuntimeMaxNumOfLatches': '1000000', 'FIntRuntimeMaxNumOfMutexes': '1000000', 'DFIntInterpolationNumParallelTasks': '5', 'FIntActivatedCountTimerMSKeyboard': '0', 'DFIntS2PhysicsSenderRate': '25000', 'DFIntClusterSenderMaxUpdateBandwidthBps': '2100000000', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntNetworkQualityResponderMaxWaitTime': '1', 'DFIntMaxReceiveToDeserializeLatencyMilliseconds': '10', 'FFlagDebugCodegenOptSize': 'True', 'DFIntTimestepArbiterAngAccelerationThresholdThou': '2000', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '5', 'DFIntClientPacketExcessMicroseconds': '1000', 'FFlagDebugCheckRenderThreading': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagDebugPerfMode': 'True', 'DFFlagRakNetUseSlidingWindow4': 'True', 'DFIntRakNetNakResendDelayMs': '1', 'DFIntRakNetSelectTimeoutMs': '1', 'DFIntClientPacketMaxDelayMs': '1', 'DFIntConnectingTimerInterval': '10', 'DFIntBufferCompressionLevel': '0', 'DFIntClientPacketHealthyAllocationPercent': '20', 'DFIntTouchSenderMaxBandwidthBps': '-1', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntCanHideGuiGroupId': '32380007', 'FFlagDebugSkyGray': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '1200', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4000', 'FFlagDisablePostFx': 'True'}, 'tag': 'PERF'}, {'name': 'Basic FPS Boost', 'desc': '108 flags · FPS + network boost', 'flags': {'DFIntTaskSchedulerTargetFps': '9999', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntTextureQualityOverride': '0', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FFlagDisablePostFx': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FIntDebugForceMSAASamples': '1', 'FIntRenderShadowIntensity': '0', 'FIntTerrainArraySliceSize': '0', 'FIntFontSizePadding': '5', 'DFFlagDisableDPIScale': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'FLogNetwork': '7', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagSolverStateReplicatedOnly2': 'True', 'DFFlagRakNetUseSlidingWindow4': 'True', 'DFFlagRakNetCalculateApplicationFeedback2': 'True', 'DFFlagReplicatorSeparateVarThresholds': 'True', 'DFFlagTaskSchedulerAvoidSleep': 'True', 'DFFlagReplicateCreateToPlayer': 'True', 'DFFlagRakNetEnablePoll': 'True', 'DFFlagRakNetDetectNetUnreachable': 'True', 'DFFlagRakNetDetectRecvThreadOverload': 'True', 'DFFlagEnableTexturePreloading': 'True', 'FFlagEnableAnimatorSkipCopyPreviousRigKeyOnJointModification': 'True', 'FFlagPreComputeAcceleratorArrayForSharingTimeCurve': 'True', 'FFlagEnablePlayerViewBoundingBoxSizeDamping': 'True', 'FFlagRenderEnableGlobalInstancingD3D10': 'True', 'FFlagLuaAppLegacyInputSettingRefactor': 'True', 'FFlagEnablePerformanceControlService': 'True', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagPreloadTextureItemsOption4': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagUserShowGuiHideToggles': 'True', 'FFlagDebugDisplayFPS': 'True', 'FFlagDebugSkyGray': 'True', 'FFlagEnableZstdDictionaryForClientSettings': 'False', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagEnableZstdForClientSettings': 'False', 'DFIntRakNetApplicationFeedbackScaleUpFactorHundredthPercent': '0', 'DFIntRakNetApplicationFeedbackScaleUpThresholdPercent': '0', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '25', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'DFIntMaxReceiveToDeserializeLatencyMilliseconds': '10', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntClientPacketHealthyAllocationPercent': '20', 'DFIntNetworkInProcessLimitGameplayMsClient': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '2', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '3', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4', 'DFIntInitialAccelerationLatencyMultTenths': '1', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntMaxProcessPacketsStepsPerCyclic': '10000', 'DFIntClientPacketMaxFrameMicroseconds': '200', 'DFIntNetworkQualityResponderMaxWaitTime': '1', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntClientPacketExcessMicroseconds': '1000', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntMegaReplicatorNumParallelTasks': '20', 'DFIntPhysicsReceiveNumParallelTasks': '20', 'DFIntBatchThumbnailResultsSizeCap': '200', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntMaxDataPacketPerSend': '2147483647', 'DFIntBufferCompressionThreshold': '100', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntNetworkQualityResponderUnit': '10', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntRakNetNakResendDelayMsMax': '100', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntConnectingTimerInterval': '10', 'DFIntMaxAcceptableUpdateDelay': '1', 'DFIntRakNetResendRttMultiple': '1', 'DFIntBufferCompressionLevel': '0', 'DFIntClientPacketMaxDelayMs': '1', 'DFIntRakNetNakResendDelayMs': '5', 'DFIntRakNetSelectTimeoutMs': '1', 'DFIntMaxFrameBufferSize': '4', 'DFIntRakNetLoopMs': '1', 'FIntSimSolverResponsiveness': '2147483647', 'FIntUITextureMaxRenderTextureSize': '1024', 'FIntRakNetResendBufferArrayLength': '128', 'FIntDebugTextureManagerSkipMips': '2', 'FIntInterpolationMaxDelayMSec': '100', 'FIntTerrainOTAMaxTextureSize': '1024', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntDefaultMeshCacheSizeMB': '256', 'FIntRenderGrassDetailStrands': '0', 'FIntCSGVoxelizerFadeRadius': '0', 'FIntRobloxGuiBlurIntensity': '0', 'FIntTaskSchedulerThreadMin': '3', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntRenderShadowmapBias': '0', 'FIntTargetRefreshRate': '240', 'FIntMeshContentProviderForceCacheSize': '268435456'}, 'tag': 'FPS'}, {'name': 'Reduced Latency (Universal)', 'desc': '10 flags · Physics & network latency', 'flags': {'FFlagUGCValidationFixResetPhysicsError': True, 'DFIntS2PhysicsSenderRate': 35200, 'DFIntPhysicsReceiveNumParallelTasks': 12, 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': 20, 'DFFlagSimEnableStepPhysicsSelective': False, 'DFFlagSimEnableStepPhysics': False, 'DFFlagSimClearNetworkPhysicsDataForAssembly': True, 'DFFlagPreventReturnOfElevatedPhysicsFPS': False, 'DFFlagPhysicsMechanismCacheOptimizeAlloc': True, 'DFFlagDebugReportElevatedPhysicsFPSTOGA': False}, 'tag': 'NET'}, {'name': "Toshiro's Config", 'desc': '90 flags · Optimized performance config', 'flags': {'CSGLevelOfDetailSwitchingDistanceL23': '0', 'DFFlagDoNotSkipMipsBasedOnSystemMemoryPS': 'True', 'DFFlagBrowserTrackerIdTelemetryEnabled': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagAddPlaySessionIdTelemetry': 'False', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagDisableDPIScale': 'True', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntLocalLightCountsInCompatibilityThrottlePerTenThousand': '0', 'DFIntDebugLimitMinTextureResolutionWhenSkipMips': '2147483647', 'DFIntExperienceStateCaptureHighlightTransparencyPercent': '0', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '20', 'DFIntRemoteEventSingleInvocationSizeLimit': '2900', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntReplicationDataCacheNumParallelTasks': '20', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntVisibilityCheckRayCastLimitPerFrame': '10', 'DFIntTreeDiffModCheckShadowReportingRate': '0', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntPhysicsReceiveNumParallelTasks': '20', 'DFIntNetworkSchemaCompressionRatio': '100', 'DFIntAnimatorThrottleMaxFramesToSkip': '1', 'DFIntMegaReplicatorNumParallelTasks': '20', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntBufferCompressionThreshold': '100', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntTextureCompositorActiveJobs': '0', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntTaskSchedulerTargetFps': '9999', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntMaxActiveAnimationTracks': '0', 'DFIntRakNetResendRttMultiple': '1', 'DFIntTextureQualityOverride': '1', 'DFIntBufferCompressionLevel': '0', 'DFIntRenderShadowHugeRadius': '0', 'DFIntS2PhysicsSenderRate': '100', 'DFIntConnectionMTUSize': '900', 'DFIntMaxFrameBufferSize': '4', 'DFIntRakNetLoopMs': '1', 'DFStringLightstepHTTPTransportUrlPath': 'null', 'DFStringLightstepHTTPTransportUrlHost': 'null', 'DFStringLightstepToken': 'null', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagRenderUseTextureManager224': 'False', 'FFlagPreloadTextureItemsOption4': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagDebugGraphicsPreferD3D11': 'False', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FFlagEnablePowerTraceModule': 'True', 'FFlagRenderInitShadowmaps': 'False', 'FFlagIncludePowerSaverMode': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagDebugDisplayFPS': 'True', 'FFlagDebugPerfMode': 'True', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FIntRenderMaxShadowAtlasUsageBeforeDownscale': '0', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '20', 'FIntRenderShadowMapDepthCacheMinNodes': '0', 'FIntRenderShadowMapDepthCacheMemLimit': '0', 'FIntDebugFRMOptionalMSAALevelOverride': '1', 'FIntUITextureMaxRenderTextureSize': '1024', 'FIntGrassMovementReducedMotionFactor': '0', 'FIntRakNetResendBufferArrayLength': '128', 'FIntSimWorldTaskQueueParallelTasks': '20', 'FIntDebugTextureManagerSkipMips': '4', 'FIntTerrainOTAMaxTextureSize': '1024', 'FIntRenderLocalLightUpdatesMin': '0', 'FIntRenderLocalLightUpdatesMax': '0', 'FIntCameraMaxZoomDistance': '99999', 'FIntDefaultMeshCacheSizeMB': '256', 'FIntUnifiedLightingBlendZone': '0', 'FIntRenderLocalLightFadeInMs': '0', 'FIntRobloxGuiBlurIntensity': '0', 'FIntTerrainArraySliceSize': '0', 'FIntDebugForceMSAASamples': '0', 'FIntRenderShadowmapBias': '0', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntSSAOMipLevels': '0', 'FLogNetwork': '7', 'TM2SkipMipsForUnstreamable2': 'True'}, 'tag': 'CFG'}, {'name': 'No Lava Damage', 'desc': '1 flag · Disables lava damage', 'flags': {'DFIntTouchSenderMaxBandwidthBps': '-9999'}, 'tag': 'FUN'}, {'name': 'No Draco Aura', 'desc': '1 flag · Removes Draco v4 aura effect', 'flags': {'DFIntRemoteEventSingleInvocationSizeLimit': '2900'}, 'tag': 'FUN'}, {'name': 'Skybox Override', 'desc': '1 flag · Forces skybox texture skip', 'flags': {'FIntDebugTextureManagerSkipMips': '10'}, 'tag': 'FUN'}, {'name': 'Dash Extender', 'desc': '2 flags · Extends dash distance', 'flags': {'DFIntSimTimestepMultiplierDebounceCount': '-1100000', 'DFIntSimAdaptiveHumanoidPDControllerSubstepMultiplier': '-999999'}, 'tag': 'FUN'}, {'name': 'No Animation', 'desc': '1 flag · Disables all player animations', 'flags': {'DFIntMaxActiveAnimationTracks': '0'}, 'tag': 'FUN'}, {'name': 'Super Jump', 'desc': '3 flags · Enables super jump physics', 'flags': {'FFlagDebugHumanoidNewPhysicsEnabled': 'True', 'DFFlagDebugSimLevitationNormalPD': 'True', 'DFIntDebugSimLevitationNormalPD100xPeriod': '3'}, 'tag': 'FUN'}, {'name': 'SpinBot Movement', 'desc': '10 flags · Crazy physics movement', 'flags': {'DFIntNonSolidFloorPercentForceApplication': '-100', 'DFIntSolidFloorMassMultTenth': '2147483647', 'DFIntSolidFloorPercentForceApplication': '100', 'DFIntMaximumFreefallMoveTimeInTenths': '2147483647', 'DFFlagDebugPhysicsSenderDoesNotShrinkSimRadius': 'True', 'DFIntMaxClientSimulationRadius': '99999', 'DFIntMinClientSimulationRadius': '99998', 'FFlagDebugUseCustomSimRadius': 'True', 'FIntSimDefaultFluidForceEnabled': '12', 'DFIntPhysicsImprovedCyclicExecutiveThrottleThresholdTenth': '-1'}, 'tag': 'FUN'}, {'name': 'FPS Unlocker', 'desc': '2 flags · Removes FPS cap', 'flags': {'DFIntTaskSchedulerTargetFps': '9999999', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False'}, 'tag': 'FPS'}, {'name': 'Display FPS', 'desc': '1 flag · Shows FPS counter', 'flags': {'FFlagDebugDisplayFPS': 'True'}, 'tag': 'FPS'}, {'name': 'No Textures', 'desc': '11 flags · Maximum performance no textures', 'flags': {'DFFlagDoNotSkipMipsBasedOnSystemMemoryPS': 'True', 'DFIntDebugLimitMinTextureResolutionWhenSkipMips': '8', 'FFlagTM2SkipMipsForUnstreamable2': 'True', 'FIntDebugTextureManagerSkipMips': '8', 'DFIntTextureQualityOverride': '0', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FFlagDisablePostFx': 'True', 'DFIntTaskSchedulerTargetFps': '9999999', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagDebugDisplayFPS': 'True', 'FFlagDebugSkyGray': 'True'}, 'tag': 'PERF'}, {'name': 'Less Ping', 'desc': '10 flags · Reduces network latency', 'flags': {'FFlagUGCValidationFixResetPhysicsError': 'True', 'DFIntS2PhysicsSenderRate': '35200', 'DFIntPhysicsReceiveNumParallelTasks': '12', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '20', 'DFFlagSimEnableStepPhysicsSelective': 'False', 'DFFlagSimEnableStepPhysics': 'False', 'DFFlagSimClearNetworkPhysicsDataForAssembly': 'True', 'DFFlagPreventReturnOfElevatedPhysicsFPS': 'False', 'DFFlagPhysicsMechanismCacheOptimizeAlloc': 'True', 'DFFlagDebugReportElevatedPhysicsFPSTOGA': 'False'}, 'tag': 'NET'}, {'name': 'Main FPS Boost', 'desc': '155 flags · Full FPS and telemetry optimization', 'flags': {'FStringGetPlayerImageDefaultTimeout': '1', 'FFlagFixSensitivityTextPrecision': 'False', 'DFIntMaxFrameBufferSize': '4', 'DFFlagDebugPerfMode': 'True', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'FFlagDebugDisableTelemetryPoint': 'True', 'DFFlagGraphicsQualityUsageTelemetry': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagSendRenderFidelityTelemetry': 'False', 'DFFlagReportRenderDistanceTelemetry': 'False', 'DFFlagSimSolverSendPerfTelemetryToElasticSearch2': 'False', 'DFFlagSimEnableBadMoverConstraintTelemetry': 'False', 'DFFlagCollectAudioPluginTelemetry': 'False', 'DFFlagEnableFmodErrorsTelemetry': 'False', 'DFFlagRccLoadSoundLengthTelemetryEnabled': 'False', 'DFFlagReportAssetRequestV1Telemetry': 'False', 'DFFlagRobloxTelemetryAddDeviceRAMPointsV2': 'False', 'DFFlagRemoveTelemetryFlushOnJobClose': 'False', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagEnableSkipUpdatingGlobalTelemetryInfo2': 'False', 'DFFlagEmitSafetyTelemetryInCallbackEnable': 'False', 'DFFlagRobloxTelemetryV2PointEncoding': 'False', 'DFFlagDSTelemetryV2ReplaceSeparator': 'False', 'FIntDebugForceMSAASamples': '1', 'FIntRenderShadowIntensity': '0', 'FFlagDisablePostFx': 'True', 'FIntDebugTextureManagerSkipMips': '2', 'FIntTerrainArraySliceSize': '0', 'FFlagDebugForceFutureIsBrightPhase2': 'True', 'DFIntTaskSchedulerTargetFps': '9999', 'FIntFontSizePadding': '2', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FIntRuntimeMaxNumOfMutexes': '1000000', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FLogNetwork': '7', 'DFFlagDisableDPIScale': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagChatTranslationSettingEnabled3': 'False', 'FFlagFasterPreciseTime4': 'True', 'DFIntAnimationLodFacsDistanceMin': '10', 'FFlagRenderNoLowFrmBloom': 'True', 'DFIntTextureQualityOverride': '0', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntJoinDataItemEstimatedCompressionRatioHundreths': '0', 'DFFlagSolverStateReplicatedOnly2': 'True', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FFlagLuaAppLegacyInputSettingRefactor': 'True', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntConnectionMTUSize': '900', 'FFlagVoiceBetaBadge': 'False', 'DFFlagClampIncomingReplicationLag': 'True', 'DFIntNetworkQualityResponderUnit': '10', 'FIntRuntimeMaxNumOfConditions': '1000000', 'FIntRobloxGuiBlurIntensity': '0', 'DFIntMaxProcessPacketsJobScaling': '10000', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FIntRuntimeMaxNumOfDPCs': '64', 'DFIntClusterCompressionLevel': '0', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'FIntGrassMovementReducedMotionFactor': '0', 'FFlagEnableZstdForClientSettings': 'False', 'DFIntClientPacketHealthyAllocationPercent': '20', 'DFIntTargetTimeDelayFacctorTenths': '10', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntRakNetApplicationFeedbackScaleUpFactorHundredthPercent': '0', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'DFIntCodecMaxIncomingPackets': '100', 'FIntRuntimeMaxNumOfSemaphores': '1000000', 'DFIntMaxReceiveToDeserializeLatencyMilliseconds': '10', 'DFIntClientPacketExcessMicroseconds': '1000', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FIntSimSolverResponsiveness': '2147483647', 'DFIntWaitOnRecvFromLoopEndedMS': '10', 'DFIntVoiceChatVolumeThousandths': '6000', 'DFIntRakNetSelectTimeoutMs': '1', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FIntRuntimeMaxNumOfSchedulers': '1000000', 'DFIntNetworkSchemaCompressionRatio': '0', 'DFIntClientNetworkInfluxHundredthsPercentage': '0', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntAnimationLodFacsVisibilityDenominator': '2', 'FFlagDebugCheckRenderThreading': 'True', 'FIntSmoothMouseSpringFrequencyTenths': '100', 'DFFlagRakNetEnablePoll': 'True', 'DFFlagReplicateCreateToPlayer': 'True', 'DFIntBufferCompressionLevel': '0', 'DFIntInitialAccelerationLatencyMultTenths': '1', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntS2PhysicsSenderRate': '64', 'DFIntClientPacketMaxDelayMs': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'DFIntNetworkQualityResponderMaxWaitTime': '1', 'DFIntAnimationLodFacsDistanceMax': '50', 'DFIntNetworkInProcessLimitGameplayMsClient': '0', 'DFIntCullFactorPixelThresholdShadowMapLowQuality': '2147483647', 'DFIntMaxDataPacketPerSend': '100000', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '2', 'FIntRenderShadowmapBias': '100', 'FFlagDebugGraphicsPreferD3D11': 'True', 'DFIntGameNetCompressionLodByteBudgetThresholdPct': '0', 'DFIntTextureCompositorActiveJobs': '0', 'DFIntMaxAcceptableUpdateDelay': '1', 'DFIntRakNetApplicationFeedbackScaleUpThresholdPercent': '0', 'FFlagLargeReplicatorEnabled2': 'True', 'DFFlagFacialAnimationStreaming2': 'False', 'DFIntRakNetNakResendDelayMs': '1', 'FFlagEnableInGameMenuDurationLogger': 'False', 'FIntTaskSchedulerThreadMin': '4', 'FFlagMessageBusCallOptimization': 'True', 'FIntActivatedCountTimerMSMouse': '300', 'FIntRenderLocalLightUpdatesMax': '2', 'FFlagFastGPULightCulling3': 'True', 'FFlagDebugRenderingSetDeterministic': 'True', 'FIntFRMMaxGrassDistance': '0', 'FIntActivatedCountTimerMSKeyboard': '300', 'FIntRenderLocalLightUpdatesMin': '6', 'FFlagPreloadAllFonts': 'True', 'FIntInterpolationMaxDelayMSec': '100', 'DFIntRakNetLoopMs': '1', 'FIntRenderGrassDetailStrands': '0', 'FIntRuntimeMaxNumOfLatches': '1000000', 'FFlagLargeReplicatorWrite2': 'True', 'FFlagDebugDisplayFPS': 'True', 'FFlagSortKeyOptimization': 'True', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagNewLightAttenuation': 'True', 'FFlagLargeReplicatorRead2': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'FIntRakNetResendBufferArrayLength': '128', 'FIntRuntimeMaxNumOfThreads': '1000000', 'FIntRomarkStartWithGraphicQualityLevel': '10', 'FIntInterpolationAwareTargetTimeLerpHundredth': '100', 'FFlagDebugDisableTelemetryV2Event': 'True', 'FIntFRMMinGrassDistance': '0', 'FIntRenderLocalLightFadeInMs': '0', 'FFlagPreComputeAcceleratorArrayForSharingTimeCurve': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'DFIntCullFactorPixelThresholdShadowMapHighQuality': '2147483647', 'FFlagDebugSkyGray': 'True', 'DFIntRakNetResendRttMultiple': '1', 'FIntDefaultJitterN': '0', 'DFIntBatchThumbnailResultsSizeCap': '200', 'DFFlagAcceleratorUpdateOnPropsAndValueTimeChange': 'True', 'DFIntClusterEstimatedCompressionRatioHundredths': '0', 'DFFlagMergeFakeInputEvents3': 'True', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntJoinDataCompressionLevel': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '3'}, 'tag': 'FPS'}, {'name': 'Blurred', 'desc': '84 flags · Smooth rendering and GPU optimized', 'flags': {'FFlagRobloxInputUsesRuntime2': 'True', 'FFlagLiveAnimationUpdateSupport': 'True', 'FFlagRealTimeAnimationEnableRefactor': 'True', 'DFFlagAnimatorAnywhere': 'True', 'DFFlagDebugForceAnisoOff': 'True', 'FIntRenderMsFrameGatherInterval': '60', 'FIntActivatedCountTimerMSKeyboard': '0', 'FIntActivatedCountTimerMSMouse': '0', 'FIntRenderNodeEnterSleepingFrames': '0', 'DFFlagAnimatorRetargetInterpolateFKCorrection': 'True', 'DFFlagSimHumanoidFirstPerson240hz': 'True', 'DFFlagSimSmoothedRunningController2': 'True', 'DFFlagSimStepPhysicsImprovedSubStepping': 'True', 'DFFlagPhysicsMechanismCacheOptimizeAlloc': 'True', 'DFFlagReplicatorSeparateVarThresholds': 'True', 'DFFlagTaskSchedulerRescheduleAsForeground': 'True', 'DFFlagEnableConcurrentHttpClientCacheReads': 'True', 'DFFlagProcess2DPipelineUseRuntimeThreading': 'True', 'DFFlagDisableDPIScale': 'True', 'DFFlagReduceCPUWhenBG': 'True', 'DFFlagAlwaysSkipDiskCache': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagAnimatorPostProcessIK': 'True', 'DFFlagFixSpecialMeshCulling': 'True', 'DFFlagReplicateCreateToPlayer': 'True', 'DFFlagRakNetUseSlidingWindow4': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagRenderEmitterOcclusionCulling': 'True', 'DFFlagRenderFastClusterOcclusionCulling': 'True', 'DFFlagRenderModelClusterOcclusionCulling': 'True', 'FFlagRenderTestEnableDistanceCulling': 'True', 'FFlagSmoothClusterOcclusionCulling2': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagPreloadTextureItemsOption4': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagRenderInitShadowmaps': 'True', 'FFlagQuaternionPoseCorrection': 'True', 'FFlagOptimizeCFrameUpdates4': 'True', 'FFlagOptimizeCFrameUpdatesIC4': 'True', 'FFlagCacheTextBoundsInGuiText': 'True', 'FFlagStyleCacheLessMemory2': 'True', 'FFlagReduceStyleCacheAllocations': 'True', 'FFlagAnimationLodIkEnabled': 'True', 'FFlagLargeReplicatorEnabled9': 'True', 'FFlagDebugDisplayFPS': 'True', 'FFlagDisablePostFx': 'True', 'FFlagDebugSkyGray': 'True', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagGraphicsEnableD3D10Compute': 'False', 'FFlagDebugGraphicsPreferVulkan': 'False', 'DFIntTaskSchedulerTargetFps': '10000', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntTextureQualityOverride': '0', 'DFIntMaxFrameBufferSize': '4', 'DFIntRakNetLoopMs': '1', 'DFIntRakNetSelectTimeoutMs': '1', 'DFIntRakNetNakResendDelayMs': '1', 'DFIntConnectionMTUSize': '900', 'DFIntNetworkSchemaCompressionRatio': '0', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntBufferCompressionLevel': '0', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FIntDebugForceMSAASamples': '1', 'FIntRenderShadowIntensity': '0', 'FIntTerrainArraySliceSize': '0', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntRenderGrassDetailStrands': '0', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FIntDefaultMeshCacheSizeMB': '256', 'FIntDebugTextureManagerSkipMips': '8', 'FIntRakNetResendBufferArrayLength': '256', 'FIntSmoothMouseSpringFrequencyTenths': '100', 'FIntInterpolationMaxDelayMSec': '100', 'FIntTaskSchedulerAutoThreadLimit': '6', 'FIntTaskSchedulerThreadMin': '1', 'FLogNetwork': '7'}, 'tag': 'PERF'}]



BUILTIN_PRESETS.append({
    'name': "Stoofs Potato V35",
    'desc': '40 flags · Minimum graphics, max perf',
    'flags': {
        'DFFlagDebugRenderForceTechnologyVoxel': 'True',
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'DFFlagTaskSchedulerAvoidSleep': 'True',
        'DFFlagDebugSkipMeshVoxelizer': 'True',
        'DFFlagEnableSoundPreloading': 'True',
        'DFFlagEnableMeshPreloading': 'True',
        'DFFlagDebugPauseVoxelizer': 'True',
        'DFFlagSimOptimizeSetSize': 'True',
        'DFFlagDebugPerfMode': 'True',
        'FFlagDebugForceFSMCPULightCulling': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagRenderGpuTextureCompressor': 'True',
        'FFlagDebugCheckRenderThreading': 'True',
        'FFlagDisablePostFx': 'True',
        'FFlagFineGrainCull': 'True',
        'FFlagDebugSkyGray': 'True',
        'FFlagResetCacheOnLeaveGame': 'True',
        'FFlagAssetPreloadingIXP': 'True',
        'FFlagRenderCBRefactor2': 'True',
        'DFIntCSGLevelOfDetailSwitchingDistance': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0',
        'DFIntAnimationLodFacsVisibilityDenominator': '0',
        'DFIntAnimationLodFacsDistanceMax': '0',
        'DFIntAnimationLodFacsDistanceMin': '0',
        'DFIntTextureQualityOverride': '0',
        'DFIntDebugFRMQualityLevelOverride': '1',
        'DFIntVideoMaxNumberOfVideosPlaying': '0',
        'DFIntMaxFrameBufferSize': '4',
        'DFIntS2PhysicsSenderRate': '128',
        'DFIntDataSenderRate': '128',
        'FIntDebugTextureManagerSkipMips': '10',
        'FIntGrassMovementReducedMotionFactor': '0',
        'FIntRenderGrassDetailStrands': '0',
        'FIntRenderShadowIntensity': '0',
        'FIntTerrainArraySliceSize': '0',
        'FIntRenderShadowmapBias': '-1',
        'FIntFRMMaxGrassDistance': '0',
        'FIntFRMMinGrassDistance': '0',
    },
    'tag': 'PERF',
})

BUILTIN_PRESETS.append({
    'name': "Stoofs Low V35",
    'desc': '35 flags · Low graphics balanced',
    'flags': {
        'DFFlagDebugRenderForceTechnologyVoxel': 'True',
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'DFFlagTaskSchedulerAvoidSleep': 'True',
        'DFFlagDebugSkipMeshVoxelizer': 'True',
        'DFFlagEnableSoundPreloading': 'True',
        'DFFlagEnableMeshPreloading': 'True',
        'DFFlagSimOptimizeSetSize': 'True',
        'DFFlagDebugPerfMode': 'True',
        'FFlagDebugForceFSMCPULightCulling': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagRenderGpuTextureCompressor': 'True',
        'FFlagNewLightAttenuation': 'True',
        'FFlagDisablePostFx': 'True',
        'FFlagFineGrainCull': 'True',
        'FFlagResetCacheOnLeaveGame': 'True',
        'FFlagAssetPreloadingIXP': 'True',
        'FFlagRenderCBRefactor2': 'True',
        'DFIntCSGLevelOfDetailSwitchingDistance': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0',
        'DFIntAnimationLodFacsVisibilityDenominator': '0',
        'DFIntAnimationLodFacsDistanceMax': '0',
        'DFIntAnimationLodFacsDistanceMin': '0',
        'DFIntTextureQualityOverride': '2',
        'DFIntDebugFRMQualityLevelOverride': '1',
        'DFIntMaxFrameBufferSize': '4',
        'DFIntS2PhysicsSenderRate': '128',
        'FIntGrassMovementReducedMotionFactor': '0',
        'FIntRenderGrassDetailStrands': '0',
        'FIntRenderShadowIntensity': '0',
        'FIntTerrainArraySliceSize': '0',
        'FIntRenderShadowmapBias': '-1',
        'FIntFRMMaxGrassDistance': '0',
        'FIntFRMMinGrassDistance': '0',
    },
    'tag': 'PERF',
})

BUILTIN_PRESETS.append({
    'name': "Stoofs Balanced V35",
    'desc': '28 flags · Balanced graphics and perf',
    'flags': {
        'DFFlagTaskSchedulerAvoidSleep': 'True',
        'DFFlagEnableSoundPreloading': 'True',
        'DFFlagEnableMeshPreloading': 'True',
        'DFFlagSimOptimizeSetSize': 'True',
        'DFFlagDebugPerfMode': 'True',
        'FFlagDebugForceFSMCPULightCulling': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagRenderGpuTextureCompressor': 'True',
        'FFlagDisablePostFx': 'True',
        'FFlagFineGrainCull': 'True',
        'FFlagResetCacheOnLeaveGame': 'True',
        'FFlagAssetPreloadingIXP': 'True',
        'FFlagRenderCBRefactor2': 'True',
        'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0',
        'DFIntAnimationLodFacsVisibilityDenominator': '0',
        'DFIntAnimationLodFacsDistanceMax': '0',
        'DFIntAnimationLodFacsDistanceMin': '0',
        'DFIntMaxFrameBufferSize': '4',
        'DFIntS2PhysicsSenderRate': '128',
        'DFIntDataSenderRate': '128',
        'FIntRenderMeshOptimizeVertexBuffer': '1',
        'FIntRenderShadowIntensity': '0',
        'FIntCameraMaxZoomDistance': '2147483647',
    },
    'tag': 'PERF',
})

BUILTIN_PRESETS.append({
    'name': "Stoofs High V35",
    'desc': '30 flags · High quality graphics',
    'flags': {
        'DFFlagTaskSchedulerAvoidSleep': 'True',
        'DFFlagDebugOverrideDPIScale': 'True',
        'DFFlagEnableSoundPreloading': 'True',
        'DFFlagEnableMeshPreloading': 'True',
        'DFFlagSimOptimizeSetSize': 'True',
        'DFFlagDisableDPIScale': 'True',
        'DFFlagDebugPerfMode': 'True',
        'FFlagDebugForceFSMCPULightCulling': 'True',
        'FFlagDebugGraphicsPreferD3D11': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagDebugSSAOForce': 'True',
        'FFlagFineGrainCull': 'True',
        'FFlagResetCacheOnLeaveGame': 'True',
        'FFlagAssetPreloadingIXP': 'True',
        'FFlagRenderCBRefactor2': 'True',
        'FFlagRenderInitShadowmaps': 'True',
        'DFIntAnimationLodFacsVisibilityDenominator': '0',
        'DFIntAnimationLodFacsDistanceMax': '0',
        'DFIntAnimationLodFacsDistanceMin': '0',
        'DFIntMaxFrameBufferSize': '4',
        'DFIntS2PhysicsSenderRate': '128',
        'FIntDebugFRMOptionalMSAALevelOverride': '2',
        'FIntDebugForceMSAASamples': '2',
        'FIntCameraMaxZoomDistance': '2147483647',
        'FIntTaskSchedulerAutoThreadLimit': '3',
    },
    'tag': 'PERF',
})

BUILTIN_PRESETS.append({
    'name': "Stoofs Ultra V35",
    'desc': '32 flags · Maximum quality graphics',
    'flags': {
        'DFFlagRenderLanczosUpsamplingNonRinging2': 'True',
        'DFFlagRenderSmootherStepUpsampling2': 'True',
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'DFFlagEnableTexturePreloading': 'True',
        'DFFlagTaskSchedulerAvoidSleep': 'True',
        'DFFlagDebugOverrideDPIScale': 'True',
        'DFFlagEnableSoundPreloading': 'True',
        'DFFlagEnableMeshPreloading': 'True',
        'DFFlagSimOptimizeSetSize': 'True',
        'DFFlagDisableDPIScale': 'True',
        'DFFlagDebugPerfMode': 'True',
        'FFlagDebugApplyHSRForTransparentMesh': 'True',
        'FFlagDebugForceFutureIsBrightPhase3': 'True',
        'FFlagDebugGridForceFractalUpsample': 'True',
        'FFlagDebugForceFSMCPULightCulling': 'True',
        'FFlagDebugGraphicsPreferD3D11': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagRenderInitShadowmaps': 'True',
        'FFlagResetCacheOnLeaveGame': 'True',
        'FFlagAssetPreloadingIXP': 'True',
        'FFlagRenderCBRefactor2': 'True',
        'DFIntTextureQualityOverride': '0',
        'DFIntMaxFrameBufferSize': '4',
        'DFIntS2PhysicsSenderRate': '128',
        'FIntDebugForceMSAASamples': '4',
        'FIntSSAOMipLevels': '8',
        'FIntTaskSchedulerAutoThreadLimit': '3',
        'FIntCameraMaxZoomDistance': '2147483647',
    },
    'tag': 'PERF',
})


BUILTIN_PRESETS.append({
    'name': "HasnBOT 0-Delay",
    'desc': '35 flags · HasnBOT best competitive config',
    'flags': {
        'FFlagHandleAltEnterFullscreenManually': 'False',
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'DFFlagDisableDPIScale': 'True',
        'DFFlagDebugRenderForceTechnologyVoxel': 'True',
        'DFFlagDebugPerfMode': 'True',
        'DFFlagDebugPauseVoxelizer': 'True',
        'FFlagDebugGraphicsPreferD3D11': 'True',
        'FFlagNewLightAttenuation': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagDisablePostFx': 'True',
        'FFlagRenderGpuTextureCompressor': 'True',
        'FFlagPreloadTextureItemsOption4': 'True',
        'FFlagPreloadAllFonts': 'True',
        'FFlagPreloadMinimalFonts': 'True',
        'FFlagDontCreatePingJob': 'True',
        'FFlagCommitToGraphicsQualityFix': 'True',
        'FFlagLightgridCPUAsyncUpdate': 'True',
        'FFlagNullCheckCloudsRendering': 'True',
        'FFlagGlobalWindRendering': 'False',
        'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False',
        'FFlagCloudsReflectOnWater': 'False',
        'FFlagTopBarUseNewBadge': 'False',
        'FFlagAdServiceEnabled': 'False',
        'FFlagVoiceBetaBadge': 'False',
        'DFIntCSGLevelOfDetailSwitchingDistance': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0',
        'DFIntDebugFRMQualityLevelOverride': '1',
        'DFIntTextureQualityOverride': '0',
        'DFIntConnectionMTUSize': '1380',
        'FIntDebugTextureManagerSkipMips': '3',
        'FIntRenderGrassDetailStrands': '0',
        'FIntRenderShadowIntensity': '0',
        'FIntCameraMaxZoomDistance': '99999',
    },
    'tag': 'USR',
})

BUILTIN_PRESETS.append({
    'name': "Sinawys Config",
    'desc': '38 flags · Sinawys competitive setup',
    'flags': {
        'DFFlagDebugRenderForceTechnologyVoxel': 'True',
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'DFFlagVoxelizerDisableTerrainSIMD': 'True',
        'DFFlagRakNetUseSlidingWindow4': 'True',
        'DFFlagDisableDPIScale': 'True',
        'DFFlagPredictedOOM': 'False',
        'DFFlagDebugPerfMode': 'True',
        'DFFlagDebugPauseVoxelizer': 'True',
        'FFlagDebugForceFutureIsBrightPhase3': 'True',
        'FFlagDebugGraphicsPreferD3D11': 'True',
        'FFlagPreloadTextureItemsOption4': 'True',
        'FFlagGraphicsEnableD3D10Compute': 'True',
        'FFlagRenderGpuTextureCompressor': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagNewLightAttenuation': 'True',
        'FFlagPreloadMinimalFonts': 'True',
        'FFlagAdServiceEnabled': 'False',
        'FFlagVoiceBetaBadge': 'False',
        'FFlagPreloadAllFonts': 'True',
        'FFlagDisablePostFx': 'True',
        'FFlagDebugSkyGray': 'True',
        'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False',
        'FFlagHandleAltEnterFullscreenManually': 'False',
        'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000',
        'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10',
        'DFIntAnimationLodFacsVisibilityDenominator': '0',
        'DFIntRaknetBandwidthPingSendEveryXSeconds': '1',
        'DFIntCSGLevelOfDetailSwitchingDistance': '1',
        'DFIntDebugFRMQualityLevelOverride': '1',
        'DFIntTextureQualityOverride': '0',
        'DFIntRakNetNakResendDelayMs': '10',
        'DFIntRakNetResendRttMultiple': '1',
        'DFIntS2PhysicsSenderRate': '100',
        'DFIntConnectionMTUSize': '900',
        'DFIntMaxFrameBufferSize': '6',
        'DFIntRakNetLoopMs': '1',
        'FIntDebugTextureManagerSkipMips': '3',
        'FIntRenderShadowIntensity': '0',
    },
    'tag': 'USR',
})

BUILTIN_PRESETS.append({
    'name': "Himitsu FFLags 2",
    'desc': '42 flags · Himitsu optimized config',
    'flags': {
        'DFFlagDebugPauseVoxelizer': 'True',
        'DFFlagDebugPhysicsSenderDoesNotShrinkSimRadius': 'True',
        'DFFlagDebugRenderForceTechnologyVoxel': 'True',
        'DFFlagDebugSkipMeshVoxelizer': 'True',
        'DFFlagEnableMeshPreloading2': 'True',
        'DFFlagEnableSoundPreloading': 'True',
        'DFFlagFastEndUpdateLoop': 'True',
        'DFFlagRakNetEnablePoll': 'True',
        'DFFlagSimOptimizeSetSize': 'True',
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'FFlagDebugCheckRenderThreading': 'True',
        'FFlagDebugDisplayFPS': 'True',
        'FFlagDebugGraphicsPreferD3D11FL10': 'True',
        'FFlagDebugRenderingSetDeterministic': 'True',
        'FFlagDebugSSAOForce': 'True',
        'FFlagDisablePostFx': 'True',
        'FFlagEnableVisBugChecks27': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagGraphicsEnableD3D10Compute': 'True',
        'FFlagHighlightOutlinesOnMobile': 'True',
        'FFlagRenderDebugCheckThreading2': 'True',
        'FFlagRenderEnableGlobalInstancingD3D10': 'True',
        'FFlagRenderLegacyShadowsQualityRefactor': 'True',
        'FFlagRenderShadowSkipHugeCulling': 'True',
        'FFlagRenderSkipReadingShaderData': 'True',
        'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False',
        'FFlagHandleAltEnterFullscreenManually': 'False',
        'FFlagGameBasicSettingsFramerateCap5': 'False',
        'DFIntCSGLevelOfDetailSwitchingDistance': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0',
        'DFIntTaskSchedulerTargetFps': '9999',
        'DFIntRakNetLoopMs': '1',
        'DFIntRakNetNakResendDelayMs': '1',
        'DFIntRakNetNakResendDelayMsMax': '1',
        'DFIntS2PhysicsSenderRate': '250',
        'DFIntTextureQualityOverride': '1',
        'FIntDebugTextureManagerSkipMips': '3',
        'FIntRenderLocalLightUpdatesMin': '6',
        'FIntRenderLocalLightUpdatesMax': '8',
        'FIntTaskSchedulerThreadMin': '10',
    },
    'tag': 'USR',
})

BUILTIN_PRESETS.append({
    'name': "EggusPrime Config",
    'desc': '30 flags · EggusPrime smooth setup',
    'flags': {
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'DFFlagDebugRenderForceTechnologyVoxel': 'True',
        'DFFlagDebugPauseVoxelizer': 'True',
        'DFFlagDisableDPIScale': 'True',
        'DFFlagDebugPerfMode': 'True',
        'DFFlagESGamePerfMonitorEnabled': 'False',
        'FFlagHandleAltEnterFullscreenManually': 'False',
        'FFlagDebugGraphicsPreferD3D11': 'True',
        'FFlagDebugGraphicsPreferD3D11FL10': 'True',
        'FFlagDebugGraphicsPreferVulkan': 'True',
        'FFlagNewLightAttenuation': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagOptimizeNetwork': 'True',
        'FFlagOptimizeNetworkRouting': 'True',
        'FFlagOptimizeNetworkTransport': 'True',
        'FFlagOptimizeServerTickRate': 'True',
        'FFlagPreloadAllFonts': 'True',
        'FFlagAdServiceEnabled': 'False',
        'FFlagFixGraphicsQuality': 'True',
        'FFlagCommitToGraphicsQualityFix': 'True',
        'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False',
        'DFIntTaskSchedulerTargetFps': '9999',
        'DFIntCSGLevelOfDetailSwitchingDistance': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0',
        'DFIntTextureQualityOverride': '0',
        'DFIntDebugFRMQualityLevelOverride': '1',
        'DFIntS2PhysicsSenderRate': '100',
        'FIntDebugTextureManagerSkipMips': '100000000',
    },
    'tag': 'USR',
})

BUILTIN_PRESETS.append({
    'name': "KJ Fflags",
    'desc': '18 flags · KJ competitive minimal',
    'flags': {
        'DFFlagDebugPauseVoxelizer': 'True',
        'FFlagGraphicsEnableD3D10Compute': 'True',
        'FFlagDebugGraphicsPreferD3D11FL10': 'True',
        'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False',
        'FFlagDebugGraphicsPreferD3D11': 'False',
        'FFlagDebugForceFSMCPULightCulling': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'DFIntRemoteEventSingleInvocationSizeLimit': '2900',
        'DFIntCSGLevelOfDetailSwitchingDistance': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0',
        'DFIntDebugFRMQualityLevelOverride': '1',
        'DFIntTextureQualityOverride': '1',
        'DFIntPerformanceControlTextureQualityBestUtility': '-1',
        'FIntRenderShadowmapBias': '0',
        'FIntRenderLocalLightUpdatesMin': '0',
        'FIntRenderLocalLightUpdatesMax': '0',
    },
    'tag': 'USR',
})

BUILTIN_PRESETS.append({
    'name': "Brampa Flags 2",
    'desc': '28 flags · Brampa performance config',
    'flags': {
        'DFFlagEnableSoundPreloading': 'True',
        'DFFlagEnableMeshPreloading2': 'True',
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'DFFlagTeleportClientAssetPreloadingEnabledIXP': 'True',
        'DFFlagTeleportClientAssetPreloadingDoingExperiment': 'True',
        'DFFlagTeleportClientAssetPreloadingDoingExperiment2': 'True',
        'DFFlagSimOptimizeSetSize': 'True',
        'DFFlagDebugSkipMeshVoxelizer': 'True',
        'DFFlagDebugPerfMode': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagRenderLegacyShadowsQualityRefactor': 'True',
        'FFlagNewLightAttenuation': 'True',
        'FFlagAssetPreloadingIXP': 'True',
        'FFlagEnableAudioPannerFiltering': 'True',
        'FFlagDebugForceFSMCPULightCulling': 'True',
        'FFlagUserHideCharacterParticlesInFirstPerson': 'True',
        'FFlagImproveShiftLockTransition': 'True',
        'FFlagMessageBusCallOptimization': 'True',
        'FFlagUserShowGuiHideToggles': 'True',
        'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False',
        'FFlagHandleAltEnterFullscreenManually': 'False',
        'FFlagVoiceBetaBadge': 'False',
        'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0',
        'DFIntDebugFRMQualityLevelOverride': '1',
        'DFIntTextureQualityOverride': '0',
        'DFIntPerformanceControlTextureQualityBestUtility': '-1',
        'FIntDebugTextureManagerSkipMips': '8',
    },
    'tag': 'USR',
})

BUILTIN_PRESETS.append({
    'name': "Aizen No Animations",
    'desc': '26 flags · Aizen config, animations disabled',
    'flags': {
        'DFFlagDebugPauseVoxelizer': 'True',
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'FFlagDebugGraphicsPreferD3D11': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagNewLightAttenuation': 'True',
        'FFlagOptimizeNetwork': 'True',
        'FFlagOptimizeNetworkRouting': 'True',
        'FFlagOptimizeNetworkTransport': 'True',
        'FFlagOptimizeServerTickRate': 'True',
        'FFlagDisablePostFx': 'True',
        'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False',
        'FFlagGameBasicSettingsFramerateCap2': 'True',
        'DFIntCSGLevelOfDetailSwitchingDistance': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0',
        'DFIntTextureQualityOverride': '0',
        'DFIntDebugFRMQualityLevelOverride': '1',
        'DFIntConnectionMTUSize': '900',
        'DFIntRakNetLoopMs': '1',
        'DFIntMaxActiveAnimationTracks': '1',
        'DFIntAnimationRateLimiterMaxAmount': '0',
        'FFlagAnimationLodBoneEnabled': 'False',
        'FFlagAnimationLodIkEnabled': 'False',
        'DFIntAnimationLodConfigVersion': '999',
        'DFIntAnimationLodBoneLocomotionFixMaxDepth': '0',
    },
    'tag': 'USR',
})

BUILTIN_PRESETS.append({
    'name': "Spec Fast Flags",
    'desc': '30 flags · Spec competitive config',
    'flags': {
        'DFFlagDebugRenderForceTechnologyVoxel': 'True',
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'DFFlagESGamePerfMonitorEnabled': 'False',
        'DFFlagDebugPauseVoxelizer': 'True',
        'DFFlagDisableDPIScale': 'True',
        'DFFlagDebugPerfMode': 'True',
        'FFlagDebugGraphicsPreferD3D11': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagPreloadTextureItemsOption4': 'True',
        'FFlagRenderGpuTextureCompressor': 'True',
        'FFlagNewLightAttenuation': 'True',
        'FFlagPreloadAllFonts': 'True',
        'FFlagPreloadMinimalFonts': 'True',
        'FFlagDisablePostFx': 'True',
        'FFlagDontCreatePingJob': 'True',
        'FFlagCommitToGraphicsQualityFix': 'True',
        'FFlagLightgridCPUAsyncUpdate': 'True',
        'FFlagNullCheckCloudsRendering': 'True',
        'FFlagGlobalWindRendering': 'False',
        'FFlagAdServiceEnabled': 'False',
        'FFlagVoiceBetaBadge': 'False',
        'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False',
        'FFlagHandleAltEnterFullscreenManually': 'False',
        'DFIntCSGLevelOfDetailSwitchingDistance': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0',
        'DFIntDebugFRMQualityLevelOverride': '1',
        'DFIntTaskSchedulerTargetFps': '9999',
        'DFIntTextureQualityOverride': '0',
    },
    'tag': 'USR',
})


BUILTIN_PRESETS.append({
    'name': "BF FPS Boost Pack",
    'desc': '30 flags · Blox Fruits FPS optimizer',
    'flags': {
        'DFFlagDebugRenderForceTechnologyVoxel': 'True',
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'DFFlagVoxelizerDisableTerrainSIMD': 'True',
        'DFFlagRakNetUseSlidingWindow4': 'True',
        'DFFlagDebugPauseVoxelizer': 'True',
        'DFFlagDisableDPIScale': 'True',
        'DFFlagDebugPerfMode': 'True',
        'DFFlagTaskSchedulerAvoidSleep': 'True',
        'FFlagDebugGraphicsPreferD3D11': 'True',
        'FFlagFastGPULightCulling3': 'True',
        'FFlagPreloadAllFonts': 'True',
        'FFlagPreloadMinimalFonts': 'True',
        'FFlagDisablePostFx': 'True',
        'FFlagNewLightAttenuation': 'True',
        'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False',
        'FFlagHandleAltEnterFullscreenManually': 'False',
        'DFIntCSGLevelOfDetailSwitchingDistance': '1',
        'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0',
        'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0',
        'DFIntDebugFRMQualityLevelOverride': '1',
        'DFIntRakNetNakResendDelayMs': '10',
        'DFIntRakNetNakResendDelayRttPercent': '50',
        'DFIntRakNetResendRttMultiple': '1',
        'DFIntS2PhysicsSenderRate': '100',
        'DFIntConnectionMTUSize': '900',
        'DFIntMaxFrameBufferSize': '6',
        'DFIntRakNetLoopMs': '1',
        'FIntDebugTextureManagerSkipMips': '3',
        'FIntRenderShadowIntensity': '0',
    },
    'tag': 'FPS',
})

BUILTIN_PRESETS.append({
    'name': "Lower Ping BF",
    'desc': '15 flags · Network ping reduction',
    'flags': {
        'FFlagOptimizeNetwork': 'True',
        'FFlagOptimizeNetworkRouting': 'True',
        'FFlagOptimizeNetworkTransport': 'True',
        'FFlagOptimizeServerTickRate': 'True',
        'DFIntConnectionMTUSize': '900',
        'FIntRakNetResendBufferArrayLength': '128',
        'DFIntServerPhysicsUpdateRate': '60',
        'DFIntServerTickRate': '60',
        'DFIntRakNetResendRttMultiple': '1',
        'DFIntRaknetBandwidthPingSendEveryXSeconds': '1',
        'DFIntOptimizePingThreshold': '50',
        'DFIntPlayerNetworkUpdateQueueSize': '20',
        'DFIntPlayerNetworkUpdateRate': '60',
        'DFIntNetworkPrediction': '120',
        'DFIntNetworkLatencyTolerance': '1',
    },
    'tag': 'NET',
})

BUILTIN_PRESETS.append({
    'name': "UltraPing Stability",
    'desc': '20 flags · Ultra stable ping config',
    'flags': {
        'DFIntBandwidthManagerApplicationDefaultBps': '1024000',
        'DFIntBandwidthManagerDataSenderMaxWorkCatchupMs': '8',
        'DFFlagAlwaysSkipDiskCache': 'False',
        'DFFlagRakNetEnablePoll': 'True',
        'DFFlagSampleAndRefreshRakPing': 'True',
        'FFlagSpecifyNetworkReplicatorScope': 'True',
        'FFlagSpecifyNetworkReplicatorScopeForItems': 'True',
        'DFIntClientPacketExcessMicroseconds': '1000',
        'DFIntClientPacketHealthyAllocationPercent': '20',
        'DFIntClientPacketMaxDelayMs': '1',
        'DFIntClientPacketMaxFrameMicroseconds': '200',
        'DFIntLargePacketQueueSizeCutoffMB': '1000',
        'DFIntMaxProcessPacketsJobScaling': '5000000',
        'DFIntMaxProcessPacketsStepsAccumulated': '5',
        'DFIntMaxProcessPacketsStepsPerCyclic': '5000',
        'DFIntMaxWaitTimeBeforeForcePacketProcessMS': '1',
        'DFIntRakNetLoopMs': '1',
        'DFIntRakNetNakResendDelayMs': '1',
        'DFIntRakNetResendRttMultiple': '1',
        'DFIntRakNetSelectTimeoutMs': '1',
    },
    'tag': 'NET',
})


BUILTIN_PRESETS.append({
    'name': "Disable Telemetry",
    'desc': '15 flags · Kill all telemetry and tracking',
    'flags': {
        'FFlagDebugDisableTelemetryEphemeralCounter': 'True',
        'FFlagDebugDisableTelemetryEphemeralStat': 'True',
        'FFlagDebugDisableTelemetryEventIngest': 'True',
        'FFlagDebugDisableTelemetryV2Counter': 'True',
        'FFlagDebugDisableTelemetryV2Event': 'True',
        'FFlagDebugDisableTelemetryV2Stat': 'True',
        'FFlagDebugDisableTelemetryPoint': 'True',
        'DFFlagBrowserTrackerIdTelemetryEnabled': 'False',
        'DFFlagGpuVsCpuBoundTelemetry': 'False',
        'DFFlagGraphicsQualityUsageTelemetry': 'False',
        'DFFlagRobloxTelemetryAddDeviceRAMPointsV2': 'False',
        'DFFlagEnableTelemetryV2FRMStats': 'False',
        'DFFlagCollectAudioPluginTelemetry': 'False',
        'DFFlagWindowsWebViewTelemetryEnabled': 'False',
        'DFFlagReportAssetRequestV1Telemetry': 'False',
    },
    'tag': 'PERF',
})

BUILTIN_PRESETS.append({
    'name': "Exclusive Fullscreen",
    'desc': '1 flag · Enable true fullscreen mode',
    'flags': {
        'FFlagHandleAltEnterFullscreenManually': 'False',
    },
    'tag': 'CFG',
})

BUILTIN_PRESETS.append({
    'name': "No Animations (New)",
    'desc': '3 flags · Disable all animations newest method',
    'flags': {
        'DFIntMaxActiveAnimationTracks': '0',
        'DFIntReplicatorAnimationTrackLimitPerAnimator': '-1',
        'DFIntAnimatorThrottleMaxFramesToSkip': '9999',
    },
    'tag': 'PERF',
})

BUILTIN_PRESETS.append({
    'name': "Reduce Screenshake",
    'desc': '4 flags · Minimizes camera shake effects',
    'flags': {
        'FFlagDisableCameraShake': 'True',
        'FFlagDisableScreenShake': 'True',
        'FFlagPreferNoAnimation': 'True',
        'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '1',
    },
    'tag': 'FUN',
})

BUILTIN_PRESETS.append({
    'name': "High Render Distance",
    'desc': '2 flags · High render dist, low texture',
    'flags': {
        'DFFlagTextureQualityOverrideEnabled': 'True',
        'DFIntTextureQualityOverride': '3',
    },
    'tag': 'FUN',
})

BUILTIN_PRESETS.append({
    'name': "No Lava + Skybox",
    'desc': '2 flags · Remove lava damage + skybox',
    'flags': {
        'FIntDebugTextureManagerSkipMips': '10',
        'DFIntTouchSenderMaxBandwidthBps': '-1',
    },
    'tag': 'FUN',
})

BUILTIN_PRESETS.append({
    'name': "21 Graphics Bars",
    'desc': '1 flag · Unlocks extra graphics quality bars',
    'flags': {
        'FFlagFixGraphicsQuality': 'True',
    },
    'tag': 'CFG',
})


BUILTIN_PRESETS += [
    {
        'name': 'Insane FPS Boost',
        'desc': '42 flags · Maximum FPS, GPU optimized, telemetry off',
        'tag': 'FPS',
        'flags': {
            'DFIntTaskSchedulerTargetFps':              '9999999',
            'FFlagTaskSchedulerLimitTargetFpsTo2402':   'False',
            'FFlagDebugDisplayFPS':                     'True',
            'FFlagDebugGraphicsPreferD3D11':            'True',
            'FFlagFastGPULightCulling3':                'True',
            'FFlagRenderGpuTextureCompressor':          'True',
            'FFlagPreloadTextureItemsOption4':          'True',
            'FFlagGraphicsEnableD3D10Compute':          'True',
            'FFlagNewLightAttenuation':                 'True',
            'FFlagDebugForceFSMCPULightCulling':        'True',
            'FFlagLightgridCPUAsyncUpdate':             'True',
            'FFlagRenderInitShadowmaps':                'False',
            'FFlagDisablePostFx':                       'True',
            'FFlagDebugSkyGray':                        'True',
            'FFlagGlobalWindRendering':                 'False',
            'FFlagCloudsReflectOnWater':                'False',
            'FFlagNullCheckCloudsRendering':            'True',
            'DFFlagTextureQualityOverrideEnabled':      'True',
            'DFIntTextureQualityOverride':              '0',
            'DFIntTextureCompositorActiveJobs':         '0',
            'DFIntDebugLimitMinTextureResolutionWhenSkipMips': '9999999',
            'DFIntDebugTextureManagerSkipMips':         '10',
            'FIntDebugTextureManagerSkipMips':          '8',
            'FIntDebugForceMSAASamples':                '0',
            'FIntRenderShadowIntensity':                '0',
            'FIntRenderShadowmapBias':                  '0',
            'FIntTerrainArraySliceSize':                '0',
            'FIntFRMMaxGrassDistance':                  '0',
            'FIntFRMMinGrassDistance':                  '0',
            'FIntRenderGrassDetailStrands':             '0',
            'FIntRobloxGuiBlurIntensity':               '0',
            'DFIntCSGLevelOfDetailSwitchingDistance':   '0',
            'DFIntCSGLevelOfDetailSwitchingDistanceL12':'0',
            'DFIntCSGLevelOfDetailSwitchingDistanceL23':'0',
            'DFIntCSGLevelOfDetailSwitchingDistanceL34':'0',
            'DFIntAnimationLodFacsVisibilityDenominator':'0',
            'DFIntAnimationLodFacsDistanceMax':         '0',
            'DFIntAnimationLodFacsDistanceMin':         '0',
            'FFlagDebugDisableTelemetryEphemeralCounter':'True',
            'FFlagDebugDisableTelemetryEphemeralStat':  'True',
            'FFlagDebugDisableTelemetryEventIngest':    'True',
            'FFlagDebugDisableTelemetryPoint':          'True',
            'DFFlagDisableDPIScale':                    'True',
            'FFlagHandleAltEnterFullscreenManually':    'False',
            'FIntFullscreenTitleBarTriggerDelayMillis': '3600000',
        },
    },
    {
        'name': 'Best Ping Reduce',
        'desc': '28 flags · Minimum latency, max packet throughput',
        'tag': 'NET',
        'flags': {
            'DFIntRakNetLoopMs':                        '1',
            'DFIntRakNetSelectTimeoutMs':               '1',
            'DFIntRakNetNakResendDelayMs':              '1',
            'DFIntRakNetNakResendDelayMsMax':           '1',
            'DFIntRakNetResendRttMultiple':             '1',
            'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100',
            'DFIntRaknetBandwidthInfluxHundredthsPercentageV2':  '10000',
            'DFIntRaknetBandwidthPingSendEveryXSeconds': '1',
            'DFIntRakNetApplicationFeedbackScaleUpThresholdPercent': '0',
            'DFIntRakNetApplicationFeedbackScaleUpFactorHundredthPercent': '0',
            'FIntRakNetResendBufferArrayLength':        '128',
            'DFIntClientPacketMaxDelayMs':              '1',
            'DFIntClientPacketMaxFrameMicroseconds':    '200',
            'DFIntClientPacketExcessMicroseconds':      '1000',
            'DFIntClientPacketHealthyAllocationPercent':'20',
            'DFIntMaxReceiveToDeserializeLatencyMilliseconds': '10',
            'DFIntMaxProcessPacketsStepsPerCyclic':     '10000',
            'DFIntMaxProcessPacketsJobScaling':         '10000',
            'DFIntMaxProcessPacketsStepsAccumulated':   '0',
            'DFIntMaxDataPacketPerSend':                '2147483647',
            'DFIntCodecMaxOutgoingFrames':              '10000',
            'DFIntCodecMaxIncomingPackets':             '100',
            'DFIntBufferCompressionLevel':              '0',
            'DFIntBufferCompressionThreshold':          '100',
            'DFFlagRakNetEnablePoll':                   'True',
            'DFFlagRakNetUseSlidingWindow4':            'True',
            'DFFlagRakNetDetectRecvThreadOverload':     'True',
            'DFFlagReplicateCreateToPlayer':            'True',
            'DFIntS2PhysicsSenderRate':                 '35200',
            'DFIntPhysicsReceiveNumParallelTasks':      '20',
            'DFIntMegaReplicatorNumParallelTasks':      '20',
            'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10',
            'DFIntNetworkQualityResponderUnit':         '10',
            'DFIntNetworkQualityResponderMaxWaitTime':  '1',
            'DFIntNetworkSchemaCompressionRatio':       '0',
            'DFIntLargePacketQueueSizeCutoffMB':        '1000',
            'DFIntConnectingTimerInterval':             '10',
            'DFIntMaxAcceptableUpdateDelay':            '1',
            'FLogNetwork':                              '7',
        },
    },
    {
        'name': "Specflag'",
        'desc': '137 flags · Full specflag optimization config',
        'tag': 'CFG',
        'flags': {
            'CSGLevelOfDetailSwitchingDistanceL12':     '0',
            'CSGLevelOfDetailSwitchingDistanceL23':     '0',
            'CSGLevelOfDetailSwitchingDistanceL34':     '0',
            'CSGLevelOfDetailSwitchingDistance':        '0',
            'DebugLimitMinTextureResolutionWhenSkipMips':'9999999999999999',
            'DebugForceFSMCPULightCulling':             'True',
            'DebugTextureManagerSkipMips':              '10',
            'DFFlagDebugEnableInterpolationVisualizer': 'True',
            'DFFlagDebugRenderForceTechnologyVoxel':    'True',
            'DFFlagTextureQualityOverrideEnabled':      'True',
            'DFFlagESGamePerfMonitorEnabled':           'False',
            'DFFlagDebugPauseVoxelizer':                'True',
            'DFFlagDisableDPIScale':                    'True',
            'DFFlagDebugPerfMode':                      'True',
            'DFIntAnimationLodFacsVisibilityDenominator':'0',
            'DFIntCSGLevelOfDetailSwitchingDistanceL34':'0',
            'DFIntCSGLevelOfDetailSwitchingDistanceL23':'0',
            'DFIntCSGLevelOfDetailSwitchingDistanceL12':'0',
            'DFIntUserIdPlayerNameLifetimeSeconds':      '86400',
            'DFIntCSGLevelOfDetailSwitchingDistance':   '0',
            'DFIntDebugTextureManagerSkipMips':         '10',
            'DFIntDebugFRMQualityLevelOverride':        '1',
            'DFIntAnimationLodFacsDistanceMax':         '0',
            'DFIntAnimationLodFacsDistanceMin':         '0',
            'DFIntTextureCompositorActiveJobs':         '0',
            'DFIntTaskSchedulerTargetFps':              '9999',
            'DFIntCanHideGuiGroupId':                   '32380007',
            'DFIntTextureQualityOverride':              '0',
            'DisablePostFx':                            'True',
            'DoNotSkipMipsBasedOnSystemMemoryPS':       'True',
            'EnablePowerTraceModule':                   'True',
            'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'True',
            'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2':   'True',
            'FFlagEnableAccessibilitySettingsInExperienceMenu2':        'True',
            'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False',
            'FFlagDebugDisableTelemetryEphemeralCounter':   'True',
            'FFlagGraphicsGLEnableHQShadersExclusion':  'False',
            'FFlagGraphicsSettingsOnlyShowValidModes':  'True',
            'FFlagEnableReportAbuseMenuRoactABTest2':   'False',
            'FFlagDebugDisableTelemetryEphemeralStat':  'True',
            'FFlagHandleAltEnterFullscreenManually':    'False',
            'FFlagUserPreventOldBubbleChatOverlap':     'False',
            'FFlagEnableBubbleChatFromChatService':     'False',
            'FFlagEnableBubbleChatConfigurationV2':     'False',
            'FFlagEnableAccessibilitySettingsAPIV2':    'True',
            'FFlagDebugDisableTelemetryEventIngest':    'True',
            'FFlagBetaBadgeLearnMoreLinkFormview':      'False',
            'FFlagEnableReportAbuseMenuLayerOnV3':      'False',
            'FFlagEnableMenuModernizationABTest2':      'False',
            'FFlagInGameMenuV1FullScreenTitleBar':      'False',
            'FFlagChatTranslationSettingEnabled3':      'False',
            'FFlagEnableInGameMenuModernization':       'False',
            'FFlagEnableInGameMenuChromeABTest2':       'False',
            'FFlagEnableMenuModernizationABTest':       'False',
            'FFlagDebugDisableOTAMaterialTexture':      'True',
            'FFlagDebugDisableTelemetryV2Counter':      'True',
            'FFlagDisableChromeFollowupOcclusion':      'True',
            'FFlagEnableReportAbuseMenuRoact2':         'False',
            'FFlagDebugDisableTelemetryV2Event':        'True',
            'FFlagDebugForceFSMCPULightCulling':        'True',
            'FFlagRenderPerformanceTelemetry':          'False',
            'FFlagCoreGuiTypeSelfViewPresent':          'False',
            'FFlagDisableChromeFollowupUnibar':         'True',
            'FFlagDebugDisableTelemetryV2Stat':         'True',
            'FFlagCommitToGraphicsQualityFix':          'True',
            'FFlagPreloadTextureItemsOption4':          'True',
            'FFlagRenderGpuTextureCompressor':          'True',
            'FFlagEnableFavoriteButtonForUgc':          'True',
            'FFlagDebugDisableTelemetryPoint':          'True',
            'FFlagEnableBetaBadgeLearnMore':            'False',
            'FFlagEnableInGameMenuControls':            'False',
            'FFlagEnableMenuControlsABTest':            'False',
            'FFlagControlBetaBadgeWithGuac':            'False',
            'FFlagDisableChromeFollowupFTUX':           'True',
            'FFlagNullCheckCloudsRendering':            'True',
            'FFlagEnableNewInviteMenuIXP2':             'False',
            'FFlagEnableAudioOutputDevice':             'False',
            'FFlagDisableChromeDefaultOpen':            'True',
            'FFlagDebugGraphicsPreferD3D11':            'True',
            'FFlagLightgridCPUAsyncUpdate':             'True',
            'FFlagDisableChromePinnedChat':             'True',
            'FFlagEnableQuickGameLaunch':               'False',
            'FFlagCloudsReflectOnWater':                'False',
            'FFlagEnableV3MenuABTest3':                 'False',
            'FFlagFastGPULightCulling3':                'True',
            'FFlagRenderCheckThreading':                'True',
            'FFlagGlobalWindRendering':                 'False',
            'FFlagPreloadMinimalFonts':                 'True',
            'FFlagDisableChromeUnibar':                 'True',
            'FFlagNewLightAttenuation':                 'True',
            'FFlagTopBarUseNewBadge':                   'False',
            'FFlagFixGraphicsQuality':                  'True',
            'FFlagDontCreatePingJob':                   'True',
            'FFlagAdServiceEnabled':                    'False',
            'FFlagLuaAppSystemBar':                     'False',
            'FFlagPreloadAllFonts':                     'True',
            'FFlagVoiceBetaBadge':                      'False',
            'FFlagDisablePostFx':                       'True',
            'FFlagMSRefactor5':                         'False',
            'FIntFullscreenTitleBarTriggerDelayMillis': '3600000',
            'FIntMeshContentProviderForceCacheSize':    '268435456',
            'FIntHSRClusterSymmetryDistancePercent':    '10000',
            'FIntStartupInfluxHundredthsPercentage':    '0',
            'FIntUITextureMaxRenderTextureSize':        '1024',
            'FIntTerrainOTAMaxTextureSize':             '1024',
            'FIntDebugTextureManagerSkipMips':          '3',
            'FIntRenderLocalLightUpdatesMin':           '1',
            'FIntRenderLocalLightUpdatesMax':           '1',
            'FIntCameraMaxZoomDistance':                '99999',
            'FIntDefaultMeshCacheSizeMB':               '256',
            'FIntRenderGrassDetailStrands':             '0',
            'FIntReportDeviceInfoRollout':              '0',
            'FIntRenderGrassHeightScaler':              '0',
            'FIntRobloxGuiBlurIntensity':               '0',
            'FIntTerrainArraySliceSize':                '8',
            'FIntRenderShadowIntensity':                '0',
            'FIntDebugForceMSAASamples':                '0',
            'FIntRenderShadowmapBias':                  '0',
            'FIntFRMMaxGrassDistance':                  '0',
            'FIntFRMMinGrassDistance':                  '0',
            'FIntFontSizePadding':                      '3',
            'FLogNetwork':                              '7',
            'FStringVoiceBetaBadgeLearnMoreLink':       'null',
            'FStringTerrainMaterialTablePre2022':       '',
            'FStringTerrainMaterialTable2022':          '',
            'IncludePowerSaverMode':                    'True',
            'PerformanceControlTextureQualityBestUtility': '-1',
            'RenderUseTextureManager224':               'False',
            'RenderShadowmapBias':                      '75',
            'TaskSchedulerLimitTargetFpsTo2402':        'False',
            'TaskSchedulerTargetFps':                   '9999999',
            'TerrainArraySliceSize':                    '0',
            'TextureQualityOverrideEnabled':            'True',
            'TextureCompositorActiveJobs':              '0',
            'TextureQualityOverride':                   '0',
            'TM2SkipMipsForUnstreamable2':              'True',
        },
    },
    {
        'name': 'Sacred Performance',
        'desc': '158 flags · Sacred curated performance + network config',
        'tag': 'PERF',
        'flags': {
            'DebugLimitMinTextureResolutionWhenSkipMips': '2147483647',
            'DoNotSkipMipsBasedOnSystemMemoryPS': 'True',
            'TM2SkipMipsForUnstreamable2': 'True',
            'RenderUseTextureManager224': 'False',
            'DebugTextureManagerSkipMips': '3',
            'EnablePowerTraceModule': 'True',
            'IncludePowerSaverMode': 'True',
            'DebugFRMQualityLevelOverride': '1',
            'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4000',
            'DFIntTouchSenderMaxBandwidthBps': '-9999',
            'DFIntTaskSchedulerTargetFps': '9999',
            'DFIntCanHideGuiGroupId': '32380007',
            'DFIntTextureQualityOverride': '0',
            'FIntFullscreenTitleBarTriggerDelayMillis': '3600000',
            'FFlagDisablePostFx': 'True',
            'FFlagDebugGraphicsPreferD3D11': 'True',
            'FIntDebugForceMSAASamples': '1',
            'FIntRenderShadowIntensity': '0',
            'FIntTerrainArraySliceSize': '0',
            'FIntFontSizePadding': '5',
            'DFFlagDisableDPIScale': 'True',
            'DFFlagTextureQualityOverrideEnabled': 'True',
            'DFFlagDebugRenderForceTechnologyVoxel': 'True',
            'FFlagDebugForceFutureIsBrightPhase3': 'True',
            'FFlagDebugGraphicsPreferD3D11FL10': 'True',
            'FLogNetwork': '7',
            'FFlagHandleAltEnterFullscreenManually': 'False',
            'DFFlagSolverStateReplicatedOnly2': 'True',
            'DFFlagRakNetUseSlidingWindow4': 'True',
            'DFFlagRakNetCalculateApplicationFeedback2': 'True',
            'DFFlagReplicatorSeparateVarThresholds': 'True',
            'DFFlagTaskSchedulerAvoidSleep': 'True',
            'DFFlagReplicateCreateToPlayer': 'True',
            'DFFlagRakNetEnablePoll': 'True',
            'DFFlagRakNetDetectNetUnreachable': 'True',
            'DFFlagRakNetDetectRecvThreadOverload': 'True',
            'DFFlagEnableTexturePreloading': 'True',
            'FFlagEnableAnimatorSkipCopyPreviousRigKeyOnJointModification': 'True',
            'FFlagPreComputeAcceleratorArrayForSharingTimeCurve': 'True',
            'FFlagEnablePlayerViewBoundingBoxSizeDamping': 'True',
            'FFlagRenderEnableGlobalInstancingD3D10': 'True',
            'FFlagLuaAppLegacyInputSettingRefactor': 'True',
            'FFlagEnablePerformanceControlService': 'True',
            'FFlagDebugForceFSMCPULightCulling': 'True',
            'FFlagGraphicsEnableD3D10Compute': 'True',
            'FFlagPreloadTextureItemsOption4': 'True',
            'FFlagRenderGpuTextureCompressor': 'True',
            'FFlagFastGPULightCulling3': 'True',
            'FFlagUserShowGuiHideToggles': 'True',
            'FFlagDebugDisplayFPS': 'True',
            'FFlagEnableZstdDictionaryForClientSettings': 'False',
            'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False',
            'FFlagEnableZstdForClientSettings': 'False',
            'DFIntRakNetApplicationFeedbackScaleUpFactorHundredthPercent': '0',
            'DFIntRakNetApplicationFeedbackScaleUpThresholdPercent': '0',
            'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000',
            'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100',
            'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '25',
            'DFIntPerformanceControlTextureQualityBestUtility': '-1',
            'DFIntMaxReceiveToDeserializeLatencyMilliseconds': '10',
            'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10',
            'DFIntAnimationLodFacsVisibilityDenominator': '0',
            'DFIntClientPacketHealthyAllocationPercent': '20',
            'DFIntNetworkInProcessLimitGameplayMsClient': '0',
            'DFIntCSGLevelOfDetailSwitchingDistanceL12': '2',
            'DFIntCSGLevelOfDetailSwitchingDistanceL23': '3',
            'DFIntInitialAccelerationLatencyMultTenths': '1',
            'DFIntRaknetBandwidthPingSendEveryXSeconds': '1',
            'DFIntMaxProcessPacketsStepsPerCyclic': '10000',
            'DFIntClientPacketMaxFrameMicroseconds': '200',
            'DFIntNetworkQualityResponderMaxWaitTime': '1',
            'DFIntCSGLevelOfDetailSwitchingDistance': '1',
            'DFIntClientPacketExcessMicroseconds': '1000',
            'DFIntMaxProcessPacketsStepsAccumulated': '0',
            'DFIntLargePacketQueueSizeCutoffMB': '1000',
            'DFIntMaxProcessPacketsJobScaling': '10000',
            'DFIntMegaReplicatorNumParallelTasks': '20',
            'DFIntPhysicsReceiveNumParallelTasks': '20',
            'DFIntBatchThumbnailResultsSizeCap': '200',
            'DFIntPerformanceControlFrameTimeMax': '1',
            'DFIntMaxDataPacketPerSend': '2147483647',
            'DFIntBufferCompressionThreshold': '100',
            'DFIntDebugFRMQualityLevelOverride': '1',
            'DFIntNetworkQualityResponderUnit': '10',
            'DFIntAnimationLodFacsDistanceMax': '0',
            'DFIntAnimationLodFacsDistanceMin': '0',
            'DFIntRakNetNakResendDelayMsMax': '100',
            'DFIntCodecMaxOutgoingFrames': '10000',
            'DFIntCodecMaxIncomingPackets': '100',
            'DFIntConnectingTimerInterval': '10',
            'DFIntMaxAcceptableUpdateDelay': '1',
            'DFIntRakNetResendRttMultiple': '1',
            'DFIntBufferCompressionLevel': '0',
            'DFIntClientPacketMaxDelayMs': '1',
            'DFIntRakNetNakResendDelayMs': '5',
            'DFIntRakNetSelectTimeoutMs': '1',
            'DFIntMaxFrameBufferSize': '4',
            'DFIntRakNetLoopMs': '1',
            'FIntSimSolverResponsiveness': '2147483647',
            'FIntUITextureMaxRenderTextureSize': '1024',
            'FIntRakNetResendBufferArrayLength': '128',
            'FIntDebugTextureManagerSkipMips': '2',
            'FIntInterpolationMaxDelayMSec': '100',
            'FIntTerrainOTAMaxTextureSize': '1024',
            'FIntRenderLocalLightUpdatesMax': '1',
            'FIntRenderLocalLightUpdatesMin': '1',
            'FIntDefaultMeshCacheSizeMB': '256',
            'FIntRenderGrassDetailStrands': '0',
            'FIntCSGVoxelizerFadeRadius': '0',
            'FIntRobloxGuiBlurIntensity': '0',
            'FIntTaskSchedulerThreadMin': '3',
            'FIntFRMMaxGrassDistance': '0',
            'FIntFRMMinGrassDistance': '0',
            'FIntRenderShadowmapBias': '0',
            'FIntTargetRefreshRate': '240',
            'FIntMeshContentProviderForceCacheSize': '268435456',
            'FFlagRobloxInputUsesRuntime2': 'True',
            'FFlagLiveAnimationUpdateSupport': 'True',
            'FFlagRealTimeAnimationEnableRefactor': 'True',
            'DFFlagAnimatorAnywhere': 'True',
            'DFFlagDebugForceAnisoOff': 'True',
            'FIntRenderMsFrameGatherInterval': '60',
            'FIntActivatedCountTimerMSKeyboard': '0',
            'FIntActivatedCountTimerMSMouse': '0',
            'FIntRenderNodeEnterSleepingFrames': '0',
            'DFFlagAnimatorRetargetInterpolateFKCorrection': 'True',
            'DFFlagSimHumanoidFirstPerson240hz': 'True',
            'DFFlagSimSmoothedRunningController2': 'True',
            'DFFlagSimStepPhysicsImprovedSubStepping': 'True',
            'DFFlagPhysicsMechanismCacheOptimizeAlloc': 'True',
            'DFFlagTaskSchedulerRescheduleAsForeground': 'True',
            'DFFlagEnableConcurrentHttpClientCacheReads': 'True',
            'DFFlagProcess2DPipelineUseRuntimeThreading': 'True',
            'DFFlagReduceCPUWhenBG': 'True',
            'DFFlagAlwaysSkipDiskCache': 'True',
            'DFFlagDebugPauseVoxelizer': 'True',
            'DFFlagAnimatorPostProcessIK': 'True',
            'DFFlagFixSpecialMeshCulling': 'True',
            'DFFlagRenderEmitterOcclusionCulling': 'True',
            'DFFlagRenderFastClusterOcclusionCulling': 'True',
            'DFFlagRenderModelClusterOcclusionCulling': 'True',
            'FFlagRenderTestEnableDistanceCulling': 'True',
            'FFlagSmoothClusterOcclusionCulling2': 'True',
            'FFlagNewLightAttenuation': 'True',
            'FFlagRenderInitShadowmaps': 'True',
            'FFlagQuaternionPoseCorrection': 'True',
            'FFlagOptimizeCFrameUpdates4': 'True',
            'FFlagOptimizeCFrameUpdatesIC4': 'True',
            'FFlagCacheTextBoundsInGuiText': 'True',
            'FFlagStyleCacheLessMemory2': 'True',
            'FFlagReduceStyleCacheAllocations': 'True',
            'FFlagAnimationLodIkEnabled': 'True',
            'FFlagLargeReplicatorEnabled9': 'True',
            'FFlagDebugGraphicsPreferVulkan': 'False',
            'DFIntConnectionMTUSize': '900',
            'DFIntNetworkSchemaCompressionRatio': '0',
            'FIntSmoothMouseSpringFrequencyTenths': '100',
            'FIntTaskSchedulerAutoThreadLimit': '6',
        },
    },

    {
        'name': 'Zero Ping',
        'desc': '20 flags · Minimum RakNet latency and packet delays',
        'tag': 'NET',
        'flags': {
            'RakNetLoopMs':                             '1',
            'RakNetSelectTimeoutMs':                    '1',
            'RakNetNakResendDelayMs':                   '1',
            'RakNetNakResendDelayMsMax':                '1',
            'RakNetResendRttMultiple':                  '1',
            'RakNetClockDriftAdjustmentPerPingMillisecond': '100',
            'RaknetBandwidthInfluxHundredthsPercentageV2':  '10000',
            'RaknetBandwidthPingSendEveryXSeconds':     '1',
            'RakNetApplicationFeedbackScaleUpThresholdPercent': '0',
            'RakNetApplicationFeedbackScaleUpFactorHundredthPercent': '0',
            'RakNetResendBufferArrayLength':            '128',
            'RakNetEnablePoll':                         'True',
            'RakNetUseSlidingWindow4':                  'True',
            'ClientPacketMaxDelayMs':                   '1',
            'ClientPacketMaxFrameMicroseconds':         '200',
            'ClientPacketExcessMicroseconds':           '1000',
            'ClientPacketHealthyAllocationPercent':     '20',
            'MaxReceiveToDeserializeLatencyMilliseconds': '10',
            'MaxAcceptableUpdateDelay':                 '1',
            'ConnectingTimerInterval':                  '10',
        },
    },
    {
        'name': 'Max Throughput',
        'desc': '12 flags · Maximum packet and replication throughput',
        'tag': 'NET',
        'flags': {
            'MaxDataPacketPerSend':                     '2147483647',
            'CodecMaxOutgoingFrames':                   '10000',
            'CodecMaxIncomingPackets':                  '100',
            'BufferCompressionThreshold':               '100',
            'BufferCompressionLevel':                   '0',
            'LargePacketQueueSizeCutoffMB':             '1000',
            'NetworkQualityResponderUnit':              '10',
            'NetworkQualityResponderMaxWaitTime':       '1',
            'NetworkSchemaCompressionRatio':            '0',
            'MaxProcessPacketsStepsPerCyclic':          '10000',
            'MaxProcessPacketsJobScaling':              '10000',
            'ConnectionMTUSize':                        '900',
        },
    },
    {
        'name': 'Physics Boost',
        'desc': '8 flags · Optimized physics and replication rates',
        'tag': 'NET',
        'flags': {
            'S2PhysicsSenderRate':                      '35200',
            'PhysicsReceiveNumParallelTasks':           '20',
            'MegaReplicatorNumParallelTasks':           '20',
            'MegaReplicatorNetworkQualityProcessorUnit': '10',
            'ReplicationDataCacheNumParallelTasks':     '20',
            'AnimationLodFacsDistanceMax':              '0',
            'AnimationLodFacsDistanceMin':              '0',
            'AnimatorThrottleMaxFramesToSkip':          '1',
        },
    },
    {
        'name': 'No Grass + No Shadows',
        'desc': '10 flags · Remove grass, shadows and terrain detail',
        'tag': 'PERF',
        'flags': {
            'FRMMaxGrassDistance':                      '0',
            'FRMMinGrassDistance':                      '0',
            'GrassMovementReducedMotionFactor':         '0',
            'RenderShadowmapBias':                      '0',
            'TerrainArraySliceSize':                    '0',
            'DebugForceMSAASamples':                    '0',
            'CSGLevelOfDetailSwitchingDistance':        '0',
            'CSGLevelOfDetailSwitchingDistanceL12':     '0',
            'CSGLevelOfDetailSwitchingDistanceL23':     '0',
            'CSGLevelOfDetailSwitchingDistanceL34':     '0',
        },
    },
    {
        'name': 'Low Texture Mode',
        'desc': '6 flags · Minimum texture quality for max FPS',
        'tag': 'PERF',
        'flags': {
            'TextureQualityOverrideEnabled':            'True',
            'TextureQualityOverride':                   '0',
            'DebugTextureManagerSkipMips':              '8',
            'DebugLimitMinTextureResolutionWhenSkipMips': '9999999',
            'TextureCompositorActiveJobs':              '0',
            'RobloxGuiBlurIntensity':                   '0',
        },
    },
    {
        'name': 'Vulkan Mode',
        'desc': '4 flags · Force Vulkan renderer for GPU efficiency',
        'tag': 'PERF',
        'flags': {
            'DebugGraphicsPreferVulkan':                'True',
            'DebugGraphicsPreferD3D11':                 'False',
            'FastGPULightCulling3':                     'True',
            'DebugForceFSMCPULightCulling':             'True',
        },
    },
    {
        'name': 'D3D11 Mode',
        'desc': '5 flags · Force D3D11 with GPU optimizations',
        'tag': 'PERF',
        'flags': {
            'DebugGraphicsPreferD3D11':                 'True',
            'DebugGraphicsPreferVulkan':                'False',
            'FastGPULightCulling3':                     'True',
            'GraphicsEnableD3D10Compute':               'True',
            'RenderGpuTextureCompressor':               'True',
        },
    },
    {
        'name': 'Unlocked FPS',
        'desc': '3 flags · Remove FPS cap and show counter',
        'tag': 'FPS',
        'flags': {
            'TaskSchedulerTargetFps':                   '9999999',
            'TargetRefreshRate':                        '9999',
            'DebugDisplayFPS':                          'True',
        },
    },
    {
        'name': 'Scheduler Boost',
        'desc': '6 flags · Multi-thread scheduler optimization',
        'tag': 'FPS',
        'flags': {
            'TaskSchedulerJobInitThreads':              '6',
            'TaskSchedulerJobInGameThreads':            '6',
            'TaskSchedulerAutoThreadLimit':             '6',
            'TaskSchedulerThreadMin':                   '4',
            'RuntimeConcurrency':                       '12',
            'ActivatedCountTimerMSMouse':               '0',
        },
    },
    {
        'name': 'Extended Camera',
        'desc': '4 flags · Max zoom and simulation radius',
        'tag': 'FUN',
        'flags': {
            'CameraMaxZoomDistance':                    '99999',
            'MaxClientSimulationRadius':                '99999',
            'MinClientSimulationRadius':                '99998',
            'DebugUseCustomSimRadius':                  'True',
        },
    },
    {
        'name': 'Gray Sky',
        'desc': '2 flags · Replace skybox with flat gray',
        'tag': 'FUN',
        'flags': {
            'DebugSkyGray':                             'True',
            'RenderInitShadowmaps':                     'False',
        },
    },
    {
        'name': 'Mouse Precision',
        'desc': '3 flags · Remove input delay and smooth mouse',
        'tag': 'FUN',
        'flags': {
            'ActivatedCountTimerMSMouse':               '0',
            'ActivatedCountTimerMSKeyboard':            '0',
            'SmoothMouseSpringFrequencyTenths':         '100',
        },
    },
    {
        'name': 'Mesh Cache Max',
        'desc': '3 flags · Maximize mesh memory cache size',
        'tag': 'CFG',
        'flags': {
            'DefaultMeshCacheSizeMB':                   '256',
            'MeshContentProviderForceCacheSize':        '268435456',
            'CanHideGuiGroupId':                        '32380007',
        },
    },
]


class RoundedButtonStyle(__import__("PyQt6.QtWidgets", fromlist=["QProxyStyle"]).QProxyStyle):
    """Force rounded corners on all QPushButtons regardless of platform style."""
    RADIUS = 8

    def drawControl(self, element, option, painter, widget=None):
        from PyQt6.QtWidgets import QStyle, QStyleOptionButton
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QPen, QBrush, QColor
        if element == QStyle.ControlElement.CE_PushButton and isinstance(option, QStyleOptionButton):
            text = option.text
            if text in ("—", "✕", "×", "✗", "−") or (widget and widget.property("transparent") is True):
                super().drawControl(element, option, painter, widget)
                return
            painter.save()
            painter.setRenderHint(painter.RenderHint.Antialiasing)
            r       = option.rect
            state   = option.state
            hovered = bool(state & QStyle.StateFlag.State_MouseOver)
            pressed = bool(state & QStyle.StateFlag.State_Sunken)
            is_apply = "APPLY TO ROBLOX" in text.upper() or "INJECT" in text.upper()
            is_kill  = "KILL" in text.upper() or "STOP" in text.upper()
            if is_apply:
                bg     = QColor("#252525") if hovered else QColor("#161616")
                border = QColor("#ffffff")
                fg     = QColor("#ffffff")
            elif is_kill and hovered:
                bg = QColor("#282828"); border = QColor("#666666"); fg = QColor("#ffffff")
            elif hovered:
                bg = QColor("#1e1e1e"); border = QColor("#444444"); fg = QColor("#ffffff")
            else:
                bg = QColor("#141414"); border = QColor("#2a2a2a"); fg = QColor("#aaaaaa")
            painter.setPen(QPen(border, 1))
            painter.setBrush(QBrush(bg))
            painter.drawRoundedRect(r.adjusted(1, 1, -1, -1), self.RADIUS, self.RADIUS)
            painter.setPen(fg)
            painter.setFont(widget.font() if widget else painter.font())
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, text)
            painter.restore()
        else:
            super().drawControl(element, option, painter, widget)

    def subElementRect(self, element, option, widget=None):
        return super().subElementRect(element, option, widget)


STYLE = """
QMainWindow, QWidget {
    background-color: #0d0d0d;
    color: #cccccc;
    font-family: 'Segoe UI', sans-serif;
}
QMainWindow {
    border-radius: 18px;
}
QWidget#titleBar {
    background-color: #0d0d0d;
    border-bottom: 1px solid #1a1a1a;
    border-radius: 18px 18px 0px 0px;
}
QWidget#titleBar QLabel:not(#sacredTitle) {
    font-size: 11px;
    color: #cccccc;
    background: transparent;
    padding-right: 8px;
}
QWidget#toolbar {
    background-color: #0d0d0d;
    border-bottom: 1px solid #1a1a1a;
    padding: 6px 10px;
    border-radius: 8px;
}
QFrame {
    border-radius: 6px;
}
QPushButton {
    background-color: #141414;
    color: #cccccc;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 5px 14px;
    font-size: 12px;
    font-weight: 500;
    outline: none;
}
QPushButton:hover {
    background-color: #1e1e1e;
    border-color: #444444;
    color: #ffffff;
}
QPushButton:pressed {
    background-color: #0d0d0d;
}
QPushButton:focus {
    outline: none;
}
QPushButton:disabled {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    color: #555555;
    font-weight: 700;
    border-radius: 6px;
}
QPushButton:checked {
    background-color: #141414;
    border-color: #444444;
    color: #cccccc;
}
QLineEdit {
    background-color: #141414;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 6px 12px;
    color: #cccccc;
    font-size: 12px;
}
QLineEdit:focus { border-color: #444444; }
QTableWidget {
    background-color: #141414;
    gridline-color: #0d0d0d;
    border: none;
    font-size: 12px;
    color: #cccccc;
    selection-background-color: #0d0d0d;
    selection-color: #cccccc;
}
QTableWidget::item { padding: 4px 10px; border-bottom: 1px solid #111111; }
QTableWidget::item:selected { background-color: #1a1a1a; color: #ffffff; }
QTableWidget::item:hover { background-color: #141414; }
QHeaderView::section {
    background-color: #0d0d0d;
    color: #2a2a2a;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 2px;
    padding: 5px 10px;
    border: none;
    border-bottom: 1px solid #0f0f0f;
}
QHeaderView { border: none; background: #0d0d0d; }
QTableWidget QHeaderView::section { border-right: none; border-left: none; }
QTableCornerButton::section { background: #0d0d0d; border: none; }
QStatusBar {
    background-color: #0d0d0d;
    border-top: 1px solid #1a1a1a;
    color: #cccccc;
    font-size: 11px;
    padding: 2px 8px;
}
QScrollBar:vertical { background: #0d0d0d; width: 4px; border-radius: 2px; margin: 0; }
QScrollBar::handle:vertical { background: #2a2a2a; border-radius: 2px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #444444; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; border:none; background:none; }
QDialog { background-color: #0d0d0d; border-radius: 12px; }
QComboBox {
    background-color: #0d0d0d;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding:4px 10px; color: #cccccc;
}
QComboBox::drop-down { border:none; }
QComboBox QAbstractItemView {
    background-color: #0d0d0d;
    color: #cccccc;
    border: 1px solid #2a2a2a;
}
"""


def make_cross_pixmap(size: int, color: QColor) -> QPixmap:
    """Draw a gothic cross as a QPixmap."""
    px = QPixmap(size, size)
    px.fill(Qt.GlobalColor.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    s = size
    cx, cy = s / 2, s / 2

    vw = s * 0.18
    hw = s * 0.55
    hh = s * 0.09
    top = s * 0.04
    bot = s * 0.96
    hy  = s * 0.36
    flare = s * 0.13

    path = QPainterPath()

    path.moveTo(cx, top)
    path.cubicTo(cx - vw*0.4, top + s*0.04,  cx - vw*0.7, hy - hh*3,  cx - vw*0.5, hy - hh*1.5)
    path.cubicTo(cx - vw*0.5, hy - hh,  cx - hw + flare*0.3, hy - hh,  cx - hw - flare*0.1, hy - hh*0.4)
    path.cubicTo(cx - hw - flare*0.5, hy - hh*0.1,  cx - hw - flare*0.5, hy + hh*0.1,  cx - hw - flare*0.1, hy + hh*0.4)
    path.cubicTo(cx - hw + flare*0.3, hy + hh,  cx - vw*0.5, hy + hh,  cx - vw*0.5, hy + hh*1.5)
    path.cubicTo(cx - vw*0.5, bot - s*0.12,  cx - vw*0.4, bot - s*0.04,  cx, bot)
    path.cubicTo(cx + vw*0.4, bot - s*0.04,  cx + vw*0.5, bot - s*0.12,  cx + vw*0.5, hy + hh*1.5)
    path.cubicTo(cx + vw*0.5, hy + hh,  cx + hw - flare*0.3, hy + hh,  cx + hw + flare*0.1, hy + hh*0.4)
    path.cubicTo(cx + hw + flare*0.5, hy + hh*0.1,  cx + hw + flare*0.5, hy - hh*0.1,  cx + hw + flare*0.1, hy - hh*0.4)
    path.cubicTo(cx + hw - flare*0.3, hy - hh,  cx + vw*0.5, hy - hh,  cx + vw*0.5, hy - hh*1.5)
    path.cubicTo(cx + vw*0.7, hy - hh*3,  cx + vw*0.4, top + s*0.04,  cx, top)
    path.closeSubpath()

    pen = QPen(QColor(255, 255, 255, 60))
    pen.setWidthF(size * 0.04)
    p.setPen(pen)
    p.setBrush(QBrush(color))
    p.drawPath(path)

    p.end()
    return px


class CrossWidget(QLabel):
    def __init__(self, size=38, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        px = make_cross_pixmap(size, QColor(255, 255, 255))
        self.setPixmap(px)
        self.setScaledContents(True)


class TitleLabel(QLabel):
    """Shimmer: cross + title in one widget, seamless looping dark band."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._text = "†  " + text
        self.setFont(QFont("Georgia", 18, QFont.Weight.Bold))
        self.setFixedHeight(54)
        self.setMinimumWidth(180)
        self.setStyleSheet("background: transparent; border: none;")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._pos = 0.0
        self._tick_speed = 0.003
        self._text_color = QColor(255, 255, 255)
        self._dark_color  = QColor(110, 110, 110)
        from PyQt6.QtCore import QTimer
        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(16)

    def _tick(self):
        self._pos = (self._pos + self._tick_speed) % 1.0
        self.update()

    def paintEvent(self, event):
        import math
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        p.setFont(self.font())
        w, h = self.width(), self.height()
        pos = self._pos

        bright = getattr(self, '_text_color', QColor(220, 220, 220))
        dark   = getattr(self, '_dark_color',  QColor(25, 25, 25))
        num_stops = 48
        half_band = 0.30

        text_mask = QPixmap(w, h)
        text_mask.fill(Qt.GlobalColor.transparent)
        mp = QPainter(text_mask)
        mp.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        mp.setFont(self.font())
        mp.setPen(QColor(255, 255, 255))
        mp.drawText(text_mask.rect(),
                    Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                    self._text)
        mp.end()

        g = QLinearGradient(0, 0, w, 0)
        for i in range(num_stops + 1):
            t_val = i / num_stops
            d = t_val - pos
            if d > 0.5: d -= 1.0
            if d < -0.5: d += 1.0
            norm = min(abs(d) / half_band, 1.0)
            ratio = 0.5 - 0.5 * math.cos(norm * math.pi)
            r  = int(dark.red()   + (bright.red()   - dark.red())   * ratio)
            gc = int(dark.green() + (bright.green() - dark.green()) * ratio)
            b  = int(dark.blue()  + (bright.blue()  - dark.blue())  * ratio)
            g.setColorAt(t_val, QColor(max(0,min(255,r)), max(0,min(255,gc)), max(0,min(255,b))))

        grad_px = QPixmap(w, h)
        grad_px.fill(Qt.GlobalColor.transparent)
        gp = QPainter(grad_px)
        gp.fillRect(0, 0, w, h, QBrush(g))
        gp.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
        gp.drawPixmap(0, 0, text_mask)
        gp.end()

        p.drawPixmap(0, 0, grad_px)
        p.end()


_DLG_STYLE = """
    QDialog {
        background-color: #0d0d0d;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        color: #cccccc;
    }
    QLabel { background: transparent; color: #cccccc;
    QLineEdit {
        background-color: #0d0d0d;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        color: #cccccc;
        padding: 7px 12px;
        font-size: 12px;
    }
    QLineEdit:focus { border-color: #444444;
    QTextEdit {
        background-color: #0d0d0d;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        color: #cccccc;
        font-family: Consolas, monospace;
        font-size: 12px;
        padding: 8px;
    }
    QListWidget {
        background-color: #0d0d0d;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        color: #cccccc;
        font-size: 12px;
        outline: none;
        padding: 4px;
    }
    QListWidget::item { padding: 9px 14px; border-radius: 6px; }
    QListWidget::item:selected { background-color: #0d0d0d;
    QListWidget::item:hover { background-color: #0d0d0d;
"""

_DLG_BTN = """
    QPushButton {
        background-color: #141414;
        color: #cccccc;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 6px 18px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    QPushButton:hover { background-color: #1e1e1e; border-color: #444; color: #fff; }
    QPushButton:pressed { background-color: #282828; }
"""
_DLG_BTN_PRIMARY = """
    QPushButton {
        background-color: #161616;
        border: 1px solid #cccccc;
        border-radius: 8px;
        color: #ffffff;
        font-size: 12px;
        font-weight: 700;
        padding: 6px 18px;
        letter-spacing: 0.5px;
    }
    QPushButton:hover { background-color: #222222; border-color: #ffffff; color: #ffffff; }
    QPushButton:pressed { background-color: #1a1a1a; }
"""
_DLG_BTN_DANGER = """
    QPushButton {
        background-color: #1a0000;
        border: 1px solid #440000;
        border-radius: 8px;
        color: #cccccc;
        font-size: 12px;
        font-weight: 700;
        padding: 6px 18px;
        letter-spacing: 0.5px;
    }
    QPushButton:hover { background-color: #141414; border-color: #444; color: #fff; }
"""


class BaseDialog(QDialog):
    """Frameless dark dialog matching main window style."""
    def __init__(self, title_text, parent=None, width=400):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumWidth(width)
        self._drag_pos = None

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        _bg = ""
        _alpha = 0.6
        _accent = QColor(255,255,255)
        mw = parent
        while mw and not hasattr(mw, '_bg_path'):
            mw = mw.parent() if hasattr(mw, 'parent') else None
        if mw and hasattr(mw, '_bg_path') and mw._bg_path:
            _bg = mw._bg_path
            _alpha = (mw._slider_bg_opacity.value()/100.0) if hasattr(mw,'_slider_bg_opacity') else 0.6
        if mw and hasattr(mw, '_theme_accent'):
            _accent = mw._theme_accent

        self._container = QWidget()
        self._container.setObjectName("dlgContainer")
        if _bg:
            try:
                px = QPixmap(_bg)
                if not px.isNull():
                    self._pending_bg = (_bg, _alpha)
            except Exception:
                pass
        bg_color = "#0d0d0d" if not _bg else "transparent"
        self._container.setStyleSheet(_DLG_STYLE + f"QWidget#dlgContainer {{ background:{bg_color}; border:1px solid #222; border-radius:12px; }}")
        outer.addWidget(self._container)

        self._root = QVBoxLayout(self._container)
        self._root.setSpacing(0)
        self._root.setContentsMargins(0, 0, 0, 0)

        title_bar = QWidget()
        title_bar.setStyleSheet("background:#0a0a0a; border-radius:12px 12px 0 0; border-bottom:1px solid #1a1a1a;")
        title_bar.setFixedHeight(44)
        title_bar.mousePressEvent   = self._tb_press
        title_bar.mouseMoveEvent    = self._tb_move
        title_bar.mouseReleaseEvent = self._tb_release
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(14, 0, 8, 0)

        lbl = QLabel(title_text)
        lbl.setStyleSheet("color:#888888; font-size:11px; font-weight:600; letter-spacing:2px; background:transparent;")
        btn_x = QPushButton("✕")
        btn_x.setFixedSize(28, 28)
        btn_x.setStyleSheet("QPushButton{background:transparent;border:none;color:#555;font-size:11px;border-radius:6px;} QPushButton:hover{background:#cc2222;color:#fff;}")
        btn_x.clicked.connect(self.reject)

        tb_layout.addWidget(lbl)
        tb_layout.addStretch()
        tb_layout.addWidget(btn_x)
        self._root.addWidget(title_bar)

        self._content = QVBoxLayout()
        self._content.setSpacing(12)
        self._content.setContentsMargins(20, 16, 20, 20)
        self._root.addLayout(self._content)

        self._apply_mask()

    def _apply_mask(self):
        from PyQt6.QtGui import QRegion
        if self.width() > 0 and self.height() > 0:
            r = self.rect()
            radius = 12
            region = QRegion(r)
            tl = QRegion(r.x(), r.y(), radius*2, radius*2, QRegion.RegionType.Ellipse)
            tr = QRegion(r.right()-radius*2+1, r.y(), radius*2, radius*2, QRegion.RegionType.Ellipse)
            bl = QRegion(r.x(), r.bottom()-radius*2+1, radius*2, radius*2, QRegion.RegionType.Ellipse)
            br = QRegion(r.right()-radius*2+1, r.bottom()-radius*2+1, radius*2, radius*2, QRegion.RegionType.Ellipse)
            tl_r = QRegion(r.x(), r.y(), radius, radius)
            tr_r = QRegion(r.right()-radius+1, r.y(), radius, radius)
            bl_r = QRegion(r.x(), r.bottom()-radius+1, radius, radius)
            br_r = QRegion(r.right()-radius+1, r.bottom()-radius+1, radius, radius)
            corners = tl_r.united(tr_r).united(bl_r).united(br_r).subtracted(
                      tl.united(tr).united(bl).united(br))
            self.setMask(region.subtracted(corners))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._apply_mask()

    def _tb_press(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
    def _tb_move(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(e.globalPosition().toPoint() - self._drag_pos)
    def _tb_release(self, e):
        self._drag_pos = None

    def showEvent(self, event):
        super().showEvent(event)
        self._apply_dlg_background()

    def _apply_dlg_background(self):
        pending = getattr(self, '_pending_bg', None)
        if not pending:
            return
        bg_path, alpha = pending
        try:
            px = QPixmap(bg_path)
            if px.isNull():
                return
            w, h = self._container.width(), self._container.height()
            if w <= 0 or h <= 0:
                w, h = self.width(), self.height()
            scaled = px.scaled(w, h,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation)
            ox = max(0, (scaled.width()-w)//2)
            oy = max(0, (scaled.height()-h)//2)
            cropped = scaled.copy(ox, oy, w, h)
            final = QPixmap(w, h)
            final.fill(QColor(13,13,13))
            rp = QPainter(final)
            rp.setOpacity(alpha)
            rp.drawPixmap(0, 0, cropped)
            rp.end()
            if not getattr(self, '_dlg_bg_lbl', None):
                self._dlg_bg_lbl = QLabel(self._container)
                self._dlg_bg_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            self._dlg_bg_lbl.setPixmap(final)
            self._dlg_bg_lbl.setGeometry(0, 0, w, h)
            self._dlg_bg_lbl.lower()
            self._dlg_bg_lbl.show()
        except Exception:
            pass

    def add(self, widget):
        self._content.addWidget(widget)

    def add_layout(self, layout):
        self._content.addLayout(layout)

    def add_spacing(self, n=8):
        self._content.addSpacing(n)


class AddFlagDialog(BaseDialog):
    def __init__(self, parent=None, name="", value="", flag_type=""):
        super().__init__("FLAG EDITOR", parent, width=360)
        lbl_name = QLabel("Flag name:")
        lbl_name.setStyleSheet("color:#666; font-size:11px; letter-spacing:1px;")
        self.add(lbl_name)
        self.nameEdit = QLineEdit(name)
        self.nameEdit.setPlaceholderText("e.g. DFIntFoo")
        self.add(self.nameEdit)

        lbl_type = QLabel("Type:")
        lbl_type.setStyleSheet("color:#666; font-size:11px; letter-spacing:1px;")
        self.add(lbl_type)
        self.typeBox = QComboBox()
        self.typeBox.addItems(["bool", "int", "float", "string"])
        self.typeBox.setStyleSheet("""
            QComboBox { background: #0d0d0d;
                        color: #cccccc;
            QComboBox::drop-down { border:none; }
            QComboBox QAbstractItemView { background: #0d0d0d;
                                          selection-background-color: #0d0d0d;
        """)
        if flag_type in ["bool", "int", "float", "string"]:
            self.typeBox.setCurrentText(flag_type)
        self.add(self.typeBox)

        lbl_val = QLabel("Value:")
        lbl_val.setStyleSheet("color:#666; font-size:11px; letter-spacing:1px;")
        self.add(lbl_val)
        self.valueEdit = QLineEdit(str(value))
        self.valueEdit.setPlaceholderText("e.g. true / 1 / 3.14")
        self.add(self.valueEdit)
        self.add_spacing(4)

        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("CANCEL"); btn_cancel.setStyleSheet(_DLG_BTN)
        btn_ok     = QPushButton("SAVE");   btn_ok.setStyleSheet(_DLG_BTN_PRIMARY)
        btn_cancel.clicked.connect(self.reject)
        btn_ok.clicked.connect(self.accept)
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)
        self.add_layout(btn_row)

    def get_data(self):
        return self.nameEdit.text().strip(), self.valueEdit.text().strip(), self.typeBox.currentText()


PRESETS_FILE = None

def get_presets_path(state):
    import os
    p = state.config_dir / "presets.json"
    return p

def load_presets(state):
    p = get_presets_path(state)
    if p.exists():
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_presets(state, presets):
    p = get_presets_path(state)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(presets, f, indent=4, ensure_ascii=False)



_BTN_S = """
    QPushButton {
        background-color: #141414;
        color: #cccccc;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 6px 18px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
    }
    QPushButton:hover { background-color: #1e1e1e; border-color: #444; color: #fff; }
    QPushButton:pressed { background-color: #282828; }
"""
_BTN_PRIMARY = """
    QPushButton {
        background-color: #141414;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        color: #cccccc;
        font-size: 12px;
        font-weight: 700;
        padding: 6px 18px;
        letter-spacing: 1px;
    }
    QPushButton:hover { background-color: #141414; border-color: #444; color: #fff; }
"""


class SavePresetDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__("PRESET MANAGER", parent, width=380)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Preset Name...")
        self.add(self.name_edit)
        self.add_spacing(4)
        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("CANCEL");      btn_cancel.setStyleSheet(_DLG_BTN)
        btn_save   = QPushButton("SAVE PRESET"); btn_save.setStyleSheet(_DLG_BTN_PRIMARY)
        btn_cancel.clicked.connect(self.reject)
        btn_save.clicked.connect(self._save)
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_save)
        self.add_layout(btn_row)
        self.name_edit.returnPressed.connect(self._save)

    def _save(self):
        if self.name_edit.text().strip():
            self.accept()

    def get_name(self):
        return self.name_edit.text().strip()


class PresetListDialog(BaseDialog):
    _CATEGORIES = [
        ('FPS',  'FPS FFlags'),
        ('NET',  'Ping FFlags'),
        ('PERF', 'Performance FFlags'),
        ('CFG',  'User Configs'),
        ('FUN',  'Fun FFlags'),
        ('MAIN', 'Featured'),
    ]

    def __init__(self, presets: dict, parent=None):
        super().__init__("PRESETS", parent, width=500)
        self.setMinimumHeight(480)
        self._presets = presets
        self._chosen  = None

        from PyQt6.QtWidgets import (QListWidget, QListWidgetItem,
                                      QStackedWidget, QHBoxLayout)
        from collections import defaultdict
        from ui.gui import BUILTIN_PRESETS

        builtin_tag = {p['name']: p.get('tag', 'CFG') for p in BUILTIN_PRESETS}

        groups = defaultdict(list)
        for name in presets:
            tag = builtin_tag.get(name, 'CFG')
            groups[tag].append(name)

        active_cats = [(tag, lbl) for tag, lbl in self._CATEGORIES
                       if tag in groups]
        for tag in groups:
            if not any(t == tag for t, _ in self._CATEGORIES):
                active_cats.append((tag, tag))

        tab_bar_w = QWidget()
        tab_bar_w.setStyleSheet("background:transparent;")
        tab_bar_w.setFixedHeight(36)
        tbl = QHBoxLayout(tab_bar_w)
        tbl.setContentsMargins(0, 0, 0, 0)
        tbl.setSpacing(4)

        _TAB_OFF = """
            QPushButton {
                background: #0d0d0d;
                border-radius: 6px; color: #cccccc;
                font-size: 11px; font-weight: 500;
                padding: 0 14px; outline: none;
            }
            QPushButton:hover { background: #0d0d0d;
            QPushButton:focus { outline: none; }
        """
        _TAB_ON = """
            QPushButton {
                background: #0d0d0d;
                border-radius: 6px; color: #cccccc;
                font-size: 11px; font-weight: 600;
                padding: 0 14px; outline: none;
            }
            QPushButton:focus { outline: none; }
        """

        self._tab_btns   = []
        self._stack      = QStackedWidget()
        self._stack.setStyleSheet("background:transparent;")
        self._list_widgets = []

        for i, (tag, lbl) in enumerate(active_cats):
            btn = QPushButton(lbl)
            btn.setFixedHeight(30)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(_TAB_OFF)
            tbl.addWidget(btn)
            self._tab_btns.append((btn, _TAB_OFF, _TAB_ON))

            lw = QListWidget()
            lw.setStyleSheet("""
                QListWidget {
                    background: #0d0d0d;
                    border-radius: 6px; color: #cccccc;
                    font-size: 12px; outline: none;
                }
                QListWidget::item { padding: 6px 10px; border-radius: 4px; }
                QListWidget::item:selected { background: #0d0d0d;
                QListWidget::item:hover { background: #0d0d0d;
            """)
            for name in sorted(groups[tag]):
                count = len(presets[name])
                item = QListWidgetItem(f"  {name}  ({count} flags)")
                item.setData(Qt.ItemDataRole.UserRole, name)
                lw.addItem(item)
            lw.doubleClicked.connect(self._load)
            self._stack.addWidget(lw)
            self._list_widgets.append(lw)

            idx = i
            def _make_switch(ix):
                def _switch():
                    self._stack.setCurrentIndex(ix)
                    for j, (b, off, on) in enumerate(self._tab_btns):
                        b.setStyleSheet(on if j == ix else off)
                return _switch
            btn.clicked.connect(_make_switch(i))

        tbl.addStretch()
        self.add(tab_bar_w)
        self.add_spacing(6)
        self.add(self._stack)
        self.add_spacing(4)

        if self._tab_btns:
            self._tab_btns[0][0].setStyleSheet(_TAB_ON)

        btn_row = QHBoxLayout()
        btn_del    = QPushButton("DELETE");      btn_del.setStyleSheet(_DLG_BTN_DANGER)
        btn_cancel = QPushButton("CANCEL");      btn_cancel.setStyleSheet(_DLG_BTN)
        btn_load   = QPushButton("LOAD PRESET"); btn_load.setStyleSheet(_DLG_BTN_PRIMARY)
        btn_del.clicked.connect(self._delete)
        btn_cancel.clicked.connect(self.reject)
        btn_load.clicked.connect(self._load)
        btn_row.addWidget(btn_del)
        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_load)
        self.add_layout(btn_row)

    def _current_name(self):
        lw = self._stack.currentWidget()
        if lw:
            item = lw.currentItem()
            if item:
                return item.data(Qt.ItemDataRole.UserRole)
        return None

    def _load(self):
        name = self._current_name()
        if name:
            self._chosen = name
            self.accept()

    def _delete(self):
        name = self._current_name()
        if name and name in self._presets:
            del self._presets[name]
            lw = self._stack.currentWidget()
            if lw:
                row = lw.currentRow()
                lw.takeItem(row)

    def get_chosen(self):      return self._chosen
    def get_updated_presets(self): return self._presets




class ImportDialog(BaseDialog):
    """Import FFlags: paste JSON or pick a file."""
    def __init__(self, parent=None):
        super().__init__("ADD FFLAGS", parent, width=480)
        self.setMinimumHeight(400)
        self._result_data = {}

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Paste JSON or key=value FFlags here...")
        self.add(self.text_edit)
        self.add_spacing(4)

        btn_add = QPushButton("ADD FFLAGS")
        btn_add.setStyleSheet(_DLG_BTN_PRIMARY)
        btn_add.clicked.connect(self._add_from_text)
        self.add(btn_add)

        btn_file = QPushButton("IMPORT FROM FILES")
        btn_file.setStyleSheet(_DLG_BTN)
        btn_file.clicked.connect(self._add_from_file)
        self.add(btn_file)

        btn_cancel = QPushButton("CANCEL")
        btn_cancel.setStyleSheet(_DLG_BTN_DANGER)
        btn_cancel.clicked.connect(self.reject)
        self.add(btn_cancel)

    def _add_from_text(self):
        raw = self.text_edit.toPlainText().strip()
        if not raw:
            return
        try:
            data = self._parse_fflag_text(raw)
            if isinstance(data, dict) and data:
                self._result_data = data
                self.accept()
            else:
                AlertDialog("ERROR", "Could not parse any FFlags.\nPaste valid JSON or key=value text.", parent=self).exec()
        except Exception as e:
            AlertDialog("PARSE ERROR", str(e), parent=self).exec()

    def _add_from_file(self):
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(
            self, "Import FFlags", "",
            "FFlag Files (*.json *.txt);;JSON Files (*.json);;Text Files (*.txt);;All Files (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read().strip()
            data = self._parse_fflag_text(raw)
            if isinstance(data, dict) and data:
                self._result_data = data
                self.accept()
            else:
                AlertDialog("ERROR", "Could not parse any FFlags from this file.\nMake sure it is a valid JSON or key=value text file.", parent=self).exec()
        except Exception as e:
            AlertDialog("ERROR", str(e), parent=self).exec()

    def _parse_fflag_text(self, raw: str) -> dict:
        """Parse JSON or plain key=value / key: value text formats."""
        try:
            result = json.loads(raw)
            if isinstance(result, dict):
                return result
        except Exception:
            pass
        result = {}
        for line in raw.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("//"):
                continue
            for sep in ("=", ":"):
                if sep in line:
                    k, _, v = line.partition(sep)
                    k = k.strip().strip('"').strip("'")
                    v = v.strip().strip('"').strip("'").rstrip(",")
                    if k:
                        result[k] = v
                    break
        return result

    def get_data(self):
        return self._result_data


class AutoApplyWorker(QThread):
    status_update = pyqtSignal(str)

    def __init__(self, state, config_file):
        super().__init__()
        self.state = state
        self.config_file = config_file
        self._running = True
        self.setTerminationEnabled(False)

    def run(self):
        from core.injector import apply_flags
        from core.config_manager import load_flags
        while self._running and getattr(self.state, 'auto_apply_enabled', False):
            try:
                data = load_flags(self.config_file)
                result = apply_flags(data)
                self.status_update.emit(f"[Auto Apply] {result}")
            except PermissionError:
                self._running = False
                self.state.auto_apply_enabled = False
                self.status_update.emit("[Auto Apply] ACCESS_DENIED")
            except Exception as e:
                err_str = str(e)
                if "error_code: 5" in err_str or "error_code:5" in err_str or "Access" in err_str:
                    self._running = False
                    self.state.auto_apply_enabled = False
                    self.status_update.emit("[Auto Apply] ACCESS_DENIED")
                else:
                    self.status_update.emit(f"[Auto Apply] Error: {e}")
            for _ in range(50):
                if not self._running:
                    break
                self.msleep(100)

    def stop(self):
        self._running = False


class ConfirmDialog(BaseDialog):
    def __init__(self, message: str, parent=None):
        super().__init__("CONFIRM", parent, width=320)
        lbl = QLabel(message)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color: #cccccc; font-size: 13px; background: transparent;")
        self.add(lbl)
        self.add_spacing(8)
        btn_row = QHBoxLayout()
        btn_no  = QPushButton("NO");  btn_no.setStyleSheet(_DLG_BTN)
        btn_yes = QPushButton("YES"); btn_yes.setStyleSheet(_DLG_BTN_PRIMARY)
        btn_no.clicked.connect(self.reject)
        btn_yes.clicked.connect(self.accept)
        btn_row.addWidget(btn_no)
        btn_row.addWidget(btn_yes)
        self.add_layout(btn_row)


class InputDialog(BaseDialog):
    """Styled single-line input dialog replacing QInputDialog."""
    def __init__(self, title, label, default="", parent=None):
        super().__init__(title, parent, width=360)
        lbl = QLabel(label)
        lbl.setStyleSheet("color:#aaaaaa; font-size:12px; background:transparent;")
        self.add(lbl)
        self._edit = QLineEdit(default)
        self._edit.setStyleSheet("""
            QLineEdit { background: #0d0d0d;
                        padding:8px 12px; color: #cccccc;
            QLineEdit:focus { border-color: #444444;
        """)
        self._edit.returnPressed.connect(self.accept)
        self.add(self._edit)
        self.add_spacing(4)
        row = QHBoxLayout()
        btn_cancel = QPushButton("CANCEL"); btn_cancel.setStyleSheet(_DLG_BTN)
        btn_ok     = QPushButton("OK");     btn_ok.setStyleSheet(_DLG_BTN_PRIMARY)
        btn_cancel.clicked.connect(self.reject)
        btn_ok.clicked.connect(self.accept)
        row.addWidget(btn_cancel)
        row.addWidget(btn_ok)
        self.add_layout(row)

    def get_text(self):
        return self._edit.text().strip()


class AlertDialog(BaseDialog):
    """Styled warning/info dialog replacing QMessageBox."""
    def __init__(self, title, message, parent=None, yes_no=False):
        super().__init__(title, parent, width=380)
        lbl = QLabel(message)
        lbl.setWordWrap(True)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("color:#cccccc; font-size:12px; background:transparent; line-height:1.5;")
        self.add(lbl)
        self.add_spacing(8)
        row = QHBoxLayout()
        self._accepted = False
        if yes_no:
            btn_no  = QPushButton("NO");  btn_no.setStyleSheet(_DLG_BTN)
            btn_yes = QPushButton("YES"); btn_yes.setStyleSheet(_DLG_BTN_PRIMARY)
            btn_no.clicked.connect(self.reject)
            btn_yes.clicked.connect(self.accept)
            row.addWidget(btn_no)
            row.addWidget(btn_yes)
        else:
            btn_ok = QPushButton("OK"); btn_ok.setStyleSheet(_DLG_BTN_PRIMARY)
            btn_ok.clicked.connect(self.accept)
            row.addWidget(btn_ok)
        self.add_layout(row)


class _ModsWatcherThread(QThread):
    """Background thread: watches for RobloxPlayerBeta.exe launch and applies mods."""
    mods_applied = pyqtSignal(str)

    def __init__(self, window):
        super().__init__()
        self._window  = window
        self._running = True
        self._was_running = False

    def stop(self):
        self._running = False
        self.quit()
        self.wait(2000)

    def run(self):
        import subprocess, time
        while self._running:
            try:
                out = subprocess.check_output(
                    'tasklist /FI "IMAGENAME eq RobloxPlayerBeta.exe" /NH',
                    shell=True, stderr=subprocess.DEVNULL
                ).decode(errors="ignore")
                is_running = "RobloxPlayerBeta.exe" in out
            except Exception:
                is_running = False

            if is_running and not self._was_running:
                time.sleep(4)
                try:
                    self._apply()
                except Exception as e:
                    self.mods_applied.emit(f"Auto Mods error: {e}")

            self._was_running = is_running
            time.sleep(3)

    def _apply(self):
        import shutil, os
        w = self._window
        roblox_dir = w._find_roblox_dir()
        if not roblox_dir:
            self.mods_applied.emit("Auto Mods: Roblox folder not found")
            return

        applied = []

        cursor_path = getattr(w, '_cursor_path', '')
        if cursor_path and os.path.isfile(cursor_path):
            try:
                dest_dir = os.path.join(roblox_dir, "content", "textures", "Cursors", "KeyboardMouse")
                os.makedirs(dest_dir, exist_ok=True)
                from PIL import Image as _Img
                img = _Img.open(cursor_path).convert("RGBA")
                img = img.resize((64, 64), _Img.LANCZOS)
                import tempfile, os as _os
                tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
                tmp.close()
                img.save(tmp.name, "PNG")
                for fname in ("ArrowFarCursor.png", "ArrowCursor.png"):
                    shutil.copy2(tmp.name, _os.path.join(dest_dir, fname))
                _os.unlink(tmp.name)
                applied.append("cursor")
            except ImportError:
                for fname in ("ArrowFarCursor.png", "ArrowCursor.png"):
                    shutil.copy2(cursor_path, os.path.join(dest_dir, fname))
                applied.append("cursor")
            except Exception:
                pass

        font_path = getattr(w, '_font_path', '')
        if font_path and os.path.isfile(font_path):
            try:
                font_dir = os.path.join(roblox_dir, "content", "fonts")
                os.makedirs(font_dir, exist_ok=True)
                ALL_FONTS = [
                    "GothamSSm-Book.ttf","GothamSSm-BookItalic.ttf","GothamSSm-Medium.ttf","GothamSSm-MediumItalic.ttf",
                    "GothamSSm-Bold.ttf","GothamSSm-BoldItalic.ttf","GothamSSm-Black.ttf","GothamSSm-BlackItalic.ttf",
                    "GothamSSm-Light.ttf","GothamSSm-LightItalic.ttf","GothamSSm-XLight.ttf","GothamSSm-XLightItalic.ttf",
                    "Nunito-Regular.ttf","Nunito-Bold.ttf","Nunito-Italic.ttf","Nunito-BoldItalic.ttf",
                    "Nunito-Light.ttf","Nunito-LightItalic.ttf","Nunito-SemiBold.ttf","Nunito-SemiBoldItalic.ttf",
                    "Nunito-ExtraBold.ttf","Nunito-ExtraBoldItalic.ttf",
                    "BuilderSans-Regular.ttf","BuilderSans-Medium.ttf","BuilderSans-Bold.ttf","BuilderSans-ExtraBold.ttf",
                    "BuilderSans-SemiBold.ttf","BuilderSans-Light.ttf","BuilderSans-Thin.ttf","BuilderSans-Italic.ttf",
                    "BuilderSans-MediumItalic.ttf","BuilderSans-BoldItalic.ttf","BuilderSans-ExtraBoldItalic.ttf",
                    "Roboto-Regular.ttf","Roboto-Bold.ttf","Roboto-Italic.ttf","Roboto-BoldItalic.ttf",
                    "Roboto-Light.ttf","Roboto-LightItalic.ttf","Roboto-Medium.ttf","Roboto-MediumItalic.ttf",
                    "Roboto-Black.ttf","Roboto-BlackItalic.ttf","Roboto-Thin.ttf","Roboto-ThinItalic.ttf",
                    "SourceSansPro-Regular.ttf","SourceSansPro-Bold.ttf","SourceSansPro-Italic.ttf","SourceSansPro-BoldItalic.ttf",
                    "SourceSansPro-Light.ttf","SourceSansPro-LightItalic.ttf","SourceSansPro-Semibold.ttf","SourceSansPro-SemiboldItalic.ttf",
                    "SourceSansPro-Black.ttf","SourceSansPro-BlackItalic.ttf","SourceSansPro-ExtraLight.ttf","SourceSansPro-ExtraLightItalic.ttf",
                    "Inconsolata-Regular.ttf","Inconsolata-Bold.ttf",
                    "TitilliumWeb-Regular.ttf","TitilliumWeb-Bold.ttf","TitilliumWeb-Italic.ttf","TitilliumWeb-BoldItalic.ttf",
                    "TitilliumWeb-Light.ttf","TitilliumWeb-LightItalic.ttf","TitilliumWeb-SemiBold.ttf","TitilliumWeb-SemiBoldItalic.ttf",
                    "TitilliumWeb-ExtraLight.ttf","TitilliumWeb-ExtraLightItalic.ttf","TitilliumWeb-Black.ttf",
                    "Arial.ttf","ArialBold.ttf","HighwayGothic.ttf",
                    "Bangers-Regular.ttf","Creepster-Regular.ttf","DenkOne-Regular.ttf","FredokaOne-Regular.ttf",
                    "Grenze-Regular.ttf","Grenze-Bold.ttf","LuckiestGuy-Regular.ttf",
                    "Merriweather-Regular.ttf","Merriweather-Bold.ttf","Merriweather-Italic.ttf","Merriweather-BoldItalic.ttf",
                    "Merriweather-Light.ttf","Merriweather-LightItalic.ttf","Michroma-Regular.ttf",
                    "Oswald-Regular.ttf","Oswald-Bold.ttf","Oswald-Light.ttf","Oswald-Medium.ttf","Oswald-SemiBold.ttf","Oswald-ExtraLight.ttf",
                    "PermanentMarker-Regular.ttf","Sarpanch-Regular.ttf","Sarpanch-Bold.ttf","Sarpanch-Medium.ttf",
                    "Sarpanch-SemiBold.ttf","Sarpanch-ExtraBold.ttf","Sarpanch-Black.ttf","SpecialElite-Regular.ttf",
                    "Ubuntu-Regular.ttf","Ubuntu-Bold.ttf","Ubuntu-Italic.ttf","Ubuntu-BoldItalic.ttf",
                    "Ubuntu-Light.ttf","Ubuntu-LightItalic.ttf","Ubuntu-Medium.ttf","Ubuntu-MediumItalic.ttf",
                    "Balthazar-Regular.ttf","RomanAntique.ttf",
                    "Jura-Regular.ttf","Jura-Bold.ttf","Jura-Light.ttf","Jura-Medium.ttf","Jura-SemiBold.ttf","Jura-DemiBold.ttf",
                    "AmaticSC-Regular.ttf","AmaticSC-Bold.ttf","Arimo-Regular.ttf","Arimo-Bold.ttf","Arimo-Italic.ttf","Arimo-BoldItalic.ttf",
                    "Gupter-Regular.ttf","Gupter-Bold.ttf","Gupter-Medium.ttf","Fondamento-Regular.ttf","Fondamento-Italic.ttf","Guru.ttf",
                ]
                for fname in ALL_FONTS:
                    dest = os.path.join(font_dir, fname)
                    if os.path.isfile(dest):
                        try: shutil.copy2(font_path, dest)
                        except Exception: pass
                try:
                    for existing in os.listdir(font_dir):
                        if existing.lower().endswith(".ttf") and existing not in ALL_FONTS:
                            try: shutil.copy2(font_path, os.path.join(font_dir, existing))
                            except Exception: pass
                except Exception: pass
                applied.append("font")
            except Exception:
                pass

        if applied:
            self.mods_applied.emit(f"Auto Mods applied: {', '.join(applied)}")
        else:
            self.mods_applied.emit("Auto Mods: nothing to apply (select cursor/font first)")



_FLAG_RISK_RED = frozenset([
    'MaxActiveAnimationTracks', 'AnimationRateLimiterMaxAmount',
    'AnimationRateLimiterAssertAmount', 'SimEnableStepPhysics',
    'SimEnableStepPhysicsSelective', 'SimClearNetworkPhysicsDataForAssembly',
    'PreventReturnOfElevatedPhysicsFPS', 'PhysicsMechanismCacheOptimizeAlloc',
    'DebugReportElevatedPhysicsFPSTOGA', 'SolverStateReplicatedOnly2',
    'RakNetLoopMs', 'RakNetNakResendDelayMs', 'RakNetResendRttMultiple',
    'RakNetNakResendDelayMsMax', 'RakNetSelectTimeoutMs',
    'RaknetBandwidthInfluxHundredthsPercentageV2', 'RakNetDetectNetUnreachable',
    'RakNetUseSlidingWindow4', 'ConnectionMTUSize',
    'TaskSchedulerTargetFps', 'TaskSchedulerLimitTargetFpsTo2402',
    'RemoteEventSingleInvocationSizeLimit',
    'ESGamePerfMonitorEnabled', 'DebugPerfMode',
])

_FLAG_RISK_GREEN = frozenset([
    'DebugSkyGray', 'DisablePostFx', 'NewLightAttenuation',
    'DebugForceFutureIsBrightPhase3', 'DebugGraphicsPreferD3D11',
    'DebugGraphicsPreferD3D11FL10', 'DebugGraphicsPreferVulkan',
    'FastGPULightCulling3', 'FineGrainCull', 'DebugForceFSMCPULightCulling',
    'RenderGpuTextureCompressor', 'DebugCheckRenderThreading',
    'RenderCBRefactor2', 'TextureQualityOverrideEnabled',
    'TextureQualityOverride', 'DebugFRMQualityLevelOverride',
    'DebugTextureManagerSkipMips', 'RenderShadowIntensity',
    'RenderGrassDetailStrands', 'FRMMaxGrassDistance', 'FRMMinGrassDistance',
    'GrassMovementReducedMotionFactor', 'RenderShadowmapBias',
    'TerrainArraySliceSize', 'CSGLevelOfDetailSwitchingDistance',
    'CSGLevelOfDetailSwitchingDistanceL12', 'CSGLevelOfDetailSwitchingDistanceL23',
    'CSGLevelOfDetailSwitchingDistanceL34',
    'AnimationLodFacsDistanceMax', 'AnimationLodFacsDistanceMin',
    'AnimationLodFacsVisibilityDenominator',
    'CameraMaxZoomDistance',
    'PreloadAllFonts', 'PreloadMinimalFonts', 'PreloadTextureItemsOption4',
    'AssetPreloadingIXP', 'EnableSoundPreloading', 'EnableMeshPreloading',
    'AdServiceEnabled', 'VoiceBetaBadge', 'TopBarUseNewBadge',
    'HandleAltEnterFullscreenManually', 'GlobalWindRendering',
    'CloudsReflectOnWater', 'NullCheckCloudsRendering',
    'LightgridCPUAsyncUpdate', 'CommitToGraphicsQualityFix',
    'FixGraphicsQuality', 'ResetCacheOnLeaveGame',
    'GraphicsEnableD3D10Compute',
])

PREFIXES_STRIP = [
    'DFFlagDebug', 'FFlagDebug', 'DFFlag', 'FFlag',
    'DFInt', 'FInt', 'DFString', 'FString',
    'DFLog', 'FLog', 'SFFlag', 'SFInt',
]

def _strip_pfx(name):
    for p in sorted(PREFIXES_STRIP, key=len, reverse=True):
        if name.startswith(p):
            return name[len(p):]
    return name

def _flag_risk(name):
    """Returns 'red', 'yellow', or 'green'."""
    bare = _strip_pfx(name)
    if bare in _FLAG_RISK_RED:
        return 'red'
    if bare in _FLAG_RISK_GREEN:
        return 'green'
    return 'yellow'


class InjectorStatusDialog(QDialog):
    log_line = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SacredWare — Injector Status")
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        self._lines = []
        self._drag_pos = None
        self._build()
        self.log_line.connect(self._append_line)
        self.resize(680, 600)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._drag_pos and e.buttons() == Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, e):
        self._drag_pos = None

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        container = QWidget()
        container.setObjectName("statusContainer")
        container.setStyleSheet("""
            QWidget#statusContainer {
                background-color: #0d0d0d;
                border: 1px solid #1a1a1a;
                border-radius: 12px;
            }
        """)
        outer.addWidget(container)

        main_l = QVBoxLayout(container)
        main_l.setContentsMargins(0, 0, 0, 16)
        main_l.setSpacing(0)

        title_bar = QWidget()
        title_bar.setFixedHeight(48)
        title_bar.setStyleSheet("background: transparent; border-bottom: 1px solid #1a1a1a;")
        tb_l = QHBoxLayout(title_bar)
        tb_l.setContentsMargins(16, 0, 10, 0)
        tb_l.setSpacing(8)

        icon_lbl = QLabel("◈")
        icon_lbl.setStyleSheet("color: #444; font-size: 14px; background: transparent;")
        title_lbl = QLabel("Injector Status")
        title_lbl.setStyleSheet("color: #888; font-size: 12px; font-weight: 600; letter-spacing: 1px; background: transparent;")
        tb_l.addWidget(icon_lbl)
        tb_l.addWidget(title_lbl)
        tb_l.addStretch()

        btn_min_s = QPushButton("—")
        btn_min_s.setFixedSize(32, 24)
        btn_min_s.setStyleSheet("QPushButton { background:transparent; border:none; color:#555; font-size:12px; border-radius:4px; } QPushButton:hover { background:#1a1a1a; color:#fff; }")
        btn_min_s.clicked.connect(self.showMinimized)

        btn_close_s = QPushButton("✕")
        btn_close_s.setFixedSize(32, 24)
        btn_close_s.setStyleSheet("QPushButton { background:transparent; border:none; color:#555; font-size:12px; border-radius:4px; } QPushButton:hover { background:#cc2222; color:#fff; }")
        btn_close_s.clicked.connect(self.close)

        tb_l.addWidget(btn_min_s)
        tb_l.addWidget(btn_close_s)
        main_l.addWidget(title_bar)

        body = QWidget()
        body.setStyleSheet("background: transparent;")
        body_l = QVBoxLayout(body)
        body_l.setContentsMargins(16, 12, 16, 0)
        body_l.setSpacing(8)
        main_l.addWidget(body)

        stats_row = QWidget(); stats_row.setStyleSheet("background:transparent;")
        stats_rl = QHBoxLayout(stats_row)
        stats_rl.setContentsMargins(0, 0, 0, 0)
        stats_rl.setSpacing(10)

        def stat_box(label):
            w = QWidget()
            w.setStyleSheet("background:#111111; border:1px solid #1e1e1e; border-radius:8px;")
            wl = QVBoxLayout(w); wl.setContentsMargins(10, 8, 10, 8); wl.setSpacing(2)
            val = QLabel("—")
            val.setStyleSheet("color:#ffffff; font-size:20px; font-weight:700; background:transparent; border:none;")
            val.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl = QLabel(label)
            lbl.setStyleSheet("color:#444; font-size:9px; font-weight:600; letter-spacing:1.5px; background:transparent; border:none;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            wl.addWidget(val); wl.addWidget(lbl)
            return w, val

        self._stat_total,   self._val_total   = stat_box("TOTAL")
        self._stat_applied, self._val_applied = stat_box("APPLIED")
        self._stat_skipped, self._val_skipped = stat_box("SKIPPED")
        self._stat_offsets, self._val_offsets = stat_box("OFFSETS")
        for w in [self._stat_total, self._stat_applied, self._stat_skipped, self._stat_offsets]:
            stats_rl.addWidget(w)
        body_l.addWidget(stats_row)

        filter_row = QWidget(); filter_row.setStyleSheet("background:transparent;")
        filter_rl = QHBoxLayout(filter_row)
        filter_rl.setContentsMargins(0, 0, 0, 0)
        filter_rl.setSpacing(6)

        lbl_filter = QLabel("Filter:")
        lbl_filter.setStyleSheet("color:#444; font-size:11px; background:transparent;")
        filter_rl.addWidget(lbl_filter)

        def filter_btn(text, color):
            b = QPushButton(text)
            b.setCheckable(True); b.setChecked(True)
            b.setStyleSheet(f"""
                QPushButton {{ background:#111; border:1px solid #1e1e1e; border-radius:6px;
                               color:#444; font-size:11px; padding:3px 12px; }}
                QPushButton:checked {{ background:#1a1a1a; border-color:{color}; color:{color}; }}
                QPushButton:hover {{ border-color:#333; color:#ccc; }}
            """)
            b.toggled.connect(self._refresh_log)
            return b

        self._btn_applied = filter_btn("✓ Applied", "#44aa44")
        self._btn_skipped = filter_btn("✗ Skipped", "#cc4444")
        self._btn_info    = filter_btn("ℹ Info",    "#4a8fd4")
        self._btn_warn    = filter_btn("⚠ Warn",    "#cc8833")
        for b in [self._btn_applied, self._btn_skipped, self._btn_info, self._btn_warn]:
            filter_rl.addWidget(b)
        filter_rl.addStretch()

        btn_clear = QPushButton("Clear")
        btn_clear.setStyleSheet(_DLG_BTN)
        btn_clear.setFixedWidth(70)
        btn_clear.clicked.connect(self._clear_log)
        btn_copy = QPushButton("Copy All")
        btn_copy.setStyleSheet(_DLG_BTN)
        btn_copy.setFixedWidth(90)
        btn_copy.clicked.connect(self._copy_log)
        filter_rl.addWidget(btn_clear)
        filter_rl.addWidget(btn_copy)
        body_l.addWidget(filter_row)

        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setMinimumHeight(300)
        self._log.setStyleSheet("""
            QTextEdit {
                background-color: #111111; border: 1px solid #1e1e1e;
                border-radius: 8px; color: #cccccc;
                font-family: 'Cascadia Code', 'Fira Code', Consolas, monospace;
                font-size: 12px; padding: 10px;
            }
            QScrollBar:vertical { background:#111; width:4px; border-radius:2px; }
            QScrollBar::handle:vertical { background:#2a2a2a; border-radius:2px; min-height:20px; }
            QScrollBar::handle:vertical:hover { background:#444; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }
        """)
        body_l.addWidget(self._log)

        leg_row = QWidget(); leg_row.setStyleSheet("background:transparent;")
        leg_l = QHBoxLayout(leg_row)
        leg_l.setContentsMargins(0, 4, 0, 0)
        leg_l.setSpacing(14)

        def legend_item(color, text):
            w = QWidget(); w.setStyleSheet("background:transparent;")
            wl = QHBoxLayout(w); wl.setContentsMargins(0,0,0,0); wl.setSpacing(5)
            dot = QLabel("●"); dot.setStyleSheet(f"color:{color}; font-size:11px; background:transparent;")
            lbl = QLabel(text); lbl.setStyleSheet("color:#444; font-size:10px; background:transparent;")
            wl.addWidget(dot); wl.addWidget(lbl)
            return w

        leg_l.addWidget(legend_item("#44cc44", "Safe / cosmetic"))
        leg_l.addWidget(legend_item("#ccaa33", "Standard flag"))
        leg_l.addWidget(legend_item("#cc4444", "Use with caution"))
        leg_l.addStretch()
        self._lbl_meta = QLabel("")
        self._lbl_meta.setStyleSheet("color:#333; font-size:10px; background:transparent;")
        self._lbl_meta.setAlignment(Qt.AlignmentFlag.AlignRight)
        leg_l.addWidget(self._lbl_meta)
        body_l.addWidget(leg_row)

        self._update_stats()

    def _flag_dot(self, name, category):
        if category not in ('applied', 'skipped'):
            return ""
        risk = _flag_risk(name)
        color = {"green": "#44cc44", "yellow": "#ccaa33", "red": "#cc4444"}[risk]
        return f'<span style="color:{color};font-size:13px;">●</span> '

    @pyqtSlot(str, str)
    def _append_line(self, text, category):
        self._lines.append((text, category))
        self._update_stats()
        self._refresh_log()

    def _refresh_log(self):
        show = set()
        if self._btn_applied.isChecked(): show.add('applied')
        if self._btn_skipped.isChecked(): show.add('skipped')
        if self._btn_info.isChecked():    show.add('info')
        if self._btn_warn.isChecked():    show.add('warn')
        show.add('err')
        html_parts = []
        for text, cat in self._lines:
            if cat not in show:
                continue
            if cat == 'applied':
                dot = self._flag_dot(text.split()[-1] if text.split() else text, cat)
                color, prefix = "#448844", "✓"
            elif cat == 'skipped':
                dot = self._flag_dot(text.split()[-1] if text.split() else text, cat)
                color, prefix = "#884444", "✗"
            elif cat == 'info':
                dot, color, prefix = "", "#4a6a8a", "ℹ"
            elif cat == 'warn':
                dot, color, prefix = "", "#886633", "⚠"
            else:
                dot, color, prefix = "", "#884444", "✗"
            escaped = text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
            html_parts.append(
                f'<div style="margin:1px 0;line-height:1.6;">{dot}'
                f'<span style="color:{color};">{prefix}</span>&nbsp;'
                f'<span style="color:#888;font-size:11px;">{escaped}</span></div>'
            )
        self._log.setHtml(
            '<div style="font-family:Cascadia Code,Fira Code,Consolas,monospace;font-size:12px;">'
            + ''.join(html_parts) + '</div>'
        )
        sb = self._log.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _update_stats(self):
        applied = sum(1 for _, c in self._lines if c == 'applied')
        skipped = sum(1 for _, c in self._lines if c == 'skipped')
        total   = applied + skipped
        self._val_total.setText(str(total) if total else "—")
        self._val_applied.setText(str(applied) if applied else "—")
        self._val_skipped.setText(str(skipped) if skipped else "—")
        try:
            from core.injector import _ACTIVE_OFFSET_COUNT, _TO_VALUE
            n = _ACTIVE_OFFSET_COUNT
            self._val_offsets.setText(str(n) if n else "—")
            self._lbl_meta.setText(f"ToValue=0x{_TO_VALUE:X}  ·  {n} offsets")
        except:
            pass

    def _clear_log(self):
        self._lines.clear()
        self._log.clear()
        for v in [self._val_total, self._val_applied, self._val_skipped]:
            v.setText("—")

    def _copy_log(self):
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText('\n'.join(t for t, _ in self._lines))

    def push(self, text, category='info'):
        self.log_line.emit(text, category)

    def push_apply_result(self, result_str, all_flags, skipped_list):
        import datetime
        self.push(f"── Apply run ──────────────── {datetime.datetime.now().strftime('%H:%M:%S')}", 'info')
        skipped_set = set(skipped_list)
        for name in all_flags:
            if name not in skipped_set:
                self.push(name, 'applied')
        for name in skipped_list:
            self.push(name, 'skipped')
        self.push(result_str, 'info')


BUILTIN_PRESETS.append({
    'name': "Acqua fflag 1",
    'desc': "175 flags",
    'flags': {'FLogNetwork': '7', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntTextureQualityOverride': '0', 'FFlagDebugDynamicRenderKiloPixels': '30', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDisablePostFx': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntTerrainArraySliceSize': '8', 'FIntDebugForceMSAASamples': '0', 'DFFlagDisableDPIScale': 'True', 'DFIntTaskSchedulerTargetFps': '9999', 'FIntRenderShadowIntensity': '0', 'DFIntCanHideGuiGroupId': '32380007', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'FFlagPreloadMinimalFonts': 'True', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FStringTerrainMaterialTable2022': '', 'FFlagEnableBetaBadgeLearnMore': 'false', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FFlagEnableMenuModernizationABTest': 'False', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'FFlagRenderCheckThreading': 'True', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'FFlagRenderPerformanceTelemetry': 'False', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'FFlagEnableBubbleChatConfigurationV2': 'False', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagEnableAudioOutputDevice': 'false', 'FFlagEnableQuickGameLaunch': 'False', 'DFFlagESGamePerfMonitorEnabled': 'False', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'FIntDefaultMeshCacheSizeMB': '256', 'FFlagEnableReportAbuseMenuRoact2': 'false', 'FFlagEnableMenuModernizationABTest2': 'False', 'FFlagCloudsReflectOnWater': 'False', 'FFlagEnableBubbleChatFromChatService': 'False', 'FIntDebugTextureManagerSkipMips': '100000000', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagAdServiceEnabled': 'False', 'DFStringHttpPointsReporterUrl': 'null', 'DFStringLightstepHTTPTransportUrlPath': 'null', 'DFStringRobloxAnalyticsURL': 'null', 'DFStringTelegrafHTTPTransportUrl': 'null', 'DFStringTelemetryV2Url': 'null', 'FFlagEnableInGameMenuChromeABTest2': 'False', 'FStringGamesUrlPath': '/games/', 'DFIntLightstepHTTPTransportHundredthsPercent2': '0', 'FFlagPreloadAllFonts': 'True', 'FStringCoreScriptBacktraceErrorUploadToken': 'null', 'DFFlagEnableLightstepReporting2': 'False', 'DFIntS2PhysicsSenderRate': '100', 'DFStringAltTelegrafHTTPTransportUrl': 'null', 'DFStringAltHttpPointsReporterUrl': 'null', 'FFlagFixGraphicsQuality': 'True', 'DFStringAnalyticsEventStreamUrlEndpoint': 'null', 'DFStringCrashUploadToBacktraceMacPlayerToken': 'null', 'DFStringCrashUploadToBacktraceBaseUrl': 'null', 'DFStringLightstepHTTPTransportUrlHost': 'null', 'DFStringLightstepToken': 'null', 'FFlagEnableReportAbuseMenuRoactABTest2': 'False', 'FIntRobloxGuiBlurIntensity': '0', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FIntFRMMinGrassDistance': '0', 'FIntFRMMaxGrassDistance': '0', 'FFlagUISUseLastFrameTimeInUpdateInputSignal': 'True', 'FFlagSimAdaptiveMinorOptimizations': 'True', 'FFlagPushFrameTimeToHarmony': 'True', 'FFlagOptimizeServerTickRate': 'True', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagOptimizeNetwork': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagMSRefactor5': 'False', 'FFlagGameBasicSettingsFramerateCap2': 'True', 'DFIntVisibilityCheckRayCastLimitPerFrame': '10', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntRakNetResendRttMultiple': '1', 'DFIntRakNetLoopMs': '1', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntPhysicsReceiveNumParallelTasks': '12', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntNetworkSchemaCompressionRatio': '100', 'DFIntNetworkLatencyTolerance': '1', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntMaxFrameBufferSize': '4', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntConnectionMTUSize': '900', 'DFIntBufferCompressionLevel': '0', 'DFIntAnimatorThrottleMaxFramesToSkip': '1', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagDebugDisableTelemetryPoint': 'True', 'DFIntCodecMaxOutgoingFrames': '10000', 'FFlagFastGPULightCulling3': 'True', 'DFIntTextureCompositorActiveJobs': '0', 'FFlagEnableAccessibilitySettingsAPIV2': 'True', 'FIntRenderGrassHeightScaler': '0', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFStringCrashUploadToBacktraceWindowsPlayerToken': 'null', 'DFIntOptimizePingThreshold': '50', 'DFIntAnimationLodFacsDistanceMin': '0', 'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'True', 'FFlagNullCheckCloudsRendering': 'True', 'FIntSimWorldTaskQueueParallelTasks': '12', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'FIntRakNetResendBufferArrayLength': '128', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFFlagEnableDynamicHeadByDefault': 'False', 'FIntCameraMaxZoomDistance': '99999', 'DFIntNetworkPrediction': '120', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFFlagDebugPauseVoxelizer': 'True', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2': 'True', 'DFIntServerTickRate': '60', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntAnimationLodFacsDistanceMax': '0', 'FIntRenderGrassDetailStrands': '0', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'FFlagDebugGraphicsPreferVulkan': 'True', 'DFIntDebugFRMQualityLevelOverride': '1', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '12', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '12', 'FFlagEnableAccessibilitySettingsInExperienceMenu2': 'True', 'FFlagDebugSkyWhite': 'True', 'FFlagOptimizeNetworkRouting': 'True', 'DFIntBufferCompressionThreshold': '100', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagChatTranslationSettingEnabled3': 'False', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntReplicationDataCacheNumParallelTasks': '12', 'DFIntMegaReplicatorNumParallelTasks': '12', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'FFlagEnableInGameMenuControls': 'False', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FIntReportDeviceInfoRollout': '0', 'FIntRenderLocalLightFadeInMs_enabled': '99999', 'FFlagVoiceBetaBadge': 'false', 'FIntRenderLocalLightUpdatesMax': '1', 'FFlagDontCreatePingJob': 'True', 'FFlagTopBarUseNewBadge': 'false', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FIntStartupInfluxHundredthsPercentage': '0', 'FFlagEnableV3MenuABTest3': 'False', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagEnableInGameMenuModernization': 'False', 'FFlagCommitToGraphicsQualityFix': 'True', 'FStringTerrainMaterialTablePre2022': '', 'DFFlagDebugPerfMode': 'True', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FFlagGlobalWindRendering': 'false', 'FFlagEnableMenuControlsABTest': 'False', 'FIntRenderShadowmapBias': '0', 'FFlagDebugRenderingSetDeterministic': 'True', 'DebugDisplayFPS': 'True'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Aizen fflags (No Animations)",
    'desc': "108 flags",
    'flags': {'DebugGraphicPreferD3D11': 'True', 'DebugGraphicsDisableOpenGL': 'True', 'DebugGraphicsDisableVulkan': 'True', 'DebugGraphicsDisableVulkan11': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagEnableDynamicHeadByDefault': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntAnimatorThrottleMaxFramesToSkip': '1', 'DFIntBufferCompressionLevel': '0', 'DFIntBufferCompressionThreshold': '100', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntConnectionMTUSize': '900', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '2', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '3', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntMaxFrameBufferSize': '4', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntMegaReplicatorNumParallelTasks': '12', 'DFIntMinimalNetworkPrediction': '0.1', 'DFIntNetworkLatencyTolerance': '1', 'DFIntNetworkPrediction': '120', 'DFIntNetworkSchemaCompressionRatio': '100', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntOptimizePingThreshold': '50', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '12', 'DFIntPhysicsReceiveNumParallelTasks': '12', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntRakNetLoopMs': '1', 'DFIntRakNetResendRttMultiple': '1', 'DFIntReplicationDataCacheNumParallelTasks': '12', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntServerTickRate': '60', 'DFIntTextureCompositorActiveJobs': '0', 'DFIntTextureQualityOverride': '0', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'DFIntVisibilityCheckRayCastLimitPerFrame': '10', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FFlagChatTranslationSettingEnabled3': 'False', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDebugDisableTelemetryV2Event': 'True', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FFlagDebugSkyGray': 'False', 'FFlagDisablePostFx': 'True', 'FFlagEnableAccessibilitySettingsAPIV2': 'True', 'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2': 'True', 'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'True', 'FFlagEnableAccessibilitySettingsInExperienceMenu2': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagGameBasicSettingsFramerateCap2': 'True', 'FFlagMSRefactor5': 'False', 'FFlagNewLightAttenuation': 'True', 'FFlagOptimizeNetwork': 'True', 'FFlagOptimizeNetworkRouting': 'True', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagOptimizeServerTickRate': 'True', 'FFlagPushFrameTimeToHarmony': 'True', 'FFlagSimAdaptiveMinorOptimizations': 'True', 'FFlagUISUseLastFrameTimeInUpdateInputSignal': 'True', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FIntRakNetResendBufferArrayLength': '128', 'FIntRenderGrassDetailStrands': '0', 'FIntRenderGrassHeightScaler': '0', 'FIntRobloxGuiBlurIntensity': '0', 'FIntSimWorldTaskQueueParallelTasks': '12', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '12', 'FIntTerrainArraySliceSize': '8', 'RakNetClockDriftAdjustmentPerPingMillisecond': '100', 'DFIntMaxActiveAnimationTracks': '1', 'DFIntAnimationRateLimiterMaxAmount': '0', 'DFIntAnimationRateLimiterSeconds': '0', 'FFlagAnimationLodBoneEnabled': 'False', 'FFlagAnimationLodIkEnabled': 'False', 'DFIntAnimationLodDerivativeGainThousandths': '0', 'DFIntAnimationLodIntegralGainThousandths': '0', 'DFIntAnimationLodProportionalGainThousandths': '0', 'DFIntAnimationLodConfigVersion': '999', 'DFIntAnimationLodBoneLocomotionFixMaxDepth': '0', 'DFFlagAllowRegistrationOfAnimationClipInCoreScripts': 'True', 'DFFlagAnimationRigThrowAssertionErrors2': 'False'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Box Fast Flags",
    'desc': "8 flags",
    'flags': {'DebugLimitMinTextureResolutionWhenSkipMips': '2147483647', 'DoNotSkipMipsBasedOnSystemMemoryPS': 'True', 'TM2SkipMipsForUnstreamable2': 'True', 'RenderUseTextureManager224': 'False', 'DebugTextureManagerSkipMips': '3', 'EnablePowerTraceModule': 'True', 'IncludePowerSaverMode': 'True', 'DebugFRMQualityLevelOverride': '1'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Comp fflags V2",
    'desc': "106 flags",
    'flags': {'FLogNetwork': '7', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'false', 'DFIntCanHideGuiGroupId': '32380007', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'DFFlagDisableDPIScale': 'True', 'DFIntTaskSchedulerTargetFps': '160', 'FIntRenderShadowIntensity': '0', 'FFlagDisablePostFx': 'True', 'FIntTerrainArraySliceSize': '8', 'FIntDebugForceMSAASamples': '0', 'DFIntTextureQualityOverride': '3', 'FFlagDebugGraphicsPreferD3D11': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagDebugForceFutureIsBrightPhase2': 'True', 'FIntFontSizePadding': '4', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagAntiCheatBypassForceLogout': 'True', 'FIntFRMMaxGrassDistance': '0', 'FFlagAntiCheatHideModifiedFiles': 'True', 'FStringPartTexturePackTablePre2022': '{\\u0022foil\\u0022:{\\u0022ids\\u0022:[\\u0022rbxassetid://9873266399\\u0022', 'FFlagMSRefactor5': 'False', 'FIntRenderGrassDensityMax': '0', 'DFIntDebugFRMQualityLevelOverride': '1', 'FFlagEnableInGameMenuChromeABTest3': 'False', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'FFlagEnableInGameMenuControls': 'True', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagAntiCheatBypassMemoryScan': 'True', 'FFlagAntiCheatReduceDetectionRate': 'True', 'FFlagAntiCheatRandomizedBehavior': 'True', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FIntFRMMinGrassDistance': '0', 'FFlagDebugDeterministicParticles': 'False', 'FFlagAntiCheatAutoReconnectOnKick': 'True', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagAntiCheatBypassSpeedCheck': 'True', 'FFlagAntiCheatBypassInstantKillDetection': 'True', 'FFlagAntiCheatBypass': 'True', 'FFlagAntiCheatFakeLegitStatus': 'True', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'FFlagAntiCheatBypassWalkSpeedCheck': 'True', 'FFlagAntiCheatDisableHeartbeatCheck': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'FFlagDebugForceFSMCPULightCulling': 'True', 'DFIntMaxFrameBufferSize': '4', 'FFlagAdServiceEnabled': 'False', 'FFlagAntiCheatBypassAimAssistDetection': 'True', 'FFlagAntiCheatBypassScriptDetection': 'True', 'FFlagAntiCheatHideFromSpectators': 'True', 'FFlagAntiCheatBypassDamageModification': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '3', 'FFlagAntiCheatAutoBypassNewDetectionMethods': 'True', 'FFlagFixParticleEmissionBias': 'False', 'FFlagDebugDisplayFPS': 'False', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FFlagFastGPULightCulling3': 'True', 'FFlagAntiCheatDisableReportSystem': 'True', 'FFlagAntiCheatDisableLogs': 'True', 'FFlagGlobalWindRendering': 'False', 'FFlagAntiCheatBypassAutoFarmDetection': 'True', 'FFlagAntiCheatDisableDetection': 'True', 'FFlagAntiCheatDelayFlagging': 'True', 'FFlagEnableMenuControlsABTest': 'False', 'FFlagEnableMenuModernizationABTest2': 'False', 'DFIntConnectionMTUSize': '900', 'FFlagLuaAppSystemBar': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4', 'FIntRenderShadowmapBias': '0', 'FFlagNewLightAttenuation': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagFixOutdatedParticles': 'False', 'FFlagEnableMenuModernizationABTest': 'False', 'FFlagFixGraphicsQuality': 'True', 'FFlagAntiCheatNoBan': 'True', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FFlagAntiCheatBypassAntiTeleport': 'True', 'FFlagFixParticleAttachmentCulling': 'False', 'FFlagAntiCheatRemoveSuspiciousActivity': 'True', 'FFlagEnableV3MenuABTest3': 'False', 'FFlagFixOutdatedTimeScaleParticles': 'False', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'FIntRenderGrassDensityMin': '0', 'FFlagGlobalWindActivated': 'False', 'FFlagEnableInGameMenuModernization': 'True', 'FFlagAntiCheatBypassNoClipDetection': 'True', 'FFlagAntiCheatBypassHitboxModification': 'True', 'FIntRenderGrassDetailStrands': '0', 'FFlagAntiCheatBypassServerChecks': 'True', 'FFlagAntiCheatBypassAbilitySpamCheck': 'True', 'FFlagAntiCheatAutoReconnectOnBan': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '2', 'FFlagAntiCheatNoKick': 'True', 'FFlagEnableInGameMenuChrome': 'True', 'FIntDebugTextureManagerSkipMips': '8', 'FIntRobloxGuiBlurIntensity': '0', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagAntiCheatBypassJumpPowerCheck': 'True', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'FFlagAntiCheatBypassTeleportDetection': 'True', 'FFlagDisableNewIGMinDUA': 'True'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "EggusPrime's fflags",
    'desc': "172 flags",
    'flags': {'FLogNetwork': '7', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntTextureQualityOverride': '0', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDisablePostFx': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntTerrainArraySliceSize': '8', 'FIntDebugForceMSAASamples': '0', 'DFFlagDisableDPIScale': 'True', 'DFIntTaskSchedulerTargetFps': '9999', 'FIntRenderShadowIntensity': '0', 'DFIntCanHideGuiGroupId': '32380007', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'FFlagPreloadMinimalFonts': 'True', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FStringTerrainMaterialTable2022': '', 'FFlagEnableBetaBadgeLearnMore': 'false', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FFlagEnableMenuModernizationABTest': 'False', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'FFlagRenderCheckThreading': 'True', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'FFlagRenderPerformanceTelemetry': 'False', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'FFlagEnableBubbleChatConfigurationV2': 'False', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagEnableAudioOutputDevice': 'false', 'FFlagEnableQuickGameLaunch': 'False', 'DFFlagESGamePerfMonitorEnabled': 'False', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'FIntDefaultMeshCacheSizeMB': '256', 'FFlagEnableReportAbuseMenuRoact2': 'false', 'FFlagEnableMenuModernizationABTest2': 'False', 'FFlagCloudsReflectOnWater': 'False', 'FFlagEnableBubbleChatFromChatService': 'False', 'FIntDebugTextureManagerSkipMips': '100000000', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagAdServiceEnabled': 'False', 'DFStringHttpPointsReporterUrl': 'null', 'DFStringLightstepHTTPTransportUrlPath': 'null', 'DFStringRobloxAnalyticsURL': 'null', 'DFStringTelegrafHTTPTransportUrl': 'null', 'DFStringTelemetryV2Url': 'null', 'FFlagEnableInGameMenuChromeABTest2': 'False', 'FStringGamesUrlPath': '/games/', 'DFIntLightstepHTTPTransportHundredthsPercent2': '0', 'FFlagPreloadAllFonts': 'True', 'FStringCoreScriptBacktraceErrorUploadToken': 'null', 'DFFlagEnableLightstepReporting2': 'False', 'DFIntS2PhysicsSenderRate': '100', 'DFStringAltTelegrafHTTPTransportUrl': 'null', 'DFStringAltHttpPointsReporterUrl': 'null', 'FFlagFixGraphicsQuality': 'True', 'DFStringAnalyticsEventStreamUrlEndpoint': 'null', 'DFStringCrashUploadToBacktraceMacPlayerToken': 'null', 'DFStringCrashUploadToBacktraceBaseUrl': 'null', 'DFStringLightstepHTTPTransportUrlHost': 'null', 'DFStringLightstepToken': 'null', 'FFlagEnableReportAbuseMenuRoactABTest2': 'False', 'FIntRobloxGuiBlurIntensity': '0', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FIntFRMMinGrassDistance': '0', 'FIntFRMMaxGrassDistance': '0', 'FFlagUISUseLastFrameTimeInUpdateInputSignal': 'True', 'FFlagSimAdaptiveMinorOptimizations': 'True', 'FFlagPushFrameTimeToHarmony': 'True', 'FFlagOptimizeServerTickRate': 'True', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagOptimizeNetwork': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagMSRefactor5': 'False', 'FFlagGameBasicSettingsFramerateCap2': 'True', 'DFIntVisibilityCheckRayCastLimitPerFrame': '10', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntRakNetResendRttMultiple': '1', 'DFIntRakNetLoopMs': '1', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntPhysicsReceiveNumParallelTasks': '12', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntNetworkSchemaCompressionRatio': '100', 'DFIntNetworkLatencyTolerance': '1', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntMaxFrameBufferSize': '4', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntConnectionMTUSize': '900', 'DFIntBufferCompressionLevel': '0', 'DFIntAnimatorThrottleMaxFramesToSkip': '1', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagDebugDisableTelemetryPoint': 'True', 'DFIntCodecMaxOutgoingFrames': '10000', 'FFlagFastGPULightCulling3': 'True', 'DFIntTextureCompositorActiveJobs': '0', 'FFlagEnableAccessibilitySettingsAPIV2': 'True', 'FIntRenderGrassHeightScaler': '0', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFStringCrashUploadToBacktraceWindowsPlayerToken': 'null', 'DFIntOptimizePingThreshold': '50', 'DFIntAnimationLodFacsDistanceMin': '0', 'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'True', 'FFlagNullCheckCloudsRendering': 'True', 'FIntSimWorldTaskQueueParallelTasks': '12', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'FIntRakNetResendBufferArrayLength': '128', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFFlagEnableDynamicHeadByDefault': 'False', 'FIntCameraMaxZoomDistance': '99999', 'DFIntNetworkPrediction': '120', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFFlagDebugPauseVoxelizer': 'True', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2': 'True', 'DFIntServerTickRate': '60', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntAnimationLodFacsDistanceMax': '0', 'FIntRenderGrassDetailStrands': '0', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'FFlagDebugGraphicsPreferVulkan': 'True', 'DFIntDebugFRMQualityLevelOverride': '1', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '12', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '12', 'FFlagEnableAccessibilitySettingsInExperienceMenu2': 'True', 'FFlagDebugSkyGray': 'False', 'FFlagOptimizeNetworkRouting': 'True', 'DFIntBufferCompressionThreshold': '100', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagChatTranslationSettingEnabled3': 'False', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntReplicationDataCacheNumParallelTasks': '12', 'DFIntMegaReplicatorNumParallelTasks': '12', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'FFlagEnableInGameMenuControls': 'False', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FIntReportDeviceInfoRollout': '0', 'FIntRenderLocalLightFadeInMs_enabled': '99999', 'FFlagVoiceBetaBadge': 'false', 'FIntRenderLocalLightUpdatesMax': '1', 'FFlagDontCreatePingJob': 'True', 'FFlagTopBarUseNewBadge': 'false', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FIntStartupInfluxHundredthsPercentage': '0', 'FFlagEnableV3MenuABTest3': 'False', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagEnableInGameMenuModernization': 'False', 'FFlagCommitToGraphicsQualityFix': 'True', 'FStringTerrainMaterialTablePre2022': '', 'DFFlagDebugPerfMode': 'True', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FFlagGlobalWindRendering': 'false', 'FFlagEnableMenuControlsABTest': 'False', 'FIntRenderShadowmapBias': '0'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "HasnBOT's 0 delay fflags (New and best one here)",
    'desc': "138 flags",
    'flags': {'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagDisableDPIScale': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntTextureQualityOverride': '0', 'FIntDebugTextureManagerSkipMips': '3', 'FFlagGlobalWindRendering': 'false', 'FFlagDisableChromeFollowupFTUX': 'True', 'TerrainArraySliceSize': '0', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagEnableV3MenuABTest3': 'False', 'FIntRenderLocalLightFadeInMs_enabled': '99999', 'FFlagFixGraphicsQuality': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FIntStartupInfluxHundredthsPercentage': '0', 'FIntDefaultMeshCacheSizeMB': '256', 'FFlagNewLightAttenuation': 'True', 'FIntUITextureMaxRenderTextureSize': '1024', 'FFlagEnableQuickGameLaunch': 'False', 'TextureCompositorActiveJobs': '0', 'DFIntConnectionMTUSize': '1380', 'FIntCameraMaxZoomDistance': '99999', 'FFlagPreloadTextureItemsOption4': 'True', 'FIntFontSizePadding': '3', 'FFlagEnableMenuModernizationABTest': 'False', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FFlagEnableInGameMenuModernization': 'False', 'FFlagDontCreatePingJob': 'True', 'TextureQualityOverrideEnabled': 'True', 'FFlagRenderCheckThreading': 'True', 'FFlagCommitToGraphicsQualityFix': 'True', 'FIntFRMMinGrassDistance': '0', 'FFlagMSRefactor5': 'False', 'FFlagLightgridCPUAsyncUpdate': 'True', 'FIntReportDeviceInfoRollout': '0', 'FFlagDebugDisableOTAMaterialTexture': 'true', 'FIntTerrainOTAMaxTextureSize': '1024', 'FFlagNullCheckCloudsRendering': 'True', 'DFIntBulletContactBreakOrthogonalThresholdActivatePercent': '2147483647', 'FIntRenderShadowmapBias': '0', 'FIntFRMMaxGrassDistance': '0', 'FIntDebugForceMSAASamples': '0', 'FFlagDisableChromeDefaultOpen': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagDisableChromeFollowupOcclusion': 'True', 'FFlagPreloadMinimalFonts': 'True', 'TextureQualityOverride': '0', 'FStringPartTexturePackTable2022': '{\r\n        "foil":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[238,238,238,255]},\r\n        "asphalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[227,227,228,234]},\r\n        "basalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[160,160,158,238]},\r\n        "brick":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[229,214,205,227]},\r\n        "cobblestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[218,219,219,243]},\r\n        "concrete":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[225,225,224,255]},\r\n        "crackedlava":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[76,79,81,156]},\r\n        "diamondplate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[210,210,210,255]},\r\n        "fabric":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[221,221,221,255]},\r\n        "glacier":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[225,229,229,243]},\r\n        "glass":{"ids":["rbxassetid://9873284556","rbxassetid://9438453972"],"color":[254,254,254,7]},\r\n        "granite":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[210,206,200,255]},\r\n        "grass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[196,196,189,241]},\r\n        "ground":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[165,165,160,240]},\r\n        "ice":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[235,239,241,248]},\r\n        "leafygrass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[182,178,175,234]},\r\n        "limestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[250,248,243,250]},\r\n        "marble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[181,183,193,249]},\r\n        "metal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[226,226,226,255]},\r\n        "mud":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[193,192,193,252]},\r\n        "pavement":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[218,218,219,236]},\r\n        "pebble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[204,203,201,234]},\r\n        "plastic":{"ids":["","rbxassetid://0"],"color":[255,255,255,255]},\r\n        "rock":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[211,211,210,248]},\r\n        "corrodedmetal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[206,177,163,180]},\r\n        "salt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[249,249,249,255]},\r\n        "sand":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[218,216,210,240]},\r\n        "sandstone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[241,234,230,246]},\r\n        "slate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[235,234,235,254]},\r\n        "snow":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[239,240,240,255]},\r\n        "wood":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[217,209,208,255]},\r\n        "woodplanks":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[207,208,206,254]}\r\n    }', 'FIntTerrainArraySliceSize': '8', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntRenderLocalLightUpdatesMax': '1', 'DFIntRakNetResendRttMultiple': '1', 'TM2SkipMipsForUnstreamable2': 'True', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FLogNetwork': '7', 'FFlagTopBarUseNewBadge': 'false', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagDisablePostFx': 'True', 'RenderShadowmapBias': '75', 'IncludePowerSaverMode': 'True', 'FIntRobloxGuiBlurIntensity': '0', 'FFlagCloudsReflectOnWater': 'False', 'FFlagDisableChromePinnedChat': 'True', 'FIntRenderGrassDetailStrands': '0', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagEnableAudioOutputDevice': 'false', 'FFlagDisableChromeUnibar': 'True', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagVoiceBetaBadge': 'false', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FIntRenderGrassHeightScaler': '0', 'FFlagEnableMenuControlsABTest': 'False', 'FFlagEnableInGameMenuControls': 'False', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagEnableReportAbuseMenuRoact2': 'false', 'FFlagPreloadAllFonts': 'True', 'FFlagRenderPerformanceTelemetry': 'False', 'FFlagEnableInGameMenuChromeABTest2': 'False', 'FFlagEnableBetaBadgeLearnMore': 'false', 'FFlagAdServiceEnabled': 'False', 'FIntRenderShadowIntensity': '0', 'FFlagDisableChromeFollowupUnibar': 'True', 'FFlagDebugDisableTelemetryV2Event': 'True', 'FFlagChatTranslationSettingEnabled3': 'false', 'FFlagLuaAppSystemBar': 'False', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'FFlagEnableBubbleChatConfigurationV2': 'False', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FFlagEnableBubbleChatFromChatService': 'False', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'EnablePowerTraceModule': 'True', 'DFIntCanHideGuiGroupId': '32380007', 'DisablePostFx': 'True', 'FFlagEnableMenuModernizationABTest2': 'False', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagInGameMenuV1FullScreenTitleBar': 'False', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2': 'true', 'FFlagEnableReportAbuseMenuRoactABTest2': 'False', 'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'true', 'DoNotSkipMipsBasedOnSystemMemoryPS': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagEnableAccessibilitySettingsInExperienceMenu2': 'true', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'FFlagEnableAccessibilitySettingsAPIV2': 'true', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'DFIntTextureCompositorActiveJobs': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFFlagDebugPerfMode': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFFlagESGamePerfMonitorEnabled': 'False', 'DFFlagDebugEnableInterpolationVisualizer': 'true', 'DebugForceFSMCPULightCulling': 'True', 'DebugLimitMinTextureResolutionWhenSkipMips': '9999999999999999', 'CSGLevelOfDetailSwitchingDistanceL23': '0', 'CSGLevelOfDetailSwitchingDistance': '0', 'CSGLevelOfDetailSwitchingDistanceL34': '0', 'CSGLevelOfDetailSwitchingDistanceL12': '0', 'FStringTerrainMaterialTable2022': '', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'RenderUseTextureManager224': 'False', 'PerformanceControlTextureQualityBestUtility': '-1', 'FStringPartTexturePackTablePre2022': '{\r\n        "foil":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255,255,255,255]},\r\n        "brick":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[204,201,200,232]},\r\n        "cobblestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[212,200,187,250]},\r\n        "concrete":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[208,208,208,255]},\r\n        "diamondplate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[170,170,170,255]},\r\n        "fabric":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[105,104,102,244]},\r\n        "glass":{"ids":["rbxassetid://7547304948","rbxassetid://7546645118"],"color":[254,254,254,7]},\r\n        "granite":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[113,113,113,255]},\r\n        "grass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[165,165,159,255]},\r\n        "ice":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255,255,255,255]},\r\n        "marble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[199,199,199,255]},\r\n        "metal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[199,199,199,255]},\r\n        "pebble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[208,208,208,255]},\r\n        "corrodedmetal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[159,119,95,200]},\r\n        "sand":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[220,220,220,255]},\r\n        "slate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[193,193,193,255]},\r\n        "wood":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[227,227,227,255]},\r\n        "woodplanks":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[212,209,203,255]},\r\n        "asphalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[123,123,123,234]},\r\n        "basalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[154,154,153,238]},\r\n        "crackedlava":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[74,78,80,156]},\r\n        "glacier":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[226,229,229,243]},\r\n        "ground":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[114,114,112,240]},\r\n        "leafygrass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[121,117,113,234]},\r\n        "limestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[235,234,230,250]},\r\n        "mud":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[130,130,130,252]},\r\n        "pavement":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[142,142,144,236]},\r\n        "rock":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[154,154,154,248]},\r\n        "salt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[220,220,221,255]},\r\n        "sandstone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[174,171,169,246]},\r\n        "snow":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[218,218,218,255]}\r\n    }', 'FStringTerrainMaterialTablePre2022': ''},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "HasnBOT's old fflags",
    'desc': "155 flags",
    'flags': {'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFIntMaxWaitTimeBeforeForcePacketProcessMS': '1', 'DFFlagSampleAndRefreshRakPing': 'True', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FStringErrorUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntMemCacheMaxCapacityMB': '2147483647', 'DFIntGraphicsOptimizationModeFRMFrameRateTarget': '240', 'FIntDefaultMeshCacheSizeMB': '256', 'FFlagAdServiceEnabled': 'False', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntMegaReplicatorNumParallelTasks': '4', 'FIntRenderGrassDetailStrands': '0', 'DFFlagRakNetUseSlidingWindow4': 'True', 'DFIntClientPacketMinMicroseconds': '1', 'FStringPerformanceSendMeasurementAPISubdomain': 'opt-out', 'FIntFRMMinGrassDistance': '0', 'FFlagReportGpuLimitedToPerfControl': 'False', 'FFlagNewLightAttenuation': 'True', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntFRMMaxGrassDistance': '0', 'DFStringAnalyticsEventStreamUrlEndpoint': 'opt-out', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'FIntDebugForceMSAASamples': '4', 'FFlagDebugNextGenReplicatorEnabledWriteCFrameColor': 'True', 'DFIntRakNetNakResendDelayMs': '1', 'FIntRenderShadowmapBias': '0', 'DFIntMaxProcessPacketsJobScaling': '5000000', 'FStringTerrainMaterialTable2022': '', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'DFIntTaskSchedulerJobInitThreads': '4', 'DFIntUserIdPlayerNameCacheSize': '33554432', 'DFIntRakNetLoopMs': '1', 'FIntTaskSchedulerMaxTempArenaSizeBytes': '2147483647', 'DFIntSignalRCoreKeepAlivePingPeriodMs': '250', 'DFStringAltHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntNetworkClusterPacketCacheNumParallelTasks': '4', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '1', 'FFlagDebugRenderingSetDeterministic': 'True', 'FFlagPreloadTextureItemsOption4': 'True', 'DFIntFileCacheReserveSize': '2147483647', 'DFIntSignalRCoreRpcQueueSize': '256', 'DFIntSignalRCoreTimerMs': '750', 'DFIntClientPacketMaxFrameMicroseconds': '200', 'DFIntTaskSchedulerTargetFps': '2147483647', 'DFIntRakNetMinAckGrowthPercent': '0', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFFlagDebugVisualizeAllPropertyChanges': 'True', 'FIntRakNetDatagramMessageIdArrayLength': '1024', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntClientPacketMaxDelayMs': '1', 'DFIntRakNetResendRttMultiple': '1', 'FIntFontSizePadding': '3', 'FIntTerrainArraySliceSize': '0', 'FFlagNewCameraControls_SpeedAdjustEnum': 'False', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntMaxFrameBufferSize': '4', 'FFlagDebugGraphicsPreferD3D11': 'True', 'DFFlagDebugPerfMode': 'True', 'DFIntBandwidthManagerApplicationDefaultBps': '1024000', 'FIntBootstrapperTelemetryReportingHundredthsPercentage': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '1', 'FFlagVoiceBetaBadge': 'False', 'FFlagEnableInGameMenuChromeABTest4': 'False', 'DFIntClientPacketExcessMicroseconds': '1000', 'FFlagFastGPULightCulling3': 'True', 'FFlagResetCacheOnLeaveGame': 'True', 'DFIntPerformanceControlReportingPeriodInMs': '700', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'FIntTaskSchedulerAutoThreadLimit': '4', 'DFIntRuntimeConcurrency': '4', 'FFlagSpecifyNetworkReplicatorScope': 'True', 'DFIntSignalRHubConnectionBaseRetryTimeMs': '100', 'FIntRenderLocalLightUpdatesMin': '1', 'DFIntSignalRCoreServerTimeoutMs': '11100', 'DFIntSignalRHubConnectionHeartbeatTimerRateMs': '1000', 'DFIntPerformanceControlFrameTimeMax': '4', 'DFIntDebugPerformanceControlFrameTime': '2', 'FFlagGameBasicSettingsFramerateCap5': 'False', 'FIntDebugTextureManagerSkipMips': '7', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagTopBarUseNewBadge': 'True', 'DFIntTouchSenderMaxBandwidthBps': '-1', 'DFFlagRakNetEnablePoll': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'DFFlagTeleportClientAssetPreloadingEnabledIXP2': 'True', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntRakNetSelectTimeoutMs': '1', 'DFFlagDisableDPIScale': 'True', 'DFIntCanHideGuiGroupId': '32380007', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '4', 'FFlagDebugGraphicsPreferVulkan': 'True', 'DFFlagDebugEnableInterpolationVisualizer': 'TRUE', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'FFlagReconnectDisabled': 'True', 'FFlagSpecifyNetworkReplicatorScopeForItems': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '1', 'DFIntConnectionMTUSize': '1472', 'DFStringRobloxAnalyticsSubDomain': 'opt-out', 'DFIntRakNetNakResendDelayRttPercent': '50', 'FIntRenderShadowIntensity': '0', 'FLogNetwork': '7', 'DFIntReplicationDataCacheNumParallelTasks': '4', 'FIntLuaGcParallelMinMultiTasks': '4', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'FIntEnableCullableScene2HundredthPercent3': '1000', 'DFIntS2PhysicsSenderRate': '35000', 'DFIntRakNetMtuValue1InBytes': '1280', 'DFIntTaskSchedulerJobInGameThreads': '4', 'DFStringHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFIntMaxProcessPacketsStepsAccumulated': '5', 'FFlagPreloadAllFonts': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'DFStringCrashUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'DFFlagDebugSkipMeshVoxelizer': 'True', 'DFIntVoiceChatVolumeThousandths': '6000', 'DFIntDebugFRMQualityLevelOverride': '1', 'FIntEmotesAnimationsPerPlayerCacheSize': '16777216', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'DFIntCodecMaxOutgoingFrames': '10000', 'FIntCameraMaxZoomDistance': '99999', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FIntRobloxGuiBlurIntensity': '0', 'FFlagFixTextureCompositorFramebufferManagement2': 'True', 'DFIntRakNetMtuValue3InBytes': '1200', 'DFIntTeleportClientAssetPreloadingHundredthsPercentage2': '1000', 'DFIntBandwidthManagerDataSenderMaxWorkCatchupMs': '8', 'DFIntTaskSchedulerBackgroundCycleRateMs': '1', 'FIntRakNetResendBufferArrayLength': '1024', 'DFStringRobloxAnalyticsURL': 'http://opt-out.roblox.com', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FFlagDebugRenderCollectGpuCounters': 'True', 'DFIntNumAssetsMaxToPreload': '9999999', 'DFIntRakNetNakResendDelayMsMax': '100', 'FFlagDisablePostFx': 'True', 'FFlagEnableCommandAutocomplete': 'False', 'FIntRuntimeMaxNumOfThreads': '2400', 'FStringTerrainMaterialTablePre2022': '', 'DFFlagTeleportClientAssetPreloadingDoingExperiment2': 'True', 'FIntTaskSchedulerThreadMin': '3', 'DFIntReportOutputDeviceInfoRateHundredthsPercentage': '0', 'DFIntReportRecordingDeviceInfoRateHundredthsPercentage': '0', 'DFIntRakNetMtuValue2InBytes': '1240', 'FFlagDebugGraphicsPreferOpenGL': 'True', 'DFIntClientPacketHealthyAllocationPercent': '20', 'FFlagTouchscreenSupport5': 'True', 'DFFlagHttpSslCertCacheEnabled3': 'True', 'DFFlagAlwaysSkipDiskCache': 'False', 'DFIntRemoteEventSingleInvocationSizeLimit': '2900'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Himitsu FFLags 2 (pretty good)",
    'desc': "156 flags",
    'flags': {'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagDebugPhysicsSenderDoesNotShrinkSimRadius': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFFlagDebugSkipMeshVoxelizer': 'True', 'DFFlagEnableMeshPreloading2': 'True', 'DFFlagEnableSoundPreloading': 'True', 'DFFlagFastEndUpdateLoop': 'True', 'DFFlagNetworkUseZstdWrapper': 'False', 'DFFlagRakNetCalculateApplicationFeedback2': 'False', 'DFFlagRakNetEnablePoll': 'True', 'DFFlagSimDcdRecompUseClosedVoxel4': 'True', 'DFFlagSimOptimizeSetSize': 'True', 'DFFlagSimSkipVoxelCDECMerge': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagUseVisBugChecks': 'True', 'DFFlagVoxelizerDisableTerrainSIMD': 'True', 'DFIntAnimatorThrottleMaxFramesToSkip': '1', 'DFIntAssetPreloading': '9999999', 'DFIntBufferCompressionLevel': '0', 'DFIntBufferCompressionThreshold': '100', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntClientNetworkInfluxHundredthsPercentage': '0', 'DFIntClusterCompressionLevel': '0', 'DFIntClusterEstimatedCompressionRatioHundredths': '0', 'DFIntClusterSenderMaxJoinBandwidthBps': '2100000000', 'DFIntClusterSenderMaxUpdateBandwidthBps': '2100000000', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntGameNetCompressionLodByteBudgetThresholdPct': '0', 'DFIntHttpRbxApiClientPerMinuteRequestLimit': '60', 'DFIntHttpRbxApiJobFrequencyInSeconds': '60', 'DFIntHttpRbxApiMaxBudgetMultiplier': '2', 'DFIntHttpRbxApiMaxRetryBudgetPerMinute': '60', 'DFIntHttpRbxApiMaxRetryCount': '3', 'DFIntHttpRbxApiMaxRetryQueueSize': '1000', 'DFIntHttpRbxApiMaxSyncRetries': '3', 'DFIntJoinDataCompressionLevel': '0', 'DFIntJoinDataItemEstimatedCompressionRatioHundreths': '0', 'DFIntMaxClientSimulationRadius': '2147000000', 'DFIntMaxFrameBufferSize': '4', 'DFIntMegaReplicatorNumParallelTasks': '20', 'DFIntMinClientSimulationRadius': '2147000000', 'DFIntMinimalSimRadiusBuffer': '2147000000', 'DFIntNetworkSchemaCompressionRatio': '0', 'DFIntNumAssetsMaxToPreload': '9999999', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '20', 'DFIntPhysicsReceiveNumParallelTasks': '20', 'DFIntRakNetApplicationFeedbackMaxSpeedBPS': '0', 'DFIntRakNetApplicationFeedbackScaleUpFactorHundredthPercent': '0', 'DFIntRakNetApplicationFeedbackScaleUpThresholdPercent': '0', 'DFIntRakNetLoopMs': '1', 'DFIntRakNetMinAckGrowthPercent': '0', 'DFIntRakNetMtuValue1InBytes': '1200', 'DFIntRakNetNakResendDelayMs': '1', 'DFIntRakNetNakResendDelayMsMax': '1', 'DFIntRakNetResendRttMultiple': '1', 'DFIntRakNetSelectTimeoutMs': '1', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntReplicationDataCacheNumParallelTasks': '20', 'DFIntRuntimeConcurrency': '9', 'DFIntS2PhysicsSenderRate': '250', 'DFIntSendGameServerDataMaxLen': '2147483647', 'DFIntSendItemLimit': '2147483647', 'DFIntSendRakNetStatsInterval': '2147483647', 'DFIntServerBandwidthPlayerSampleRate': '2147483647', 'DFIntServerBandwidthPlayerSampleRateFacsOverride': '2147483647', 'DFIntServerFramesBetweenJoins': '1', 'DFIntServerRakNetBandwidthPlayerSampleRate': '2147483647', 'DFIntTaskSchedulerTargetFps': '9999', 'DFIntTextureQualityOverride': '1', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntTouchSenderMaxBandwidthBps': '950000', 'DFIntTouchSenderMaxBandwidthBpsScaling': '950000', 'DFIntTrackCountryRegionAPIHundredthsPercent': '10000', 'DFIntVisibilityCheckRayCastLimitPerFrame': '10', 'FFlagAdServiceEnabled': 'False', 'FFlagAddHapticsToggle': 'False', 'FFlagAlwaysShowVRToggleV3': 'False', 'FFlagChatTranslationSettingEnabled3': 'False', 'FFlagDataModelPatcherForceLocal': 'True', 'FFlagDebugCheckRenderThreading': 'True', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDebugDisableTelemetryV2Event': 'True', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagDebugDisplayFPS': 'True', 'FFlagDebugForceFutureIsBrightPhase2': 'False', 'FFlagDebugForceFutureIsBrightPhase3': 'False', 'FFlagDebugGraphicsPreferD3D11': 'False', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'FFlagDebugRenderingSetDeterministic': 'True', 'FFlagDebugSSAOForce': 'True', 'FFlagDisableFeedbackSoothsayerCheck': 'False', 'FFlagDisablePostFx': 'True', 'FFlagEnableHamburgerIcon': 'False', 'FFlagEnableQuickGameLaunch': 'True', 'FFlagEnableVisBugChecks27': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagGameBasicSettingsFramerateCap5': 'False', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagHighlightOutlinesOnMobile': 'True', 'FFlagLuaAppLegacyInputSettingRefactor': 'True', 'FFlagPushFrameTimeToHarmony': 'True', 'FFlagRenderDebugCheckThreading2': 'True', 'FFlagRenderEnableGlobalInstancingD3D10': 'True', 'FFlagRenderEnableGlobalInstancingD3D11': 'False', 'FFlagRenderLegacyShadowsQualityRefactor': 'True', 'FFlagRenderShadowSkipHugeCulling': 'True', 'FFlagRenderSkipReadingShaderData': 'True', 'FFlagRenderUnifiedLighting12': 'True', 'FFlagSimCSGV3IncrementalTriangulationStreamingCompression': 'False', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagToastNotificationsProtocolEnabled2': 'False', 'FFlagUISUseLastFrameTimeInUpdateInputSignal': 'True', 'FFlagUserHideCharacterParticlesInFirstPerson': 'True', 'FFlagUserShowGuiHideToggles': 'True', 'FFlagUserUpdateInputConnections': 'True', 'FFlagVisBugChecksThreadYield': 'True', 'FIntActivatedCountTimerMSKeyboard': '0', 'FIntActivatedCountTimerMSMouse': '0', 'FIntCLI20390_2': '0', 'FIntDebugForceMSAASamples': '1', 'FIntDebugTextureManagerSkipMips': '3', 'FIntDirectionalAttenuationMaxPoints': '1', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntPerformanceControlStaticTextureQualityBestUtility': '-1', 'FIntRakNetResendBufferArrayLength': '1000', 'FIntRenderGrassDetailStrands': '0', 'FIntRenderLocalLightFadeInMs': '0', 'FIntRenderLocalLightUpdatesMax': '8', 'FIntRenderLocalLightUpdatesMin': '6', 'FIntRenderMaxShadowAtlasUsageBeforeDownscale': '1', 'FIntRenderShadowIntensity': '0', 'FIntRenderShadowmapBias': '-1', 'FIntRobloxGuiBlurIntensity': '0', 'FIntRomarkStartWithGraphicQualityLevel': '6', 'FIntSSAOMipLevels': '1', 'FIntSimWorldTaskQueueParallelTasks': '20', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '20', 'FIntTaskSchedulerThreadMin': '10', 'FIntTerrainArraySliceSize': '0', 'FIntUnifiedLightingBlendZone': '1', 'FIntV1MenuLanguageSelectionFeaturePerMillageRollout': '0', 'FLogNetwork': '7'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Ryzon Flags",
    'desc': "99 flags",
    'flags': {'FIntDebugForceMSAASamples': '0', 'FFlagEnableMenuModernizationABTest2': 'False', 'DFFlagDisableDPIScale': 'True', 'FIntRenderLocalLightFadeInMs_enabled': '99999', 'FFlagEnableAudioOutputDevice': 'false', 'FIntUITextureMaxRenderTextureSize': '1024', 'FIntRenderGrassDetailStrands': '0', 'FFlagGlobalWindRendering': 'false', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagCloudsReflectOnWater': 'False', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'FFlagEnableMenuModernizationABTest': 'False', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'FFlagEnableQuickGameLaunch': 'False', 'DFIntAnimationLodFacsDistanceMin': '1', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagMSRefactor5': 'False', 'FFlagRenderCheckThreading': 'True', 'FIntFRMMinGrassDistance': '0', 'FIntStartupInfluxHundredthsPercentage': '0', 'DFIntTaskSchedulerTargetFps': '9999', 'FFlagEnableBubbleChatConfigurationV2': 'False', 'DFFlagESGamePerfMonitorEnabled': 'False', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FFlagFixGraphicsQuality': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FintRenderGrassHeightScaler': '0', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagPreloadTextureItemsOption4': 'True', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagEnableMenuControlsABTest': 'False', 'FIntRenderShadowIntensity': '0', 'FIntLightingDefaultClearColorARGB': 'True;255', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FStringTerrainMaterialTablePre2022': '', 'FFlagDebugDisableTelemetryEventIngest': 'False', 'DFFlagDebugPerfMode': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FFlagTopBarUseNewBadge': 'false', 'FFlagVoiceBetaBadge': 'false', 'FFlagDebugSkyGray': 'True', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'FFlagDebugDisableOTAMaterialTexture': 'true', 'FIntRenderShadowmapBias': '0', 'FFlagDisablePostFx': 'True', 'FFlagEnableBubbleChatFromChatService': 'False', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagRenderPerformanceTelemetry': 'False', 'FIntDefaultMeshCacheSizeMB': '256', 'FStringTerrainMaterialTable2022': '', 'FStringPartTexturePackTable2022': '{\\u0022foil\\u0022:{\\u0022ids\\u0022:[\\u0022rbxassetid://0\\u0022', 'FIntRobloxGuiBlurIntensity': '0', 'FFlagCommitToGraphicsQualityFix': 'True', 'FIntFRMMaxGrassDistance': '1', 'FFlagPreloadMinimalFonts': 'True', 'FFlagEnableInGameMenuControls': 'False', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FIntFlagUpdateVersion': 'Bhaggo', 'FFlagAdServiceEnabled': 'False', 'FIntTerrainOTAMaxTextureSize': '1024', 'FFlagFastGPULightCulling3': 'True', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FFlagPreloadAllFonts': 'True', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagEnableBetaBadgeLearnMore': 'false', 'FFlagEnableInGameMenuChromeABTest2': 'False', 'FFlagDebugDisableTelemetryEphemeralStat': 'False', 'FFlagDebugDisableTelemetryPoint': 'False', 'FFlagDontCreatePingJob': 'True', 'FStringPartTexturePackTablePre2022': '{\\u0022foil\\u0022:{\\u0022ids\\u0022:[\\u0022rbxassetid://0\\u0022', 'FFlagNewLightAttenuation': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FIntReportDeviceInfoRollout': '0', 'FFlagEnableInGameMenuModernization': 'False', 'FFlagEnableReportAbuseMenuRoact2': 'false', 'FFlagEnableReportAbuseMenuRoactABTest2': 'False', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FFlagEnableV3MenuABTest3': 'False', 'FIntCameraMaxZoomDistance': '99999', 'FFlagDebugDisableTelemetryV2Event': 'False', 'FFlagNullCheckCloudsRendering': 'True', 'FIntTerrainArraySliceSize': '8', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'DFIntAnimationLodFacsDistanceMax': '1', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntTextureQualityOverride': '2', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '1', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntRenderLocalLightUpdatesMin': '1', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntTextureCompositorActiveJobs': '0'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Sendo Fast Flags",
    'desc': "96 flags",
    'flags': {'DebugGraphicPreferD3D11': 'true', 'DebugGraphicsDisableOpenGL': 'true', 'DebugGraphicsDisableVulkan': 'true', 'DebugGraphicsDisableVulkan11': 'true', 'DFFlagDebugPauseVoxelizer': 'true', 'DFFlagEnableDynamicHeadByDefault': 'false', 'DFFlagTextureQualityOverrideEnabled': 'true', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntAnimatorThrottleMaxFramesToSkip': '1', 'DFIntBufferCompressionLevel': '0', 'DFIntBufferCompressionThreshold': '100', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntConnectionMTUSize': '900', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '2', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '3', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntMaxFrameBufferSize': '4', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntMegaReplicatorNumParallelTasks': '12', 'DFIntMinimalNetworkPrediction': '0.1', 'DFIntNetworkLatencyTolerance': '1', 'DFIntNetworkPrediction': '120', 'DFIntNetworkSchemaCompressionRatio': '100', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntOptimizePingThreshold': '50', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '12', 'DFIntPhysicsReceiveNumParallelTasks': '12', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntRakNetLoopMs': '1', 'DFIntRakNetResendRttMultiple': '1', 'DFIntReplicationDataCacheNumParallelTasks': '12', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntServerTickRate': '60', 'DFIntTextureCompositorActiveJobs': '0', 'DFIntTextureQualityOverride': '0', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'DFIntVisibilityCheckRayCastLimitPerFrame': '10', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FFlagChatTranslationSettingEnabled3': 'false', 'FFlagDebugDisableTelemetryEphemeralCounter': 'true', 'FFlagDebugDisableTelemetryEphemeralStat': 'true', 'FFlagDebugDisableTelemetryEventIngest': 'true', 'FFlagDebugDisableTelemetryPoint': 'true', 'FFlagDebugDisableTelemetryV2Counter': 'true', 'FFlagDebugDisableTelemetryV2Event': 'true', 'FFlagDebugDisableTelemetryV2Stat': 'true', 'FFlagDebugGraphicsPreferD3D11': 'true', 'FFlagDebugGraphicsPreferVulkan': 'true', 'FFlagDebugSkyGray': 'false', 'FFlagDisablePostFx': 'true', 'FFlagEnableAccessibilitySettingsAPIV2': 'true', 'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2': 'true', 'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'true', 'FFlagEnableAccessibilitySettingsInExperienceMenu2': 'true', 'FFlagFastGPULightCulling3': 'true', 'FFlagGameBasicSettingsFramerateCap2': 'true', 'FFlagMSRefactor5': 'false', 'FFlagNewLightAttenuation': 'true', 'FFlagOptimizeNetwork': 'true', 'FFlagOptimizeNetworkRouting': 'true', 'FFlagOptimizeNetworkTransport': 'true', 'FFlagOptimizeServerTickRate': 'true', 'FFlagPushFrameTimeToHarmony': 'true', 'FFlagSimAdaptiveMinorOptimizations': 'true', 'FFlagUISUseLastFrameTimeInUpdateInputSignal': 'true', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FIntRakNetResendBufferArrayLength': '128', 'FIntRenderGrassDetailStrands': '0', 'FIntRenderGrassHeightScaler': '0', 'FIntRobloxGuiBlurIntensity': '0', 'FIntSimWorldTaskQueueParallelTasks': '12', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '12', 'FIntTerrainArraySliceSize': '8', 'RakNetClockDriftAdjustmentPerPingMillisecond': '100'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Sendo Fflags V2 (Old)",
    'desc': "194 flags",
    'flags': {'FLogNetwork': '7', 'DFIntTaskSchedulerTargetFps': '5588562', 'DFFlagDisableDPIScale': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FIntDebugForceMSAASamples': '1', 'DFIntTextureQualityOverride': '0', 'FFlagDebugGraphicsPreferD3D11FL10': 'false', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FFlagDisablePostFx': 'True', 'FIntRenderShadowIntensity': '0', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'FIntTerrainArraySliceSize': '0', 'DFIntCanHideGuiGroupId': '32380007', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagDebugForceFutureIsBrightPhase2': 'True', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FIntFontSizePadding': '3', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'DFIntOptimizePingThreshold': '50', 'DFFlagSimReportCPUInfo': 'False', 'FFlagDebugGraphicsPreferOpenGL': 'True', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'FFlagFastGPULightCulling3': 'True', 'DFIntLightstepHTTPTransportHundredthsPercent2': '0', 'FIntBootstrapperTelemetryReportingHundredthsPercentage': '0', 'DFFlagDebugVisualizerTrackRotationPredictions': 'True', 'FFlagDebugSkyGray': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FIntRenderLocalLightUpdatesMin': '1', 'FFlagOptimizeServerTickRate': 'True', 'FIntFRMMaxGrassDistance': '0', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FStringInGameMenuChromeForcedUserIds': '1353919681', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntS2PhysicsSenderRate': '35000', 'FFlagFixGraphicsQuality': 'True', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'DFIntRakNetLoopMs': '1', 'DFIntNetworkPrediction': '120', 'DFIntRakNetNakResendDelayMs': '10', 'FFlagOptimizeNetworkRouting': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagDebugGraphicsDisableDirect3D11': 'False', 'FFlagEnableV3MenuABTest3': 'False', 'FFlagOptimizeNetwork': 'True', 'DFIntUserIdPlayerNameCacheSize': '33554432', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'FIntRenderGrassHeightScaler': '0', 'FFlagEnableInGameMenuChromeABTest3': 'False', 'DFFlagDebugVisualizeAllPropertyChanges': 'True', 'FFlagRenderCheckThreading': 'True', 'FIntCameraMaxZoomDistance': '99999', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FFlagEnableMenuControlsABTest': 'False', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FIntTerrainOTAMaxTextureSize': '1024', 'DFFlagDebugVisualizationImprovements': 'True', 'DFIntDebugFRMQualityLevelOverride': '3', 'DFIntHardwareTelemetryHundredthsPercent': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '1', 'FFlagEnableInGameMenuModernization': 'True', 'DFIntReportRecordingDeviceInfoRateHundredthsPercentage': '0', 'DFIntRakNetNakResendDelayRttPercent': '50', 'FFlagEnableInGameMenuChrome': 'True', 'DFIntPlayerNetworkUpdateRate': '60', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagDisableNewIGMinDUA': 'True', 'FIntFRMMinGrassDistance': '0', 'FFlagEnableQuickGameLaunch': 'False', 'FFlagPreloadAllFonts': 'True', 'FStringErrorUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFFlagDebugEnableInterpolationVisualize': 'true', 'FFlagOptimizeNetworkTransport': 'True', 'DFFlagDebugEnableInterpolationVisualizer': 'TRUE', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'FFlagDebugDisableTelemetryV2Event': 'True', 'FFlagEnableMenuModernizationABTest': 'False', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FIntEmotesAnimationsPerPlayerCacheSize': '16777216', 'FStringPartTexturePackTable2022': '{\\u0022glass\\u0022:{\\u0022ids\\u0022:[\\u0022rbxassetid://9873284556\\u0022', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'DFIntCodecMaxOutgoingFrames': '10000', 'FFlagEnableInGameMenuControls': 'True', 'DFStringAltTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'FStringPerformanceSendMeasurementAPISubdomain': 'opt-out', 'FIntRenderGrassDetailStrands': '0', 'FFlagDebugDisplayFPS': 'True', 'FFlagEnableMenuModernizationABTest2': 'False', 'FFlagTopBarUseNewBadge': 'True', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'FIntRakNetResendBufferArrayLength': '1024', 'DFIntRakNetResendRttMultiple': '1', 'DFIntMaxFrameBufferSize': '4', 'DFIntGoogleAnalyticsLoadPlayerHundredth': '0', 'FFlagSimIslandizerManager': 'false', 'FFlagReconnectDisabled': 'True', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntServerTickRate': '60', 'DFIntNetworkLatencyTolerance': '1', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FFlagGameBasicSettingsFramerateCap5': 'False', 'FIntRobloxGuiBlurIntensity': '0', 'DFLogHttpTraceLight': '0', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDontCreatePingJob': 'True', 'DFFlagEnableFmodErrorsTelemetry': 'False', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'DFIntConnectionMTUSize': '1472', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'FFlagDebugLightGridShowChunks': 'False', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'DFFlagRakNetUseSlidingWindow4': 'True', 'FIntLmsClientRollout2': '0', 'DFIntRakNetMtuValue2InBytes': '1240', 'FFlagLuaAppExitModalDoNotShow': 'True', 'FIntDefaultMeshCacheSizeMB': '256', 'DFStringRobloxAnalyticsSubDomain': 'opt-out', 'FFlagEnableInGameMenuV3': 'True', 'DFFlagEnableGCapsHardwareTelemetry': 'False', 'FFlagCommitToGraphicsQualityFix': 'True', 'DFFlagDebugAnalyticsSendUserId': 'False', 'DFFlagEnableHardwareTelemetry': 'False', 'DFIntRakNetMtuValue3InBytes': '1200', 'FStringCredit': 'Potato Mode | @KiwisASkid on YT', 'FIntRenderShadowmapBias': '0', 'DFStringHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'FIntUITextureMaxRenderTextureSize': '1024', 'FFlagLuaAppSystemBar': 'False', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'DFFlagEnableLightstepReporting2': 'False', 'FStringPartTexturePackTablePre2022': '{\\u0022glass\\u0022:{\\u0022ids\\u0022:[\\u0022rbxassetid://7547304948\\u0022', 'FFlagBatchAssetApi': 'True', 'FIntRakNetDatagramMessageIdArrayLength': '1024', 'FFlagPreloadTextureItemsOption4': 'True', 'DFIntRakNetMtuValue1InBytes': '1280', 'FFlagEnableSoundTelemetry': 'False', 'DFIntRakNetNakResendDelayMsMax': '100', 'FIntRenderLocalLightUpdatesMax': '1', 'DFFlagDebugPauseVoxelizer': 'True', 'DFStringAltHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFStringCrashUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'DFStringAnalyticsEventStreamUrlEndpoint': 'opt-out', 'FFlagLuaAppExitModal2': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '1', 'DFFlagAudioDeviceTelemetry': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagBatchAssetApiNoFallbackOnFail': 'False', 'DFFlagQueueDataPingFromSendData': 'True', 'FFlagAnimationClipMemCacheEnabled': 'True', 'DFStringTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'DFIntReportOutputDeviceInfoRateHundredthsPercentage': '0', 'FFlagInGameMenuV1FullScreenTitleBar': 'False', 'FFlagGpuGeometryManager7': 'True', 'DFStringRobloxAnalyticsURL': 'http://opt-out.roblox.com', 'FFlagAdServiceEnabled': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '1', 'FFlagDebugRenderingSetDeterministic': 'True', 'FIntRomarkStartWithGraphicQualityLevel': '1', 'FIntRuntimeMaxNumOfThreads': '2400', 'FIntTaskSchedulerThreadMin': '3', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'FStringTerrainMaterialTable2022': '', 'FStringTerrainMaterialTablePre2022': '', 'FFlagCloudsReflectOnWater': 'True', 'FFlagEnableCommandAutocomplete': 'False', 'FFlagEnableBetaFacialAnimation2': 'False', 'DFFlagLoadCharacterLayeredClothingProperty2': 'False', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'DFFlagEnableDynamicHeadByDefault': 'False', 'DFIntVoiceChatVolumeThousandths': '6000', 'DFFlagDebugPerfMode': 'True', 'FFlagEnableAccessibilitySettingsAPIV2': 'True', 'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2': 'True', 'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'True', 'FFlagEnableAccessibilitySettingsInExperienceMenu2': 'True', 'FFlagInGameMenuV1ExitModal': 'True', 'FFlagInGameMenuV1LeaveToHome': 'False', 'FFlagVoiceBetaBadge': 'False', 'DFFlagDebugSkipMeshVoxelizer': 'True', 'FIntDebugTextureManagerSkipMips': '2'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Sendo Theme.Optimized.4.Usage(Client_ZoroForm)",
    'desc': "194 flags",
    'flags': {'FLogNetwork': '7', 'DFIntTaskSchedulerTargetFps': '5588562', 'DFFlagDisableDPIScale': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FIntDebugForceMSAASamples': '1', 'DFIntTextureQualityOverride': '0', 'FFlagDebugGraphicsPreferD3D11FL10': 'false', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FFlagDisablePostFx': 'True', 'FIntRenderShadowIntensity': '0', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'FIntTerrainArraySliceSize': '0', 'DFIntCanHideGuiGroupId': '32380007', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagDebugForceFutureIsBrightPhase2': 'True', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FIntFontSizePadding': '3', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'DFIntOptimizePingThreshold': '50', 'DFFlagSimReportCPUInfo': 'False', 'FFlagDebugGraphicsPreferOpenGL': 'True', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'FFlagFastGPULightCulling3': 'True', 'DFIntLightstepHTTPTransportHundredthsPercent2': '0', 'FIntBootstrapperTelemetryReportingHundredthsPercentage': '0', 'DFFlagDebugVisualizerTrackRotationPredictions': 'True', 'FFlagDebugSkyGray': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FIntRenderLocalLightUpdatesMin': '1', 'FFlagOptimizeServerTickRate': 'True', 'FIntFRMMaxGrassDistance': '0', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FStringInGameMenuChromeForcedUserIds': '1353919681', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntS2PhysicsSenderRate': '35000', 'FFlagFixGraphicsQuality': 'True', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'DFIntRakNetLoopMs': '1', 'DFIntNetworkPrediction': '120', 'DFIntRakNetNakResendDelayMs': '10', 'FFlagOptimizeNetworkRouting': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagDebugGraphicsDisableDirect3D11': 'False', 'FFlagEnableV3MenuABTest3': 'False', 'FFlagOptimizeNetwork': 'True', 'DFIntUserIdPlayerNameCacheSize': '33554432', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'FIntRenderGrassHeightScaler': '0', 'FFlagEnableInGameMenuChromeABTest3': 'False', 'DFFlagDebugVisualizeAllPropertyChanges': 'True', 'FFlagRenderCheckThreading': 'True', 'FIntCameraMaxZoomDistance': '99999', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FFlagEnableMenuControlsABTest': 'False', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FIntTerrainOTAMaxTextureSize': '1024', 'DFFlagDebugVisualizationImprovements': 'True', 'DFIntDebugFRMQualityLevelOverride': '3', 'DFIntHardwareTelemetryHundredthsPercent': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '1', 'FFlagEnableInGameMenuModernization': 'True', 'DFIntReportRecordingDeviceInfoRateHundredthsPercentage': '0', 'DFIntRakNetNakResendDelayRttPercent': '50', 'FFlagEnableInGameMenuChrome': 'True', 'DFIntPlayerNetworkUpdateRate': '60', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagDisableNewIGMinDUA': 'True', 'FIntFRMMinGrassDistance': '0', 'FFlagEnableQuickGameLaunch': 'False', 'FFlagPreloadAllFonts': 'True', 'FStringErrorUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFFlagDebugEnableInterpolationVisualize': 'true', 'FFlagOptimizeNetworkTransport': 'True', 'DFFlagDebugEnableInterpolationVisualizer': 'TRUE', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'FFlagDebugDisableTelemetryV2Event': 'True', 'FFlagEnableMenuModernizationABTest': 'False', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FIntEmotesAnimationsPerPlayerCacheSize': '16777216', 'FStringPartTexturePackTable2022': '{\\u0022glass\\u0022:{\\u0022ids\\u0022:[\\u0022rbxassetid://9873284556\\u0022', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'DFIntCodecMaxOutgoingFrames': '10000', 'FFlagEnableInGameMenuControls': 'True', 'DFStringAltTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'FStringPerformanceSendMeasurementAPISubdomain': 'opt-out', 'FIntRenderGrassDetailStrands': '0', 'FFlagDebugDisplayFPS': 'True', 'FFlagEnableMenuModernizationABTest2': 'False', 'FFlagTopBarUseNewBadge': 'True', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'FIntRakNetResendBufferArrayLength': '1024', 'DFIntRakNetResendRttMultiple': '1', 'DFIntMaxFrameBufferSize': '4', 'DFIntGoogleAnalyticsLoadPlayerHundredth': '0', 'FFlagSimIslandizerManager': 'false', 'FFlagReconnectDisabled': 'True', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntServerTickRate': '60', 'DFIntNetworkLatencyTolerance': '1', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FFlagGameBasicSettingsFramerateCap5': 'False', 'FIntRobloxGuiBlurIntensity': '0', 'DFLogHttpTraceLight': '0', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDontCreatePingJob': 'True', 'DFFlagEnableFmodErrorsTelemetry': 'False', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'DFIntConnectionMTUSize': '1472', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'FFlagDebugLightGridShowChunks': 'False', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'DFFlagRakNetUseSlidingWindow4': 'True', 'FIntLmsClientRollout2': '0', 'DFIntRakNetMtuValue2InBytes': '1240', 'FFlagLuaAppExitModalDoNotShow': 'True', 'FIntDefaultMeshCacheSizeMB': '256', 'DFStringRobloxAnalyticsSubDomain': 'opt-out', 'FFlagEnableInGameMenuV3': 'True', 'DFFlagEnableGCapsHardwareTelemetry': 'False', 'FFlagCommitToGraphicsQualityFix': 'True', 'DFFlagDebugAnalyticsSendUserId': 'False', 'DFFlagEnableHardwareTelemetry': 'False', 'DFIntRakNetMtuValue3InBytes': '1200', 'FStringCredit': 'Potato Mode | @KiwisASkid on YT', 'FIntRenderShadowmapBias': '0', 'DFStringHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'FIntUITextureMaxRenderTextureSize': '1024', 'FFlagLuaAppSystemBar': 'False', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'DFFlagEnableLightstepReporting2': 'False', 'FStringPartTexturePackTablePre2022': '{\\u0022glass\\u0022:{\\u0022ids\\u0022:[\\u0022rbxassetid://7547304948\\u0022', 'FFlagBatchAssetApi': 'True', 'FIntRakNetDatagramMessageIdArrayLength': '1024', 'FFlagPreloadTextureItemsOption4': 'True', 'DFIntRakNetMtuValue1InBytes': '1280', 'FFlagEnableSoundTelemetry': 'False', 'DFIntRakNetNakResendDelayMsMax': '100', 'FIntRenderLocalLightUpdatesMax': '1', 'DFFlagDebugPauseVoxelizer': 'True', 'DFStringAltHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFStringCrashUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'DFStringAnalyticsEventStreamUrlEndpoint': 'opt-out', 'FFlagLuaAppExitModal2': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '1', 'DFFlagAudioDeviceTelemetry': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagBatchAssetApiNoFallbackOnFail': 'False', 'DFFlagQueueDataPingFromSendData': 'True', 'FFlagAnimationClipMemCacheEnabled': 'True', 'DFStringTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'DFIntReportOutputDeviceInfoRateHundredthsPercentage': '0', 'FFlagInGameMenuV1FullScreenTitleBar': 'False', 'FFlagGpuGeometryManager7': 'True', 'DFStringRobloxAnalyticsURL': 'http://opt-out.roblox.com', 'FFlagAdServiceEnabled': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '1', 'FFlagDebugRenderingSetDeterministic': 'True', 'FIntRomarkStartWithGraphicQualityLevel': '1', 'FIntRuntimeMaxNumOfThreads': '2400', 'FIntTaskSchedulerThreadMin': '3', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'FStringTerrainMaterialTable2022': '', 'FStringTerrainMaterialTablePre2022': '', 'FFlagCloudsReflectOnWater': 'True', 'FFlagEnableCommandAutocomplete': 'False', 'FFlagEnableBetaFacialAnimation2': 'False', 'DFFlagLoadCharacterLayeredClothingProperty2': 'False', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'DFFlagEnableDynamicHeadByDefault': 'False', 'DFIntVoiceChatVolumeThousandths': '6000', 'DFFlagDebugPerfMode': 'True', 'FFlagEnableAccessibilitySettingsAPIV2': 'True', 'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2': 'True', 'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'True', 'FFlagEnableAccessibilitySettingsInExperienceMenu2': 'True', 'FFlagInGameMenuV1ExitModal': 'True', 'FFlagInGameMenuV1LeaveToHome': 'False', 'FFlagVoiceBetaBadge': 'False', 'DFFlagDebugSkipMeshVoxelizer': 'True', 'FIntDebugTextureManagerSkipMips': '2'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Sinawys fflags",
    'desc': "147 flags",
    'flags': {'DFFlagDebugPerformanceControlEnableMemoryOverrideImGui': 'True', 'DFFlagBrowserTrackerIdTelemetryEnabled': 'False', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagVoxelizerDisableTerrainSIMD': 'True', 'DFFlagFacialAnimationStreaming2': 'False', 'DFFlagESGamePerfMonitorEnabled': 'False', 'DFFlagRakNetUseSlidingWindow4': 'True', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagDisableDPIScale': 'True', 'DFFlagPredictedOOM': 'False', 'DFFlagDebugPerfMode': 'True', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntReportRecordingDeviceInfoRateHundredthsPercentage': '0', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntReportOutputDeviceInfoRateHundredthsPercentage': '0', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'DFIntCrashReportingHundredthsPercentage': '0', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntUserIdPlayerNameCacheSize': '33554432', 'DFIntCrashUploadToBacktracePercentage': '0', 'DFIntRakNetNakResendDelayRttPercent': '50', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntStartupTracingInfluxRollout': '0', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntTextureCompositorActiveJobs': '0', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntRakNetNakResendDelayMsMax': '100', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntRakNetMtuValue2InBytes': '1240', 'DFIntRakNetMtuValue1InBytes': '1280', 'DFIntRakNetMtuValue3InBytes': '1200', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntRakNetNakResendDelayMs': '10', 'DFIntRakNetResendRttMultiple': '1', 'DFIntTextureQualityOverride': '0', 'DFIntS2PhysicsSenderRate': '100', 'DFIntPredictedOOMPercent': '0', 'DFIntConnectionMTUSize': '900', 'DFIntMaxFrameBufferSize': '6', 'DFIntRakNetLoopMs': '1', 'DFStringAnalyticsNS1BeaconConfig': 'https://opt-out.roblox.com', 'DFStringCrashUploadToBacktraceWindowsPlayerToken': 'null', 'DFStringCrashUploadToBacktraceMacPlayerToken': 'null', 'DFStringAnalyticsEventStreamUrlEndpoint': 'null', 'DFStringCrashUploadToBacktraceBaseUrl': 'null', 'DFStringLightstepHTTPTransportUrlPath': 'null', 'DFStringLightstepHTTPTransportUrlHost': 'null', 'DFStringAnalyticsNS1ApplicationId': 'opt-out', 'DFStringRobloxAnalyticsSubDomain': 'opt-out', 'DFStringAltHttpPointsReporterUrl': 'null', 'DFStringHttpPointsReporterUrl': 'null', 'DFStringRobloxAnalyticsURL': 'null', 'DFStringTelemetryV2Url': 'null', 'DFStringLightstepToken': 'null', 'FFlagFacialAnimationStreamingSearchForReplacementWhenRemovingAnimator': 'False', 'FFlagFacialAnimationStreamingServiceUniverseSettingsEnableAudio': 'False', 'FFlagFacialAnimationStreamingServiceUniverseSettingsEnableVideo': 'False', 'FFlagFacialAnimationStreamingValidateAnimatorBeforeRemoving': 'False', 'FFlagFacialAnimationStreamingCheckPauseStateAfterEmote2': 'False', 'FFlagAvatarChatServiceExposeClientFeaturesForVoiceChat': 'False', 'FFlagFacialAnimationStreamingIfNoDynamicHeadDisableA2C': 'False', 'FFlagFacialAnimationStreamingClearTrackImprovementsV2': 'False', 'FFlagFacialAnimationStreamingServiceUserSettingsMock': 'False', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagLocServicePerformanceAnalyticsEnabled': 'False', 'FFlagVoiceChatServiceManagerUseAvatarChat': 'False', 'FFlagFacialAnimationRecordingBetaFeature': 'False', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagEnableBubbleChatFromChatService': 'False', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FFlagChatTranslationSettingEnabled3': 'False', 'FFlagEnableInGameMenuChromeABTest4': 'False', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagDebugRenderingSetDeterministic': 'True', 'FFlagPreloadTextureItemsOption4': 'True', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagEnableInGameMenuChrome': 'False', 'FFlagTrackMacWebLaunchFlow': 'False', 'FFlagFastGPULightCulling3': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagPreloadMinimalFonts': 'True', 'FFlagAdServiceEnabled': 'False', 'FFlagVoiceBetaBadge': 'false', 'FFlagPreloadAllFonts': 'True', 'FFlagDisablePostFx': 'True', 'FFlagDebugSkyGray': 'True', 'FIntBootstrapperTelemetryReportingHundredthsPercentage': '0', 'FIntV1MenuLanguageSelectionFeaturePerMillageRollout': '0', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FIntEmotesAnimationsPerPlayerCacheSize': '16777216', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FIntRakNetDatagramMessageIdArrayLength': '1024', 'FIntLinkBrowserTrackerToDeviceRollout': '0', 'FIntStartupInfluxHundredthsPercentage': '0', 'FIntUITextureMaxRenderTextureSize': '1000', 'FIntRakNetResendBufferArrayLength': '128', 'FIntDebugTextRenderingMaxDistance': '0', 'FIntRenderForceVideoMemorySize': '800', 'FIntDebugTextureManagerSkipMips': '3', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntTerrainOTAMaxTextureSize': '10', 'FIntCameraMaxZoomDistance': '1000', 'FIntRenderGrassDetailStrands': '0', 'FIntDefaultMeshCacheSizeMB': '256', 'FIntRenderLocalLightFadeInMs': '1', 'FIntReportDeviceInfoRollout': '0', 'FIntRobloxGuiBlurIntensity': '0', 'FIntRenderShadowIntensity': '0', 'FIntTerrainArraySliceSize': '0', 'FIntDebugForceMSAASamples': '1', 'FIntRenderShadowmapBias': '0', 'FIntFRMMinGrassDistance': '0', 'FIntFRMMaxGrassDistance': '0', 'FIntLmsClientRollout2': '0', 'FIntFontSizePadding': '2', 'FLogNetwork': '7', 'FStringFacialAnimation1BetaFeatureUrl': 'https://opt-out.roblox.com/', 'FStringErrorUploadToBacktraceBaseUrl': 'https://opt-out.roblox.com', 'FStringPerformanceSendMeasurementAPISubdomain': 'opt-out', 'FStringCoreScriptBacktraceErrorUploadToken': 'null', 'FStringTerrainMaterialTablePre2022': '', 'FStringTerrainMaterialTable2022': '', 'FStringGamesUrlPath': '/games/'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "SkipMips lvl 10",
    'desc': "23 flags",
    'flags': {'TextureCompositorActiveJobs': '0', 'RenderShadowmapBias': '75', 'CSGLevelOfDetailSwitchingDistanceL34': '0', 'CSGLevelOfDetailSwitchingDistanceL23': '0', 'CSGLevelOfDetailSwitchingDistanceL12': '0', 'CSGLevelOfDetailSwitchingDistance': '0', 'TerrainArraySliceSize': '0', 'PerformanceControlTextureQualityBestUtility': '-1', 'RenderUseTextureManager224': 'False', 'IncludePowerSaverMode': 'True', 'EnablePowerTraceModule': 'True', 'DebugForceFSMCPULightCulling': 'True', 'DoNotSkipMipsBasedOnSystemMemoryPS': 'True', 'DebugLimitMinTextureResolutionWhenSkipMips': '9999999999999999', 'TM2SkipMipsForUnstreamable2': 'True', 'DebugTextureManagerSkipMips': '10', 'TextureQualityOverride': '0', 'TextureQualityOverrideEnabled': 'True', 'DisablePostFx': 'True', 'TaskSchedulerTargetFps': '9999999', 'TaskSchedulerLimitTargetFpsTo2402': 'False', 'DebugSkyGray': 'False', 'DFIntDebugTextureManagerSkipMips': '10'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "Womp FFlags",
    'desc': "161 flags",
    'flags': {'DFIntGameNetPVHeaderTranslationZeroCutoffExponent': '-1', 'FFlagDebugCheckRenderThreading': 'True', 'DFFlagAcceleratorUpdateOnPropsAndValueTimeChange': 'True', 'DFIntRakNetMtuValue1InBytes': '1492', 'FIntRuntimeMaxNumOfThreads': '1000000', 'FFlagFasterPreciseTime4': 'True', 'DFFlagGCPolicyFastMode': 'True', 'DFIntRakNetApplicationFeedbackScaleUpFactorHundredthPercent': '0', 'DFFlagSimSmoothedRunningController2': 'True', 'FFlagReduceDirtyFlagSettings': 'True', 'DFIntMaxFrameBufferSize': '4', 'DFIntClientPacketMaxFrameMicroseconds': '200', 'FFlagEnhancedNightVisibility': 'True', 'FFlagCanReplicateContentPropertiesServer': 'True', 'DFIntTargetTimeDelayFacctorTenths': '15', 'DFIntHttpBatchApi_maxWaitMs': '40', 'DFFlagFixNetworkPingSpikes': 'True', 'FIntRuntimeMaxNumOfMutexes': '1000000', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntRakNetSelectTimeoutMs': '1', 'DFIntHttpBatchApi_minWaitMs': '5', 'DFIntCodecMaxOutgoingFrames': '1000', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'FFlagTouchscreenSupport': 'True', 'DFIntInterpolationFrameRotVelocityThresholdMillionth': '0', 'FIntSSAOMipLevels': '0', 'FFlagEnableFastGameJoin': 'True', 'DFIntClientPacketMaxDelayMs': '1', 'DFIntMaxReceiveToDeserializeLatencyMilliseconds': '10', 'FFlagRenderLightSaturateColor': 'True', 'FFlagDebugNextGenReplicatorEnabledWriteCFrameColor': 'True', 'DFFlagClampIncomingReplicationLag': 'True', 'FFlagFixChunkLightingUpdate2': 'True', 'DFFlagReplicatorSeparateVarThresholds': 'True', 'DFFlagHumanoidReplicateSimulated2TurnOffLocalState': 'True', 'FFlagDebugEnableDirectAudioOcclusion2': 'True', 'DFIntMaxNumReplicatorsToDisconnectPerFrame': '2000', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntReplicatorVariantContainerCountLimit': '2147483647', 'FFlagFastGPULightCulling3': 'True', 'FIntRenderShadowIntensity': '0', 'DFIntAssetPreloading': '2147483647', 'DFFlagRakNetEnablePoll': 'True', 'DFFlagRakNetFixBwCollapse': 'True', 'FIntRuntimeMaxNumOfDPCs': '64', 'DFIntConnectionMTUSize': '1472', 'FFlagDebugForceGenerateHSR': 'True', 'DFIntInitialAccelerationLatencyMultTenths': '1', 'DFFlagReplicatorCheckReadTableCollisions': 'True', 'DFIntCodecMaxIncomingPackets': '100', 'DFFlagFixPlayerPhysicsStutter': 'True', 'DFFlagSolverStateReplicatedOnly2': 'True', 'DFIntBandwidthManagerApplicationDefaultBps': '1024000', 'FFlagNextGenReplicatorEnabledRead': 'True', 'DFFlagHumanoidReplicateSimulated2': 'True', 'DFFlagSimOptimizeGeometryChangedAssemblies3': 'True', 'DFFlagGraphicsOptimizationModeMVPExposureEnrollment4': 'False', 'FFlagSortKeyOptimization': 'True', 'FFlagRenderDynamicResolutionScale': 'True', 'DFIntRakNetMtuValue2InBytes': '1516', 'DFIntRakNetResendRttMultiple': '1', 'DFIntTimestepArbiterHumanoidLinearVelThreshold': '1', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntDebugSimPhysicsSteppingMethodOverride': '10000000', 'FFlagHighlightOutlinesOnMobile': 'True', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFIntHttpBatchApi_cacheDelayMs': '15', 'FFlagRenderFixFog': 'True', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFFlagUpdateBoundExtentsForHugeMixedReplicationComponents': 'True', 'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '25', 'DFFlagSimDcdRefactorSetPhysics': 'True', 'DFIntGameNetPVHeaderRotationOrientIdToleranceExponent': '0', 'DFIntServerFramesBetweenJoins': '1', 'DFIntBatchThumbnailResultsSizeCap': '200', 'FFlagLuaAppEnableFoundationColors7': 'True', 'DFIntGameNetPVHeaderLinearVelocityZeroCutoffExponent': '-1', 'DFIntRakNetLoopMs': '1', 'DFIntReplicationVariantLimitHundredthPercent': '0', 'DFIntJoinDataItemEstimatedCompressionRatioHundreths': '0', 'FFlagLargeReplicatorEnabled3': 'True', 'DFIntInterpolationFrameVelocityThresholdMillionth': '0', 'FFlagEnableZstdForClientSettings': 'False', 'DFFlagLightGridSimdNew3': 'True', 'DFIntRakNetMtuValue3InBytes': '1516', 'FIntSmoothMouseSpringFrequencyTenths': '100', 'FFlagDebugRenderCollectGpuCounters': 'True', 'FFlagPreComputeAcceleratorArrayForSharingTimeCurve': 'True', 'DFFlagFixKeyboardInputDelay': 'True', 'DFIntPhysicsFPS': '240', 'DFFlagHighlightOutlinesOnMobile': 'True', 'DFIntRakNetNakResendDelayMs': '1', 'FFlagUISUseLastFrameTimeInUpdateInputSignal': 'True', 'DFIntReplicatorCountLimitInfluxHundrethsPercentage': '0', 'FFlagDebugNextGenRepAttributeRep': 'True', 'DFIntNetworkQualityResponderMaxWaitTime': '1', 'DFIntWaitOnRecvFromLoopEndedMS': '10', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFFlagReplicatorDisKickSize': 'True', 'DFIntVoiceChatVolumeThousandths': '1500', 'FFlagDebugGraphicsPreferD3D11': 'True', 'DFIntGameNetPVHeaderRotationalVelocityZeroCutoffExponent': '-1', 'DFFlagFixSkyBoxTextureBlurrines': 'True', 'FIntRuntimeMaxNumOfLatches': '1000000', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFIntTimestepArbiterHumanoidTurningVelThreshold': '1', 'FIntInterpolationMaxDelayMSec': '100', 'DFIntInterpolationFramePositionThresholdMillionth': '0', 'DFFlagEnableFastGameJoin': 'True', 'FFlagRenderFixBrokenAvatarShadow': 'true', 'DFIntReplicatorVariantKickRateLimitMax': '2147483647', 'DFIntNetworkSendRate': '60', 'FIntRuntimeMaxNumOfSchedulers': '1000000', 'FIntInterpolationAwareTargetTimeLerpHundredth': '40', 'FFlagRenderOptimizeFrameRate': 'True', 'DFIntClusterEstimatedCompressionRatioHundredths': '0', 'DFFlagDebugPerfMode': 'True', 'DFIntMaxDataPacketPerSend': '2147483647', 'DFFlagMergeFakeInputEvents3': 'True', 'DFIntTaskSchedulerTargetFps': '240', 'DFIntBandwidthManagerDataSenderMaxWorkCatchupMs': '8', 'FFlagOptimizeCFrameUpdates': 'True', 'FFlagDisablePostFx': 'True', 'DFIntCameraMaxZoomDistance': '2147483647', 'DFFlagFixMouseInputDelay': 'True', 'DFIntNetworkQualityResponderUnit': '10', 'FFlagEnableInGameMenuDurationLogger': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagLargeReplicatorEnabled2': 'True', 'FIntRuntimeMaxNumOfSemaphores': '1000000', 'FFlagCreationDBCompressRequest': 'False', 'FFlagRenderEnableGlobalInstancingD3D11': 'False', 'DFIntNetworkSchemaCompressionRatio': '0', 'DFIntBufferCompressionLevel': '0', 'FFlagSimDcdEnableDelta2': 'True', 'FFlagUserCameraControlLastInputTypeUpdate': 'False', 'DFFlagMouseMoveOncePerFrame': 'False', 'DFIntReplicationVariantKickLimitBytes': '2147483647', 'DFIntClientNetworkInfluxHundredthsPercentage': '0', 'DFFlagFrameTimeStdDev': 'False', 'DFFlagReplicateCreateToPlayer': 'True', 'FIntCLI20390_2': '0', 'DFIntJoinDataCompressionLevel': '0', 'FIntDefaultJitterN': '0', 'DFFlagNextGenRepRollbackOverbudgetPackets': 'True', 'DFIntRakNetApplicationFeedbackScaleUpThresholdPercent': '0', 'DFFlagDebugParallelLuau': 'True', 'FFlagImproveShiftLockTransition': 'True', 'FIntRenderAmbientLight': '100', 'DFIntNetworkInProcessLimitGameplayMsClient': '0', 'FFlagLargeReplicatorRead2': 'True', 'DFIntClientPacketHealthyAllocationPercent': '20', 'DFIntMaxAcceptableUpdateDelay': '1', 'FIntRuntimeMaxNumOfConditions': '1000000', 'DFIntS2PhysicsSenderRate': '128', 'FLogNetwork': '7', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntClientPacketExcessMicroseconds': '1000', 'FFlagLargeReplicatorWrite2': 'True', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntIncorrectlyPausedReplicationHundredthsPercentage': '0'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "wNegi's Fast Flags",
    'desc': "180 flags",
    'flags': {'FLogNetwork': '7', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntTextureQualityOverride': '3', 'DFIntSmoothTerrainPhysicsRayAabbSlop': '-9999', 'DFIntS2PhysicsSenderRate': '25000', 'DFFlagSimOptimizeSetSize': 'True', 'DFFlagMergeFakeInputEvents3': 'True', 'DFFlagAcceleratorUpdateOnPropsAndValueTimeChange': 'True', 'DFFlagTeleportClientAssetPreloadingDoingExperiment2': 'True', 'FIntRuntimeMaxNumOfSchedulers': '1000000', 'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '25', 'DFFlagReplicatorSeparateVarThresholds': 'True', 'DFIntClientPacketMaxFrameMicroseconds': '200', 'FFlagNewCameraControls_SpeedAdjustEnum': 'False', 'DFIntJoinDataItemEstimatedCompressionRatioHundreths': '0', 'DFIntRakNetNakResendDelayMsMax': '1', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFFlagSimSmoothedRunningController2': 'True', 'DFIntReplicationDataCacheNumParallelTasks': '5', 'DFIntGraphicsOptimizationModeFRMFrameRateTarget': '144', 'DFIntRakNetLoopMs': '1', 'DFFlagCanClientReplicateProp': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'FIntRuntimeMaxNumOfSemaphores': '1000000', 'DFIntTimestepArbiterAccelerationModelFactorThou': '50000', 'DFIntMaxFrameBufferSize': '4', 'DFIntServerBandwidthPlayerSampleRateFacsOverride': '2147483647', 'DFFlagDebugLargeReplicatorForceFullSend': 'true', 'FFlagDebugAvatarChatVisualization': 'True', 'DFFlagTeleportClientAssetPreloadingEnabledIXP2': 'True', 'FFlagEnableZstdForClientSettings': 'False', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'FIntSmoothMouseSpringFrequencyTenths': '100', 'DFIntTouchSenderMaxBandwidthBpsScaling': '2', 'DFFlagCorrectServerReplicatorStatsIP': 'True', 'DFFlagNextGenRepRollbackOverbudgetPackets': 'True', 'FFlagEnableInGameMenuSongbirdABTest': 'False', 'DFIntTaskSchedulerJobInitThreads': '6', 'FIntRobloxGuiBlurIntensity': '0', 'DFFlagRakNetEnablePoll': 'True', 'FIntEnableCullableScene2HundredthPercent3': '1000', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntSendItemLimit': '5', 'DFIntDataSenderRate': '20000', 'DFIntClusterSenderMaxJoinBandwidthBps': '2100000000', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntPhysicsReceiveNumParallelTasks': '5', 'DFIntNetworkClusterPacketCacheNumParallelTasks': '5', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntRuntimeConcurrency': '12', 'DFIntFrameRateMSToReduceTouchEvents': '30', 'DFIntClusterCompressionLevel': '0', 'DFFlagAnimatorEnableNewAdornments': 'True', 'DFFlagJointIrregularityOptimization': 'True', 'DFIntRakNetApplicationFeedbackMaxSpeedBPS': '0', 'DFFlagTeleportClientAssetPreloadingEnabled9': 'True', 'FIntInterpolationMaxDelayMSec': '100', 'DFIntNumAssetsMaxToPreload': '9999999', 'DFFlagDebugLargeReplicatorDisableDelta': 'true', 'DFFlagRakNetUnblockSelectOnShutdownByWritingToSocket': 'True', 'DFFlagClampIncomingReplicationLag': 'True', 'FIntFRMMaxGrassDistance': '0', 'FIntTaskSchedulerAutoThreadLimit': '6', 'FIntRuntimeMaxNumOfConditions': '1000000', 'DFIntTaskSchedulerJobInGameThreads': '6', 'DFFlagRakNetDetectRecvThreadOverload': 'True', 'DFIntBatchThumbnailResultsSizeCap': '200', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'FFlagDebugRenderingSetDeterministic': 'True', 'DFIntGameNetCompressionLodByteBudgetThresholdPct': '0', 'DFIntNetworkQualityResponderUnit': '10', 'DFIntBufferCompressionThreshold': '100', 'FFlagEnablePerformanceControlService': 'True', 'DFFlagReplicatorCheckReadTableCollisions': 'True', 'FIntGrassMovementReducedMotionFactor': '0', 'DFFlagReplicateCreateToPlayer': 'True', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'FIntDebugTextureManagerSkipMips': '6', 'FFlagQuaternionPoseCorrection': 'True', 'DFFlagAnimatorAnywhere': 'True', 'FFlagLuaMenuPerfImprovements': 'True', 'FIntSimSolverResponsiveness': '2147483647', 'DFIntNetworkInProcessLimitGameplayMsClient': '0', 'FIntRuntimeMaxNumOfThreads': '1000000', 'DFIntServerBandwidthPlayerSampleRate': '2147483647', 'DFIntClientNetworkInfluxHundredthsPercentage': '0', 'FIntRuntimeMaxNumOfDPCs': '64', 'DFIntWaitOnRecvFromLoopEndedMS': '10', 'DFIntRakNetApplicationFeedbackScaleUpThresholdPercent': '0', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntNetworkSchemaCompressionRatio': '0', 'FIntRakNetResendBufferArrayLength': '256', 'DFIntMaxDataPacketPerSend': '2147483647', 'DFIntMegaReplicatorNumParallelTasks': '5', 'FIntActivatedCountTimerMSMouse': '0', 'DFIntSendRakNetStatsInterval': '2147483647', 'DFIntDebugPerformanceControlFrameTime': '2', 'FIntRenderGrassDetailStrands': '0', 'DFIntClusterEstimatedCompressionRatioHundredths': '0', 'DFIntPerformanceControlFrameTimeMax': '1', 'FIntRuntimeMaxNumOfLatches': '1000000', 'DFIntSendGameServerDataMaxLen': '9999999', 'FIntRuntimeMaxNumOfMutexes': '1000000', 'DFIntInterpolationNumParallelTasks': '5', 'FIntActivatedCountTimerMSKeyboard': '0', 'DFIntServerRakNetBandwidthPlayerSampleRate': '2147483647', 'DFIntClusterSenderMaxUpdateBandwidthBps': '2100000000', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntNetworkQualityResponderMaxWaitTime': '1', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntMaxReceiveToDeserializeLatencyMilliseconds': '10', 'FFlagDebugCodegenOptSize': 'True', 'DFIntTimestepArbiterAngAccelerationThresholdThou': '2000', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '5', 'DFIntClientPacketExcessMicroseconds': '1000', 'FFlagDebugCheckRenderThreading': 'True', 'DFFlagNetworkUseZstdWrapper': 'False', 'FFlagSimCSGV3IncrementalTriangulationStreamingCompression': 'False', 'FFlagLuaAppLegacyInputSettingRefactor': 'True', 'FFlagSortKeyOptimization': 'True', 'DFFlagRakNetCalculateApplicationFeedback2': 'False', 'FFlagFastGPULightCulling3': 'True', 'FFlagKeepZeroInfluenceBones': 'False', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagDebugNextGenReplicatorEnabledWriteCFrameColor': 'True', 'FFlagAdServiceEnabled': 'False', 'FFlagEnableAnimatorSkipCopyPreviousRigKeyOnJointModification': 'True', 'FFlagDebugRenderCollectGpuCounters': 'True', 'FFlagMouseGetPartOptimization': 'True', 'FFlagFasterPreciseTime4': 'True', 'FFlagRenderSkipReadingShaderData': 'True', 'DFFlagDebugPerfMode': 'True', 'FFlagFixTextureCompositorFramebufferManagement2': 'True', 'FFlagPreComputeAcceleratorArrayForSharingTimeCurve': 'True', 'FFlagDebugDisableOptimizedBytecode': 'False', 'FFlagEnableZstdDictionaryForClientSettings': 'False', 'DFIntMaxMissedWorldStepsRemembered': '2147483467', 'FIntRenderShadowmapBias': '0', 'DFFlagRakNetUseSlidingWindow4': 'True', 'DFIntMaxProcessPacketsJobScaling': '10000', 'FIntLuaGcParallelMinMultiTasks': '6', 'DFFlagSolverStateReplicatedOnly2': 'True', 'FIntFRMMinGrassDistance': '0', 'DFIntTeleportClientAssetPreloadingHundredthsPercentage2': '1000', 'FFlagOnlyDecrementCompletenessIfReplicating': 'True', 'FFlagUserCameraControlLastInputTypeUpdate': 'True', 'FFlagReportGpuLimitedToPerfControl': 'False', 'FFlagRenderDebugCheckThreading2': 'True', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagMessageBusCallOptimization': 'True', 'DFFlagDebugOverrideDPIScale': 'False', 'DFIntRakNetNakResendDelayMs': '1', 'DFIntRakNetSelectTimeoutMs': '1', 'DFIntClientPacketMaxDelayMs': '1', 'DFIntConnectingTimerInterval': '10', 'DFIntBufferCompressionLevel': '0', 'DFIntClientPacketHealthyAllocationPercent': '20', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'DFIntPerformanceControlReportingPeriodInMs': '700', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntTouchSenderMaxBandwidthBps': '-1', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntServerFramesBetweenJoins': '1', 'DFIntMaxAcceptableUpdateDelay': '1', 'DFIntInitialAccelerationLatencyMultTenths': '1', 'DFIntJoinDataCompressionLevel': '0', 'DFFlagRakNetDetectNetUnreachable': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagFastEndUpdateLoop': 'true', 'DFIntRakNetApplicationFeedbackScaleUpFactorHundredthPercent': '0', 'FFlagTouchscreenSupport': 'True', 'DFIntReplicatorAnimationTrackLimitPerAnimator': '-1', 'DFIntRemoteEventSingleInvocationSizeLimit': '2900', 'DFFlagAnimatorPostProcessIK': 'True', 'DFIntSimBlockLargeLocalToolWeldManipulationsThreshold': '-1', 'FFlagDebugSkyGray': 'True', 'DFIntPerformanceControlTextureQualityBestUtility': '-1'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Hasnbot Custom Flags 1",
    'desc': "110 flags",
    'flags': {'DFFlagDebugEnableInterpolationVisualizer': 'TRUE', 'DFFlagDebugVisualizeAllPropertyChanges': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagRakNetUseSlidingWindow4': 'True', 'DFFlagDebugSkipMeshVoxelizer': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagDisableDPIScale': 'True', 'DFFlagDebugPerfMode': 'True', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntReportRecordingDeviceInfoRateHundredthsPercentage': '0', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'DFIntReportOutputDeviceInfoRateHundredthsPercentage': '0', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '1', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '1', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntUserIdPlayerNameCacheSize': '33554432', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntRakNetNakResendDelayRttPercent': '50', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntVoiceChatVolumeThousandths': '6000', 'DFIntDebugFRMQualityLevelOverride': '3', 'DFIntTaskSchedulerTargetFps': '5588562', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntRakNetNakResendDelayMsMax': '100', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntRakNetMtuValue3InBytes': '1200', 'DFIntRakNetMtuValue1InBytes': '1280', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntRakNetMtuValue2InBytes': '1240', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntRakNetNakResendDelayMs': '10', 'DFIntS2PhysicsSenderRate': '35000', 'DFIntRakNetResendRttMultiple': '1', 'DFIntTextureQualityOverride': '0', 'DFIntConnectionMTUSize': '1472', 'DFIntMaxFrameBufferSize': '4', 'DFIntRakNetLoopMs': '1', 'DFStringCrashUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'DFStringAltHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFStringHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFStringRobloxAnalyticsURL': 'http://opt-out.roblox.com', 'DFStringAnalyticsEventStreamUrlEndpoint': 'opt-out', 'DFStringRobloxAnalyticsSubDomain': 'opt-out', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagGameBasicSettingsFramerateCap5': 'False', 'FFlagDebugRenderingSetDeterministic': 'True', 'FFlagEnableInGameMenuChromeABTest4': 'False', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagPreloadTextureItemsOption4': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagEnableCommandAutocomplete': 'False', 'FFlagDebugGraphicsPreferOpenGL': 'True', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagTopBarUseNewBadge': 'True', 'FFlagAdServiceEnabled': 'False', 'FFlagReconnectDisabled': 'True', 'FFlagDebugDisplayFPS': 'True', 'FFlagPreloadAllFonts': 'True', 'FFlagVoiceBetaBadge': 'False', 'FFlagDisablePostFx': 'True', 'FFlagDebugSkyGray': 'True', 'FIntBootstrapperTelemetryReportingHundredthsPercentage': '0', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FIntEmotesAnimationsPerPlayerCacheSize': '16777216', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FIntRakNetDatagramMessageIdArrayLength': '1024', 'FIntRomarkStartWithGraphicQualityLevel': '1', 'FIntRakNetResendBufferArrayLength': '1024', 'FIntUITextureMaxRenderTextureSize': '1024', 'FIntTerrainOTAMaxTextureSize': '1024', 'FIntDebugTextureManagerSkipMips': '2', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntCameraMaxZoomDistance': '99999', 'FIntRuntimeMaxNumOfThreads': '2400', 'FIntDefaultMeshCacheSizeMB': '256', 'FIntRenderGrassDetailStrands': '0', 'FIntTaskSchedulerThreadMin': '3', 'FIntRobloxGuiBlurIntensity': '0', 'FIntDebugForceMSAASamples': '1', 'FIntTerrainArraySliceSize': '0', 'FIntRenderShadowIntensity': '0', 'FIntRenderShadowmapBias': '0', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntLmsClientRollout2': '0', 'FIntFontSizePadding': '3', 'FLogNetwork': '7', 'FStringErrorUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'FStringPerformanceSendMeasurementAPISubdomain': 'opt-out', 'FStringTerrainMaterialTablePre2022': '', 'FStringTerrainMaterialTable2022': ''},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Hasnbot Custom Flags 3",
    'desc': "93 flags",
    'flags': {'DFFlagBrowserTrackerIdTelemetryEnabled': 'False', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagVideoCaptureServiceEnabled': 'False', 'DFFlagESGamePerfMonitorEnabled': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagDisableDPIScale': 'True', 'DFFlagPredictedOOM': 'False', 'DFFlagDebugPerfMode': 'True', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'DFIntCrashReportingHundredthsPercentage': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntCrashUploadToBacktracePercentage': '0', 'DFIntUserIdPlayerNameCacheSize': '33554432', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntStartupTracingInfluxRollout': '0', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntTaskSchedulerTargetFps': '240', 'DFIntTextureQualityOverride': '6', 'DFIntS2PhysicsSenderRate': '250', 'DFIntConnectionMTUSize': '900', 'DFIntPredictedOOMPercent': '0', 'DFLogHttpTraceError': '0', 'DFStringAnalyticsNS1BeaconConfig': 'https://opt-out.roblox.com', 'DFStringCrashUploadToBacktraceWindowsPlayerToken': 'null', 'DFStringCrashUploadToBacktraceMacPlayerToken': 'null', 'DFStringAnalyticsEventStreamUrlEndpoint': 'opt-out', 'DFStringCrashUploadToBacktraceBaseUrl': 'null', 'DFStringLightstepHTTPTransportUrlPath': 'null', 'DFStringLightstepHTTPTransportUrlHost': 'null', 'DFStringAnalyticsNS1ApplicationId': 'opt-out', 'DFStringRobloxAnalyticsSubDomain': 'opt-out', 'DFStringAltHttpPointsReporterUrl': 'null', 'DFStringHttpPointsReporterUrl': 'null', 'DFStringRobloxAnalyticsURL': 'null', 'DFStringTelemetryV2Url': 'null', 'DFStringLightstepToken': 'null', 'FFlagFacialAnimationStreamingServiceUniverseSettingsEnableVideo': 'False', 'FFlagFacialAnimationStreamingServiceUniverseSettingsEnableAudio': 'False', 'FFlagAvatarChatServiceExposeClientFeaturesForVoiceChat': 'False', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagLocServicePerformanceAnalyticsEnabled': 'False', 'FFlagVoiceChatServiceManagerUseAvatarChat': 'False', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FFlagEnableInGameMenuModernization': 'False', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagDebugRenderingSetDeterministic': 'True', 'FFlagPreloadTextureItemsOption4': 'True', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagTrackMacWebLaunchFlow': 'False', 'FFlagFastGPULightCulling3': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagPreloadMinimalFonts': 'True', 'FFlagAdServiceEnabled': 'False', 'FFlagVoiceBetaBadge': 'false', 'FFlagPreloadAllFonts': 'True', 'FFlagDisablePostFx': 'True', 'FIntBootstrapperTelemetryReportingHundredthsPercentage': '0', 'FIntLightingDefaultClearColorARGB': 'True;255,255,255,255', 'FIntV1MenuLanguageSelectionFeaturePerMillageRollout': '0', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FIntEmotesAnimationsPerPlayerCacheSize': '16777216', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FIntLinkBrowserTrackerToDeviceRollout': '0', 'FIntStartupInfluxHundredthsPercentage': '0', 'FIntUITextureMaxRenderTextureSize': '1024', 'FIntTerrainOTAMaxTextureSize': '1024', 'FIntCameraMaxZoomDistance': '99999', 'FIntRenderGrassDetailStrands': '0', 'FIntDefaultMeshCacheSizeMB': '256', 'FIntReportDeviceInfoRollout': '0', 'FIntRenderShadowIntensity': '0', 'FIntRenderShadowmapBias': '0', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntLmsClientRollout2': '0', 'FIntFontSizePadding': '3', 'FLogNetwork': '7', 'FStringErrorUploadToBacktraceBaseUrl': 'https://opt-out.roblox.com', 'FStringPerformanceSendMeasurementAPISubdomain': 'opt-out', 'FStringCoreScriptBacktraceErrorUploadToken': 'null', 'FStringTerrainMaterialTablePre2022': '', 'FStringTerrainMaterialTable2022': '', 'FStringGamesUrlPath': '/games/', 'GoogleAnalyticsAccountPropertyIDPlayer': 'null', 'GoogleAnalyticsAccountPropertyID': 'null'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Hasnbot Custom Flags 4",
    'desc': "78 flags",
    'flags': {'DFFlagEnableSkipUpdatingGlobalTelemetryInfo5': 'False', 'DFFlagEmitSafetyTelemetryInCallbackEnable': 'False', 'DFFlagRobloxTelemetryAddDeviceRAMPointsV2': 'False', 'DFFlagRccLoadSoundLengthTelemetryEnabled': 'False', 'DFFlagBrowserTrackerIdTelemetryEnabled': 'False', 'DFFlagReportRenderDistanceTelemetry': 'False', 'DFFlagGraphicsQualityUsageTelemetry': 'False', 'DFFlagReportAssetRequestV1Telemetry': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagCollectAudioPluginTelemetry': 'False', 'DFFlagRobloxTelemetryAddDeviceRAM': 'False', 'DFFlagClientRolloutPhaseTelemetry': 'False', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagDisableFastLogTelemetry': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagDisableDPIScale': 'True', 'DFFlagDebugPerfMode': 'True', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntContentProviderPreloadHangTelemetryHundredthsPercentage': '0', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntRakNetNakResendDelayRttPercent': '50', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntRakNetNakResendDelayMsMax': '100', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntRakNetMtuValue1InBytes': '1280', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntTaskSchedulerTargetFps': '9999', 'DFIntRakNetMtuValue2InBytes': '1240', 'DFIntRakNetMtuValue3InBytes': '1200', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntRakNetResendRttMultiple': '1', 'DFIntRakNetNakResendDelayMs': '10', 'DFIntTextureQualityOverride': '0', 'DFIntMaxFrameBufferSize': '4', 'DFIntRakNetLoopMs': '1', 'DFStringTelemetryV2Url': 'null', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagPreloadTextureItemsOption4': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagPreloadMinimalFonts': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagDisablePostFx': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FIntUITextureMaxRenderTextureSize': '1024', 'FIntTerrainOTAMaxTextureSize': '1024', 'FIntDebugTextureManagerSkipMips': '8', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntRenderGrassDetailStrands': '0', 'FIntRobloxGuiBlurIntensity': '0', 'FIntTerrainArraySliceSize': '0', 'FIntDebugForceMSAASamples': '1', 'FIntRenderShadowIntensity': '0', 'FIntFRMMaxGrassDistance': '0', 'FIntRenderShadowmapBias': '0', 'FIntFontSizePadding': '0', 'FIntSSAOMipLevels': '0', 'FLogLoginTelemetry': '0', 'FLogNetwork': '7'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "hasnbot Custom flags 5",
    'desc': "67 flags",
    'flags': {'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagDisableDPIScale': 'True', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '12', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'DFIntReplicationDataCacheNumParallelTasks': '12', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntVisibilityCheckRayCastLimitPerFrame': '10', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '2', 'DFIntTouchSenderMaxBandwidthBpsScaling': '-1', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntPhysicsReceiveNumParallelTasks': '12', 'DFIntNetworkSchemaCompressionRatio': '100', 'DFIntAnimatorThrottleMaxFramesToSkip': '1', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntMegaReplicatorNumParallelTasks': '12', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntBufferCompressionThreshold': '100', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntTextureCompositorActiveJobs': '0', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntTaskSchedulerTargetFps': '240', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntRakNetResendRttMultiple': '1', 'DFIntBufferCompressionLevel': '0', 'DFIntTextureQualityOverride': '0', 'DFIntConnectionMTUSize': '900', 'DFIntMaxFrameBufferSize': '4', 'DFIntRakNetLoopMs': '1', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagChatTranslationSettingEnabled3': 'False', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagDisablePostFx': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '12', 'FIntSimWorldTaskQueueParallelTasks': '12', 'FIntRakNetResendBufferArrayLength': '128', 'FIntRenderGrassDetailStrands': '0', 'FIntRobloxGuiBlurIntensity': '0', 'FIntTerrainArraySliceSize': '8', 'FIntRenderShadowIntensity': '0', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntFontSizePadding': '3', 'FLogNetwork': '7'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Better graphics",
    'desc': "195 flags",
    'flags': {'DFFlagOptimizeNoCollisionPrimitiveInMidphaseCrash': 'True', 'DFFlagPerformanceControlEnableMemoryProbing3': 'True', 'DFFlagRenderLanczosUpsamplingNonRinging2': 'True', 'DFFlagRenderSmootherStepUpsampling2': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagEnableTexturePreloading': 'True', 'DFFlagTaskSchedulerAvoidSleep': 'True', 'DFFlagDebugOverrideDPIScale': 'True', 'DFFlagEnableSoundPreloading': 'True', 'DFFlagEnableMeshPreloading': 'True', 'DFFlagSimOptimizeSetSize': 'True', 'DFFlagDisableDPIScale': 'True', 'DFFlagDebugPerfMode': 'True', 'DFFlagAggCpuMemRCC': 'True', 'DFFlagVoiceChatPossibleDuplicateSubscriptionsTelemetry': 'False', 'DFFlagSimAdaptiveAdjustTimestepForControllerManager': 'False', 'DFFlagEnableSkipUpdatingGlobalTelemetryInfo2': 'False', 'DFFlagEmitSafetyTelemetryInCallbackEnable': 'False', 'DFFlagRenderBlurMakeResolutionIndependent': 'False', 'DFFlagRobloxTelemetryAddDeviceRAMPointsV2': 'False', 'DFFlagRccLoadSoundLengthTelemetryEnabled': 'False', 'DFFlagWindowsWebViewTelemetryEnabled': 'False', 'DFFlagGraphicsQualityUsageTelemetry': 'False', 'DFFlagReportAssetRequestV1Telemetry': 'False', 'DFFlagReportRenderDistanceTelemetry': 'False', 'DFFlagCollectAudioPluginTelemetry': 'False', 'DFFlagRobloxTelemetryAddDeviceRAM': 'False', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagAlwaysSkipDiskCache': 'False', 'DFFlagNewPackageAnalytics': 'False', 'FFlagPerformanceControlEnablePortTextureManagerTrimMemory': 'True', 'FFlagEnablePreferredTextSizeSettingInMenus2': 'True', 'FFlagKeyframeSequenceUseRuntimeSyncPrims': 'True', 'FFlagUserRaycastPerformanceImprovements': 'True', 'FFlagEnableHarmonyOnFrameRateManager4': 'True', 'FFlagDebugApplyHSRForTransparentMesh': 'True', 'FFlagRemovedRbxRenderingPreProcessor': 'True', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagLargeReplicatorSerializeWrite4': 'True', 'FFlagDebugGridForceFractalUpsample': 'True', 'FFlagLargeReplicatorSerializeRead3': 'True', 'FFlagAvoidUnnecessaryQuadtreeLock': 'True', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagEnablePreferredTextSizeScale': 'True', 'FFlagSHUseNewComputeLevelUsesOBB': 'True', 'FFlagDebugCheckRenderThreading': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagQuaternionPoseCorrection': 'True', 'FFlagVideoFixSoundVolumeRange': 'True', 'FFlagLargeReplicatorEnabled9': 'True', 'FFlagUserShowGuiHideToggles2': 'True', 'FFlagUserShowGuiHideToggles': 'True', 'FFlagDebugForceGenerateHSR': 'True', 'FFlagDisableMemoryTracking': 'True', 'FFlagEnableFPSAndFrameTime': 'True', 'FFlagHSRClusterImprovement': 'True', 'FFlagLargeReplicatorWrite5': 'True', 'FFlagResetCacheOnLeaveGame': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagLargeReplicatorRead5': 'True', 'FFlagRenderInitShadowmaps': 'True', 'FFlagSHUseNewComputeLevel': 'True', 'FFlagAssetPreloadingIXP': 'True', 'FFlagRenderCBRefactor2': 'True', 'FFlagDebugPerfMode': 'True', 'FFlagVoiceChatRobloxAudioDeviceUpdateRecordedBufferTelemetryEnabled': 'False', 'FFlagVoiceChatCustomAudioDeviceEnableNeedMorePlayoutTelemetry3': 'False', 'FFlagVoiceChatCullingEnableMutedSubsTelemetry': 'False', 'FFlagVoiceChatCullingEnableStaleSubsTelemetry': 'False', 'FFlagVoiceChatPeerConnectionTelemetryDetails': 'False', 'FFlagVngLogoutGlobalAppSessionsOnConversion': 'False', 'FFlagVoiceChatSubscriptionsDroppedTelemetry': 'False', 'FFlagUpdateHTTPCookieStorageFromWKWebView': 'False', 'FFlagChatTranslationEnableSystemMessage': 'False', 'FFlagLuaVoiceChatAnalyticsUseCounterV2': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagLuaVoiceChatAnalyticsUseEventsV2': 'False', 'FFlagDisableFeedbackSoothsayerCheck': 'False', 'FFlagEnableLuaVoiceChatAnalyticsV2': 'False', 'FFlagSimStepPhysicsEnableTelemetry': 'False', 'FFlagGlobalSettingsEngineModule3': 'False', 'FFlagSyncWebViewCookieToEngine2': 'False', 'FFlagPropertiesEnableTelemetry': 'False', 'FFlagControlBetaBadgeWithGuac': 'False', 'FFlagEnableTelemetryProtocol': 'False', 'FFlagEnableTelemetryService1': 'False', 'FFlagEnableNudgeAnalyticsV2': 'False', 'FFlagLuaAppHomeVngAppUpsell': 'False', 'FFlagEnableChromeAnalytics': 'False', 'FFlagOpenTelemetryEnabled2': 'False', 'FFlagAlwaysShowVRToggleV3': 'False', 'FFlagOpenTelemetryEnabled': 'False', 'FFlagVngTOSRevisedEnabled': 'False', 'DFIntPolicyServiceReportDetailIsNotSubjectToChinaPoliciesHundredthsPercentage': '10000', 'DFIntTimestepArbiterBoundingBoxIntersectionThresholdThou1': '1073741823', 'DFIntTimestepArbiterBoundingBoxIntersectionThresholdThou2': '2147483646', 'DFIntTimestepArbiterVelocityCriteriaThresholdFourDt': '1073741823', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimitPartsModels': '0', 'DFIntTimestepArbiterVelocityCriteriaThresholdTwoDt': '2147483646', 'DFIntTimestepArbiterAngAccelerationThresholdThou': '1073741823', 'DFIntVoiceChatTaskStatsTelemetryThrottleHundrethsPercent': '0', 'DFIntNetworkStreamingGCMaxMicroSecondLimitPartsModels': '0', 'DFIntWindowsWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntSimExplicitlyCappedTimestepMultiplier': '2147483646', 'DFIntTimestepArbiterConditionNumberThresholdThou': '1000', 'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '15', 'DFIntGraphicsOptimizationModeMinFrameTimeTargetMs': '10', 'DFIntHttpBatchApiShutdownInfluxHundrethsPercentage': '0', 'DFIntTimestepArbiterAccelerationModelFactorThou': '1000', 'DFIntMacWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntBandwidthManagerApplicationDefaultBps': '1024000', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionHeartbeatTimerRateMs': '1000', 'DFIntBandwidthManagerDataSenderMaxWorkCatchupMs': '8', 'DFIntMemoryUtilityCurveSlopeMultiplierHundreths': '1', 'DFIntTimestepArbiterHumanoidTurningVelThreshold': '1', 'DFIntTrackCountryRegionAPIHundredthsPercent': '10000', 'DFIntMemoryUtilityCurveBaseHundrethsPercent': '2500', 'DFIntMemoryUtilityCurveTotalMemoryReserve': '102400', 'DFIntTimestepArbiterHumanoidLinearVelThreshold': '1', 'DFIntMemoryUtilityCurveInitialDeltaHundredths': '1', 'DFIntMemoryUtilityCurvePenaltyBuffer': '2000000000', 'DFIntMemoryUtilityCurveFinalDeltaHundredths': '1', 'DFIntNetworkStreamingGCMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionBaseRetryTimeMs': '100', 'DFIntSimDefaultHumanoidTimestepMultiplier': '8', 'DFIntTimestepArbiterCollidingHumanoidTsm': '25', 'DFIntSignalRCoreKeepAlivePingPeriodMs': '250', 'DFIntHttpBatchApi_bgRefreshMaxDelayMs': '30', 'DFIntMaxUREPayloadSingleLimit': '2147483647', 'DFIntAnalyticsServiceMonitoringPeriod': '0', 'DFIntSignalRCoreHandshakeTimeoutMs': '3000', 'DFIntSignalRCoreRpcQueueSize': '2147483647', 'DFIntNumAssetsMaxToPreload': '2147483647', 'DFIntMemoryUtilityCurveNumSegments': '0', 'DFIntSignalRCoreHubMaxBackoffMs': '5000', 'DFIntSignalRCoreServerTimeoutMs': '1100', 'DFIntTotalRepPayloadLimit': '2147483647', 'DFIntFileCacheReserveSize': '134217728', 'DFIntCliTcMaxPayloadRcv': '2147483647', 'DFIntCliTcMaxPayloadSnd': '2147483647', 'DFIntMaxDataPayloadSize': '2147483647', 'DFIntRccTcMaxPayloadRcv': '2147483647', 'DFIntRccTcMaxPayloadSnd': '2147483647', 'DFIntTimestepArbiterOmegaThou': '1000', 'DFIntSignalRCoreHubBaseRetryMs': '10', 'DFIntCliMaxPayloadRcv': '2147483647', 'DFIntCliMaxPayloadSnd': '2147483647', 'DFIntHttpBatchApi_cacheDelayMs': '5', 'DFIntRccMaxPayloadRcv': '2147483647', 'DFIntRccMaxPayloadSnd': '2147483647', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntNetworkStreamMinGrowSize': '0', 'DFIntHttpAnalyticsMaxHistory': '0', 'DFIntHttpBatchApi_bgDelayMs': '10', 'DFIntSchemaNetworkStreamSize': '0', 'DFIntHttpBatchApi_maxReqs': '128', 'DFIntHttpBatchApi_maxWaitMs': '5', 'DFIntHttpBatchApi_minWaitMs': '1', 'DFIntApiRateLimit': '2147483647', 'DFIntCLI61964inKB': '2147483647', 'DFIntNetworkStreamInitSize': '0', 'DFIntS2PhysicsSenderRate': '128', 'DFIntSignalRCoreTimerMs': '50', 'DFIntMaxFrameBufferSize': '4', 'DFIntDataSenderRate': '128', 'DFIntHttpBatchLimit': '64', 'FIntMaxTimestepMultiplierIntegrationError': '2147483647', 'FIntTaskSchedulerMaxTempArenaSizeBytes': '2147483647', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntMaxTimestepMultiplierAcceleration': '2147483647', 'FIntMaxTimestepMultiplierContstraint': '2147483647', 'FIntOpenTelemetryScheduleDelayMillis': '2147483647', 'FIntStudioWebView2TelemetryHundredthsPercent': '0', 'FIntMaxTimestepMultiplierBuoyancy': '2147483647', 'FIntMaxTimestepMultiplierHumanoid': '2147483647', 'FIntMaxTimestepMultiplierVelocity': '2147483647', 'FIntProfileTelemetryTickRateMs': '2147483647', 'FIntLuaAnalyticsReleasePeriod': '2147483647', 'FIntCameraMaxZoomDistance': '2147483647', 'FIntTaskSchedulerAutoThreadLimit': '3', 'FIntRenderLocalLightUpdatesMin': '0', 'FIntMininumRequiredMemoryInGB': '0', 'FIntMininumRequiredMemoryInMB': '0', 'FIntDebugForceMSAASamples': '4', 'FIntSSAOMipLevels': '8', 'FStringPhysicsAdaptiveTimeSteppingIXP': 'Physics.DefaultTimeStepping', 'FStringExperienceGuidelinesExplainedPageUrl': 'https://www.gov.cn', 'FStringGoogleAnalyticsAccountPropertyLuaTest': 'null', 'FStringRbxAnalyticsSessionsAllowlist': 'null', 'FStringGetPlayerImageDefaultTimeout': '1', 'FStringAnalyticsSessionIdName': 'null', 'FStringTencentAuthPath': '/tencent/', 'FStringVNGWebshopUrl': 'null'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "Everything Blurry fflags",
    'desc': "55 flags",
    'flags': {'FFlagGraphicsTextureQuality': '1', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagFastGPULightCulling3': 'True', 'DebugLimitMinTextureResolutionWhenSkipMips': '9999999999999999', 'FIntCameraFarZPlane': '750', 'FFlagDebugNextGenReplicatorEnabledWriteCFrameColor': 'true', 'DFIntRakNetUseSlidingWindow2_minSpeed': '1000', 'FFlagRenderInitShadowmaps': 'True', 'DFIntTextureQualityLevel': '1', 'DFIntMaxDataPacketPerSend': '2147483647', 'FIntDebugFRMOptionalMSAALevelOverride': '1', 'FFlagDebugGraphicsPreferD3D11': 'True', 'DFFlagDebugPerfMode': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'CSGLevelOfDetailSwitchingDistanceL12': '0', 'CSGLevelOfDetailSwitchingDistanceL23': '0', 'CSGLevelOfDetailSwitchingDistanceL34': '0', 'CSGLevelOfDetailSwitchingDistance': '0', 'DebugTextureManagerSkipMips': '3', 'DFIntDebugDynamicRenderKiloPixels': '922', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagDisableDPIScale': 'True', 'DFIntTextureQualityOverride': '1', 'DisablePostFx': 'True', 'DoNotSkipMipsBasedOnSystemMemoryPS': 'True', 'EnablePowerTraceModule': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagEnableBubbleChatFromChatService': 'False', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagPreloadTextureItemsOption4': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FIntDebugTextureManagerSkipMips': '3', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntRenderGrassDetailStrands': '0', 'FIntReportDeviceInfoRollout': '0', 'FIntRenderGrassHeightScaler': '0', 'FIntRobloxGuiBlurIntensity': '0', 'FIntTerrainArraySliceSize': '8', 'FIntRenderShadowIntensity': '0', 'FIntDebugForceMSAASamples': '1', 'FIntRenderShadowmapBias': '0', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FLogNetwork': '7', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'PerformanceControlTextureQualityBestUtility': '-1', 'RenderUseTextureManager224': 'False', 'RenderShadowmapBias': '75', 'TerrainArraySliceSize': '1', 'FFlagDebugDisplayFPS': 'True', 'TextureQualityOverrideEnabled': 'True', 'TextureQualityOverride': '1', 'DFIntS2PhysicsSenderRate': '555', 'DFIntDataSenderRate': '555'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "Stoofs_Balanced_Graphics_V35",
    'desc': "148 flags",
    'flags': {'DFFlagOptimizeNoCollisionPrimitiveInMidphaseCrash': 'True', 'DFFlagPerformanceControlEnableMemoryProbing3': 'True', 'DFFlagEnableTexturePreloading': 'True', 'DFFlagTaskSchedulerAvoidSleep': 'True', 'DFFlagDebugSkipMeshVoxelizer': 'True', 'DFFlagEnableSoundPreloading': 'True', 'DFFlagEnableMeshPreloading': 'True', 'DFFlagSimOptimizeSetSize': 'True', 'DFFlagDebugPerfMode': 'True', 'DFFlagAggCpuMemRCC': 'True', 'DFFlagVoiceChatPossibleDuplicateSubscriptionsTelemetry': 'False', 'DFFlagEnableSkipUpdatingGlobalTelemetryInfo2': 'False', 'DFFlagRenderBloomMakeResolutionIndependent': 'False', 'DFFlagEmitSafetyTelemetryInCallbackEnable': 'False', 'DFFlagRenderBlurMakeResolutionIndependent': 'False', 'DFFlagRobloxTelemetryAddDeviceRAMPointsV2': 'False', 'DFFlagRccLoadSoundLengthTelemetryEnabled': 'False', 'DFFlagWindowsWebViewTelemetryEnabled': 'False', 'DFFlagGraphicsQualityUsageTelemetry': 'False', 'DFFlagReportAssetRequestV1Telemetry': 'False', 'DFFlagReportRenderDistanceTelemetry': 'False', 'DFFlagCollectAudioPluginTelemetry': 'False', 'DFFlagRobloxTelemetryAddDeviceRAM': 'False', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagNewPackageAnalytics': 'False', 'FFlagPerformanceControlEnablePortTextureManagerTrimMemory': 'True', 'FFlagEnablePreferredTextSizeSettingInMenus2': 'True', 'FFlagKeyframeSequenceUseRuntimeSyncPrims': 'True', 'FFlagUserRaycastPerformanceImprovements': 'True', 'FFlagEnableHarmonyOnFrameRateManager4': 'True', 'FFlagDebugApplyHSRForTransparentMesh': 'True', 'FFlagAvoidUnnecessaryQuadtreeLock': 'True', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagEnablePreferredTextSizeScale': 'True', 'FFlagSHUseNewComputeLevelUsesOBB': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagDebugCheckRenderThreading': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagQuaternionPoseCorrection': 'True', 'FFlagUserShowGuiHideToggles2': 'True', 'FFlagUserShowGuiHideToggles': 'True', 'FFlagDebugForceGenerateHSR': 'True', 'FFlagDisableMemoryTracking': 'True', 'FFlagEnableFPSAndFrameTime': 'True', 'FFlagHSRClusterImprovement': 'True', 'FFlagResetCacheOnLeaveGame': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagSHUseNewComputeLevel': 'True', 'FFlagAssetPreloadingIXP': 'True', 'FFlagRenderCBRefactor2': 'True', 'FFlagDisablePostFx': 'True', 'FFlagFineGrainCull': 'True', 'FFlagVoiceChatRobloxAudioDeviceUpdateRecordedBufferTelemetryEnabled': 'False', 'FFlagVoiceChatCustomAudioDeviceEnableNeedMorePlayoutTelemetry3': 'False', 'FFlagVoiceChatCullingEnableMutedSubsTelemetry': 'False', 'FFlagVoiceChatCullingEnableStaleSubsTelemetry': 'False', 'FFlagVoiceChatPeerConnectionTelemetryDetails': 'False', 'FFlagVngLogoutGlobalAppSessionsOnConversion': 'False', 'FFlagVoiceChatSubscriptionsDroppedTelemetry': 'False', 'FFlagUpdateHTTPCookieStorageFromWKWebView': 'False', 'FFlagChatTranslationEnableSystemMessage': 'False', 'FFlagLuaVoiceChatAnalyticsUseCounterV2': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagLuaVoiceChatAnalyticsUseEventsV2': 'False', 'FFlagDisableFeedbackSoothsayerCheck': 'False', 'FFlagEnableLuaVoiceChatAnalyticsV2': 'False', 'FFlagSimStepPhysicsEnableTelemetry': 'False', 'FFlagSyncWebViewCookieToEngine2': 'False', 'FFlagPropertiesEnableTelemetry': 'False', 'FFlagControlBetaBadgeWithGuac': 'False', 'FFlagEnableTelemetryProtocol': 'False', 'FFlagEnableTelemetryService1': 'False', 'FFlagEnableNudgeAnalyticsV2': 'False', 'FFlagLuaAppHomeVngAppUpsell': 'False', 'FFlagEnableChromeAnalytics': 'False', 'FFlagOpenTelemetryEnabled2': 'False', 'FFlagAlwaysShowVRToggleV3': 'False', 'FFlagOpenTelemetryEnabled': 'False', 'FFlagVngTOSRevisedEnabled': 'False', 'DFIntPolicyServiceReportDetailIsNotSubjectToChinaPoliciesHundredthsPercentage': '10000', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimitPartsModels': '0', 'DFIntVoiceChatTaskStatsTelemetryThrottleHundrethsPercent': '0', 'DFIntNetworkStreamingGCMaxMicroSecondLimitPartsModels': '0', 'DFIntWindowsWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '15', 'DFIntGraphicsOptimizationModeMinFrameTimeTargetMs': '10', 'DFIntHttpBatchApiShutdownInfluxHundrethsPercentage': '0', 'DFIntMacWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionHeartbeatTimerRateMs': '1000', 'DFIntMemoryUtilityCurveSlopeMultiplierHundreths': '1', 'DFIntTrackCountryRegionAPIHundredthsPercent': '10000', 'DFIntMemoryUtilityCurveBaseHundrethsPercent': '2500', 'DFIntMemoryUtilityCurveTotalMemoryReserve': '102400', 'DFIntMemoryUtilityCurveInitialDeltaHundredths': '1', 'DFIntMemoryUtilityCurvePenaltyBuffer': '2000000000', 'DFIntMemoryUtilityCurveFinalDeltaHundredths': '1', 'DFIntNetworkStreamingGCMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionBaseRetryTimeMs': '100', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntSignalRCoreKeepAlivePingPeriodMs': '250', 'DFIntHttpBatchApi_bgRefreshMaxDelayMs': '30', 'DFIntAnalyticsServiceMonitoringPeriod': '0', 'DFIntSignalRCoreHandshakeTimeoutMs': '3000', 'DFIntSignalRCoreRpcQueueSize': '2147483647', 'DFIntNumAssetsMaxToPreload': '2147483647', 'DFIntMemoryUtilityCurveNumSegments': '0', 'DFIntSignalRCoreHubMaxBackoffMs': '5000', 'DFIntSignalRCoreServerTimeoutMs': '1100', 'DFIntFileCacheReserveSize': '134217728', 'DFIntSignalRCoreHubBaseRetryMs': '10', 'DFIntHttpBatchApi_cacheDelayMs': '5', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntNetworkStreamMinGrowSize': '0', 'DFIntHttpAnalyticsMaxHistory': '0', 'DFIntHttpBatchApi_bgDelayMs': '10', 'DFIntSchemaNetworkStreamSize': '0', 'DFIntHttpBatchApi_maxReqs': '128', 'DFIntHttpBatchApi_maxWaitMs': '5', 'DFIntHttpBatchApi_minWaitMs': '1', 'DFIntApiRateLimit': '2147483647', 'DFIntCLI61964inKB': '2147483647', 'DFIntNetworkStreamInitSize': '0', 'DFIntS2PhysicsSenderRate': '128', 'DFIntSignalRCoreTimerMs': '50', 'DFIntMaxFrameBufferSize': '4', 'DFIntDataSenderRate': '128', 'DFIntHttpBatchLimit': '64', 'FIntTaskSchedulerMaxTempArenaSizeBytes': '2147483647', 'FIntOpenTelemetryScheduleDelayMillis': '2147483647', 'FIntStudioWebView2TelemetryHundredthsPercent': '0', 'FIntProfileTelemetryTickRateMs': '2147483647', 'FIntLuaAnalyticsReleasePeriod': '2147483647', 'FIntCameraMaxZoomDistance': '2147483647', 'FIntRenderMeshOptimizeVertexBuffer': '1', 'FIntTaskSchedulerAutoThreadLimit': '3', 'FIntRenderLocalLightUpdatesMin': '0', 'FIntMininumRequiredMemoryInGB': '0', 'FIntMininumRequiredMemoryInMB': '0', 'FIntRenderShadowIntensity': '0', 'FStringExperienceGuidelinesExplainedPageUrl': 'https://www.gov.cn', 'FStringGoogleAnalyticsAccountPropertyLuaTest': 'null', 'FStringRbxAnalyticsSessionsAllowlist': 'null', 'FStringGetPlayerImageDefaultTimeout': '1', 'FStringAnalyticsSessionIdName': 'null', 'FStringTencentAuthPath': '/tencent/', 'FStringVNGWebshopUrl': 'null'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "Stoofs_High_Graphics_V35",
    'desc': "176 flags",
    'flags': {'DFFlagOptimizeNoCollisionPrimitiveInMidphaseCrash': 'True', 'DFFlagPerformanceControlEnableMemoryProbing3': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagEnableTexturePreloading': 'True', 'DFFlagTaskSchedulerAvoidSleep': 'True', 'DFFlagDebugOverrideDPIScale': 'True', 'DFFlagEnableSoundPreloading': 'True', 'DFFlagEnableMeshPreloading': 'True', 'DFFlagSimOptimizeSetSize': 'True', 'DFFlagDisableDPIScale': 'True', 'DFFlagDebugPerfMode': 'True', 'DFFlagAggCpuMemRCC': 'True', 'DFFlagVoiceChatPossibleDuplicateSubscriptionsTelemetry': 'False', 'DFFlagSimAdaptiveAdjustTimestepForControllerManager': 'False', 'DFFlagEnableSkipUpdatingGlobalTelemetryInfo2': 'False', 'DFFlagEmitSafetyTelemetryInCallbackEnable': 'False', 'DFFlagRenderBlurMakeResolutionIndependent': 'False', 'DFFlagRobloxTelemetryAddDeviceRAMPointsV2': 'False', 'DFFlagRccLoadSoundLengthTelemetryEnabled': 'False', 'DFFlagWindowsWebViewTelemetryEnabled': 'False', 'DFFlagGraphicsQualityUsageTelemetry': 'False', 'DFFlagReportAssetRequestV1Telemetry': 'False', 'DFFlagReportRenderDistanceTelemetry': 'False', 'DFFlagCollectAudioPluginTelemetry': 'False', 'DFFlagRobloxTelemetryAddDeviceRAM': 'False', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagAlwaysSkipDiskCache': 'False', 'DFFlagNewPackageAnalytics': 'False', 'FFlagPerformanceControlEnablePortTextureManagerTrimMemory': 'True', 'FFlagEnablePreferredTextSizeSettingInMenus2': 'True', 'FFlagKeyframeSequenceUseRuntimeSyncPrims': 'True', 'FFlagUserRaycastPerformanceImprovements': 'True', 'FFlagEnableHarmonyOnFrameRateManager4': 'True', 'FFlagDebugApplyHSRForTransparentMesh': 'True', 'FFlagRemovedRbxRenderingPreProcessor': 'true', 'FFlagAvoidUnnecessaryQuadtreeLock': 'True', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagEnablePreferredTextSizeScale': 'True', 'FFlagSHUseNewComputeLevelUsesOBB': 'True', 'FFlagDebugCheckRenderThreading': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagQuaternionPoseCorrection': 'True', 'FFlagVideoFixSoundVolumeRange': 'true', 'FFlagUserShowGuiHideToggles2': 'True', 'FFlagUserShowGuiHideToggles': 'True', 'FFlagDebugForceGenerateHSR': 'True', 'FFlagDisableMemoryTracking': 'True', 'FFlagEnableFPSAndFrameTime': 'True', 'FFlagHSRClusterImprovement': 'True', 'FFlagResetCacheOnLeaveGame': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagRenderInitShadowmaps': 'True', 'FFlagSHUseNewComputeLevel': 'True', 'FFlagAssetPreloadingIXP': 'True', 'FFlagRenderCBRefactor2': 'True', 'FFlagDebugSSAOForce': 'True', 'FFlagDebugPerfMode': 'True', 'FFlagFineGrainCull': 'True', 'FFlagVoiceChatRobloxAudioDeviceUpdateRecordedBufferTelemetryEnabled': 'False', 'FFlagVoiceChatCustomAudioDeviceEnableNeedMorePlayoutTelemetry3': 'False', 'FFlagVoiceChatCullingEnableMutedSubsTelemetry': 'False', 'FFlagVoiceChatCullingEnableStaleSubsTelemetry': 'False', 'FFlagVoiceChatPeerConnectionTelemetryDetails': 'False', 'FFlagVngLogoutGlobalAppSessionsOnConversion': 'False', 'FFlagVoiceChatSubscriptionsDroppedTelemetry': 'False', 'FFlagUpdateHTTPCookieStorageFromWKWebView': 'False', 'FFlagChatTranslationEnableSystemMessage': 'False', 'FFlagLuaVoiceChatAnalyticsUseCounterV2': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagLuaVoiceChatAnalyticsUseEventsV2': 'False', 'FFlagDisableFeedbackSoothsayerCheck': 'False', 'FFlagEnableLuaVoiceChatAnalyticsV2': 'False', 'FFlagSimStepPhysicsEnableTelemetry': 'False', 'FFlagSyncWebViewCookieToEngine2': 'False', 'FFlagPropertiesEnableTelemetry': 'False', 'FFlagControlBetaBadgeWithGuac': 'False', 'FFlagEnableTelemetryProtocol': 'False', 'FFlagEnableTelemetryService1': 'False', 'FFlagEnableNudgeAnalyticsV2': 'False', 'FFlagLuaAppHomeVngAppUpsell': 'False', 'FFlagEnableChromeAnalytics': 'False', 'FFlagOpenTelemetryEnabled2': 'False', 'FFlagAlwaysShowVRToggleV3': 'False', 'FFlagOpenTelemetryEnabled': 'False', 'FFlagVngTOSRevisedEnabled': 'False', 'DFIntPolicyServiceReportDetailIsNotSubjectToChinaPoliciesHundredthsPercentage': '10000', 'DFIntTimestepArbiterBoundingBoxIntersectionThresholdThou1': '1073741823', 'DFIntTimestepArbiterBoundingBoxIntersectionThresholdThou2': '2147483646', 'DFIntTimestepArbiterVelocityCriteriaThresholdFourDt': '1073741823', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimitPartsModels': '0', 'DFIntTimestepArbiterVelocityCriteriaThresholdTwoDt': '2147483646', 'DFIntTimestepArbiterAngAccelerationThresholdThou': '1073741823', 'DFIntVoiceChatTaskStatsTelemetryThrottleHundrethsPercent': '0', 'DFIntNetworkStreamingGCMaxMicroSecondLimitPartsModels': '0', 'DFIntWindowsWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntSimExplicitlyCappedTimestepMultiplier': '2147483646', 'DFIntTimestepArbiterConditionNumberThresholdThou': '1000', 'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '15', 'DFIntGraphicsOptimizationModeMinFrameTimeTargetMs': '10', 'DFIntHttpBatchApiShutdownInfluxHundrethsPercentage': '0', 'DFIntTimestepArbiterAccelerationModelFactorThou': '1000', 'DFIntMacWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntBandwidthManagerApplicationDefaultBps': '1024000', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionHeartbeatTimerRateMs': '1000', 'DFIntBandwidthManagerDataSenderMaxWorkCatchupMs': '8', 'DFIntMemoryUtilityCurveSlopeMultiplierHundreths': '1', 'DFIntTimestepArbiterHumanoidTurningVelThreshold': '1', 'DFIntTrackCountryRegionAPIHundredthsPercent': '10000', 'DFIntMemoryUtilityCurveBaseHundrethsPercent': '2500', 'DFIntMemoryUtilityCurveTotalMemoryReserve': '102400', 'DFIntTimestepArbiterHumanoidLinearVelThreshold': '1', 'DFIntMemoryUtilityCurveInitialDeltaHundredths': '1', 'DFIntMemoryUtilityCurvePenaltyBuffer': '2000000000', 'DFIntMemoryUtilityCurveFinalDeltaHundredths': '1', 'DFIntNetworkStreamingGCMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionBaseRetryTimeMs': '100', 'DFIntSimDefaultHumanoidTimestepMultiplier': '8', 'DFIntTimestepArbiterCollidingHumanoidTsm': '25', 'DFIntSignalRCoreKeepAlivePingPeriodMs': '250', 'DFIntHttpBatchApi_bgRefreshMaxDelayMs': '30', 'DFIntAnalyticsServiceMonitoringPeriod': '0', 'DFIntSignalRCoreHandshakeTimeoutMs': '3000', 'DFIntSignalRCoreRpcQueueSize': '2147483647', 'DFIntNumAssetsMaxToPreload': '2147483647', 'DFIntMemoryUtilityCurveNumSegments': '0', 'DFIntSignalRCoreHubMaxBackoffMs': '5000', 'DFIntSignalRCoreServerTimeoutMs': '1100', 'DFIntFileCacheReserveSize': '134217728', 'DFIntTimestepArbiterOmegaThou': '1000', 'DFIntSignalRCoreHubBaseRetryMs': '10', 'DFIntHttpBatchApi_cacheDelayMs': '5', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntNetworkStreamMinGrowSize': '0', 'DFIntHttpAnalyticsMaxHistory': '0', 'DFIntHttpBatchApi_bgDelayMs': '10', 'DFIntSchemaNetworkStreamSize': '0', 'DFIntHttpBatchApi_maxReqs': '128', 'DFIntHttpBatchApi_maxWaitMs': '5', 'DFIntHttpBatchApi_minWaitMs': '1', 'DFIntApiRateLimit': '2147483647', 'DFIntCLI61964inKB': '2147483647', 'DFIntNetworkStreamInitSize': '0', 'DFIntS2PhysicsSenderRate': '128', 'DFIntSignalRCoreTimerMs': '50', 'DFIntMaxFrameBufferSize': '4', 'DFIntDataSenderRate': '128', 'DFIntHttpBatchLimit': '64', 'FIntMaxTimestepMultiplierIntegrationError': '2147483647', 'FIntTaskSchedulerMaxTempArenaSizeBytes': '2147483647', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntMaxTimestepMultiplierAcceleration': '2147483647', 'FIntMaxTimestepMultiplierContstraint': '2147483647', 'FIntOpenTelemetryScheduleDelayMillis': '2147483647', 'FIntStudioWebView2TelemetryHundredthsPercent': '0', 'FIntMaxTimestepMultiplierBuoyancy': '2147483647', 'FIntMaxTimestepMultiplierHumanoid': '2147483647', 'FIntMaxTimestepMultiplierVelocity': '2147483647', 'FIntProfileTelemetryTickRateMs': '2147483647', 'FIntLuaAnalyticsReleasePeriod': '2147483647', 'FIntDebugFRMOptionalMSAALevelOverride': '2', 'FIntCameraMaxZoomDistance': '2147483647', 'FIntTaskSchedulerAutoThreadLimit': '3', 'FIntRenderLocalLightUpdatesMin': '0', 'FIntMininumRequiredMemoryInGB': '0', 'FIntMininumRequiredMemoryInMB': '0', 'FIntDebugForceMSAASamples': '2', 'FStringPhysicsAdaptiveTimeSteppingIXP': 'Physics.DefaultTimeStepping', 'FStringExperienceGuidelinesExplainedPageUrl': 'https://www.gov.cn', 'FStringGoogleAnalyticsAccountPropertyLuaTest': 'null', 'FStringRbxAnalyticsSessionsAllowlist': 'null', 'FStringGetPlayerImageDefaultTimeout': '1', 'FStringAnalyticsSessionIdName': 'null', 'FStringTencentAuthPath': '/tencent/', 'FStringVNGWebshopUrl': 'null'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "Stoofs_Low_Graphics_V35",
    'desc': "172 flags",
    'flags': {'DFFlagOptimizeNoCollisionPrimitiveInMidphaseCrash': 'True', 'DFFlagPerformanceControlEnableMemoryProbing3': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagEnableTexturePreloading': 'True', 'DFFlagTaskSchedulerAvoidSleep': 'True', 'DFFlagDebugSkipMeshVoxelizer': 'True', 'DFFlagEnableSoundPreloading': 'True', 'DFFlagEnableMeshPreloading': 'True', 'DFFlagSimOptimizeSetSize': 'True', 'DFFlagDebugPerfMode': 'True', 'DFFlagAggCpuMemRCC': 'True', 'DFFlagVoiceChatPossibleDuplicateSubscriptionsTelemetry': 'False', 'DFFlagEnableSkipUpdatingGlobalTelemetryInfo2': 'False', 'DFFlagRenderBloomMakeResolutionIndependent': 'False', 'DFFlagEmitSafetyTelemetryInCallbackEnable': 'False', 'DFFlagRenderBlurMakeResolutionIndependent': 'False', 'DFFlagRobloxTelemetryAddDeviceRAMPointsV2': 'False', 'DFFlagRccLoadSoundLengthTelemetryEnabled': 'False', 'DFFlagWindowsWebViewTelemetryEnabled': 'False', 'DFFlagGraphicsQualityUsageTelemetry': 'False', 'DFFlagReportAssetRequestV1Telemetry': 'False', 'DFFlagReportRenderDistanceTelemetry': 'False', 'DFFlagCollectAudioPluginTelemetry': 'False', 'DFFlagRobloxTelemetryAddDeviceRAM': 'False', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagAlwaysSkipDiskCache': 'False', 'DFFlagNewPackageAnalytics': 'False', 'FFlagPerformanceControlEnablePortTextureManagerTrimMemory': 'True', 'FFlagEnablePreferredTextSizeSettingInMenus2': 'True', 'FFlagKeyframeSequenceUseRuntimeSyncPrims': 'True', 'FFlagEnableHarmonyOnFrameRateManager4': 'True', 'FFlagDebugApplyHSRForTransparentMesh': 'True', 'FFlagDebugRenderingSetDeterministic': 'True', 'FFlagAvoidUnnecessaryQuadtreeLock': 'True', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagEnablePreferredTextSizeScale': 'True', 'FFlagSHUseNewComputeLevelUsesOBB': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagDebugCheckRenderThreading': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagQuaternionPoseCorrection': 'True', 'FFlagVideoFixSoundVolumeRange': 'true', 'FFlagUserShowGuiHideToggles2': 'True', 'FFlagUserShowGuiHideToggles': 'True', 'FFlagDebugForceGenerateHSR': 'True', 'FFlagDisableMemoryTracking': 'True', 'FFlagEnableFPSAndFrameTime': 'True', 'FFlagHSRClusterImprovement': 'True', 'FFlagResetCacheOnLeaveGame': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagSHUseNewComputeLevel': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagAssetPreloadingIXP': 'True', 'FFlagRenderCBRefactor2': 'True', 'FFlagDebugPerfMode': 'True', 'FFlagDisablePostFx': 'True', 'FFlagFineGrainCull': 'True', 'FFlagVoiceChatRobloxAudioDeviceUpdateRecordedBufferTelemetryEnabled': 'False', 'FFlagVoiceChatCustomAudioDeviceEnableNeedMorePlayoutTelemetry3': 'False', 'FFlagVoiceChatCullingEnableMutedSubsTelemetry': 'False', 'FFlagVoiceChatCullingEnableStaleSubsTelemetry': 'False', 'FFlagVoiceChatPeerConnectionTelemetryDetails': 'False', 'FFlagVngLogoutGlobalAppSessionsOnConversion': 'False', 'FFlagVoiceChatSubscriptionsDroppedTelemetry': 'False', 'FFlagUpdateHTTPCookieStorageFromWKWebView': 'False', 'FFlagChatTranslationEnableSystemMessage': 'False', 'FFlagLuaVoiceChatAnalyticsUseCounterV2': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagLuaVoiceChatAnalyticsUseEventsV2': 'False', 'FFlagDisableFeedbackSoothsayerCheck': 'False', 'FFlagEnableLuaVoiceChatAnalyticsV2': 'False', 'FFlagSimStepPhysicsEnableTelemetry': 'False', 'FFlagSyncWebViewCookieToEngine2': 'False', 'FFlagPropertiesEnableTelemetry': 'False', 'FFlagControlBetaBadgeWithGuac': 'False', 'FFlagEnableTelemetryProtocol': 'False', 'FFlagEnableTelemetryService1': 'False', 'FFlagEnableNudgeAnalyticsV2': 'False', 'FFlagLuaAppHomeVngAppUpsell': 'False', 'FFlagEnableChromeAnalytics': 'False', 'FFlagOpenTelemetryEnabled2': 'False', 'FFlagAlwaysShowVRToggleV3': 'False', 'FFlagOpenTelemetryEnabled': 'False', 'FFlagVngTOSRevisedEnabled': 'False', 'FFlagRenderNoLowFrmBloom': 'False', 'DFIntPolicyServiceReportDetailIsNotSubjectToChinaPoliciesHundredthsPercentage': '10000', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimitPartsModels': '0', 'DFIntVoiceChatTaskStatsTelemetryThrottleHundrethsPercent': '0', 'DFIntNetworkStreamingGCMaxMicroSecondLimitPartsModels': '0', 'DFIntWindowsWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '15', 'DFIntGraphicsOptimizationModeMinFrameTimeTargetMs': '10', 'DFIntHttpBatchApiShutdownInfluxHundrethsPercentage': '0', 'DFIntMacWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionHeartbeatTimerRateMs': '1000', 'DFIntMemoryUtilityCurveSlopeMultiplierHundreths': '1', 'DFIntTrackCountryRegionAPIHundredthsPercent': '10000', 'DFIntMemoryUtilityCurveBaseHundrethsPercent': '2500', 'DFIntMemoryUtilityCurveTotalMemoryReserve': '102400', 'DFIntMemoryUtilityCurveInitialDeltaHundredths': '1', 'DFIntMemoryUtilityCurvePenaltyBuffer': '2000000000', 'DFIntMemoryUtilityCurveFinalDeltaHundredths': '1', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntNetworkStreamingGCMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionBaseRetryTimeMs': '100', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntSignalRCoreKeepAlivePingPeriodMs': '250', 'DFIntHttpBatchApi_bgRefreshMaxDelayMs': '30', 'DFIntAnalyticsServiceMonitoringPeriod': '0', 'DFIntSignalRCoreHandshakeTimeoutMs': '3000', 'DFIntSignalRCoreRpcQueueSize': '2147483647', 'DFIntNumAssetsMaxToPreload': '2147483647', 'DFIntMemoryUtilityCurveNumSegments': '0', 'DFIntSignalRCoreHubMaxBackoffMs': '5000', 'DFIntSignalRCoreServerTimeoutMs': '1100', 'DFIntFileCacheReserveSize': '134217728', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntSignalRCoreHubBaseRetryMs': '10', 'DFIntHttpBatchApi_cacheDelayMs': '5', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntNetworkStreamMinGrowSize': '0', 'DFIntHttpAnalyticsMaxHistory': '0', 'DFIntHttpBatchApi_bgDelayMs': '10', 'DFIntSchemaNetworkStreamSize': '0', 'DFIntHttpBatchApi_maxReqs': '128', 'DFIntHttpBatchApi_maxWaitMs': '5', 'DFIntHttpBatchApi_minWaitMs': '1', 'DFIntTextureQualityOverride': '2', 'DFIntApiRateLimit': '2147483647', 'DFIntCLI61964inKB': '2147483647', 'DFIntNetworkStreamInitSize': '0', 'DFIntS2PhysicsSenderRate': '128', 'DFIntSignalRCoreTimerMs': '50', 'DFIntMaxFrameBufferSize': '4', 'DFIntDataSenderRate': '128', 'DFIntHttpBatchLimit': '64', 'FIntTaskSchedulerMaxTempArenaSizeBytes': '2147483647', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntOpenTelemetryScheduleDelayMillis': '2147483647', 'FIntStudioWebView2TelemetryHundredthsPercent': '0', 'FIntMaquettesFrameRateBufferPercentage': '50', 'FIntProfileTelemetryTickRateMs': '2147483647', 'FIntLuaAnalyticsReleasePeriod': '2147483647', 'FIntDebugFRMOptionalMSAALevelOverride': '1', 'FIntGrassMovementReducedMotionFactor': '0', 'FIntCameraMaxZoomDistance': '2147483647', 'FIntRenderMeshOptimizeVertexBuffer': '1', 'FIntTaskSchedulerAutoThreadLimit': '3', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntRenderLocalLightUpdatesMin': '0', 'FIntMininumRequiredMemoryInGB': '0', 'FIntMininumRequiredMemoryInMB': '0', 'FIntRenderGrassDetailStrands': '0', 'FIntDebugForceMSAASamples': '1', 'FIntRenderShadowIntensity': '0', 'FIntTerrainArraySliceSize': '0', 'FIntRenderShadowmapBias': '-1', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FStringExperienceGuidelinesExplainedPageUrl': 'https://www.gov.cn', 'FStringGoogleAnalyticsAccountPropertyLuaTest': 'null', 'FStringRbxAnalyticsSessionsAllowlist': 'null', 'FStringGetPlayerImageDefaultTimeout': '1', 'FStringAnalyticsSessionIdName': 'null', 'FStringTencentAuthPath': '/tencent/', 'FStringVNGWebshopUrl': 'null'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "Stoofs_Potato_Graphics_V35",
    'desc': "179 flags",
    'flags': {'DFFlagOptimizeNoCollisionPrimitiveInMidphaseCrash': 'True', 'DFFlagPerformanceControlEnableMemoryProbing3': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagEnableTexturePreloading': 'True', 'DFFlagTaskSchedulerAvoidSleep': 'True', 'DFFlagDebugSkipMeshVoxelizer': 'True', 'DFFlagEnableSoundPreloading': 'True', 'DFFlagEnableMeshPreloading': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagSimOptimizeSetSize': 'True', 'DFFlagDebugPerfMode': 'True', 'DFFlagAggCpuMemRCC': 'True', 'DFFlagVoiceChatPossibleDuplicateSubscriptionsTelemetry': 'False', 'DFFlagEnableSkipUpdatingGlobalTelemetryInfo2': 'False', 'DFFlagRenderBloomMakeResolutionIndependent': 'False', 'DFFlagEmitSafetyTelemetryInCallbackEnable': 'False', 'DFFlagRenderBlurMakeResolutionIndependent': 'False', 'DFFlagRobloxTelemetryAddDeviceRAMPointsV2': 'False', 'DFFlagRccLoadSoundLengthTelemetryEnabled': 'False', 'DFFlagWindowsWebViewTelemetryEnabled': 'False', 'DFFlagGraphicsQualityUsageTelemetry': 'False', 'DFFlagReportAssetRequestV1Telemetry': 'False', 'DFFlagReportRenderDistanceTelemetry': 'False', 'DFFlagCollectAudioPluginTelemetry': 'False', 'DFFlagRobloxTelemetryAddDeviceRAM': 'False', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagAlwaysSkipDiskCache': 'False', 'DFFlagNewPackageAnalytics': 'False', 'FFlagPerformanceControlEnablePortTextureManagerTrimMemory': 'True', 'FFlagEnablePreferredTextSizeSettingInMenus2': 'True', 'FFlagKeyframeSequenceUseRuntimeSyncPrims': 'True', 'FFlagEnableHarmonyOnFrameRateManager4': 'True', 'FFlagDebugApplyHSRForTransparentMesh': 'True', 'FFlagDebugRenderingSetDeterministic': 'True', 'FFlagAvoidUnnecessaryQuadtreeLock': 'True', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'FFlagEnablePreferredTextSizeScale': 'True', 'FFlagSHUseNewComputeLevelUsesOBB': 'True', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagDebugCheckRenderThreading': 'True', 'FFlagQuaternionPoseCorrection': 'True', 'FFlagVideoFixSoundVolumeRange': 'true', 'FFlagUserShowGuiHideToggles2': 'True', 'FFlagUserShowGuiHideToggles': 'True', 'FFlagDebugForceGenerateHSR': 'True', 'FFlagDisableMemoryTracking': 'True', 'FFlagEnableFPSAndFrameTime': 'True', 'FFlagHSRClusterImprovement': 'True', 'FFlagResetCacheOnLeaveGame': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagSHUseNewComputeLevel': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagAssetPreloadingIXP': 'True', 'FFlagRenderCBRefactor2': 'True', 'FFlagDebugPerfMode': 'True', 'FFlagDisablePostFx': 'True', 'FFlagFineGrainCull': 'True', 'FFlagDebugSkyGray': 'True', 'FFlagVoiceChatRobloxAudioDeviceUpdateRecordedBufferTelemetryEnabled': 'False', 'FFlagVoiceChatCustomAudioDeviceEnableNeedMorePlayoutTelemetry3': 'False', 'FFlagVoiceChatCullingEnableMutedSubsTelemetry': 'False', 'FFlagVoiceChatCullingEnableStaleSubsTelemetry': 'False', 'FFlagVoiceChatPeerConnectionTelemetryDetails': 'False', 'FFlagVngLogoutGlobalAppSessionsOnConversion': 'False', 'FFlagVoiceChatSubscriptionsDroppedTelemetry': 'False', 'FFlagUpdateHTTPCookieStorageFromWKWebView': 'False', 'FFlagChatTranslationEnableSystemMessage': 'False', 'FFlagLuaVoiceChatAnalyticsUseCounterV2': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagLuaVoiceChatAnalyticsUseEventsV2': 'False', 'FFlagDisableFeedbackSoothsayerCheck': 'False', 'FFlagEnableLuaVoiceChatAnalyticsV2': 'False', 'FFlagSimStepPhysicsEnableTelemetry': 'False', 'FFlagSyncWebViewCookieToEngine2': 'False', 'FFlagPropertiesEnableTelemetry': 'False', 'FFlagControlBetaBadgeWithGuac': 'False', 'FFlagEnableTelemetryProtocol': 'False', 'FFlagEnableTelemetryService1': 'False', 'FFlagEnableNudgeAnalyticsV2': 'False', 'FFlagLuaAppHomeVngAppUpsell': 'False', 'FFlagEnableChromeAnalytics': 'False', 'FFlagOpenTelemetryEnabled2': 'False', 'FFlagAlwaysShowVRToggleV3': 'False', 'FFlagOpenTelemetryEnabled': 'False', 'FFlagVngTOSRevisedEnabled': 'False', 'FFlagRenderNoLowFrmBloom': 'False', 'DFIntPolicyServiceReportDetailIsNotSubjectToChinaPoliciesHundredthsPercentage': '10000', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimitPartsModels': '0', 'DFIntVoiceChatTaskStatsTelemetryThrottleHundrethsPercent': '0', 'DFIntNetworkStreamingGCMaxMicroSecondLimitPartsModels': '0', 'DFIntWindowsWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '15', 'DFIntGraphicsOptimizationModeMinFrameTimeTargetMs': '10', 'DFIntHttpBatchApiShutdownInfluxHundrethsPercentage': '0', 'DFIntMacWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionHeartbeatTimerRateMs': '1000', 'DFIntMemoryUtilityCurveSlopeMultiplierHundreths': '1', 'DFIntTrackCountryRegionAPIHundredthsPercent': '10000', 'DFIntMemoryUtilityCurveBaseHundrethsPercent': '2500', 'DFIntMemoryUtilityCurveTotalMemoryReserve': '102400', 'DFIntMemoryUtilityCurveInitialDeltaHundredths': '1', 'DFIntMemoryUtilityCurvePenaltyBuffer': '2000000000', 'DFIntMemoryUtilityCurveFinalDeltaHundredths': '1', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntNetworkStreamingGCMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionBaseRetryTimeMs': '100', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntSignalRCoreKeepAlivePingPeriodMs': '250', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntHttpBatchApi_bgRefreshMaxDelayMs': '30', 'DFIntAnalyticsServiceMonitoringPeriod': '0', 'DFIntSignalRCoreHandshakeTimeoutMs': '3000', 'DFIntSignalRCoreRpcQueueSize': '2147483647', 'DFIntNumAssetsMaxToPreload': '2147483647', 'DFIntMemoryUtilityCurveNumSegments': '0', 'DFIntSignalRCoreHubMaxBackoffMs': '5000', 'DFIntSignalRCoreServerTimeoutMs': '1100', 'DFIntVideoMaxNumberOfVideosPlaying': '0', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntFileCacheReserveSize': '134217728', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntSignalRCoreHubBaseRetryMs': '10', 'DFIntHttpBatchApi_cacheDelayMs': '5', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntNetworkStreamMinGrowSize': '0', 'DFIntDebugRestrictGCDistance': '1', 'DFIntHttpAnalyticsMaxHistory': '0', 'DFIntHttpBatchApi_bgDelayMs': '10', 'DFIntSchemaNetworkStreamSize': '0', 'DFIntHttpBatchApi_maxReqs': '128', 'DFIntHttpBatchApi_maxWaitMs': '5', 'DFIntHttpBatchApi_minWaitMs': '1', 'DFIntTextureQualityOverride': '0', 'DFIntApiRateLimit': '2147483647', 'DFIntCLI61964inKB': '2147483647', 'DFIntNetworkStreamInitSize': '0', 'DFIntS2PhysicsSenderRate': '128', 'DFIntSignalRCoreTimerMs': '50', 'DFIntLCCageDeformLimit': '-1', 'DFIntMaxFrameBufferSize': '4', 'DFIntDataSenderRate': '128', 'DFIntHttpBatchLimit': '64', 'FIntTaskSchedulerMaxTempArenaSizeBytes': '2147483647', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntOpenTelemetryScheduleDelayMillis': '2147483647', 'FIntStudioWebView2TelemetryHundredthsPercent': '0', 'FIntProfileTelemetryTickRateMs': '2147483647', 'FIntLuaAnalyticsReleasePeriod': '2147483647', 'FIntDebugFRMOptionalMSAALevelOverride': '1', 'FIntGrassMovementReducedMotionFactor': '0', 'FIntCameraMaxZoomDistance': '2147483647', 'FIntRenderMeshOptimizeVertexBuffer': '1', 'FIntDebugTextureManagerSkipMips': '10', 'FIntTaskSchedulerAutoThreadLimit': '3', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntRenderLocalLightUpdatesMin': '0', 'FIntMininumRequiredMemoryInGB': '0', 'FIntMininumRequiredMemoryInMB': '0', 'FIntRenderGrassDetailStrands': '0', 'FIntDebugForceMSAASamples': '1', 'FIntRenderShadowIntensity': '0', 'FIntTerrainArraySliceSize': '0', 'FIntRenderShadowmapBias': '-1', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FStringExperienceGuidelinesExplainedPageUrl': 'https://www.gov.cn', 'FStringGoogleAnalyticsAccountPropertyLuaTest': 'null', 'FStringRbxAnalyticsSessionsAllowlist': 'null', 'FStringGetPlayerImageDefaultTimeout': '1', 'FStringAnalyticsSessionIdName': 'null', 'FStringTencentAuthPath': '/tencent/', 'FStringVNGWebshopUrl': 'null'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "Stoofs_Ultra_Graphics_V35",
    'desc': "195 flags",
    'flags': {'DFFlagOptimizeNoCollisionPrimitiveInMidphaseCrash': 'True', 'DFFlagPerformanceControlEnableMemoryProbing3': 'True', 'DFFlagRenderLanczosUpsamplingNonRinging2': 'True', 'DFFlagRenderSmootherStepUpsampling2': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFFlagEnableTexturePreloading': 'True', 'DFFlagTaskSchedulerAvoidSleep': 'True', 'DFFlagDebugOverrideDPIScale': 'True', 'DFFlagEnableSoundPreloading': 'True', 'DFFlagEnableMeshPreloading': 'True', 'DFFlagSimOptimizeSetSize': 'True', 'DFFlagDisableDPIScale': 'True', 'DFFlagDebugPerfMode': 'True', 'DFFlagAggCpuMemRCC': 'True', 'DFFlagVoiceChatPossibleDuplicateSubscriptionsTelemetry': 'False', 'DFFlagSimAdaptiveAdjustTimestepForControllerManager': 'False', 'DFFlagEnableSkipUpdatingGlobalTelemetryInfo2': 'False', 'DFFlagEmitSafetyTelemetryInCallbackEnable': 'False', 'DFFlagRenderBlurMakeResolutionIndependent': 'False', 'DFFlagRobloxTelemetryAddDeviceRAMPointsV2': 'False', 'DFFlagRccLoadSoundLengthTelemetryEnabled': 'False', 'DFFlagWindowsWebViewTelemetryEnabled': 'False', 'DFFlagGraphicsQualityUsageTelemetry': 'False', 'DFFlagReportAssetRequestV1Telemetry': 'False', 'DFFlagReportRenderDistanceTelemetry': 'False', 'DFFlagCollectAudioPluginTelemetry': 'False', 'DFFlagRobloxTelemetryAddDeviceRAM': 'False', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagAlwaysSkipDiskCache': 'False', 'DFFlagNewPackageAnalytics': 'False', 'FFlagPerformanceControlEnablePortTextureManagerTrimMemory': 'True', 'FFlagEnablePreferredTextSizeSettingInMenus2': 'True', 'FFlagKeyframeSequenceUseRuntimeSyncPrims': 'True', 'FFlagUserRaycastPerformanceImprovements': 'True', 'FFlagEnableHarmonyOnFrameRateManager4': 'True', 'FFlagDebugApplyHSRForTransparentMesh': 'True', 'FFlagRemovedRbxRenderingPreProcessor': 'True', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagLargeReplicatorSerializeWrite4': 'True', 'FFlagDebugGridForceFractalUpsample': 'True', 'FFlagLargeReplicatorSerializeRead3': 'True', 'FFlagAvoidUnnecessaryQuadtreeLock': 'True', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagEnablePreferredTextSizeScale': 'True', 'FFlagSHUseNewComputeLevelUsesOBB': 'True', 'FFlagDebugCheckRenderThreading': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagQuaternionPoseCorrection': 'True', 'FFlagVideoFixSoundVolumeRange': 'True', 'FFlagLargeReplicatorEnabled9': 'True', 'FFlagUserShowGuiHideToggles2': 'True', 'FFlagUserShowGuiHideToggles': 'True', 'FFlagDebugForceGenerateHSR': 'True', 'FFlagDisableMemoryTracking': 'True', 'FFlagEnableFPSAndFrameTime': 'True', 'FFlagHSRClusterImprovement': 'True', 'FFlagLargeReplicatorWrite5': 'True', 'FFlagResetCacheOnLeaveGame': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagLargeReplicatorRead5': 'True', 'FFlagRenderInitShadowmaps': 'True', 'FFlagSHUseNewComputeLevel': 'True', 'FFlagAssetPreloadingIXP': 'True', 'FFlagRenderCBRefactor2': 'True', 'FFlagDebugPerfMode': 'True', 'FFlagVoiceChatRobloxAudioDeviceUpdateRecordedBufferTelemetryEnabled': 'False', 'FFlagVoiceChatCustomAudioDeviceEnableNeedMorePlayoutTelemetry3': 'False', 'FFlagVoiceChatCullingEnableMutedSubsTelemetry': 'False', 'FFlagVoiceChatCullingEnableStaleSubsTelemetry': 'False', 'FFlagVoiceChatPeerConnectionTelemetryDetails': 'False', 'FFlagVngLogoutGlobalAppSessionsOnConversion': 'False', 'FFlagVoiceChatSubscriptionsDroppedTelemetry': 'False', 'FFlagUpdateHTTPCookieStorageFromWKWebView': 'False', 'FFlagChatTranslationEnableSystemMessage': 'False', 'FFlagLuaVoiceChatAnalyticsUseCounterV2': 'False', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagLuaVoiceChatAnalyticsUseEventsV2': 'False', 'FFlagDisableFeedbackSoothsayerCheck': 'False', 'FFlagEnableLuaVoiceChatAnalyticsV2': 'False', 'FFlagSimStepPhysicsEnableTelemetry': 'False', 'FFlagGlobalSettingsEngineModule3': 'False', 'FFlagSyncWebViewCookieToEngine2': 'False', 'FFlagPropertiesEnableTelemetry': 'False', 'FFlagControlBetaBadgeWithGuac': 'False', 'FFlagEnableTelemetryProtocol': 'False', 'FFlagEnableTelemetryService1': 'False', 'FFlagEnableNudgeAnalyticsV2': 'False', 'FFlagLuaAppHomeVngAppUpsell': 'False', 'FFlagEnableChromeAnalytics': 'False', 'FFlagOpenTelemetryEnabled2': 'False', 'FFlagAlwaysShowVRToggleV3': 'False', 'FFlagOpenTelemetryEnabled': 'False', 'FFlagVngTOSRevisedEnabled': 'False', 'DFIntPolicyServiceReportDetailIsNotSubjectToChinaPoliciesHundredthsPercentage': '10000', 'DFIntTimestepArbiterBoundingBoxIntersectionThresholdThou1': '1073741823', 'DFIntTimestepArbiterBoundingBoxIntersectionThresholdThou2': '2147483646', 'DFIntTimestepArbiterVelocityCriteriaThresholdFourDt': '1073741823', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimitPartsModels': '0', 'DFIntTimestepArbiterVelocityCriteriaThresholdTwoDt': '2147483646', 'DFIntTimestepArbiterAngAccelerationThresholdThou': '1073741823', 'DFIntVoiceChatTaskStatsTelemetryThrottleHundrethsPercent': '0', 'DFIntNetworkStreamingGCMaxMicroSecondLimitPartsModels': '0', 'DFIntWindowsWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntSimExplicitlyCappedTimestepMultiplier': '2147483646', 'DFIntTimestepArbiterConditionNumberThresholdThou': '1000', 'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '15', 'DFIntGraphicsOptimizationModeMinFrameTimeTargetMs': '10', 'DFIntHttpBatchApiShutdownInfluxHundrethsPercentage': '0', 'DFIntTimestepArbiterAccelerationModelFactorThou': '1000', 'DFIntMacWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntBandwidthManagerApplicationDefaultBps': '1024000', 'DFIntNetworkStreamingGCUrgentMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionHeartbeatTimerRateMs': '1000', 'DFIntBandwidthManagerDataSenderMaxWorkCatchupMs': '8', 'DFIntMemoryUtilityCurveSlopeMultiplierHundreths': '1', 'DFIntTimestepArbiterHumanoidTurningVelThreshold': '1', 'DFIntTrackCountryRegionAPIHundredthsPercent': '10000', 'DFIntMemoryUtilityCurveBaseHundrethsPercent': '2500', 'DFIntMemoryUtilityCurveTotalMemoryReserve': '102400', 'DFIntTimestepArbiterHumanoidLinearVelThreshold': '1', 'DFIntMemoryUtilityCurveInitialDeltaHundredths': '1', 'DFIntMemoryUtilityCurvePenaltyBuffer': '2000000000', 'DFIntMemoryUtilityCurveFinalDeltaHundredths': '1', 'DFIntNetworkStreamingGCMaxMicroSecondLimit': '0', 'DFIntSignalRHubConnectionBaseRetryTimeMs': '100', 'DFIntSimDefaultHumanoidTimestepMultiplier': '8', 'DFIntTimestepArbiterCollidingHumanoidTsm': '25', 'DFIntSignalRCoreKeepAlivePingPeriodMs': '250', 'DFIntHttpBatchApi_bgRefreshMaxDelayMs': '30', 'DFIntMaxUREPayloadSingleLimit': '2147483647', 'DFIntAnalyticsServiceMonitoringPeriod': '0', 'DFIntSignalRCoreHandshakeTimeoutMs': '3000', 'DFIntSignalRCoreRpcQueueSize': '2147483647', 'DFIntNumAssetsMaxToPreload': '2147483647', 'DFIntMemoryUtilityCurveNumSegments': '0', 'DFIntSignalRCoreHubMaxBackoffMs': '5000', 'DFIntSignalRCoreServerTimeoutMs': '1100', 'DFIntTotalRepPayloadLimit': '2147483647', 'DFIntFileCacheReserveSize': '134217728', 'DFIntCliTcMaxPayloadRcv': '2147483647', 'DFIntCliTcMaxPayloadSnd': '2147483647', 'DFIntMaxDataPayloadSize': '2147483647', 'DFIntRccTcMaxPayloadRcv': '2147483647', 'DFIntRccTcMaxPayloadSnd': '2147483647', 'DFIntTimestepArbiterOmegaThou': '1000', 'DFIntSignalRCoreHubBaseRetryMs': '10', 'DFIntCliMaxPayloadRcv': '2147483647', 'DFIntCliMaxPayloadSnd': '2147483647', 'DFIntHttpBatchApi_cacheDelayMs': '5', 'DFIntRccMaxPayloadRcv': '2147483647', 'DFIntRccMaxPayloadSnd': '2147483647', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntNetworkStreamMinGrowSize': '0', 'DFIntHttpAnalyticsMaxHistory': '0', 'DFIntHttpBatchApi_bgDelayMs': '10', 'DFIntSchemaNetworkStreamSize': '0', 'DFIntHttpBatchApi_maxReqs': '128', 'DFIntHttpBatchApi_maxWaitMs': '5', 'DFIntHttpBatchApi_minWaitMs': '1', 'DFIntApiRateLimit': '2147483647', 'DFIntCLI61964inKB': '2147483647', 'DFIntNetworkStreamInitSize': '0', 'DFIntS2PhysicsSenderRate': '128', 'DFIntSignalRCoreTimerMs': '50', 'DFIntMaxFrameBufferSize': '4', 'DFIntDataSenderRate': '128', 'DFIntHttpBatchLimit': '64', 'FIntMaxTimestepMultiplierIntegrationError': '2147483647', 'FIntTaskSchedulerMaxTempArenaSizeBytes': '2147483647', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntMaxTimestepMultiplierAcceleration': '2147483647', 'FIntMaxTimestepMultiplierContstraint': '2147483647', 'FIntOpenTelemetryScheduleDelayMillis': '2147483647', 'FIntStudioWebView2TelemetryHundredthsPercent': '0', 'FIntMaxTimestepMultiplierBuoyancy': '2147483647', 'FIntMaxTimestepMultiplierHumanoid': '2147483647', 'FIntMaxTimestepMultiplierVelocity': '2147483647', 'FIntProfileTelemetryTickRateMs': '2147483647', 'FIntLuaAnalyticsReleasePeriod': '2147483647', 'FIntCameraMaxZoomDistance': '2147483647', 'FIntTaskSchedulerAutoThreadLimit': '3', 'FIntRenderLocalLightUpdatesMin': '0', 'FIntMininumRequiredMemoryInGB': '0', 'FIntMininumRequiredMemoryInMB': '0', 'FIntDebugForceMSAASamples': '4', 'FIntSSAOMipLevels': '8', 'FStringPhysicsAdaptiveTimeSteppingIXP': 'Physics.DefaultTimeStepping', 'FStringExperienceGuidelinesExplainedPageUrl': 'https://www.gov.cn', 'FStringGoogleAnalyticsAccountPropertyLuaTest': 'null', 'FStringRbxAnalyticsSessionsAllowlist': 'null', 'FStringGetPlayerImageDefaultTimeout': '1', 'FStringAnalyticsSessionIdName': 'null', 'FStringTencentAuthPath': '/tencent/', 'FStringVNGWebshopUrl': 'null'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "Use if 1st super low end pc dosent work",
    'desc': "168 flags",
    'flags': {'FLogNetwork': '7', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagHighlightOutlinesOnMobile': 'True', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDebugDisableTelemetryV2Event': 'True', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FIntRenderShadowIntensity': '0', 'FFlagDisablePostFx': 'True', 'FIntTerrainArraySliceSize': '0', 'DFIntTaskSchedulerTargetFps': '60', 'FStringDebugGraphicsPreferredGPUName': 'Intel(R) HD Graphics', 'FFlagDisableFeedbackSoothsayerCheck': 'False', 'DFFlagDisableDPIScale': 'False', 'DFIntCanHideGuiGroupId': '32380007', 'FFlagAlwaysShowVRToggleV3': 'False', 'FFlagChatTranslationSettingEnabled3': 'False', 'FFlagUserShowGuiHideToggles': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntV1MenuLanguageSelectionFeaturePerMillageRollout': '0', 'FFlagEnablePartyVoiceOnlyForEligibleUsers': 'False', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFIntLCCageDeformLimit': '-1', 'FIntFRMMaxGrassDistance': '0', 'DFFlagPerformanceControlEnableMemoryProbing3': 'True', 'FIntPhysicsStepsPerSecond': '0', 'FIntRenderLocalLightUpdatesMax': '1', 'FFlagMessageBusCallOptimization': 'True', 'DFFlagRobloxTelemetryAddDeviceRAMPointsV2': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntHACDPointSampleDistApartTenths': '2147483647', 'FStringGetPlayerImageDefaultTimeout': '1', 'DFFlagTeleportClientAssetPreloadingDoingExperiment2': 'True', 'DFFlagTeleportClientAssetPreloadingEnabledIXP': 'True', 'DFIntPreloadAvatarAssets': '2147483647', 'FIntRenderMaxShadowAtlasUsageBeforeDownscale': '0', 'FIntRenderLocalLightUpdatesMin': '1', 'DFFlagEnablePreloadAvatarAssets': 'True', 'FIntRenderGrassDetailStrands': '0', 'DFFlagEnableSkipUpdatingGlobalTelemetryInfo2': 'False', 'DFIntTextureQualityOverride': '0', 'FFlagAvatarChatIncludeSelfViewOnTelemetry': 'False', 'DFIntNumAssetsMaxToPreload': '2147483647', 'DFFlagReportAssetRequestV1Telemetry': 'False', 'DFFlagEmitSafetyTelemetryInCallbackEnable': 'False', 'FFlagRenderSkipReadingShaderData': 'False', 'DFIntTrackCountryRegionAPIHundredthsPercent': '10000', 'DFFlagSimSolverSendPerfTelemetryToElasticSearch2': 'False', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagFixSensitivityTextPrecision': 'False', 'FIntUnifiedLightingBlendZone': '0', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFFlagRenderHighlightManagerPrepare': 'True', 'DFFlagRobloxTelemetryV2PointEncoding': 'False', 'FFlagFixParticleAttachmentCulling': 'False', 'FIntSSAOMipLevels': '0', 'FFlagEnablePreferredTextSizeStyleFixesInAvatarExp': 'True', 'DFIntTeleportClientAssetPreloadingHundredthsPercentage2': '100000', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagTeleportClientAssetPreloadingDoingExperiment': 'True', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'FFlagUserCameraControlLastInputTypeUpdate': 'False', 'FFlagVideoReportHardwareBufferMetrics': 'True', 'FFlagAddHapticsToggle': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'FFlagImproveShiftLockTransition': 'True', 'FIntSSAO': '0', 'DFIntSignalRCoreHubMaxBackoffMs': '5000', 'FFlagFastGPULightCulling3': 'True', 'FStringTencentAuthPath': 'null', 'DFIntSignalRCoreHubBaseRetryMs': '10', 'DFFlagRemoveTelemetryFlushOnJobClose': 'False', 'FIntDebugFRMOptionalMSAALevelOverride': '0', 'DFIntS2PhysicsSenderRate': '128', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntAnimationLodFacsDistanceMax': '0', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'DFIntContentProviderPreloadHangTelemetryHundredthsPercentage': '0', 'FFlagShaderLightingRefactor': 'False', 'DFFlagSimOptimizeSetSize': 'True', 'DFFlagDSTelemetryV2ReplaceSeparator': 'False', 'DFIntCharacterLoadTime': '1', 'DFFlagEnableSoundPreloading': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'FFlagBetaBadgeLearnMoreLinkFormview': 'False', 'DFIntMemoryUtilityCurveTotalMemoryReserve': '0', 'FFlagUserBetterInertialScrolling': 'True', 'FIntVertexSmoothingGroupTolerance': '0', 'DFIntAssetPreloading': '2147483647', 'FFlagContentProviderPreloadHangTelemetry': 'False', 'FFlagVoiceBetaBadge': 'False', 'FIntPreferredTextSizeSettingBetaFeatureRolloutPercent': '100', 'FFlagControlBetaBadgeWithGuac': 'False', 'FStringTerrainMaterialTablePre2022': '', 'DFFlagCollectAudioPluginTelemetry': 'False', 'FFlagGameBasicSettingsFramerateCap5': 'false', 'FFlagLuauCodegen': 'True', 'DFIntMaxFrameBufferSize': '4', 'FFlagPreloadTextureItemsOption4': 'True', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'FFlagVideoServiceAddHardwareCodecMetrics': 'True', 'DFFlagTeleportClientAssetPreloadingEnabledIXP2': 'True', 'DFIntTeleportClientAssetPreloadingHundredthsPercentage': '100000', 'FFlagEnableBubbleChatFromChatService': 'False', 'FIntDebugTextureManagerSkipMips': '8', 'DFIntVideoMaxNumberOfVideosPlaying': '0', 'FFlagShoeSkipRenderMesh': 'False', 'FIntUITextureMaxUpdateDepth': '-1', 'FFlagAssetPreloadingIXP': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'FIntRenderShadowmapBias': '0', 'DFIntMemoryUtilityCurveBaseHundrethsPercent': '10000', 'FIntGrassMovementReducedMotionFactor': '0', 'FIntDirectionalAttenuationMaxPoints': '0', 'FFlagTextureUseACR3': 'True', 'DFIntSignalRCoreServerTimeoutMs': '20000', 'FFlagEnablePreferredTextSizeGuiService': 'True', 'FStringTerrainMaterialTable2022': '', 'FFlagEnablePreferredTextSizeScale': 'True', 'FFlagUnifiedLightingBetaFeature': 'False', 'DFIntSignalRCoreRpcQueueSize': '2147483647', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FIntDebugForceMSAASamples': '0', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagNewLightAttenuation': 'True', 'FFlagFixOutdatedParticles2': 'False', 'DFFlagEnableMeshPreloading2': 'False', 'FFlagRenderNoLowFrmBloom': 'False', 'FFlagFixOutdatedTimeScaleParticles': 'False', 'DFIntSignalRCoreKeepAlivePingPeriodMs': '25', 'DFFlagEnableTexturePreloading': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagFRMRefactor': 'False', 'DFFlagRobloxTelemetryAddDeviceRAM': 'False', 'FIntFRMMinGrassDistance': '0', 'FFlagFixParticleEmissionBias2': 'False', 'DFFlagTaskSchedulerAvoidSleep': 'True', 'DFFlagSampleAndRefreshRakPing': 'True', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagEnablePreferredTextSizeStyleFixesInAppShell3': 'True', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'FIntCameraMaxZoomDistance': '2147483647', 'DFFlagDebugOverrideDPIScale': 'False', 'DFFlagGraphicsQualityUsageTelemetry': 'False', 'DFFlagEnableFmodErrorsTelemetry': 'False', 'FIntRenderLocalLightFadeInMs': '0', 'FFlagDebugForceFSMCPULightCulling': 'True', 'DFIntSignalRCoreHandshakeTimeoutMs': '3000', 'DFFlagDebugPerfMode': 'True', 'FFlagEnablePartyVoiceOnlyForUnfilteredThreads': 'False', 'FFlagChatTranslationEnableSystemMessage': 'False', 'DFFlagRccLoadSoundLengthTelemetryEnabled': 'False', 'FFlagRenderLegacyShadowsQualityRefactor': 'True', 'FIntCLI20390_2': '0', 'FIntTextureUseACRHundredthPercent': '10000', 'FIntRenderMeshOptimizeVertexBuffer': '1', 'FFlagLoginPageOptimizedPngs': 'True', 'FFlagDebugCheckRenderThreading': 'True', 'DFIntAnimationLodFacsDistanceMin': '0', 'FFlagDebugSSAOForce': 'False', 'FFlagQuaternionPoseCorrection': 'True', 'FFlagAddDMLogging': 'False', 'DFIntMemoryUtilityCurveNumSegments': '100', 'FFlagPreloadAllFonts': 'True', 'FFlagEnablePreferredTextSizeSettingInMenus2': 'True', 'FFlagRenderFixGrassPrepass': 'False'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "less graphics Fast flag",
    'desc': "108 flags",
    'flags': {'DFFlagCollectAudioPluginTelemetry': 'False', 'DFFlagDSTelemetryV2ReplaceSeparator': 'False', 'DFFlagDebugPerfMode': 'True', 'DFFlagEmitSafetyTelemetryInCallbackEnable': 'False', 'DFFlagEnableFmodErrorsTelemetry': 'False', 'DFFlagEnableMeshPreloading2': 'True', 'DFFlagEnableSkipUpdatingGlobalTelemetryInfo2': 'False', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagGraphicsQualityUsageTelemetry': 'False', 'DFFlagPerformanceControlEnableMemoryProbing3': 'True', 'DFFlagRccLoadSoundLengthTelemetryEnabled': 'False', 'DFFlagReportAssetRequestV1Telemetry': 'False', 'DFFlagReportRenderDistanceTelemetry': 'False', 'DFFlagRobloxTelemetryAddDeviceRAMPointsV2': 'False', 'DFFlagRobloxTelemetryV2PointEncoding': 'False', 'DFFlagSendRenderFidelityTelemetry': 'False', 'DFFlagTaskSchedulerAvoidSleep': 'True', 'DFFlagVoiceChatPossibleDuplicateSubscriptionsTelemetry': 'False', 'DFFlagWindowsWebViewTelemetryEnabled': 'False', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntAssetCacheErrorLogHundredthsPercent': '2147483647', 'DFIntBandwidthManagerApplicationDefaultBps': '796850000', 'DFIntBandwidthManagerDataSenderMaxWorkCatchupMs': '5', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntCachedPatchLoadDelayMilliseconds': '1', 'DFIntCharacterLoadTime': '1', 'DFIntDataSenderRate': '256', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntFileCacheReserveSize': '1036372536', 'DFIntHttpCacheAsyncWriterMaxPendingSize': '1036372536', 'DFIntHttpCacheCleanScheduleAfterMs': '1036372536', 'DFIntHttpCacheCleanUpToAvailableSpaceMiB': '1036372536', 'DFIntHttpCacheEvictionExemptionMapMaxSize': '1036372536', 'DFIntHttpCachePerfHundredthsPercent': '1036372536', 'DFIntHttpCachePerfSamplingRate': '1036372536', 'DFIntHttpCacheReportSlowWritesMinDuration': '1036372536', 'DFIntMacWebViewTelemetryThrottleHundredthsPercent': '0', 'DFIntMaxFrameBufferSize': '4', 'DFIntMemCacheMaxCapacityMB': '1036372536', 'DFIntNumAssetsMaxToPreload': '2147483647', 'DFIntPolicyServiceReportDetailIsNotSubjectToChinaPoliciesHundredthsPercentage': '10000', 'DFIntReportCacheDirSizesHundredthsPercent': '1036372536', 'DFIntS2PhysicsSenderRate': '256', 'DFIntSignalRCoreHandshakeTimeoutMs': '3000', 'DFIntSignalRCoreHubBaseRetryMs': '10', 'DFIntSignalRCoreHubMaxBackoffMs': '5000', 'DFIntSignalRCoreKeepAlivePingPeriodMs': '25', 'DFIntSignalRCoreRpcQueueSize': '2147483647', 'DFIntSignalRCoreServerTimeoutMs': '20000', 'DFIntSoundServiceCacheCleanupMaxAgeDays': '1036372536', 'DFIntThirdPartyInMemoryCacheCapacity': '1036372536', 'DFIntUserIdPlayerNameCacheLifetimeSeconds': '1036372536', 'DFIntVoiceChatTaskStatsTelemetryThrottleHundrethsPercent': '0', 'DFIntWindowsWebViewTelemetryThrottleHundredthsPercent': '0', 'DFStringTelemetryV2Url': '0.0.0.0', 'DFStringWebviewUrlAllowlist': 'www.youtube-nocookie.com', 'FFlagClearCacheableContentProviderOnGameLaunch': 'True', 'FFlagDebugForceFSMCPULightCulling': 'True', 'FFlagDebugRenderingSetDeterministic': 'True', 'FFlagDebugSkyGray': 'True', 'FFlagEnableFPSAndFrameTime': 'True', 'FFlagEnableLuaVoiceChatAnalyticsV2': 'False', 'FFlagEnableTelemetryProtocol': 'False', 'FFlagEnableTelemetryService1': 'False', 'FFlagFastGPULightCulling3': 'True', 'FFlagLuaVoiceChatAnalyticsBanMessage': 'False', 'FFlagLuaVoiceChatAnalyticsUseCounterV2': 'False', 'FFlagLuaVoiceChatAnalyticsUseEventsV2': 'False', 'FFlagLuaVoiceChatAnalyticsUsePointsV2': 'False', 'FFlagNewLightAttenuation': 'True', 'FFlagOpenTelemetryEnabled': 'False', 'FFlagPropertiesEnableTelemetry': 'False', 'FFlagRenderNoLowFrmBloom': 'False', 'FFlagSyncWebViewCookieToEngine2': 'False', 'FFlagUpdateHTTPCookieStorageFromWKWebView': 'False', 'FFlagUseCachedAudibilityMeasurements': 'True', 'FFlagVoiceChatCullingEnableMutedSubsTelemetry': 'False', 'FFlagVoiceChatCullingEnableStaleSubsTelemetry': 'False', 'FFlagVoiceChatCustomAudioDeviceEnableNeedMorePlayoutTelemetry3': 'False', 'FFlagVoiceChatCustomAudioMixerEnableUpdateSourcesTelemetry2': 'False', 'FFlagVoiceChatDontSendTelemetryForPubIceTrickle': 'False', 'FFlagVoiceChatPeerConnectionTelemetryDetails': 'False', 'FFlagVoiceChatRobloxAudioDeviceUpdateRecordedBufferTelemetryEnabled': 'False', 'FFlagVoiceChatSubscriptionsDroppedTelemetry': 'False', 'FIntCameraMaxZoomDistance': '2147483647', 'FIntDebugFRMOptionalMSAALevelOverride': '0', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntGrassMovementReducedMotionFactor': '0', 'FIntLuaVoiceChatAnalyticsPointsThrottle': '0', 'FIntRenderGrassDetailStrands': '0', 'FIntRenderLocalLightFadeInMs': '0', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntRenderShadowmapBias': '-1', 'FIntStudioWebView2TelemetryHundredthsPercent': '0', 'FLogRobloxTelemetry': '0', 'FLogTencentAuthPath': 'null', 'FStringExperienceGuidelinesExplainedPageUrl': 'https://www.gov.cn', 'FStringGetPlayerImageDefaultTimeout': '1', 'FStringTencentAuthPath': 'null', 'FStringXboxExperienceGuidelinesUrl': 'https://www.gov.cn'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "lower ping",
    'desc': "16 flags",
    'flags': {'DFIntConnectionMTUSize': '900', 'FIntRakNetResendBufferArrayLength': '128', 'FFlagOptimizeNetwork': 'True', 'FFlagOptimizeNetworkRouting': 'True', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagOptimizeServerTickRate': 'True', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntServerTickRate': '60', 'DFIntRakNetResendRttMultiple': '1', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntOptimizePingThreshold': '50', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntNetworkPrediction': '120', 'DFIntNetworkLatencyTolerance': '1', 'DFIntMinimalNetworkPrediction': '0.1'},
    'tag': "NET",
})

BUILTIN_PRESETS.append({
    'name': "Disable Telemetry (useless if u already get 100+ fps)",
    'desc': "68 flags",
    'flags': {'DFFlagBrowserTrackerIdTelemetryEnabled': 'False', 'DFFlagDSTelemetryEnableMetricRecorder': 'False', 'DFFlagEmitSafetyTelemetryInCallbackEnable': 'False', 'DFFlagEnableCppSoundTelemetry6': 'False', 'DFFlagEnablePerfDataGatherTelemetry2': 'False', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagRccLoadSoundLengthTelemetryEnabled': 'False', 'DFFlagWindowsWebViewTelemetryEnabled': 'False', 'FFlagEnableAvatarFacechatReplOverRCCTelemetry': 'False', 'FFlagEnableClickToMoveUsageTelemetry2': 'False', 'FFlagEnableLogCullingTelemetryForControl': 'False', 'FFlagEnableMessageBusUnSubscribeErrorTelemetry': 'False', 'FFlagEnableServiceInitBreakdownTelemetry': 'False', 'FFlagEnableSoundSessionTelemetry5': 'False', 'FFlagEnableTelemetryProtocol': 'False', 'FFlagEnableTelemetryService1': 'False', 'FFlagEnableTelemetryServiceMemoryCPUInfo': 'False', 'FFlagEnableTelemetryServicePlaySessionInfo': 'False', 'FFlagEnableVRComfortSettingsTelemetry': 'False', 'FFlagOpenTelemetryEnabled2': 'False', 'FFlagOpenTelemetryUseOtlpExportingEnabled': 'False', 'FFlagSimCSGV3EnableMemoryTelemetry': 'False', 'FFlagSimCSGV3EnableSpeedMemoryTelemetry': 'False', 'FFlagSimStepPhysicsEnableTelemetry': 'False', 'FFlagVoiceChatCullingEnableStaleSubsTelemetry': 'False', 'FFlagVoiceChatCustomAudioDeviceEnableNeedMorePlayoutTelemetry3': 'False', 'FFlagVoiceChatRobloxAudioDeviceUpdateRecordedBufferTelemetryEnabled': 'False', 'DFFlagDebugDisableTelemetryAfterTest': 'True', 'DFFlagDisableFastLogTelemetry': 'True', 'DFFlagEnableQualityResetSessionTracking': 'False', 'FFlagEnableAffiliateLinksAuthenticatedVisitTracking': 'False', 'FFlagEnableAffiliateLinksQualifiedSignUpTracking': 'False', 'FFlagEnableExperienceMenuSessionTracking': 'False', 'FFlagEnableLastLoginMethodTracking': 'False', 'FFlagDisableMemoryTracking': 'True', 'FFlagDisableStreamingTunableMemoryTracking': 'True', 'DFFlagCLI_147010_ReportAttributesWithHangTelemetry2': 'False', 'DFFlagReportAssetRequestV1Telemetry': 'False', 'DFFlagReportAssetRequestV2Telemetry': 'False', 'DFFlagReportLegacyFRMStatsToTelemetryV2': 'False', 'DFFlagReportMemoryStatsToTelemetryV2': 'False', 'DFFlagReportRenderDistanceTelemetry': 'False', 'DFFlagReportReplicatorStatsToTelemetryV22': 'False', 'FFlagReportFRMGPUFrameTimeTelemetryInPerfdata': 'False', 'FFlagReportMeshesUploadTelemetry': 'False', 'FFlagReportRenderDistanceTelemetry': 'False', 'DFIntPerformanceControlEventBasedTelemetryEffectPredictionEventNumReportsPerSecond': '0', 'DFIntPerformanceControlEventBasedTelemetryTunableChangeEventNumReportsPerSecond': '0', 'DFIntServerReportRakNetBandwidthTelemetryHundredthsPercentage': '0', 'DFFlagPolicyServiceReportIsNotSubjectToChinaPolicies': 'True', 'DFFlagPolicyServiceReportDetailIsNotSubjectToChinaPolicies': 'True', 'DFIntPolicyServiceReportDetailIsNotSubjectToChinaPoliciesHundredthsPercentage': '0', 'DFFlagReportOutputDeviceWithRobloxTelemetry': 'False', 'DFIntReportDeviceInfoRate': '0', 'DFIntReportOutputDeviceInfoEventRateHundredthsPercentage': '0', 'DFIntReportOutputDeviceInfoRateHundredthsPercentage': '0', 'DFIntReportRecordingDeviceInfoEventRateHundredthsPercentage': '0', 'DFIntReportRecordingDeviceInfoRateHundredthsPercentage': '0', 'FFlagCrashpadReportVendorDeviceFLevelQLevelWindows': 'False', 'FFlagLoadAndReportDeviceBTIDCookie': 'False', 'FIntReportDeviceInfoRollout': '0', 'FIntProfileTelemetryTickRateMs': '2147483647', 'DFIntAnimatorTelemetryCollectionRate': '0', 'DFIntPerformanceControlEventBasedTelemetryEffectPredictionEventRatePoints': '0', 'DFIntPerformanceControlEventBasedTelemetryTunableChangeEventRatePoints': '0', 'FIntOpenTelemetrySampleRateHundredthPercent': '0', 'DFIntTrackerTelemetryEventRate': '0', 'DFFlagRobloxTelemetryReliabilityCounterRefactor2': 'False'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "New no animations",
    'desc': "173 flags",
    'flags': {'FFlagHandleAltEnterFullscreenManually': 'False', 'FLogNetwork': '7', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFFlagSimOptimizeSetSize': 'True', 'FFlagKeepZeroInfluenceBones': 'False', 'DFFlagTeleportClientAssetPreloadingEnabled9': 'True', 'DFIntJoinDataCompressionLevel': '0', 'DFIntTimestepArbiterAccelerationModelFactorThou': '50000', 'DFIntNetworkInProcessLimitGameplayMsClient': '0', 'DFFlagFastEndUpdateLoop': 'true', 'DFFlagRakNetCalculateApplicationFeedback2': 'False', 'DFIntPhysicsReceiveNumParallelTasks': '5', 'FFlagDebugDisableOptimizedBytecode': 'False', 'FIntDebugTextureManagerSkipMips': '6', 'FFlagEnableAnimatorSkipCopyPreviousRigKeyOnJointModification': 'True', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'FFlagPreComputeAcceleratorArrayForSharingTimeCurve': 'True', 'DFIntServerRakNetBandwidthPlayerSampleRate': '2147483647', 'FFlagRenderDebugCheckThreading2': 'True', 'DFIntDebugPerformanceControlFrameTime': '2', 'FFlagAdServiceEnabled': 'False', 'FIntRuntimeMaxNumOfThreads': '1000000', 'FIntGrassMovementReducedMotionFactor': '0', 'DFFlagMergeFakeInputEvents3': 'True', 'DFFlagRakNetDetectNetUnreachable': 'True', 'FIntRobloxGuiBlurIntensity': '0', 'FFlagTouchscreenSupport': 'True', 'DFIntGraphicsOptimizationModeMaxFrameTimeTargetMs': '25', 'DFIntSendRakNetStatsInterval': '2147483647', 'FFlagEnableZstdForClientSettings': 'False', 'DFIntGraphicsOptimizationModeFRMFrameRateTarget': '144', 'DFIntTouchSenderMaxBandwidthBps': '-1', 'DFIntRakNetLoopMs': '1', 'DFIntMaxMissedWorldStepsRemembered': '2147483467', 'FFlagNewCameraControls_SpeedAdjustEnum': 'False', 'DFFlagAnimatorAnywhere': 'True', 'DFFlagTeleportClientAssetPreloadingDoingExperiment2': 'True', 'DFIntInterpolationNumParallelTasks': '5', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFFlagSolverStateReplicatedOnly2': 'True', 'FFlagFasterPreciseTime4': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntSendGameServerDataMaxLen': '9999999', 'FIntRuntimeMaxNumOfSchedulers': '1000000', 'FFlagLuaMenuPerfImprovements': 'True', 'DFIntClusterEstimatedCompressionRatioHundredths': '0', 'DFFlagReplicateCreateToPlayer': 'True', 'DFIntMegaReplicatorNumParallelTasks': '5', 'DFFlagRakNetUnblockSelectOnShutdownByWritingToSocket': 'True', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntServerFramesBetweenJoins': '1', 'FIntTaskSchedulerAutoThreadLimit': '6', 'DFIntRuntimeConcurrency': '12', 'DFIntDataSenderRate': '20000', 'DFIntClusterCompressionLevel': '0', 'FFlagDebugRenderCollectGpuCounters': 'True', 'DFFlagDebugLargeReplicatorForceFullSend': 'true', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'DFFlagDebugOverrideDPIScale': 'False', 'DFIntReplicatorAnimationTrackLimitPerAnimator': '-1', 'DFIntBufferCompressionLevel': '0', 'DFIntClientPacketHealthyAllocationPercent': '20', 'FFlagSortKeyOptimization': 'True', 'FIntRenderGrassDetailStrands': '0', 'FFlagMouseGetPartOptimization': 'True', 'DFFlagAnimatorEnableNewAdornments': 'True', 'FIntSmoothMouseSpringFrequencyTenths': '100', 'DFIntBufferCompressionThreshold': '100', 'DFIntConnectingTimerInterval': '10', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntRakNetNakResendDelayMsMax': '1', 'FIntRakNetResendBufferArrayLength': '256', 'DFFlagDebugPerfMode': 'True', 'DFFlagAcceleratorUpdateOnPropsAndValueTimeChange': 'True', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntGameNetCompressionLodByteBudgetThresholdPct': '0', 'DFIntClientPacketExcessMicroseconds': '1000', 'DFIntMaxFrameBufferSize': '4', 'DFIntFrameRateMSToReduceTouchEvents': '30', 'DFIntReplicationDataCacheNumParallelTasks': '5', 'FFlagEnableInGameMenuSongbirdABTest': 'False', 'DFIntBatchThumbnailResultsSizeCap': '200', 'FIntFRMMaxGrassDistance': '0', 'DFIntWaitOnRecvFromLoopEndedMS': '10', 'FFlagRenderSkipReadingShaderData': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFIntClientNetworkInfluxHundredthsPercentage': '0', 'DFIntRakNetApplicationFeedbackScaleUpThresholdPercent': '0', 'FFlagDebugForceFSMCPULightCulling': 'True', 'DFIntRakNetSelectTimeoutMs': '1', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntServerBandwidthPlayerSampleRateFacsOverride': '2147483647', 'DFFlagReplicatorCheckReadTableCollisions': 'True', 'DFFlagNetworkUseZstdWrapper': 'False', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'DFFlagRakNetUseSlidingWindow4': 'True', 'DFIntServerBandwidthPlayerSampleRate': '2147483647', 'FFlagLuaAppLegacyInputSettingRefactor': 'True', 'FFlagEnableZstdDictionaryForClientSettings': 'False', 'DFIntSendItemLimit': '5', 'DFFlagTeleportClientAssetPreloadingEnabledIXP2': 'True', 'FIntRuntimeMaxNumOfLatches': '1000000', 'DFIntNumAssetsMaxToPreload': '9999999', 'DFIntMaxReceiveToDeserializeLatencyMilliseconds': '10', 'DFIntPerformanceControlReportingPeriodInMs': '700', 'FFlagFastGPULightCulling3': 'True', 'DFIntJoinDataItemEstimatedCompressionRatioHundreths': '0', 'DFFlagCorrectServerReplicatorStatsIP': 'True', 'DFFlagNextGenRepRollbackOverbudgetPackets': 'True', 'FIntEnableCullableScene2HundredthPercent3': '1000', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'FFlagDebugCheckRenderThreading': 'True', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFFlagDebugLargeReplicatorDisableDelta': 'true', 'FFlagFixTextureCompositorFramebufferManagement2': 'True', 'FIntRuntimeMaxNumOfSemaphores': '1000000', 'FFlagDebugAvatarChatVisualization': 'True', 'DFIntClusterSenderMaxJoinBandwidthBps': '2100000000', 'FIntActivatedCountTimerMSKeyboard': '0', 'DFIntClusterSenderMaxUpdateBandwidthBps': '2100000000', 'DFIntRakNetNakResendDelayMs': '1', 'DFFlagRakNetDetectRecvThreadOverload': 'True', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'FFlagDebugNextGenReplicatorEnabledWriteCFrameColor': 'True', 'FFlagDebugCodegenOptSize': 'True', 'DFIntClientPacketMaxFrameMicroseconds': '200', 'DFIntRakNetApplicationFeedbackMaxSpeedBPS': '0', 'DFIntTimestepArbiterAngAccelerationThresholdThou': '2000', 'FIntRenderShadowmapBias': '0', 'DFFlagJointIrregularityOptimization': 'True', 'DFIntCodecMaxOutgoingFrames': '10000', 'FIntFRMMinGrassDistance': '0', 'DFFlagRakNetEnablePoll': 'True', 'FIntLuaGcParallelMinMultiTasks': '6', 'DFIntNetworkClusterPacketCacheNumParallelTasks': '5', 'FIntSimSolverResponsiveness': '2147483647', 'FFlagDebugRenderingSetDeterministic': 'True', 'DFIntNetworkSchemaCompressionRatio': '0', 'FFlagQuaternionPoseCorrection': 'True', 'FIntRuntimeMaxNumOfConditions': '1000000', 'DFIntMaxDataPacketPerSend': '2147483647', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagUserCameraControlLastInputTypeUpdate': 'True', 'DFIntClientPacketMaxDelayMs': '1', 'DFIntTeleportClientAssetPreloadingHundredthsPercentage2': '1000', 'FIntActivatedCountTimerMSMouse': '0', 'DFIntInitialAccelerationLatencyMultTenths': '1', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntS2PhysicsSenderRate': '25000', 'DFIntPerformanceControlFrameTimeMax': '1', 'FFlagEnablePerformanceControlService': 'True', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '5', 'DFIntTaskSchedulerJobInGameThreads': '6', 'DFIntTaskSchedulerJobInitThreads': '6', 'DFIntNetworkQualityResponderUnit': '10', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntNetworkQualityResponderMaxWaitTime': '1', 'FFlagReportGpuLimitedToPerfControl': 'False', 'FIntInterpolationMaxDelayMSec': '100', 'DFIntTouchSenderMaxBandwidthBpsScaling': '2', 'DFFlagClampIncomingReplicationLag': 'True', 'DFIntRakNetApplicationFeedbackScaleUpFactorHundredthPercent': '0', 'FIntRuntimeMaxNumOfDPCs': '64', 'DFFlagCanClientReplicateProp': 'False', 'FFlagSimCSGV3IncrementalTriangulationStreamingCompression': 'False', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFFlagReplicatorSeparateVarThresholds': 'True', 'FFlagMessageBusCallOptimization': 'True', 'DFIntMaxAcceptableUpdateDelay': '1', 'FIntRuntimeMaxNumOfMutexes': '1000000', 'FFlagOnlyDecrementCompletenessIfReplicating': 'True', 'DFFlagSimSmoothedRunningController2': 'True', 'DFIntMaxActiveAnimationTracks': '0'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "UNCAP FPS",
    'desc': "2 flags",
    'flags': {'DFIntTaskSchedulerTargetFps': '2147483647', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "black sky",
    'desc': "4 flags",
    'flags': {'FIntDebugTextureManagerSkipMips': '8', 'DFIntTextureQualityOverride': '0', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FIntVertexSmoothingGroupTolerance': '10000'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "Reduce screenshake",
    'desc': "141 flags",
    'flags': {'DFIntLargePacketQueueSizeCutoffMB': '1000', 'FStringErrorUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'FIntRenderShadowIntensity': '0', 'DFIntRakNetNakResendDelayRttPercent': '50', 'DFIntReportRecordingDeviceInfoRateHundredthsPercentage': '0', 'DFIntDebugFRMQualityLevelOverride': '3', 'FFlagDebugGraphicsPreferD3D11': 'True', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'FIntTerrainOTAMaxTextureSize': '1024', 'FFlagDisablePostFx': 'True', 'DFIntRakNetLoopMs': '1', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'FFlagRenderGpuTextureCompressor': 'True', 'FIntMeshContentProviderForceCacheSize': '268435456', 'DFIntUserIdPlayerNameCacheSize': '33554432', 'FFlagDebugGraphicsPreferVulkan': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FIntTerrainArraySliceSize': '0', 'FIntFontSizePadding': '3', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'FIntBootstrapperTelemetryReportingHundredthsPercentage': '0', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '1', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntRakNetStaleSendQueueTriggerMs': '1', 'DFStringCrashUploadToBacktraceMacPlayerToken': 'null', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'DFStringAnalyticsEventStreamUrlEndpoint': 'null', 'DFStringLightstepHTTPTransportUrlHost': 'null', 'DFIntClientPacketMaxFrameMicroseconds': '80', 'DFIntTextureQualityOverride': '1', 'DFIntS2PhysicsSenderRate': '100', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFStringLightstepToken': 'null', 'FFlagEnableInGameMenuChromeABTest4': 'False', 'DFStringCrashUploadToBacktraceWindowsPlayerToken': 'null', 'FFlagDebugGraphicsPreferOpenGL': 'True', 'DFIntNetworkQualityResponderUnit': '50', 'DFStringTelemetryV2Url': 'null', 'DFStringHttpPointsReporterUrl': 'null', 'DFIntMaxProcessPacketsStepsPerCyclic': '70000', 'DFStringRobloxAnalyticsURL': 'null', 'FStringCoreScriptBacktraceErrorUploadToken': 'null', 'FFlagNewLightAttenuation': 'True', 'FIntEmotesAnimationsPerPlayerCacheSize': '16777216', 'DFStringCrashUploadToBacktraceBaseUrl': 'null', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FLogNetwork': '7', 'FIntFRMMinGrassDistance': '0', 'FIntDebugForceMSAASamples': '1', 'FFlagGraphicsEnableD3D10Compute': 'True', 'DFStringAltHttpPointsReporterUrl': 'null', 'DFIntRakNetMtuValue2InBytes': '3950', 'DFIntRakNetNakResendDelayMs': '10', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '1', 'DFFlagDebugEnableInterpolationVisualizer': 'TRUE', 'DFIntRakNetMtuValue1InBytes': '4000', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'DFIntMaxFrameBufferSize': '30', 'FFlagPreloadTextureItemsOption4': 'True', 'FFlagEnableQuickGameLaunch': 'True', 'DFFlagDebugVisualizeAllPropertyChanges': 'True', 'DFIntRakNetPingFrequencyMillisecond': '1', 'FFlagPreloadAllFonts': 'True', 'DFIntTeleportClientAssetPreloadingHundredthsPercentage2': '500000', 'DFStringLightstepHTTPTransportUrlPath': 'null', 'DFIntVisibilityCheckRayCastLimitPerFrame': '200', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '1', 'DFFlagDisableDPIScale': 'True', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntFRMMaxGrassDistance': '0', 'FStringGamesUrlPath': '/games/', 'DFIntTaskSchedulerTargetFps': '60', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '500000', 'FIntCameraMaxZoomDistance': '99999', 'DFIntInterpolationNumParallelTasks': '50', 'DFIntNumAssetsMaxToPreload': '2147483647', 'FFlagFastGPULightCulling3': 'True', 'FFlagAdServiceEnabled': 'False', 'FStringPerformanceSendMeasurementAPISubdomain': 'opt-out', 'FIntRenderGrassDetailStrands': '0', 'FFlagTopBarUseNewBadge': 'True', 'FIntRakNetResendBufferArrayLength': '1024', 'DFIntRakNetResendRttMultiple': '1', 'FFlagReconnectDisabled': 'True', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FFlagGameBasicSettingsFramerateCap5': 'False', 'FIntRobloxGuiBlurIntensity': '0', 'DFIntConnectionMTUSize': '1472', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFFlagRakNetUseSlidingWindow4': 'True', 'FIntDefaultMeshCacheSizeMB': '256', 'DFStringRobloxAnalyticsSubDomain': 'opt-out', 'DFIntRakNetMtuValue3InBytes': '1200', 'FIntRenderShadowmapBias': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'FIntUITextureMaxRenderTextureSize': '1024', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'FIntRakNetDatagramMessageIdArrayLength': '1024', 'DFIntRakNetNakResendDelayMsMax': '100', 'FIntRenderLocalLightUpdatesMax': '1', 'DFFlagDebugPauseVoxelizer': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '1', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFIntReportOutputDeviceInfoRateHundredthsPercentage': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '1', 'FFlagDebugRenderingSetDeterministic': 'True', 'FIntRomarkStartWithGraphicQualityLevel': '1', 'FIntRuntimeMaxNumOfThreads': '2400', 'FIntTaskSchedulerThreadMin': '3', 'FStringTerrainMaterialTable2022': '', 'FStringTerrainMaterialTablePre2022': '', 'FFlagEnableCommandAutocomplete': 'False', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'DFIntVoiceChatVolumeThousandths': '6000', 'DFFlagDebugPerfMode': 'True', 'FFlagVoiceBetaBadge': 'False', 'DFFlagDebugSkipMeshVoxelizer': 'True', 'FIntDebugTextureManagerSkipMips': '2', 'DFIntTouchSenderMaxBandwidthBpsScaling': '-1', 'DFIntCanHideGuiGroupId': '32380007', 'DFIntAnimationLodFacsDistanceMin': '0', 'FFlagFacialAnimationStreamingServiceUniverseSettingsEnableVideo': 'False', 'DFIntAnimationLodFacsDistanceMax': '0', 'FStringFacialAnimation1BetaFeatureUrl': 'https://opt-out.roblox.com/', 'FFlagFacialAnimationStreamingCheckPauseStateAfterEmote2': 'False', 'FFlagFacialAnimationStreamingServiceUniverseSettingsEnableAudio': 'False', 'FFlagFacialAnimationStreamingClearTrackImprovementsV2': 'False', 'FFlagFacialAnimationStreamingServiceUserSettingsMock': 'False', 'FFlagFacialAnimationStreamingSearchForReplacementWhenRemovingAnimator': 'False', 'DFFlagFacialAnimationStreaming2': 'False', 'DFFlagReduceFacialAnimationsWhenFacsStreaming2': 'False', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'FFlagFacialAnimationStreamingValidateAnimatorBeforeRemoving': 'False', 'FFlagFacialAnimationStreamingIfNoDynamicHeadDisableA2C': 'False', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagFacialAnimationRecordingBetaFeature': 'False', 'FFlagRenderHighlightTransparency': 'True'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "high render distance low graphics",
    'desc': "2 flags",
    'flags': {'DFFlagTextureQualityOverrideEnabled': 'true', 'DFIntTextureQualityOverride': '3'},
    'tag': "PERF",
})

BUILTIN_PRESETS.append({
    'name': "sky box + no lava damage",
    'desc': "2 flags",
    'flags': {'FIntDebugTextureManagerSkipMips': '10', 'DFIntTouchSenderMaxBandwidthBps': '-1'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "WFfflags (hasnbot PC) 16 LP + 240fps",
    'desc': "34 flags",
    'flags': {'DFFlagTeleportClientAssetPreloadingDoingExperiment2': 'true', 'DFFlagTeleportClientAssetPreloadingEnabledIXP2': 'true', 'DFFlagNextGenRepRollbackOverbudgetPackets': 'true', 'DFFlagTeleportClientAssetPreloadingEnabled9': 'true', 'FFlagDebugNextGenReplicatorEnabledWriteCFrameColor': 'true', 'FFlagFixTextureCompositorFramebufferManagement2': 'true', 'FFlagUserCameraControlLastInputTypeUpdate': 'true', 'FFlagRenderDynamicResolutionScale9': 'true', 'FFlagGraphicsEnableD3D10Compute': 'true', 'FFlagDebugRenderCollectGpuCounters': 'true', 'FFlagRenderSkipReadingShaderData': 'true', 'FFlagSimEnableDCD16': 'true', 'FFlagTouchscreenSupport': 'true', 'FFlagNewCameraControls_SpeedAdjustEnum': 'false', 'FFlagReportGpuLimitedToPerfControl': 'false', 'FFlagAdServiceEnabled': 'false', 'DFIntTeleportClientAssetPreloadingHundredthsPercentage2': '1000', 'DFIntGraphicsOptimizationModeFRMFrameRateTarget': '240', 'DFIntPerformanceControlReportingPeriodInMs': '700', 'DFIntDebugPerformanceControlFrameTime': '2', 'DFIntFrameRateMSToReduceTouchEvents': '30', 'DFIntPerformanceControlFrameTimeMax': '4', 'DFIntNumAssetsMaxToPreload': '9999999', 'DFIntMaxFrameBufferSize': '4', 'DFIntRuntimeConcurrency': '16', 'DFIntMegaReplicatorNumParallelTasks': '16', 'DFIntNetworkClusterPacketCacheNumParallelTasks': '16', 'DFIntReplicationDataCacheNumParallelTasks': '16', 'DFIntTaskSchedulerJobInGameThreads': '16', 'DFIntTaskSchedulerJobInitThreads': '16', 'FIntEnableCullableScene2HundredthPercent3': '1000', 'FIntLuaGcParallelMinMultiTasks': '16', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '16', 'FIntTaskSchedulerAutoThreadLimit': '16'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Wfflags (change depending on PC)",
    'desc': "34 flags",
    'flags': {'DFFlagTeleportClientAssetPreloadingDoingExperiment2': 'True', 'DFFlagTeleportClientAssetPreloadingEnabledIXP2': 'True', 'DFFlagNextGenRepRollbackOverbudgetPackets': 'True', 'DFFlagTeleportClientAssetPreloadingEnabled9': 'True', 'FFlagDebugNextGenReplicatorEnabledWriteCFrameColor': 'True', 'FFlagFixTextureCompositorFramebufferManagement2': 'True', 'FFlagUserCameraControlLastInputTypeUpdate': 'True', 'FFlagRenderDynamicResolutionScale9': 'True', 'FFlagGraphicsEnableD3D10Compute': 'True', 'FFlagDebugRenderCollectGpuCounters': 'True', 'FFlagRenderSkipReadingShaderData': 'True', 'FFlagSimEnableDCD16': 'True', 'FFlagTouchscreenSupport': 'True', 'FFlagNewCameraControls_SpeedAdjustEnum': 'False', 'FFlagReportGpuLimitedToPerfControl': 'False', 'FFlagAdServiceEnabled': 'False', 'DFIntTeleportClientAssetPreloadingHundredthsPercentage2': '1000', 'DFIntGraphicsOptimizationModeFRMFrameRateTarget': '144', 'DFIntPerformanceControlReportingPeriodInMs': '700', 'DFIntDebugPerformanceControlFrameTime': '2', 'DFIntFrameRateMSToReduceTouchEvents': '30', 'DFIntPerformanceControlFrameTimeMax': '4', 'DFIntNumAssetsMaxToPreload': '9999999', 'DFIntMaxFrameBufferSize': '4', 'DFIntRuntimeConcurrency': '16', 'DFIntMegaReplicatorNumParallelTasks': '16', 'DFIntNetworkClusterPacketCacheNumParallelTasks': '16', 'DFIntReplicationDataCacheNumParallelTasks': '16', 'DFIntTaskSchedulerJobInGameThreads': '16', 'DFIntTaskSchedulerJobInitThreads': '16', 'FIntEnableCullableScene2HundredthPercent3': '1000', 'FIntLuaGcParallelMinMultiTasks': '16', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '16', 'FIntTaskSchedulerAutoThreadLimit': '16'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "10 FINAL i hope",
    'desc': "10 flags",
    'flags': {'FFlagAvatarRenderIdleAnimations': 'false', 'FFlagAvatarRenderFacialAnimations': 'false', 'DFFlagSimOptimizeGeometryChangedAssemblies3': 'true', 'FFlagCameraInterpolationReducedMotion': 'true', 'FIntGrassMovementReducedMotionFactor': '0', 'FFlagGfxDisableOneLink': 'true', 'FFlagRenderCheckThreading': 'true', 'DFIntMaxFrameBufferSize': '4', 'FFlagPreloadAllFonts': 'true', 'FFlagEnableQuickGameLaunch': 'false'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "11 CHERRY on top",
    'desc': "10 flags",
    'flags': {'DFIntDebugDynamicRenderKiloPixels': '100', 'FIntRenderShadowIntensity': '0', 'FFlagDebugSkyGray': 'true', 'FFlagFastGPULightCulling3': 'true', 'FIntTerrainArraySliceSize': '0', 'FIntDebugTextureManagerSkipMips': '2', 'FFlagDisablePostFx': 'true', 'DFIntFRMQualityLevelOverride': '1', 'FIntRenderLocalLightUpdateRate': '1', 'FFlagRenderCheckThreading': 'true'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "2 new best box",
    'desc': "8 flags",
    'flags': {'DebugLimitMinTextureResolutionWhenSkipMips': '2147483647', 'DoNotSkipMipsBasedOnSystemMemoryPS': 'True', 'TM2SkipMipsForUnstreamable2': 'True', 'RenderUseTextureManager224': 'False', 'DebugTextureManagerSkipMips': '3', 'EnablePowerTraceModule': 'True', 'IncludePowerSaverMode': 'True', 'DebugFRMQualityLevelOverride': '1'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "3 additional flags to sigma and box",
    'desc': "30 flags",
    'flags': {'FFlagDebugDisableParticles': 'True', 'FIntParticleMaxEmitters': '0', 'FFlagDebugForceSingleThreadedParticles': 'True', 'FFlagDebugDisableBeams': 'True', 'FIntDebugMaxBeams': '0', 'FFlagRenderAtmosphericSkies': 'False', 'FFlagAtmosphericSkies': 'False', 'FFlagDebugDisablePostFX': 'True', 'FFlagRenderDepthOfField': 'False', 'FFlagRenderSunRays': 'False', 'FFlagRenderBloom': 'False', 'FIntFRMMinGrassDistance': '0', 'FIntRenderGrassDetailStrands': '0', 'FIntFRMDistanceSensitivityFactor': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'FFlagDebugDisableShadows': 'True', 'FFlagRenderInitShadowmaps': 'False', 'FIntRenderLocalLightFadeStartDistance': '1', 'FIntRenderLocalLightFadeEndDistance': '2', 'FIntRenderLocalLightUpdatesMin': '0', 'FIntMaxLocalLightsPerCell': '0', 'FFlagGraphicsUseReducedShaderComplexity': 'True', 'FFlagRenderFixFog': 'False', 'FFlagGlobalWindRendering': 'False', 'FFlagGlobalWindActivated': 'False', 'FIntRenderGrassHeightFieldCorrelation': '0', 'FFlagRenderEnableGlobalInstancingD3D11': 'True', 'FFlagDebugRenderForceTechnologyVoxel': 'True', 'FIntSSAOSamples': '0'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "4 SMEAR",
    'desc': "14 flags",
    'flags': {'DFFlagTextureQualityOverrideEnabled': 'true', 'FIntTextureQualityOverride': '1', 'FIntRomarkTextureQualityModifier': '-20', 'FIntMaxTextureSize': '1', 'FIntMeshLODQualityLow': '0', 'FIntRenderShadowIntensity': '0', 'DFFlagDebugPauseVoxelizer': 'true', 'FFlagDisablePostFx': 'true', 'DFFlagDebugRenderForceTechnologyVoxel': 'true', 'FFlagDebugSSAOForce': 'false', 'FIntSSAOMipLevels': '0', 'FFlagDebugSkyGray': 'true', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "5 SMEAR 2",
    'desc': "13 flags",
    'flags': {'DFFlagTextureQualityOverrideEnabled': 'true', 'DFIntTextureQualityOverride': '0', 'FIntTextureCompositorLowResFactor': '1', 'FIntMaxTextureSize': '1', 'FIntDebugTextureManagerSkipMips': '8', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'FIntRenderShadowIntensity': '0', 'DFFlagDebugRenderForceTechnologyVoxel': 'true', 'FFlagDebugSkyGray': 'true', 'FFlagDisablePostFx': 'true'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "6 ADD",
    'desc': "15 flags",
    'flags': {'DFFlagTextureQualityOverrideEnabled': 'true', 'DFIntTextureQualityOverride': '0', 'FIntTextureCompositorLowResFactor': '1', 'FIntMaxTextureSize': '1', 'FIntDebugTextureManagerSkipMips': '8', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'FIntRenderShadowIntensity': '0', 'DFFlagDebugRenderForceTechnologyVoxel': 'true', 'FFlagDebugSkyGray': 'true', 'FFlagDisablePostFx': 'true', 'FIntFRMMaxGrassDistance': '0', 'FIntRenderReflectanceTextureSize': '1'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "7 BLUR RENDER",
    'desc': "7 flags",
    'flags': {'FIntRenderLocalLightUpdatesMax': '1', 'DFFlagDebugPauseVoxelizer': 'True', 'FIntRenderDynamicLightUpdateRate': '1', 'FIntUnifiedLightingBlendZone': '0', 'FFlagShaderLightingRefactor': 'True', 'DFIntCSGv2LodsToGenerate': '0', 'DFIntCSGv2LodMinTriangleCount': '0'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "8 CRANK",
    'desc': "10 flags",
    'flags': {'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagRenderShadows': 'false', 'FIntRenderShadowDistance': '0', 'FFlagGlobalWindActivated': 'false', 'FIntRenderLocalLightUpdatesMax': '1', 'DFFlagDebugPauseVoxelizer': 'True', 'FIntRenderDynamicLightUpdateRate': '1', 'DFIntMaxFrameBufferSize': '4'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "9 step",
    'desc': "10 flags",
    'flags': {'FFlagFacialAnimationStreamlining': 'false', 'FIntAnimationSkipRenderingUpdateRate': '100', 'FFlagAnimationLodRefactor': 'true', 'FFlagCameraShakeRefactor': 'false', 'FIntCameraShakeIntensity': '0', 'FFlagEnableExplosionVFXShaking': 'false', 'FIntRenderPhysicsGridRadius': '32', 'FFlagInterpolationInPhysicsLoop': 'True', 'DFIntMaxFrameBufferSize': '4', 'DFFlagDebugPauseVoxelizer': 'True'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "Acquaflag2",
    'desc': "196 flags",
    'flags': {'FLogNetwork': '7', 'FFlagFixGraphicsQuality': 'True', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'FIntFRMMaxGrassDistance': '0', 'FFlagEnableMenuControlsABTest': 'False', 'DFFlagDisableDPIScale': 'True', 'FFlagEnableInGameMenuModernization': 'False', 'DFIntTaskSchedulerTargetFps': '69420', 'FFlagEnableInGameMenuControls': 'False', 'FFlagEnableV3MenuABTest3': 'True', 'DFIntCanHideGuiGroupId': '32380007', 'FFlagDisableNewIGMinDUA': 'True', 'DFStringCrashUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagEnableMenuModernizationABTest': 'False', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDebugGraphicsPreferOpenGL': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '1', 'DFIntReportOutputDeviceInfoRateHundredthsPercentage': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagEnableLightstepReporting2': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagEnableFmodErrorsTelemetry': 'False', 'FStringPerformanceSendMeasurementAPISubdomain': 'opt-out', 'FFlagCommitToGraphicsQualityFix': 'True', 'DFIntRakNetMtuValue2InBytes': '1240', 'FFlagRenderGpuTextureCompressor': 'True', 'FIntUITextureMaxRenderTextureSize': '1024', 'FIntDebugForceMSAASamples': '1', 'FFlagDisablePostFx': 'True', 'FFlagPreloadAllFonts': 'True', 'FStringInGameMenuChromeForcedUserIds': '1353919681', 'DFStringRobloxAnalyticsURL': 'http://opt-out.roblox.com', 'DFIntRakNetNakResendDelayMs': '10', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagEnableInGameMenuV3': 'True', 'DFIntConnectionMTUSize': '900', 'FStringNote': 'CHANGE TO false IF YOU DONT WANNA HAVE GRAY SKYBOX', 'FIntRenderShadowIntensity': '0', 'FIntRakNetResendBufferArrayLength': '1024', 'DFIntCodecMaxOutgoingFrames': '10000', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FIntTerrainArraySliceSize': '8', 'DFIntRakNetResendRttMultiple': '1', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FFlagOptimizeNetworkRouting': 'True', 'FFlagOptimizeNetwork': 'True', 'DFStringAltHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'FFlagDontCreatePingJob': 'True', 'DFFlagQueueDataPingFromSendData': 'True', 'FFlagAdServiceEnabled': 'False', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFFlagEnableGCapsHardwareTelemetry': 'False', 'DFIntRakNetMtuValue3InBytes': '1200', 'DFIntOptimizePingThreshold': '50', 'FIntLmsClientRollout2': '0', 'DFStringRobloxAnalyticsSubDomain': 'opt-out', 'FFlagFastGPULightCulling3': 'True', 'FFlagLuaAppSystemBar': 'False', 'DFFlagRakNetUseSlidingWindow4': 'True', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'DFIntTextureQualityOverride': '0', 'DFFlagDebugAnalyticsSendUserId': 'False', 'DFFlagAudioDeviceTelemetry': 'False', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'DFStringHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'FIntFontSizePadding': '3', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'FStringPartTexturePackTablePre2022': '{"foil":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[238,238,238,255]},"asphalt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[227,227,228,234]},"basalt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[160,160,158,238]},"brick":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[229,214,205,227]},"cobblestone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,219,219,243]},"concrete":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[225,225,224,255]},"crackedlava":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[76,79,81,156]},"diamondplate":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[210,210,210,255]},"fabric":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[221,221,221,255]},"glacier":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[225,229,229,243]},"glass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[254,254,254,7]},"granite":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[210,206,200,255]},"grass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[196,196,189,241]},"ground":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[165,165,160,240]},"ice":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[235,239,241,248]},"leafygrass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[182,178,175,234]},"limestone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[250,248,243,250]},"marble":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[181,183,193,249]},"metal":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[226,226,226,255]},"mud":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[193,192,193,252]},"pavement":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,218,219,236]},"pebble":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[204,203,201,234]},"plastic":{"ids":["","rbxassetid://13576561565"],"color":[255,255,255,255]},"rock":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[211,211,210,248]},"corrodedmetal":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[206,177,163,180]},"salt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[249,249,249,255]},"sand":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,216,210,240]},"sandstone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[241,234,230,246]},"slate":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[235,234,235,254]},"snow":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[239,240,240,255]},"wood":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[217,209,208,255]},"woodplanks":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[207,208,206,254]}}', 'DFIntUserIdPlayerNameCacheSize': '33554432', 'FFlagInGameMenuV1FullScreenTitleBar': 'False', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'DFIntLightstepHTTPTransportHundredthsPercent2': '0', 'DFIntRakNetMtuValue1InBytes': '1280', 'FFlagOptimizeServerTickRate': 'True', 'DFIntRakNetLoopMs': '1', 'FFlagDebugLightGridShowChunks': 'False', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'FIntRenderGrassHeightScaler': '0', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'FIntRenderGrassDetailStrands': '0', 'FIntFRMMinGrassDistance': '0', 'DFIntGoogleAnalyticsLoadPlayerHundredth': '0', 'FFlagDebugDisplayFPS': 'False', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntNetworkPrediction': '120', 'DFFlagSimReportCPUInfo': 'False', 'FFlagEnableQuickGameLaunch': 'False', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'FFlagTopBarUseNewBadge': 'True', 'FIntBootstrapperTelemetryReportingHundredthsPercentage': '0', 'DFIntDebugFRMQualityLevelOverride': '1', 'FIntRenderShadowmapBias': '0', 'DFStringAnalyticsEventStreamUrlEndpoint': 'opt-out', 'DFIntRakNetNakResendDelayRttPercent': '50', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FIntRakNetDatagramMessageIdArrayLength': '1024', 'FIntRenderLocalLightUpdatesMin': '1', 'FFlagDebugSkyGray': 'False', 'FIntRenderLocalLightUpdatesMax': '1', 'FFlagNewLightAttenuation': 'True', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'FIntMeshContentProviderForceCacheSize': '268435456', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntRakNetNakResendDelayMsMax': '100', 'FFlagEnableMenuModernizationABTest2': 'False', 'FFlagGameBasicSettingsFramerateCap5': 'True', 'FFlagReconnectDisabled': 'True', 'FFlagGpuGeometryManager7': 'True', 'DFIntServerTickRate': '60', 'DFFlagBatchAssetApiNoFallbackOnFail': 'False', 'FStringCredit': 'Potato Mode | @KiwisASkid on YT', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'DFIntHardwareTelemetryHundredthsPercent': '0', 'FIntEmotesAnimationsPerPlayerCacheSize': '16777216', 'FIntDefaultMeshCacheSizeMB': '256', 'DFIntReportRecordingDeviceInfoRateHundredthsPercentage': '0', 'FFlagBatchAssetApi': 'True', 'DFStringAltTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FStringTopBarBadgeLearnMoreLink': 'https://youtube.com/@KiwisASkid/', 'FStringErrorUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'FFlagLuaAppExitModalDoNotShow': 'True', 'DFIntNetworkLatencyTolerance': '1', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFStringTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'FFlagLuaAppExitModal2': 'False', 'FFlagAnimationClipMemCacheEnabled': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '1', 'FFlagPreloadTextureItemsOption4': 'True', 'FIntTerrainOTAMaxTextureSize': '1024', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagEnableSoundTelemetry': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '1', 'FStringPartTexturePackTable2022': '{"foil":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"asphalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"basalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"brick":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"cobblestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"concrete":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"crackedlava":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"diamondplate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"fabric":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"glacier":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"glass":{"ids":["rbxassetid://98732842556","rbxassetid://9438453972"],"color":[255, 255, 255, 255]},"granite":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"grass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"ground":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"ice":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"leafygrass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"limestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"marble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"metal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"mud":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"pavement":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"pebble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"plastic":{"ids":["","rbxassetid://0"],"color":[255, 255, 255, 255]},"rock":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"corrodedmetal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"salt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"sand":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"sandstone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"slate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"snow":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"wood":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"woodplanks":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]}}', 'DFFlagEnableHardwareTelemetry': 'False', 'FFlagEnableInGameMenuChrome': 'True', 'FFlagEnableInGameMenuChromeABTest3': 'False', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'DFIntMaxFrameBufferSize': '4', 'FFlagDebugRenderingSetDeterministic': 'False', 'FIntRomarkStartWithGraphicQualityLevel': '1', 'FIntRuntimeMaxNumOfThreads': '2400', 'FIntTaskSchedulerThreadMin': '3', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'FFlagRenderPerformanceTelemetry': 'False', 'FIntRenderLocalLightFadeInMs_enabled': '99999', 'FFlagEnableAudioOutputDevice': 'false', 'FFlagEnableReportAbuseMenuRoact2': 'false', 'FIntReportDeviceInfoRollout': '0', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagDebugDisableOTAMaterialTexture': 'true', 'FFlagEnableReportAbuseMenuRoactABTest2': 'False', 'DFIntAnimationLodFacsDistanceMax': '0', 'FFlagEnableBubbleChatFromChatService': 'False', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'DFFlagESGamePerfMonitorEnabled': 'False', 'FIntStartupInfluxHundredthsPercentage': '0', 'FFlagEnableBetaBadgeLearnMore': 'false', 'FFlagEnableInGameMenuChromeABTest2': 'False', 'FFlagVoiceBetaBadge': 'false', 'FFlagEnableBubbleChatConfigurationV2': 'False', 'FFlagMSRefactor5': 'False', 'DFFlagDebugPerfMode': 'True', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FFlagGlobalWindRendering': 'false', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FFlagCloudsReflectOnWater': 'False', 'FFlagRenderCheckThreading': 'True', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FIntRobloxGuiBlurIntensity': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagPreloadMinimalFonts': 'True', 'FFlagNullCheckCloudsRendering': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagGameBasicSettingsFramerateCap': 'True', 'FIntCameraMaxZoomDistance': '99999', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'DFIntAnimationLodFacsDistanceMin': '0', 'FStringTerrainMaterialTablePre2022': '', 'FStringTerrainMaterialTable2022': ''},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "Moonia flag 2",
    'desc': "106 flags",
    'flags': {'FIntDebugTextureManagerSkipMips': '3', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'FFlagTelemetryCacheCleanupSlowStats3': 'False', 'DFFlagDebugDisableTelemetryAfterTest': 'True', 'FFlagSkipAttributeCopyIfNoTelemetry': 'True', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagHttpCacheTrackAllAssets2': 'False', 'DFFlagDisableFastLogTelemetry': 'True', 'DFFlagEXPCHAT1499Telemetry': 'False', 'DFFlagEXPR2140Telemetry': 'False', 'FFlagAdServiceEnabled': 'False', 'FFlagLuaAppHomeVngAppUpsell': 'False', 'FStringVNGWebshopUrl': 'null', 'FStringGameLaunchLinkURL': '(?:(?:https?://\\w+\\.roblox(?:labs)?\\.com(?:/[A-Za-z]{2}(-[A-Za-z0-9]{2,3})?)?/games/start\\?)|(?:roblox(?:mobile)?://(?:experiences/start\\?)?))(?:(?:(?:(?:id=\\d+)|(?:placeid=\\d+)|(?:accessCode=(?:\\w|\\-)+)|(?:reservedServerAccessCode=(?:\\w|\\-)+)|(?:launchData=(?:.+))|(?:eventId=(?:\\d+)/?', 'DFStringTelemetryV2Url': 'https://opt-out.roblox.com/', 'DFStringRobloxAnalyticsURL': 'https://opt-out.roblox.com/', 'DFStringHttpPointsReporterUrl': 'https://opt-out.roblox.com/', 'DFStringCrashUploadToBacktraceBaseUrl': 'https://opt-out.roblox.com/', 'FStringTencentAuthPath': 'Unterial', 'FLogTencentAuthPath': 'Unterial', 'DFIntRobloxTelemetryBatchedReporterTimerIntervalMs': '2147483647', 'DFIntRobloxTelemetryTryCutAndSendSignalTimerIntervalMs': '2147483647', 'DFIntRbxStorageTelemetryIntervalMS': '2147483647', 'FIntProfileTelemetryTickRateMs': '2147483647', 'DFStringRobloxTelemetryReliabilityCountAllowList': 'null', 'FStringCategorizedL2SessionNamesForTelemetryCounter': 'null', 'FFlagEnableTelemetryProtocol': 'False', 'FFlagEnableTelemetryService1': 'False', 'FFlagEnableServiceInitBreakdownTelemetry': 'False', 'FFlagOpenTelemetryEnabled2': 'False', 'FLogRealtimeProtocol': 'Error,0', 'DFIntDataModelAnalysisServiceTelemetryThrottle': '0', 'DFIntRobloxTelemetryRealtimeEventsThrottleHundredthsPercent': '0', 'DFFlagReportReplicatorStatsToTelemetryV22': 'False', 'FFlagRealtimeReliabilityMeasurementEnable': 'False', 'DFFlagEnableRLReceiveFailureTracking': 'False', 'DFFlagCorrectServerReplicatorStatsIP': 'False', 'DFFlagXhrTrackSeq': 'False', 'DFFlagHttpTrackBandwidthBasedOnMsgSize': 'False', 'DFFlagRakNetTelemV2DownloadBwTracker': 'False', 'DFFlagHttpTelemV2DownloadBwTracker': 'False', 'DFLogClientRecvFromRaknet': 'Error,0', 'DFLogLargeReplicatorTrace': 'Error,0', 'FFlagSimDcdRefactorDelta3': 'True', 'FFlagSimDcdDeltaReplication': 'True', 'DFFlagReplicateCreateToPlayer': 'True', 'DFFlagSolverStateReplicatedOnly2': 'True', 'DFFlagReplicatorSeparateVarThresholds': 'True', 'DFFlagUpdateBoundExtentsForHugeMixedReplicationComponents': 'True', 'FFlagSpecifyNetworkReplicatorScopeForItems': 'True', 'FFlagSpecifyNetworkReplicatorScope': 'True', 'DFIntServerBandwidthPlayerSampleRateFacsOverride': '2147465500', 'DFIntServerRakNetBandwidthPlayerSampleRate': '2147465500', 'DFIntReportNetworkSyncMemoryUsage2EveryXSeconds': '86400', 'DFIntNetworkObjectStatsCollectorGlobalCapThrottleHP': '0', 'DFIntServerBandwidthPlayerSampleRate': '2147465500', 'DFIntMaxDebugNetworkUpdateTimestamps': '0', 'DFIntSendRakNetStatsInterval': '86400', 'DFIntMaxProcessPacketsStepsPerCyclic': '100', 'DFIntMaxProcessPacketsJobScaling': '250', 'DFIntSignalRCoreRpcQueueSize': '256', 'DFIntSignalRCoreTimerMs': '750', 'FStringPhysicsAdaptiveTimeSteppingIXP': 'Physics.DefaultTimeStepping', 'DFFlagSimAdaptiveAdjustTimestepForControllerManager': 'False', 'FFlagEnablePhysicsAdaptiveTimeSteppingIXP': 'True', 'DFIntTimestepArbiterCollidingHumanoidTsm': '100', 'DFIntSimDefaultHumanoidTimestepMultiplier': '100', 'DFIntSimExplicitlyCappedTimestepMultiplier': '500', 'FIntMaxTimestepMultiplierVelocity': '100', 'FIntMaxTimestepMultiplierHumanoid': '100', 'FIntMaxTimestepMultiplierAcceleration': '100', 'DFIntTimestepArbiterHumanoidLinearVelThreshold': '10', 'DFIntTimestepArbiterHumanoidTurningVelThreshold': '6', 'DFIntGraphicsOptimizationModeMinFrameTimeTargetMs': '10', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFIntMaxFrameBufferSize': '4', 'FIntDefaultJitterN': '0', 'DFIntAnimatorRetargetInterpolateFKCorrectionMinAngleDeg': '0', 'DFIntAnimatorRetargetInterpolateFKCorrectionMaxAngleDeg': '360', 'DFIntAngularVelociryLimit': '360', 'DFFlagSimActivateLinearVelocityReactionForceEnabled': 'False', 'DFFlagSimAdaptiveExplicitlyMarkInterpolatedAssemblies': 'True', 'DFFlagDebugDisableAngularVelocityInterpolationComponent': 'True', 'FIntLinearDeformerSmoothScalePct': '10', 'FIntLinearDeformerTriWeightMode': '0', 'DFFlagAcceleratorUpdateOnPropsAndValueTimeChange': 'True', 'FFlagPreComputeAcceleratorArrayForSharingTimeCurve': 'True', 'FFlagKeyframeSequenceUseRuntimeSyncPrims': 'True', 'FFlagHumanoidStateUseRuntimeSyncPrims': 'True', 'DFFlagMergeFakeInputEvents4': 'True', 'FFlagUserCameraControlLastInputTypeUpdate': 'False', 'FFlagMovePrerenderV2': 'False', 'DFIntLatencyLoggingThresholdMs': '86400000', 'DFFlagSimSmoothedRunningController2': 'True', 'DFFlagHumanoidReplicateSimulated2': 'True', 'FFlagLuaMenuPerfImprovements': 'True', 'FIntInterpolationMaxDelayMSec': '100', 'FIntCLI20390_2': '1', 'FFlagFasterPreciseTime4': 'True', 'DFIntTaskSchedulerTargetFps': '3000', 'FFlagDebugDisplayFPS': 'False', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FIntTaskSchedulerAutoThreadLimit': '15', 'DFIntRuntimeConcurrency': '15', 'DFIntGraphicsOptimizationModeFRMFrameRateTarget': '240', 'DFIntDebugDynamicRenderKiloPixels': '-1'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "SEM BRILHO",
    'desc': "120 flags",
    'flags': {'DFIntTaskSchedulerTargetFps': '9999', 'FIntGetPlayerImageDefaultTimeout': '1', 'FIntMaxFrameBufferSize': '1', 'FBoolDebugPerfMode': 'True', 'FBoolHandleAltEnterFullscreenManually': 'False', 'FBoolHighlightOutlinesOnMobile': 'True', 'FBoolGraphicsQualityUsageTelemetry': 'False', 'FIntBulletContactBreakOrthogonalThresholdActivatePercent': '2147483647', 'FIntBulletContactBreakOrthogonalThresholdPercent': '-2147483647', 'FIntBulletContactBreakThresholdPercent': '-2147483648', 'FIntMaximumUnstickForceInGs': '-50000', 'FBoolRccLoadSoundLengthTelemetryEnabled': 'False', 'FBoolReportAssetRequestV1Telemetry': 'False', 'FBoolRobloxTelemetryAddDeviceRAMPointsV2': 'False', 'FIntDebugForceMSAASamples': '1', 'FIntRuntimeMaxNumOfMutexes': '1000000', 'FBoolDisableDPIScale': 'True', 'FIntAnimationLodFacsDistanceMin': '10', 'FIntJoinDataItemEstimatedCompressionRatioHundreths': '0', 'FIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FBoolLuaAppLegacyInputSettingRefactor': 'True', 'FIntCanHideGuiGroupId': '32380007', 'FIntConnectionMTUSize': '900', 'FIntNetworkQualityResponderUnit': '10', 'FIntRuntimeMaxNumOfConditions': '1000000', 'FIntRobloxGuiBlurIntensity': '0', 'FIntMaxProcessPacketsJobScaling': '10000', 'FIntClusterCompressionLevel': '0', 'FIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'FIntGrassMovementReducedMotionFactor': '0', 'FBoolEnableZstdForClientSettings': 'False', 'FIntClientPacketHealthyAllocationPercent': '20', 'FIntTargetTimeDelayFacctorTenths': '13', 'FIntMaxProcessPacketsStepsAccumulated': '0', 'FIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'FIntRakNetApplicationFeedbackScaleUpFactorHundredthPercent': '0', 'FIntCodecMaxIncomingPackets': '100', 'FBoolRenderDebugCheckThreading2': 'True', 'FIntRuntimeMaxNumOfSemaphores': '1000000', 'FIntMaxReceiveToDeserializeLatencyMilliseconds': '10', 'FIntClientPacketExcessMicroseconds': '1000', 'FIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FIntSimSolverResponsiveness': '2147483647', 'FIntWaitOnRecvFromLoopEndedMS': '10', 'FIntVoiceChatVolumeThousandths': '6000', 'FIntRakNetSelectTimeoutMs': '1', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FIntRuntimeMaxNumOfSchedulers': '1000000', 'FIntNetworkSchemaCompressionRatio': '0', 'FIntClientNetworkInfluxHundredthsPercentage': '0', 'FIntMaxProcessPacketsStepsPerCyclic': '5000', 'FIntAnimationLodFacsVisibilityDenominator': '2', 'FBoolDebugCheckRenderThreading': 'True', 'FIntSmoothMouseSpringFrequencyTenths': '100', 'FBoolRakNetEnablePoll': 'True', 'FBoolReplicateCreateToPlayer': 'True', 'FIntBufferCompressionLevel': '0', 'FIntInitialAccelerationLatencyMultTenths': '1', 'FIntClientPacketMaxDelayMs': '1', 'FIntNetworkQualityResponderMaxWaitTime': '1', 'FIntAnimationLodFacsDistanceMax': '50', 'FIntNetworkInProcessLimitGameplayMsClient': '0', 'FIntMaxDataPacketPerSend': '100000', 'FBoolDebugGraphicsPreferD3D11': 'True', 'FIntGameNetCompressionLodByteBudgetThresholdPct': '0', 'FIntMaxAcceptableUpdateDelay': '1', 'FIntRakNetApplicationFeedbackScaleUpThresholdPercent': '0', 'FBoolFacialAnimationStreaming2': 'False', 'FIntRakNetNakResendDelayMs': '1', 'FStringTerrainMaterialTable2022': '', 'FIntTaskSchedulerThreadMin': '4', 'FIntActivatedCountTimerMSMouse': '300', 'FIntRenderLocalLightUpdatesMax': '2', 'FBoolFastGPULightCulling3': 'True', 'FBoolDebugRenderingSetDeterministic': 'True', 'FIntFRMMaxGrassDistance': '0', 'FIntActivatedCountTimerMSKeyboard': '300', 'FIntRenderLocalLightUpdatesMin': '6', 'FIntInterpolationMaxDelayMSec': '500', 'FIntRakNetLoopMs': '1', 'FIntRuntimeMaxNumOfLatches': '1000000', 'FBoolUserCameraControlLastInputTypeUpdate': 'False', 'FBoolGraphicsGLEnableHQShadersExclusion': 'False', 'FIntTrackCountryRegionAPIHundredthsPercent': '10000', 'FBoolDebugPauseVoxelizer': 'True', 'FIntRakNetResendBufferArrayLength': '128', 'FStringTerrainMaterialTablePre2022': '', 'FIntRuntimeMaxNumOfThreads': '1000000', 'FIntInterpolationAwareTargetTimeLerpHundredth': '100', 'FIntFRMMinGrassDistance': '0', 'FIntRenderLocalLightFadeInMs': '0', 'FBoolGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FIntRakNetResendRttMultiple': '1', 'FIntDefaultJitterN': '0', 'FIntBatchThumbnailResultsSizeCap': '200', 'FBoolUseVisBugChecks': 'False', 'FBoolAcceleratorUpdateOnPropsAndValueTimeChange': 'True', 'FIntClusterEstimatedCompressionRatioHundredths': '0', 'FIntDebugFRMQualityLevelOverride': '1', 'FIntLargePacketQueueSizeCutoffMB': '1000', 'FIntJoinDataCompressionLevel': '0', 'FIntCLI20390_2': '0', 'FIntDebugTextureManagerSkipMips': '3', 'FBoolTM2SkipMipsForUnstreamable2': 'True', 'FBoolDebugMechanismInterpolationWorldSpace': 'True', 'FBoolSimLocalBallSocketInterpolation': 'True', 'FIntCheckPVDifferencesForInterpolationMinRotVelThresholdRadsPerSecHundredth': '0', 'FIntCheckPVDifferencesForInterpolationMinVelThresholdStudsPerSecHundredth': '0', 'FIntGameplayNetInterpolationDistanceCorrectionSampleMillionth': '1000000', 'FIntInterpolationFramePositionThresholdMillionth': '1', 'FIntInterpolationFrameRotVelocityThresholdMillionth': '1', 'FIntInterpolationFrameVelocityThresholdMillionth': '1', 'FIntInterpolationMinAssemblyCount': '1', 'FIntInterpolationNumMechanismsBatchSize': '4', 'FIntInterpolationNumMechanismsPerTask': '4', 'FIntInterpolationNumParallelTasks': '350', 'FIntMaxInterpolationRecursionsBeforeCheck': '50', 'FIntNumFramesToKeepAfterInterpolation': '2', 'FBoolInterpolationAwareTargetTime': 'False', 'FIntMaxAverageFrameDelayExceedFactor': '0'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "Wizerflag",
    'desc': "193 flags",
    'flags': {'FLogNetwork': '7', 'FFlagFixGraphicsQuality': 'True', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'FIntFRMMaxGrassDistance': '0', 'FFlagEnableMenuControlsABTest': 'False', 'DFFlagDisableDPIScale': 'True', 'FFlagEnableInGameMenuModernization': 'False', 'DFIntTaskSchedulerTargetFps': '69420', 'FFlagEnableInGameMenuControls': 'False', 'FFlagEnableV3MenuABTest3': 'True', 'DFIntCanHideGuiGroupId': '32380007', 'FFlagDisableNewIGMinDUA': 'True', 'DFStringCrashUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagEnableMenuModernizationABTest': 'False', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDebugGraphicsPreferOpenGL': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '1', 'DFIntReportOutputDeviceInfoRateHundredthsPercentage': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagEnableLightstepReporting2': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagEnableFmodErrorsTelemetry': 'False', 'FStringPerformanceSendMeasurementAPISubdomain': 'opt-out', 'FFlagCommitToGraphicsQualityFix': 'True', 'DFIntRakNetMtuValue2InBytes': '1240', 'FFlagRenderGpuTextureCompressor': 'True', 'FIntUITextureMaxRenderTextureSize': '1024', 'FIntDebugForceMSAASamples': '1', 'FFlagDisablePostFx': 'True', 'FStringInGameMenuChromeForcedUserIds': '1353919681', 'DFStringRobloxAnalyticsURL': 'http://opt-out.roblox.com', 'DFIntRakNetNakResendDelayMs': '10', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagEnableInGameMenuV3': 'True', 'DFIntConnectionMTUSize': '900', 'FStringNote': 'CHANGE TO false IF YOU DONT WANNA HAVE GRAY SKYBOX', 'FIntRenderShadowIntensity': '0', 'FIntRakNetResendBufferArrayLength': '1024', 'DFIntCodecMaxOutgoingFrames': '10000', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FIntTerrainArraySliceSize': '8', 'DFIntRakNetResendRttMultiple': '1', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FFlagOptimizeNetworkRouting': 'True', 'FFlagOptimizeNetwork': 'True', 'DFStringAltHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'FFlagDontCreatePingJob': 'True', 'DFFlagQueueDataPingFromSendData': 'True', 'FFlagAdServiceEnabled': 'False', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFFlagEnableGCapsHardwareTelemetry': 'False', 'DFIntRakNetMtuValue3InBytes': '1200', 'DFIntOptimizePingThreshold': '50', 'FIntLmsClientRollout2': '0', 'DFStringRobloxAnalyticsSubDomain': 'opt-out', 'FFlagFastGPULightCulling3': 'True', 'FFlagLuaAppSystemBar': 'False', 'DFFlagRakNetUseSlidingWindow4': 'True', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'DFIntTextureQualityOverride': '0', 'DFFlagDebugAnalyticsSendUserId': 'False', 'DFFlagAudioDeviceTelemetry': 'False', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'DFStringHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'FStringPartTexturePackTablePre2022': '{"foil":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[238,238,238,255]},"asphalt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[227,227,228,234]},"basalt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[160,160,158,238]},"brick":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[229,214,205,227]},"cobblestone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,219,219,243]},"concrete":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[225,225,224,255]},"crackedlava":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[76,79,81,156]},"diamondplate":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[210,210,210,255]},"fabric":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[221,221,221,255]},"glacier":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[225,229,229,243]},"glass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[254,254,254,7]},"granite":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[210,206,200,255]},"grass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[196,196,189,241]},"ground":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[165,165,160,240]},"ice":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[235,239,241,248]},"leafygrass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[182,178,175,234]},"limestone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[250,248,243,250]},"marble":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[181,183,193,249]},"metal":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[226,226,226,255]},"mud":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[193,192,193,252]},"pavement":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,218,219,236]},"pebble":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[204,203,201,234]},"plastic":{"ids":["","rbxassetid://13576561565"],"color":[255,255,255,255]},"rock":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[211,211,210,248]},"corrodedmetal":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[206,177,163,180]},"salt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[249,249,249,255]},"sand":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,216,210,240]},"sandstone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[241,234,230,246]},"slate":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[235,234,235,254]},"snow":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[239,240,240,255]},"wood":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[217,209,208,255]},"woodplanks":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[207,208,206,254]}}', 'DFIntUserIdPlayerNameCacheSize': '33554432', 'FFlagInGameMenuV1FullScreenTitleBar': 'False', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'DFIntLightstepHTTPTransportHundredthsPercent2': '0', 'DFIntRakNetMtuValue1InBytes': '1280', 'FFlagOptimizeServerTickRate': 'True', 'DFIntRakNetLoopMs': '1', 'FFlagDebugLightGridShowChunks': 'False', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'FIntRenderGrassHeightScaler': '0', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'FIntRenderGrassDetailStrands': '0', 'FIntFRMMinGrassDistance': '0', 'DFIntGoogleAnalyticsLoadPlayerHundredth': '0', 'FFlagDebugDisplayFPS': 'False', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntNetworkPrediction': '120', 'DFFlagSimReportCPUInfo': 'False', 'FFlagEnableQuickGameLaunch': 'False', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'FFlagTopBarUseNewBadge': 'True', 'FIntBootstrapperTelemetryReportingHundredthsPercentage': '0', 'DFIntDebugFRMQualityLevelOverride': '1', 'FIntRenderShadowmapBias': '0', 'DFStringAnalyticsEventStreamUrlEndpoint': 'opt-out', 'DFIntRakNetNakResendDelayRttPercent': '50', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FIntRakNetDatagramMessageIdArrayLength': '1024', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntRenderLocalLightUpdatesMax': '1', 'FFlagNewLightAttenuation': 'True', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'FIntMeshContentProviderForceCacheSize': '268435456', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntRakNetNakResendDelayMsMax': '100', 'FFlagEnableMenuModernizationABTest2': 'False', 'FFlagGameBasicSettingsFramerateCap5': 'True', 'FFlagReconnectDisabled': 'True', 'FFlagGpuGeometryManager7': 'True', 'DFIntServerTickRate': '60', 'DFFlagBatchAssetApiNoFallbackOnFail': 'False', 'FStringCredit': 'Potato Mode | @KiwisASkid on YT', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'DFIntHardwareTelemetryHundredthsPercent': '0', 'FIntEmotesAnimationsPerPlayerCacheSize': '16777216', 'FIntDefaultMeshCacheSizeMB': '256', 'DFIntReportRecordingDeviceInfoRateHundredthsPercentage': '0', 'FFlagBatchAssetApi': 'True', 'DFStringAltTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FStringTopBarBadgeLearnMoreLink': 'https://youtube.com/@KiwisASkid/', 'FStringErrorUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'FFlagLuaAppExitModalDoNotShow': 'True', 'DFIntNetworkLatencyTolerance': '1', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFStringTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'FFlagLuaAppExitModal2': 'False', 'FFlagAnimationClipMemCacheEnabled': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '1', 'FFlagPreloadTextureItemsOption4': 'True', 'FIntTerrainOTAMaxTextureSize': '1024', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagEnableSoundTelemetry': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '1', 'FStringPartTexturePackTable2022': '{"foil":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"asphalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"basalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"brick":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"cobblestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"concrete":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"crackedlava":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"diamondplate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"fabric":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"glacier":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"glass":{"ids":["rbxassetid://98732842556","rbxassetid://9438453972"],"color":[255, 255, 255, 255]},"granite":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"grass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"ground":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"ice":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"leafygrass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"limestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"marble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"metal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"mud":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"pavement":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"pebble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"plastic":{"ids":["","rbxassetid://0"],"color":[255, 255, 255, 255]},"rock":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"corrodedmetal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"salt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"sand":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"sandstone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"slate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"snow":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"wood":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"woodplanks":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]}}', 'DFFlagEnableHardwareTelemetry': 'False', 'DFIntDebugRestrictGCDistance': '1', 'FFlagEnableInGameMenuChrome': 'True', 'FFlagEnableInGameMenuChromeABTest3': 'False', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'DFIntMaxFrameBufferSize': '4', 'FFlagDebugRenderingSetDeterministic': 'False', 'FIntRomarkStartWithGraphicQualityLevel': '1', 'FIntRuntimeMaxNumOfThreads': '2400', 'FIntTaskSchedulerThreadMin': '3', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'FFlagRenderPerformanceTelemetry': 'False', 'FIntRenderLocalLightFadeInMs_enabled': '99999', 'FFlagEnableAudioOutputDevice': 'false', 'FFlagEnableReportAbuseMenuRoact2': 'false', 'FIntReportDeviceInfoRollout': '0', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagDebugDisableOTAMaterialTexture': 'true', 'FFlagEnableReportAbuseMenuRoactABTest2': 'False', 'DFIntAnimationLodFacsDistanceMax': '0', 'FFlagEnableBubbleChatFromChatService': 'False', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'DFFlagESGamePerfMonitorEnabled': 'False', 'FIntStartupInfluxHundredthsPercentage': '0', 'FFlagEnableBetaBadgeLearnMore': 'false', 'FFlagEnableInGameMenuChromeABTest2': 'False', 'FFlagVoiceBetaBadge': 'false', 'FFlagEnableBubbleChatConfigurationV2': 'False', 'FFlagMSRefactor5': 'False', 'DFFlagDebugPerfMode': 'True', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FFlagGlobalWindRendering': 'false', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FFlagCloudsReflectOnWater': 'False', 'FFlagRenderCheckThreading': 'True', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FIntRobloxGuiBlurIntensity': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagNullCheckCloudsRendering': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagGameBasicSettingsFramerateCap': 'True', 'FIntCameraMaxZoomDistance': '99999', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'DFIntAnimationLodFacsDistanceMin': '0', 'FStringTerrainMaterialTablePre2022': '', 'FStringTerrainMaterialTable2022': ''},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "acquaflag1",
    'desc': "172 flags",
    'flags': {'FLogNetwork': '7', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntTextureQualityOverride': '0', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDisablePostFx': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntTerrainArraySliceSize': '8', 'FIntDebugForceMSAASamples': '0', 'DFFlagDisableDPIScale': 'True', 'DFIntTaskSchedulerTargetFps': '9999', 'FIntRenderShadowIntensity': '0', 'DFIntCanHideGuiGroupId': '32380007', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'FFlagPreloadMinimalFonts': 'True', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FStringTerrainMaterialTable2022': '', 'FFlagEnableBetaBadgeLearnMore': 'false', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FFlagEnableMenuModernizationABTest': 'False', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'FFlagRenderCheckThreading': 'True', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'FFlagRenderPerformanceTelemetry': 'False', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'FFlagEnableBubbleChatConfigurationV2': 'False', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagEnableAudioOutputDevice': 'false', 'FFlagEnableQuickGameLaunch': 'False', 'DFFlagESGamePerfMonitorEnabled': 'False', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'FIntDefaultMeshCacheSizeMB': '256', 'FFlagEnableReportAbuseMenuRoact2': 'false', 'FFlagEnableMenuModernizationABTest2': 'False', 'FFlagCloudsReflectOnWater': 'False', 'FFlagEnableBubbleChatFromChatService': 'False', 'FIntDebugTextureManagerSkipMips': '100000000', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagAdServiceEnabled': 'False', 'DFStringHttpPointsReporterUrl': 'null', 'DFStringLightstepHTTPTransportUrlPath': 'null', 'DFStringRobloxAnalyticsURL': 'null', 'DFStringTelegrafHTTPTransportUrl': 'null', 'DFStringTelemetryV2Url': 'null', 'FFlagEnableInGameMenuChromeABTest2': 'False', 'FStringGamesUrlPath': '/games/', 'DFIntLightstepHTTPTransportHundredthsPercent2': '0', 'FFlagPreloadAllFonts': 'True', 'FStringCoreScriptBacktraceErrorUploadToken': 'null', 'DFFlagEnableLightstepReporting2': 'False', 'DFIntS2PhysicsSenderRate': '100', 'DFStringAltTelegrafHTTPTransportUrl': 'null', 'DFStringAltHttpPointsReporterUrl': 'null', 'FFlagFixGraphicsQuality': 'True', 'DFStringAnalyticsEventStreamUrlEndpoint': 'null', 'DFStringCrashUploadToBacktraceMacPlayerToken': 'null', 'DFStringCrashUploadToBacktraceBaseUrl': 'null', 'DFStringLightstepHTTPTransportUrlHost': 'null', 'DFStringLightstepToken': 'null', 'FFlagEnableReportAbuseMenuRoactABTest2': 'False', 'FIntRobloxGuiBlurIntensity': '0', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FIntFRMMinGrassDistance': '0', 'FIntFRMMaxGrassDistance': '0', 'FFlagUISUseLastFrameTimeInUpdateInputSignal': 'True', 'FFlagSimAdaptiveMinorOptimizations': 'True', 'FFlagPushFrameTimeToHarmony': 'True', 'FFlagOptimizeServerTickRate': 'True', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagOptimizeNetwork': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagMSRefactor5': 'False', 'FFlagGameBasicSettingsFramerateCap2': 'True', 'DFIntVisibilityCheckRayCastLimitPerFrame': '10', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntRakNetResendRttMultiple': '1', 'DFIntRakNetLoopMs': '1', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntPhysicsReceiveNumParallelTasks': '12', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntNetworkSchemaCompressionRatio': '100', 'DFIntNetworkLatencyTolerance': '1', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntMaxFrameBufferSize': '4', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntConnectionMTUSize': '900', 'DFIntBufferCompressionLevel': '0', 'DFIntAnimatorThrottleMaxFramesToSkip': '1', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagDebugDisableTelemetryPoint': 'True', 'DFIntCodecMaxOutgoingFrames': '10000', 'FFlagFastGPULightCulling3': 'True', 'DFIntTextureCompositorActiveJobs': '0', 'FFlagEnableAccessibilitySettingsAPIV2': 'True', 'FIntRenderGrassHeightScaler': '0', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFStringCrashUploadToBacktraceWindowsPlayerToken': 'null', 'DFIntOptimizePingThreshold': '50', 'DFIntAnimationLodFacsDistanceMin': '0', 'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'True', 'FFlagNullCheckCloudsRendering': 'True', 'FIntSimWorldTaskQueueParallelTasks': '12', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'FIntRakNetResendBufferArrayLength': '128', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFFlagEnableDynamicHeadByDefault': 'False', 'FIntCameraMaxZoomDistance': '99999', 'DFIntNetworkPrediction': '120', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFFlagDebugPauseVoxelizer': 'True', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2': 'True', 'DFIntServerTickRate': '60', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntAnimationLodFacsDistanceMax': '0', 'FIntRenderGrassDetailStrands': '0', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'FFlagDebugGraphicsPreferVulkan': 'True', 'DFIntDebugFRMQualityLevelOverride': '1', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '12', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '12', 'FFlagEnableAccessibilitySettingsInExperienceMenu2': 'True', 'FFlagDebugSkyGray': 'False', 'FFlagOptimizeNetworkRouting': 'True', 'DFIntBufferCompressionThreshold': '100', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagChatTranslationSettingEnabled3': 'False', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntReplicationDataCacheNumParallelTasks': '12', 'DFIntMegaReplicatorNumParallelTasks': '12', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'FFlagEnableInGameMenuControls': 'False', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FIntReportDeviceInfoRollout': '0', 'FIntRenderLocalLightFadeInMs_enabled': '99999', 'FFlagVoiceBetaBadge': 'false', 'FIntRenderLocalLightUpdatesMax': '1', 'FFlagDontCreatePingJob': 'True', 'FFlagTopBarUseNewBadge': 'false', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FIntStartupInfluxHundredthsPercentage': '0', 'FFlagEnableV3MenuABTest3': 'False', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagEnableInGameMenuModernization': 'False', 'FFlagCommitToGraphicsQualityFix': 'True', 'FStringTerrainMaterialTablePre2022': '', 'DFFlagDebugPerfMode': 'True', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FFlagGlobalWindRendering': 'false', 'FFlagEnableMenuControlsABTest': 'False', 'FIntRenderShadowmapBias': '0'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "acquaflag3",
    'desc': "73 flags",
    'flags': {'FLogNetwork': '1', 'FIntRenderShadowIntensity': '0', 'FFlagDisablePostFx': 'True', 'FIntTerrainArraySliceSize': '0', 'DFIntTaskSchedulerTargetFps': '300', 'DFIntTextureQualityOverride': '0', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'DFIntCanHideGuiGroupId': '32380007', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FIntDebugForceMSAASamples': '1', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFFlagDisableDPIScale': 'True', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagCommitToGraphicsQualityFix': 'True', 'FFlagEnableInGameMenuModernization': 'True', 'FIntCameraMaxZoomDistance': '1000', 'FFlagDebugGraphicsPreferD3D11FL10': 'False', 'FFlagEnableInGameMenuChrome': 'False', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'FFlagPreloadAllFonts': 'True', 'DFIntPerformanceControlTextureQualityBestUtility': '-2', 'FFlagDebugDisableTelemetryPoint': 'True', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FFlagGlobalWindRendering': 'false', 'FIntRenderLocalLightUpdatesMax': '1', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'SFFlagFacialAnimation1BetaFeatureRoleSet': 'False', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagFacialAnimationRecordingBetaFeature': 'False', 'FIntTerrainOTAMaxTextureSize': '10', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagFacialAnimationStreamingIfNoDynamicHeadDisableA2C': 'False', 'FFlagFacialAnimationStreamingServiceUserSettingsCache': 'False', 'FFlagDisableNewIGMinDUA': 'True', 'FFlagFacialAnimationStreamingServiceUseServerThrottling': 'False', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'SFFlagFacialAnimation1BetaFeatureRolloutPercent': 'False', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagNewLightAttenuation': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'FIntFontSizePadding': '1', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'DFIntMaxFrameBufferSize': '6', 'FFlagUserCameraShake': 'False', 'FFlagDisableCameraShake': 'True', 'DFIntCameraShakeSpeed': '0', 'FFlagUserDisableDeltaTimeShaking': 'True', 'FFlagUserDisableExplosionShake': 'True', 'FFlagUserDisableDynamicCameraShaking': 'True', 'FFlagUserDisableDamageShake': 'True', 'FFlagUserDisableCameraFrameTimeVariation': 'True', 'FFlagUserDisableTimeBasedEffects': 'True', 'FFlagUserDisableDynamicHeadBob': 'True', 'FFlagUserDisableCameraBob': 'True', 'FFlagUserDisableLandingShake': 'True', 'FFlagUserDisableCameraTilt': 'True', 'FFlagUserDisableAllCameraEffects': 'True', 'FFlagUserDisableWeaponRecoilEffect': 'True', 'FFlagUserDisableMotionBlur': 'True', 'FFlagUserDisableHeadBob': 'True', 'FFlagUserLimitCameraFrameRate': 'True', 'FFlagUserForceStableCameraUpdate': 'True', 'FFlagSmoothCameraMotion': 'True', 'FFlagUserEnableRecoilShake': 'False', 'FFlagUserEnableJumpShake': 'False', 'FFlagUserEnableExplosionShake': 'False', 'FFlagUserEnableDamageShake': 'False', 'FFlagUserEnableVehicleShake': 'False', 'FFlagUserEnableScriptedShake': 'False', 'FFlagUserEnablePhysicsShake': 'False'},
    'tag': "USR",
})

BUILTIN_PRESETS.append({
    'name': "message (1)",
    'desc': "96 flags",
    'flags': {'DebugGraphicPreferD3D11': 'True', 'DebugGraphicsDisableOpenGL': 'True', 'DebugGraphicsDisableVulkan': 'True', 'DebugGraphicsDisableVulkan11': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagEnableDynamicHeadByDefault': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntAnimatorThrottleMaxFramesToSkip': '1', 'DFIntBufferCompressionLevel': '0', 'DFIntBufferCompressionThreshold': '100', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntConnectionMTUSize': '900', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '2', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '3', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntMaxFrameBufferSize': '4', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntMegaReplicatorNumParallelTasks': '12', 'DFIntMinimalNetworkPrediction': '0.1', 'DFIntNetworkLatencyTolerance': '1', 'DFIntNetworkPrediction': '120', 'DFIntNetworkSchemaCompressionRatio': '100', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntOptimizePingThreshold': '50', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '12', 'DFIntPhysicsReceiveNumParallelTasks': '12', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntRakNetLoopMs': '1', 'DFIntRakNetResendRttMultiple': '1', 'DFIntReplicationDataCacheNumParallelTasks': '12', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntServerTickRate': '60', 'DFIntTextureCompositorActiveJobs': '0', 'DFIntTextureQualityOverride': '0', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'DFIntVisibilityCheckRayCastLimitPerFrame': '10', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FFlagChatTranslationSettingEnabled3': 'False', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDebugDisableTelemetryV2Event': 'True', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FFlagDebugSkyGray': 'False', 'FFlagDisablePostFx': 'True', 'FFlagEnableAccessibilitySettingsAPIV2': 'True', 'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2': 'True', 'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'True', 'FFlagEnableAccessibilitySettingsInExperienceMenu2': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagGameBasicSettingsFramerateCap2': 'True', 'FFlagMSRefactor5': 'False', 'FFlagNewLightAttenuation': 'True', 'FFlagOptimizeNetwork': 'True', 'FFlagOptimizeNetworkRouting': 'True', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagOptimizeServerTickRate': 'True', 'FFlagPushFrameTimeToHarmony': 'True', 'FFlagSimAdaptiveMinorOptimizations': 'True', 'FFlagUISUseLastFrameTimeInUpdateInputSignal': 'True', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FIntRakNetResendBufferArrayLength': '128', 'FIntRenderGrassDetailStrands': '0', 'FIntRenderGrassHeightScaler': '0', 'FIntRobloxGuiBlurIntensity': '0', 'FIntSimWorldTaskQueueParallelTasks': '12', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '12', 'FIntTerrainArraySliceSize': '8', 'RakNetClockDriftAdjustmentPerPingMillisecond': '100'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "message (11)",
    'desc': "108 flags",
    'flags': {'FIntDebugTextureManagerSkipMips': '8', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'FFlagTelemetryCacheCleanupSlowStats3': 'False', 'DFFlagDebugDisableTelemetryAfterTest': 'True', 'FFlagSkipAttributeCopyIfNoTelemetry': 'True', 'DFFlagEnableTelemetryV2FRMStats': 'False', 'DFFlagHttpCacheTrackAllAssets2': 'False', 'DFFlagDisableFastLogTelemetry': 'True', 'DFFlagEXPCHAT1499Telemetry': 'False', 'DFFlagEXPR2140Telemetry': 'False', 'FFlagAdServiceEnabled': 'False', 'FFlagLuaAppHomeVngAppUpsell': 'False', 'FStringVNGWebshopUrl': 'null', 'FStringGameLaunchLinkURL': '(?:(?:https?://\\w+\\.roblox(?:labs)?\\.com(?:/[A-Za-z]{2}(-[A-Za-z0-9]{2,3})?)?/games/start\\?)|(?:roblox(?:mobile)?://(?:experiences/start\\?)?))(?:(?:(?:(?:id=\\d+)|(?:placeid=\\d+)|(?:accessCode=(?:\\w|\\-)+)|(?:reservedServerAccessCode=(?:\\w|\\-)+)|(?:launchData=(?:.+))|(?:eventId=(?:\\d+)/?', 'DFStringTelemetryV2Url': 'https://opt-out.roblox.com/', 'DFStringRobloxAnalyticsURL': 'https://opt-out.roblox.com/', 'DFStringHttpPointsReporterUrl': 'https://opt-out.roblox.com/', 'DFStringCrashUploadToBacktraceBaseUrl': 'https://opt-out.roblox.com/', 'FStringTencentAuthPath': 'Unterial', 'FLogTencentAuthPath': 'Unterial', 'DFIntRobloxTelemetryBatchedReporterTimerIntervalMs': '2147483647', 'DFIntRobloxTelemetryTryCutAndSendSignalTimerIntervalMs': '2147483647', 'DFIntRbxStorageTelemetryIntervalMS': '2147483647', 'FIntProfileTelemetryTickRateMs': '2147483647', 'DFStringRobloxTelemetryReliabilityCountAllowList': 'null', 'FStringCategorizedL2SessionNamesForTelemetryCounter': 'null', 'FFlagEnableTelemetryProtocol': 'False', 'FFlagEnableTelemetryService1': 'False', 'FFlagEnableServiceInitBreakdownTelemetry': 'False', 'FFlagOpenTelemetryEnabled2': 'False', 'FLogRealtimeProtocol': 'Error,0', 'DFIntDataModelAnalysisServiceTelemetryThrottle': '0', 'DFIntRobloxTelemetryRealtimeEventsThrottleHundredthsPercent': '0', 'DFFlagReportReplicatorStatsToTelemetryV22': 'False', 'FFlagRealtimeReliabilityMeasurementEnable': 'False', 'DFFlagEnableRLReceiveFailureTracking': 'False', 'DFFlagCorrectServerReplicatorStatsIP': 'False', 'DFFlagXhrTrackSeq': 'False', 'DFFlagHttpTrackBandwidthBasedOnMsgSize': 'False', 'DFFlagRakNetTelemV2DownloadBwTracker': 'False', 'DFFlagHttpTelemV2DownloadBwTracker': 'False', 'DFLogClientRecvFromRaknet': 'Error,0', 'DFLogLargeReplicatorTrace': 'Error,0', 'FFlagSimDcdRefactorDelta3': 'True', 'FFlagSimDcdDeltaReplication': 'True', 'DFFlagReplicateCreateToPlayer': 'True', 'DFFlagSolverStateReplicatedOnly2': 'True', 'DFFlagReplicatorSeparateVarThresholds': 'True', 'DFFlagUpdateBoundExtentsForHugeMixedReplicationComponents': 'True', 'FFlagSpecifyNetworkReplicatorScopeForItems': 'True', 'FFlagSpecifyNetworkReplicatorScope': 'True', 'DFIntServerBandwidthPlayerSampleRateFacsOverride': '2147465500', 'DFIntServerRakNetBandwidthPlayerSampleRate': '2147465500', 'DFIntReportNetworkSyncMemoryUsage2EveryXSeconds': '86400', 'DFIntNetworkObjectStatsCollectorGlobalCapThrottleHP': '0', 'DFIntServerBandwidthPlayerSampleRate': '2147465500', 'DFIntMaxDebugNetworkUpdateTimestamps': '0', 'DFIntSendRakNetStatsInterval': '86400', 'DFIntBandwidthManagerDataSenderMaxWorkCatchupMs': '1850', 'DFIntMaxProcessPacketsStepsPerCyclic': '100', 'DFIntMaxProcessPacketsJobScaling': '250', 'DFIntSignalRCoreRpcQueueSize': '256', 'DFIntSignalRCoreTimerMs': '750', 'FStringPhysicsAdaptiveTimeSteppingIXP': 'Physics.DefaultTimeStepping', 'DFFlagSimAdaptiveAdjustTimestepForControllerManager': 'False', 'FFlagEnablePhysicsAdaptiveTimeSteppingIXP': 'True', 'DFIntTimestepArbiterCollidingHumanoidTsm': '100', 'DFIntSimDefaultHumanoidTimestepMultiplier': '100', 'DFIntSimExplicitlyCappedTimestepMultiplier': '500', 'FIntMaxTimestepMultiplierVelocity': '100', 'FIntMaxTimestepMultiplierHumanoid': '100', 'FIntMaxTimestepMultiplierAcceleration': '100', 'DFIntTimestepArbiterHumanoidLinearVelThreshold': '10', 'DFIntTimestepArbiterHumanoidTurningVelThreshold': '6', 'DFIntGraphicsOptimizationModeMinFrameTimeTargetMs': '10', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFIntMaxFrameBufferSize': '4', 'FIntDefaultJitterN': '0', 'DFIntAnimatorRetargetInterpolateFKCorrectionMinAngleDeg': '0', 'DFIntAnimatorRetargetInterpolateFKCorrectionMaxAngleDeg': '360', 'DFIntAngularVelociryLimit': '360', 'DFFlagSimActivateLinearVelocityReactionForceEnabled': 'False', 'DFFlagSimAdaptiveExplicitlyMarkInterpolatedAssemblies': 'True', 'DFFlagDebugDisableAngularVelocityInterpolationComponent': 'True', 'FIntLinearDeformerSmoothScalePct': '10', 'FIntLinearDeformerTriWeightMode': '0', 'DFFlagAcceleratorUpdateOnPropsAndValueTimeChange': 'True', 'FFlagPreComputeAcceleratorArrayForSharingTimeCurve': 'True', 'FFlagKeyframeSequenceUseRuntimeSyncPrims': 'True', 'FFlagHumanoidStateUseRuntimeSyncPrims': 'True', 'DFFlagMergeFakeInputEvents4': 'True', 'FFlagUserCameraControlLastInputTypeUpdate': 'False', 'FFlagMovePrerenderV2': 'False', 'DFIntLatencyLoggingThresholdMs': '86400000', 'DFFlagSimSmoothedRunningController2': 'True', 'DFFlagHumanoidReplicateSimulated2': 'True', 'FFlagLuaMenuPerfImprovements': 'True', 'FIntInterpolationMaxDelayMSec': '100', 'DFIntS2PhysicsSenderRate': '240', 'FIntCLI20390_2': '1', 'FFlagFasterPreciseTime4': 'True', 'DFIntTaskSchedulerTargetFps': '3000', 'FFlagDebugDisplayFPS': 'False', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FIntTaskSchedulerAutoThreadLimit': '15', 'DFIntRuntimeConcurrency': '15', 'DFIntGraphicsOptimizationModeFRMFrameRateTarget': '240', 'DFIntDebugDynamicRenderKiloPixels': '-1'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "message (2) (1)",
    'desc': "166 flags",
    'flags': {'FLogNetwork': '7', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntTextureQualityOverride': '3', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FIntDebugForceMSAASamples': '1', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDisablePostFx': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'DFIntTaskSchedulerTargetFps': '99999', 'DFFlagDisableDPIScale': 'True', 'FIntRenderShadowIntensity': '0', 'FIntTerrainArraySliceSize': '0', 'DFIntCanHideGuiGroupId': '32380007', 'DFFlagDebugEnableInterpolationVisualizer': 'true', 'FFlagDebugDisplayFPS': 'True', 'FFlagNewNetworking': 'False', 'FFlagUseUnifiedRenderStepped': 'False', 'FFlagFixMeshPartScaling': 'False', 'FFlagEnableTerrainOptimizations': 'True', 'DFStringTelegrafHTTPTransportUrl': 'null', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFStringCrashUploadToBacktraceWindowsPlayerToken': 'null', 'FFlagEnableNewHeapSnapshots': 'False', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagFastGPULightCulling3': 'True', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntRakNetMtuValue1InBytes': '1280', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntRenderingThrottleDelayInMS': '1', 'DFStringCrashUploadToBacktraceMacPlayerToken': 'null', 'FFlagUseDeferredContext': 'False', 'FFlagDebugDisableTelemetryPoint': 'True', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFStringAnalyticsEventStreamUrlEndpoint': 'null', 'FFlagGameBasicSettingsFramerateCap5': 'False', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'FFlagEnableInGameMenuChromeABTest2': 'False', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFStringTelemetryV2Url': 'null', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'FStringGamesUrlPath': '/games/', 'FFlagOptimizeEmotes': 'False', 'FFlagPreloadAllFonts': 'True', 'FFlagEnableTerrainFoliageOptimizations': 'True', 'DFFlagDebugSkipMeshVoxelizer': 'True', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'DFFlagBaseNetworkMetrics': 'False', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntRunningBaseOrientationP': '115', 'DFFlagDebugPerfMode': 'False', 'DFFlagDebugPauseVoxelizer': 'True', 'FFlagEnableHumanoidLuaSideCaching': 'False', 'DFStringLightstepHTTPTransportUrlHost': 'null', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFIntNewRunningBaseAltitudeD': '45', 'DFFlagDisableFastLogTelemetry': 'True', 'FFlagLuaAppSystemBar': 'False', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'FFlagDebugCrashReports': 'False', 'FFlagFixScalingModelRendering': 'False', 'DFFlagEnableLightstepReporting2': 'False', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntCodecMaxIncomingPackets': '100', 'FFlagTweenOptimizations': 'True', 'FFlagFixGraphicsQuality': 'True', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FStringCoreScriptBacktraceErrorUploadToken': 'null', 'FFlagUseNewAnimationSystem': 'False', 'FFlagUseParticlesV2': 'False', 'FFlagAdServiceEnabled': 'False', 'DFStringAltTelegrafHTTPTransportUrl': 'null', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagRenderFixFog': 'True', 'DFStringCrashUploadToBacktraceBaseUrl': 'null', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFFlagBrowserTrackerIdTelemetryEnabled': 'False', 'FFlagEnableReportAbuseMenuRoactABTest2': 'False', 'FFlagCommitToGraphicsQualityFix': 'True', 'DFStringHttpPointsReporterUrl': 'null', 'FStringFFlagVersion': 'RCO v1.00 | High Graphics', 'DFIntLightstepHTTPTransportHundredthsPercent2': '0', 'FFlagSimIslandizerManager': 'false', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFStringAltHttpPointsReporterUrl': 'null', 'DFIntS2PhysicsSenderRate': '100', 'DFStringLightstepHTTPTransportUrlPath': 'null', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFStringRobloxAnalyticsURL': 'null', 'FFlagAnimatePhysics': 'False', 'FFlagUseDynamicSun': 'False', 'FFlagNewLightAttenuation': 'True', 'DFIntRakNetMtuValue3InBytes': '1200', 'DFIntRakNetMtuValue2InBytes': '1240', 'DFIntRakNetLoopMs': '1', 'DFStringLightstepToken': 'null', 'FFlagEnableNewInput': 'True', 'FFlagEnableLightAttachToPart': 'False', 'FFlagEnableMenuModernizationABTest': 'False', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'FFlagGlobalWindRendering': 'false', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'FFlagVoiceBetaBadge': 'false', 'FIntUITextureMaxRenderTextureSize': '1024', 'FFlagEnableMenuControlsABTest': 'False', 'FFlagEnableBubbleChatFromChatService': 'False', 'FFlagDebugSkyGray': 'false', 'FIntStartupInfluxHundredthsPercentage': '0', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagEnableMenuModernizationABTest2': 'False', 'FIntRenderLocalLightFadeInMs_enabled': '99999', 'FFlagMSRefactor5': 'False', 'FFlagRenderCheckThreading': 'True', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FIntDefaultMeshCacheSizeMB': '256', 'FFlagRenderPerformanceTelemetry': 'False', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'FFlagEnableAudioOutputDevice': 'false', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FIntRenderGrassDetailStrands': '0', 'FFlagPreloadTextureItemsOption4': 'True', 'DFFlagESGamePerfMonitorEnabled': 'False', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FFlagTopBarUseNewBadge': 'false', 'FFlagRenderGpuTextureCompressor': 'True', 'FIntFRMMinGrassDistance': '0', 'FFlagDebugDisableOTAMaterialTexture': 'true', 'FStringTerrainMaterialTable2022': '', 'FFlagEnableBubbleChatConfigurationV2': 'False', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FIntRenderShadowmapBias': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'FFlagEnableQuickGameLaunch': 'False', 'FStringTerrainMaterialTablePre2022': '', 'FFlagCloudsReflectOnWater': 'False', 'FStringPartTexturePackTable2022': '{"foil":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[238,238,238,255]},"asphalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[227,227,228,234]},"basalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[160,160,158,238]},"brick":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[229,214,205,227]},"cobblestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[218,219,219,243]},"concrete":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[225,225,224,255]},"crackedlava":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[76,79,81,156]},"diamondplate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[210,210,210,255]},"fabric":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[221,221,221,255]},"glacier":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[225,229,229,243]},"glass":{"ids":["rbxassetid://9873284556","rbxassetid://9438453972"],"color":[254,254,254,7]},"granite":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[210,206,200,255]},"grass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[196,196,189,241]},"ground":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[165,165,160,240]},"ice":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[235,239,241,248]},"leafygrass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[182,178,175,234]},"limestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[250,248,243,250]},"marble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[181,183,193,249]},"metal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[226,226,226,255]},"mud":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[193,192,193,252]},"pavement":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[218,218,219,236]},"pebble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[204,203,201,234]},"plastic":{"ids":["","rbxassetid://0"],"color":[255,255,255,255]},"rock":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[211,211,210,248]},"corrodedmetal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[206,177,163,180]},"salt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[249,249,249,255]},"sand":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[218,216,210,240]},"sandstone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[241,234,230,246]},"slate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[235,234,235,254]},"snow":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[239,240,240,255]},"wood":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[217,209,208,255]},"woodplanks":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[207,208,206,254]}}', 'FIntRobloxGuiBlurIntensity': '0', 'FIntFRMMaxGrassDistance': '0', 'FFlagPreloadMinimalFonts': 'True', 'FFlagEnableInGameMenuControls': 'False', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FIntTerrainOTAMaxTextureSize': '1024', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FFlagEnableBetaBadgeLearnMore': 'false', 'FFlagDontCreatePingJob': 'True', 'FStringPartTexturePackTablePre2022': '{"foil":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255,255,255,255]},"brick":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[204,201,200,232]},"cobblestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[212,200,187,250]},"concrete":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[208,208,208,255]},"diamondplate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[170,170,170,255]},"fabric":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[105,104,102,244]},"glass":{"ids":["rbxassetid://7547304948","rbxassetid://7546645118"],"color":[254,254,254,7]},"granite":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[113,113,113,255]},"grass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[165,165,159,255]},"ice":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255,255,255,255]},"marble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[199,199,199,255]},"metal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[199,199,199,255]},"pebble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[208,208,208,255]},"corrodedmetal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[159,119,95,200]},"sand":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[220,220,220,255]},"slate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[193,193,193,255]},"wood":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[227,227,227,255]},"woodplanks":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[212,209,203,255]},"asphalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[123,123,123,234]},"basalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[154,154,153,238]},"crackedlava":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[74,78,80,156]},"glacier":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[226,229,229,243]},"ground":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[114,114,112,240]},"leafygrass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[121,117,113,234]},"limestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[235,234,230,250]},"mud":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[130,130,130,252]},"pavement":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[142,142,144,236]},"rock":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[154,154,154,248]},"salt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[220,220,221,255]},"sandstone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[174,171,169,246]},"snow":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[218,218,218,255]}}', 'FIntReportDeviceInfoRollout': '0', 'FFlagEnableInGameMenuModernization': 'False', 'FFlagEnableReportAbuseMenuRoact2': 'false', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FFlagEnableV3MenuABTest3': 'False', 'FIntCameraMaxZoomDistance': '99999', 'FFlagNullCheckCloudsRendering': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'DFIntAnimationLodFacsDistanceMax': '0', 'FIntRenderLocalLightUpdatesMax': '1', 'FIntRenderLocalLightUpdatesMin': '1', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntTextureCompositorActiveJobs': '0'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "message (2)",
    'desc': "96 flags",
    'flags': {'DebugGraphicPreferD3D11': 'True', 'DebugGraphicsDisableOpenGL': 'True', 'DebugGraphicsDisableVulkan': 'True', 'DebugGraphicsDisableVulkan11': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagEnableDynamicHeadByDefault': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntAnimationLodFacsDistanceMax': '0', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'DFIntAnimatorThrottleMaxFramesToSkip': '1', 'DFIntBufferCompressionLevel': '0', 'DFIntBufferCompressionThreshold': '100', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntConnectionMTUSize': '900', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '2', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '3', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4', 'DFIntDebugFRMQualityLevelOverride': '1', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFIntMaxFrameBufferSize': '4', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFIntMegaReplicatorNumParallelTasks': '12', 'DFIntMinimalNetworkPrediction': '0.1', 'DFIntNetworkLatencyTolerance': '1', 'DFIntNetworkPrediction': '120', 'DFIntNetworkSchemaCompressionRatio': '100', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntOptimizePingThreshold': '50', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '12', 'DFIntPhysicsReceiveNumParallelTasks': '12', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntRakNetLoopMs': '1', 'DFIntRakNetResendRttMultiple': '1', 'DFIntReplicationDataCacheNumParallelTasks': '12', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntServerTickRate': '60', 'DFIntTextureCompositorActiveJobs': '0', 'DFIntTextureQualityOverride': '0', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'DFIntVisibilityCheckRayCastLimitPerFrame': '10', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FFlagChatTranslationSettingEnabled3': 'False', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDebugDisableTelemetryV2Event': 'True', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FFlagDebugSkyGray': 'False', 'FFlagDisablePostFx': 'True', 'FFlagEnableAccessibilitySettingsAPIV2': 'True', 'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2': 'True', 'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'True', 'FFlagEnableAccessibilitySettingsInExperienceMenu2': 'True', 'FFlagFastGPULightCulling3': 'True', 'FFlagGameBasicSettingsFramerateCap2': 'True', 'FFlagMSRefactor5': 'False', 'FFlagNewLightAttenuation': 'True', 'FFlagOptimizeNetwork': 'True', 'FFlagOptimizeNetworkRouting': 'True', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagOptimizeServerTickRate': 'True', 'FFlagPushFrameTimeToHarmony': 'True', 'FFlagSimAdaptiveMinorOptimizations': 'True', 'FFlagUISUseLastFrameTimeInUpdateInputSignal': 'True', 'FIntFRMMaxGrassDistance': '0', 'FIntFRMMinGrassDistance': '0', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FIntRakNetResendBufferArrayLength': '128', 'FIntRenderGrassDetailStrands': '0', 'FIntRenderGrassHeightScaler': '0', 'FIntRobloxGuiBlurIntensity': '0', 'FIntSimWorldTaskQueueParallelTasks': '12', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '12', 'FIntTerrainArraySliceSize': '8', 'RakNetClockDriftAdjustmentPerPingMillisecond': '100'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "message (3)",
    'desc': "197 flags",
    'flags': {'FLogNetwork': '7', 'FFlagFixGraphicsQuality': 'True', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'FIntFRMMaxGrassDistance': '0', 'FFlagEnableMenuControlsABTest': 'False', 'DFFlagDisableDPIScale': 'True', 'FFlagEnableInGameMenuModernization': 'False', 'DFIntTaskSchedulerTargetFps': '69420', 'FFlagEnableInGameMenuControls': 'False', 'FFlagEnableV3MenuABTest3': 'True', 'DFIntCanHideGuiGroupId': '32380007', 'FFlagDisableNewIGMinDUA': 'True', 'DFStringCrashUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagEnableMenuModernizationABTest': 'False', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDebugGraphicsPreferOpenGL': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '1', 'DFIntReportOutputDeviceInfoRateHundredthsPercentage': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagEnableLightstepReporting2': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagEnableFmodErrorsTelemetry': 'False', 'FStringPerformanceSendMeasurementAPISubdomain': 'opt-out', 'FFlagCommitToGraphicsQualityFix': 'True', 'DFIntRakNetMtuValue2InBytes': '1240', 'FFlagRenderGpuTextureCompressor': 'True', 'FIntUITextureMaxRenderTextureSize': '1024', 'FIntDebugForceMSAASamples': '1', 'FFlagDisablePostFx': 'True', 'FFlagPreloadAllFonts': 'True', 'FStringInGameMenuChromeForcedUserIds': '1353919681', 'DFStringRobloxAnalyticsURL': 'http://opt-out.roblox.com', 'DFIntRakNetNakResendDelayMs': '10', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagEnableInGameMenuV3': 'True', 'DFIntConnectionMTUSize': '900', 'FStringNote': 'CHANGE TO false IF YOU DONT WANNA HAVE GRAY SKYBOX', 'FIntRenderShadowIntensity': '0', 'FIntRakNetResendBufferArrayLength': '1024', 'DFIntCodecMaxOutgoingFrames': '10000', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FIntTerrainArraySliceSize': '8', 'DFIntRakNetResendRttMultiple': '1', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FFlagOptimizeNetworkRouting': 'True', 'FFlagOptimizeNetwork': 'True', 'DFStringAltHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'FFlagDontCreatePingJob': 'True', 'DFFlagQueueDataPingFromSendData': 'True', 'FFlagAdServiceEnabled': 'False', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFFlagEnableGCapsHardwareTelemetry': 'False', 'DFIntRakNetMtuValue3InBytes': '1200', 'DFIntOptimizePingThreshold': '50', 'FIntLmsClientRollout2': '0', 'DFStringRobloxAnalyticsSubDomain': 'opt-out', 'FFlagFastGPULightCulling3': 'True', 'FFlagLuaAppSystemBar': 'False', 'DFFlagRakNetUseSlidingWindow4': 'True', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'DFIntTextureQualityOverride': '0', 'DFFlagDebugAnalyticsSendUserId': 'False', 'DFFlagAudioDeviceTelemetry': 'False', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'DFStringHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'FIntFontSizePadding': '3', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'FStringPartTexturePackTablePre2022': '{"foil":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[238,238,238,255]},"asphalt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[227,227,228,234]},"basalt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[160,160,158,238]},"brick":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[229,214,205,227]},"cobblestone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,219,219,243]},"concrete":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[225,225,224,255]},"crackedlava":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[76,79,81,156]},"diamondplate":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[210,210,210,255]},"fabric":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[221,221,221,255]},"glacier":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[225,229,229,243]},"glass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[254,254,254,7]},"granite":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[210,206,200,255]},"grass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[196,196,189,241]},"ground":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[165,165,160,240]},"ice":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[235,239,241,248]},"leafygrass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[182,178,175,234]},"limestone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[250,248,243,250]},"marble":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[181,183,193,249]},"metal":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[226,226,226,255]},"mud":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[193,192,193,252]},"pavement":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,218,219,236]},"pebble":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[204,203,201,234]},"plastic":{"ids":["","rbxassetid://13576561565"],"color":[255,255,255,255]},"rock":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[211,211,210,248]},"corrodedmetal":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[206,177,163,180]},"salt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[249,249,249,255]},"sand":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,216,210,240]},"sandstone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[241,234,230,246]},"slate":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[235,234,235,254]},"snow":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[239,240,240,255]},"wood":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[217,209,208,255]},"woodplanks":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[207,208,206,254]}}', 'DFIntUserIdPlayerNameCacheSize': '33554432', 'FFlagInGameMenuV1FullScreenTitleBar': 'False', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'DFIntLightstepHTTPTransportHundredthsPercent2': '0', 'DFIntRakNetMtuValue1InBytes': '1280', 'FFlagOptimizeServerTickRate': 'True', 'DFIntRakNetLoopMs': '1', 'FFlagDebugLightGridShowChunks': 'False', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'FIntRenderGrassHeightScaler': '0', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'FIntRenderGrassDetailStrands': '0', 'FIntFRMMinGrassDistance': '0', 'DFIntGoogleAnalyticsLoadPlayerHundredth': '0', 'FFlagDebugDisplayFPS': 'False', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntNetworkPrediction': '120', 'DFFlagSimReportCPUInfo': 'False', 'FFlagEnableQuickGameLaunch': 'False', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'FFlagTopBarUseNewBadge': 'True', 'FIntBootstrapperTelemetryReportingHundredthsPercentage': '0', 'DFIntDebugFRMQualityLevelOverride': '1', 'FIntRenderShadowmapBias': '0', 'DFStringAnalyticsEventStreamUrlEndpoint': 'opt-out', 'DFIntRakNetNakResendDelayRttPercent': '50', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FIntRakNetDatagramMessageIdArrayLength': '1024', 'FIntRenderLocalLightUpdatesMin': '1', 'FFlagDebugSkyGray': 'True', 'FIntRenderLocalLightUpdatesMax': '1', 'FFlagNewLightAttenuation': 'True', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'FIntMeshContentProviderForceCacheSize': '268435456', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntRakNetNakResendDelayMsMax': '100', 'FFlagEnableMenuModernizationABTest2': 'False', 'FFlagGameBasicSettingsFramerateCap5': 'True', 'FFlagReconnectDisabled': 'True', 'FFlagGpuGeometryManager7': 'True', 'DFIntServerTickRate': '60', 'DFFlagBatchAssetApiNoFallbackOnFail': 'False', 'FStringCredit': 'Potato Mode | @KiwisASkid on YT', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'DFIntHardwareTelemetryHundredthsPercent': '0', 'FIntEmotesAnimationsPerPlayerCacheSize': '16777216', 'FIntDefaultMeshCacheSizeMB': '256', 'DFIntReportRecordingDeviceInfoRateHundredthsPercentage': '0', 'FFlagBatchAssetApi': 'True', 'DFStringAltTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FStringTopBarBadgeLearnMoreLink': 'https://youtube.com/@KiwisASkid/', 'FStringErrorUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'FFlagLuaAppExitModalDoNotShow': 'True', 'DFIntNetworkLatencyTolerance': '1', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFStringTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'FFlagLuaAppExitModal2': 'False', 'FFlagAnimationClipMemCacheEnabled': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '1', 'FFlagPreloadTextureItemsOption4': 'True', 'FIntTerrainOTAMaxTextureSize': '1024', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagEnableSoundTelemetry': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '1', 'FStringPartTexturePackTable2022': '{"foil":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"asphalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"basalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"brick":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"cobblestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"concrete":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"crackedlava":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"diamondplate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"fabric":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"glacier":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"glass":{"ids":["rbxassetid://98732842556","rbxassetid://9438453972"],"color":[255, 255, 255, 255]},"granite":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"grass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"ground":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"ice":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"leafygrass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"limestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"marble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"metal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"mud":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"pavement":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"pebble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"plastic":{"ids":["","rbxassetid://0"],"color":[255, 255, 255, 255]},"rock":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"corrodedmetal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"salt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"sand":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"sandstone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"slate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"snow":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"wood":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"woodplanks":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]}}', 'DFFlagEnableHardwareTelemetry': 'False', 'DFIntDebugRestrictGCDistance': '1', 'FFlagEnableInGameMenuChrome': 'True', 'FFlagEnableInGameMenuChromeABTest3': 'False', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'DFIntMaxFrameBufferSize': '4', 'FFlagDebugRenderingSetDeterministic': 'False', 'FIntRomarkStartWithGraphicQualityLevel': '1', 'FIntRuntimeMaxNumOfThreads': '2400', 'FIntTaskSchedulerThreadMin': '3', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'FFlagRenderPerformanceTelemetry': 'False', 'FIntRenderLocalLightFadeInMs_enabled': '99999', 'FFlagEnableAudioOutputDevice': 'false', 'FFlagEnableReportAbuseMenuRoact2': 'false', 'FIntReportDeviceInfoRollout': '0', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagDebugDisableOTAMaterialTexture': 'true', 'FFlagEnableReportAbuseMenuRoactABTest2': 'False', 'DFIntAnimationLodFacsDistanceMax': '0', 'FFlagEnableBubbleChatFromChatService': 'False', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'DFFlagESGamePerfMonitorEnabled': 'False', 'FIntStartupInfluxHundredthsPercentage': '0', 'FFlagEnableBetaBadgeLearnMore': 'false', 'FFlagEnableInGameMenuChromeABTest2': 'False', 'FFlagVoiceBetaBadge': 'false', 'FFlagEnableBubbleChatConfigurationV2': 'False', 'FFlagMSRefactor5': 'False', 'DFFlagDebugPerfMode': 'True', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FFlagGlobalWindRendering': 'false', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FFlagCloudsReflectOnWater': 'False', 'FFlagRenderCheckThreading': 'True', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FIntRobloxGuiBlurIntensity': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagPreloadMinimalFonts': 'True', 'FFlagNullCheckCloudsRendering': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagGameBasicSettingsFramerateCap': 'True', 'FIntCameraMaxZoomDistance': '99999', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'DFIntAnimationLodFacsDistanceMin': '0', 'FStringTerrainMaterialTablePre2022': '', 'FStringTerrainMaterialTable2022': ''},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "message (4)",
    'desc': "197 flags",
    'flags': {'FLogNetwork': '7', 'FFlagFixGraphicsQuality': 'True', 'DFIntHttpCurlConnectionCacheSize': '134217728', 'FIntFRMMaxGrassDistance': '0', 'FFlagEnableMenuControlsABTest': 'False', 'DFFlagDisableDPIScale': 'True', 'FFlagEnableInGameMenuModernization': 'False', 'DFIntTaskSchedulerTargetFps': '69420', 'FFlagEnableInGameMenuControls': 'False', 'FFlagEnableV3MenuABTest3': 'True', 'DFIntCanHideGuiGroupId': '32380007', 'FFlagDisableNewIGMinDUA': 'True', 'DFStringCrashUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagEnableMenuModernizationABTest': 'False', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDebugGraphicsPreferOpenGL': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '1', 'DFIntReportOutputDeviceInfoRateHundredthsPercentage': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'DFFlagDebugPauseVoxelizer': 'True', 'DFFlagEnableLightstepReporting2': 'False', 'DFFlagGpuVsCpuBoundTelemetry': 'False', 'DFFlagEnableFmodErrorsTelemetry': 'False', 'FStringPerformanceSendMeasurementAPISubdomain': 'opt-out', 'FFlagCommitToGraphicsQualityFix': 'True', 'DFIntRakNetMtuValue2InBytes': '1240', 'FFlagRenderGpuTextureCompressor': 'True', 'FIntUITextureMaxRenderTextureSize': '1024', 'FIntDebugForceMSAASamples': '1', 'FFlagDisablePostFx': 'True', 'FFlagPreloadAllFonts': 'True', 'FStringInGameMenuChromeForcedUserIds': '1353919681', 'DFStringRobloxAnalyticsURL': 'http://opt-out.roblox.com', 'DFIntRakNetNakResendDelayMs': '10', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagEnableInGameMenuV3': 'True', 'DFIntConnectionMTUSize': '900', 'FStringNote': 'CHANGE TO false IF YOU DONT WANNA HAVE GRAY SKYBOX', 'FIntRenderShadowIntensity': '0', 'FIntRakNetResendBufferArrayLength': '1024', 'DFIntCodecMaxOutgoingFrames': '10000', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FIntTerrainArraySliceSize': '8', 'DFIntRakNetResendRttMultiple': '1', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FFlagOptimizeNetworkRouting': 'True', 'FFlagOptimizeNetwork': 'True', 'DFStringAltHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'FFlagDontCreatePingJob': 'True', 'DFFlagQueueDataPingFromSendData': 'True', 'FFlagAdServiceEnabled': 'False', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFFlagEnableGCapsHardwareTelemetry': 'False', 'DFIntRakNetMtuValue3InBytes': '1200', 'DFIntOptimizePingThreshold': '50', 'FIntLmsClientRollout2': '0', 'DFStringRobloxAnalyticsSubDomain': 'opt-out', 'FFlagFastGPULightCulling3': 'True', 'FFlagLuaAppSystemBar': 'False', 'DFFlagRakNetUseSlidingWindow4': 'True', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'DFIntTextureQualityOverride': '0', 'DFFlagDebugAnalyticsSendUserId': 'False', 'DFFlagAudioDeviceTelemetry': 'False', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'DFStringHttpPointsReporterUrl': 'http://opt-out.roblox.com', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'FIntFontSizePadding': '3', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'FStringPartTexturePackTablePre2022': '{"foil":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[238,238,238,255]},"asphalt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[227,227,228,234]},"basalt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[160,160,158,238]},"brick":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[229,214,205,227]},"cobblestone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,219,219,243]},"concrete":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[225,225,224,255]},"crackedlava":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[76,79,81,156]},"diamondplate":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[210,210,210,255]},"fabric":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[221,221,221,255]},"glacier":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[225,229,229,243]},"glass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[254,254,254,7]},"granite":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[210,206,200,255]},"grass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[196,196,189,241]},"ground":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[165,165,160,240]},"ice":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[235,239,241,248]},"leafygrass":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[182,178,175,234]},"limestone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[250,248,243,250]},"marble":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[181,183,193,249]},"metal":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[226,226,226,255]},"mud":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[193,192,193,252]},"pavement":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,218,219,236]},"pebble":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[204,203,201,234]},"plastic":{"ids":["","rbxassetid://13576561565"],"color":[255,255,255,255]},"rock":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[211,211,210,248]},"corrodedmetal":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[206,177,163,180]},"salt":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[249,249,249,255]},"sand":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[218,216,210,240]},"sandstone":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[241,234,230,246]},"slate":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[235,234,235,254]},"snow":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[239,240,240,255]},"wood":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[217,209,208,255]},"woodplanks":{"ids":["rbxassetid://13576561565","rbxassetid://13576561565"],"color":[207,208,206,254]}}', 'DFIntUserIdPlayerNameCacheSize': '33554432', 'FFlagInGameMenuV1FullScreenTitleBar': 'False', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'DFIntLightstepHTTPTransportHundredthsPercent2': '0', 'DFIntRakNetMtuValue1InBytes': '1280', 'FFlagOptimizeServerTickRate': 'True', 'DFIntRakNetLoopMs': '1', 'FFlagDebugLightGridShowChunks': 'False', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'FIntRenderGrassHeightScaler': '0', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'FIntRenderGrassDetailStrands': '0', 'FIntFRMMinGrassDistance': '0', 'DFIntGoogleAnalyticsLoadPlayerHundredth': '0', 'FFlagDebugDisplayFPS': 'False', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntNetworkPrediction': '120', 'DFFlagSimReportCPUInfo': 'False', 'FFlagEnableQuickGameLaunch': 'False', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'FFlagTopBarUseNewBadge': 'True', 'FIntBootstrapperTelemetryReportingHundredthsPercentage': '0', 'DFIntDebugFRMQualityLevelOverride': '1', 'FIntRenderShadowmapBias': '0', 'DFStringAnalyticsEventStreamUrlEndpoint': 'opt-out', 'DFIntRakNetNakResendDelayRttPercent': '50', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FIntRakNetDatagramMessageIdArrayLength': '1024', 'FIntRenderLocalLightUpdatesMin': '1', 'FFlagDebugSkyGray': 'True', 'FIntRenderLocalLightUpdatesMax': '1', 'FFlagNewLightAttenuation': 'True', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'FIntMeshContentProviderForceCacheSize': '268435456', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntRakNetNakResendDelayMsMax': '100', 'FFlagEnableMenuModernizationABTest2': 'False', 'FFlagGameBasicSettingsFramerateCap5': 'True', 'FFlagReconnectDisabled': 'True', 'FFlagGpuGeometryManager7': 'True', 'DFIntServerTickRate': '60', 'DFFlagBatchAssetApiNoFallbackOnFail': 'False', 'FStringCredit': 'Potato Mode | @KiwisASkid on YT', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'DFIntHardwareTelemetryHundredthsPercent': '0', 'FIntEmotesAnimationsPerPlayerCacheSize': '16777216', 'FIntDefaultMeshCacheSizeMB': '256', 'DFIntReportRecordingDeviceInfoRateHundredthsPercentage': '0', 'FFlagBatchAssetApi': 'True', 'DFStringAltTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FStringTopBarBadgeLearnMoreLink': 'https://youtube.com/@KiwisASkid/', 'FStringErrorUploadToBacktraceBaseUrl': 'http://opt-out.roblox.com', 'FFlagLuaAppExitModalDoNotShow': 'True', 'DFIntNetworkLatencyTolerance': '1', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFStringTelegrafHTTPTransportUrl': 'http://opt-out.roblox.com', 'FFlagLuaAppExitModal2': 'False', 'FFlagAnimationClipMemCacheEnabled': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '1', 'FFlagPreloadTextureItemsOption4': 'True', 'FIntTerrainOTAMaxTextureSize': '1024', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagEnableSoundTelemetry': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '1', 'FStringPartTexturePackTable2022': '{"foil":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"asphalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"basalt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"brick":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"cobblestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"concrete":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"crackedlava":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"diamondplate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"fabric":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"glacier":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"glass":{"ids":["rbxassetid://98732842556","rbxassetid://9438453972"],"color":[255, 255, 255, 255]},"granite":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"grass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"ground":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"ice":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"leafygrass":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"limestone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"marble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"metal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"mud":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"pavement":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"pebble":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"plastic":{"ids":["","rbxassetid://0"],"color":[255, 255, 255, 255]},"rock":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"corrodedmetal":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"salt":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"sand":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"sandstone":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"slate":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"snow":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"wood":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]},"woodplanks":{"ids":["rbxassetid://0","rbxassetid://0"],"color":[255, 255, 255, 255]}}', 'DFFlagEnableHardwareTelemetry': 'False', 'DFIntDebugRestrictGCDistance': '1', 'FFlagEnableInGameMenuChrome': 'True', 'FFlagEnableInGameMenuChromeABTest3': 'False', 'FFlagDebugGraphicsPreferVulkan': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'DFIntMaxFrameBufferSize': '4', 'FFlagDebugRenderingSetDeterministic': 'False', 'FIntRomarkStartWithGraphicQualityLevel': '1', 'FIntRuntimeMaxNumOfThreads': '2400', 'FIntTaskSchedulerThreadMin': '3', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'FFlagRenderPerformanceTelemetry': 'False', 'FIntRenderLocalLightFadeInMs_enabled': '99999', 'FFlagEnableAudioOutputDevice': 'false', 'FFlagEnableReportAbuseMenuRoact2': 'false', 'FIntReportDeviceInfoRollout': '0', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagDebugDisableOTAMaterialTexture': 'true', 'FFlagEnableReportAbuseMenuRoactABTest2': 'False', 'DFIntAnimationLodFacsDistanceMax': '0', 'FFlagEnableBubbleChatFromChatService': 'False', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'DFFlagESGamePerfMonitorEnabled': 'False', 'FIntStartupInfluxHundredthsPercentage': '0', 'FFlagEnableBetaBadgeLearnMore': 'false', 'FFlagEnableInGameMenuChromeABTest2': 'False', 'FFlagVoiceBetaBadge': 'false', 'FFlagEnableBubbleChatConfigurationV2': 'False', 'FFlagMSRefactor5': 'False', 'DFFlagDebugPerfMode': 'True', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FFlagGlobalWindRendering': 'false', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FFlagCloudsReflectOnWater': 'False', 'FFlagRenderCheckThreading': 'True', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FIntRobloxGuiBlurIntensity': '0', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagPreloadMinimalFonts': 'True', 'FFlagNullCheckCloudsRendering': 'True', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FFlagGameBasicSettingsFramerateCap': 'True', 'FIntCameraMaxZoomDistance': '99999', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'DFIntAnimationLodFacsDistanceMin': '0', 'FStringTerrainMaterialTablePre2022': '', 'FStringTerrainMaterialTable2022': ''},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "message (5)",
    'desc': "172 flags",
    'flags': {'FLogNetwork': '7', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntTextureQualityOverride': '0', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagDisablePostFx': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'FIntTerrainArraySliceSize': '8', 'FIntDebugForceMSAASamples': '0', 'DFFlagDisableDPIScale': 'True', 'DFIntTaskSchedulerTargetFps': '9999', 'FIntRenderShadowIntensity': '0', 'DFIntCanHideGuiGroupId': '32380007', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'FFlagPreloadMinimalFonts': 'True', 'FFlagUserPreventOldBubbleChatOverlap': 'False', 'FStringTerrainMaterialTable2022': '', 'FFlagEnableBetaBadgeLearnMore': 'false', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'FFlagBetaBadgeLearnMoreLinkFormview': 'false', 'FFlagEnableMenuModernizationABTest': 'False', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'FFlagRenderCheckThreading': 'True', 'FFlagCoreGuiTypeSelfViewPresent': 'False', 'FFlagRenderPerformanceTelemetry': 'False', 'DFIntUserIdPlayerNameLifetimeSeconds': '86400', 'FFlagEnableBubbleChatConfigurationV2': 'False', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagEnableAudioOutputDevice': 'false', 'FFlagEnableQuickGameLaunch': 'False', 'DFFlagESGamePerfMonitorEnabled': 'False', 'FStringVoiceBetaBadgeLearnMoreLink': 'null', 'FIntDefaultMeshCacheSizeMB': '256', 'FFlagEnableReportAbuseMenuRoact2': 'false', 'FFlagEnableMenuModernizationABTest2': 'False', 'FFlagCloudsReflectOnWater': 'False', 'FFlagEnableBubbleChatFromChatService': 'False', 'FIntDebugTextureManagerSkipMips': '100000000', 'FFlagTaskSchedulerLimitTargetFpsTo2402': 'False', 'FFlagAdServiceEnabled': 'False', 'DFStringHttpPointsReporterUrl': 'null', 'DFStringLightstepHTTPTransportUrlPath': 'null', 'DFStringRobloxAnalyticsURL': 'null', 'DFStringTelegrafHTTPTransportUrl': 'null', 'DFStringTelemetryV2Url': 'null', 'FFlagEnableInGameMenuChromeABTest2': 'False', 'FStringGamesUrlPath': '/games/', 'DFIntLightstepHTTPTransportHundredthsPercent2': '0', 'FFlagPreloadAllFonts': 'True', 'FStringCoreScriptBacktraceErrorUploadToken': 'null', 'DFFlagEnableLightstepReporting2': 'False', 'DFIntS2PhysicsSenderRate': '100', 'DFStringAltTelegrafHTTPTransportUrl': 'null', 'DFStringAltHttpPointsReporterUrl': 'null', 'FFlagFixGraphicsQuality': 'True', 'DFStringAnalyticsEventStreamUrlEndpoint': 'null', 'DFStringCrashUploadToBacktraceMacPlayerToken': 'null', 'DFStringCrashUploadToBacktraceBaseUrl': 'null', 'DFStringLightstepHTTPTransportUrlHost': 'null', 'DFStringLightstepToken': 'null', 'FFlagEnableReportAbuseMenuRoactABTest2': 'False', 'FIntRobloxGuiBlurIntensity': '0', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FIntFRMMinGrassDistance': '0', 'FIntFRMMaxGrassDistance': '0', 'FFlagUISUseLastFrameTimeInUpdateInputSignal': 'True', 'FFlagSimAdaptiveMinorOptimizations': 'True', 'FFlagPushFrameTimeToHarmony': 'True', 'FFlagOptimizeServerTickRate': 'True', 'FFlagOptimizeNetworkTransport': 'True', 'FFlagOptimizeNetwork': 'True', 'FFlagNewLightAttenuation': 'True', 'FFlagMSRefactor5': 'False', 'FFlagGameBasicSettingsFramerateCap2': 'True', 'DFIntVisibilityCheckRayCastLimitPerFrame': '10', 'DFIntTimeBetweenSendConnectionAttemptsMS': '200', 'DFIntRakNetResendRttMultiple': '1', 'DFIntRakNetLoopMs': '1', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFIntPlayerNetworkUpdateRate': '60', 'DFIntPlayerNetworkUpdateQueueSize': '20', 'DFIntPhysicsReceiveNumParallelTasks': '12', 'DFIntPerformanceControlFrameTimeMax': '1', 'DFIntNetworkSchemaCompressionRatio': '100', 'DFIntNetworkLatencyTolerance': '1', 'DFIntMaxProcessPacketsJobScaling': '10000', 'DFIntMaxFrameBufferSize': '4', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'DFIntConnectionMTUSize': '900', 'DFIntBufferCompressionLevel': '0', 'DFIntAnimatorThrottleMaxFramesToSkip': '1', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagDebugDisableTelemetryPoint': 'True', 'DFIntCodecMaxOutgoingFrames': '10000', 'FFlagFastGPULightCulling3': 'True', 'DFIntTextureCompositorActiveJobs': '0', 'FFlagEnableAccessibilitySettingsAPIV2': 'True', 'FIntRenderGrassHeightScaler': '0', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFStringCrashUploadToBacktraceWindowsPlayerToken': 'null', 'DFIntOptimizePingThreshold': '50', 'DFIntAnimationLodFacsDistanceMin': '0', 'FFlagEnableAccessibilitySettingsEffectsInExperienceChat': 'True', 'FFlagNullCheckCloudsRendering': 'True', 'FIntSimWorldTaskQueueParallelTasks': '12', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'FIntRakNetResendBufferArrayLength': '128', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFFlagEnableDynamicHeadByDefault': 'False', 'FIntCameraMaxZoomDistance': '99999', 'DFIntNetworkPrediction': '120', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFFlagDebugPauseVoxelizer': 'True', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'FFlagEnableAccessibilitySettingsEffectsInCoreScripts2': 'True', 'DFIntServerTickRate': '60', 'DFIntNumFramesAllowedToBeAboveError': '1', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntAnimationLodFacsDistanceMax': '0', 'FIntRenderGrassDetailStrands': '0', 'DFIntPerformanceControlFrameTimeMaxUtility': '-1', 'FFlagDebugGraphicsPreferVulkan': 'True', 'DFIntDebugFRMQualityLevelOverride': '1', 'FIntSmoothClusterTaskQueueMaxParallelTasks': '12', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'DFIntPhysicsAnalyticsHighFrequencyIntervalSec': '12', 'FFlagEnableAccessibilitySettingsInExperienceMenu2': 'True', 'FFlagDebugSkyGray': 'False', 'FFlagOptimizeNetworkRouting': 'True', 'DFIntBufferCompressionThreshold': '100', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagChatTranslationSettingEnabled3': 'False', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntReplicationDataCacheNumParallelTasks': '12', 'DFIntMegaReplicatorNumParallelTasks': '12', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'DFIntServerPhysicsUpdateRate': '60', 'DFIntCodecMaxIncomingPackets': '100', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'FFlagEnableInGameMenuControls': 'False', 'FFlagEnableNewInviteMenuIXP2': 'False', 'FIntReportDeviceInfoRollout': '0', 'FIntRenderLocalLightFadeInMs_enabled': '99999', 'FFlagVoiceBetaBadge': 'false', 'FIntRenderLocalLightUpdatesMax': '1', 'FFlagDontCreatePingJob': 'True', 'FFlagTopBarUseNewBadge': 'false', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'FIntStartupInfluxHundredthsPercentage': '0', 'FFlagEnableV3MenuABTest3': 'False', 'FIntMeshContentProviderForceCacheSize': '268435456', 'FFlagControlBetaBadgeWithGuac': 'false', 'FFlagEnableInGameMenuModernization': 'False', 'FFlagCommitToGraphicsQualityFix': 'True', 'FStringTerrainMaterialTablePre2022': '', 'DFFlagDebugPerfMode': 'True', 'FIntRenderLocalLightUpdatesMin': '1', 'FIntHSRClusterSymmetryDistancePercent': '10000', 'FFlagGlobalWindRendering': 'false', 'FFlagEnableMenuControlsABTest': 'False', 'FIntRenderShadowmapBias': '0'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "message (7)",
    'desc': "102 flags",
    'flags': {'FLogNetwork': '7', 'FFlagHandleAltEnterFullscreenManually': 'False', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntTextureQualityOverride': '3', 'DFIntTaskSchedulerTargetFps': '240', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'DFIntCanHideGuiGroupId': '32380007', 'DFFlagDisableDPIScale': 'True', 'FIntRenderShadowIntensity': '0', 'FFlagDisablePostFx': 'True', 'FIntTerrainArraySliceSize': '0', 'FFlagDebugGraphicsPreferD3D11FL10': 'True', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagDebugForceFutureIsBrightPhase2': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FIntFontSizePadding': '2', 'FFlagFixGraphicsQuality': 'True', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'FIntDebugForceMSAASamples': '1', 'FFlagEnableInGameMenuModernization': 'False', 'FFlagDebugDisableTelemetryPoint': 'True', 'FFlagAdServiceEnabled': 'False', 'DFIntAnimationLodFacsDistanceMin': '0', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'SFFlagFacialAnimation1BetaFeatureRolloutPercent': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '3', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'DFIntCSGLevelOfDetailSwitchingDistance': '1', 'SFFlagFacialAnimationRecordingBetaFeatureRoleSet': 'False', 'FFlagFacialAnimationStreamingServiceUniverseSettingsEnableVideo': 'False', 'DFIntAnimationLodFacsDistanceMax': '0', 'FIntFRMMinGrassDistance': '0', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '2', 'FIntFRMMaxGrassDistance': '0', 'FLogFacialAnimation1BetaFeatureUrl': 'https://opt-out.roblox.com/', 'SFFlagFacialAnimationRecordingBetaFeatureRolloutPercent': 'False', 'FStringFacialAnimation1BetaFeatureUrl': 'https://opt-out.roblox.com/', 'FFlagFacialAnimationStreamingCheckPauseStateAfterEmote2': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '4', 'FFlagEnableMenuControlsABTest': 'False', 'DFFlagDebugPauseVoxelizer': 'True', 'FFlagFacialAnimationStreamingServiceUniverseSettingsEnableAudio': 'False', 'FFlagFacialAnimationStreamingClearTrackImprovementsV2': 'False', 'FStringFacialAnimationRecordingBetaFeatureUrl': 'https://opt-out.roblox.com/', 'FFlagFacialAnimationStreamingServiceUserSettingsMock': 'False', 'DFIntCodecMaxIncomingPackets': '100', 'SFFlagFacialAnimationStreamRccThrottleServerCount': 'False', 'FFlagFacialAnimationStreamingServiceUserSettingsCache': 'False', 'FFlagFacialAnimationStreamingRcc': 'False', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'FFlagFacialAnimationStreamingServiceUserSettingsOptInVideo': 'False', 'FFlagGlobalWindRendering': 'False', 'FFlagFacialAnimationStreamingSearchForReplacementWhenRemovingAnimator': 'False', 'DFIntDebugFRMQualityLevelOverride': '1', 'FFlagFacialAnimationStreamingClearAllConnectionsFix2': 'False', 'FIntRobloxGuiBlurIntensity': '0', 'FFlagFacialAnimationRecordingInStudio': 'False', 'DFFlagFacialAnimationStreaming2': 'False', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'FFlagFacialAnimationStreamingServiceUserSettingsOptInAudio': 'False', 'DFFlagReduceFacialAnimationsWhenFacsStreaming': 'False', 'FLogFacialAnimationRecordingBetaFeatureUrl': 'https://opt-out.roblox.com/', 'SFFlagFacialAnimation1BetaFeatureRoleSet': 'False', 'FFlagFacialAnimationStreamingUseEnableFlags2': 'False', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'FIntMockClientLightingTechnologyIxpExperimentMode': '0', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'FFlagFacialAnimationStreamingServiceUniverseSettingsMock': 'False', 'FFlagEnableV3MenuABTest3': 'False', 'SFFlagReduceFacialAnimationsAudioVideoMode': 'False', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'DFIntMaxFrameBufferSize': '4', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'FFlagFacialAnimation1BetaFeature': 'False', 'FFlagGlobalWindActivated': 'False', 'DFIntRakNetLoopMs': '1', 'FFlagEnableInGameMenuControls': 'False', 'DFFlagReduceFacialAnimationsWhenFacsStreaming2': 'False', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFIntConnectionMTUSize': '900', 'FFlagEnableInGameMenuChromeABTest3': 'False', 'DFIntCodecMaxOutgoingFrames': '10000', 'FFlagFacialAnimationStreamingServiceUseServerThrottling': 'False', 'DFIntTimestepArbiterThresholdCFLThou': '300', 'DFIntTouchSenderMaxBandwidthBpsScaling': '-1', 'DFIntMaxProcessPacketsJobScaling': '10000', 'FFlagFacialAnimationStreamingValidateAnimatorBeforeRemoving': 'False', 'FFlagFacialAnimationStreamingIfNoDynamicHeadDisableA2C': 'False', 'DFIntAnimationLodFacsVisibilityDenominator': '0', 'FFlagDebugDisableTelemetryV2Event': 'True', 'FFlagFacialAnimationRecordingBetaFeature': 'False', 'FIntRenderGrassDetailStrands': '0', 'DFFlagVideoCaptureServiceEnabled': 'False', 'FFlagDebugTestingThingFreecam': 'True', 'DFIntDebugDynamicRenderKiloPixels': '1'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "message (9)",
    'desc': "74 flags",
    'flags': {'FLogNetwork': '1', 'FIntRenderShadowIntensity': '0', 'FFlagDisablePostFx': 'True', 'FIntTerrainArraySliceSize': '0', 'DFIntTaskSchedulerTargetFps': '300', 'DFIntTextureQualityOverride': '0', 'DFFlagTextureQualityOverrideEnabled': 'True', 'FIntFullscreenTitleBarTriggerDelayMillis': '18000000', 'DFIntCanHideGuiGroupId': '32380007', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FIntDebugForceMSAASamples': '1', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFFlagDisableDPIScale': 'True', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagDebugGraphicsPreferD3D11': 'True', 'FFlagCommitToGraphicsQualityFix': 'True', 'FFlagEnableInGameMenuModernization': 'True', 'FIntCameraMaxZoomDistance': '1000', 'FFlagDebugGraphicsPreferD3D11FL10': 'False', 'FFlagEnableInGameMenuChrome': 'False', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'FFlagPreloadAllFonts': 'True', 'DFIntPerformanceControlTextureQualityBestUtility': '-2', 'FFlagDebugDisableTelemetryPoint': 'True', 'FIntMockClientLightingTechnologyIxpExperimentQualityLevel': '7', 'FFlagGlobalWindRendering': 'false', 'FIntRenderLocalLightUpdatesMax': '1', 'FFlagEnableReportAbuseMenuLayerOnV3': 'false', 'SFFlagFacialAnimation1BetaFeatureRoleSet': 'False', 'FFlagGraphicsSettingsOnlyShowValidModes': 'True', 'FFlagFacialAnimationRecordingBetaFeature': 'False', 'FIntTerrainOTAMaxTextureSize': '10', 'DFIntClientLightingEnvmapPlacementTelemetryHundredthsPercent': '100', 'FFlagEnableFavoriteButtonForUgc': 'true', 'FFlagDebugSkyGray': 'True', 'FFlagFacialAnimationStreamingIfNoDynamicHeadDisableA2C': 'False', 'FFlagFacialAnimationStreamingServiceUserSettingsCache': 'False', 'FFlagDisableNewIGMinDUA': 'True', 'FFlagFacialAnimationStreamingServiceUseServerThrottling': 'False', 'FFlagGraphicsGLEnableSuperHQShadersExclusion': 'False', 'SFFlagFacialAnimation1BetaFeatureRolloutPercent': 'False', 'FFlagRenderGpuTextureCompressor': 'True', 'FFlagNewLightAttenuation': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'FIntFontSizePadding': '2', 'FFlagGraphicsGLEnableHQShadersExclusion': 'False', 'DFIntMaxFrameBufferSize': '6', 'FFlagUserCameraShake': 'False', 'FFlagDisableCameraShake': 'True', 'DFIntCameraShakeSpeed': '0', 'FFlagUserDisableDeltaTimeShaking': 'True', 'FFlagUserDisableExplosionShake': 'True', 'FFlagUserDisableDynamicCameraShaking': 'True', 'FFlagUserDisableDamageShake': 'True', 'FFlagUserDisableCameraFrameTimeVariation': 'True', 'FFlagUserDisableTimeBasedEffects': 'True', 'FFlagUserDisableDynamicHeadBob': 'True', 'FFlagUserDisableCameraBob': 'True', 'FFlagUserDisableLandingShake': 'True', 'FFlagUserDisableCameraTilt': 'True', 'FFlagUserDisableAllCameraEffects': 'True', 'FFlagUserDisableWeaponRecoilEffect': 'True', 'FFlagUserDisableMotionBlur': 'True', 'FFlagUserDisableHeadBob': 'True', 'FFlagUserLimitCameraFrameRate': 'True', 'FFlagUserForceStableCameraUpdate': 'True', 'FFlagSmoothCameraMotion': 'True', 'FFlagUserEnableRecoilShake': 'False', 'FFlagUserEnableJumpShake': 'False', 'FFlagUserEnableExplosionShake': 'False', 'FFlagUserEnableDamageShake': 'False', 'FFlagUserEnableVehicleShake': 'False', 'FFlagUserEnableScriptedShake': 'False', 'FFlagUserEnablePhysicsShake': 'False'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "qwdkmo (1)",
    'desc': "22 flags",
    'flags': {'TextureCompositorActiveJobs': '0', 'RenderShadowmapBias': '75', 'CSGLevelOfDetailSwitchingDistanceL34': '0', 'CSGLevelOfDetailSwitchingDistanceL23': '0', 'CSGLevelOfDetailSwitchingDistanceL12': '0', 'CSGLevelOfDetailSwitchingDistance': '0', 'TerrainArraySliceSize': '0', 'PerformanceControlTextureQualityBestUtility': '-1', 'RenderUseTextureManager224': 'False', 'IncludePowerSaverMode': 'True', 'EnablePowerTraceModule': 'True', 'DebugForceFSMCPULightCulling': 'True', 'DoNotSkipMipsBasedOnSystemMemoryPS': 'True', 'DebugLimitMinTextureResolutionWhenSkipMips': '9999999999999999', 'TM2SkipMipsForUnstreamable2': 'True', 'DebugTextureManagerSkipMips': '3', 'TextureQualityOverride': '0', 'TextureQualityOverrideEnabled': 'True', 'DisablePostFx': 'True', 'DFIntTaskSchedulerTargetFps': '9999', 'TaskSchedulerLimitTargetFpsTo2402': 'False', 'DFIntDebugTextureManagerSkipMips': '3'},
    'tag': "FUN",
})

BUILTIN_PRESETS.append({
    'name': "x",
    'desc': "153 flags",
    'flags': {'DFIntTaskSchedulerTargetFps': '9999', 'FFlagAdServiceEnabled': 'False', 'FFlagDebugDisableTelemetryEphemeralCounter': 'True', 'FIntDebugForceMSAASamples': '1', 'DFStringLightstepToken': 'null', 'FFlagDebugForceFutureIsBrightPhase3': 'True', 'FFlagDebugGraphicsPreferD3D11FL10': 'False', 'DFStringRobloxAnalyticsURL': 'null', 'FFlagFixGraphicsQuality': 'True', 'DFIntRaknetBandwidthInfluxHundredthsPercentageV2': '10000', 'DFFlagDebugPerfMode': 'False', 'FStringCoreScriptBacktraceErrorUploadToken': 'null', 'DFIntDebugFRMQualityLevelOverride': '1', 'FFlagDebugDisableTelemetryEventIngest': 'True', 'DFStringCrashUploadToBacktraceBaseUrl': 'null', 'FFlagEnableV3MenuABTest3': 'False', 'FIntRuntimeMaxNumOfThreads': '2400', 'FFlagDebugDisableTelemetryPoint': 'True', 'FIntDebugTextureManagerSkipMips': '3', 'DFIntCodecMaxIncomingPackets': '100', 'FFlagPreloadAllFonts': 'False', 'FFlagFastGPULightCulling3': 'True', 'DFStringTelemetryV2Url': 'null', 'DFIntPerformanceControlTextureQualityBestUtility': '-1', 'FFlagDisablePostFx': 'True', 'DFIntRakNetResendRttMultiple': '1', 'FFlagDisableNewIGMinDUA': 'True', 'DFFlagDebugPauseVoxelizer': 'True', 'FFlagDebugCheckRenderThreading': 'True', 'FFlagDebugDisableTelemetryV2Event': 'True', 'DFIntRenderingThrottleDelayInMS': '1', 'FFlagDebugDisableTelemetryV2Counter': 'True', 'DFStringCrashUploadToBacktraceMacPlayerToken': 'null', 'FFlagDebugGraphicsPreferD3D11': 'True', 'DFStringAltHttpPointsReporterUrl': 'null', 'DFIntConnectionMTUSize': '1200', 'FFlagDebugGraphicsPreferOpenGL': 'True', 'FFlagEnableInGameMenuChrome': 'True', 'DFIntWaitOnRecvFromLoopEndedMS': '100', 'FFlagDebugDisableTelemetryEphemeralStat': 'True', 'DFFlagDisableDPIScale': 'True', 'DFIntCodecMaxOutgoingFrames': '10000', 'DFIntRaknetBandwidthPingSendEveryXSeconds': '1', 'FFlagDebugRenderingSetDeterministic': 'True', 'FFlagDebugDisableTelemetryV2Stat': 'True', 'DFFlagTextureQualityOverrideEnabled': 'True', 'DFIntWaitOnUpdateNetworkLoopEndedMS': '100', 'FFlagDebugGraphicsPreferVulkan': 'True', 'DFIntRakNetClockDriftAdjustmentPerPingMillisecond': '100', 'DFFlagDebugRenderForceTechnologyVoxel': 'True', 'DFIntCSGLevelOfDetailSwitchingDistance': '0', 'FFlagEnableInGameMenuChromeABTest3': 'False', 'DFIntCSGLevelOfDetailSwitchingDistanceL34': '0', 'DFIntTextureQualityOverride': '0', 'DFStringLightstepHTTPTransportUrlHost': 'null', 'FIntRenderShadowIntensity': '0', 'DFIntRakNetLoopMs': '1', 'FFlagEnableMenuControlsABTest': 'False', 'FIntFullscreenTitleBarTriggerDelayMillis': '3600000', 'DFStringLightstepHTTPTransportUrlPath': 'null', 'FFlagEnableInGameMenuModernization': 'True', 'DFIntMaxProcessPacketsJobScaling': '10000', 'FIntTerrainArraySliceSize': '0', 'DFIntTextureCompositorActiveJobs': '0', 'DFIntMegaReplicatorNetworkQualityProcessorUnit': '10', 'DFStringHttpPointsReporterUrl': 'null', 'FFlagEnableInGameMenuControls': 'True', 'DFIntClientLightingTechnologyChangedTelemetryHundredthsPercent': '0', 'DFIntMaxProcessPacketsStepsPerCyclic': '5000', 'FFlagRenderDebugCheckThreading2': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL23': '0', 'DFIntLargePacketQueueSizeCutoffMB': '1000', 'DFFlagDisableFastLogTelemetry': 'True', 'DFIntCSGLevelOfDetailSwitchingDistanceL12': '0', 'DFIntMaxProcessPacketsStepsAccumulated': '0', 'FFlagNewLightAttenuation': 'True', 'FFlagGameBasicSettingsFramerateCap5': 'True', 'FIntTaskSchedulerThreadMin': '3', 'DFFlagBrowserTrackerIdTelemetryEnabled': 'False', 'FLogNetwork': '7', 'FFlagHandleAltEnterFullscreenManually': 'False', 'FFlagHighlightOutlinesOnMobile': 'True', 'FFlagDisableCameraShake': 'True', 'FFlagMinimizeCameraTilt': 'True', 'FFlagDisableFirstPersonViewBob': 'True', 'FIntCameraShakeIntensity': '0', 'FFlagReduceCameraShakeDuringGameplay': 'True', 'FFlagDisableExplosionShake': 'True', 'FFlagReduceRecoilEffects': 'True', 'FFlagDisableVehicleCameraShake': 'True', 'FFlagReduceImpactShake': 'True', 'FFlagLowMotionBlur': 'True', 'FFlagDisableCharacterLandingShake': 'True', 'FFlagDisablePhysicsImpactShake': 'True', 'FFlagReduceWeaponShake': 'True', 'FFlagDisableCutsceneCameraShake': 'True', 'FFlagReduceEnvironmentShake': 'True', 'FFlagNoShakeFromRunning': 'True', 'FFlagDisableShakeFromJumping': 'True', 'FFlagDisablePostProcessingShake': 'True', 'FFlagDisableCameraBob': 'True', 'FFlagReduceFallImpactShake': 'True', 'FFlagDisableWindShake': 'True', 'FFlagDisableCollisionShake': 'True', 'FFlagDisableShakeFromExplosions': 'True', 'FFlagDisableShakeFromDestruction': 'True', 'FFlagDisableShakeFromLanding': 'True', 'FFlagDisableEarthquakeEffects': 'True', 'FFlagReduceCameraDrag': 'True', 'FFlagReduceViewModelShake': 'True', 'FFlagDisableGunViewModelBob': 'True', 'FFlagReduceScreenVibration': 'True', 'FFlagDisableUnderwaterCameraShake': 'True', 'FFlagNoCameraShakeFromHitEffects': 'True', 'FFlagNoCameraShakeFromEnvironmentalImpact': 'True', 'FFlagNoCameraShakeFromProjectileCollisions': 'True', 'FFlagNoCameraShakeFromDestructionEffects': 'True', 'FFlagNoCameraShakeFromExplosionVFX': 'True', 'FFlagNoCameraShakeFromCharacterCombat': 'True', 'FFlagNoCameraShakeFromDamageIndicators': 'True', 'FFlagNoCameraShakeFromSkillImpact': 'True', 'FFlagNoCameraShakeFromCombatSkills': 'True', 'FFlagNoCameraShakeFromCollisionImpact': 'True', 'FFlagNoCameraShakeFromEnvironmentalCollisions': 'True', 'FFlagNoCameraShakeFromExplosionEffects': 'True', 'FFlagNoCameraShakeFromPlayerHits': 'True', 'FFlagNoCameraShakeFromProjectileAttacks': 'True', 'FFlagNoCameraShakeFromSpecialMoves': 'True', 'FFlagNoCameraShakeOnAnyExplosion': 'True', 'FFlagNoCameraShakeOnCombat': 'True', 'FFlagNoCameraShakeFromEnvironmentalEffects': 'True', 'FFlagNoCameraShakeFromVehicleMovement': 'True', 'FFlagNoCameraShakeFromAbilities': 'True', 'FFlagNoCameraShakeFromEnvironmentalHazards': 'True', 'FFlagNoCameraShakeFromTransformations': 'True', 'FFlagNoCameraShakeFromInteractions': 'True', 'FFlagNoCameraShakeFromCollisions': 'True', 'FFlagNoCameraShakeFromLanding': 'True', 'FFlagNoCameraShakeFromDamage': 'True', 'FFlagNoCameraShakeFromStatusEffects': 'True', 'FFlagNoCameraShakeFromCutscenes': 'True', 'FFlagNoCameraShakeFromSkills': 'True', 'FFlagNoCameraShakeFromWeapons': 'True', 'FFlagNoCameraShakeFromMagic': 'True', 'FFlagNoCameraShakeFromPlayerMovement': 'True', 'FFlagNoCameraShakeFromWeaponFiring': 'True', 'FFlagNoCameraShakeFromEnvironmentalImpacts': 'True', 'FFlagNoCameraShakeFromExplosionDamage': 'True', 'FFlagNoCameraShakeFromGameMechanics': 'True', 'FFlagNoCameraShakeFromCharacterInteractions': 'True', 'FFlagNoCameraShakeFromDynamicEvents': 'True', 'FFlagNoCameraShakeFromPlayerAbilities': 'True', 'FFlagNoCameraShakeFromGameAnimations': 'True'},
    'tag': "FUN",
})


class MainWindow(QMainWindow):
    _offset_status_signal = pyqtSignal(str)
    _offset_done_signal   = pyqtSignal(str)

    def __init__(self, state):
        super().__init__()
        self.state = state
        self.auto_worker = None
        self.all_flags = {}
        self._status_window = None

        self.setWindowTitle("sacredware")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setMinimumSize(900, 580)
        self.resize(1060, 680)
        self._drag_pos = None

        try:
            ico = Path(__file__).parent.parent / "cr.ico"
            if ico.exists():
                self.setWindowIcon(QIcon(str(ico)))
        except Exception:
            pass

        self.setStyleSheet(STYLE)
        self._build_ui()
        self._bg_label = None
        self._load_flags()
        self.centralWidget().setStyleSheet("border-radius: 18px; background: #0d0d0d;")
        self._setup_tray()
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(200, self._load_app_settings)
        QTimer.singleShot(500, self._apply_startup_behaviors)
        QTimer.singleShot(1500, self._auto_update_offsets_silent)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(0)
        root.setContentsMargins(0, 0, 0, 0)

        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(54)
        title_bar.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        title_bar.mousePressEvent   = self._tb_mouse_press
        title_bar.mouseMoveEvent    = self._tb_mouse_move
        title_bar.mouseReleaseEvent = self._tb_mouse_release
        tb = QHBoxLayout(title_bar)
        tb.setContentsMargins(18, 0, 10, 0)
        tb.setSpacing(12)

        title_label = TitleLabel("SacredWare")
        title_label.setObjectName("sacredTitle")
        from PyQt6.QtWidgets import QSizePolicy
        title_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.status_top = QLabel("Ready")
        self.status_top.setObjectName("statusLabel")
        self.status_top.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.status_top.setStyleSheet("color: #444444; background: transparent; padding-right: 4px;")

        self.btn_settings = QPushButton()
        self.btn_settings.setFixedSize(36, 30)
        self.btn_settings.setToolTip("Settings")
        self.btn_settings.setCheckable(True)
        self.btn_settings.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_settings.setStyleSheet("""
            QPushButton {
                background: transparent; border: none;
                border-radius: 8px; padding: 0; outline: none;
            }
            QPushButton:hover { background: rgba(255,255,255,0.05); }
            QPushButton:focus { outline: none; }
        """)

        def _make_gear_icon(active=False):
            from PyQt6.QtSvg import QSvgRenderer
            from PyQt6.QtGui import QPixmap, QPainter as _GP
            color = "#ffffff" if active else "#555555"
            svg = (
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" ' +
                f'stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
                '<circle cx="12" cy="12" r="3"/>' +
                '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06' +
                'a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09' +
                'A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83' +
                'l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09' +
                'A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83' +
                'l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09' +
                'a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83' +
                'l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09' +
                'a1.65 1.65 0 0 0-1.51 1z"/></svg>'
            )
            renderer = QSvgRenderer(svg.encode())
            px = QPixmap(20, 20)
            px.fill(Qt.GlobalColor.transparent)
            p = _GP(px)
            p.setRenderHint(_GP.RenderHint.Antialiasing)
            renderer.render(p)
            p.end()
            return QIcon(px)

        self._gear_icon_off = _make_gear_icon(False)
        self._gear_icon_on  = _make_gear_icon(True)
        self.btn_settings.setIcon(self._gear_icon_off)
        self.btn_settings.setIconSize(QSize(20, 20))

        def _on_settings_toggled(checked):
            self.btn_settings.setIcon(self._gear_icon_on if checked else self._gear_icon_off)
            self._toggle_settings()
        self.btn_settings.clicked.connect(_on_settings_toggled)

        btn_min = QPushButton("—")
        btn_min.setFixedSize(38, 28)
        btn_min.setStyleSheet("""
            QPushButton { background: transparent; border: none; color: #666666; font-size: 14px; border-radius: 6px; padding: 0; }
            QPushButton:hover { background: #1a1a1a; color: #ffffff; border-radius: 6px; }
        """)
        btn_min.clicked.connect(self.showMinimized)

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(38, 28)
        btn_close.setStyleSheet("""
            QPushButton { background: transparent; border: none; color: #666666; font-size: 14px; border-radius: 6px; padding: 0; }
            QPushButton:hover { background: #cc2222; color: #ffffff; border-radius: 6px; }
        """)
        btn_close.clicked.connect(self.close)

        self.btn_discord = QPushButton()
        self.btn_discord.setFixedSize(30, 30)
        self.btn_discord.setCursor(Qt.CursorShape.PointingHandCursor)
        discord_lbl = QLabel(self.btn_discord)
        discord_lbl.setFixedSize(30, 30)
        discord_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        discord_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        from PyQt6.QtSvg import QSvgRenderer
        from PyQt6.QtGui import QPainter as _P
        _SVG = b"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path fill='white' d='M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057c.002.022.015.043.03.054a19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z'/></svg>"""
        try:
            renderer = QSvgRenderer(_SVG)
            px = QPixmap(22, 22)
            px.fill(Qt.GlobalColor.transparent)
            pp = _P(px)
            pp.setCompositionMode(_P.CompositionMode.CompositionMode_SourceOver)
            pp.setRenderHint(_P.RenderHint.Antialiasing)
            renderer.render(pp)
            pp.end()
            discord_lbl.setPixmap(px)
            discord_lbl.setStyleSheet("background: transparent;")
        except Exception:
            discord_lbl.setText("D")
            discord_lbl.setStyleSheet("color:white;font-weight:700;font-size:13px;background:transparent;")
        self.btn_discord.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: transparent;
            }
        """)
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        self._discord_glow = QGraphicsDropShadowEffect()
        self._discord_glow.setBlurRadius(0)
        self._discord_glow.setColor(QColor(255, 255, 255, 0))
        self._discord_glow.setOffset(0, 0)
        self.btn_discord.setGraphicsEffect(self._discord_glow)

        from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
        self._discord_anim_in  = QPropertyAnimation(self._discord_glow, b"blurRadius")
        self._discord_anim_in.setDuration(180)
        self._discord_anim_in.setStartValue(0)
        self._discord_anim_in.setEndValue(22)
        self._discord_anim_in.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._discord_anim_out = QPropertyAnimation(self._discord_glow, b"blurRadius")
        self._discord_anim_out.setDuration(280)
        self._discord_anim_out.setStartValue(22)
        self._discord_anim_out.setEndValue(0)
        self._discord_anim_out.setEasingCurve(QEasingCurve.Type.InCubic)

        self._discord_popup = QLabel(self)
        self._discord_popup.setText("Join for more!\nPhantom Society™")
        self._discord_popup.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._discord_popup.setStyleSheet("""
            QLabel {
                background: rgba(10,10,10,0.95);
                color: #cccccc;
                font-size: 11px;
                font-weight: 500;
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 8px;
                padding: 7px 14px;
                line-height: 1.4;
            }
        """)
        self._discord_popup.adjustSize()
        self._discord_popup.hide()
        self._discord_popup.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        self._popup_opacity = QGraphicsOpacityEffect()
        self._popup_opacity.setOpacity(0.0)
        self._discord_popup.setGraphicsEffect(self._popup_opacity)

        self._popup_anim_in  = QPropertyAnimation(self._popup_opacity, b"opacity")
        self._popup_anim_in.setDuration(160)
        self._popup_anim_in.setStartValue(0.0)
        self._popup_anim_in.setEndValue(1.0)
        self._popup_anim_in.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._popup_anim_out = QPropertyAnimation(self._popup_opacity, b"opacity")
        self._popup_anim_out.setDuration(200)
        self._popup_anim_out.setStartValue(1.0)
        self._popup_anim_out.setEndValue(0.0)
        self._popup_anim_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self._popup_anim_out.finished.connect(self._discord_popup.hide)

        def _dc_enter(e):
            self._discord_glow.setColor(QColor(255, 255, 255, 210))
            self._discord_anim_out.stop()
            self._discord_anim_in.start()
            self._discord_popup.adjustSize()
            btn_pos = self.btn_discord.mapTo(self, self.btn_discord.rect().bottomLeft())
            pw = self._discord_popup.width()
            ph = self._discord_popup.height()
            x = btn_pos.x() - pw // 2 + self.btn_discord.width() // 2
            y = btn_pos.y() + 6
            x = max(8, min(x, self.width() - pw - 8))
            self._discord_popup.move(x, y)
            self._discord_popup.show()
            self._popup_anim_out.stop()
            self._popup_anim_in.start()

        def _dc_leave(e):
            self._discord_anim_in.stop()
            self._discord_anim_out.start()
            self._popup_anim_in.stop()
            self._popup_anim_out.start()

        self.btn_discord.enterEvent = _dc_enter
        self.btn_discord.leaveEvent = _dc_leave
        self.btn_discord.clicked.connect(lambda: __import__('webbrowser').open("https://discord.gg/Cznsg3cb"))

        tb.addWidget(title_label)
        tb.addStretch()
        tb.addWidget(self.status_top)
        tb.addWidget(self.btn_settings)
        tb.addWidget(btn_min)
        tb.addWidget(btn_close)
        root.addWidget(title_bar)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: transparent;")
        root.addWidget(self.stack)

        self._page_main = QWidget()
        self._page_main.setStyleSheet("background: transparent;")
        main_layout = QVBoxLayout(self._page_main)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.stack.addWidget(self._page_main)

        self._page_settings = QWidget()
        self._page_settings.setStyleSheet("background: transparent;")
        settings_layout = QVBoxLayout(self._page_settings)
        settings_layout.setSpacing(0)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        self.stack.addWidget(self._page_settings)
        self._build_settings_page(settings_layout)

        root = main_layout

        toolbar = QWidget()
        toolbar.setObjectName("toolbar")
        toolbar.setFixedHeight(46)
        tl = QHBoxLayout(toolbar)
        tl.setContentsMargins(12, 0, 12, 0)
        tl.setSpacing(6)

        _bs = """
            QPushButton {
                background-color: #141414;
                color: #cccccc;
                border: 1px solid #2a2a2a;
                border-radius: 8px;
                padding: 6px 16px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1e1e1e;
                border-color: #444444;
                color: #ffffff;
            }
            QPushButton:pressed { background-color: #0d0d0d; }
        """
        self.btn_add = QPushButton("Add"); self.btn_add.setStyleSheet(_bs)
        self.btn_remove = QPushButton("Remove"); self.btn_remove.setStyleSheet(_bs)
        self.btn_duplicate = QPushButton("Duplicate"); self.btn_duplicate.setStyleSheet(_bs)
        self.btn_clear = QPushButton("Remove All"); self.btn_clear.setStyleSheet(_bs)
        self.btn_import = QPushButton("Import"); self.btn_import.setStyleSheet(_bs)
        self.btn_export = QPushButton("Export"); self.btn_export.setStyleSheet(_bs)
        self.btn_backup = QPushButton("Backup"); self.btn_backup.setStyleSheet(_bs)
        self.btn_presets = QPushButton("Presets"); self.btn_presets.setStyleSheet(_bs)

        for b in [self.btn_add, self.btn_remove, self.btn_duplicate, self.btn_clear,
                  self.btn_import, self.btn_export, self.btn_presets]:
            tl.addWidget(b)

        tl.addStretch()

        _auto_off = """
            QPushButton {
                background-color: #1a0000;
                color: #cc3333;
                border: 1px solid #440000;
                border-radius: 8px;
                padding: 5px 14px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover { background-color: #220000; border-color: #882222; color: #ff4444; }
            QPushButton:pressed { background-color: #1a0000; }
        """
        _auto_on = """
            QPushButton {
                background-color: #141414;
                color: #cccccc;
                border: 1px solid #2a2a2a;
                border-radius: 8px;
                padding: 5px 14px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover { background-color: #1e1e1e; border-color: #444444; color: #ffffff; }
            QPushButton:pressed { background-color: #0d0d0d; }
        """
        self._auto_off_style = _auto_off
        self._auto_on_style  = _auto_on

        self.btn_auto = QPushButton("Auto Apply: OFF")
        self.btn_auto.setObjectName("btnAuto")
        self.btn_auto.setStyleSheet(_auto_off)

        self.btn_apply = QPushButton("Apply to Roblox")
        self.btn_apply.setObjectName("btnApply")
        self.btn_apply.setStyleSheet("""
            QPushButton {
                background-color: #161616;
                border: 1px solid #cccccc;
                color: #ffffff;
                font-weight: 700;
                border-radius: 8px;
                padding: 5px 14px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #222222; border-color: #ffffff; }
            QPushButton:pressed { background-color: #1a1a1a; }
        """)

        self.btn_kill = QPushButton("Kill Switch")
        self.btn_kill.setObjectName("btnKill")
        self.btn_kill.setStyleSheet("""
            QPushButton {
                background-color: #1a0000;
                color: #cc3333;
                border: 1px solid #440000;
                border-radius: 8px;
                padding: 5px 14px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover { background-color: #220000; border-color: #882222; color: #ff4444; }
            QPushButton:pressed { background-color: #1a0000; }
        """)

        for b in [self.btn_auto, self.btn_apply, self.btn_kill]:
            tl.addWidget(b)

        self.btn_update_offsets = QPushButton("⟳ Offsets")
        self.btn_update_offsets.setToolTip("Download latest FFlag offsets from remote")
        self.btn_update_offsets.setStyleSheet("""
            QPushButton {
                background-color: #141414;
                color: #aaaaaa;
                border: 1px solid #2a2a2a;
                border-radius: 8px;
                padding: 5px 14px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover { background-color: #1e1e1e; border-color: #444444; color: #ffffff; }
            QPushButton:pressed { background-color: #282828; }
            QPushButton:disabled { color: #333; border-color: #1a1a1a; }
        """)
        self.btn_update_offsets.clicked.connect(self._update_offsets)
        tl.addWidget(self.btn_update_offsets)
        root.addWidget(toolbar)

        search_bar = QWidget()
        search_bar.setStyleSheet("background:#0d0d0d; border-bottom: 1px solid #141414;")
        self._search_bar = search_bar
        sl = QHBoxLayout(search_bar)
        sl.setContentsMargins(12, 6, 12, 6)
        sl.setSpacing(8)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search flags...")
        sl.addWidget(self.search)
        self._search_scope = QPushButton("Name")
        self._search_scope.setCheckable(True)
        self._search_scope.setChecked(False)
        self._search_scope.setFixedSize(70, 28)
        self._search_scope.setStyleSheet("")
        self._search_scope.clicked.connect(self._toggle_search_scope)
        sl.addWidget(self._search_scope)
        self._count_label = QLabel("0 flags")
        self._count_label.setStyleSheet("color:#333; font-size:11px; background:transparent; min-width:60px;")
        self._count_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        sl.addWidget(self._count_label)
        root.addWidget(search_bar)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["#", "NAME", "TYPE", "VALUE"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(2, 90)
        self.table.setColumnWidth(3, 180)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.table.verticalScrollBar().setStyleSheet("""
            QScrollBar:vertical {
                background: transparent;
                width: 4px;
                margin: 0;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical {
                background: #2a2a2a;
                border-radius: 2px;
                min-height: 24px;
            }
            QScrollBar::handle:vertical:hover { background: #444444; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        """)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.table.setDragDropMode(QTableWidget.DragDropMode.InternalMove)
        self.table.setDragEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.setDropIndicatorShown(True)
        self.table.setDragDropOverwriteMode(False)
        self.table.setSortingEnabled(False)
        self.table.horizontalHeader().sectionClicked.connect(self._sort_by_column)
        self.table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #0d0d0d;
                color: #2a2a2a;
                font-size: 9px;
                font-weight: 600;
                letter-spacing: 2px;
                padding: 5px 10px;
                border: none;
                border-bottom: 1px solid #111111;
            }
        """)
        self._sort_col = -1
        self._sort_asc = True
        root.addWidget(self.table)

        bottom_bar = QWidget()
        bottom_bar.setStyleSheet("background:#090909; border-top: 1px solid #1a1a1a;")
        self._bottom_bar = bottom_bar
        bottom_bar.setFixedHeight(28)
        bl = QHBoxLayout(bottom_bar)
        bl.setContentsMargins(10, 0, 10, 0)
        bl.setSpacing(8)

        self.roblox_dot = QLabel("●")
        self.roblox_dot.setStyleSheet("color: #cc3333; font-size: 14px; background: transparent;")
        self.roblox_dot.setToolTip("Roblox: Not Running")

        self.status_msg = QLabel("Ready")
        self.status_msg.setStyleSheet("color: #444444; font-size: 11px; background: transparent;")

        bl.addWidget(self.roblox_dot)
        bl.addWidget(self.status_msg)
        bl.addStretch()

        self.btn_discord.setFixedSize(30, 28)
        self.btn_discord.setToolTip("Join our Discord")
        bl.addWidget(self.btn_discord)

        root.addWidget(bottom_bar)

        from PyQt6.QtCore import QTimer
        self._roblox_timer = QTimer(self)
        self._roblox_timer.timeout.connect(self._check_roblox)
        self._roblox_timer.start(2000)

        self.search.textChanged.connect(self._filter_table)
        self._search_by_value = False
        self.btn_add.clicked.connect(self._add_flag)
        self.btn_remove.clicked.connect(self._remove_flag)
        self.btn_duplicate.clicked.connect(self._duplicate_flag)
        self.btn_clear.clicked.connect(self._clear_flags)
        self.btn_apply.clicked.connect(self._apply_flags)
        self.btn_kill.clicked.connect(self._kill_switch)
        self.btn_auto.clicked.connect(self._toggle_auto_apply)
        self.btn_import.clicked.connect(self._import_flags)
        self.btn_export.clicked.connect(self._export_flags)
        self.btn_backup.clicked.connect(self._backup)
        self.btn_presets.clicked.connect(self._open_presets)
        self.table.doubleClicked.connect(self._edit_flag)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._table_context_menu)
        self.table.model().rowsMoved.connect(self._on_rows_moved)

    def _load_flags(self):
        try:
            from core.config_manager import load_flags, ensure_config_exists
            ensure_config_exists(self.state.config_file)
            raw = load_flags(self.state.config_file)
            self.state.last_loaded_data = raw
        except Exception:
            raw = {}
        self._apply_validation(raw)

    def _apply_validation(self, raw: dict):
        """Run validator, update table and show result in status bar."""
        try:
            from core.validator import validate_flags
            result = validate_flags(raw)
            self.all_flags = result.valid
            msg = result.summary()
            if result.roblox_missing:
                self._set_status(f"⚪  {msg}")
            elif result.skipped_count == 0:
                self._set_status(f"✔  {msg}")
            else:
                self._set_status(f"⚠  {msg}")
            if hasattr(self, 'status_top'):
                if result.skipped_count > 0:
                    self.status_top.setText(
                        f"{result.valid_count}/{result.total} valid  ·  "
                        f"{result.skipped_count} skipped"
                    )
                else:
                    self.status_top.setText(
                        f"{result.valid_count} flags loaded"
                    )
        except Exception:
            self.all_flags = raw
        self._populate_table(self.all_flags)

    def _populate_table(self, data: dict):
        self.table.setRowCount(0)
        for i, (name, value) in enumerate(data.items()):
            self.table.insertRow(i)
            self.table.setRowHeight(i, 36)

            num = QTableWidgetItem(str(i + 1))
            num.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            num.setForeground(QColor("#333333"))
            self.table.setItem(i, 0, num)

            name_item = QTableWidgetItem(name)
            name_item.setForeground(getattr(self, '_flag_name_color', QColor("#7eb8f7")))
            self.table.setItem(i, 1, name_item)

            v_str = str(value).lower()
            if v_str in ("true", "false"):
                ftype = "bool"
            elif "." in v_str:
                try: float(v_str); ftype = "float"
                except: ftype = "string"
            else:
                try: int(v_str); ftype = "int"
                except: ftype = "string"

            type_item = QTableWidgetItem(ftype.upper())
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            type_item.setForeground(QColor("#555555"))
            self.table.setItem(i, 2, type_item)

            val_item = QTableWidgetItem(str(value))
            val_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            val_item.setForeground(getattr(self, '_value_text_color', QColor("#e8e8e8")))
            self.table.setItem(i, 3, val_item)

        counts = {"bool": 0, "int": 0, "float": 0, "string": 0}
        for v in data.values():
            s = str(v).lower()
            if s in ("true","false"): counts["bool"] += 1
            elif "." in s:
                try: float(s); counts["float"] += 1
                except: counts["string"] += 1
            else:
                try: int(s); counts["int"] += 1
                except: counts["string"] += 1
        parts = []
        for t, c in counts.items():
            if c: parts.append(f"{c} {t}")
        stat = " · ".join(parts) if parts else "empty"
        self._set_status(f"{len(data)} flags  |  {stat}")
        self.status_top.setText(f"{len(data)} flags")
        if hasattr(self, '_count_label'):
            self._count_label.setText(f"{len(data)} flags")

    def _merge_flags(self, new_flags: dict) -> int:
        """Merge new_flags into self.all_flags. Existing keys are NOT overwritten.
        Returns count of actually added (new) flags."""
        added = 0
        for k, v in new_flags.items():
            if k not in self.all_flags:
                sv = str(v).lower()
                if sv == "true":
                    self.all_flags[k] = True
                elif sv == "false":
                    self.all_flags[k] = False
                else:
                    try:
                        self.all_flags[k] = int(v)
                    except (ValueError, TypeError):
                        try:
                            self.all_flags[k] = float(v)
                        except (ValueError, TypeError):
                            self.all_flags[k] = str(v)
                added += 1
        return added

    def _save_flags(self):
        from core.config_manager import save_flags
        save_flags(self.state.config_file, self.all_flags)
        self._tray_update_count()

    def _filter_table(self, text=None):
        if text is None:
            text = self.search.text() if hasattr(self, 'search') else ""
        if not text:
            self._populate_table(self.all_flags)
            return
        tl = text.lower()
        if getattr(self, '_search_by_value', False):
            filtered = {k: v for k, v in self.all_flags.items()
                        if tl in k.lower() or tl in str(v).lower()}
        else:
            filtered = {k: v for k, v in self.all_flags.items() if tl in k.lower()}
        self._populate_table(filtered)

    def _toggle_search_scope(self):
        self._search_by_value = self._search_scope.isChecked()
        self._search_scope.setText("Name+Val" if self._search_by_value else "Name")
        self._filter_table()

    def _add_flag(self):
        dlg = AddFlagDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name, value, ftype = dlg.get_data()
            if name:
                if ftype == "bool": value = value.lower() in ("true","1","yes")
                elif ftype == "int":
                    try: value = int(value)
                    except: value = 0
                elif ftype == "float":
                    try: value = float(value)
                    except: value = 0.0
                self.all_flags[name] = value
                self._save_flags()
                self._populate_table(self.all_flags)

    def _edit_flag(self, index):
        row = index.row()
        name  = self.table.item(row, 1).text()
        value = self.table.item(row, 3).text()
        ftype = self.table.item(row, 2).text().lower()
        dlg = AddFlagDialog(self, name=name, value=value, flag_type=ftype)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            new_name, new_value, new_type = dlg.get_data()
            if new_name:
                del self.all_flags[name]
                if new_type == "bool": new_value = new_value.lower() in ("true","1","yes")
                elif new_type == "int":
                    try: new_value = int(new_value)
                    except: new_value = 0
                elif new_type == "float":
                    try: new_value = float(new_value)
                    except: new_value = 0.0
                self.all_flags[new_name] = new_value
                self._save_flags()
                self._populate_table(self.all_flags)

    def _remove_flag(self):
        self._remove_selected_flags()

    def _duplicate_flag(self):
        """Duplicate selected flags — appends _copy suffix if name already exists."""
        rows = sorted(set(i.row() for i in self.table.selectedItems()))
        if not rows:
            self._set_status("Select a flag to duplicate")
            return
        added = 0
        for row in rows:
            item = self.table.item(row, 1)
            if not item: continue
            name = item.text()
            value = self.all_flags.get(name)
            if value is None: continue
            new_name = name + "_copy"
            suffix = 2
            while new_name in self.all_flags:
                new_name = f"{name}_copy{suffix}"
                suffix += 1
            self.all_flags[new_name] = value
            added += 1
        if added:
            self._save_flags()
            self._populate_table(self.all_flags)
            self._set_status(f"Duplicated {added} flag(s)")

    def _remove_selected_flags(self):
        """Remove all selected rows (multi-select support)."""
        rows = sorted(set(i.row() for i in self.table.selectedItems()), reverse=True)
        if not rows:
            return
        names = []
        for row in rows:
            item = self.table.item(row, 1)
            if item:
                names.append(item.text())
        for name in names:
            self.all_flags.pop(name, None)
        self._save_flags()
        self._populate_table(self.all_flags)
        self._set_status(f"Removed {len(names)} flag(s)")

    def _sort_by_column(self, col):
        """Sort all_flags by column: 1=name, 2=type, 3=value."""
        if col not in (1, 2, 3): return
        if self._sort_col == col:
            self._sort_asc = not self._sort_asc
        else:
            self._sort_col = col
            self._sort_asc = True
        def key_fn(item):
            k, v = item
            if col == 1: return k.lower()
            if col == 2:
                s = str(v).lower()
                if s in ("true","false"): return "bool"
                try: int(s); return "int"
                except: pass
                try: float(s); return "float"
                except: return "string"
            return str(v).lower()
        self.all_flags = dict(sorted(self.all_flags.items(), key=key_fn, reverse=not self._sort_asc))
        self._save_flags()
        self._populate_table(self.all_flags)
        arrow = " ▲" if self._sort_asc else " ▼"
        labels = {1: "NAME", 2: "TYPE", 3: "VALUE"}
        for c, lbl in [(0,"#"),(1,"NAME"),(2,"TYPE"),(3,"VALUE")]:
            self.table.horizontalHeaderItem(c).setText(lbl + (arrow if c == col else ""))

    def _on_rows_moved(self, parent, start, end, dest_parent, dest_row):
        """Sync all_flags order after drag-drop row reorder."""
        keys = list(self.all_flags.keys())
        moved_keys = keys[start:end+1]
        remaining = [k for i, k in enumerate(keys) if i < start or i > end]
        adj = dest_row if dest_row <= start else dest_row - (end - start + 1)
        adj = max(0, min(adj, len(remaining)))
        new_keys = remaining[:adj] + moved_keys + remaining[adj:]
        self.all_flags = {k: self.all_flags[k] for k in new_keys if k in self.all_flags}
        self._save_flags()

    def _table_context_menu(self, pos):
        """Right-click context menu for the flag table."""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QClipboard
        rows = sorted(set(i.row() for i in self.table.selectedItems()))
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background: #0d0d0d;
                    color: #cccccc;
            QMenu::item { padding:7px 18px; border-radius:5px; }
            QMenu::item:selected { background: #0d0d0d;
            QMenu::separator { height:1px; background: #0d0d0d;
        """)
        if len(rows) == 1:
            row = rows[0]
            name_item = self.table.item(row, 1)
            val_item  = self.table.item(row, 3)
            if name_item and val_item:
                act_copy_name  = menu.addAction("⎘  Copy Name")
                act_copy_val   = menu.addAction("⎘  Copy Value")
                act_copy_pair  = menu.addAction("⎘  Copy as JSON")
                menu.addSeparator()
                act_edit       = menu.addAction("✎  Edit")
                act_dup        = menu.addAction("⊞  Duplicate")
                menu.addSeparator()
                act_del        = menu.addAction("✕  Delete")
                chosen = menu.exec(self.table.viewport().mapToGlobal(pos))
                if chosen == act_copy_name:
                    QApplication.clipboard().setText(name_item.text())
                elif chosen == act_copy_val:
                    QApplication.clipboard().setText(val_item.text())
                elif chosen == act_copy_pair:
                    import json as _json
                    pair = {name_item.text(): self.all_flags.get(name_item.text(), val_item.text())}
                    QApplication.clipboard().setText(_json.dumps(pair, indent=2))
                elif chosen == act_edit:
                    self._edit_flag(self.table.model().index(row, 1))
                elif chosen == act_dup:
                    self.table.clearSelection()
                    self.table.selectRow(row)
                    self._duplicate_flag()
                elif chosen == act_del:
                    self._remove_selected_flags()
        elif len(rows) > 1:
            act_dup = menu.addAction(f"⊞  Duplicate {len(rows)} flags")
            menu.addSeparator()
            act_del = menu.addAction(f"✕  Delete {len(rows)} flags")
            chosen = menu.exec(self.table.viewport().mapToGlobal(pos))
            if chosen == act_dup:
                self._duplicate_flag()
            elif chosen == act_del:
                self._remove_selected_flags()

    def _clear_flags(self):
        should_confirm = getattr(self, '_chk_confirm_clear', None)
        if should_confirm is None or should_confirm.isChecked():
            dlg = ConfirmDialog("Remove all flags?", self)
            if dlg.exec() != QDialog.DialogCode.Accepted:
                return
        self.all_flags = {}
        self._save_flags()
        self._populate_table(self.all_flags)

    def _open_status_window(self):
        if self._status_window is None or not self._status_window.isVisible():
            self._status_window = InjectorStatusDialog(None)
            try:
                from core.injector import _ACTIVE_OFFSET_COUNT, _TO_VALUE, _LIST_POINTER_OFF
                self._status_window.push(
                    f"Offset table: {_ACTIVE_OFFSET_COUNT} flags loaded  ·  "
                    f"ToValue=0x{_TO_VALUE:X}  ·  ListPointer=0x{_LIST_POINTER_OFF:X}",
                    'info'
                )
            except Exception:
                pass
            self._status_window.show()
        else:
            self._status_window.raise_()
            self._status_window.activateWindow()

    def _auto_update_offsets_silent(self):
        """Called once on startup — update offsets silently, no UI disruption."""
        try:
            self._offset_status_signal.connect(self._set_status)
            self._offset_done_signal.connect(self._on_offset_done_silent)
        except Exception:
            pass
        try:
            from core.injector import update_offsets_async
            update_offsets_async(
                status_cb=lambda msg: None,
                done_cb=lambda r: self._offset_done_signal.emit(r),
            )
        except Exception as e:
            print(f"[GUI] Auto offset update failed: {e}")

    @pyqtSlot(str)
    def _on_offset_done_silent(self, result: str):
        """Runs on main thread via signal — safe to touch UI."""
        print(f"[GUI] Auto offset update: {result}")
        if result.startswith("✓"):
            self._set_status(result)
        try:
            self.btn_update_offsets.setEnabled(True)
            self.btn_update_offsets.setText("⟳ Offsets")
        except Exception:
            pass

    def _update_offsets(self):
        """Download latest FFlag offsets from remote and reload."""
        from core.injector import update_offsets_async, get_offset_debug

        btn = self.btn_update_offsets
        btn.setEnabled(False)
        btn.setText("Updating...")
        self._set_status("Fetching offsets from remote...")

        try:
            self._offset_status_signal.disconnect()
        except Exception:
            pass
        try:
            self._offset_done_signal.disconnect()
        except Exception:
            pass
        self._offset_status_signal.connect(self._set_status)
        self._offset_done_signal.connect(self._on_offset_done_manual)

        update_offsets_async(
            status_cb=lambda msg: self._offset_status_signal.emit(msg),
            done_cb=lambda r: self._offset_done_signal.emit(r),
        )

    @pyqtSlot(str)
    def _on_offset_done_manual(self, result: str):
        """Runs on main thread via signal — safe to touch UI."""
        from core.injector import get_offset_debug
        btn = self.btn_update_offsets
        btn.setEnabled(True)
        btn.setText("⟳ Offsets")
        self._set_status(result)
        try:
            print(f"[GUI] Offsets updated — {get_offset_debug()}")
        except Exception:
            pass
        try:
            self._offset_status_signal.disconnect(self._set_status)
        except Exception:
            pass
        try:
            self._offset_done_signal.disconnect(self._on_offset_done_manual)
        except Exception:
            pass

    def _apply_flags(self):
        from core.injector import apply_flags
        self.btn_apply.setEnabled(False)
        self.btn_apply.setText("Applying...")
        self._set_status("Applying FFlags to Roblox...")

        import threading
        def _worker():
            try:
                import ctypes
                ctypes.windll.kernel32.SetThreadPriority(
                    ctypes.windll.kernel32.GetCurrentThread(), -1)
            except:
                pass
            try:
                result = apply_flags(self.all_flags)
            except Exception as e:
                result = f"Error: {e}"
            from PyQt6.QtCore import QMetaObject, Qt, Q_ARG
            QMetaObject.invokeMethod(self, "_on_apply_done",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, result))

        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    @pyqtSlot(str)
    def _on_apply_done(self, result: str):
        self.btn_apply.setEnabled(True)
        self.btn_apply.setText("Apply to Roblox")
        self._set_status(result)
        self.status_top.setText(result)

        if self._status_window and self._status_window.isVisible():
            try:
                from core.injector import _instance
                skipped = getattr(_instance, '_last_skipped', [])
                applied_names = [n for n in self.all_flags if n not in skipped]
                self._status_window.push_apply_result(result, list(self.all_flags.keys()), skipped)
            except Exception:
                self._status_window.push(result, 'info')

    def _kill_switch(self):
        """
        Kill Switch: writes default/zero values to every applied FFlag
        in Roblox memory, effectively reverting them in-game.
        Does NOT clear the editor — flags stay visible, only Roblox is reset.
        """
        killed  = 0
        failed  = 0
        roblox_missing = False

        if self.all_flags:
            try:
                from core.injector import _instance, apply_flags

                if not _instance.pm or not _instance.is_process_alive():
                    _instance.detach()
                    if not _instance.attach():
                        roblox_missing = True
                        raise RuntimeError("Roblox not found")
                    _instance.flag_cache.clear()
                    _instance.cached_singleton = 0

                zero_data = {}
                for k, v in self.all_flags.items():
                    s = str(v).lower()
                    if s in ('true', 'false'):
                        zero_data[k] = 'false'
                    elif '.' in s:
                        try: float(s); zero_data[k] = '0.0'
                        except: zero_data[k] = 'false'
                    else:
                        try: int(s); zero_data[k] = '0'
                        except: zero_data[k] = 'false'

                if zero_data:
                    _instance.flag_cache.clear()
                    for k, v in zero_data.items():
                        try:
                            if _instance.set_value(k, v):
                                killed += 1
                            else:
                                failed += 1
                        except Exception:
                            failed += 1

            except RuntimeError:
                pass
            except Exception:
                pass

        if roblox_missing:
            msg = "Kill Switch — Roblox not running. Editor unchanged."
        elif killed == 0 and not self.all_flags:
            msg = "Kill Switch — no flags loaded in editor."
        elif failed > 0:
            msg = f"Kill Switch — {killed} flags reset in Roblox, {failed} failed."
        else:
            msg = f"Kill Switch — {killed} flags reset to default in Roblox."

        self._set_status(msg)
        self.status_top.setText(f"Killed {killed}" if killed else "Kill Switch")

    def _trigger_lagswitch(self):
        """Lag Switch — drops FPS for a short duration then restores."""
        from core.lagswitch import trigger as ls_trigger

        fps      = getattr(self, '_slider_ls_fps', None)
        dur      = getattr(self, '_slider_ls_dur', None)
        fps_val  = fps.value() if fps else 15
        dur_val  = (dur.value() / 10.0) if dur else 0.7

        orig_fps = 2147483647
        if hasattr(self, 'all_flags'):
            for k in ('DFIntTaskSchedulerTargetFps', 'TaskSchedulerTargetFps'):
                if k in self.all_flags:
                    try: orig_fps = int(self.all_flags[k])
                    except: pass
                    break

        ls_trigger(fps=fps_val, duration=dur_val, original_fps=orig_fps)

    def _on_auto_apply_status(self, msg: str):
        """Handle status updates from AutoApplyWorker, including Access Denied."""
        if "ACCESS_DENIED" in msg:
            self.btn_auto.setText("Auto Apply: OFF")
            self._update_auto_styles()
            if getattr(self, '_act_auto', None):
                self._act_auto.setText("⟳ Auto Apply: OFF")
            if getattr(self, '_tray', None):
                self._tray.setToolTip("SacredWare — FFlags running")
            self._restore_apply_style()
            self._set_status("⚠ Auto Apply stopped — Access Denied")
            from PyQt6.QtWidgets import QMessageBox
            AlertDialog(
                "ACCESS DENIED",
                "Auto Apply stopped — Access Denied\n\n"
                "Windows blocked SacredWare from writing to Roblox.\n\n"
                "Right-click SacredWare.exe\n→ Run as Administrator",
                parent=self
            ).exec()
        else:
            self._set_status(msg)

    def _toggle_auto_apply(self):
        self.btn_auto.setEnabled(False)
        try:
            if not self.state.auto_apply_enabled:
                self.state.auto_apply_enabled = True
                if self.auto_worker is not None:
                    self.auto_worker.stop()
                    self.auto_worker.wait(1000)
                    self.auto_worker = None
                self.auto_worker = AutoApplyWorker(self.state, self.state.config_file)
                self.auto_worker.status_update.connect(self._on_auto_apply_status)
                self.auto_worker.start()
                self.btn_auto.setText("Auto Apply: ON")
                self.btn_auto.setStyleSheet(self._auto_on_style)
                if getattr(self, '_act_auto', None): self._act_auto.setText("⟳ Auto Apply: ON  ✓")
                if getattr(self, '_tray', None): self._tray.setToolTip("SacredWare — Auto Apply ON")
                self._restore_apply_style()
            else:
                self.state.auto_apply_enabled = False
                if self.auto_worker is not None:
                    self.auto_worker.stop()
                    self.auto_worker.wait(1000)
                    self.auto_worker = None
                self.btn_auto.setText("Auto Apply: OFF")
                self._update_auto_styles()
                if getattr(self, '_act_auto', None): self._act_auto.setText("⟳ Auto Apply: OFF")
                if getattr(self, '_tray', None): self._tray.setToolTip("SacredWare — FFlags running")
                self._set_status("Auto Apply turned off.")
                self._restore_apply_style()
        finally:
            self.btn_auto.setEnabled(True)
            self._restore_apply_style()

    def _restore_apply_style(self):
        """Reapply the current accent color to Apply button."""
        ac = getattr(self, '_theme_accent', QColor(255,255,255))
        is_transparent = getattr(self, '_bg_path', '') != ''
        if is_transparent:
            self.btn_apply.setStyleSheet(f"""
                QPushButton {{ background:rgba(0,0,0,0.4); border:1px solid rgb({ac.red()},{ac.green()},{ac.blue()});
                               color:rgb({ac.red()},{ac.green()},{ac.blue()}); font-weight:700;
                               border-radius:8px; padding:5px 14px; font-size:12px; }}
                QPushButton:hover {{ background:rgba(255,255,255,0.15); color: #ffffff; }}
                QPushButton:pressed {{ background:rgba(0,0,0,0.6); }}
            """)
        else:
            self.btn_apply.setStyleSheet(f"""
                QPushButton {{ background-color: #161616;
                               border: 1px solid rgb({ac.red()},{ac.green()},{ac.blue()});
                               color:rgb({ac.red()},{ac.green()},{ac.blue()});
                               font-weight:700; border-radius:8px; padding:5px 14px; font-size:12px; }}
                QPushButton:hover {{ background-color: #222222; border-color: rgb({min(ac.red()+40,255)},{min(ac.green()+40,255)},{min(ac.blue()+40,255)}); color: #ffffff; }}
                QPushButton:pressed {{ background-color: #1a1a1a; }}
            """)

    def _update_auto_styles(self):
        c = getattr(self, '_btn_color_val', QColor(20, 20, 20))
        is_transparent = getattr(self, '_bg_path', '') != ''
        if is_transparent:
            self._auto_off_style = """
                QPushButton { background:rgba(0,0,0,0.35); color: #cccccc;
                              border:1px solid rgba(255,255,255,0.1); border-radius:8px;
                              padding:5px 14px; font-size:12px; font-weight:500; }
                QPushButton:hover { background:rgba(255,255,255,0.1); border-color:rgba(255,255,255,0.3); color: #ffffff; }
                QPushButton:pressed { background:rgba(255,255,255,0.05); }
            """
            _scope_style = """
                QPushButton { background:rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.1);
                              border-radius:6px; color: #cccccc; }
                QPushButton:checked { background:rgba(255,255,255,0.1); border-color:rgba(255,255,255,0.3); color: #ffffff; }
                QPushButton:hover { border-color:rgba(255,255,255,0.2); color: #ffffff; }
            """
        else:
            self._auto_off_style = f"""
                QPushButton {{ background-color:rgb({c.red()},{c.green()},{c.blue()}); color: #cccccc;
                              border:1px solid #2a2a2a; border-radius:8px;
                              padding:5px 14px; font-size:12px; font-weight:500; }}
                QPushButton:hover {{ background-color:rgb({min(c.red()+20,255)},{min(c.green()+20,255)},{min(c.blue()+20,255)}); border-color: #444444; color: #ffffff; }}
                QPushButton:pressed {{ background-color:rgb({max(c.red()-10,0)},{max(c.green()-10,0)},{max(c.blue()-10,0)}); }}
            """
            _scope_style = f"""
                QPushButton {{ background-color:rgb({c.red()},{c.green()},{c.blue()}); border:1px solid #2a2a2a;
                              border-radius:6px; color: #cccccc; }}
                QPushButton:checked {{ background-color:rgb({min(c.red()+15,255)},{min(c.green()+15,255)},{min(c.blue()+15,255)}); border-color: #444444; }}
                QPushButton:hover {{ border-color: #444444; color: #ffffff; }}
            """
        self._auto_on_style = """
            QPushButton { background-color: #141414; color: #cccccc;
                          border: 1px solid #2a2a2a; border-radius:8px;
                          padding:5px 14px; font-size:12px; font-weight:500; }
            QPushButton:hover { background-color: #1e1e1e; border-color: #444444; color: #ffffff; }
            QPushButton:pressed { background-color: #0d0d0d; }
        """
        if not getattr(self.state, 'auto_apply_enabled', False):
            self.btn_auto.setStyleSheet(self._auto_off_style)
        if hasattr(self, '_search_scope'):
            self._search_scope.setStyleSheet(_scope_style)

    def _save_preset(self):
        if not self.all_flags:
            self._set_status("No flags to save.")
            return
        dlg = SavePresetDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            name = dlg.get_name()
            presets = load_presets(self.state)
            presets[name] = dict(self.all_flags)
            save_presets(self.state, presets)
            self._set_status(f"Preset '{name}' saved ({len(self.all_flags)} flags).")

    def _open_presets(self):
        presets = load_presets(self.state)
        if not presets:
            self._save_preset()
            return
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background: #0d0d0d;
            QMenu::item { padding:8px 20px; border-radius:4px; }
            QMenu::item:selected { background: #0d0d0d;
        """)
        act_load = menu.addAction("☰  Browse Presets")
        menu.addSeparator()
        act_save = menu.addAction("＋  Save Current as Preset")
        chosen = menu.exec(self.btn_presets.mapToGlobal(
            self.btn_presets.rect().bottomLeft()))
        if chosen == act_load:
            dlg = PresetListDialog(presets, self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                name = dlg.get_chosen()
                save_presets(self.state, dlg.get_updated_presets())
                if name and name in dlg.get_updated_presets():
                    flags = dlg.get_updated_presets()[name]
                    try:
                        from core.validator import validate_flags
                        vr = validate_flags(flags)
                        flags_to_add = vr.valid
                        if vr.skipped_count > 0 and not vr.roblox_missing:
                            self._set_status(
                                f"⚠  Preset: {vr.skipped_count} invalid flags skipped, "
                                f"{vr.valid_count} valid loaded."
                            )
                    except Exception:
                        flags_to_add = flags
                    added = self._merge_flags(flags_to_add)
                    skipped = len(flags_to_add) - added
                    self._save_flags()
                    self._populate_table(self.all_flags)
                    msg = f"Added preset '{name}' — {added} new flags"
                    if skipped: msg += f" ({skipped} duplicates skipped)"
                    self._set_status(msg)
        elif chosen == act_save:
            self._save_preset()

    def _import_flags(self):
        dlg = ImportDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            try:
                from core.validator import validate_flags
                vr = validate_flags(data)
                data = vr.valid
                if not vr.roblox_missing and vr.skipped_count > 0:
                    self._set_status(
                        f"⚠  Import: {vr.skipped_count} invalid flags skipped, "
                        f"{vr.valid_count} valid."
                    )
            except Exception:
                pass
            added = self._merge_flags(data)
            skipped = len(data) - added
            self._save_flags()
            self._populate_table(self.all_flags)
            msg = f"Imported {added} flags"
            if skipped: msg += f" ({skipped} duplicates skipped)"
            self._set_status(msg)

    def _export_flags(self):
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getSaveFileName(
            self, "Export FFlags", "flags.json",
            "JSON Files (*.json);;Text Files (*.txt);;All Files (*)"
        )
        if not path:
            return
        try:
            if path.endswith(".txt"):
                entries = []
                for k, v in self.all_flags.items():
                    entries.append('    "' + k + '": "' + str(v) + '"')
                txt_out = "{" + chr(10) + ("," + chr(10)).join(entries) + chr(10) + "}"
                with open(path, "w", encoding="utf-8") as f:
                    f.write(txt_out)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(self.all_flags, f, indent=4, ensure_ascii=False)
            self._set_status(f"Exported {len(self.all_flags)} flags to {path}")
        except Exception as e:
            self._set_status(f"Export error: {e}")

    def _backup(self):
        from core.actions import action_backup
        self._set_status(action_backup(self.state))


    def _set_status(self, msg):
        try:
            self.status_msg.setText(msg)
        except Exception:
            pass

    def _check_roblox(self):
        import ctypes.wintypes, ctypes
        try:
            import subprocess
            out = subprocess.check_output(
                'tasklist /FI "IMAGENAME eq RobloxPlayerBeta.exe" /NH',
                shell=True, stderr=subprocess.DEVNULL).decode()
            running = "RobloxPlayerBeta.exe" in out
        except Exception:
            running = False
        if running:
            self.roblox_dot.setStyleSheet("color: #22cc44; font-size: 14px; background: transparent;")
            self.roblox_dot.setToolTip("Roblox: Running")
            if not getattr(self, '_warmup_done', False):
                self._warmup_done = True
                try:
                    from core.injector import warmup_singleton
                    warmup_singleton()
                except Exception:
                    pass
        else:
            self.roblox_dot.setStyleSheet("color: #cc3333; font-size: 14px; background: transparent;")
            self.roblox_dot.setToolTip("Roblox: Not Running")
            self._warmup_done = False

    def _toggle_settings(self):
        if self.btn_settings.isChecked():
            self.stack.setCurrentIndex(1)
            self.status_top.setText("Settings")
        else:
            self.stack.setCurrentIndex(0)
            self.status_top.setText(f"{len(self.all_flags)} flags")

    def _build_settings_page(self, layout):
        _SLIDER_STYLE = """
            QSlider::groove:horizontal { background: #1a1a1a; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: #cccccc; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }
            QSlider::sub-page:horizontal { background: #cccccc; height: 4px; border-radius: 2px; }
        """
        _CHK_STYLE = """
            QCheckBox { background: transparent; }
            QCheckBox::indicator { width:18px; height:18px; border:1px solid #2a2a2a; border-radius:4px; background:#141414; }
            QCheckBox::indicator:checked { background: #cccccc; border-color: #cccccc; image: none; }
        """
        _LABEL = "color: #888888; font-size: 12px; background: transparent;"
        _VAL   = "color: #cccccc; font-size: 12px; background: transparent; min-width: 36px;"
        _DIVIDER = "background: #1a1a1a; max-height: 1px; border: none;"

        def setting_row(label_text, widget, val_label=None):
            row = QWidget(); row.setStyleSheet("background:transparent;")
            rl = QHBoxLayout(row); rl.setContentsMargins(0,0,0,0); rl.setSpacing(10)
            lbl = QLabel(label_text); lbl.setStyleSheet(_LABEL)
            rl.addWidget(lbl); rl.addStretch(); rl.addWidget(widget)
            if val_label: rl.addWidget(val_label)
            return row

        def divider():
            d = QFrame(); d.setFrameShape(QFrame.Shape.HLine)
            d.setStyleSheet(_DIVIDER); return d

        self._settings_stack = QStackedWidget()
        self._settings_stack.setStyleSheet("background: transparent;")

        pg0 = QWidget(); pg0.setStyleSheet("background:transparent;")
        pg0_layout = QVBoxLayout(pg0)
        pg0_layout.setSpacing(0); pg0_layout.setContentsMargins(16,12,16,12)

        scroll0 = QScrollArea(); scroll0.setWidgetResizable(True)
        scroll0.setStyleSheet("QScrollArea{border:none;background:transparent;} QScrollBar:vertical{background:#0d0d0d;width:4px;} QScrollBar::handle:vertical{background:#222;border-radius:2px;} QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{height:0;}")
        c0 = QWidget(); c0.setStyleSheet("background:transparent;")
        c0l = QVBoxLayout(c0); c0l.setSpacing(12); c0l.setContentsMargins(0,0,0,0)

        self._lbl_interval_val = QLabel("5s"); self._lbl_interval_val.setStyleSheet(_VAL)
        self._slider_interval = QSlider(Qt.Orientation.Horizontal)
        self._slider_interval.setRange(2, 30); self._slider_interval.setValue(5)
        self._slider_interval.setFixedWidth(140); self._slider_interval.setStyleSheet(_SLIDER_STYLE)
        self._slider_interval.valueChanged.connect(lambda v: (
            self._lbl_interval_val.setText(f"{v}s"),
            setattr(self, '_auto_interval', v)
        ))
        c0l.addWidget(setting_row("Auto Apply interval", self._slider_interval, self._lbl_interval_val))
        c0l.addWidget(divider())

        self._chk_autostart = QCheckBox(); self._chk_autostart.setStyleSheet(_CHK_STYLE)
        c0l.addWidget(setting_row("Auto Apply on startup", self._chk_autostart))
        c0l.addWidget(divider())

        self._chk_inject_launch = QCheckBox(); self._chk_inject_launch.setStyleSheet(_CHK_STYLE)
        c0l.addWidget(setting_row("Inject when Roblox launches", self._chk_inject_launch))
        c0l.addWidget(divider())

        self._chk_tray_startup = QCheckBox(); self._chk_tray_startup.setStyleSheet(_CHK_STYLE)
        c0l.addWidget(setting_row("Start minimized to tray", self._chk_tray_startup))
        c0l.addWidget(divider())

        self._chk_run_on_boot = QCheckBox(); self._chk_run_on_boot.setStyleSheet(_CHK_STYLE)
        self._chk_run_on_boot.toggled.connect(self._set_windows_startup)
        c0l.addWidget(setting_row("Run on Windows startup", self._chk_run_on_boot))
        c0l.addWidget(divider())

        self._chk_kill_clears = QCheckBox(); self._chk_kill_clears.setStyleSheet(_CHK_STYLE)
        self._chk_kill_clears.setChecked(False)
        c0l.addWidget(setting_row("Kill switch also clears flags.json", self._chk_kill_clears))
        c0l.addWidget(divider())

        self._chk_confirm_clear = QCheckBox(); self._chk_confirm_clear.setStyleSheet(_CHK_STYLE)
        self._chk_confirm_clear.setChecked(True)
        c0l.addWidget(setting_row("Confirm before Remove All", self._chk_confirm_clear))
        c0l.addWidget(divider())

        self._chk_show_count = QCheckBox(); self._chk_show_count.setStyleSheet(_CHK_STYLE)
        self._chk_show_count.setChecked(True)
        c0l.addWidget(setting_row("Show flag count in title bar", self._chk_show_count))
        c0l.addWidget(divider())

        lbl_kb = QLabel("KEYBINDS"); lbl_kb.setStyleSheet("color:#333;font-size:10px;font-weight:700;letter-spacing:2px;background:transparent;")
        c0l.addWidget(lbl_kb)

        _KB_BTN = "QPushButton{background:#111;border:1px solid #1e1e1e;border-radius:8px;color:#555;font-size:11px;padding:5px 12px;min-width:90px;} QPushButton:hover{border-color:#333;color:#aaa;}"

        self._binds = {"apply": None, "auto": None, "kill": None, "lagswitch": None}

        def bind_row(label, key):
            row = QWidget(); row.setStyleSheet("background:transparent;")
            rl = QHBoxLayout(row); rl.setContentsMargins(0,0,0,0); rl.setSpacing(8)
            lbl = QLabel(label); lbl.setStyleSheet("color:#888;font-size:12px;background:transparent;")
            btn = QPushButton("Not set")
            btn.setStyleSheet(_KB_BTN)
            btn.setCheckable(False)
            btn.clicked.connect(lambda _, k=key, b=btn: self._start_bind_capture(k, b))
            setattr(self, f'_bind_btn_{key}', btn)
            btn_reset = QPushButton("↺ Reset")
            btn_reset.setFixedWidth(62)
            btn_reset.setStyleSheet("QPushButton{background:#0d0d0d;border:1px solid #1a1a1a;border-radius:8px;color:#444;font-size:10px;padding:4px 6px;} QPushButton:hover{border-color:#444;color:#888;}")
            btn_reset.clicked.connect(lambda _, k=key, b=btn: self._clear_bind(k, b))
            rl.addWidget(lbl); rl.addStretch(); rl.addWidget(btn_reset); rl.addWidget(btn)
            return row

        c0l.addWidget(bind_row("Apply to Roblox", "apply"))
        c0l.addWidget(divider())
        c0l.addWidget(bind_row("Auto Apply ON/OFF", "auto"))
        c0l.addWidget(divider())
        c0l.addWidget(bind_row("Kill Switch", "kill"))
        c0l.addWidget(divider())
        c0l.addWidget(bind_row("Lag Switch", "lagswitch"))
        c0l.addWidget(divider())

        _LS_SECTION = "color: #444444; font-size: 10px; font-weight: 700; letter-spacing: 2px; background: transparent;"
        ls_title = QLabel("LAG SWITCH"); ls_title.setStyleSheet(_LS_SECTION)
        c0l.addWidget(ls_title)

        self._lbl_ls_fps = QLabel("15"); self._lbl_ls_fps.setStyleSheet(_VAL)
        self._slider_ls_fps = QSlider(Qt.Orientation.Horizontal)
        self._slider_ls_fps.setRange(1, 60); self._slider_ls_fps.setValue(15)
        self._slider_ls_fps.setFixedWidth(140); self._slider_ls_fps.setStyleSheet(_SLIDER_STYLE)
        self._slider_ls_fps.valueChanged.connect(lambda v: self._lbl_ls_fps.setText(str(v)))
        c0l.addWidget(setting_row("Drop to FPS", self._slider_ls_fps, self._lbl_ls_fps))
        c0l.addWidget(divider())

        self._lbl_ls_dur = QLabel("0.7s"); self._lbl_ls_dur.setStyleSheet(_VAL)
        self._slider_ls_dur = QSlider(Qt.Orientation.Horizontal)
        self._slider_ls_dur.setRange(1, 30); self._slider_ls_dur.setValue(7)
        self._slider_ls_dur.setFixedWidth(140); self._slider_ls_dur.setStyleSheet(_SLIDER_STYLE)
        self._slider_ls_dur.valueChanged.connect(lambda v: self._lbl_ls_dur.setText(f"{v/10:.1f}s"))
        c0l.addWidget(setting_row("Duration", self._slider_ls_dur, self._lbl_ls_dur))
        c0l.addWidget(divider())

        lbl_diag = QLabel("DIAGNOSTICS")
        lbl_diag.setStyleSheet("color:#333;font-size:10px;font-weight:700;letter-spacing:2px;background:transparent;")
        c0l.addWidget(lbl_diag)
        btn_status_win = QPushButton("Injector Status")
        btn_status_win.setStyleSheet(_DLG_BTN)
        btn_status_win.setFixedWidth(180)
        btn_status_win.clicked.connect(self._open_status_window)
        c0l.addWidget(setting_row("View injection log & stats", btn_status_win))

        c0l.addStretch()

        scroll0.setWidget(c0); pg0_layout.addWidget(scroll0)
        self._settings_stack.addWidget(pg0)

        pg1 = QWidget(); pg1.setStyleSheet("background:transparent;")
        pg1_layout = QVBoxLayout(pg1)
        pg1_layout.setSpacing(0); pg1_layout.setContentsMargins(16,12,16,12)

        scroll1 = QScrollArea(); scroll1.setWidgetResizable(True)
        scroll1.setStyleSheet(scroll0.styleSheet())
        c1 = QWidget(); c1.setStyleSheet("background:transparent;")
        c1l = QVBoxLayout(c1); c1l.setSpacing(12); c1l.setContentsMargins(0,0,0,0)

        lbl_s1 = QLabel("SHIMMER"); lbl_s1.setStyleSheet("color:#333;font-size:10px;font-weight:700;letter-spacing:2px;background:transparent;")
        c1l.addWidget(lbl_s1)

        self._lbl_shim_val = QLabel("normal"); self._lbl_shim_val.setStyleSheet(_VAL)
        self._slider_shim = QSlider(Qt.Orientation.Horizontal)
        self._slider_shim.setRange(1, 5); self._slider_shim.setValue(3)
        self._slider_shim.setFixedWidth(140); self._slider_shim.setStyleSheet(_SLIDER_STYLE)
        speed_map = {1:"very slow", 2:"slow", 3:"normal", 4:"fast", 5:"very fast"}
        speed_vals = {1: 0.001, 2: 0.002, 3: 0.004, 4: 0.008, 5: 0.014}
        def _on_shim_change(v):
            self._lbl_shim_val.setText(speed_map.get(v, "normal"))
            lbl = self.findChild(TitleLabel)
            if lbl: lbl._tick_speed = speed_vals.get(v, 0.004)
        self._slider_shim.valueChanged.connect(_on_shim_change)
        c1l.addWidget(setting_row("Speed", self._slider_shim, self._lbl_shim_val))
        c1l.addWidget(divider())

        self._shimmer_text_color = QColor(220, 220, 220)
        self._btn_shim_text = QPushButton("  ████  Text color")
        self._btn_shim_text.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:#888;font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;color:#fff;}}")
        self._update_shim_btn_preview()
        self._btn_shim_text.clicked.connect(self._pick_shimmer_text_color)
        c1l.addWidget(setting_row("Title text color", self._btn_shim_text))
        c1l.addWidget(divider())

        self._shimmer_dark_color = QColor(25, 25, 25)
        self._btn_shim_dark = QPushButton("  ████  Dark gradient")
        self._btn_shim_dark.setStyleSheet(self._btn_shim_text.styleSheet())
        self._update_shim_dark_btn_preview()
        self._btn_shim_dark.clicked.connect(self._pick_shimmer_dark_color)
        c1l.addWidget(setting_row("Shimmer dark color", self._btn_shim_dark))
        c1l.addWidget(divider())

        lbl_s2 = QLabel("THEME"); lbl_s2.setStyleSheet(lbl_s1.styleSheet())
        c1l.addWidget(lbl_s2)

        self._theme_accent = QColor(255, 255, 255)
        self._btn_accent = QPushButton("  ████  Accent color")
        self._btn_accent.setStyleSheet(self._btn_shim_text.styleSheet())
        self._update_accent_btn_preview()
        self._btn_accent.clicked.connect(self._pick_accent_color)
        c1l.addWidget(setting_row("Button accent", self._btn_accent))
        c1l.addWidget(divider())

        self._btn_color = QPushButton("  ████  Button color")
        self._btn_color.setStyleSheet(self._btn_shim_text.styleSheet())
        self._btn_color_val = QColor(20, 20, 20)
        self._update_btn_color_preview()
        self._btn_color.clicked.connect(self._pick_btn_color)
        c1l.addWidget(setting_row("Button background", self._btn_color))
        c1l.addWidget(divider())

        lbl_s3 = QLabel("BACKGROUND"); lbl_s3.setStyleSheet(lbl_s1.styleSheet())
        c1l.addWidget(lbl_s3)

        self._bg_path = ""
        bg_row = QWidget(); bg_row.setStyleSheet("background:transparent;")
        bg_rl = QHBoxLayout(bg_row); bg_rl.setContentsMargins(0,0,0,0); bg_rl.setSpacing(8)
        self._lbl_bg_path = QLabel("No image selected")
        self._lbl_bg_path.setStyleSheet("color:#444;font-size:11px;background:transparent;")
        self._lbl_bg_path.setWordWrap(True)
        btn_pick_bg = QPushButton("Browse…")
        btn_pick_bg.setFixedWidth(80)
        btn_pick_bg.setStyleSheet("QPushButton{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:#888;font-size:12px;padding:4px 10px;} QPushButton:hover{border-color:#444;color:#fff;}")
        btn_pick_bg.clicked.connect(self._pick_background)
        btn_clear_bg = QPushButton("Clear")
        btn_clear_bg.setFixedWidth(54)
        btn_clear_bg.setStyleSheet(btn_pick_bg.styleSheet())
        btn_clear_bg.clicked.connect(self._clear_background)
        bg_rl.addWidget(self._lbl_bg_path)
        bg_rl.addStretch()
        bg_rl.addWidget(btn_pick_bg)
        bg_rl.addWidget(btn_clear_bg)
        c1l.addWidget(bg_row)
        c1l.addWidget(divider())

        self._lbl_bg_opacity = QLabel("60%"); self._lbl_bg_opacity.setStyleSheet(_VAL)
        self._slider_bg_opacity = QSlider(Qt.Orientation.Horizontal)
        self._slider_bg_opacity.setRange(10, 100); self._slider_bg_opacity.setValue(60)
        self._slider_bg_opacity.setFixedWidth(140); self._slider_bg_opacity.setStyleSheet(_SLIDER_STYLE)
        self._slider_bg_opacity.valueChanged.connect(lambda v: (
            self._lbl_bg_opacity.setText(f"{v}%"),
            self._apply_background(),
            self._save_app_settings()
        ))
        c1l.addWidget(setting_row("Background opacity", self._slider_bg_opacity, self._lbl_bg_opacity))
        c1l.addWidget(divider())

        self._bg_solid_color = QColor(13, 13, 13)
        self._btn_bg_color = QPushButton("  ████  Background color")
        self._btn_bg_color.setStyleSheet("QPushButton{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:#888;font-size:12px;padding:5px 12px;} QPushButton:hover{border-color:#444;color:#fff;}")
        self._btn_bg_color.clicked.connect(self._pick_bg_color)
        c1l.addWidget(setting_row("Solid color (no image)", self._btn_bg_color))
        c1l.addWidget(divider())

        lbl_revert = QLabel("RESET"); lbl_revert.setStyleSheet(lbl_s1.styleSheet())
        c1l.addWidget(lbl_revert)
        btn_revert = QPushButton("↺  Revert All to Default")
        btn_revert.setStyleSheet("""
            QPushButton { background: #1a0000; color: #cc3333;
                          border: 1px solid #440000; border-radius: 8px;
                          padding: 6px 18px; font-size: 12px; }
            QPushButton:hover { background: #220000; border-color: #882222; color: #ff4444; }
            QPushButton:pressed { background: #1a0000; }
        """)
        btn_revert.clicked.connect(self._revert_app_settings)
        c1l.addWidget(btn_revert)
        c1l.addWidget(divider())

        lbl_s_colors = QLabel("COLORS"); lbl_s_colors.setStyleSheet(lbl_s1.styleSheet())
        c1l.addWidget(lbl_s_colors)

        self._flag_name_color = QColor(126, 184, 247)
        self._btn_flag_color = QPushButton("  ████  Flag name color")
        self._btn_flag_color.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:rgb(126,184,247);font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")
        self._btn_flag_color.clicked.connect(self._pick_flag_color)
        c1l.addWidget(setting_row("FFlag name color", self._btn_flag_color))
        c1l.addWidget(divider())

        self._general_text_color = QColor(187, 187, 187)
        self._btn_text_color = QPushButton("  ████  General text")
        self._btn_text_color.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:#bbbbbb;font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")
        self._btn_text_color.clicked.connect(self._pick_general_text_color)
        c1l.addWidget(setting_row("General text color", self._btn_text_color))
        c1l.addWidget(divider())

        self._value_text_color = QColor(232, 232, 232)
        self._btn_value_color = QPushButton("  ████  Value color")
        self._btn_value_color.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:#e8e8e8;font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")
        self._btn_value_color.clicked.connect(self._pick_value_color)
        c1l.addWidget(setting_row("Value text color", self._btn_value_color))
        c1l.addWidget(divider())

        lbl_s_title = QLabel("TITLE BAR"); lbl_s_title.setStyleSheet(lbl_s1.styleSheet())
        c1l.addWidget(lbl_s_title)

        title_row = QWidget(); title_row.setStyleSheet("background:transparent;")
        title_rl = QHBoxLayout(title_row); title_rl.setContentsMargins(0,0,0,0); title_rl.setSpacing(8)
        lbl_title_edit = QLabel("Title text"); lbl_title_edit.setStyleSheet("color:#888;font-size:12px;background:transparent;")
        self._edit_title = QLineEdit("✟  SacredWare")
        self._edit_title.setFixedWidth(220)
        self._edit_title.setStyleSheet("QLineEdit{background:#111;border:1px solid #222;border-radius:8px;color:#ccc;padding:5px 10px;font-size:14px;} QLineEdit:focus{border-color:#444;}")
        self._edit_title.textChanged.connect(self._update_title_text)
        self._edit_cross = None
        title_rl.addWidget(lbl_title_edit); title_rl.addStretch(); title_rl.addWidget(self._edit_title)
        c1l.addWidget(title_row)
        c1l.addWidget(divider())

        lbl_s4 = QLabel("OTHER"); lbl_s4.setStyleSheet(lbl_s1.styleSheet())
        c1l.addWidget(lbl_s4)

        self._chk_compact = QCheckBox(); self._chk_compact.setStyleSheet(_CHK_STYLE)
        self._chk_compact.toggled.connect(self._apply_compact_mode)
        c1l.addWidget(setting_row("Compact row height", self._chk_compact))
        c1l.addWidget(divider())

        self._chk_show_type = QCheckBox(); self._chk_show_type.setStyleSheet(_CHK_STYLE)
        self._chk_show_type.setChecked(True)
        self._chk_show_type.toggled.connect(lambda v: self.table.setColumnHidden(2, not v))
        c1l.addWidget(setting_row("Show TYPE column", self._chk_show_type))
        c1l.addWidget(divider())

        self._chk_alt_rows = QCheckBox(); self._chk_alt_rows.setStyleSheet(_CHK_STYLE)
        self._chk_alt_rows.toggled.connect(lambda v: self.table.setAlternatingRowColors(v))
        c1l.addWidget(setting_row("Alternating row colors", self._chk_alt_rows))
        c1l.addStretch()

        scroll1.setWidget(c1); pg1_layout.addWidget(scroll1)
        self._settings_stack.addWidget(pg1)

        pg2_inner = QWidget(); pg2_inner.setStyleSheet("background:transparent;")
        pg2_layout = QVBoxLayout(pg2_inner)
        pg2_layout.setSpacing(6); pg2_layout.setContentsMargins(14,10,14,10)

        pg2_scroll = QScrollArea(); pg2_scroll.setWidgetResizable(True)
        pg2_scroll.setStyleSheet("QScrollArea{background:transparent;border:none;} QScrollBar:vertical{background:#0d0d0d;width:5px;border-radius:3px;} QScrollBar::handle:vertical{background:#2a2a2a;border-radius:3px;} QScrollBar::handle:vertical:hover{background:#444;}")
        pg2_scroll.setWidget(pg2_inner)

        _tag_colors = {"MAIN":"#4a8fd4","PERF":"#cc8833","FPS":"#44aa44","NET":"#9955cc","CFG":"#d4914a","FUN":"#cc4488","USR":"#dd7744"}

        _CAT_ORDER = [
            ('USR',  'User Configs'),
            ('FPS',  'FPS FFlags'),
            ('NET',  'Ping FFlags'),
            ('PERF', 'Performance FFlags'),
            ('CFG',  'Config FFlags'),
            ('FUN',  'Fun FFlags'),
            ('MAIN', 'Featured'),
        ]

        from collections import defaultdict
        cat_presets = defaultdict(list)
        for preset in BUILTIN_PRESETS:
            cat_presets[preset.get('tag', 'CFG')].append(preset)

        cat_tab_bar = QWidget()
        cat_tab_bar.setStyleSheet("background:transparent;")
        cat_tab_bar.setFixedHeight(38)
        ctbl = QHBoxLayout(cat_tab_bar)
        ctbl.setContentsMargins(0, 0, 0, 6)
        ctbl.setSpacing(4)

        _CAT_OFF = """QPushButton {
            background: transparent;
            color: #555555;
            border: 1px solid #2a2a2a;
            border-radius: 6px;
            padding:0 12px; outline:none; height:26px;
            font-size: 11px;
        }
        QPushButton:hover { color: #cccccc; border-color: #444444; }
        QPushButton:focus { outline:none; }"""

        cat_stack = QStackedWidget()
        cat_stack.setStyleSheet("background:transparent;")

        cat_tab_btns = []

        active_cats = [(tag, lbl) for tag, lbl in _CAT_ORDER if tag in cat_presets]

        for i, (tag, lbl) in enumerate(active_cats):
            tc = _tag_colors.get(tag, "#888")
            _CAT_ON = f"""QPushButton {{
                background:rgba(0,0,0,0.4); border:1px solid {tc};
                border-radius:6px; color:{tc}; font-size:11px; font-weight:600;
                padding:0 12px; outline:none; height:26px;
            }}
            QPushButton:focus {{ outline:none; }}"""

            btn = QPushButton(lbl)
            btn.setFixedHeight(26)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(_CAT_OFF)
            btn.setProperty("transparent", True)
            ctbl.addWidget(btn)
            cat_tab_btns.append((btn, _CAT_OFF, _CAT_ON))

            inner = QWidget(); inner.setStyleSheet("background:transparent;")
            inner_l = QVBoxLayout(inner)
            inner_l.setSpacing(6); inner_l.setContentsMargins(0,0,0,0)

            for preset in cat_presets[tag]:
                card = QWidget()
                card.setStyleSheet("""QWidget {
                    background: rgba(15,15,15,0.85);
                    border: 1px solid #2a2a2a;
                }
                QWidget:hover { border-color: #333333; background: rgba(22,22,22,0.9); }""")
                card.setCursor(Qt.CursorShape.PointingHandCursor)
                card.setFixedHeight(62)
                cl = QHBoxLayout(card)
                cl.setContentsMargins(14, 0, 14, 0); cl.setSpacing(12)

                text_col = QVBoxLayout(); text_col.setSpacing(2); text_col.setContentsMargins(0,0,0,0)
                name_lbl = QLabel(preset["name"])
                name_lbl.setStyleSheet("color:#e8e8e8; font-size:13px; font-weight:700; background:transparent; border:none;")
                desc_lbl = QLabel(preset["desc"])
                desc_lbl.setStyleSheet("color:#444444; font-size:10px; background:transparent; border:none;")
                text_col.addWidget(name_lbl); text_col.addWidget(desc_lbl)
                cl.addLayout(text_col); cl.addStretch()

                apply_btn = QPushButton("Add →")
                apply_btn.setFixedSize(76, 28)
                apply_btn.setStyleSheet(f"""QPushButton {{
                    background:transparent; border:1px solid #2a2a2a;
                    border-radius:7px; color: #cccccc; font-size:11px;
                }}
                QPushButton:hover {{ background:rgba(255,255,255,0.06); border-color:{tc}; color:{tc}; }}""")
                apply_btn.clicked.connect(lambda _, p=preset: self._apply_builtin_preset(p))
                card.mousePressEvent = lambda e, p=preset: self._apply_builtin_preset(p)
                cl.addWidget(apply_btn)
                inner_l.addWidget(card)

            inner_l.addStretch()
            scroll = QScrollArea(); scroll.setWidgetResizable(True)
            scroll.setStyleSheet("QScrollArea{background:transparent;border:none;} QScrollBar:vertical{background:#0d0d0d;width:5px;border-radius:3px;} QScrollBar::handle:vertical{background:#2a2a2a;border-radius:3px;} QScrollBar::handle:vertical:hover{background:#444;}")
            scroll.setWidget(inner)
            cat_stack.addWidget(scroll)

            def _make_switch(ix, on_style, off_styles):
                def _sw():
                    cat_stack.setCurrentIndex(ix)
                    for j, (b, off, on) in enumerate(cat_tab_btns):
                        b.setStyleSheet(on if j == ix else off)
                return _sw
            btn.clicked.connect(_make_switch(i, _CAT_ON, _CAT_OFF))

        ctbl.addStretch()

        if cat_tab_btns:
            cat_tab_btns[0][0].setStyleSheet(cat_tab_btns[0][2])

        pg2_layout.addWidget(cat_tab_bar)
        pg2_layout.addWidget(cat_stack, 1)
        self._settings_stack.addWidget(pg2_scroll)

        layout.addWidget(self._settings_stack)

        page_cfg = QWidget(); page_cfg.setStyleSheet('background:transparent;')
        cfg_scroll = QScrollArea(); cfg_scroll.setWidgetResizable(True)
        cfg_scroll.setStyleSheet('QScrollArea{background:transparent;border:none;} QScrollBar:vertical{background:#111;width:6px;border-radius:3px;} QScrollBar::handle:vertical{background:#333;border-radius:3px;} QScrollBar::handle:vertical:hover{background:#555;}')
        cfg_scroll.setWidget(page_cfg)
        self._settings_stack.addWidget(cfg_scroll)
        c3l = QVBoxLayout(page_cfg)
        c3l.setContentsMargins(20, 16, 20, 16)
        c3l.setSpacing(14)

        def cfg_section(title):
            lbl = QLabel(title)
            lbl.setStyleSheet('color:#444444; font-size:10px; font-weight:700; letter-spacing:2px; background:transparent;')
            c3l.addWidget(lbl)

        _CFG_BTN = 'QPushButton{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:#cccccc;font-size:12px;font-weight:600;padding:10px 18px;}QPushButton:hover{background:#1e1e1e;border-color:#555;color:#fff;}QPushButton:pressed{background:#0d0d0d;}'
        _CFG_BTN_ACC = 'QPushButton{background:#0f1a0f;border:1px solid #2a4a2a;border-radius:8px;color:#55cc55;font-size:12px;font-weight:600;padding:10px 18px;}QPushButton:hover{background:#152415;border-color:#3a6a3a;color:#77ee77;}QPushButton:pressed{background:#0a120a;}'

        cfg_section('EXPORT')
        exp_info = QLabel('Export your current customisation as a .swcfg file.\nBackground image is embedded \u2014 anyone can import it.')
        exp_info.setStyleSheet('color:#555; font-size:11px; background:transparent;')
        exp_info.setWordWrap(True)
        c3l.addWidget(exp_info)
        self.btn_export_cfg = QPushButton('Export Config (.swcfg)')
        self.btn_export_cfg.clicked.connect(self._export_app_config)
        c3l.addWidget(self.btn_export_cfg)

        c3l.addSpacing(8)
        cfg_section('IMPORT')
        imp_info = QLabel('Import a .swcfg config shared by someone else.\nThis will replace your current customisation.')
        imp_info.setStyleSheet('color:#555; font-size:11px; background:transparent;')
        imp_info.setWordWrap(True)
        c3l.addWidget(imp_info)
        self.btn_import_cfg = QPushButton('Import Config (.swcfg)')
        self.btn_import_cfg.clicked.connect(self._import_app_config)
        c3l.addWidget(self.btn_import_cfg)

        c3l.addSpacing(8)
        cfg_section('SAVED CONFIGS')
        saved_info = QLabel('Your exported configs are saved in the configs folder. Share the .swcfg file.')
        saved_info.setStyleSheet('color:#555; font-size:11px; background:transparent;')
        saved_info.setWordWrap(True)
        c3l.addWidget(saved_info)
        self._cfg_saved_label = QLabel('No configs saved yet.')
        self._cfg_saved_label.setStyleSheet('color:#333; font-size:11px; background:transparent;')
        c3l.addWidget(self._cfg_saved_label)
        self.btn_open_cfg_folder = QPushButton('Open Configs Folder')
        self.btn_open_cfg_folder.clicked.connect(self._open_configs_folder)
        c3l.addWidget(self.btn_open_cfg_folder)
        c3l.addStretch()
        self._refresh_cfg_list()

        page_mods = QWidget(); page_mods.setStyleSheet('background:transparent;')
        mods_scroll = QScrollArea(); mods_scroll.setWidgetResizable(True)
        mods_scroll.setStyleSheet('QScrollArea{background:transparent;border:none;} QScrollBar:vertical{background:#111;width:6px;border-radius:3px;} QScrollBar::handle:vertical{background:#333;border-radius:3px;} QScrollBar::handle:vertical:hover{background:#555;}')
        mods_scroll.setWidget(page_mods)
        self._settings_stack.addWidget(mods_scroll)
        m_layout = QVBoxLayout(page_mods)
        m_layout.setContentsMargins(20, 16, 20, 16)
        m_layout.setSpacing(14)

        def mods_section(title):
            lbl = QLabel(title)
            lbl.setStyleSheet('color:#444444; font-size:10px; font-weight:700; letter-spacing:2px; background:transparent;')
            m_layout.addWidget(lbl)

        _MOD_BTN  = 'QPushButton{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:#cccccc;font-size:12px;font-weight:600;padding:10px 18px;}QPushButton:hover{background:#1e1e1e;border-color:#555;color:#fff;}QPushButton:pressed{background:#0d0d0d;}'
        _MOD_BTN_DANGER = 'QPushButton{background:#1a0a0a;border:1px solid #3a1a1a;border-radius:8px;color:#cc4444;font-size:12px;font-weight:600;padding:6px 14px;}QPushButton:hover{background:#220d0d;border-color:#cc4444;color:#ff6666;}'

        mods_section('CUSTOM CURSOR')
        cur_info = QLabel('Replace the Roblox in-game cursor with a custom .png image.')
        cur_info.setStyleSheet('color:#555; font-size:11px; background:transparent;')
        cur_info.setWordWrap(True)
        m_layout.addWidget(cur_info)

        cur_preview_row = QHBoxLayout(); cur_preview_row.setSpacing(12)
        self._cursor_preview = QLabel()
        self._cursor_preview.setFixedSize(48, 48)
        self._cursor_preview.setStyleSheet('background:#111; border:1px solid #222; border-radius:8px;')
        self._cursor_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._cursor_status = QLabel('No cursor set')
        self._cursor_status.setStyleSheet('color:#444; font-size:11px; background:transparent;')
        self._cursor_status.setWordWrap(True)
        cur_preview_row.addWidget(self._cursor_preview)
        cur_preview_row.addWidget(self._cursor_status)
        cur_preview_row.addStretch()
        m_layout.addLayout(cur_preview_row)

        cur_btn_row = QHBoxLayout(); cur_btn_row.setSpacing(8)
        self.btn_set_cursor = QPushButton('Choose Cursor (.png)')
        self.btn_set_cursor.setStyleSheet(_MOD_BTN)
        self.btn_set_cursor.clicked.connect(self._pick_cursor)
        btn_cursor_presets = QPushButton('Presets ▾')
        btn_cursor_presets.setFixedWidth(90)
        btn_cursor_presets.setStyleSheet(_MOD_BTN)
        btn_cursor_presets.clicked.connect(self._open_cursor_presets_menu)
        btn_clear_cursor = QPushButton('Clear')
        btn_clear_cursor.setFixedWidth(70)
        btn_clear_cursor.setStyleSheet(_MOD_BTN_DANGER)
        btn_clear_cursor.clicked.connect(self._clear_cursor)
        cur_btn_row.addWidget(self.btn_set_cursor)
        cur_btn_row.addWidget(btn_cursor_presets)
        cur_btn_row.addWidget(btn_clear_cursor)
        m_layout.addLayout(cur_btn_row)

        m_layout.addSpacing(10)

        mods_section('CUSTOM FONT')
        font_info = QLabel('Replace the default Roblox UI font with a custom .ttf or .otf font.')
        font_info.setStyleSheet('color:#555; font-size:11px; background:transparent;')
        font_info.setWordWrap(True)
        m_layout.addWidget(font_info)

        font_preview_row = QHBoxLayout(); font_preview_row.setSpacing(12)
        self._font_preview = QLabel('Aa')
        self._font_preview.setFixedSize(48, 48)
        self._font_preview.setStyleSheet('background:#111; border:1px solid #222; border-radius:8px; color:#666; font-size:18px;')
        self._font_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._font_status = QLabel('No font set')
        self._font_status.setStyleSheet('color:#444; font-size:11px; background:transparent;')
        self._font_status.setWordWrap(True)
        font_preview_row.addWidget(self._font_preview)
        font_preview_row.addWidget(self._font_status)
        font_preview_row.addStretch()
        m_layout.addLayout(font_preview_row)

        font_btn_row = QHBoxLayout(); font_btn_row.setSpacing(8)
        self.btn_set_font = QPushButton('Choose Font (.ttf / .otf)')
        self.btn_set_font.setStyleSheet(_MOD_BTN)
        self.btn_set_font.clicked.connect(self._pick_font)
        btn_clear_font = QPushButton('Clear')
        btn_clear_font.setFixedWidth(70)
        btn_clear_font.setStyleSheet(_MOD_BTN_DANGER)
        btn_clear_font.clicked.connect(self._clear_font)
        font_btn_row.addWidget(self.btn_set_font)
        font_btn_row.addWidget(btn_clear_font)
        m_layout.addLayout(font_btn_row)

        m_layout.addSpacing(10)

        mods_section('HOW IT WORKS')
        how_info = QLabel(
            'Custom cursor and font are applied by copying files into the active '
            'Roblox installation folder.\n\n'
            'Cursor saves as: content/textures/Cursors/KeyboardMouse/ArrowFarCursor.png\n'
            'Font saves as: content/fonts/CustomFont.ttf (mapped via ClientSettings)\n\n'
            'Click Apply Mods to Roblox to write the files. '
            'Click Clear to remove them and restore defaults.'
        )
        how_info.setStyleSheet('color:#3a3a3a; font-size:10px; background:transparent; line-height:1.6;')
        how_info.setWordWrap(True)
        m_layout.addWidget(how_info)

        m_layout.addSpacing(8)
        self.btn_apply_mods = QPushButton('Apply Mods to Roblox')
        self.btn_apply_mods.setStyleSheet(
            'QPushButton{background:#0f1a0f;border:1px solid #2a4a2a;border-radius:8px;'
            'color:#55cc55;font-size:12px;font-weight:700;padding:11px 18px;}'
            'QPushButton:hover{background:#152415;border-color:#3a6a3a;color:#77ee77;}'
            'QPushButton:pressed{background:#0a120a;}'
        )
        self.btn_apply_mods.clicked.connect(self._apply_mods)
        m_layout.addWidget(self.btn_apply_mods)

        m_layout.addSpacing(10)
        mods_section('AUTO APPLY MODS')
        auto_info = QLabel(
            'Automatically apply cursor and font every time Roblox launches.\n'
            'Monitors for RobloxPlayerBeta.exe in the background.'
        )
        auto_info.setStyleSheet('color:#555; font-size:11px; background:transparent;')
        auto_info.setWordWrap(True)
        m_layout.addWidget(auto_info)

        self.btn_auto_mods = QPushButton('Auto Apply Mods: OFF')
        self.btn_auto_mods.setCheckable(True)
        self.btn_auto_mods.setStyleSheet(
            'QPushButton{background:#141414;border:1px solid #2a2a2a;border-radius:8px;'
            'color:#555;font-size:12px;font-weight:600;padding:10px 18px;outline:none;}'
            'QPushButton:hover{background:#1e1e1e;border-color:#444;color:#aaa;}'
            'QPushButton:checked{background:#0f1a0f;border:1px solid #2a4a2a;color:#55cc55;}'
            'QPushButton:checked:hover{background:#152415;border-color:#3a6a3a;color:#77ee77;}'
            'QPushButton:focus{outline:none;}'
        )
        self.btn_auto_mods.clicked.connect(self._toggle_auto_mods)
        m_layout.addWidget(self.btn_auto_mods)
        m_layout.addStretch()

        self._cursor_path   = ''
        self._font_path     = ''
        self._auto_mods_on  = False
        self._mods_watcher  = None
        self._load_mods_state()


        page_offsets = QWidget(); page_offsets.setStyleSheet('background:transparent;')
        off_layout = QVBoxLayout(page_offsets)
        off_layout.setContentsMargins(20, 20, 20, 20)
        off_layout.setSpacing(16)

        _SEC_LBL = 'color:#444444; font-size:10px; font-weight:700; letter-spacing:2px; background:transparent;'
        _INFO_LBL = 'color:#666666; font-size:11px; background:transparent;'

        sec_lbl = QLabel('OFFSET FILE'); sec_lbl.setStyleSheet(_SEC_LBL)
        off_layout.addWidget(sec_lbl)

        info = QLabel(
            'Drop a new fflags.json here to update offsets without rebuilding.\n'
            'SacredWare uses direct memory offsets from this file — update it\n'
            'each time Roblox updates to keep injection working.'
        )
        info.setStyleSheet(_INFO_LBL)
        info.setWordWrap(True)
        off_layout.addWidget(info)

        class _DropZone(QLabel):
            file_dropped = pyqtSignal(str)

            def __init__(self):
                super().__init__()
                self.setAcceptDrops(True)
                self.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setMinimumHeight(120)
                self._set_idle()

            def _set_idle(self):
                self.setText('Drop fflags.json here\nor click Browse')
                self.setStyleSheet(
                    'QLabel{background:#0d0d0d; border:2px dashed #2a2a2a; border-radius:12px;'
                    'color:#555555; font-size:12px; font-weight:600;}'
                )

            def _set_hover(self):
                self.setStyleSheet(
                    'QLabel{background:#111111; border:2px dashed #ffffff; border-radius:12px;'
                    'color:#cccccc; font-size:12px; font-weight:600;}'
                )

            def _set_ok(self, filename):
                self.setText(f'✓  Loaded: {filename}')
                self.setStyleSheet(
                    'QLabel{background:#0d1a0d; border:2px solid #2a4a2a; border-radius:12px;'
                    'color:#55cc55; font-size:12px; font-weight:600;}'
                )

            def _set_err(self, msg):
                self.setText(f'✗  {msg}')
                self.setStyleSheet(
                    'QLabel{background:#1a0d0d; border:2px solid #4a2a2a; border-radius:12px;'
                    'color:#cc5555; font-size:12px; font-weight:600;}'
                )

            def dragEnterEvent(self, e):
                if e.mimeData().hasUrls():
                    urls = e.mimeData().urls()
                    if any(u.toLocalFile().lower().endswith('.json') for u in urls):
                        e.acceptProposedAction()
                        self._set_hover()
                        return
                e.ignore()

            def dragLeaveEvent(self, e):
                self._set_idle()

            def dropEvent(self, e):
                self._set_idle()
                urls = e.mimeData().urls()
                for u in urls:
                    path = u.toLocalFile()
                    if path.lower().endswith('.json'):
                        self.file_dropped.emit(path)
                        return

        drop_zone = _DropZone()
        off_layout.addWidget(drop_zone)

        btn_row = QWidget(); btn_row.setStyleSheet('background:transparent;')
        btn_rl = QHBoxLayout(btn_row)
        btn_rl.setContentsMargins(0,0,0,0); btn_rl.setSpacing(8)

        _BTN_S = ('QPushButton{background:#141414;border:1px solid #2a2a2a;border-radius:8px;'
                  'color:#cccccc;font-size:12px;font-weight:600;padding:8px 16px;}'
                  'QPushButton:hover{background:#1e1e1e;border-color:#555;color:#fff;}')

        btn_browse_off = QPushButton('Browse fflags.json')
        btn_browse_off.setStyleSheet(_BTN_S)
        btn_browse_off.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_open_off_folder = QPushButton('Open Offsets Folder')
        btn_open_off_folder.setStyleSheet(_BTN_S)
        btn_open_off_folder.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_rl.addWidget(btn_browse_off)
        btn_rl.addWidget(btn_open_off_folder)
        btn_rl.addStretch()
        off_layout.addWidget(btn_row)

        self._off_status_lbl = QLabel()
        self._off_status_lbl.setStyleSheet('color:#555; font-size:11px; background:transparent;')
        self._off_status_lbl.setWordWrap(True)
        off_layout.addWidget(self._off_status_lbl)
        off_layout.addStretch()

        import os as _os
        import shutil as _shutil

        def _get_offsets_dir():
            import sys as _sys
            meipass = getattr(_sys, '_MEIPASS', None)
            if meipass:
                d = _os.path.join(meipass, 'offsets')
            else:
                d = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'offsets')
            _os.makedirs(d, exist_ok=True)
            return d

        def _update_off_status():
            d = _get_offsets_dir()
            f = _os.path.join(d, 'fflags.json')
            from core.injector import _FLAG_OFFSETS as _FFLAG_OFFSETS
            if _FFLAG_OFFSETS:
                self._off_status_lbl.setText(
                    f'Active offsets: {len(_FFLAG_OFFSETS):,} flags loaded\nFile: {f}'
                )
            else:
                self._off_status_lbl.setText('No offset file loaded. Drop fflags.json above.')

        def _load_offset_file(path):
            try:
                import json as _json
                with open(path, 'r', encoding='utf-8') as f:
                    d = _json.load(f)
                flags = d.get('FFlagOffsets', {}).get('FFlags', {})
                if not flags:
                    drop_zone._set_err('Not a valid fflags.json (no FFlags key)')
                    return
                dest_dir = _get_offsets_dir()
                dest = _os.path.join(dest_dir, 'fflags.json')
                _shutil.copy2(path, dest)
                from core import injector as _inj
                _inj._load_offset_table(dest)
                _inj._instance.flag_cache.clear()
                drop_zone._set_ok(f'{_os.path.basename(path)} ({len(flags):,} flags)')
                _update_off_status()
            except Exception as e:
                drop_zone._set_err(str(e)[:60])

        drop_zone.file_dropped.connect(_load_offset_file)

        def _browse_offset_file():
            from PyQt6.QtWidgets import QFileDialog as _FD
            path, _ = _FD.getOpenFileName(
                self, 'Select fflags.json', '', 'JSON files (*.json)')
            if path:
                _load_offset_file(path)

        def _open_offsets_folder():
            import subprocess
            d = _get_offsets_dir()
            subprocess.Popen(f'explorer "{d}"', shell=True)

        btn_browse_off.clicked.connect(_browse_offset_file)
        btn_open_off_folder.clicked.connect(_open_offsets_folder)
        _update_off_status()

        self._settings_stack.addWidget(page_offsets)

        self._settings_tab_bar = QWidget()
        self._settings_tab_bar.setStyleSheet(
            "background:rgba(10,10,10,0.95); border-top:1px solid #1a1a1a;"
        )
        self._settings_tab_bar.setFixedHeight(52)
        tbl = QHBoxLayout(self._settings_tab_bar)
        tbl.setContentsMargins(8, 6, 8, 6)
        tbl.setSpacing(2)

        _SVGS = {
            "GENERAL": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>''',
            "APPLICATION": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="10" height="10" rx="1"/><rect x="3" y="16" width="4" height="4" rx="0.5"/><rect x="10" y="16" width="4" height="4" rx="0.5"/><path d="M17 3h4v10h-4V3z"/><path d="M17 17l2-2 2 2-2 2-2-2z"/></svg>''',
            "PRESETS": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8H3a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h18a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1z"/><path d="M3 8l2 13h14l2-13"/><path d="M10 4V2M14 4V2"/><path d="M9 14h6M11 11v6"/></svg>''',
            "CONFIGS": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/><circle cx="15" cy="6" r="2" fill="{c}" stroke="none"/><circle cx="9" cy="12" r="2" fill="{c}" stroke="none"/><circle cx="16" cy="18" r="2" fill="{c}" stroke="none"/></svg>''',
            "MODS": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>''',
            "OFFSETS": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>''',
        }

        def _make_icon_pixmap(svg_key, color_hex, size=20):
            from PyQt6.QtSvg import QSvgRenderer
            from PyQt6.QtGui import QPixmap, QPainter as _P
            svg_str = _SVGS[svg_key].replace("{c}", color_hex)
            renderer = QSvgRenderer(svg_str.encode())
            px = QPixmap(size, size)
            px.fill(Qt.GlobalColor.transparent)
            p = _P(px)
            p.setRenderHint(_P.RenderHint.Antialiasing)
            renderer.render(p)
            p.end()
            return px

        _PILL_OFF_STYLE = """
            QPushButton {
                background: transparent; border: none; border-radius: 18px;
                padding: 0; outline: none;
            }
            QPushButton:hover { background: rgba(255,255,255,0.06); }
            QPushButton:focus { outline: none; }
        """
        _PILL_ON_STYLE = """
            QPushButton {
                background: #0d0d0d;
                padding: 0; outline: none;
            }
            QPushButton:focus { outline: none; }
        """

        _TAB_NAMES = ["GENERAL", "APPLICATION", "PRESETS", "CONFIGS", "MODS", "OFFSETS"]
        _COLOR_OFF  = "#555555"
        _COLOR_ON   = "#ffffff"

        tbl.addStretch()
        self._tab_btns   = []
        self._tab_labels = []
        self._tab_names_list = _TAB_NAMES
        self._make_tab_icon  = _make_icon_pixmap
        self._svgs_map       = _SVGS
        self._col_off        = _COLOR_OFF
        self._col_on         = _COLOR_ON

        for i, name in enumerate(_TAB_NAMES):
            tab_w = QWidget()
            tab_w.setStyleSheet("background:transparent;")
            tab_hl = QHBoxLayout(tab_w)
            tab_hl.setContentsMargins(2, 0, 2, 0)
            tab_hl.setSpacing(4)

            btn = QPushButton()
            btn.setCheckable(True)
            btn.setFixedSize(36, 36)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(_PILL_OFF_STYLE)
            btn.setIcon(QIcon(_make_icon_pixmap(name, _COLOR_OFF)))
            btn.setIconSize(QSize(20, 20))
            idx = i
            btn.clicked.connect(lambda _, ix=idx: self._switch_settings_tab(ix))
            tab_hl.addWidget(btn)

            lbl = QLabel(name)
            lbl.setStyleSheet(
                "color:#ffffff; font-size:10px; font-weight:700; "
                "background:transparent; letter-spacing:0.5px;"
            )
            lbl.hide()
            tab_hl.addWidget(lbl)

            tbl.addWidget(tab_w)
            self._tab_btns.append(btn)
            self._tab_labels.append(lbl)

        tbl.addStretch()

        btn_back = QPushButton("✕")
        btn_back.setFixedSize(28, 28)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setStyleSheet(
            "QPushButton{background:transparent;border:none;color:#333;font-size:12px;"
            "border-radius:6px;outline:none;}"
            "QPushButton:hover{color:#777;}"
            "QPushButton:focus{outline:none;}"
        )
        btn_back.clicked.connect(self._close_settings)
        tbl.addWidget(btn_back)

        self._tab_off_style = _PILL_OFF_STYLE
        self._tab_on_style  = _PILL_ON_STYLE
        self._switch_settings_tab(0)
        layout.addWidget(self._settings_tab_bar)

    def _update_shim_btn_preview(self):
        c = self._shimmer_text_color
        self._btn_shim_text.setText(f"  ████  Text color")
        self._btn_shim_text.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:rgb({c.red()},{c.green()},{c.blue()});font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")

    def _update_shim_dark_btn_preview(self):
        c = self._shimmer_dark_color
        self._btn_shim_dark.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:rgb({c.red()},{c.green()},{c.blue()});font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")

    def _update_accent_btn_preview(self):
        c = self._theme_accent
        self._btn_accent.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:rgb({c.red()},{c.green()},{c.blue()});font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")

    def _update_btn_color_preview(self):
        c = self._btn_color_val
        self._btn_color.setStyleSheet(f"QPushButton{{background:rgb({c.red()},{c.green()},{c.blue()});border:1px solid #2a2a2a;border-radius:8px;color:#aaaaaa;font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;color:#fff;}}")

    def _pick_shimmer_text_color(self):
        from PyQt6.QtWidgets import QColorDialog
        c = QColorDialog.getColor(self._shimmer_text_color, self, "Shimmer text color")
        if c.isValid():
            self._shimmer_text_color = c
            self._update_shim_btn_preview()
            lbl = self.findChild(TitleLabel)
            if lbl: lbl._text_color = c

    def _pick_shimmer_dark_color(self):
        from PyQt6.QtWidgets import QColorDialog
        c = QColorDialog.getColor(self._shimmer_dark_color, self, "Shimmer dark color")
        if c.isValid():
            self._shimmer_dark_color = c
            self._update_shim_dark_btn_preview()
            lbl = self.findChild(TitleLabel)
            if lbl: lbl._dark_color = c

    def _revert_app_settings(self):
        """Reset all APPLICATION settings to defaults."""
        self._tick_speed = 0.004
        self._slider_shim.setValue(3)
        lbl = self.findChild(TitleLabel)
        if lbl:
            lbl._tick_speed = 0.004
            lbl._text_color = QColor(220, 220, 220)
            lbl._dark_color  = QColor(25, 25, 25)
        self._shimmer_text_color = QColor(220, 220, 220)
        self._shimmer_dark_color = QColor(25, 25, 25)
        self._update_shim_btn_preview()
        self._update_shim_dark_btn_preview()
        self._theme_accent = QColor(255, 255, 255)
        self._btn_color_val = QColor(20, 20, 20)
        self._update_accent_btn_preview()
        self._update_btn_color_preview()
        self.btn_apply.setStyleSheet("""
            QPushButton { background-color: #161616;
                          border: 1px solid #cccccc;
                          color: #ffffff;
                          font-weight:700; border-radius:8px; padding:5px 14px; font-size:12px; }
            QPushButton:hover { background-color: #222222; border-color: #ffffff; }
            QPushButton:pressed { background-color: #1a1a1a; }
        """)
        _bs_default = """
            QPushButton { background-color: #141414; color: #aaaaaa;
                          border: 1px solid #2a2a2a;
                          border-radius:8px; padding:5px 14px; font-size:12px; font-weight:500; }
            QPushButton:hover { background-color: #1e1e1e; border-color: #444444; color: #ffffff; }
            QPushButton:pressed { background-color: #0d0d0d; }
        """
        for btn in [self.btn_add, self.btn_remove, self.btn_duplicate, self.btn_clear,
                    self.btn_import, self.btn_export, self.btn_presets,
                    self.btn_auto, self.btn_kill,
                        self.btn_export_cfg, self.btn_import_cfg, self.btn_open_cfg_folder]:
            btn.setStyleSheet(_bs_default)
        self._btn_color_val = QColor(20, 20, 20)
        self._update_auto_styles()
        self._bg_path = ""
        self._lbl_bg_path.setText("No image selected")
        self._bg_solid_color = QColor(13, 13, 13)
        self._btn_bg_color.setStyleSheet("QPushButton{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:#888;font-size:12px;padding:5px 12px;} QPushButton:hover{border-color:#444;color:#fff;}")
        self.centralWidget().setStyleSheet("border-radius:18px; background:#0d0d0d;")
        if getattr(self, '_bg_widget', None):
            self._bg_widget.hide()
        self._set_transparent_bg(False)
        self._slider_bg_opacity.setValue(60)
        self._flag_name_color = QColor(126, 184, 247)
        self._general_text_color = QColor(187, 187, 187)
        self._value_text_color = QColor(232, 232, 232)
        self._btn_flag_color.setStyleSheet("QPushButton{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:rgb(126,184,247);font-size:12px;padding:5px 12px;} QPushButton:hover{border-color:#444;}")
        self._btn_text_color.setStyleSheet("QPushButton{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:#bbbbbb;font-size:12px;padding:5px 12px;} QPushButton:hover{border-color:#444;}")
        self._btn_value_color.setStyleSheet("QPushButton{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:#e8e8e8;font-size:12px;padding:5px 12px;} QPushButton:hover{border-color:#444;}")
        self._repopulate_with_colors()
        self._chk_compact.setChecked(False)
        self._chk_show_type.setChecked(True)
        self._chk_alt_rows.setChecked(False)
        self._save_app_settings()
        self._set_status("Application settings reverted to default.")

    def _pick_bg_color(self):
        from PyQt6.QtWidgets import QColorDialog
        c = QColorDialog.getColor(self._bg_solid_color, self, "Background color")
        if c.isValid():
            self._bg_solid_color = c
            self._btn_bg_color.setStyleSheet(f"QPushButton{{background:rgb({c.red()},{c.green()},{c.blue()});border:1px solid #2a2a2a;border-radius:8px;color:#aaaaaa;font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")
            self._bg_path = ""
            self._lbl_bg_path.setText("No image selected")
            self.centralWidget().setStyleSheet(f"border-radius:18px; background:rgb({c.red()},{c.green()},{c.blue()});")

    def _pick_accent_color(self):
        from PyQt6.QtWidgets import QColorDialog
        c = QColorDialog.getColor(self._theme_accent, self, "Accent color")
        if c.isValid():
            self._theme_accent = c
            self._update_accent_btn_preview()
            self.btn_apply.setStyleSheet(f"""
                QPushButton {{
                    background-color: #141414;
                    border: 1px solid rgb({c.red()},{c.green()},{c.blue()});
                    color: rgb({c.red()},{c.green()},{c.blue()});
                    font-weight: 700; border-radius: 8px;
                    padding: 5px 14px; font-size: 12px;
                }}
                QPushButton:hover {{ background-color: #222222; border-color: rgb({min(c.red()+40,255)},{min(c.green()+40,255)},{min(c.blue()+40,255)}); color: #ffffff; }}
                QPushButton:pressed {{ background-color: #1a1a1a; }}
            """)

    def _pick_btn_color(self):
        from PyQt6.QtWidgets import QColorDialog
        c = QColorDialog.getColor(self._btn_color_val, self, "Button background color")
        if c.isValid():
            self._btn_color_val = c
            self._update_btn_color_preview()
            new_style = f"""
                QPushButton {{
                    background-color: rgb({c.red()},{c.green()},{c.blue()});
                    color: #cccccc;
                    border-radius: 8px; padding: 6px 14px; font-size: 13px; font-weight: 500;
                }}
                QPushButton:hover {{ background-color: rgb({min(c.red()+20,255)},{min(c.green()+20,255)},{min(c.blue()+20,255)}); border-color: #444444;
                QPushButton:pressed {{ background-color: rgb({max(c.red()-10,0)},{max(c.green()-10,0)},{max(c.blue()-10,0)}); }}
            """
            for btn in [self.btn_add, self.btn_remove, self.btn_duplicate, self.btn_clear,
                        self.btn_import, self.btn_export, self.btn_presets,
                        self.btn_auto, self.btn_kill,
                        self.btn_export_cfg, self.btn_import_cfg, self.btn_open_cfg_folder]:
                btn.setStyleSheet(new_style)
            self._update_auto_styles()

    def _pick_background(self):
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self, "Select background image", "",
                                               "Images (*.png *.jpg *.jpeg *.webp)")
        if path:
            self._bg_path = path
            import os
            self._lbl_bg_path.setText(os.path.basename(path))
            self._apply_background()
            self._save_app_settings()

    def _clear_background(self):
        self._bg_path = ""
        self._lbl_bg_path.setText("No image selected")
        if getattr(self, '_bg_widget', None):
            self._bg_widget.hide()
        self._set_transparent_bg(False)

    def _set_transparent_bg(self, transparent: bool):
        """Toggle transparency of all widgets to show/hide background image."""
        cw = self.centralWidget()
        _T = "rgba(0,0,0,0)"
        if transparent:
            cw.setStyleSheet("border-radius:18px; background:transparent;")
            self.table.setStyleSheet("""
                QTableWidget { background:transparent; gridline-color:rgba(0,0,0,0);
                               border:none; font-size:12px; color: #cccccc; }
                QTableWidget::item { padding:4px 10px; border-bottom:1px solid rgba(255,255,255,0.03); background:transparent; }
                QTableWidget::item:selected { background:rgba(255,255,255,0.1); color: #ffffff; }
                QHeaderView::section { background:rgba(0,0,0,0.3); color: #2a2a2a;
                                       font-size:9px; font-weight:600; letter-spacing:2px; padding:5px 10px;
                                       border:none; border-bottom:1px solid rgba(255,255,255,0.03); }
                QScrollBar:vertical { background:transparent; width:5px; }
                QScrollBar::handle:vertical { background:rgba(255,255,255,0.2); border-radius:3px; }
            """)
            if hasattr(self, 'search'):
                self.search.setStyleSheet("""
                    QLineEdit { background:rgba(0,0,0,0.35); border:1px solid rgba(255,255,255,0.1);
                                border-radius:8px; padding:6px 12px; color: #cccccc;
                    QLineEdit:focus { border-color:rgba(255,255,255,0.3); }
                """)
            if hasattr(self, '_search_bar'):
                self._search_bar.setStyleSheet("background:transparent; border-bottom:1px solid rgba(255,255,255,0.06);")
            if hasattr(self, '_bottom_bar'):
                self._bottom_bar.setStyleSheet("background:transparent; border-top:1px solid rgba(255,255,255,0.06);")
            if hasattr(self, '_settings_tab_bar'):
                self._settings_tab_bar.setStyleSheet("background:rgba(0,0,0,0.5); border-top:1px solid rgba(255,255,255,0.06);")
            if hasattr(self, '_settings_stack'):
                for i in range(self._settings_stack.count()):
                    pg = self._settings_stack.widget(i)
                    if pg: pg.setStyleSheet("background:transparent;")
            _BTN_T = "QPushButton{background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.1);border-radius:8px;color:#aaa;font-size:12px;padding:5px 12px;} QPushButton:hover{border-color:rgba(255,255,255,0.3);color:#fff;}"
            for attr in ['_btn_shim_text','_btn_shim_dark','_btn_accent','_btn_color',
                         '_btn_flag_color','_btn_text_color','_btn_value_color',
                         '_btn_bg_color','_btn_pick_bg']:
                btn = getattr(self, attr, None)
                if btn: btn.setStyleSheet(_BTN_T)
            if hasattr(self, 'status_msg'):
                self.status_msg.setStyleSheet("color:#aaa; font-size:11px; background:transparent;")
            if hasattr(self, 'roblox_dot'):
                self.roblox_dot.setStyleSheet(self.roblox_dot.styleSheet().replace("background: transparent","background:transparent"))
            ac = getattr(self, '_theme_accent', QColor(255,255,255))
            self.btn_apply.setStyleSheet(f"""
                QPushButton {{ background:rgba(0,0,0,0.4); border:1px solid rgb({ac.red()},{ac.green()},{ac.blue()});
                               color:rgb({ac.red()},{ac.green()},{ac.blue()}); font-weight:700;
                               border-radius:8px; padding:5px 14px; font-size:12px; }}
                QPushButton:hover {{ background:rgba(255,255,255,0.15); color: #ffffff; }}
                QPushButton:pressed {{ background:rgba(0,0,0,0.6); }}
            """)
            self.btn_settings.setStyleSheet("""
                QPushButton { background:transparent; border:none;
                              color:rgba(255,255,255,0.4); font-size:15px; border-radius:8px; padding:0; outline:none; }
                QPushButton:hover { background:transparent; color:rgba(255,255,255,0.9); }
                QPushButton:checked { background:transparent; color: #cccccc; }
                QPushButton:focus { outline:none; }
            """)
            _bs_t = """
                QPushButton { background:rgba(0,0,0,0.35); color: #cccccc;
                              border:1px solid rgba(255,255,255,0.1); border-radius:8px;
                              padding:6px 14px; font-size:13px; font-weight:500; }
                QPushButton:hover { background:rgba(255,255,255,0.1); border-color:rgba(255,255,255,0.3); color: #cccccc;
                QPushButton:pressed { background:rgba(255,255,255,0.05); }
            """
            for btn in [self.btn_add, self.btn_remove, self.btn_duplicate, self.btn_clear,
                        self.btn_import, self.btn_export, self.btn_presets,
                        self.btn_auto, self.btn_kill,
                        self.btn_export_cfg, self.btn_import_cfg, self.btn_open_cfg_folder]:
                btn.setStyleSheet(_bs_t)
            self._update_auto_styles()
        else:
            cw.setStyleSheet("border-radius:18px; background:#0d0d0d;")
            self.table.setStyleSheet("")
            self.setStyleSheet(STYLE)
            if hasattr(self, '_search_bar'):
                self._search_bar.setStyleSheet("background:#0d0d0d; border-bottom:1px solid #141414;")
            if hasattr(self, '_bottom_bar'):
                self._bottom_bar.setStyleSheet("background:#090909; border-top:1px solid #1a1a1a;")
            if hasattr(self, '_settings_tab_bar'):
                self._settings_tab_bar.setStyleSheet("background:rgba(10,10,10,0.92); border-top:1px solid #1a1a1a;")
            if hasattr(self, '_settings_stack'):
                for i in range(self._settings_stack.count()):
                    pg = self._settings_stack.widget(i)
                    if pg: pg.setStyleSheet("background:transparent;")
            if hasattr(self, 'status_msg'):
                self.status_msg.setStyleSheet("color:#444444; font-size:11px; background:transparent;")
            if hasattr(self, 'search'):
                self.search.setStyleSheet("""
                    QLineEdit { background: #0d0d0d;
                                padding:6px 12px; color: #cccccc;
                    QLineEdit:focus { border-color: #444444;
                """)
            self._restore_apply_style()
            self.btn_settings.setStyleSheet("""
                QPushButton { background:transparent; border:none; color:rgba(255,255,255,0.35);
                              font-size:15px; border-radius:8px; padding:0; outline:none; }
                QPushButton:hover { background:transparent; color:rgba(255,255,255,0.8); }
                QPushButton:checked { background:transparent; color: #cccccc; }
                QPushButton:focus { outline:none; }
            """)
            c = getattr(self, '_btn_color_val', QColor(20, 20, 20))
            _bs_default = f"""
                QPushButton {{ background-color:rgb({c.red()},{c.green()},{c.blue()}); color: #cccccc;
                              border-radius:8px; padding:6px 14px; font-size:13px; font-weight:500; }}
                QPushButton:hover {{ background-color:rgb({min(c.red()+20,255)},{min(c.green()+20,255)},{min(c.blue()+20,255)}); border-color: #444444;
                QPushButton:pressed {{ background-color:rgb({max(c.red()-10,0)},{max(c.green()-10,0)},{max(c.blue()-10,0)}); }}
            """
            for btn in [self.btn_add, self.btn_remove, self.btn_duplicate, self.btn_clear,
                        self.btn_import, self.btn_export, self.btn_presets,
                        self.btn_auto, self.btn_kill,
                        self.btn_export_cfg, self.btn_import_cfg, self.btn_open_cfg_folder]:
                btn.setStyleSheet(_bs_default)
            self._update_auto_styles()

    def _apply_background(self):
        cw = self.centralWidget()
        if not self._bg_path:
            if getattr(self, '_bg_widget', None):
                self._bg_widget.hide()
            self._set_transparent_bg(False)
            return
        try:
            px = QPixmap(self._bg_path)
            if px.isNull():
                self._set_status(f"Cannot load: {self._bg_path}")
                return
            opacity = getattr(self, '_slider_bg_opacity', None)
            alpha = (opacity.value() / 100.0) if opacity else 0.6
            w, h = cw.width(), cw.height()
            if w <= 0 or h <= 0:
                w, h = self.width(), self.height()
            scaled = px.scaled(w, h,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation)
            ox = max(0, (scaled.width() - w) // 2)
            oy = max(0, (scaled.height() - h) // 2)
            cropped = scaled.copy(ox, oy, w, h)
            final = QPixmap(w, h)
            final.fill(QColor(13, 13, 13))
            rp = QPainter(final)
            rp.setOpacity(alpha)
            rp.drawPixmap(0, 0, cropped)
            rp.end()
            if not getattr(self, '_bg_widget', None):
                self._bg_widget = QLabel(cw)
                self._bg_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            self._bg_widget.setParent(cw)
            self._bg_widget.setPixmap(final)
            self._bg_widget.setGeometry(0, 0, w, h)
            self._bg_widget.lower()
            self._bg_widget.show()
            self._set_transparent_bg(True)
            self._set_status("Background applied.")
        except Exception as e:
            self._set_status(f"Background error: {e}")

    def _pick_flag_color(self):
        from PyQt6.QtWidgets import QColorDialog
        c = QColorDialog.getColor(self._flag_name_color, self, "FFlag name color")
        if c.isValid():
            self._flag_name_color = c
            self._btn_flag_color.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:rgb({c.red()},{c.green()},{c.blue()});font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")
            self._repopulate_with_colors()
        self._save_app_settings()

    def _pick_general_text_color(self):
        from PyQt6.QtWidgets import QColorDialog
        c = QColorDialog.getColor(self._general_text_color, self, "General text color")
        if c.isValid():
            self._general_text_color = c
            self._btn_text_color.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:rgb({c.red()},{c.green()},{c.blue()});font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")
            self.setStyleSheet(self.styleSheet())
            self._repopulate_with_colors()
        self._save_app_settings()

    def _pick_value_color(self):
        from PyQt6.QtWidgets import QColorDialog
        c = QColorDialog.getColor(self._value_text_color, self, "Value text color")
        if c.isValid():
            self._value_text_color = c
            self._btn_value_color.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:rgb({c.red()},{c.green()},{c.blue()});font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")
            self._repopulate_with_colors()
        self._save_app_settings()

    def _update_title_text(self):
        """Update TitleLabel text from combined title field."""
        edit = getattr(self, '_edit_title', None)
        if not edit:
            return
        text = edit.text() or "✟  SacredWare"
        lbl = self.findChild(TitleLabel)
        if lbl:
            lbl._text = text
        self._save_app_settings()

    def _start_bind_capture(self, key, btn):
        """Enter capture mode — shows mouse button picker or waits for key press."""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QAction

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background: #0d0d0d;
            QMenu::item { color: #cccccc;
            QMenu::item:selected { background: #0d0d0d;
            QMenu::separator { background: #0d0d0d;
        """)

        kb_action  = menu.addAction("⌨  Keyboard key")
        menu.addSeparator()
        m4_action  = menu.addAction("🖱  Mouse4 (side back)")
        m5_action  = menu.addAction("🖱  Mouse5 (side forward)")
        m3_action  = menu.addAction("🖱  Mouse3 (middle)")
        menu.addSeparator()
        cancel_action = menu.addAction("✕  Cancel")

        chosen = menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))

        if chosen == kb_action:
            btn.setText("Press key...")
            btn.setStyleSheet("QPushButton{background:#1a1a00;border:1px solid #555500;border-radius:8px;color:#ffff00;font-size:11px;padding:5px 12px;min-width:90px;}")
            self._capturing_bind = (key, btn)
            QApplication.instance().installEventFilter(self)
        elif chosen in (m3_action, m4_action, m5_action):
            bind_map = {m3_action: "Mouse3", m4_action: "Mouse4", m5_action: "Mouse5"}
            bind_str = bind_map[chosen]
            self._binds[key] = bind_str
            btn.setText(bind_str)
            btn.setStyleSheet("QPushButton{background:#001a00;border:1px solid #005500;border-radius:8px;color:#44ff44;font-size:11px;padding:5px 12px;min-width:90px;} QPushButton:hover{border-color:#00aa00;}")
            self._save_app_settings()
            self._update_hotkeys()

    @pyqtSlot()
    def _apply_capture_bind_str(self):
        """Called on main thread to apply a pending mouse bind during capture."""
        bind_str = getattr(self, '_pending_capture_bind', None)
        if not bind_str:
            return
        self._pending_capture_bind = None
        cap = getattr(self, '_capturing_bind', None)
        if not cap:
            return
        key_name, btn = cap
        self._binds[key_name] = bind_str
        btn.setText(bind_str)
        btn.setStyleSheet("QPushButton{background:#001a00;border:1px solid #005500;border-radius:8px;color:#44ff44;font-size:11px;padding:5px 12px;min-width:90px;} QPushButton:hover{border-color:#00aa00;}")
        self._capturing_bind = None
        QApplication.instance().removeEventFilter(self)
        cl = getattr(self, '_capture_mouse_listener', None)
        if cl:
            try: cl.stop()
            except: pass
        self._save_app_settings()
        self._update_hotkeys()

    def _clear_bind(self, key, btn):
        self._binds[key] = None
        btn.setText("Not set")
        btn.setStyleSheet("QPushButton{background:#111;border:1px solid #1e1e1e;border-radius:8px;color:#555;font-size:11px;padding:5px 12px;min-width:90px;} QPushButton:hover{border-color:#333;color:#aaa;}")
        self._save_app_settings()

    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        from PyQt6.QtGui import QKeyEvent, QMouseEvent
        cap = getattr(self, '_capturing_bind', None)
        if cap:
            key_name, btn = cap
            bind_str = None
            if event.type() == QEvent.Type.KeyPress:
                ke = event
                mod = ke.modifiers()
                k = ke.key()
                from PyQt6.QtCore import Qt as _Qt
                if k in (_Qt.Key.Key_Control, _Qt.Key.Key_Shift, _Qt.Key.Key_Alt,
                         _Qt.Key.Key_Meta, _Qt.Key.Key_AltGr):
                    return False
                _QT_KEY_MAP = {
                    _Qt.Key.Key_F1:'f1',_Qt.Key.Key_F2:'f2',_Qt.Key.Key_F3:'f3',
                    _Qt.Key.Key_F4:'f4',_Qt.Key.Key_F5:'f5',_Qt.Key.Key_F6:'f6',
                    _Qt.Key.Key_F7:'f7',_Qt.Key.Key_F8:'f8',_Qt.Key.Key_F9:'f9',
                    _Qt.Key.Key_F10:'f10',_Qt.Key.Key_F11:'f11',_Qt.Key.Key_F12:'f12',
                    _Qt.Key.Key_Up:'up',_Qt.Key.Key_Down:'down',
                    _Qt.Key.Key_Left:'left',_Qt.Key.Key_Right:'right',
                    _Qt.Key.Key_Return:'enter',_Qt.Key.Key_Enter:'enter',
                    _Qt.Key.Key_Escape:'esc',_Qt.Key.Key_Tab:'tab',
                    _Qt.Key.Key_Backspace:'backspace',_Qt.Key.Key_Delete:'delete',
                    _Qt.Key.Key_Insert:'insert',_Qt.Key.Key_Home:'home',
                    _Qt.Key.Key_End:'end',_Qt.Key.Key_PageUp:'page up',
                    _Qt.Key.Key_PageDown:'page down',_Qt.Key.Key_Space:'space',
                    _Qt.Key.Key_CapsLock:'caps lock',_Qt.Key.Key_NumLock:'num lock',
                }
                qt_key = _Qt.Key(k)
                if qt_key in _QT_KEY_MAP:
                    key_name_str = _QT_KEY_MAP[qt_key]
                elif ke.text().strip():
                    key_name_str = ke.text().lower()
                else:
                    key_name_str = qt_key.name.replace("Key_","").lower()
                parts = []
                if mod & _Qt.KeyboardModifier.AltModifier: parts.append("alt")
                if mod & _Qt.KeyboardModifier.ShiftModifier: parts.append("shift")
                if mod & _Qt.KeyboardModifier.ControlModifier: parts.append("ctrl")
                parts.append(key_name_str)
                bind_str = "+".join(parts)
            elif event.type() == QEvent.Type.MouseButtonPress:
                me = event
                btn_map = {
                    1: "Mouse1", 2: "Mouse2", 4: "Mouse3",
                }
                bind_str = btn_map.get(int(me.button()), None)

            if bind_str:
                self._binds[key_name] = bind_str
                btn.setText(bind_str)
                btn.setStyleSheet("QPushButton{background:#001a00;border:1px solid #005500;border-radius:8px;color:#44ff44;font-size:11px;padding:5px 12px;min-width:90px;} QPushButton:hover{border-color:#00aa00;}")
                self._capturing_bind = None
                QApplication.instance().removeEventFilter(self)
                self._save_app_settings()
                self._update_hotkeys()
                return True
        return False

    def _update_hotkeys(self):
        """Install GLOBAL hotkeys — works even when Roblox is focused.
        Supports keyboard keys AND mouse buttons (Mouse4, Mouse5 etc.)
        """
        for sc in getattr(self, '_shortcuts', []):
            try: sc.setEnabled(False); sc.deleteLater()
            except: pass
        self._shortcuts = []

        kb_stop_old = getattr(self, '_kb_hook_stop', None)
        if kb_stop_old:
            try: kb_stop_old.set()
            except: pass
        self._kb_hook_stop = None

        ml = getattr(self, '_mouse_listener', None)
        if ml:
            try: ml.stop()
            except: pass
        self._mouse_listener = None

        actions = {
            "apply":     self._apply_flags,
            "auto":      self._toggle_auto_apply,
            "kill":      self._kill_switch,
            "lagswitch": self._trigger_lagswitch,
        }

        mouse_binds = {}   # "Mouse4" -> action
        kb_binds    = {}   # "g" -> action

        for key, bind_str in self._binds.items():
            if not bind_str:
                continue
            action = actions.get(key)
            if not action:
                continue
            if bind_str.startswith("Mouse"):
                mouse_binds[bind_str] = action
            else:
                kb_binds[bind_str.lower()] = action

        import queue as _shared_queue
        import threading as _shared_threading
        _action_queue = _shared_queue.Queue()

        def _shared_action_worker():
            while True:
                try:
                    act = _action_queue.get(timeout=0.2)
                    if act is None:
                        break
                    act()
                except _shared_queue.Empty:
                    pass
                except Exception:
                    pass

        _worker_thread = _shared_threading.Thread(target=_shared_action_worker, daemon=True)
        _worker_thread.start()
        self._hotkey_action_queue   = _action_queue
        self._hotkey_worker_thread  = _worker_thread

        kb_stop = getattr(self, '_kb_hook_stop', None)
        if kb_stop:
            try: kb_stop.set()
            except: pass
        self._kb_hook_stop = None
        self._kb_sc_map = {}

        if kb_binds:
            import threading, ctypes, ctypes.wintypes as _wt

            _NAME_TO_VK = {
                'f1':0x70,'f2':0x71,'f3':0x72,'f4':0x73,'f5':0x74,'f6':0x75,
                'f7':0x76,'f8':0x77,'f9':0x78,'f10':0x79,'f11':0x7A,'f12':0x7B,
                'space':0x20,'enter':0x0D,'esc':0x1B,'escape':0x1B,'tab':0x09,
                'backspace':0x08,'delete':0x2E,'insert':0x2D,
                'home':0x24,'end':0x23,'page up':0x21,'page down':0x22,
                'up':0x26,'down':0x28,'left':0x25,'right':0x27,
                'caps lock':0x14,'num lock':0x90,'scroll lock':0x91,
                'shift':0x10,'ctrl':0x11,'alt':0x12,
                'left shift':0xA0,'right shift':0xA1,
                'left ctrl':0xA2,'right ctrl':0xA3,
                'left alt':0xA4,'right alt':0xA5,
                'num0':0x60,'num1':0x61,'num2':0x62,'num3':0x63,'num4':0x64,
                'num5':0x65,'num6':0x66,'num7':0x67,'num8':0x68,'num9':0x69,
            }

            u32_map = ctypes.WinDLL('user32', use_last_error=True)
            for hk, action in kb_binds.items():
                vk = None
                if len(hk) == 1:
                    res = u32_map.VkKeyScanW(ord(hk))
                    if res != -1:
                        vk = res & 0xFF
                else:
                    vk = _NAME_TO_VK.get(hk.lower())

                if vk is not None:
                    sc = u32_map.MapVirtualKeyW(vk, 0)
                    if sc:
                        self._kb_sc_map[sc] = action
                        print(f"[Hotkey] kb '{hk}' VK=0x{vk:02X} SC={sc}")
                    else:
                        self._kb_sc_map[('vk', vk)] = action
                        print(f"[Hotkey] kb '{hk}' VK=0x{vk:02X} (no SC, using VK)")
                else:
                    print(f"[Hotkey] kb '{hk}' — could not resolve VK, skipped")

            if self._kb_sc_map:
                kb_stop_evt = threading.Event()
                self._kb_hook_stop = kb_stop_evt
                _sc_map_ref = self._kb_sc_map   # capture by ref — dict won't be replaced
                _action_queue = self._hotkey_action_queue

                def _kb_hook_thread():
                    import ctypes, ctypes.wintypes as _wt, struct

                    u32 = ctypes.WinDLL('user32', use_last_error=True)

                    WH_KEYBOARD_LL = 13
                    WM_KEYDOWN     = 0x0100
                    WM_SYSKEYDOWN  = 0x0104

                    class KBDLLHOOKSTRUCT(ctypes.Structure):
                        _fields_ = [
                            ('vkCode',      _wt.DWORD),
                            ('scanCode',    _wt.DWORD),
                            ('flags',       _wt.DWORD),
                            ('time',        _wt.DWORD),
                            ('dwExtraInfo', ctypes.c_ulonglong),
                        ]

                    HOOKPROC = ctypes.WINFUNCTYPE(
                        ctypes.c_longlong,
                        ctypes.c_int,
                        ctypes.c_ulonglong,
                        ctypes.c_longlong,
                    )
                    u32.CallNextHookEx.restype  = ctypes.c_longlong
                    u32.CallNextHookEx.argtypes = [
                        ctypes.c_void_p, ctypes.c_int,
                        ctypes.c_ulonglong, ctypes.c_longlong,
                    ]

                    hook = [None]

                    def _proc(nCode, wParam, lParam):
                        try:
                            if nCode >= 0 and wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
                                kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
                                sc = kb.scanCode
                                vk = kb.vkCode
                                act = _sc_map_ref.get(sc) or _sc_map_ref.get(('vk', vk))
                                if act:
                                    _action_queue.put(act)
                        except Exception:
                            pass
                        return u32.CallNextHookEx(hook[0], nCode, wParam, lParam)

                    cb = HOOKPROC(_proc)
                    hook[0] = u32.SetWindowsHookExW(WH_KEYBOARD_LL, cb, None, 0)
                    if not hook[0]:
                        print(f"[Hotkey] kb hook failed err={ctypes.get_last_error()}")
                        return
                    print(f"[Hotkey] kb WH_KEYBOARD_LL hook OK, SC map: {list(_sc_map_ref.keys())}")

                    msg = _wt.MSG()
                    while not kb_stop_evt.is_set():
                        r = u32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1)
                        if r > 0:
                            u32.TranslateMessage(ctypes.byref(msg))
                            u32.DispatchMessageW(ctypes.byref(msg))
                        else:
                            kb_stop_evt.wait(0.005)

                    u32.UnhookWindowsHookEx(hook[0])
                    print("[Hotkey] kb hook removed")

                t = threading.Thread(target=_kb_hook_thread, daemon=True)
                t.start()

        _stop = getattr(self, '_mouse_hook_stop', None)
        if _stop:
            try: _stop.set()
            except: pass
        self._mouse_hook_stop = None
        self._mouse_listener  = None

        if mouse_binds:
            import threading, ctypes, ctypes.wintypes as _wt

            _BIND_MAP = {}
            for name, action in mouse_binds.items():
                if name == "Mouse3": _BIND_MAP[0x0207] = action
                elif name == "Mouse4": _BIND_MAP[(0x020B, 1)] = action
                elif name == "Mouse5": _BIND_MAP[(0x020B, 2)] = action

            import queue as _queue
            _action_queue = self._hotkey_action_queue

            stop_evt = threading.Event()
            self._mouse_hook_stop = stop_evt

            class _MSLL(ctypes.Structure):
                _fields_ = [("pt", _wt.POINT), ("mouseData", _wt.DWORD),
                             ("flags", _wt.DWORD), ("time", _wt.DWORD),
                             ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

            def _hook_thread():
                u32 = ctypes.WinDLL("user32", use_last_error=True)
                HOOKPROC = ctypes.WINFUNCTYPE(
                    ctypes.c_longlong,
                    ctypes.c_int,
                    ctypes.c_ulonglong,
                    ctypes.c_longlong,
                )

                u32.CallNextHookEx.restype  = ctypes.c_longlong
                u32.CallNextHookEx.argtypes = [
                    ctypes.c_void_p,
                    ctypes.c_int,
                    ctypes.c_ulonglong,
                    ctypes.c_longlong,
                ]

                hook = [None]
                def _proc(nCode, wParam, lParam):
                    try:
                        if nCode >= 0:
                            act = None
                            if wParam in _BIND_MAP:
                                act = _BIND_MAP[wParam]
                            elif wParam == 0x020B:
                                ms = ctypes.cast(lParam, ctypes.POINTER(_MSLL))
                                xb = (ms.contents.mouseData >> 16) & 0xFFFF
                                act = _BIND_MAP.get((0x020B, xb))
                            if act:
                                _action_queue.put(act)
                    except Exception:
                        pass
                    return u32.CallNextHookEx(hook[0], nCode, wParam, lParam)

                cb = HOOKPROC(_proc)
                hook[0] = u32.SetWindowsHookExW(14, cb, None, 0)
                if not hook[0]:
                    print(f"[Hotkey] hook failed err={ctypes.get_last_error()}")
                    return
                print(f"[Hotkey] mouse hook OK: {list(mouse_binds.keys())}")

                msg = _wt.MSG()
                while not stop_evt.is_set():
                    r = u32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1)
                    if r > 0:
                        u32.TranslateMessage(ctypes.byref(msg))
                        u32.DispatchMessageW(ctypes.byref(msg))
                    else:
                        stop_evt.wait(0.001)

                u32.UnhookWindowsHookEx(hook[0])
                print("[Hotkey] mouse hook removed")

            t = threading.Thread(target=_hook_thread, daemon=True)
            t.start()
            self._mouse_listener = t

    def _repopulate_with_colors(self):
        """Re-render table with current custom colors."""
        fc = getattr(self, '_flag_name_color', QColor(126,184,247))
        vc = getattr(self, '_value_text_color', QColor(232,232,232))
        for row in range(self.table.rowCount()):
            ni = self.table.item(row, 1)
            vi = self.table.item(row, 3)
            if ni: ni.setForeground(fc)
            if vi: vi.setForeground(vc)

    def _switch_settings_tab(self, index):
        self._settings_stack.setCurrentIndex(index)
        for i, btn in enumerate(self._tab_btns):
            is_active = (i == index)
            btn.setChecked(is_active)
            btn.setStyleSheet(self._tab_on_style if is_active else self._tab_off_style)
            if hasattr(self, '_make_tab_icon') and hasattr(self, '_tab_names_list'):
                try:
                    name  = self._tab_names_list[i]
                    color = self._col_on if is_active else self._col_off
                    from PyQt6.QtGui import QIcon
                    from PyQt6.QtCore import QSize
                    btn.setIcon(QIcon(self._make_tab_icon(name, color)))
                    btn.setIconSize(QSize(20, 20))
                except Exception:
                    pass
            if hasattr(self, '_tab_labels') and i < len(self._tab_labels):
                lbl = self._tab_labels[i]
                if is_active: lbl.show()
                else: lbl.hide()

    def _close_settings(self):
        self.btn_settings.setChecked(False)
        self._toggle_settings()

    def _apply_compact_mode(self, compact):
        row_h = 26 if compact else 36
        for i in range(self.table.rowCount()):
            self.table.setRowHeight(i, row_h)
        self.table.verticalHeader().setDefaultSectionSize(row_h)

    def _refresh_builtin_presets(self):
        pass

    def _apply_builtin_preset(self, preset: dict):
        """Show confirm dialog then load preset flags, filtering invalid singleton flags."""
        name  = preset["name"]
        flags = preset["flags"]
        count = len(flags)
        dlg = ConfirmDialog(f"Add \"{name}\" ({count} flags) to editor?", self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            try:
                from core.validator import validate_flags
                vr = validate_flags(flags)
                valid_flags = vr.valid
                if not vr.roblox_missing and vr.skipped_count > 0:
                    self._set_status(
                        f"⚠  Preset '{name}': {vr.skipped_count} invalid flags skipped, "
                        f"{vr.valid_count} valid added."
                    )
            except Exception:
                valid_flags = flags

            added   = self._merge_flags(valid_flags)
            skipped = len(valid_flags) - added
            self._save_flags()
            self._populate_table(self.all_flags)
            msg = f"Added preset '{name}' — {added} new flags"
            if skipped:
                msg += f" ({skipped} duplicates skipped)"
            if not hasattr(self, '_last_status_was_validation') or not vr.skipped_count:
                self._set_status(msg)
            self._close_settings()




    def _configs_dir(self):
        d = self.state.config_dir / "configs"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _refresh_cfg_list(self):
        """Update the saved configs label in CONFIGS tab."""
        if not hasattr(self, '_cfg_saved_label'):
            return
        d = self._configs_dir()
        files = sorted(d.glob("*.swcfg"), key=lambda f: f.stat().st_mtime, reverse=True)
        if not files:
            self._cfg_saved_label.setText("No configs saved yet.")
        else:
            lines = []
            for f in files[:8]:
                sz = f.stat().st_size
                sz_str = f"{sz//1024} KB" if sz >= 1024 else f"{sz} B"
                lines.append(f"  {f.stem}  ({sz_str})")
            self._cfg_saved_label.setText("\n".join(lines))

    def _open_configs_folder(self):
        import subprocess, os
        d = self._configs_dir()
        try:
            subprocess.Popen(f'explorer "{d}"')
        except Exception:
            os.startfile(str(d))

    def _export_app_config(self):
        """Export current app_settings.json + background image as a .swcfg file."""
        from PyQt6.QtWidgets import QFileDialog, QInputDialog
        import zipfile, base64, json as _json, os, datetime

        dlg_name = InputDialog("EXPORT CONFIG", "Config name:", default="my_config", parent=self)
        if dlg_name.exec() != QDialog.DialogCode.Accepted:
            return
        name = dlg_name.get_text().replace(" ", "_")
        if not name:
            return

        default_path = str(self._configs_dir() / f"{name}.swcfg")
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Config", default_path, "SacredWare Config (*.swcfg)"
        )
        if not path:
            return

        try:
            def c2h(c): return f"#{c.red():02x}{c.green():02x}{c.blue():02x}"
            def sv(attr, default):
                w = getattr(self, attr, None)
                return w.value() if w is not None else default
            def sb(attr, default):
                w = getattr(self, attr, None)
                return w.isChecked() if w is not None else default
            def st(attr, default):
                w = getattr(self, attr, None)
                return w.text() if w is not None else default

            bg_path = getattr(self, '_bg_path', '')
            settings = {
                "swcfg_version":  1,
                "config_name":    name,
                "exported_at":    datetime.datetime.now().isoformat(timespec='seconds'),
                "bg_path":        os.path.basename(bg_path) if bg_path else "",
                "bg_opacity":     sv('_slider_bg_opacity', 60),
                "bg_solid":       c2h(getattr(self, '_bg_solid_color', QColor(13,13,13))),
                "shimmer_text":   c2h(getattr(self, '_shimmer_text_color', QColor(220,220,220))),
                "shimmer_dark":   c2h(getattr(self, '_shimmer_dark_color', QColor(25,25,25))),
                "shimmer_speed":  sv('_slider_shim', 3),
                "accent":         c2h(getattr(self, '_theme_accent', QColor(255,255,255))),
                "btn_bg":         c2h(getattr(self, '_btn_color_val', QColor(20,20,20))),
                "flag_color":     c2h(getattr(self, '_flag_name_color', QColor(126,184,247))),
                "text_color":     c2h(getattr(self, '_general_text_color', QColor(187,187,187))),
                "value_color":    c2h(getattr(self, '_value_text_color', QColor(232,232,232))),
                "compact":        sb('_chk_compact', False),
                "show_type":      sb('_chk_show_type', True),
                "alt_rows":       sb('_chk_alt_rows', False),
                "title_full":     st('_edit_title', "\u271f  SacredWare"),
            }

            with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr("settings.json", _json.dumps(settings, indent=2, ensure_ascii=False))
                if bg_path and os.path.isfile(bg_path):
                    ext = os.path.splitext(bg_path)[1].lower() or ".png"
                    with open(bg_path, 'rb') as img_f:
                        img_data = img_f.read()
                    zf.writestr(f"background{ext}", img_data)

            self._set_status(f"Config exported: {os.path.basename(path)}")
            self._refresh_cfg_list()

        except Exception as e:
            self._set_status(f"Export error: {e}")
            from PyQt6.QtWidgets import QMessageBox
            AlertDialog("EXPORT FAILED", str(e), parent=self).exec()

    def _import_app_config(self):
        """Import a .swcfg file and apply all settings including background."""
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        import zipfile, json as _json, os

        path, _ = QFileDialog.getOpenFileName(
            self, "Import Config", str(self._configs_dir()),
            "SacredWare Config (*.swcfg);;All Files (*)"
        )
        if not path:
            return

        try:
            with zipfile.ZipFile(path, 'r') as zf:
                names = zf.namelist()
                if "settings.json" not in names:
                    AlertDialog("INVALID CONFIG", "Not a valid .swcfg file\n(missing settings.json)", parent=self).exec()
                    return

                data = _json.loads(zf.read("settings.json").decode("utf-8"))

                bg_candidates = [n for n in names if n.startswith("background.") or n.startswith("background")]
                restored_bg_path = ""
                if bg_candidates:
                    bg_name = bg_candidates[0]
                    ext = os.path.splitext(bg_name)[1] or ".png"
                    bg_dest = self.state.config_dir / f"imported_bg{ext}"
                    with open(bg_dest, 'wb') as f:
                        f.write(zf.read(bg_name))
                    restored_bg_path = str(bg_dest)

            cfg_name = data.get("config_name", os.path.basename(path))
            exported_at = data.get("exported_at", "unknown")
            has_bg = bool(restored_bg_path)
            bg_line = "Background: included" if has_bg else "Background: not included"
            msg = f"Import config: {cfg_name}\nExported: {exported_at}\n{bg_line}\n\nThis will replace your current customisation."
            dlg_confirm = AlertDialog("IMPORT CONFIG", msg, parent=self, yes_no=True)
            if dlg_confirm.exec() != QDialog.DialogCode.Accepted:
                return

            if restored_bg_path:
                data["bg_path"] = restored_bg_path
            else:
                data["bg_path"] = ""

            sf = self._settings_file()
            import json as _json2
            with open(sf, "w", encoding="utf-8") as f:
                _json2.dump(data, f, indent=2, ensure_ascii=False)

            self._load_app_settings()
            self._set_status(f"Config imported: {cfg_name}")

        except Exception as e:
            self._set_status(f"Import error: {e}")
            AlertDialog("IMPORT FAILED", str(e), parent=self).exec()



    def _mods_state_file(self):
        return self.state.config_dir / "mods_state.json"

    def _load_mods_state(self):
        """Load saved cursor/font paths and refresh UI."""
        import json as _j
        try:
            with open(self._mods_state_file(), "r", encoding="utf-8") as f:
                d = _j.load(f)
            self._cursor_path  = d.get("cursor_path", "")
            self._font_path    = d.get("font_path", "")
            self._auto_mods_on = d.get("auto_mods", False)
        except Exception:
            self._cursor_path  = ""
            self._font_path    = ""
            self._auto_mods_on = False
        self._refresh_mods_ui()
        if self._auto_mods_on:
            self._start_mods_watcher()
            if hasattr(self, 'btn_auto_mods'):
                self.btn_auto_mods.setChecked(True)
                self.btn_auto_mods.setText('Auto Apply Mods: ON')

    def _save_mods_state(self):
        import json as _j
        try:
            self._mods_state_file().parent.mkdir(parents=True, exist_ok=True)
            with open(self._mods_state_file(), "w", encoding="utf-8") as f:
                _j.dump({
                    "cursor_path": self._cursor_path,
                    "font_path":   self._font_path,
                    "auto_mods":   getattr(self, '_auto_mods_on', False),
                }, f)
        except Exception:
            pass

    def _refresh_mods_ui(self):
        """Update cursor and font preview widgets."""
        import os
        from PyQt6.QtGui import QPixmap

        if self._cursor_path and os.path.isfile(self._cursor_path):
            px = QPixmap(self._cursor_path).scaled(
                40, 40,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self._cursor_preview.setPixmap(px)
            self._cursor_status.setText(os.path.basename(self._cursor_path))
            self._cursor_status.setStyleSheet("color:#cccccc; font-size:11px; background:transparent;")
        else:
            self._cursor_preview.setPixmap(QPixmap())
            self._cursor_preview.setText("?")
            self._cursor_status.setText("No cursor set")
            self._cursor_status.setStyleSheet("color:#444; font-size:11px; background:transparent;")

        if self._font_path and os.path.isfile(self._font_path):
            from PyQt6.QtGui import QFontDatabase, QFont
            fid = QFontDatabase.addApplicationFont(self._font_path)
            families = QFontDatabase.applicationFontFamilies(fid)
            if families:
                self._font_preview.setFont(QFont(families[0], 16))
                self._font_preview.setStyleSheet(
                    "background:#111; border:1px solid #222; border-radius:8px; color:#e8e8e8; font-size:16px;"
                )
            self._font_status.setText(os.path.basename(self._font_path))
            self._font_status.setStyleSheet("color:#cccccc; font-size:11px; background:transparent;")
        else:
            self._font_preview.setText("Aa")
            self._font_preview.setStyleSheet(
                "background:#111; border:1px solid #222; border-radius:8px; color:#666; font-size:18px;"
            )
            self._font_status.setText("No font set")
            self._font_status.setStyleSheet("color:#444; font-size:11px; background:transparent;")

    def _open_cursor_presets_menu(self):
        """Show inline dropdown menu with built-in cursor presets."""
        from PyQt6.QtWidgets import QMenu
        from PyQt6.QtGui import QPixmap, QIcon, QImage
        import base64

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #0d0d0d;
                border-radius:8px; padding:4px;
            }
            QMenu::item {
                color: #cccccc;
                padding:7px 16px 7px 10px; border-radius:5px;
            }
            QMenu::item:selected { background: #0d0d0d;
            QMenu::separator { background: #0d0d0d;
        """)

        for preset_id, display_name in _BUILTIN_CURSOR_NAMES.items():
            b64 = _BUILTIN_CURSORS.get(preset_id, '')
            action = menu.addAction(display_name)
            try:
                raw = base64.b64decode(b64)
                img = QImage.fromData(raw)
                px  = QPixmap.fromImage(img).scaled(
                    20, 20,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                action.setIcon(QIcon(px))
            except Exception:
                pass
            action.setData(preset_id)

        btn = self.sender()
        chosen = menu.exec(btn.mapToGlobal(btn.rect().bottomLeft()))
        if chosen and chosen.data():
            self._apply_cursor_preset(chosen.data())

    def _apply_cursor_preset(self, preset_id: str):
        """Apply a built-in cursor preset by writing it as a temp PNG."""
        import base64, tempfile, os
        b64 = _BUILTIN_CURSORS.get(preset_id)
        if not b64:
            return
        try:
            raw = base64.b64decode(b64)
            tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False,
                                              prefix=f'sacrx_cursor_{preset_id}_')
            tmp.write(raw)
            tmp.close()
            self._cursor_path = tmp.name
            self._save_mods_state()
            self._refresh_mods_ui()
            name = _BUILTIN_CURSOR_NAMES.get(preset_id, preset_id)
            self._set_status(f"Cursor preset '{name}' selected — click Apply Mods")
        except Exception as e:
            self._set_status(f"Cursor preset error: {e}")

    def _pick_cursor(self):
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose Cursor Image", "",
            "Cursor / Image files (*.png *.cur *.ico *.jpg *.jpeg);;All Files (*)"
        )
        if not path:
            return

        import os, tempfile, struct, io
        ext = os.path.splitext(path)[1].lower()

        if ext in ('.cur', '.ico'):
            try:
                from PIL import Image
                data = open(path, 'rb').read()
                count = struct.unpack_from('<H', data, 4)[0]
                best_size  = 0
                best_offset = 0
                best_length = 0
                for i in range(count):
                    base = 6 + i * 16
                    w      = data[base]     or 256
                    h      = data[base + 1] or 256
                    length = struct.unpack_from('<I', data, base + 8)[0]
                    offset = struct.unpack_from('<I', data, base + 12)[0]
                    if w * h > best_size:
                        best_size   = w * h
                        best_offset = offset
                        best_length = length

                img_data = data[best_offset: best_offset + best_length]
                img = Image.open(io.BytesIO(img_data)).convert('RGBA')
                img = img.resize((64, 64), Image.LANCZOS)

                tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                img.save(tmp.name, format='PNG')
                tmp.close()
                path = tmp.name
                self._set_status("Cursor converted from .cur to PNG — click Apply Mods")
            except Exception as e:
                self._set_status(f"Failed to convert cursor: {e}")
                return
        else:
            try:
                from PIL import Image
                img = Image.open(path).convert('RGBA')
                if img.size != (64, 64):
                    img = img.resize((64, 64), Image.LANCZOS)
                    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                    img.save(tmp.name, format='PNG')
                    tmp.close()
                    path = tmp.name
            except Exception:
                pass

        self._cursor_path = path
        self._save_mods_state()
        self._refresh_mods_ui()
        self._set_status("Cursor selected — click Apply Mods to Roblox")

    def _clear_cursor(self):
        self._cursor_path = ""
        self._save_mods_state()
        self._refresh_mods_ui()
        roblox_dir = self._find_roblox_dir()
        if roblox_dir:
            import os, shutil as _sh
            cursor_dir = os.path.join(roblox_dir, "content", "textures", "Cursors", "KeyboardMouse")
            restored = 0
            for fname in ("ArrowFarCursor.png", "ArrowCursor.png"):
                dest   = os.path.join(cursor_dir, fname)
                backup = dest + ".bak"
                if os.path.isfile(backup):
                    try:
                        _sh.copy2(backup, dest)
                        os.remove(backup)
                        restored += 1
                    except Exception:
                        pass
                elif os.path.isfile(dest):
                    try:
                        os.remove(dest)
                    except Exception:
                        pass
            msg = f"Cursor removed — {restored} originals restored" if restored else "Cursor cleared from Roblox"
        else:
            msg = "Cursor cleared"
        self._set_status(msg)

    def _pick_font(self):
        from PyQt6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose Font", "", "Font Files (*.ttf *.otf);;TrueType (*.ttf);;OpenType (*.otf);;All Files (*)"
        )
        if path:
            self._font_path = path
            self._save_mods_state()
            self._refresh_mods_ui()
            self._set_status("Font selected — click Apply Mods to Roblox")

    def _clear_font(self):
        self._font_path = ""
        self._save_mods_state()
        self._refresh_mods_ui()
        roblox_dir = self._find_roblox_dir()
        if roblox_dir:
            import os, shutil as _sh
            font_dir = os.path.join(roblox_dir, "content", "fonts")
            restored = 0
            for fname in ['GothamSSm-Book.ttf', 'GothamSSm-BookItalic.ttf', 'GothamSSm-Medium.ttf', 'GothamSSm-MediumItalic.ttf', 'GothamSSm-Bold.ttf', 'GothamSSm-BoldItalic.ttf', 'GothamSSm-Black.ttf', 'GothamSSm-BlackItalic.ttf', 'GothamSSm-Light.ttf', 'GothamSSm-LightItalic.ttf', 'GothamSSm-XLight.ttf', 'GothamSSm-XLightItalic.ttf', 'Nunito-Regular.ttf', 'Nunito-Bold.ttf', 'Nunito-Italic.ttf', 'Nunito-BoldItalic.ttf', 'Nunito-Light.ttf', 'Nunito-LightItalic.ttf', 'Nunito-SemiBold.ttf', 'Nunito-SemiBoldItalic.ttf', 'Nunito-ExtraBold.ttf', 'Nunito-ExtraBoldItalic.ttf', 'BuilderSans-Regular.ttf', 'BuilderSans-Medium.ttf', 'BuilderSans-Bold.ttf', 'BuilderSans-ExtraBold.ttf', 'BuilderSans-SemiBold.ttf', 'BuilderSans-Light.ttf', 'BuilderSans-Thin.ttf', 'BuilderSans-Italic.ttf', 'BuilderSans-MediumItalic.ttf', 'BuilderSans-BoldItalic.ttf', 'BuilderSans-ExtraBoldItalic.ttf', 'Roboto-Regular.ttf', 'Roboto-Bold.ttf', 'Roboto-Italic.ttf', 'Roboto-BoldItalic.ttf', 'Roboto-Light.ttf', 'Roboto-LightItalic.ttf', 'Roboto-Medium.ttf', 'Roboto-MediumItalic.ttf', 'Roboto-Black.ttf', 'Roboto-BlackItalic.ttf', 'Roboto-Thin.ttf', 'Roboto-ThinItalic.ttf', 'SourceSansPro-Regular.ttf', 'SourceSansPro-Bold.ttf', 'SourceSansPro-Italic.ttf', 'SourceSansPro-BoldItalic.ttf', 'SourceSansPro-Light.ttf', 'SourceSansPro-LightItalic.ttf', 'SourceSansPro-Semibold.ttf', 'SourceSansPro-SemiboldItalic.ttf', 'SourceSansPro-Black.ttf', 'SourceSansPro-BlackItalic.ttf', 'SourceSansPro-ExtraLight.ttf', 'SourceSansPro-ExtraLightItalic.ttf', 'Inconsolata-Regular.ttf', 'Inconsolata-Bold.ttf', 'TitilliumWeb-Regular.ttf', 'TitilliumWeb-Bold.ttf', 'TitilliumWeb-Italic.ttf', 'TitilliumWeb-BoldItalic.ttf', 'TitilliumWeb-Light.ttf', 'TitilliumWeb-LightItalic.ttf', 'TitilliumWeb-SemiBold.ttf', 'TitilliumWeb-SemiBoldItalic.ttf', 'TitilliumWeb-ExtraLight.ttf', 'TitilliumWeb-ExtraLightItalic.ttf', 'TitilliumWeb-Black.ttf', 'Arial.ttf', 'ArialBold.ttf', 'HighwayGothic.ttf', 'Bangers-Regular.ttf', 'Creepster-Regular.ttf', 'DenkOne-Regular.ttf', 'FredokaOne-Regular.ttf', 'Grenze-Regular.ttf', 'Grenze-Bold.ttf', 'LuckiestGuy-Regular.ttf', 'Merriweather-Regular.ttf', 'Merriweather-Bold.ttf', 'Merriweather-Italic.ttf', 'Merriweather-BoldItalic.ttf', 'Merriweather-Light.ttf', 'Merriweather-LightItalic.ttf', 'Michroma-Regular.ttf', 'Oswald-Regular.ttf', 'Oswald-Bold.ttf', 'Oswald-Light.ttf', 'Oswald-Medium.ttf', 'Oswald-SemiBold.ttf', 'Oswald-ExtraLight.ttf', 'PermanentMarker-Regular.ttf', 'Sarpanch-Regular.ttf', 'Sarpanch-Bold.ttf', 'Sarpanch-Medium.ttf', 'Sarpanch-SemiBold.ttf', 'Sarpanch-ExtraBold.ttf', 'Sarpanch-Black.ttf', 'SpecialElite-Regular.ttf', 'Ubuntu-Regular.ttf', 'Ubuntu-Bold.ttf', 'Ubuntu-Italic.ttf', 'Ubuntu-BoldItalic.ttf', 'Ubuntu-Light.ttf', 'Ubuntu-LightItalic.ttf', 'Ubuntu-Medium.ttf', 'Ubuntu-MediumItalic.ttf', 'Balthazar-Regular.ttf', 'RomanAntique.ttf', 'Jura-Regular.ttf', 'Jura-Bold.ttf', 'Jura-Light.ttf', 'Jura-Medium.ttf', 'Jura-SemiBold.ttf', 'Jura-DemiBold.ttf', 'AmaticSC-Regular.ttf', 'AmaticSC-Bold.ttf', 'Arimo-Regular.ttf', 'Arimo-Bold.ttf', 'Arimo-Italic.ttf', 'Arimo-BoldItalic.ttf', 'Gupter-Regular.ttf', 'Gupter-Bold.ttf', 'Gupter-Medium.ttf', 'Fondamento-Regular.ttf', 'Fondamento-Italic.ttf', 'Guru.ttf']:
                dest   = os.path.join(font_dir, fname)
                backup = dest + ".bak"
                if os.path.isfile(backup):
                    try:
                        _sh.copy2(backup, dest)
                        os.remove(backup)
                        restored += 1
                    except Exception:
                        pass
            msg = f"Font cleared — {restored} originals restored" if restored else "Font cleared"
        else:
            msg = "Font cleared"
        self._set_status(msg)

    def _find_roblox_dir(self):
        """Find the active Roblox installation directory."""
        import os, glob, subprocess

        local_app = os.environ.get("LOCALAPPDATA", "")
        candidates = []

        try:
            import subprocess as _sp
            _cmd = ['wmic', 'process', 'where', 'name="RobloxPlayerBeta.exe"', 'get', 'ExecutablePath', '/value']
            _out = _sp.check_output(_cmd, shell=False, stderr=_sp.DEVNULL, timeout=3).decode(errors='ignore')
            for _line in _out.splitlines():
                if 'ExecutablePath=' in _line:
                    _exe = _line.split('=', 1)[1].strip()
                    if _exe and os.path.isfile(_exe):
                        return os.path.dirname(_exe)
        except Exception:
            pass

        if local_app:
            launchers = ['Roblox', 'Bloxstrap', 'Froststrap', 'Fishstrap',
                         'Solara', 'Arcturus', 'Vinegar']
            for launcher in launchers:
                candidates += sorted(
                    glob.glob(os.path.join(local_app, launcher, 'Versions', 'version-*')),
                    reverse=True
                )
                candidates += [os.path.join(local_app, launcher, 'Versions')]
                candidates += [os.path.join(local_app, launcher)]

        for path in candidates:
            exe = os.path.join(path, 'RobloxPlayerBeta.exe')
            if os.path.isfile(exe):
                return path
        return None

    def _apply_mods(self):
        """Copy cursor and font files into the Roblox installation."""
        import shutil, os

        roblox_dir = self._find_roblox_dir()
        if not roblox_dir:
            AlertDialog(
                "ROBLOX NOT FOUND",
                "Could not locate your Roblox installation.\n\n"
                "Make sure Roblox is installed and has been launched at least once.",
                parent=self
            ).exec()
            return

        applied = []
        errors  = []

        if self._cursor_path and os.path.isfile(self._cursor_path):
            dest_dir = os.path.join(roblox_dir, "content", "textures", "Cursors", "KeyboardMouse")
            try:
                os.makedirs(dest_dir, exist_ok=True)
                for fname in ("ArrowFarCursor.png", "ArrowCursor.png"):
                    shutil.copy2(self._cursor_path, os.path.join(dest_dir, fname))
                applied.append("Cursor")
            except Exception as e:
                errors.append(f"Cursor: {e}")

        if self._font_path and os.path.isfile(self._font_path):
            font_dir = os.path.join(roblox_dir, "content", "fonts")
            try:
                os.makedirs(font_dir, exist_ok=True)
                ext = os.path.splitext(self._font_path)[1].lower() or ".ttf"

                target_fonts = ['GothamSSm-Book.ttf', 'GothamSSm-BookItalic.ttf', 'GothamSSm-Medium.ttf', 'GothamSSm-MediumItalic.ttf', 'GothamSSm-Bold.ttf', 'GothamSSm-BoldItalic.ttf', 'GothamSSm-Black.ttf', 'GothamSSm-BlackItalic.ttf', 'GothamSSm-Light.ttf', 'GothamSSm-LightItalic.ttf', 'GothamSSm-XLight.ttf', 'GothamSSm-XLightItalic.ttf', 'Nunito-Regular.ttf', 'Nunito-Bold.ttf', 'Nunito-Italic.ttf', 'Nunito-BoldItalic.ttf', 'Nunito-Light.ttf', 'Nunito-LightItalic.ttf', 'Nunito-SemiBold.ttf', 'Nunito-SemiBoldItalic.ttf', 'Nunito-ExtraBold.ttf', 'Nunito-ExtraBoldItalic.ttf', 'BuilderSans-Regular.ttf', 'BuilderSans-Medium.ttf', 'BuilderSans-Bold.ttf', 'BuilderSans-ExtraBold.ttf', 'BuilderSans-SemiBold.ttf', 'BuilderSans-Light.ttf', 'BuilderSans-Thin.ttf', 'BuilderSans-Italic.ttf', 'BuilderSans-MediumItalic.ttf', 'BuilderSans-BoldItalic.ttf', 'BuilderSans-ExtraBoldItalic.ttf', 'Roboto-Regular.ttf', 'Roboto-Bold.ttf', 'Roboto-Italic.ttf', 'Roboto-BoldItalic.ttf', 'Roboto-Light.ttf', 'Roboto-LightItalic.ttf', 'Roboto-Medium.ttf', 'Roboto-MediumItalic.ttf', 'Roboto-Black.ttf', 'Roboto-BlackItalic.ttf', 'Roboto-Thin.ttf', 'Roboto-ThinItalic.ttf', 'SourceSansPro-Regular.ttf', 'SourceSansPro-Bold.ttf', 'SourceSansPro-Italic.ttf', 'SourceSansPro-BoldItalic.ttf', 'SourceSansPro-Light.ttf', 'SourceSansPro-LightItalic.ttf', 'SourceSansPro-Semibold.ttf', 'SourceSansPro-SemiboldItalic.ttf', 'SourceSansPro-Black.ttf', 'SourceSansPro-BlackItalic.ttf', 'SourceSansPro-ExtraLight.ttf', 'SourceSansPro-ExtraLightItalic.ttf', 'Inconsolata-Regular.ttf', 'Inconsolata-Bold.ttf', 'TitilliumWeb-Regular.ttf', 'TitilliumWeb-Bold.ttf', 'TitilliumWeb-Italic.ttf', 'TitilliumWeb-BoldItalic.ttf', 'TitilliumWeb-Light.ttf', 'TitilliumWeb-LightItalic.ttf', 'TitilliumWeb-SemiBold.ttf', 'TitilliumWeb-SemiBoldItalic.ttf', 'TitilliumWeb-ExtraLight.ttf', 'TitilliumWeb-ExtraLightItalic.ttf', 'TitilliumWeb-Black.ttf', 'Arial.ttf', 'ArialBold.ttf', 'HighwayGothic.ttf', 'Bangers-Regular.ttf', 'Creepster-Regular.ttf', 'DenkOne-Regular.ttf', 'FredokaOne-Regular.ttf', 'Grenze-Regular.ttf', 'Grenze-Bold.ttf', 'LuckiestGuy-Regular.ttf', 'Merriweather-Regular.ttf', 'Merriweather-Bold.ttf', 'Merriweather-Italic.ttf', 'Merriweather-BoldItalic.ttf', 'Merriweather-Light.ttf', 'Merriweather-LightItalic.ttf', 'Michroma-Regular.ttf', 'Oswald-Regular.ttf', 'Oswald-Bold.ttf', 'Oswald-Light.ttf', 'Oswald-Medium.ttf', 'Oswald-SemiBold.ttf', 'Oswald-ExtraLight.ttf', 'PermanentMarker-Regular.ttf', 'Sarpanch-Regular.ttf', 'Sarpanch-Bold.ttf', 'Sarpanch-Medium.ttf', 'Sarpanch-SemiBold.ttf', 'Sarpanch-ExtraBold.ttf', 'Sarpanch-Black.ttf', 'SpecialElite-Regular.ttf', 'Ubuntu-Regular.ttf', 'Ubuntu-Bold.ttf', 'Ubuntu-Italic.ttf', 'Ubuntu-BoldItalic.ttf', 'Ubuntu-Light.ttf', 'Ubuntu-LightItalic.ttf', 'Ubuntu-Medium.ttf', 'Ubuntu-MediumItalic.ttf', 'Balthazar-Regular.ttf', 'RomanAntique.ttf', 'Jura-Regular.ttf', 'Jura-Bold.ttf', 'Jura-Light.ttf', 'Jura-Medium.ttf', 'Jura-SemiBold.ttf', 'Jura-DemiBold.ttf', 'AmaticSC-Regular.ttf', 'AmaticSC-Bold.ttf', 'Arimo-Regular.ttf', 'Arimo-Bold.ttf', 'Arimo-Italic.ttf', 'Arimo-BoldItalic.ttf', 'Gupter-Regular.ttf', 'Gupter-Bold.ttf', 'Gupter-Medium.ttf', 'Fondamento-Regular.ttf', 'Fondamento-Italic.ttf', 'Guru.ttf']

                replaced = 0
                for fname in target_fonts:
                    dest = os.path.join(font_dir, fname)
                    backup = dest + ".bak"
                    if os.path.isfile(dest) and not os.path.isfile(backup):
                        shutil.copy2(dest, backup)
                    try:
                        shutil.copy2(self._font_path, dest)
                        replaced += 1
                    except Exception:
                        pass

                try:
                    for existing in os.listdir(font_dir):
                        if existing.lower().endswith(".ttf") and existing not in target_fonts:
                            dest = os.path.join(font_dir, existing)
                            backup = dest + ".bak"
                            if not os.path.isfile(backup):
                                shutil.copy2(dest, backup)
                            try:
                                shutil.copy2(self._font_path, dest)
                                replaced += 1
                            except Exception:
                                pass
                except Exception:
                    pass

                if replaced > 0:
                    applied.append(f"Font ({replaced} files replaced)")
                else:
                    errors.append("Font: no font files found in Roblox folder to replace")

            except Exception as e:
                errors.append(f"Font: {e}")

        if not applied and not errors:
            AlertDialog(
                "NOTHING TO APPLY",
                "Select a cursor or font first.",
                parent=self
            ).exec()
            return

        msg = ""
        if applied:
            msg += f"Applied: {', '.join(applied)}\n"
        if errors:
            msg += f"Errors:\n" + "\n".join(errors)

        AlertDialog("MODS APPLIED", msg.strip(), parent=self).exec()
        self._set_status(f"Mods applied: {', '.join(applied)}" if applied else "Apply failed")



    def _toggle_auto_mods(self):
        """Toggle the auto-mods watcher on/off."""
        if not self._auto_mods_on:
            self._auto_mods_on = True
            self.btn_auto_mods.setChecked(True)
            self.btn_auto_mods.setText('Auto Apply Mods: ON')
            self._start_mods_watcher()
            self._set_status("Auto Apply Mods enabled — watching for Roblox")
        else:
            self._auto_mods_on = False
            self.btn_auto_mods.setChecked(False)
            self.btn_auto_mods.setText('Auto Apply Mods: OFF')
            self._stop_mods_watcher()
            self._set_status("Auto Apply Mods disabled")
        self._save_mods_state()

    def _start_mods_watcher(self):
        """Start background thread that watches for Roblox and applies mods."""
        self._stop_mods_watcher()
        self._mods_watcher = _ModsWatcherThread(self)
        self._mods_watcher.mods_applied.connect(self._on_mods_auto_applied)
        self._mods_watcher.start()

    def _stop_mods_watcher(self):
        """Stop the mods watcher thread."""
        if self._mods_watcher:
            try:
                self._mods_watcher.stop()
                self._mods_watcher = None
            except Exception:
                pass

    def _on_mods_auto_applied(self, msg: str):
        """Called when auto-mods watcher applies mods."""
        self._set_status(msg)

    def _settings_file(self):
        import pathlib
        p = self.state.config_dir / "app_settings.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def _save_app_settings(self):
        import json as _json
        def c2h(c): return f"#{c.red():02x}{c.green():02x}{c.blue():02x}"
        def sv(attr, default):
            w = getattr(self, attr, None)
            return w.value() if w is not None else default
        def sb(attr, default):
            w = getattr(self, attr, None)
            return w.isChecked() if w is not None else default
        def st(attr, default):
            w = getattr(self, attr, None)
            return w.text() if w is not None else default
        data = {
            "bg_path":       getattr(self, '_bg_path', ""),
            "bg_opacity":    sv('_slider_bg_opacity', 60),
            "bg_solid":      c2h(getattr(self, '_bg_solid_color', QColor(13,13,13))),
            "shimmer_text":  c2h(getattr(self, '_shimmer_text_color', QColor(220,220,220))),
            "shimmer_dark":  c2h(getattr(self, '_shimmer_dark_color', QColor(25,25,25))),
            "shimmer_speed": sv('_slider_shim', 3),
            "accent":        c2h(getattr(self, '_theme_accent', QColor(255,255,255))),
            "btn_bg":        c2h(getattr(self, '_btn_color_val', QColor(20,20,20))),
            "flag_color":    c2h(getattr(self, '_flag_name_color', QColor(126,184,247))),
            "text_color":    c2h(getattr(self, '_general_text_color', QColor(187,187,187))),
            "value_color":   c2h(getattr(self, '_value_text_color', QColor(232,232,232))),
            "compact":       sb('_chk_compact', False),
            "show_type":     sb('_chk_show_type', True),
            "alt_rows":      sb('_chk_alt_rows', False),
            "auto_interval": sv('_slider_interval', 5),
            "autostart":     sb('_chk_autostart', False),
            "inject_launch": sb('_chk_inject_launch', False),
            "tray_startup":  sb('_chk_tray_startup', False),
            "run_on_boot":   sb('_chk_run_on_boot', False),
            "binds":         getattr(self, '_binds', {}),
            "title_full":    st('_edit_title', "✟  SacredWare"),
        }
        try:
            sf = self._settings_file()
            sf.parent.mkdir(parents=True, exist_ok=True)
            with open(sf, "w", encoding="utf-8") as f:
                _json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self._set_status(f"Save error: {e}")

    def _load_app_settings(self):
        import json as _json, os as _os
        try:
            sf = self._settings_file()
            if not sf.exists():
                return
            with open(sf, encoding="utf-8") as f:
                data = _json.load(f)
        except Exception as e:
            self._set_status(f"Settings load error: {e}")
            return

        def h2c(h):
            try:
                h = str(h).lstrip("#")
                if len(h) != 6: return QColor(0,0,0)
                return QColor(int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))
            except Exception:
                return QColor(0,0,0)

        if "shimmer_text" in data:
            self._shimmer_text_color = h2c(data["shimmer_text"])
            lbl = self.findChild(TitleLabel)
            if lbl: lbl._text_color = self._shimmer_text_color
            self._update_shim_btn_preview()

        if "shimmer_dark" in data:
            self._shimmer_dark_color = h2c(data["shimmer_dark"])
            lbl = self.findChild(TitleLabel)
            if lbl: lbl._dark_color = self._shimmer_dark_color
            self._update_shim_dark_btn_preview()

        if "shimmer_speed" in data and hasattr(self, '_slider_shim'):
            self._slider_shim.blockSignals(True)
            self._slider_shim.setValue(int(data["shimmer_speed"]))
            self._slider_shim.blockSignals(False)
            speed_vals = {1:0.001, 2:0.002, 3:0.004, 4:0.008, 5:0.014}
            lbl = self.findChild(TitleLabel)
            if lbl: lbl._tick_speed = speed_vals.get(int(data["shimmer_speed"]), 0.004)

        if "accent" in data:
            self._theme_accent = h2c(data["accent"])
            self._update_accent_btn_preview()
            c = self._theme_accent
            self.btn_apply.setStyleSheet(f"""
                QPushButton {{ background-color: #0d0d0d;
                               color:rgb({c.red()},{c.green()},{c.blue()}); font-weight:700;
                               border:1px solid rgb({c.red()},{c.green()},{c.blue()});
                               border-radius:8px; padding:5px 14px; font-size:12px; }}
                QPushButton:hover {{ background-color: #141414; border-color: rgb({min(c.red()+40,255)},{min(c.green()+40,255)},{min(c.blue()+40,255)}); }}
                QPushButton:pressed {{ background-color: #0a0a0a; }}
            """)

        if "btn_bg" in data:
            self._btn_color_val = h2c(data["btn_bg"])
            self._update_btn_color_preview()
            c = self._btn_color_val
            new_style = f"""
                QPushButton {{ background-color:rgb({c.red()},{c.green()},{c.blue()});
                               color: #cccccc;
                               border: 1px solid #2a2a2a;
                               border-radius:8px; padding:6px 14px; font-size:13px; font-weight:500; }}
                QPushButton:hover {{ background-color:rgb({min(c.red()+20,255)},{min(c.green()+20,255)},{min(c.blue()+20,255)}); border-color: #444444; }}
                QPushButton:pressed {{ background-color:rgb({max(c.red()-10,0)},{max(c.green()-10,0)},{max(c.blue()-10,0)}); }}
            """
            for btn in [self.btn_add, self.btn_remove, self.btn_duplicate, self.btn_clear,
                        self.btn_import, self.btn_export, self.btn_presets,
                        self.btn_auto, self.btn_kill,
                        self.btn_export_cfg, self.btn_import_cfg, self.btn_open_cfg_folder]:
                btn.setStyleSheet(new_style)
            self._update_auto_styles()

        if "flag_color" in data:
            self._flag_name_color = h2c(data["flag_color"])
            self._btn_flag_color.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:rgb({self._flag_name_color.red()},{self._flag_name_color.green()},{self._flag_name_color.blue()});font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")
        if "value_color" in data:
            self._value_text_color = h2c(data["value_color"])
            self._btn_value_color.setStyleSheet(f"QPushButton{{background:#141414;border:1px solid #2a2a2a;border-radius:8px;color:rgb({self._value_text_color.red()},{self._value_text_color.green()},{self._value_text_color.blue()});font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")

        for key, attr in [("compact","_chk_compact"),("show_type","_chk_show_type"),
                           ("alt_rows","_chk_alt_rows"),("autostart","_chk_autostart"),
                           ("inject_launch","_chk_inject_launch"),("tray_startup","_chk_tray_startup")]:
            if key in data and hasattr(self, attr):
                w = getattr(self, attr)
                w.blockSignals(True)
                w.setChecked(bool(data[key]))
                w.blockSignals(False)
        if "compact" in data:
            self._apply_compact_mode(bool(data["compact"]))
        if "show_type" in data:
            self.table.setColumnHidden(2, not bool(data["show_type"]))
        if "alt_rows" in data:
            self.table.setAlternatingRowColors(bool(data["alt_rows"]))

        if "run_on_boot" in data and hasattr(self, '_chk_run_on_boot'):
            self._chk_run_on_boot.blockSignals(True)
            self._chk_run_on_boot.setChecked(bool(data["run_on_boot"]))
            self._chk_run_on_boot.blockSignals(False)

        if "auto_interval" in data and hasattr(self, '_slider_interval'):
            self._slider_interval.blockSignals(True)
            self._slider_interval.setValue(int(data["auto_interval"]))
            self._slider_interval.blockSignals(False)

        if "binds" in data and hasattr(self, '_binds'):
            _KB_ON  = "QPushButton{background:#001a00;border:1px solid #005500;border-radius:8px;color:#44ff44;font-size:11px;padding:5px 12px;min-width:90px;}"
            _KB_OFF = "QPushButton{background:#111;border:1px solid #1e1e1e;border-radius:8px;color:#555;font-size:11px;padding:5px 12px;min-width:90px;}"
            for k, v in data["binds"].items():
                if k in self._binds:
                    self._binds[k] = v
                    btn = getattr(self, f'_bind_btn_{k}', None)
                    if btn:
                        btn.setText(v if v else "Not set")
                        btn.setStyleSheet(_KB_ON if v else _KB_OFF)
            self._update_hotkeys()

        if "title_full" in data and hasattr(self, '_edit_title') and self._edit_title:
            self._edit_title.blockSignals(True)
            self._edit_title.setText(data["title_full"])
            self._edit_title.blockSignals(False)
        self._update_title_text()

        if "bg_opacity" in data and hasattr(self, '_slider_bg_opacity'):
            self._slider_bg_opacity.blockSignals(True)
            self._slider_bg_opacity.setValue(int(data["bg_opacity"]))
            self._slider_bg_opacity.blockSignals(False)
            self._lbl_bg_opacity.setText(f"{int(data['bg_opacity'])}%")

        if data.get("bg_path") and _os.path.exists(str(data["bg_path"])):
            self._bg_path = data["bg_path"]
            self._lbl_bg_path.setText(_os.path.basename(self._bg_path))
            self._apply_background()
        elif data.get("bg_solid") and data["bg_solid"] != "#0d0d0d":
            c = h2c(data["bg_solid"])
            self._bg_solid_color = c
            self._btn_bg_color.setStyleSheet(f"QPushButton{{background:rgb({c.red()},{c.green()},{c.blue()});border:1px solid #2a2a2a;border-radius:8px;color:#aaaaaa;font-size:12px;padding:5px 12px;}} QPushButton:hover{{border-color:#444;}}")
            self.centralWidget().setStyleSheet(f"border-radius:18px; background:rgb({c.red()},{c.green()},{c.blue()});")

        self._repopulate_with_colors()
        self._set_status("Settings loaded.")
        if "bg_opacity" in data and hasattr(self, '_slider_bg_opacity'):
            self._slider_bg_opacity.setValue(data["bg_opacity"])
        if data.get("bg_path") and __import__('os').path.exists(data["bg_path"]):
            self._bg_path = data["bg_path"]
            self._lbl_bg_path.setText(__import__('os').path.basename(self._bg_path))
            self._apply_background()
        self._repopulate_with_colors()

    def _setup_tray(self):
        """Setup system tray icon and menu — Docker Desktop style."""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            self._tray = None
            return
        self._tray = QSystemTrayIcon(self)
        ico_path = str(__import__('pathlib').Path(__file__).parent.parent / "cr.ico")
        from PyQt6.QtGui import QIcon as _QI
        ico = _QI(ico_path)
        if ico.isNull():
            ico = self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon)
        self._tray.setIcon(ico)
        self._tray.setToolTip("SacredWare")

        tray_menu = QMenu()
        tray_menu.setStyleSheet("""
            QMenu {
                background: #111111;
                border: 1px solid #2a2a2a;
                border-radius: 10px;
                color: #cccccc;
                padding: 6px 4px;
                font-size: 13px;
            }
            QMenu::item {
                padding: 8px 20px 8px 16px;
                border-radius: 6px;
                margin: 1px 4px;
            }
            QMenu::item:selected {
                background: #1e1e1e;
                color: #ffffff;
            }
            QMenu::item:disabled {
                color: #555555;
                background: transparent;
            }
            QMenu::separator {
                background: #2a2a2a;
                height: 1px;
                margin: 4px 8px;
            }
        """)

        act_status = tray_menu.addAction("● SacredWare is running")
        act_status.setEnabled(False)
        tray_menu.addSeparator()

        act_show = tray_menu.addAction("  Show Window")
        act_flags = tray_menu.addAction("  Apply FFlags to Roblox")
        tray_menu.addSeparator()

        self._act_auto = tray_menu.addAction("  Auto Apply FFlags: OFF")
        tray_menu.addSeparator()

        self._act_flag_count = tray_menu.addAction("  0 flags loaded")
        self._act_flag_count.setEnabled(False)
        tray_menu.addSeparator()

        act_settings = tray_menu.addAction("  Open Settings")
        tray_menu.addSeparator()
        act_quit = tray_menu.addAction("  Quit SacredWare")

        act_show.triggered.connect(self._tray_show)
        act_flags.triggered.connect(self._apply_flags)
        self._act_auto.triggered.connect(self._toggle_auto_apply)
        act_settings.triggered.connect(lambda: (self._tray_show(), self._toggle_settings()) if not self.isVisible() else self._toggle_settings())
        act_quit.triggered.connect(self._tray_quit)

        self._tray.setContextMenu(tray_menu)
        self._tray.activated.connect(self._tray_activated)
        self._tray.show()

        self._tray_update_count()

    def _tray_update_count(self):
        """Update flag count shown in tray menu."""
        if hasattr(self, '_act_flag_count'):
            n = len(getattr(self, 'all_flags', {}))
            self._act_flag_count.setText(f"  {n} flag{'s' if n != 1 else ''} loaded")

    def _tray_show(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _tray_quit(self):
        self._tray_really_quit = True
        self._save_app_settings()
        if self.auto_worker:
            try: self.auto_worker.stop()
            except Exception: pass
        if getattr(self, '_tray', None):
            self._tray.hide()
        QApplication.instance().quit()

    def _tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._tray_show()

    def closeEvent(self, event):
        self._save_app_settings()
        if getattr(self, '_tray', None) and not getattr(self, '_tray_really_quit', False):
            event.ignore()
            self.hide()
            if getattr(self, '_tray', None):
                self._tray.showMessage(
                    "SacredWare",
                    "Running in background. Double-click tray icon to reopen.",
                    QSystemTrayIcon.MessageIcon.Information, 2000)
        else:
            if self.auto_worker:
                self.auto_worker.stop()
            event.accept()

    def _apply_startup_behaviors(self):
        """Called 300ms after load — apply auto-start and tray behaviors."""
        if getattr(self, '_chk_autostart', None) and self._chk_autostart.isChecked():
            if not self.state.auto_apply_enabled:
                self._toggle_auto_apply()
        if getattr(self, '_chk_tray_startup', None) and self._chk_tray_startup.isChecked():
            if getattr(self, '_tray', None):
                self.hide()

    def _set_windows_startup(self, enabled: bool):
        """Add/remove app from Windows startup registry."""
        try:
            import winreg, sys as _sys
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE)
            app_path = _sys.executable if getattr(_sys, 'frozen', False) else                        f'"{_sys.executable}" "{__import__("os").path.abspath(__file__)}"'
            if enabled:
                winreg.SetValueEx(key, "sacredware", 0, winreg.REG_SZ, app_path)
                self._set_status("Added to Windows startup.")
            else:
                try:
                    winreg.DeleteValue(key, "sacredware")
                    self._set_status("Removed from Windows startup.")
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            self._set_status(f"Startup registry error: {e}")

    def showEvent(self, event):
        super().showEvent(event)
        self._apply_round_corners()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_round_corners()

    def _apply_round_corners(self):
        from PyQt6.QtGui import QRegion
        radius = 18
        rect = self.rect()
        region = QRegion(rect, QRegion.RegionType.Rectangle)
        tl = QRegion(rect.x(), rect.y(), radius*2, radius*2, QRegion.RegionType.Ellipse)
        tr = QRegion(rect.right()-radius*2+1, rect.y(), radius*2, radius*2, QRegion.RegionType.Ellipse)
        bl = QRegion(rect.x(), rect.bottom()-radius*2+1, radius*2, radius*2, QRegion.RegionType.Ellipse)
        br = QRegion(rect.right()-radius*2+1, rect.bottom()-radius*2+1, radius*2, radius*2, QRegion.RegionType.Ellipse)
        corner_mask = tl.united(tr).united(bl).united(br)
        tl_r = QRegion(rect.x(), rect.y(), radius, radius, QRegion.RegionType.Rectangle)
        tr_r = QRegion(rect.right()-radius+1, rect.y(), radius, radius, QRegion.RegionType.Rectangle)
        bl_r = QRegion(rect.x(), rect.bottom()-radius+1, radius, radius, QRegion.RegionType.Rectangle)
        br_r = QRegion(rect.right()-radius+1, rect.bottom()-radius+1, radius, radius, QRegion.RegionType.Rectangle)
        corners = tl_r.united(tr_r).united(bl_r).united(br_r).subtracted(corner_mask)
        self.setMask(region.subtracted(corners))
        try:
            import ctypes
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                int(self.winId()), 33,
                ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int))
        except Exception:
            pass

    def _tb_mouse_press(self, event):
        from PyQt6.QtCore import Qt as _Qt
        if event.button() == _Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def _tb_mouse_move(self, event):
        from PyQt6.QtCore import Qt as _Qt
        if event.buttons() == _Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def _tb_mouse_release(self, event):
        self._drag_pos = None


class _NoRoundOverride(object):
    """Mixin to prevent style engine from ignoring border-radius."""
    pass

def run_gui(state):
    app = QApplication(sys.argv)
    palette = app.palette()
    from PyQt6.QtGui import QPalette
    palette.setColor(QPalette.ColorRole.Window,        QColor(13, 13, 13))
    palette.setColor(QPalette.ColorRole.WindowText,    QColor(232, 232, 232))
    palette.setColor(QPalette.ColorRole.Base,          QColor(17, 17, 17))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(20, 20, 20))
    palette.setColor(QPalette.ColorRole.Text,          QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Button,        QColor(20, 20, 20))
    palette.setColor(QPalette.ColorRole.ButtonText,    QColor(200, 200, 200))
    palette.setColor(QPalette.ColorRole.Highlight,     QColor(40, 40, 40))
    app.setPalette(palette)
    app.setStyle(RoundedButtonStyle("Windows"))
    from pathlib import Path as _Path
    _ico_path = _Path(__file__).parent.parent / "cr.ico"
    if _ico_path.exists():
        _app_icon = QIcon(str(_ico_path))
        app.setWindowIcon(_app_icon)
    window = MainWindow(state)
    window.show()
    sys.exit(app.exec())
