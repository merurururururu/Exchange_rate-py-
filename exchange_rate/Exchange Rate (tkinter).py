from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests

API_KEY = "ac60f1e030747f714e5d826f"

class Converter(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        self.base_input = TextInput(hint_text="Base currency (e.g. USD)", multiline=False, size_hint_y=None, height=40)
        self.amount_input = TextInput(hint_text="Amount", multiline=False, input_filter='float', size_hint_y=None, height=40)
        self.targets_input = TextInput(hint_text="Target currencies (comma-separated)", multiline=False, size_hint_y=None, height=40)
        
        self.convert_button = Button(text="Convert", size_hint_y=None, height=50, background_color=(0, 0.5, 0.2, 1))
        self.convert_button.bind(on_press=self.convert_currency)
        
        self.result_label = Label(text="", halign="left", valign="top", size_hint_y=None)
        self.result_label.bind(texture_size=self.update_label_height)

        self.scroll = ScrollView(size_hint=(1, 1))
        self.scroll.add_widget(self.result_label)

        self.add_widget(self.base_input)
        self.add_widget(self.amount_input)
        self.add_widget(self.targets_input)
        self.add_widget(self.convert_button)
        self.add_widget(self.scroll)

    def update_label_height(self, instance, value):
        self.result_label.height = value[1]
        self.result_label.text_size = (self.scroll.width - 20, None)

    def convert_currency(self, instance):
        base = self.base_input.text.strip().upper()
        targets = self.targets_input.text.strip().upper().split(",")
        try:
            amount = float(self.amount_input.text.strip())
        except ValueError:
            self.result_label.text = "❌ Invalid amount."
            return

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base}"
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code != 200 or "conversion_rates" not in data:
                self.result_label.text = "❌ Error: Invalid base currency or API issue."
                return

            rates = data["conversion_rates"]
            output = ""

            # Convert to requested targets
            for target in targets:
                target = target.strip()
                if target in rates:
                    converted = amount * rates[target]
                    output += f"{amount} {base} = {converted:.2f} {target}\n"
                else:
                    output += f"❌ Currency '{target}' not found.\n"

            # Top 5 most valuable currencies
            output += "\n💹 Top 5 exchange rates:\n"
            top_5 = sorted(rates.items(), key=lambda x: -x[1])[:5]
            for currency, rate in top_5:
                output += f"1 {base} = {rate:.2f} {currency}\n"

            self.result_label.text = output

        except Exception as e:
            self.result_label.text = f"❌ Error: {str(e)}"

class CurrencyConverterApp(App):
    def build(self):
        return Converter()

if __name__ == "__main__":
    CurrencyConverterApp().run()
