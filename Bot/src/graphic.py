import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


GRAPHIC_SAVE_PATH = "./data/"
TEMPERATURE_KEY = "Temperature"
HUMIDITY_KEY = "Humidity"
RANGE_KEY = "Range"


graph_type_dict = {
    TEMPERATURE_KEY: {"graph_title" : "Température en fonction du temps", "x_label" : "temps", "y_label" : "temperature (°C)"},
    HUMIDITY_KEY : {"graph_title" : "Humidité en fonction du temps", "x_label" : "temps", "y_label" : "taux d'humidité (en %)"},
    RANGE_KEY : {"graph_title" : "Distance en fonction du temps", "x_label" : "temps", "y_label" : "distance (en m)"},
}


def generate_unique_graph(data : list, graph_type : str, save_path : str = GRAPHIC_SAVE_PATH):
    """"""

    current_type_info = graph_type_dict[graph_type]
    fig, ax = plt.subplots()
    ax.plot([x for x in range(len(data))], data)
    ax.set_title(current_type_info["graph_title"])
    ax.set_xlabel(current_type_info["x_label"])
    ax.set_ylabel(current_type_info["y_label"])
    print(graph_type)
    fig.savefig(f"{save_path}{graph_type}_graph.png")


def generate_all_graph(all_data : dict, save_path : str = GRAPHIC_SAVE_PATH):
    """"""
    
    #A is for humidity, B for range and C for temperature:
    fig, axes = plt.subplot_mosaic("AB;CC")
    #Plot humidity data:
    axes["A"].plot([x for x in range(len(all_data[HUMIDITY_KEY]))], all_data[HUMIDITY_KEY])
    axes["A"].set_title(graph_type_dict[HUMIDITY_KEY]["graph_title"])
    axes["A"].set_xlabel(graph_type_dict[HUMIDITY_KEY]["x_label"])
    axes["A"].set_ylabel(graph_type_dict[HUMIDITY_KEY]["y_label"])
    #Plot range data:
    axes["B"].plot([x for x in range(len(all_data[RANGE_KEY]))], all_data[RANGE_KEY])
    axes["B"].set_title(graph_type_dict[RANGE_KEY]["graph_title"])
    axes["B"].set_xlabel(graph_type_dict[RANGE_KEY]["x_label"])
    axes["B"].set_ylabel(graph_type_dict[RANGE_KEY]["y_label"])
    #Plot TEMPERATURE_KEY data:
    axes["C"].plot([x for x in range(len(all_data[TEMPERATURE_KEY]))], all_data[TEMPERATURE_KEY])
    axes["C"].set_title(graph_type_dict[TEMPERATURE_KEY]["graph_title"])
    axes["C"].set_xlabel(graph_type_dict[TEMPERATURE_KEY]["x_label"])
    axes["C"].set_ylabel(graph_type_dict[TEMPERATURE_KEY]["y_label"])

    plt.tight_layout()
    fig.savefig(f"{save_path}all_graph.png")