import weather_forecast
import gradio as gr


def get_temp(city):
    weather = weather_forecast.get_weather(config, city)
    return f"Temp: {weather['temp']}"

def get_pressure(city):
    weather = weather_forecast.get_weather(config, city)
    return f"Pressure: {weather['pressure']}"

def get_wind_speed(city):
    weather = weather_forecast.get_weather(config, city)
    return f"Wind Speed: {weather['wind_speed']}"


def enable_buttons(button1):
    return gr.Button(interactive=True)


def initialise_gui():

    with gr.Blocks() as gui:

        with gr.Row():
            input_city_textbox = gr.Textbox(label="City", lines=1)
        with gr.Row():
            temp_button = gr.Button("Temperature", variant="primary", interactive=False)
            pressure_button = gr.Button("Pressure", variant="primary", interactive=False)
            wind_speed_button = gr.Button("Wind Speed", variant="primary", interactive=False)

        with gr.Row():
            output_textbox = gr.Textbox(label="Result", lines=1)

        temp_button.click(fn=get_temp, inputs=input_city_textbox, outputs=output_textbox)
        pressure_button.click(fn=get_pressure, inputs=input_city_textbox, outputs=output_textbox)
        wind_speed_button.click(fn=get_wind_speed, inputs=input_city_textbox, outputs=output_textbox)
        input_city_textbox.change(fn=enable_buttons, inputs= temp_button, outputs= temp_button)

    gui.launch(show_error=True)

if __name__ == '__main__':
    config = weather_forecast.read_config()
    initialise_gui()


