import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

COLORS = [
    'rgb(201, 167, 57)',
    'rgb(89, 110, 216)',
    'rgb(156, 185, 52)',
    'rgb(161, 95, 211)',
    'rgb(92, 195, 84)',
    'rgb(201, 78, 177)',
    'rgb(79, 142, 44)',
    'rgb(223, 72, 124)',
    'rgb(106, 194, 130)',
    'rgb(207, 72, 51)',
    'rgb(81, 195, 168)',
    'rgb(163, 74, 118)',
    'rgb(64, 141, 78)',
    'rgb(126, 93, 164)',
    'rgb(224, 136, 48)',
    'rgb(104, 141, 206)',
    'rgb(156, 170, 90)',
    'rgb(216, 141, 199)',
    'rgb(51, 125, 92)',
    'rgb(174, 76, 82)',
    'rgb(74, 184, 210)',
    'rgb(156, 95, 43)',
    'rgb(111, 111, 40)',
    'rgb(229, 133, 116)',
    'rgb(207, 160, 106)'
]


def cubes(pos_x, pos_y, pos_z, color, name=None):
    # create points
    x, y, z = np.meshgrid(
        np.linspace(pos_x, pos_x + 1, 2),
        np.linspace(pos_y, pos_y + 1, 2),
        np.linspace(pos_z, pos_z + 1, 2),
    )
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()

    return go.Mesh3d(x=x, y=y, z=z, alphahull=1, flatshading=True, color=color,
                     lighting={'diffuse': 0.1, 'specular': 2.0, 'roughness': 0.5},
                     name=name)


def visualize3d(matrixes):
    fig = make_subplots(rows=len(matrixes), cols=1, subplot_titles=[f"Truck {i + 1}" for i in range(len(matrixes))],
                        specs=[[{'type': 'scatter3d'}] for _ in range(len(matrixes))])

    max_dims = [[len(matrixes[i]), len(matrixes[i][0]), len(matrixes[i][0][0])] for i in range(len(matrixes))]
    for idx, matrix in enumerate(matrixes):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                for k in range(len(matrix[0][0])):
                    if matrix[i][j][k] == 0:
                        continue
                    max_dims[idx][0] = max(max_dims[idx][0], i)
                    max_dims[idx][1] = max(max_dims[idx][1], j)
                    max_dims[idx][2] = max(max_dims[idx][2], k)

        for j in range(len(matrix)):
            for k in range(len(matrix[0])):
                for l in range(len(matrix[0][0])):
                    if matrix[j][k][l] == 0:
                        continue
                    pos_x = j
                    pos_y = k
                    pos_z = l
                    color = COLORS[(matrix[j][k][l] - 1) % len(COLORS)]
                    trace = cubes(pos_x, pos_y, pos_z, color)
                    fig.add_trace(trace, row=idx + 1, col=1)

        invisible_cube = cubes(max_dims[idx][0] - 1, max_dims[idx][1] - 1, max_dims[idx][2] - 1,
                               'rgba(0,0,0,0)', name="invisible_cube")
        fig.add_trace(invisible_cube, row=idx + 1, col=1)

    fig.update_layout(height=600 * len(matrixes), width=800, title_text="Trucks", title_font_size=30)
    # save in a png file

    #random_int = np.random.randint(100000)
    #fig.write_image("images/fig_" + str(random_int) + ".png")
    fig.show()
