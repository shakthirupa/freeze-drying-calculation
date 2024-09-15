from flask import Flask, request, jsonify, render_template, redirect, url_for
import math

app = Flask(__name__)

def calculate_freeze_drying(thickness, initial_moisture, final_moisture, density, latent_heat, heat_input_temp, frozen_juice_temp, thermal_conductivity, pressure, temperature1, temperature2):
    lambda_ = latent_heat * 1000

    # Freeze drying calculation-1
    h = (density * lambda_) / thermal_conductivity
    w = initial_moisture - final_moisture
    g = (thickness ** 2) * w * h * 0.5
    m = heat_input_temp - frozen_juice_temp
    t = g / m
    answer1 = t / 3600  # in hours
    tu = heat_input_temp - frozen_juice_temp
    j = thermal_conductivity * tu
    d = 10**6
    di = d * j
    u = thickness * lambda_
    y = di / u  # in Pa
    o=pressure-y
    efficiency = temperature1 / temperature2 * 100
    results = {
        'time_hours': round(answer1, 2),
        'pressure_pa': round(y, 2),
        'vapour_pressure': round(o, 2),
        'efficiency': round(efficiency, 2)
    }

    return results

def calculate_freeze_drying2(saturation_pressure, sublimation_temp, condenser_temp):
    # Freeze drying calculation-2
    ke = 0.018
    th = sublimation_temp + 273
    n = math.sqrt(th)
    gmax = (saturation_pressure * ke) / n

    uj = gmax * 1000
    uk = uj / 3600  # in KW

    results = {
        'sublimation_rate': round(gmax, 2),
        'power_kw': round(uk, 2),
        'condenser_capacity_l': round(gmax / 1000, 6)
    }

    return results

@app.route('/')
def index():
    return render_template('access.html')

@app.route('/validate_key', methods=['POST'])
def validate_key():
    access_key = request.form['access']
    if access_key == "1431":
        return redirect(url_for('calculator'))
    else:
        return render_template('access.html', error="Invalid Access Key")

@app.route('/calculator')
def calculator():
    return render_template('indeoxi.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        thickness = float(request.form['value1'])
        initial_moisture = float(request.form['value2'])
        final_moisture = float(request.form['value3'])
        density = float(request.form['value4'])
        latent_heat = float(request.form['value5'])
        heat_input_temp = float(request.form['value6'])
        frozen_juice_temp = float(request.form['value7'])
        thermal_conductivity = float(request.form['value8'])
        pressure = float(request.form['pressure'])
        temperature1 = float(request.form['temp'])
        temperature2 = float(request.form['temperature'])

        results = calculate_freeze_drying(thickness, initial_moisture, final_moisture, density, latent_heat, heat_input_temp, frozen_juice_temp, thermal_conductivity, pressure, temperature1, temperature2)
        
        return jsonify(results)
    except Exception as e:
        print(f"Error: {e}")  # Print the error to the console
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/calculation2')
def calculation2():
    return render_template('indexi.html')

@app.route('/calculate2', methods=['POST'])
def calculate2():
    try:
        saturation_pressure = request.form.get('piw')
        sublimation_temp = request.form.get('kl')
        condenser_temp = request.form.get('yi')
        
        if saturation_pressure is None or sublimation_temp is None or condenser_temp is None:
            raise ValueError("Missing form data")
        
        saturation_pressure = float(saturation_pressure)
        sublimation_temp = float(sublimation_temp)
        condenser_temp = float(condenser_temp)
        
        results = calculate_freeze_drying2(saturation_pressure, sublimation_temp, condenser_temp)
        
        return jsonify(results)

    except ValueError as ve:
        print(f"Value Error: {ve}")
        return jsonify({'error': f'Invalid input: {str(ve)}'}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
