import json


def get_occupancy_report(Correlation_Lawn, Correlation_Lights, Correlation_Car, Correlation_Bin, Correlation_Human):
    data = {
        "Correlation_Lawn": Correlation_Lawn,
        "Correlation_Lights": Correlation_Lights,
        "Correlation_Car": Correlation_Car,
        "Correlation_Bin": Correlation_Bin,
        "Correlation_Human": Correlation_Human
    }
    json_string = json.dumps(data)

    return json_string

