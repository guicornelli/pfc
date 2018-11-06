import numpy as np
import matplotlib.pyplot as plt
from InfosVariaveisCopia import caracteristicas
# from Tipos import temperature

def sunburst(nodes, total=np.pi * 2, offset=0, level=0, ax=None):
    ax = ax or plt.subplot(111, projection='polar')

    if level == 0 and len(nodes) == 1:
        label, value, subnodes = nodes[0]
        ax.bar([0], [0.5], [np.pi * 2])
        ax.text(0, 0, label, ha='center', va='center')
        sunburst(subnodes, total=value, level=level + 1, ax=ax)
    elif nodes:
        d = np.pi * 2 / total
        labels = []
        widths = []
        local_offset = offset
        for label, value, subnodes in nodes:
            labels.append(label)
            widths.append(value * d)
            sunburst(subnodes, total=total, offset=local_offset,
                     level=level + 1, ax=ax)
            local_offset += value
        values = np.cumsum([offset * d] + widths[:-1])
        heights = [1] * len(nodes)
        bottoms = np.zeros(len(nodes)) + level - 0.5
        rects = ax.bar(values, heights, widths, bottoms, linewidth=1,
                       edgecolor='white', align='edge')
        for rect, label in zip(rects, labels):
            x = rect.get_x() + rect.get_width() / 2
            y = rect.get_y() + rect.get_height() / 2
            rotation = (90 + (360 - np.degrees(x) % 180)) % 360
            ax.text(x, y, label, rotation=rotation, ha='center', va='center')

    if level == 0:
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location('N')
        ax.set_axis_off()

# group_names = ['Temperatura', 'Performance', 'Elétrico', 'Óleo', 'Vibração', 'Disponibilidade', 'Status']
# group_size = [len(temperature), len(performance), len(eletric), len(oil), len(vibration), len(availability),
#              len(status)]

values = [[round((caracteristicas.get('ActivePowerSetpoint_A01').get('max')), 3),
           round((caracteristicas.get('ActivePowerSetpoint_A01').get('max')), 3)],
          [round((caracteristicas.get('ActivePowerSetpoint_A01').get('media')), 3),
           round((caracteristicas.get('ActivePowerSetpoint_A01').get('media')), 3)],
          [round((caracteristicas.get('ActivePowerSetpoint_A01').get('mediamovel')), 3),
           round((caracteristicas.get('ActivePowerSetpoint_A01').get('mediamovel')), 3)],
          [round((caracteristicas.get('ActivePowerSetpoint_A01').get('min')), 3),
           round((caracteristicas.get('ActivePowerSetpoint_A01').get('min')), 3)],
          [(caracteristicas.get('ActivePowerSetpoint_A01').get('tamanho')),
           (caracteristicas.get('ActivePowerSetpoint_A01').get('tamanho'))],
          [round((caracteristicas.get('ActivePowerSetpoint_A01').get('t(s)exec') / 60.0), 3),
           round((caracteristicas.get('ActivePowerSetpoint_A01').get('t(s)exec') / 60.0), 3)]]

rows = ['Max', 'Min', 'Avg', 'M_Avg', 'N_Points', 'T_Calc(m)']

data = [('/', 100, [('home', 70, [('Images', 40, []),
                                  ('Videos', 20, []),
                                  ('Documents', 5, [])]),
                    ('usr', 15,  [('src', 6, []),
                                  ('lib', 4, []),
                                  ('share', 2, []),
                                  ('bin', 1, []),
                                  ('local', 1, []),
                                  ('include', 1, [])])])]

sunburst(data)
plt.show()