import math
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def calculate_freeze_drying(thickness, initial_moisture, final_moisture, density, latent_heat, heat_input_temp, frozen_juice_temp, thermal_conductivity, saturation_pressure, sublimation_temp, condenser_temp):
    lambda_ = latent_heat * 1000
    
    # Freeze drying calculation-1
    h = (density * lambda_) / thermal_conductivity
    w = initial_moisture - final_moisture
    g = (thickness ** 2) * w * h * 0.5
    m = heat_input_temp - frozen_juice_temp
    t = g / m
    answer1 = t / 3600  # in hours

    # Freeze drying calculation-2
    tu = heat_input_temp - frozen_juice_temp
    j = thermal_conductivity * tu
    d = 10**6
    di = d * j
    u = thickness * lambda_
    y = di / u  # in Pa

    # Sublimation rate
    ri = saturation_pressure - y
    efficiency = sublimation_temp / condenser_temp * 100
    
    ke = 0.018
    th = sublimation_temp + 273
    n = math.sqrt(th)
    gmax = (saturation_pressure * ke) / n
    
    uj = gmax * latent_heat
    uk = uj / 3600  # in KW

    results = {
        'time_hours': round(answer1, 2),
        'pressure_pa': round(y, 2),
        'vapour_pressure_ice': round(ri, 2),
        'efficiency_percentage': round(efficiency, 2),
        'sublimation_rate': round(gmax, 2),
        'power_kw': round(uk, 2),
        'condenser_capacity_l': round(gmax / 1000, 2)
    }

    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    thickness = float(request.form['value1'])
    initial_moisture = float(request.form['value2'])
    final_moisture = float(request.form['value3'])
    density = float(request.form['value4'])
    latent_heat = float(request.form['value5'])
    heat_input_temp = float(request.form['value6'])
    frozen_juice_temp = float(request.form['value7'])
    thermal_conductivity = float(request.form['value8'])
    saturation_pressure = float(request.form['piw'])
    sublimation_temp = float(request.form['kl'])
    condenser_temp = float(request.form['yi'])

    results = calculate_freeze_drying(thickness, initial_moisture, final_moisture, density, latent_heat, heat_input_temp, frozen_juice_temp, thermal_conductivity, saturation_pressure, sublimation_temp, condenser_temp)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
