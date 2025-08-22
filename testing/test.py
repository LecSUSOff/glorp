from rio import *

class Render(Component):
    clicks: any = 0
    def _on_press(this):
        this.clicks = this.clicks + 1
    def build(this):
        return (Column((Button(("Click me"), on_press = this._on_press)), (Text((f"You clicked the button {this.clicks} time(s)")))))

app = App(build=Render)

app.run_in_window()