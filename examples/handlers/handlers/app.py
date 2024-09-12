import asyncio
import random

import httpx

import toga
from toga.constants import COLUMN
from toga.style import Pack


class HandlerApp(toga.App):
    # Button callback functions
    def do_clear(self, widget, **kwargs):
        self.counter = 0
        self.label_1.text = "Ready."
        self.label_2.text = "Ready."
        self.function_label.text = "Ready."
        self.generator_label.text = "Ready."
        self.async_label.text = "Ready."

    def do_function(self, widget, **kwargs):
        """A normal functional handler."""
        # This handler is invoked, and returns immediately
        self.function_label.text = "Here's a random number: {}".format(
            random.randint(0, 100)
        )

    def do_generator(self, widget, **kwargs):
        """A generator-based handler."""
        # The generator yields a number; that number is the number of seconds
        # to yield to the main event loop before processing is resumed.
        widget.enabled = False
        for i in range(1, 10):
            self.generator_label.text = f"Iteration {i}"
            yield 1
        self.generator_label.text = "Ready."
        widget.enabled = True

    async def do_async(self, widget, **kwargs):
        """An async handler."""
        # This handler is integrated with the main event loop; every call to
        # await yields control so that other OS events can be processed.
        widget.enabled = False
        for i in range(1, 10):
            self.async_label.text = f"Iteration {i}"
            await asyncio.sleep(2)
        self.async_label.text = "Ready."
        widget.enabled = True

    async def on_running(self, **kwargs):
        """A task started when the app is running."""
        # This task runs in the background, without blocking the main event loop
        while True:
            self.counter += 1
            self.label_1.text = f"On Running: Iteration {self.counter}"
            await asyncio.sleep(1)

    async def do_background_task(self, **kwargs):
        """A background task."""
        # This task runs in the background, without blocking the main event loop
        while True:
            self.counter += 1
            self.label_2.text = f"Background: Iteration {self.counter}"
            await asyncio.sleep(1)

    async def do_web_get(self, widget, **kwargs):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://jsonplaceholder.typicode.com/posts/{random.randint(0, 100)}"
            )

        payload = response.json()

        self.web_label.text = payload["title"]

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow()

        # Labels to show responses.
        self.label_1 = toga.Label("Ready.", style=Pack(padding=10))
        self.label_2 = toga.Label("Ready.", style=Pack(padding=10))
        self.function_label = toga.Label("Ready.", style=Pack(padding=10))
        self.generator_label = toga.Label("Ready.", style=Pack(padding=10))
        self.async_label = toga.Label("Ready.", style=Pack(padding=10))
        self.web_label = toga.Label("Ready.", style=Pack(padding=10))

        # Add a background task.
        self.counter = 0
        asyncio.create_task(self.do_background_task())

        # Buttons
        btn_style = Pack(flex=1)
        btn_function = toga.Button(
            "Function callback", on_press=self.do_function, style=btn_style
        )
        btn_generator = toga.Button(
            "Generator callback", on_press=self.do_generator, style=btn_style
        )
        btn_async = toga.Button(
            "Async callback", on_press=self.do_async, style=btn_style
        )
        btn_clear = toga.Button("Clear", on_press=self.do_clear, style=btn_style)
        btn_web = toga.Button(
            "Get web content", on_press=self.do_web_get, style=btn_style
        )

        # Outermost box
        box = toga.Box(
            children=[
                self.label_1,
                self.label_2,
                btn_function,
                self.function_label,
                btn_generator,
                self.generator_label,
                btn_async,
                self.async_label,
                btn_web,
                self.web_label,
                btn_clear,
            ],
            style=Pack(flex=1, direction=COLUMN, padding=10),
        )

        # Add the content on the main window
        self.main_window.content = box

        # Show the main window
        self.main_window.show()


def main():
    return HandlerApp("Handlers", "org.beeware.toga.examples.handlers")


if __name__ == "__main__":
    app = main()
    app.main_loop()
